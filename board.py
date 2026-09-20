#!/usr/bin/env python3
"""
board.py — full-board game-state extractor (Layer 1 of the coach pipeline).

Ingests raw Riot match + timeline and produces a complete, timestamped board
state: every player's identity, position, gold, level and items across every
frame, plus the full event stream (kills, objectives, buildings, item purchases,
wards). The existing fetch_match.condense() only keeps "you"; this keeps everyone,
which is what game-state reasoning needs (e.g. "Baron with your TP toplaner in the
side wave is fine; Baron while your fed ADC is stuck in a side wave is not").

Also provides situation_at() — a timestamp -> concise fact-sheet that grounds the
LLM coach (Layer 2). All facts are computed deterministically; nothing is guessed.

NOTE: built against the documented MATCH-V5 schema. Needs a one-time smoke test
against a real timeline to confirm field names (run fetch_match.py --count 1 to
produce raw data, then `python board.py <raw-timeline>` — see `--help`).
"""

import argparse
import json
import math

# --- constants -------------------------------------------------------------

# Summoner spell IDs (Data Dragon).
SUMMONER_SPELLS = {
    1: "Cleanse", 3: "Exhaust", 4: "Flash", 6: "Ghost", 7: "Heal",
    11: "Smite", 12: "Teleport", 14: "Ignite", 21: "Barrier",
}

FLASH_ID, TELEPORT_ID, SMITE_ID = 4, 12, 11

# Objective monster types (timeline `monsterType`).
BARON = "BARON_NASHOR"
DRAGON = "DRAGON"
RIFT_HERALD = "RIFTHERALD"
VOID_GRUBS = "HORDE"
ATKHAN = "ATKHAN"
ELDER = "ELDER_DRAGON"

# Approximate map-center coordinates of the major objective pits (map units).
# Best-effort: used only to compute "how far is X from the objective".
OBJECTIVE_POS = {
    BARON: {"x": 4993, "y": 10461},
    DRAGON: {"x": 9866, "y": 4414},
    RIFT_HERALD: {"x": 4993, "y": 10461},  # herald spawns in baron pit (pre-20)
    VOID_GRUBS: {"x": 6652, "y": 9690},
    ATKHAN: {"x": 8184, "y": 6608},
    ELDER: {"x": 9866, "y": 4414},
}

# --- extraction ------------------------------------------------------------


def _norm_event(ev):
    """Normalize a raw timeline event into a compact, typed dict."""
    t = ev["timestamp"] / 60000.0  # minutes
    pos = ev.get("position", {})
    e = {
        "min": round(t, 1),
        "type": ev["type"],
        "x": pos.get("x"),
        "y": pos.get("y"),
    }
    et = ev["type"]
    if et == "CHAMPION_KILL":
        e.update({
            "killer": ev.get("killerId"),
            "victim": ev.get("victimId"),
            "assists": ev.get("assistingParticipantIds", []),
        })
    elif et == "CHAMPION_SPECIAL_KILL":
        e.update({"killer": ev.get("killerId"), "kill_type": ev.get("killType")})
    elif et == "ELITE_MONSTER_KILL":
        e.update({
            "monster": ev.get("monsterType"),
            "sub": ev.get("monsterSubType"),
            "team": ev.get("killerTeamId"),
            "killer": ev.get("killerId"),
        })
    elif et == "BUILDING_KILL":
        e.update({
            "building": ev.get("buildingType"),
            "tower": ev.get("towerType"),
            "lane": ev.get("laneType"),
            "team": ev.get("teamId"),
            "killer": ev.get("killerId"),
        })
    elif et in ("ITEM_PURCHASED", "ITEM_DESTROYED", "ITEM_SOLD", "ITEM_UNDO"):
        e.update({"participant": ev.get("participantId"), "item_id": ev.get("itemId")})
    elif et == "WARD_PLACED":
        e.update({"participant": ev.get("creatorId"), "ward": ev.get("wardType")})
    elif et == "WARD_KILLED":
        e.update({"participant": ev.get("killerId"), "ward": ev.get("wardType")})
    elif et == "LEVEL_UP":
        e.update({"participant": ev.get("participantId"), "level": ev.get("level")})
    elif et == "SKILL_LEVEL_UP":
        e.update({"participant": ev.get("participantId"), "skill": ev.get("skillSlot")})
    return e


def extract_board(match, timeline, puuid):
    """Turn raw match + timeline into a full-board dict.

    `match`    : the MATCH-V5 /matches/{id} JSON
    `timeline` : the MATCH-V5 /matches/{id}/timeline JSON
    `puuid`    : the summoner we care about (marks `is_me`)
    """
    info = match["info"]
    participants = info["participants"]
    me = next(p for p in participants if p["puuid"] == puuid)

    ti = timeline["info"]
    frame_interval = ti.get("frameInterval", 60000)
    frames = ti.get("frames", [])

    # roster: one entry per participant (1..10)
    players = {}
    for p in participants:
        s1, s2 = p.get("summoner1Id"), p.get("summoner2Id")
        sums = {s1, s2}
        players[p["participantId"]] = {
            "champion": p["championName"],
            "team": p["teamId"],
            "role": (p.get("teamPosition") or p.get("individualPosition")
                     or p.get("lane") or "?"),
            "is_me": p["puuid"] == puuid,
            "summoners": [s1, s2],
            "has_flash": FLASH_ID in sums,
            "has_tp": TELEPORT_ID in sums,
            "has_smite": SMITE_ID in sums,
        }

    # events: embedded per-frame in the current API, top-level in older responses
    raw_events = ti.get("events")
    if raw_events is None:
        raw_events = []
        for f in frames:
            raw_events.extend(f.get("events", []))
    events = [_norm_event(ev) for ev in raw_events]

    # snapshots: every frame, every player
    snapshots = []
    for i, f in enumerate(frames):
        fp = {}
        for pid_str, pf in f.get("participantFrames", {}).items():
            pid = int(pid_str)
            fp[pid] = {
                "x": pf["position"]["x"],
                "y": pf["position"]["y"],
                "gold": pf.get("totalGold"),
                "unspent": pf.get("currentGold"),
                "level": pf.get("level"),
                "xp": pf.get("xp"),
                "cs": (pf.get("minionsKilled", 0) + pf.get("jungleMinionsKilled", 0)),
            }
        snapshots.append({
            "min": round(i * frame_interval / 60000.0, 1),
            "players": fp,
        })

    return {
        "match_id": match["metadata"]["matchId"],
        "duration_min": round(frame_interval * len(frames) / 60000.0, 1),
        "frame_interval": frame_interval,
        "me_id": me["participantId"],
        "players": players,
        "snapshots": snapshots,
        "events": events,
    }


# --- situation builder (Layer 2 seed) -------------------------------------


def _snap_at(board, minute):
    best = None
    for s in board["snapshots"]:
        if s["min"] <= minute:
            best = s
        else:
            break
    return best


def _lane(x, y):
    """Best-effort lane bucket from map coordinates (approximate)."""
    if x is None or y is None:
        return "unknown"
    # map is roughly 14820 x 14880, rotated 45deg. Coarse heuristics only.
    if y > 11500 and x < 9000:
        return "top"
    if y < 3300 and x > 5800:
        return "bot"
    if x < 1500 or y < 1500:
        return "base"
    if x > 13300 or y > 13300:
        return "enemy_base"
    if 3000 < x < 11800 and abs(x - y) < 2600:
        return "mid"
    return "jungle"


def _respawn_estimate(level, game_min):
    """Rough respawn seconds (level-scaled, capped by late-game ramp)."""
    base = 6 + max(level, 1) * 2.5
    late = min(20, game_min * 0.3)  # late-game deaths are longer
    return min(60.0, base + late)


def _death_times(board):
    """Last death minute for each participant."""
    deaths = {}
    for ev in board["events"]:
        if ev["type"] == "CHAMPION_KILL" and ev.get("victim") is not None:
            deaths[ev["victim"]] = ev["min"]
    return deaths


def _dist(a, b):
    if None in (a.get("x"), a.get("y"), b.get("x"), b.get("y")):
        return None
    return math.hypot(a["x"] - b["x"], a["y"] - b["y"])


def situation_at(board, minute):
    """Emit a concise, deterministic fact-sheet of the game state at `minute`.

    Returns a dict with: time, gold diff, objective status, and a per-player
    status list (alive/dead, lane, gold, level, fed, has_tp, distance to Baron
    and Dragon). This is the grounding context for the LLM coach.
    """
    snap = _snap_at(board, minute)
    players = board["players"]
    me_team = players[board["me_id"]]["team"]
    game_min = board["duration_min"]

    # team totals + gold diff from the snapshot
    gold = {100: 0, 200: 0}
    if snap:
        for pid, ps in snap["players"].items():
            team = players[pid]["team"]
            gold[team] += ps.get("gold") or 0
    my_gold, en_gold = gold.get(me_team, 0), gold.get(300 - me_team, 0)
    gold_diff = my_gold - en_gold

    # objective status: last elite kill per type up to `minute`, + dragon counts
    objectives = {}
    dragon_counts = {100: 0, 200: 0}
    for ev in board["events"]:
        if ev["type"] != "ELITE_MONSTER_KILL" or ev["min"] > minute:
            continue
        m = ev.get("monster")
        team = ev.get("team")
        if m == DRAGON or m == ELDER:
            if team in dragon_counts:
                dragon_counts[team] += 1
        if m:
            objectives[m] = {
                "last_taken_min": ev["min"],
                "team": team,
                "sub": ev.get("sub"),
            }

    # per-player status
    death_times = _death_times(board)
    # "fed" = top 3 players by gold at this snapshot
    fed = set()
    if snap:
        ranked = sorted(
            ((pid, ps.get("gold") or 0) for pid, ps in snap["players"].items()),
            key=lambda kv: kv[1], reverse=True,
        )
        fed = {pid for pid, _ in ranked[:3]}

    player_status = []
    for pid in sorted(players):
        pl = players[pid]
        ps = (snap["players"].get(pid) if snap else None) or {}
        x, y = ps.get("x"), ps.get("y")
        lvl = ps.get("level")
        last_death = death_times.get(pid)
        respawn = _respawn_estimate(lvl or 9, game_min) / 60.0
        likely_dead = (last_death is not None and (minute - last_death) < respawn)
        player_status.append({
            "participant_id": pid,
            "champion": pl["champion"],
            "team": pl["team"],
            "role": pl["role"],
            "is_me": pl["is_me"],
            "lane": _lane(x, y),
            "x": x, "y": y,
            "gold": ps.get("gold"),
            "level": lvl,
            "fed": pid in fed,
            "has_tp": pl["has_tp"],
            "likely_dead": likely_dead,
            "last_death_min": last_death,
            "dist_baron": _dist({"x": x, "y": y}, OBJECTIVE_POS[BARON]),
            "dist_dragon": _dist({"x": x, "y": y}, OBJECTIVE_POS[DRAGON]),
        })

    return {
        "minute": minute,
        "gold_diff": gold_diff,          # + = my team ahead
        "dragon_counts": dragon_counts,  # {teamId: soul points}
        "objectives": objectives,        # last-taken state of each objective
        "players": player_status,
    }


# --- CLI -------------------------------------------------------------------


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("timeline_json", nargs="?", help="raw MATCH-V5 timeline JSON")
    ap.add_argument("match_json", nargs="?", help="raw MATCH-V5 match JSON")
    ap.add_argument("--puuid", help="your puuid (marks is_me)")
    ap.add_argument("--at", type=float, default=20.0,
                    help="minute to build the situation fact-sheet at")
    args = ap.parse_args()

    if not (args.timeline_json and args.match_json):
        ap.error("need both <timeline_json> and <match_json>")

    with open(args.timeline_json) as f:
        tl = json.load(f)
    with open(args.match_json) as f:
        match = json.load(f)

    if not args.puuid:
        args.puuid = match["info"]["participants"][0]["puuid"]

    board = extract_board(match, tl, args.puuid)
    print(json.dumps(board, indent=2)[:2000], "...\n")
    print("--- situation at %.1fmin ---" % args.at)
    print(json.dumps(situation_at(board, args.at), indent=2))


if __name__ == "__main__":
    main()
