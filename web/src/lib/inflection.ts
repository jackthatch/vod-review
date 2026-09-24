// inflection.ts — flag inflection points (Layer 3 of the coach pipeline).
//
// Port of inflection.py: the four deterministic detectors + analyze(). Where
// moments.ts flags *outcomes* (you died, they got the objective), this flags
// *decisions*: when a contest started, a teamfight broke out, you rotated, or
// you recalled to shop. Runs on the FULL board (board.extractBoard), not the
// me-only Story.

import type { Moment } from "@/lib/types";
import { OBJECTIVE_POS, dist, lane, monsterLabel, type Board } from "@/lib/board";

function detectObjectiveContests(
  board: Board,
  radius = 3500,
  minPlayers = 4,
  lookbackMin = 1.5,
): Moment[] {
  const inflections: Moment[] = [];
  for (const ev of board.events) {
    if (ev.type !== "ELITE_MONSTER_KILL") continue;
    const monster = ev.monster;
    const pit = monster ? OBJECTIVE_POS[monster] : undefined;
    if (!pit) continue;
    const killMin = ev.min;
    let start: number | null = null;
    for (const s of board.snapshots) {
      if (s.min < killMin - lookbackMin) continue;
      if (s.min > killMin) break;
      let near = 0;
      for (const ps of Object.values(s.players)) {
        const d = dist(ps, pit);
        if (d != null && d <= radius) near++;
      }
      if (near >= minPlayers) {
        start = s.min;
        break;
      }
    }
    if (start != null && start < killMin) {
      inflections.push({
        type: "objective_contest",
        min: start,
        objective: monster,
        sub: ev.sub,
        secured_by: ev.team,
        secured_min: killMin,
        score: 2500,
        detail: `${monsterLabel(monster, ev.sub)} contest began at ${start}min (>=${minPlayers} champions at the pit), secured by team ${ev.team} at ${killMin}min`,
      });
    }
  }
  return inflections;
}

function detectTeamfights(board: Board, minAssists = 2): Moment[] {
  const inflections: Moment[] = [];
  for (const ev of board.events) {
    if (ev.type !== "CHAMPION_KILL") continue;
    const assists = ev.assists ?? [];
    if (assists.length >= minAssists) {
      const involved = assists.length + 2;
      inflections.push({
        type: "teamfight",
        min: ev.min,
        participants: involved,
        score: 1500 + 100 * assists.length,
        detail: `teamfight at ${ev.min}min (${involved} champions involved)`,
      });
    }
  }
  return inflections;
}

function detectRotations(board: Board, meId: number | null, minDist = 5000): Moment[] {
  const id = meId ?? board.me_id;
  const inflections: Moment[] = [];
  let prev: { x: number; y: number } | null = null;
  for (const s of board.snapshots) {
    const ps = s.players[id];
    if (!ps) continue;
    if (prev != null) {
      const d = dist(prev, ps);
      if (d != null && d >= minDist) {
        const fromLane = lane(prev.x, prev.y);
        const toLane = lane(ps.x, ps.y);
        const isBase =
          fromLane === "base" ||
          fromLane === "enemy_base" ||
          toLane === "base" ||
          toLane === "enemy_base";
        if (!isBase && fromLane !== toLane) {
          inflections.push({
            type: "rotation",
            min: s.min,
            from: fromLane,
            to: toLane,
            distance: Math.round(d),
            score: 800,
            detail: `rotated ${fromLane} -> ${toLane} at ${s.min}min (${Math.round(d)} units)`,
          });
        }
      }
    }
    prev = ps;
  }
  return inflections;
}

function detectRecalls(board: Board, meId: number | null, goldDrop = 400): Moment[] {
  const id = meId ?? board.me_id;
  const inflections: Moment[] = [];
  let prev: { x: number; y: number; unspent: number | null } | null = null;
  for (const s of board.snapshots) {
    const ps = s.players[id];
    if (!ps) continue;
    if (prev != null) {
      const l = lane(ps.x, ps.y);
      const spent = (prev.unspent ?? 0) - (ps.unspent ?? 0);
      if ((l === "base" || l === "enemy_base") && spent >= goldDrop) {
        inflections.push({
          type: "recall_buy",
          min: s.min,
          gold_spent: spent,
          score: 600,
          detail: `recalled to base at ${s.min}min, spent ~${spent}g`,
        });
      }
    }
    prev = ps;
  }
  return inflections;
}

export function analyze(board: Board, meId: number | null = null): Moment[] {
  const inflections: Moment[] = [];
  inflections.push(...detectObjectiveContests(board));
  inflections.push(...detectTeamfights(board));
  inflections.push(...detectRotations(board, meId));
  inflections.push(...detectRecalls(board, meId));
  for (const i of inflections) i.score = Math.round((i.score as number) * 10) / 10;
  inflections.sort((a, b) => a.min - b.min);
  return inflections;
}
