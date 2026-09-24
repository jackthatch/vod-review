// moments.ts — flag pivotal moments in a single condensed match Story.
//
// Port of analyze() + the four detectors from moments.py. Deterministic
// detection only (no LLM): overstay deaths, contested objectives,
// death-at-objective, and power-spike gaps — ranked by an impact score.
//
// Signature mirrors the plan: analyze(story, { overstay_gold, range_units,
// window_sec, gap_min }) — the same thresholds stored in `preferences`.

import type { Moment } from "@/lib/types";
import type { Story, Snapshot } from "@/lib/condense";
import { contestContext, monsterLabel, type Board } from "@/lib/board";

type AnalyzeOptions = {
  overstay_gold: number;
  range_units: number;
  window_sec: number;
  gap_min: number;
};

/** Euclidean distance between two {x, y} points (LoL map units). */
function dist(
  a: { x?: number | null; y?: number | null },
  b: { x?: number | null; y?: number | null },
): number | null {
  const ax = a.x;
  const ay = a.y;
  const bx = b.x;
  const by = b.y;
  if (ax == null || ay == null || bx == null || by == null) return null;
  return Math.hypot(ax - bx, ay - by);
}

/** Last snapshot at or before `minute`; null if none exists. */
function snapAt(snapshots: Snapshot[], minute: number): Snapshot | null {
  let best: Snapshot | null = null;
  for (const s of snapshots) {
    if (s.min <= minute) best = s;
    else break;
  }
  return best;
}

function detectOverstays(story: Story, threshold: number): Moment[] {
  const moments: Moment[] = [];
  for (const d of story.deaths) {
    const g = d.current_gold;
    if (g != null && g >= threshold) {
      moments.push({
        type: "overstay_death",
        min: d.min,
        gold_held: g,
        score: g, // more unspent gold = worse overstay
        detail: `died at ${d.min}min holding ${g}g unspent`,
      });
    }
  }
  return moments;
}

function detectContestedObjectives(
  story: Story,
  rangeUnits: number,
  board?: Board | null,
): Moment[] {
  const moments: Moment[] = [];
  const myTeam = story.team_id;
  for (const o of story.objectives) {
    if (o.team == null || o.team === myTeam) continue; // your team secured it
    if (o.mine) continue;
    const me = snapAt(story.snapshots, o.min);
    if (!me) continue;
    const d = dist(me, o);
    if (d == null || d > rangeUnits) continue;

    const label = monsterLabel(o.type, o.sub);
    const contest = board
      ? (contestContext(board, o.type, o.min, rangeUnits) as {
          me_location: string | null;
          me_proximity: string;
          allies_near: number;
          enemies_near: number;
          team_committed: boolean;
        })
      : null;

    const where = contest ? (contest.me_location ?? contest.me_proximity) : null;
    let detail: string;
    if (contest && !contest.team_committed) {
      detail =
        `${label} conceded to enemy at ${o.min}min — you were ${where}; ` +
        `only ${contest.allies_near} ally near vs ${contest.enemies_near} enemies ` +
        `at the pit (team not committed)`;
    } else if (contest) {
      detail =
        `${label} lost to enemy at ${o.min}min — contested ` +
        `${contest.allies_near}v${contest.enemies_near} at the pit` +
        (where ? `, you were ${where}` : "");
    } else {
      detail = `${label} secured by enemy at ${o.min}min`;
    }

    moments.push({
      type: "contested_objective",
      min: o.min,
      objective: o.type,
      sub: o.sub,
      contest,
      score: 3000 - d, // closer = higher impact
      detail,
    });
  }
  return moments;
}

function detectDeathsAtObjective(story: Story, windowSec: number): Moment[] {
  const moments: Moment[] = [];
  for (const d of story.deaths) {
    for (const o of story.objectives) {
      const dt = Math.abs(d.min - o.min) * 60;
      if (dt <= windowSec) {
        moments.push({
          type: "death_at_objective",
          min: d.min,
          objective: o.type,
          sub: o.sub,
          objective_min: o.min,
          score: 2000 - dt, // closer to objective = more tied to fight
          detail: `died at ${d.min}min ${Math.round(dt)}s around ${monsterLabel(o.type, o.sub)} fight (obj at ${o.min}min)`,
        });
        break; // one objective per death is enough
      }
    }
  }
  return moments;
}

function detectPowerSpikeGaps(
  story: Story,
  gapMin: number,
  spikeThreshold = 25,
): Moment[] {
  const moments: Moment[] = [];
  const snaps = story.snapshots;
  if (snaps.length < 2) return moments;

  // Spike = an AD jump of >= spikeThreshold between consecutive snapshots.
  const spikeTimes: number[] = [];
  for (let i = 1; i < snaps.length; i++) {
    const prevAd = snaps[i - 1].attack_damage;
    const curAd = snaps[i].attack_damage;
    if (
      prevAd != null &&
      curAd != null &&
      curAd - prevAd >= spikeThreshold
    ) {
      spikeTimes.push(snaps[i].min);
    }
  }
  if (spikeTimes.length === 0) return moments;

  // Gaps from start → first spike, between spikes, and after the last spike.
  const bounds = [0.0, ...spikeTimes, snaps[snaps.length - 1].min];
  for (let j = 0; j < bounds.length - 1; j++) {
    const gap = bounds[j + 1] - bounds[j];
    if (gap >= gapMin) {
      const golds = snaps
        .filter(
          (s) =>
            bounds[j] <= s.min &&
            s.min <= bounds[j + 1] &&
            s.current_gold != null,
        )
        .map((s) => s.current_gold);
      const avgGold =
        golds.length > 0
          ? Math.round(golds.reduce((a, b) => a + b, 0) / golds.length)
          : 0;
      moments.push({
        type: "power_spike_gap",
        min: Math.round(bounds[j + 1] * 10) / 10,
        gap_minutes: Math.round(gap * 10) / 10,
        avg_gold_held: avgGold,
        score: gap * 100,
        detail: `no item completed from ${Math.round(bounds[j] * 10) / 10}–${Math.round(bounds[j + 1] * 10) / 10}min (${Math.round(gap * 10) / 10}min) while holding ~${avgGold}g`,
      });
    }
  }
  return moments;
}

export function analyze(
  story: Story,
  opts: AnalyzeOptions,
  board?: Board | null,
): Moment[] {
  const moments: Moment[] = [];
  moments.push(...detectOverstays(story, opts.overstay_gold));
  moments.push(...detectContestedObjectives(story, opts.range_units, board));
  moments.push(...detectDeathsAtObjective(story, opts.window_sec));
  moments.push(...detectPowerSpikeGaps(story, opts.gap_min));

  // Rank by impact score, highest first.
  for (const m of moments) {
    m.score = Math.round(m.score * 10) / 10;
  }
  moments.sort((a, b) => b.score - a.score);
  return moments;
}
