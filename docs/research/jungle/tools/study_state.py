#!/usr/bin/env python3
"""
study_state.py — deterministic state/planner for the jungle research study.

Single source of truth is the FILESYSTEM: an axis is "done" when its findings
file exists. No separate database, no drift.

Used by the one-shot runner (see ../ONE-SHOT-RUN.md) to decide what to research
next, and by anyone wanting a status readout.

Commands:
    status                 human summary of all axes
    next [--batch N]       emit the next N pending axes as JSON (default 3)
    goal <axis>            emit just the goal string for one axis (for delegate_task)
    verify                 report axes whose findings file is missing/thin

Exit codes: 0 ok, 1 = nothing pending (status) / bad axis (goal).

Design notes for the one-shot run:
  * Hermes fans out at most 3 sub-agents concurrently -> default batch is 3.
  * One sub-agent per axis. Never bundle axes into one sub-agent; run 1 showed
    bundled/multi-goal agents exhaust their iteration budget before writing.
  * Each sub-agent MUST write its findings file. The orchestrator verifies and,
    if missing, salvages the substance from the returned summary.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass, asdict

HERE = os.path.dirname(os.path.abspath(__file__))
STUDY_DIR = os.path.dirname(HERE)              # docs/research/jungle
FINDINGS = os.path.join(STUDY_DIR, "findings")
MAX_BATCH = 3                                   # Hermes concurrency cap

# One-time run-1 artifact: axes 1-3 were originally salvaged from sub-agent
# summaries rather than written by the agents. The one-shot run rewrote all
# three properly (2026-09-24), so this set is now empty. Kept as a mechanism:
# add an axis number here to force it to be re-researched.
#
# ORCHESTRATOR-OWNED. Sub-agents must NOT edit this file or the README — doing
# so races against sibling agents. See ONE-SHOT-RUN.md §6.
PROVISIONAL: set[int] = set()


@dataclass(frozen=True)
class Axis:
    num: int
    slug: str
    title: str
    goal: str

    @property
    def path(self) -> str:
        return os.path.join(FINDINGS, f"{self.num:02d}-{self.slug}.md")

    @property
    def done(self) -> bool:
        # "done" = file exists, has real content (not a stub), and is not one of
        # the run-1 salvaged files still awaiting a clean pass.
        if self.num in PROVISIONAL:
            return False
        if not os.path.exists(self.path):
            return False
        return os.path.getsize(self.path) > 400


AXES: list[Axis] = [
    Axis(1, "how-games-are-decided",
         "How games are actually decided in solo queue",
         "Establish how LoL games are won/lost in solo queue: win conditions; "
         "is it snowball-driven or near coin-flip; the relative predictive weight "
         "of early vs late game. Must cite Riot primary sources and academic "
         "prediction work. Include measured numbers where they exist."),
    Axis(2, "jungle-impact-on-winrate",
         "Causal impact of jungle play on win rate",
         "Quantify which jungle behaviours correlate most with winning: KP%, "
         "CS/min, early deaths, objective participation, gank conversion. Use "
         "lolalytics/u.gg/op.gg aggregates (fetch via tools/fetch_page.py) and "
         "any analyst/Riot data. State effect sizes and confidence."),
    Axis(3, "objective-value",
         "Objective value: drakes, Voidgrubs, Herald, Baron, soul",
         "Measure the win-rate impact of each major objective and correct "
         "prioritisation. NOTE: Atakhan + Feats of Strength were REMOVED in "
         "patch 26.1 — do not treat them as live. Cite patch-dated sources."),
    Axis(4, "tempo-and-pathing",
         "Tempo & pathing theory",
         "Advanced jungle clear/route theory: how tempo is defined and measured, "
         "what separates strong from weak pathing, first-clear optimisation, and "
         "how tempo converts to win probability. Distinguish durable theory from "
         "patch-specific routes (date the latter)."),
    Axis(5, "gank-theory",
         "Gank theory: when ganks convert",
         "When and why ganks succeed: lane selection, timing windows, expected "
         "value, counter-gank risk. Include measured gank-success stats if "
         "obtainable; otherwise clearly mark as analyst consensus."),
    Axis(6, "vision-and-information",
         "Vision & information advantage in the jungle",
         "Ward economy, vision denial, information advantage as a win driver. "
         "Quantify where possible (control-ward counts, vision score "
         "correlations); cite sources."),
    Axis(7, "counterjungling-invades",
         "Counter-jungling, invades, vertical jungling",
         "Risk/reward of invades, counter-jungling and vertical jungling: win-"
         "rate impact, conditions under which it pays, and failure modes."),
    Axis(8, "archetype-winrate-drivers",
         "Win-rate drivers per jungle archetype",
         "What separates good from great players on carry vs gank vs tank "
         "junglers: the specific behaviours/metrics that differ. Tie to the six "
         "archetypes in docs/jungle-playbook.md §4."),
    Axis(9, "champion-pool-effects",
         "Champion-pool effects on win rate",
         "Does pool breadth help or hurt? One-trick vs flexible pool, mastery "
         "curves, win-rate-vs-games-played data (lolalytics/u.gg have this). "
         "Quantify."),
    Axis(10, "how-players-improve",
         "What actually improves solo-queue players fastest",
         "Evidence on review methods, coaching, deliberate practice in LoL and "
         "adjacent domains. What review behaviours actually move rank. This "
         "directly informs the product's coach design."),
    Axis(11, "rank-leak-distribution",
         "Rank-tier leak distribution",
         "Which mistakes concentrate at which ranks (Iron->Challenger): jungle-"
         "relevant leaks by tier. Use aggregates where possible; flag opinion."),
    Axis(12, "meta-snapshot",
         "Current jungle meta snapshot (PATCH-DATED)",
         "A dated snapshot of the live jungle meta: top champions, tier lists, "
         "win/pick/ban rates at a stated rank band and patch. MUST be "
         "re-verified each patch — mark clearly as perishable."),
]


def _by_num(num: int) -> Axis | None:
    return next((a for a in AXES if a.num == num), None)


def cmd_status() -> int:
    done = [a for a in AXES if a.done]
    pending = [a for a in AXES if not a.done]
    print(f"Jungle study — {len(done)}/{len(AXES)} axes done\n")
    for a in AXES:
        mark = "☑" if a.done else "☐"
        size = f"{os.path.getsize(a.path):>5}B" if os.path.exists(a.path) else "   -- "
        print(f"  {mark} {a.num:>2}. [{size}] {a.title}")
    print(f"\nPending: {len(pending)}  |  next batch (<= {MAX_BATCH}): "
          f"{[a.num for a in pending[:MAX_BATCH]]}")
    return 0


def cmd_next(batch: int) -> int:
    pending = [a for a in AXES if not a.done][:batch]
    if not pending:
        print("[]")
        return 1
    out = [{"num": a.num, "title": a.title, "goal": a.goal,
            "deliverable": os.path.relpath(a.path, STUDY_DIR)} for a in pending]
    print(json.dumps(out, indent=2))
    return 0


def cmd_goal(num: int) -> int:
    a = _by_num(num)
    if not a:
        print(f"no such axis: {num}", file=sys.stderr)
        return 1
    print(json.dumps({"num": a.num, "title": a.title, "goal": a.goal,
                      "deliverable": os.path.relpath(a.path, STUDY_DIR)}, indent=2))
    return 0


def cmd_verify() -> int:
    """Report axes whose findings file is missing or thin (<400B => likely a stub)."""
    bad = []
    for a in AXES:
        if a.num in PROVISIONAL:
            bad.append((a.num, "PROVISIONAL (run-1 salvage; needs clean pass)"))
        elif not os.path.exists(a.path):
            bad.append((a.num, "MISSING"))
        elif os.path.getsize(a.path) <= 400:
            bad.append((a.num, f"THIN ({os.path.getsize(a.path)}B)"))
    if bad:
        for num, why in bad:
            print(f"  axis {num}: {why}")
        return 1
    print("all findings files present and non-trivial")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="jungle study state/planner")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("status")
    p_next = sub.add_parser("next")
    p_next.add_argument("--batch", type=int, default=MAX_BATCH)
    p_goal = sub.add_parser("goal")
    p_goal.add_argument("axis", type=int)
    sub.add_parser("verify")
    args = ap.parse_args()

    if args.cmd == "status":
        return cmd_status()
    if args.cmd == "next":
        return cmd_next(max(1, min(args.batch, MAX_BATCH)))
    if args.cmd == "goal":
        return cmd_goal(args.axis)
    if args.cmd == "verify":
        return cmd_verify()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
