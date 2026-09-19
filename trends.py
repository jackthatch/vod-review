#!/usr/bin/env python3
"""
trends.py — aggregate condensed match JSONs (from fetch_match.py) into a
"leak profile": recurring patterns in your jungle gameplay.

Usage:
    python trends.py --data data --champion Graves
    python trends.py --data data --champion Graves --json

Metrics (jungle-focused):
    - first-clear speed (time to 6 camps)
    - CS/min
    - deaths/game + death timing distribution
    - overstay rate (% of deaths holding >= --overstay-gold unspent)
    - objective control (dragons/heralds/barons secured by your team / by you)
    - kill participation (kills + assists per game)
"""
import argparse
import glob
import json
import os
from collections import Counter, defaultdict


def load(data_dir, champion=None, role=None):
    matches = []
    for path in sorted(glob.glob(os.path.join(data_dir, "*.json"))):
        with open(path) as f:
            m = json.load(f)
        if champion and m["champion"].lower() != champion.lower():
            continue
        if role and m.get("role", "").upper() != role.upper():
            continue
        matches.append(m)
    return matches


def _avg(vals):
    vals = [v for v in vals if v is not None]
    return round(sum(vals) / len(vals), 2) if vals else None


def _snap_at(snapshots, minute):
    """Last snapshot at or before `minute`; None if none exists."""
    best = None
    for s in snapshots:
        if s["min"] <= minute:
            best = s
        else:
            break
    return best


def _level_time(matches, target_level):
    """Average minute at which the player first reaches `target_level`."""
    times = []
    for m in matches:
        for s in m["snapshots"]:
            if s["level"] >= target_level:
                times.append(s["min"])
                break
    return _avg(times)


def _item_spikes(snapshots, threshold=25):
    """Detect item purchases as attack-damage jumps >= threshold between
    adjacent snapshots (ignores small drift from buffs/level-ups)."""
    spikes = []
    for i in range(1, len(snapshots)):
        prev = snapshots[i - 1].get("attack_damage")
        cur = snapshots[i].get("attack_damage")
        if prev is not None and cur is not None and (cur - prev) >= threshold:
            spikes.append({"min": snapshots[i]["min"], "ad": cur, "delta": cur - prev})
    return spikes


def analyze(matches, overstay_gold):
    n = len(matches)
    if n == 0:
        return None

    wins = sum(1 for m in matches if m["win"])

    first_clears = [m["first_clear_min"] for m in matches]
    cs_min = [m["stats"]["total_cs"] / m["duration_min"] for m in matches]
    deaths_pg = [m["stats"]["deaths"] for m in matches]
    kp = [m["stats"]["kills"] + m["stats"]["assists"] for m in matches]

    # --- new snapshot-derived metrics ---
    gpm = [m["stats"]["gold"] / m["duration_min"] for m in matches]
    level_6 = _level_time(matches, 6)
    level_11 = _level_time(matches, 11)

    # AD at fixed minutes (item-spike / power-spike benchmark)
    ad10 = [(_snap_at(m["snapshots"], 10) or {}).get("attack_damage") for m in matches]
    ad20 = [(_snap_at(m["snapshots"], 20) or {}).get("attack_damage") for m in matches]

    # farming-vs-fighting split: final champ-damage / total-damage ratio
    fight_ratios = []
    dmg_taken = []
    for m in matches:
        if not m["snapshots"]:
            continue
        last = m["snapshots"][-1]
        td = last.get("total_damage")
        dc = last.get("damage_to_champions")
        if td and dc is not None:
            fight_ratios.append(dc / td)
        if last.get("damage_taken") is not None:
            dmg_taken.append(last["damage_taken"] / m["duration_min"])

    # item purchase timings
    spikes = []
    for m in matches:
        spikes.extend(_item_spikes(m["snapshots"]))

    # death timing + overstay
    buckets = Counter()
    total_deaths = 0
    overstays = 0
    overstay_examples = []
    for m in matches:
        for d in m["deaths"]:
            total_deaths += 1
            minute = d["min"]
            if minute < 5:
                buckets["0-5"] += 1
            elif minute < 10:
                buckets["5-10"] += 1
            elif minute < 15:
                buckets["10-15"] += 1
            elif minute < 20:
                buckets["15-20"] += 1
            else:
                buckets["20+"] += 1

            if d["current_gold"] is not None and d["current_gold"] >= overstay_gold:
                overstays += 1
                if len(overstay_examples) < 5:
                    overstay_examples.append(
                        {"match": m["match_id"], "min": d["min"],
                         "gold": d["current_gold"]}
                    )

    # objective control
    obj = defaultdict(lambda: [0, 0, 0])  # type -> [total, team_secured, my_smite]
    for m in matches:
        for o in m["objectives"]:
            otype = o["type"]
            obj[otype][0] += 1
            if o["team"] == m["team_id"]:
                obj[otype][1] += 1
            if o["mine"]:
                obj[otype][2] += 1

    return {
        "games": n,
        "winrate": round(100 * wins / n, 1),
        "first_clear_avg_min": _avg(first_clears),
        "cs_per_min": _avg(cs_min),
        "gold_per_min": _avg(gpm),
        "level_6_min": level_6,
        "level_11_min": level_11,
        "ad_at_10min": _avg(ad10),
        "ad_at_20min": _avg(ad20),
        "fight_ratio_pct": round(100 * _avg(fight_ratios), 1) if fight_ratios else None,
        "damage_taken_per_min": _avg(dmg_taken),
        "item_spikes": spikes,
        "deaths_per_game": _avg(deaths_pg),
        "kp_avg": _avg(kp),
        "death_timing": dict(buckets),
        "overstay_pct": round(100 * overstays / total_deaths, 1) if total_deaths else 0.0,
        "overstay_examples": overstay_examples,
        "objectives": {
            k: {"total": v[0], "team_secured": v[1], "my_smite": v[2]}
            for k, v in obj.items()
        },
    }


def report(r, champion):
    lines = []
    lines.append("=" * 56)
    title = f"Jungle Leak Profile"
    if champion:
        title += f" — {champion}"
    lines.append(f"{title} ({r['games']} games, {r['winrate']}% WR)")
    lines.append("=" * 56)

    fc = r["first_clear_avg_min"]
    lines.append(f"  First clear (6 camps): {fc}m avg" if fc else "  First clear: n/a")
    lines.append(f"  CS/min:                {r['cs_per_min']}")
    lines.append(f"  Gold/min:              {r['gold_per_min']}")
    lines.append(f"  Deaths/game:           {r['deaths_per_game']}")
    lines.append(f"  Kill participation:    {r['kp_avg']} (kills+assists)/game")

    lines.append("")
    lines.append("  Power spikes:")
    lines.append(f"    Level 6 (avg):       {r['level_6_min']} min")
    lines.append(f"    Level 11 (avg):      {r['level_11_min']} min")
    lines.append(f"    AD @ 10min (avg):    {r['ad_at_10min']}")
    lines.append(f"    AD @ 20min (avg):    {r['ad_at_20min']}")
    lines.append(f"    Item purchases:      {len(r['item_spikes'])} detected "
                 f"({_avg([s['delta'] for s in r['item_spikes']]) or 0} avg AD jump)")

    lines.append("")
    lines.append(f"  Farming-vs-fighting:   {r['fight_ratio_pct']}% of dmg to champions"
                 if r["fight_ratio_pct"] is not None else
                 "  Farming-vs-fighting:   n/a")
    lines.append(f"  Damage taken/min:      {r['damage_taken_per_min']}")

    lines.append("")
    lines.append("  Death timing distribution:")
    for k in ["0-5", "5-10", "10-15", "15-20", "20+"]:
        if k in r["death_timing"]:
            lines.append(f"    {k:>5} min: {r['death_timing'][k]}")

    lines.append("")
    lines.append(f"  Overstay rate (died holding >= {r.get('_overstay_gold','?')}g): "
                 f"{r['overstay_pct']}% of deaths")
    for ex in r["overstay_examples"]:
        lines.append(f"    e.g. died at {ex['min']}min with {ex['gold']}g unspent")

    if r["objectives"]:
        lines.append("")
        lines.append("  Objective control (total / your team / your smite):")
        for otype, v in sorted(r["objectives"].items()):
            lines.append(f"    {otype:<14} {v['total']:>2} / {v['team_secured']:>2} / "
                         f"{v['my_smite']:>2}")

    lines.append("=" * 56)
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="data")
    ap.add_argument("--champion", default=None,
                    help="only include matches on this champion")
    ap.add_argument("--role", default=None, help="filter by role (e.g. JUNGLE)")
    ap.add_argument("--overstay-gold", type=int, default=1000,
                    help="unspent-gold threshold for 'overstayed' flag")
    ap.add_argument("--json", action="store_true", help="emit raw JSON")
    args = ap.parse_args()

    matches = load(args.data, champion=args.champion, role=args.role)
    if not matches:
        msg = f"No matches found in {args.data}"
        if args.champion:
            msg += f" for champion {args.champion}"
        print(msg)
        return

    r = analyze(matches, args.overstay_gold)
    r["_overstay_gold"] = args.overstay_gold

    if args.json:
        print(json.dumps(r, indent=2))
    else:
        print(report(r, args.champion))


if __name__ == "__main__":
    main()
