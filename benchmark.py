#!/usr/bin/env python3
"""
benchmark.py — diff a player's profile against pro solo-queue junglers.

Answers "is my 8.0 CS/min actually bad for Graves, or normal?" by comparing the
same metrics the leak profile computes, across two datasets fetched by
fetch_match.py.

Usage:
    # fetch the player + pros first (separate --out dirs)
    python fetch_match.py --name jugking --tag fines --region na1 --count 30 --out data/me
    python fetch_match.py --name JUGKlNG --tag kr --region kr --count 30 --out data/canyon

    python benchmark.py --me data/me --pros data/canyon --champion Graves
    python benchmark.py --me data/me --pros data/canyon --json

Env: none (reads local JSON files).
"""
import argparse
import json

import trends


def load_champion(data_dir, champion):
    """Load condensed matches from a dir, filtered to one champion."""
    return trends.load(data_dir, champion=champion)


def _metric(matches, fn):
    vals = [fn(m) for m in matches if fn(m) is not None]
    return round(sum(vals) / len(vals), 2) if vals else None


def compare(me, pros):
    """Return a dict of metric -> {me, pro, delta, delta_pct}."""
    metrics = {}

    def add(key, mine, theirs, higher_is_better=True):
        if mine is None or theirs is None:
            metrics[key] = {"me": mine, "pro": theirs, "delta": None, "delta_pct": None}
            return
        delta = round(mine - theirs, 2)
        pct = round(100 * delta / theirs, 1) if theirs else None
        metrics[key] = {
            "me": mine, "pro": theirs, "delta": delta, "delta_pct": pct,
        }

    def cs_pm(m):
        return m["stats"]["total_cs"] / m["duration_min"]

    def gold_pm(m):
        return m["stats"]["gold"] / m["duration_min"]

    def kp(m):
        return m["stats"]["kills"] + m["stats"]["assists"]

    def deaths_pg(m):
        return m["stats"]["deaths"]

    def first_clear(m):
        return m["first_clear_min"]

    def ad_at(m, minute):
        s = trends._snap_at(m["snapshots"], minute)
        return s.get("attack_damage") if s else None

    add("cs_per_min", _metric(me, cs_pm), _metric(pros, cs_pm))
    add("gold_per_min", _metric(me, gold_pm), _metric(pros, gold_pm))
    add("kill_participation", _metric(me, kp), _metric(pros, kp))
    add("deaths_per_game", _metric(me, deaths_pg), _metric(pros, deaths_pg),
        higher_is_better=False)
    add("first_clear_min", _metric(me, first_clear), _metric(pros, first_clear),
        higher_is_better=False)
    add("ad_at_10min", _metric(me, lambda m: ad_at(m, 10)),
        _metric(pros, lambda m: ad_at(m, 10)))
    add("ad_at_20min", _metric(me, lambda m: ad_at(m, 20)),
        _metric(pros, lambda m: ad_at(m, 20)))

    return metrics


def report(metrics, champion):
    lines = []
    lines.append("=" * 60)
    title = f"Benchmark vs pros"
    if champion:
        title += f" — {champion}"
    lines.append(title)
    lines.append("=" * 60)
    lines.append(f"  {'metric':<20} {'you':>8} {'pro':>8} {'Δ':>8} {'Δ%':>8}")
    lines.append("  " + "-" * 52)
    for key, v in metrics.items():
        if v["me"] is None or v["pro"] is None:
            lines.append(f"  {key:<20} {'—':>8} {'—':>8} {'—':>8}")
            continue
        sign = "+" if v["delta"] >= 0 else ""
        lines.append(
            f"  {key:<20} {v['me']:>8} {v['pro']:>8} "
            f"{sign}{v['delta']:>7} {sign}{v['delta_pct']}%"
        )
    lines.append("=" * 60)
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--me", required=True, help="dir with your condensed matches")
    ap.add_argument("--pros", required=True, help="dir with pro condensed matches")
    ap.add_argument("--champion", default=None)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    me = load_champion(args.me, args.champion)
    pros = load_champion(args.pros, args.champion)
    if not me:
        print(f"No matches for you in {args.me}"
              + (f" on {args.champion}" if args.champion else ""))
        return
    if not pros:
        print(f"No pro matches in {args.pros}"
              + (f" on {args.champion}" if args.champion else ""))
        return

    metrics = compare(me, pros)

    if args.json:
        print(json.dumps({
            "champion": args.champion,
            "n_me": len(me),
            "n_pro": len(pros),
            "metrics": metrics,
        }, indent=2))
    else:
        print(report(metrics, args.champion))


if __name__ == "__main__":
    main()
