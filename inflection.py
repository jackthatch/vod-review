#!/usr/bin/env python3
"""
inflection.py — flag inflection points (Layer 3 of the coach pipeline).

Where `moments.py` flags *outcomes* (you died, they got the objective),
`inflection.py` flags *decisions*: the instant a contest started, when a
teamfight broke out, when you rotated across the map, when you recalled to buy.

These run on the FULL board (board.extract_board), not the "me-only" condensed
story, because a decision only makes sense in context of all 10 players.

This is the deterministic detection layer that grounds the LLM coach (Layer 4):
each inflection point is a timestamp the coach can resolve with
`board.situation_at(t)` to answer "what was the state, was this the right call?".

Usage:
    python inflection.py <timeline.json> <match.json> [--puuid ...] [--json]

Detectors (all deterministic):
    - objective_contest — >= N champions converged on a live objective pit before
                          it was secured (the *start* of the fight, not the end)
    - teamfight        — a kill with >= N assists (a multi-champ engagement)
    - rotation         — you crossed a lane boundary in a single frame (cross-map)
    - recall_buy       — you were in base while spending >= N gold (a shop trip)
"""

import argparse
import json
import math

from board import OBJECTIVE_POS, _dist, _lane, monster_label


# --- detectors -------------------------------------------------------------


def detect_objective_contests(board, radius=3500, min_players=4, lookback_min=1.5):
    """The moment >= min_players converged on an objective pit shortly before it
    was secured. Captures when the contest *started*, not who won it."""
    inflections = []
    snaps = board["snapshots"]
    for ev in board["events"]:
        if ev["type"] != "ELITE_MONSTER_KILL":
            continue
        monster = ev.get("monster")
        pit = OBJECTIVE_POS.get(monster)
        if not pit:
            continue
        kill_min = ev["min"]
        start = None
        for s in snaps:
            if s["min"] < kill_min - lookback_min:
                continue
            if s["min"] > kill_min:
                break
            near = 0
            for ps in s["players"].values():
                d = _dist(ps, pit)
                if d is not None and d <= radius:
                    near += 1
            if near >= min_players:
                start = s["min"]
                break
        if start is not None and start < kill_min:
            inflections.append({
                "type": "objective_contest",
                "min": start,
                "objective": monster,
                "sub": ev.get("sub"),
                "secured_by": ev.get("team"),
                "secured_min": kill_min,
                "score": 2500,
                "detail": (f"{monster_label(monster, ev.get('sub'))} contest began "
                           f"at {start}min (>={min_players} champions at the pit), "
                           f"secured by team {ev.get('team')} at {kill_min}min"),
            })
    return inflections


def detect_teamfights(board, min_assists=2):
    """A kill with >= min_assists assistants — a multi-champion engagement."""
    inflections = []
    for ev in board["events"]:
        if ev["type"] != "CHAMPION_KILL":
            continue
        assists = ev.get("assists") or []
        if len(assists) >= min_assists:
            involved = len(assists) + 2  # killer + victim + assistants
            inflections.append({
                "type": "teamfight",
                "min": ev["min"],
                "participants": involved,
                "score": 1500 + 100 * len(assists),
                "detail": (f"teamfight at {ev['min']}min "
                           f"({involved} champions involved)"),
            })
    return inflections


def detect_rotations(board, me_id=None, min_dist=5000):
    """You crossed a lane boundary in one frame interval (a cross-map move).

    Base trips are excluded — going to base to shop is a recall (handled by
    detect_recalls), not a tactical rotation. Only lane<->lane and lane<->jungle
    moves count."""
    if me_id is None:
        me_id = board["me_id"]
    inflections = []
    prev = None
    for s in board["snapshots"]:
        ps = s["players"].get(me_id)
        if not ps:
            continue
        if prev is not None:
            d = _dist(prev, ps)
            if d is not None and d >= min_dist:
                from_lane = _lane(prev.get("x"), prev.get("y"))
                to_lane = _lane(ps.get("x"), ps.get("y"))
                if from_lane in ("base", "enemy_base") or \
                   to_lane in ("base", "enemy_base"):
                    pass  # recall trip, not a rotation
                elif from_lane != to_lane:
                    inflections.append({
                        "type": "rotation",
                        "min": s["min"],
                        "from": from_lane,
                        "to": to_lane,
                        "distance": round(d),
                        "score": 800,
                        "detail": (f"rotated {from_lane} -> {to_lane} at {s['min']}min "
                                   f"({round(d)} units)"),
                    })
        prev = ps
    return inflections


def detect_recalls(board, me_id=None, gold_drop=400):
    """You were in base while unspent gold dropped >= gold_drop (a shop trip)."""
    if me_id is None:
        me_id = board["me_id"]
    inflections = []
    prev = None
    for s in board["snapshots"]:
        ps = s["players"].get(me_id)
        if not ps:
            continue
        if prev is not None:
            lane = _lane(ps.get("x"), ps.get("y"))
            spent = (prev.get("unspent") or 0) - (ps.get("unspent") or 0)
            if lane in ("base", "enemy_base") and spent >= gold_drop:
                inflections.append({
                    "type": "recall_buy",
                    "min": s["min"],
                    "gold_spent": spent,
                    "score": 600,
                    "detail": f"recalled to base at {s['min']}min, spent ~{spent}g",
                })
        prev = ps
    return inflections


# --- orchestration ---------------------------------------------------------


def analyze(board):
    """Run every detector and return inflection points in chronological order
    (a decision timeline). Each carries a `score` for impact-ranking if desired."""
    inflections = []
    inflections += detect_objective_contests(board)
    inflections += detect_teamfights(board)
    inflections += detect_rotations(board)
    inflections += detect_recalls(board)
    for i in inflections:
        i["score"] = round(i["score"], 1)
    inflections.sort(key=lambda i: i["min"])
    return inflections


def report(board, inflections):
    lines = []
    lines.append("=" * 60)
    lines.append(f"Inflection points — {board['match_id']} "
                 f"({board['duration_min']}min)")
    lines.append("=" * 60)
    if not inflections:
        lines.append("  No inflection points flagged.")
    for i, ip in enumerate(inflections, 1):
        lines.append(f"\n  {i}. [{ip['min']:>5}min] {ip['type']}: {ip['detail']}")
    lines.append("\n" + "=" * 60)
    return "\n".join(lines)


# --- CLI -------------------------------------------------------------------


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("timeline_json", help="raw MATCH-V5 timeline JSON")
    ap.add_argument("match_json", help="raw MATCH-V5 match JSON")
    ap.add_argument("--puuid", help="your puuid (marks is_me)")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    import board as b
    with open(args.timeline_json) as f:
        tl = json.load(f)
    with open(args.match_json) as f:
        match = json.load(f)
    if not args.puuid:
        args.puuid = match["info"]["participants"][0]["puuid"]

    bd = b.extract_board(match, tl, args.puuid)
    inflections = analyze(bd)

    if args.json:
        print(json.dumps(inflections, indent=2))
    else:
        print(report(bd, inflections))


if __name__ == "__main__":
    main()
