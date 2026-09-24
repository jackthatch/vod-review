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

# Friendly display names for objective monster enums, so the coach/UI say
# "Void Grubs" rather than the raw enum "HORDE".
MONSTER_NAMES = {
    VOID_GRUBS: "Void Grubs",
    DRAGON: "Dragon",
    RIFT_HERALD: "Rift Herald",
    BARON: "Baron Nashor",
    ATKHAN: "Atakhan",
    ELDER: "Elder Dragon",
}
DRAGON_SUB_NAMES = {
    "EARTH_DRAGON": "Earth Drake",
    "FIRE_DRAGON": "Fire Drake",
    "WATER_DRAGON": "Ocean Drake",
    "AIR_DRAGON": "Cloud Drake",
    "HEXTECH_DRAGON": "Hextech Drake",
    "CHEMTECH_DRAGON": "Chemtech Drake",
}


def monster_label(monster, sub=None):
    """Human-friendly objective name; prefers the dragon sub-type when present."""
    if sub and sub in DRAGON_SUB_NAMES:
        return DRAGON_SUB_NAMES[sub]
    return MONSTER_NAMES.get(monster, monster or "objective")

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

# Named Summoner's Rift landmarks (approximate map units, map 11). Blue side
# sits bottom-left, red side top-right; the map is ~symmetric under a 180°
# rotation. Used to give human-readable locations ("at your red buff") instead
# of raw coordinates, which mean nothing to a player.
LANDMARKS = [
    ("fountain", 400, 400, "blue"),
    ("blue buff", 3900, 7900, "blue"),
    ("gromp", 2100, 8400, "blue"),
    ("wolves", 3800, 6500, "blue"),
    ("raptors", 7000, 5450, "blue"),
    ("red buff", 7800, 4050, "blue"),
    ("krugs", 8400, 2800, "blue"),
    ("fountain", 14400, 14400, "red"),
    ("blue buff", 10920, 6980, "red"),
    ("gromp", 12720, 6480, "red"),
    ("wolves", 11020, 8380, "red"),
    ("raptors", 7820, 9430, "red"),
    ("red buff", 7020, 10830, "red"),
    ("krugs", 6420, 12080, "red"),
    ("Baron pit", 4993, 10461, "neutral"),
    ("Dragon pit", 9866, 4414, "neutral"),
]

# How close (map units) a point must be to a landmark to take its name.
LANDMARK_RADIUS = 1700


def _owner_prefix(owner, my_team):
    if owner == "neutral" or my_team is None:
        return ""
    same = (owner == "blue" and my_team == 100) or (owner == "red" and my_team == 200)
    return "your " if same else "enemy "


def location_label(x, y, my_team=None):
    """Human-readable map location for a point (e.g. 'at your red buff').

    Returns None when we can't place it. Landmarks are approximate, so this is a
    best-effort label, not a precise read.
    """
    if x is None or y is None:
        return None

    best = None
    for name, lx, ly, owner in LANDMARKS:
        d = math.hypot(x - lx, y - ly)
        if best is None or d < best[0]:
            best = (d, name, owner)
    if best and best[0] <= LANDMARK_RADIUS:
        _, name, owner = best
        return f"at {_owner_prefix(owner, my_team)}{name}"

    lane = _lane(x, y)
    if lane == "top":
        return "in top lane"
    if lane == "bot":
        return "in bot lane"
    if lane == "mid":
        return "in mid lane"
    if lane == "base":
        return "in your base" if my_team == 100 else "in the enemy base"
    if lane == "enemy_base":
        return "in your base" if my_team == 200 else "in the enemy base"
    # jungle vs river: the river runs along the anti-diagonal
    if abs(x + y - 14820) < 1600:
        return "in the river"
    my_half = {100: "blue", 200: "red"}.get(my_team)
    half = "blue" if math.hypot(x - 400, y - 400) < math.hypot(x - 14400, y - 14400) else "red"
    if my_half is None:
        return f"in the {half} jungle"
    return "in your jungle" if half == my_half else "in the enemy jungle"

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
        d_baron = _dist({"x": x, "y": y}, OBJECTIVE_POS[BARON])
        d_dragon = _dist({"x": x, "y": y}, OBJECTIVE_POS[DRAGON])
        player_status.append({
            "participant_id": pid,
            "champion": pl["champion"],
            "team": pl["team"],
            "role": pl["role"],
            "is_me": pl["is_me"],
            "lane": _lane(x, y),
            "location": location_label(x, y, me_team),
            "x": x, "y": y,
            "gold": ps.get("gold"),
            "level": lvl,
            "fed": pid in fed,
            "has_tp": pl["has_tp"],
            "likely_dead": likely_dead,
            "last_death_min": last_death,
            "near_baron": d_baron is not None and d_baron <= 3500,
            "near_dragon": d_dragon is not None and d_dragon <= 3500,
        })

    return {
        "minute": minute,
        "gold_diff": gold_diff,          # + = my team ahead
        "dragon_counts": dragon_counts,  # {teamId: soul points}
        "objectives": objectives,        # last-taken state of each objective
        "players": player_status,
    }


# --- objective contest context --------------------------------------------

CONTEST_RADIUS = 3500  # map units — "near the pit" for presence counting


def proximity_label(d):
    """Human-friendly distance-to-objective bucket (replaces raw map units)."""
    if d is None:
        return "unknown"
    if d <= 800:
        return "in the pit"
    if d <= 1500:
        return "at the pit entrance"
    if d <= 3000:
        return "in the river nearby"
    return "across the map"


def contest_context(board, monster, minute, radius=CONTEST_RADIUS):
    """Deterministic read of who was at the objective pit when it was taken.

    Distinguishes "we contested and lost" from "we conceded" (few allies near),
    and surfaces the stakes (gold diff, dragon soul point, who was alive) so the
    coach can judge whether letting the objective go was actually correct.

    All fields are computed from the board — nothing is guessed.
    """
    snap = _snap_at(board, minute)
    players = board["players"]
    me_id = board["me_id"]
    me_team = players[me_id]["team"]
    enemy_team = 300 - me_team
    pit = OBJECTIVE_POS.get(monster)
    deaths = _death_times(board)
    game_min = board["duration_min"]

    allies_near = enemies_near = 0
    allies_alive = enemies_alive = 0
    ally_lanes = []

    for pid in sorted(players):
        pl = players[pid]
        ps = (snap["players"].get(pid) if snap else None) or {}
        last_death = deaths.get(pid)
        respawn = _respawn_estimate(ps.get("level") or 9, game_min) / 60.0
        alive = last_death is None or (minute - last_death) >= respawn
        if not alive:
            continue
        if pl["team"] == me_team:
            allies_alive += 1
            ally_lanes.append(_lane(ps.get("x"), ps.get("y")))
        else:
            enemies_alive += 1
        d = _dist(ps, pit) if pit else None
        if d is not None and d <= radius:
            if pl["team"] == me_team:
                allies_near += 1
            else:
                enemies_near += 1

    my_ps = (snap["players"].get(me_id) if snap else None) or {}
    me_dist = _dist(my_ps, pit) if pit else None
    me_location = location_label(my_ps.get("x"), my_ps.get("y"), me_team)

    gold = {100: 0, 200: 0}
    if snap:
        for pid, ps in snap["players"].items():
            gold[players[pid]["team"]] += ps.get("gold") or 0
    gold_diff = gold.get(me_team, 0) - gold.get(enemy_team, 0)

    # Dragon soul stakes: is this the enemy's 4th dragon (soul point)?
    enemy_dragons = 0
    for ev in board["events"]:
        if (ev["type"] == "ELITE_MONSTER_KILL" and ev["min"] < minute
                and ev.get("monster") == DRAGON and ev.get("team") == enemy_team):
            enemy_dragons += 1
    dragon_number = enemy_dragons + 1 if monster == DRAGON else None
    soul_point = monster == DRAGON and enemy_dragons == 3

    return {
        "me_location": me_location,
        "me_proximity": proximity_label(me_dist),
        "allies_near": allies_near,
        "enemies_near": enemies_near,
        "allies_alive": allies_alive,
        "enemies_alive": enemies_alive,
        "ally_lanes": ally_lanes,
        "gold_diff": gold_diff,
        "dragon_number": dragon_number,
        "soul_point": soul_point,
        "team_committed": allies_near >= 2,
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
