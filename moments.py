#!/usr/bin/env python3
"""
moments.py — flag pivotal moments in a single condensed match JSON.

Turns a per-game "story" (from fetch_match.py) into a short, ranked list of
moments that likely decided the game. This is the deterministic detection layer
that feeds the coaching/LLM layer (see VISION.md: "detection is deterministic,
explanation is generative").

Usage:
    python moments.py data/NA1_1234567890.json
    python moments.py data/NA1_1234567890.json --json
    python moments.py data/NA1_1234567890.json --overstay-gold 1200 --range 3000

Detectors (all deterministic, all ranked by an impact score):
    - overstay death   — died while holding >= N unspent gold
    - contested objective — an objective was secured by the enemy team while you
                             were within `--range` units of it (you were there but
                             didn't/couldn't stop it)
    - death at objective — you died within `--window` sec of an objective fight
    - power-spike gap  — a long stretch holding gold with no item completed
"""

import argparse
import json
import math

from board import monster_label, contest_context


def _dist(a, b):
    """Euclidean distance between two {x, y} points (LoL map units)."""
    ax, ay = a.get("x"), a.get("y")
    bx, by = b.get("x"), b.get("y")
    if None in (ax, ay, bx, by):
        return None
    return math.hypot(ax - bx, ay - by)


def _snap_at(snapshots, minute):
    """Last snapshot at or before `minute`; None if none exists."""
    best = None
    for s in snapshots:
        if s["min"] <= minute:
            best = s
        else:
            break
    return best


def _my_team(match):
    return match.get("team_id")


def detect_overstays(match, threshold):
    """Deaths while holding >= threshold unspent gold."""
    moments = []
    for d in match.get("deaths", []):
        g = d.get("current_gold")
        if g is not None and g >= threshold:
            moments.append({
                "type": "overstay_death",
                "min": d["min"],
                "gold_held": g,
                "score": g,  # more unspent gold = worse overstay
                "detail": f"died at {d['min']}min holding {g}g unspent",
            })
    return moments


def detect_contested_objectives(match, range_units, board=None):
    """Enemy team secured an objective while you were within `range_units`.

    When a `board` is supplied, the moment is enriched with a contest context
    (who was at the pit, who was alive, gold state, soul stakes) so we can tell
    "we contested and lost" apart from "we conceded" — and say so in the detail.
    """
    moments = []
    my_team = _my_team(match)
    for o in match.get("objectives", []):
        if o.get("team") is None or o["team"] == my_team:
            continue  # your team secured it (or unknown) — not a "lost contest"
        if o.get("mine"):
            continue
        me = _snap_at(match.get("snapshots", []), o["min"])
        if not me:
            continue
        d = _dist(me, o)
        if d is None or d > range_units:
            continue

        label = monster_label(o.get("type"), o.get("sub"))
        contest = (contest_context(board, o.get("type"), o["min"], range_units)
                   if board is not None else None)

        where = (contest["me_location"] or contest["me_proximity"]) if contest else None
        if contest and not contest["team_committed"]:
            detail = (f"{label} conceded to enemy at {o['min']}min — you were "
                      f"{where}; only {contest['allies_near']} ally near vs "
                      f"{contest['enemies_near']} enemies at the pit "
                      f"(team not committed)")
        elif contest:
            detail = (f"{label} lost to enemy at {o['min']}min — contested "
                      f"{contest['allies_near']}v{contest['enemies_near']} at the pit"
                      + (f", you were {where}" if where else ""))
        else:
            detail = f"{label} secured by enemy at {o['min']}min"

        moments.append({
            "type": "contested_objective",
            "min": o["min"],
            "objective": o.get("type"),
            "sub": o.get("sub"),
            "contest": contest,
            "score": 3000 - d,  # closer = higher impact
            "detail": detail,
        })
    return moments


def detect_deaths_at_objective(match, window_sec):
    """You died within `window_sec` of an objective being secured (a fight at it)."""
    moments = []
    objectives = match.get("objectives", [])
    for d in match.get("deaths", []):
        for o in objectives:
            dt = abs(d["min"] - o["min"]) * 60
            if dt <= window_sec:
                moments.append({
                    "type": "death_at_objective",
                    "min": d["min"],
                    "objective": o.get("type"),
                    "sub": o.get("sub"),
                    "objective_min": o["min"],
                    "score": 2000 - dt,  # closer to objective = more tied to fight
                    "detail": (f"died at {d['min']}min "
                               f"{'%.0f' % dt}s around "
                               f"{monster_label(o.get('type'), o.get('sub'))} "
                               f"fight (obj at {o['min']}min)"),
                })
                break  # one objective per death is enough
    return moments


def detect_power_spike_gaps(match, gap_min, spike_threshold=25):
    """Long stretch holding gold with no item completed (AD jump)."""
    moments = []
    snaps = match.get("snapshots", [])
    if len(snaps) < 2:
        return moments

    last_spike = None
    for i in range(1, len(snaps)):
        prev_ad = snaps[i - 1].get("attack_damage")
        cur_ad = snaps[i].get("attack_damage")
        if prev_ad is not None and cur_ad is not None and (cur_ad - prev_ad) >= spike_threshold:
            last_spike = snaps[i]["min"]

    # find the longest gap between consecutive spikes holding gold
    spike_times = []
    for i in range(1, len(snaps)):
        prev_ad = snaps[i - 1].get("attack_damage")
        cur_ad = snaps[i].get("attack_damage")
        if prev_ad is not None and cur_ad is not None and (cur_ad - prev_ad) >= spike_threshold:
            spike_times.append(snaps[i]["min"])

    if not spike_times:
        return moments

    # gap from start to first spike, and between spikes, and after last spike
    bounds = [0.0] + spike_times + [snaps[-1]["min"]]
    for j in range(len(bounds) - 1):
        gap = bounds[j + 1] - bounds[j]
        if gap >= gap_min:
            # average gold held across that window
            golds = [s["current_gold"] for s in snaps
                     if bounds[j] <= s["min"] <= bounds[j + 1] and s.get("current_gold")]
            avg_gold = round(sum(golds) / len(golds)) if golds else 0
            moments.append({
                "type": "power_spike_gap",
                "min": round(bounds[j + 1], 1),
                "gap_minutes": round(gap, 1),
                "avg_gold_held": avg_gold,
                "score": gap * 100,
                "detail": (f"no item completed from {round(bounds[j],1)}–"
                           f"{round(bounds[j+1],1)}min ({round(gap,1)}min) while "
                           f"holding ~{avg_gold}g"),
            })
    return moments


def analyze(match, overstay_gold=1000, range_units=3000, window_sec=30,
            gap_min=6.0, board=None):
    moments = []
    moments += detect_overstays(match, overstay_gold)
    moments += detect_contested_objectives(match, range_units, board)
    moments += detect_deaths_at_objective(match, window_sec)
    moments += detect_power_spike_gaps(match, gap_min)

    # rank by impact score, highest first
    for m in moments:
        m["score"] = round(m["score"], 1)
    moments.sort(key=lambda m: m["score"], reverse=True)
    return moments


def report(match, moments):
    lines = []
    champ = match.get("champion", "?")
    result = "Win" if match.get("win") else "Loss"
    lines.append("=" * 60)
    lines.append(f"Pivotal moments — {champ} {result} "
                 f"({match.get('duration_min', '?')}min)")
    lines.append("=" * 60)
    if not moments:
        lines.append("  No significant moments flagged.")
    for i, m in enumerate(moments, 1):
        lines.append(f"\n  {i}. [{m['type']}] {m['detail']}")
    lines.append("\n" + "=" * 60)
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("match_json", help="path to a condensed match JSON")
    ap.add_argument("--overstay-gold", type=int, default=1000)
    ap.add_argument("--range", type=int, default=3000,
                    help="distance (map units) to count as 'contesting' an objective")
    ap.add_argument("--window", type=int, default=30,
                    help="seconds around an objective to count as a 'fight'")
    ap.add_argument("--gap-min", type=float, default=6.0,
                    help="min minutes between item completions to flag a gap")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--top", type=int, default=10, help="max moments to show")
    args = ap.parse_args()

    with open(args.match_json) as f:
        match = json.load(f)

    moments = analyze(match, args.overstay_gold, args.range, args.window,
                      args.gap_min)
    moments = moments[: args.top]

    if args.json:
        print(json.dumps(moments, indent=2))
    else:
        print(report(match, moments))


if __name__ == "__main__":
    main()
