#!/usr/bin/env python3
"""
jungle_events.py — Layer 3.5: jungle-behaviour detector (ganks, lane presence,
invades) computed deterministically from the Riot timeline.

WHY THIS EXISTS
---------------
The jungle research study (docs/research/jungle/) found that the two metrics
everyone coaches junglers with — **gank conversion rate** and **invade success
rate** — are *not measured anywhere in public data*. Riot doesn't track ganks;
no stat site exposes "attempts -> conversions"; the academic literature has no
such dataset. So we compute them ourselves from timeline events + positions.

HONESTY CONTRACT (read before trusting a number)
------------------------------------------------
Riot's timeline samples player positions only **once per minute**
(participantFrames) outside of kill/objective events. That has consequences:

* **Converted ganks are measured** (high confidence): a CHAMPION_KILL where an
  enemy jungler participated and the victim died in their own lane.
* **Failed ganks are NOT directly observable** (low confidence): with 1/min
  sampling we can only see "the jungler was in this lane at a sampled minute".
  A visit with no kill nearby is a *proxy* for an attempt, not evidence of one.
  Every such figure is labelled and must be hedged by the coach.
* **Invades** are inferred from the jungler being in the enemy half; the window
  is bounded by the sampling interval, so durations are approximate (±1 min).

Nothing here is guessed: every field derives from an event or a snapshot.
Do not present `*_proxy` fields as measured.

Usage:
    python jungle_events.py --raw-dir data/raw --match NA1_1234567890
    from jungle_events import detect
    je = detect(board)
"""

import argparse
import json
import os

import board as board_mod

# --- role / lane mapping ----------------------------------------------------

# teamPosition -> the lane that role occupies. Both bot-lane roles map to "bot".
LANE_FOR_ROLE = {
    "TOP": "top",
    "MIDDLE": "mid",
    "BOTTOM": "bot",
    "UTILITY": "bot",
    "MID": "mid",       # some payloads use short forms
    "BOT": "bot",
    "ADC": "bot",
    "SUPPORT": "bot",
}

LANES = ("top", "mid", "bot")

# How long after a sampled lane visit we still credit a kill to that visit.
VISIT_KILL_WINDOW_MIN = 1.5


def _is_jungler(players, pid):
    return bool(players.get(pid, {}).get("has_smite"))


def _half(x, y):
    """Which half of the map a point is in ('blue' bottom-left / 'red' top-right)."""
    if x is None or y is None:
        return None
    return "blue" if (x + y) < 14800 else "red"


def _team_half(team):
    return {100: "blue", 200: "red"}.get(team)


def _kills(board):
    return [e for e in board["events"] if e["type"] == "CHAMPION_KILL"]


def _junglers(board):
    return {pid: pl for pid, pl in board["players"].items() if pl.get("has_smite")}


# --- ganks ------------------------------------------------------------------

def detect_ganks(board):
    """Converted ganks: kills in a lane where a jungler participated.

    A gank is recorded when (a) the victim is a lane-role player, (b) they died
    inside their own lane, and (c) at least one enemy-team jungler killed or
    assisted. `counter_gank` marks kills where both teams' junglers showed up.
    """
    players = board["players"]
    out = []
    for ev in _kills(board):
        victim = players.get(ev.get("victim"))
        if not victim:
            continue
        vrole = victim.get("role")
        if vrole not in LANE_FOR_ROLE:
            continue
        vlan = board_mod._lane(ev.get("x"), ev.get("y"))
        if vlan != LANE_FOR_ROLE[vrole]:
            continue  # died outside their lane -> not a gank on them

        involved = []
        if ev.get("killer") is not None:
            involved.append(ev["killer"])
        involved.extend(ev.get("assists") or [])

        attackers = [p for p in involved if players.get(p, {}).get("team") != victim["team"]]
        atk_junglers = [p for p in attackers if _is_jungler(players, p)]
        if not atk_junglers:
            continue  # a solo lane kill, not a gank

        def_team = victim["team"]
        def_junglers = [p for p in involved if players.get(p, {}).get("team") == def_team
                        and _is_jungler(players, p)]

        ganker = players[atk_junglers[0]]
        out.append({
            "min": ev["min"],
            "lane": vlan,
            "ganker_team": ganker["team"],
            "ganker_champion": ganker["champion"],
            "victim_champion": victim["champion"],
            "victim_role": vrole,
            "counter_gank": bool(def_junglers),
            # kill happened on the victim's own half => they were pushed up
            # (covers dives and over-extension; not proof of a tower dive)
            "on_victim_side": _half(ev.get("x"), ev.get("y")) == _team_half(def_team),
            "participants": len(attackers),
        })
    return out


# --- lane presence (gank attempts, proxy) -----------------------------------

def detect_lane_visits(board):
    """Sampled moments a jungler was standing in a lane it doesn't own.

    PROXY ONLY. With 1/minute sampling this is evidence of *presence*, not proof
    of a gank attempt. `kill_within_window` marks whether a kill then happened in
    that same lane shortly after — a conversion signal, not a full attempt count.
    """
    players = board["players"]
    kills = _kills(board)
    visits = []

    for jid, jpl in _junglers(board).items():
        last = None  # (lane, start_min) of the run in progress
        for snap in board["snapshots"]:
            ps = snap["players"].get(jid)
            if not ps:
                continue
            lane = board_mod._lane(ps.get("x"), ps.get("y"))
            if lane in LANES:
                if last and last[0] == lane:
                    last = (lane, last[1])  # extend run, keep original start
                else:
                    last = (lane, snap["min"])
            else:
                if last:
                    visits.append(_finish_visit(board, jid, last, kills))
                    last = None
        if last:
            visits.append(_finish_visit(board, jid, last, kills))
    return visits


def _finish_visit(board, jid, run, kills):
    lane, start = run
    jpl = board["players"][jid]
    near = [
        k for k in kills
        if k["min"] >= start and k["min"] <= start + VISIT_KILL_WINDOW_MIN
        and board_mod._lane(k.get("x"), k.get("y")) == lane
        and (k.get("killer") == jid or jid in (k.get("assists") or []))
    ]
    return {
        "min": start,
        "lane": lane,
        "jungler_champion": jpl["champion"],
        "jungler_team": jpl["team"],
        "kill_within_window": bool(near),
        "kills": len(near),
    }


# --- invades ----------------------------------------------------------------

def detect_invades(board):
    """Windows where a jungler was in the ENEMY half's jungle or river.

    Consecutive sampled minutes are merged into one window. Outcome is read from
    kills in that window: kills the jungler participated in (success) and deaths
    of the jungler (failed invade). Durations are approximate (±1 min sampling).
    """
    players = board["players"]
    kills = _kills(board)
    out = []

    for jid, jpl in _junglers(board).items():
        my_half = _team_half(jpl["team"])
        run = None  # list of minutes
        windows = []
        for snap in board["snapshots"]:
            ps = snap["players"].get(jid)
            if not ps:
                continue
            x, y = ps.get("x"), ps.get("y")
            h = _half(x, y)
            lane = board_mod._lane(x, y)
            # Only the jungle and river quadrants count (river buckets to
            # "jungle" in _lane). Lanes are excluded by construction.
            in_enemy_jungle = (h is not None and h != my_half and lane == "jungle")
            if in_enemy_jungle:
                if run and snap["min"] - run[-1] <= 1.1:
                    run.append(snap["min"])
                else:
                    if run:
                        windows.append(run)
                    run = [snap["min"]]
            else:
                if run:
                    windows.append(run)
                    run = None
        if run:
            windows.append(run)

        for w in windows:
            start, end = w[0], w[-1]
            involved_kills = [
                k for k in kills
                if start <= k["min"] <= end + 0.5
                and (k.get("killer") == jid or jid in (k.get("assists") or []))
            ]
            died = any(k["min"] >= start and k["min"] <= end + 0.5 and k.get("victim") == jid
                       for k in kills)
            out.append({
                "start_min": start,
                "end_min": end,
                "duration_min": round(end - start, 1),
                "jungler_champion": jpl["champion"],
                "jungler_team": jpl["team"],
                "kills": len(involved_kills),
                "died": died,
            })
    return out


# --- top level --------------------------------------------------------------

def detect(board):
    """Run every detector and summarise both junglers' games."""
    players = board["players"]
    me_team = players[board["me_id"]]["team"]
    enemy_team = 300 - me_team

    ganks = detect_ganks(board)
    visits = detect_lane_visits(board)
    invades = detect_invades(board)

    def side(team):
        g = [k for k in ganks if k["ganker_team"] == team]
        v = [x for x in visits if x["jungler_team"] == team]
        iv = [x for x in invades if x["jungler_team"] == team]
        return {
            "gank_kills": len(g),
            "ganks_on_lanes": sorted({k["lane"] for k in g}),
            "lane_visits_proxy": len(v),
            "visits_with_kill_proxy": sum(1 for x in v if x["kill_within_window"]),
            "invade_windows": len(iv),
            "invade_kills": sum(x["kills"] for x in iv),
            "invade_deaths": sum(1 for x in iv if x["died"]),
        }

    return {
        "ganks": ganks,
        "lane_visits": visits,
        "invades": invades,
        "summary": {"me": side(me_team), "enemy_jungler": side(enemy_team)},
        "caveat": ("Converted ganks and invade windows are measured. Lane-visit "
                   "counts are a PROXY for attempts: Riot samples positions only "
                   "once per minute, so failed ganks are not directly observable. "
                   "Never present proxy fields as measured."),
    }


# --- CLI --------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description="Detect ganks/invades from a timeline.")
    ap.add_argument("--raw-dir", default="data/raw")
    ap.add_argument("--match", required=True)
    ap.add_argument("--puuid", help="your puuid (defaults to first participant)")
    ap.add_argument("--summary", action="store_true", help="print only the summary")
    args = ap.parse_args()

    with open(os.path.join(args.raw_dir, f"{args.match}.match.json")) as f:
        match = json.load(f)
    with open(os.path.join(args.raw_dir, f"{args.match}.timeline.json")) as f:
        tl = json.load(f)
    puuid = args.puuid or match["metadata"]["participants"][0]

    b = board_mod.extract_board(match, tl, puuid)
    res = detect(b)
    print(json.dumps(res["summary"] if args.summary else res, indent=2, default=str))


if __name__ == "__main__":
    main()
