// jungle_events.ts — Layer 3.5: jungle-behaviour detector (ganks, lane presence,
// invades) computed deterministically from the Riot timeline.
//
// Port of jungle_events.py. WHY THIS EXISTS: the jungle research study found
// that gank-conversion and invade-success rates are NOT measured anywhere in
// public data — Riot doesn't track ganks. So we compute them from the timeline.
//
// HONESTY CONTRACT: Riot samples positions only ONCE PER MINUTE outside of kill
// events. Therefore:
//   * Converted ganks and invade windows are MEASURED.
//   * Lane visits are a PROXY for gank attempts — failed ganks are not directly
//     observable. Never present `*_proxy` fields as measured.
//   * Invade durations are approximate (+/- 1 min sampling).

import { lane as laneOf, type Board, type PlayerInfo } from "@/lib/board";

// teamPosition -> the lane that role occupies. Both bot-lane roles map to "bot".
const LANE_FOR_ROLE: Record<string, string> = {
  TOP: "top",
  MIDDLE: "mid",
  BOTTOM: "bot",
  UTILITY: "bot",
  MID: "mid",
  BOT: "bot",
  ADC: "bot",
  SUPPORT: "bot",
};

const LANES = ["top", "mid", "bot"] as const;

// How long after a sampled lane visit we still credit a kill to that visit.
const VISIT_KILL_WINDOW_MIN = 1.5;

export interface Gank {
  min: number;
  lane: string;
  ganker_team: number;
  ganker_champion: string;
  victim_champion: string;
  victim_role: string;
  counter_gank: boolean;
  on_victim_side: boolean;
  participants: number;
}

export interface LaneVisit {
  min: number;
  lane: string;
  jungler_champion: string;
  jungler_team: number;
  kill_within_window: boolean;
  kills: number;
}

export interface Invade {
  start_min: number;
  end_min: number;
  duration_min: number;
  jungler_champion: string;
  jungler_team: number;
  kills: number;
  died: boolean;
}

export interface JungleSideSummary {
  gank_kills: number;
  ganks_on_lanes: string[];
  lane_visits_proxy: number;
  visits_with_kill_proxy: number;
  invade_windows: number;
  invade_kills: number;
  invade_deaths: number;
}

export interface JungleEvents {
  ganks: Gank[];
  lane_visits: LaneVisit[];
  invades: Invade[];
  summary: { me: JungleSideSummary; enemy_jungler: JungleSideSummary };
  caveat: string;
}

function isJungler(players: Record<number, PlayerInfo>, pid: number): boolean {
  return !!players[pid]?.has_smite;
}

/** Which half of the map a point is in ('blue' bottom-left / 'red' top-right). */
function half(x: number | null, y: number | null): string | null {
  if (x == null || y == null) return null;
  return x + y < 14800 ? "blue" : "red";
}

function teamHalf(team: number): string | null {
  return team === 100 ? "blue" : team === 200 ? "red" : null;
}

function killsOf(board: Board) {
  return board.events.filter((e) => e.type === "CHAMPION_KILL");
}

function junglerIds(board: Board): number[] {
  return Object.entries(board.players)
    .filter(([, pl]) => pl.has_smite)
    .map(([pid]) => Number(pid));
}

// --- ganks ------------------------------------------------------------------

export function detectGanks(board: Board): Gank[] {
  const players = board.players;
  const out: Gank[] = [];
  for (const ev of killsOf(board)) {
    const victim = ev.victim != null ? players[ev.victim] : undefined;
    if (!victim) continue;
    const vrole = victim.role;
    if (!(vrole in LANE_FOR_ROLE)) continue;
    if (laneOf(ev.x, ev.y) !== LANE_FOR_ROLE[vrole]) continue; // died outside their lane

    const involved: number[] = [];
    if (ev.killer != null) involved.push(ev.killer);
    for (const a of ev.assists ?? []) involved.push(a);

    const attackers = involved.filter((p) => players[p]?.team !== victim.team);
    const atkJunglers = attackers.filter((p) => isJungler(players, p));
    if (atkJunglers.length === 0) continue; // a solo lane kill, not a gank

    const defJunglers = involved.filter(
      (p) => players[p]?.team === victim.team && isJungler(players, p),
    );

    const ganker = players[atkJunglers[0]];
    out.push({
      min: ev.min,
      lane: laneOf(ev.x, ev.y),
      ganker_team: ganker.team,
      ganker_champion: ganker.champion,
      victim_champion: victim.champion,
      victim_role: vrole,
      counter_gank: defJunglers.length > 0,
      on_victim_side: half(ev.x, ev.y) === teamHalf(victim.team),
      participants: attackers.length,
    });
  }
  return out;
}

// --- lane presence (gank attempts, proxy) -----------------------------------

export function detectLaneVisits(board: Board): LaneVisit[] {
  const kills = killsOf(board);
  const visits: LaneVisit[] = [];

  for (const jid of junglerIds(board)) {
    let run: { lane: string; start: number } | null = null;
    for (const snap of board.snapshots) {
      const ps = snap.players[jid];
      if (!ps) continue;
      const ln = laneOf(ps.x, ps.y);
      if ((LANES as readonly string[]).includes(ln)) {
        if (run && run.lane === ln) {
          // extend the run, keep original start
        } else {
          run = { lane: ln, start: snap.min };
        }
      } else if (run) {
        visits.push(finishVisit(board, jid, run, kills));
        run = null;
      }
    }
    if (run) visits.push(finishVisit(board, jid, run, kills));
  }
  return visits;
}

function finishVisit(
  board: Board,
  jid: number,
  run: { lane: string; start: number },
  kills: ReturnType<typeof killsOf>,
): LaneVisit {
  const jpl = board.players[jid];
  const near = kills.filter(
    (k) =>
      k.min >= run.start &&
      k.min <= run.start + VISIT_KILL_WINDOW_MIN &&
      laneOf(k.x, k.y) === run!.lane &&
      (k.killer === jid || (k.assists ?? []).includes(jid)),
  );
  return {
    min: run.start,
    lane: run.lane,
    jungler_champion: jpl.champion,
    jungler_team: jpl.team,
    kill_within_window: near.length > 0,
    kills: near.length,
  };
}

// --- invades ----------------------------------------------------------------

export function detectInvades(board: Board): Invade[] {
  const kills = killsOf(board);
  const out: Invade[] = [];

  for (const jid of junglerIds(board)) {
    const myHalf = teamHalf(board.players[jid].team);
    let run: number[] | null = null;
    const windows: number[][] = [];

    for (const snap of board.snapshots) {
      const ps = snap.players[jid];
      if (!ps) continue;
      const h = half(ps.x, ps.y);
      const ln = laneOf(ps.x, ps.y);
      // Only the jungle and river quadrants count (river buckets to "jungle").
      const inEnemyJungle = h != null && h !== myHalf && ln === "jungle";
      if (inEnemyJungle) {
        if (run && snap.min - run[run.length - 1] <= 1.1) run.push(snap.min);
        else {
          if (run) windows.push(run);
          run = [snap.min];
        }
      } else if (run) {
        windows.push(run);
        run = null;
      }
    }
    if (run) windows.push(run);

    for (const w of windows) {
      const start = w[0];
      const end = w[w.length - 1];
      const involved = kills.filter(
        (k) =>
          k.min >= start &&
          k.min <= end + 0.5 &&
          (k.killer === jid || (k.assists ?? []).includes(jid)),
      );
      const died = kills.some(
        (k) => k.min >= start && k.min <= end + 0.5 && k.victim === jid,
      );
      out.push({
        start_min: start,
        end_min: end,
        duration_min: Math.round((end - start) * 10) / 10,
        jungler_champion: board.players[jid].champion,
        jungler_team: board.players[jid].team,
        kills: involved.length,
        died,
      });
    }
  }
  return out;
}

// --- top level --------------------------------------------------------------

export const JUNGLE_CAVEAT =
  "Converted ganks and invade windows are measured. Lane-visit counts are a " +
  "PROXY for attempts: Riot samples positions only once per minute, so failed " +
  "ganks are not directly observable. Never present proxy fields as measured.";

export function detect(board: Board): JungleEvents {
  const meTeam = board.players[board.me_id].team;
  const enemyTeam = 300 - meTeam;

  const ganks = detectGanks(board);
  const visits = detectLaneVisits(board);
  const invades = detectInvades(board);

  const side = (team: number): JungleSideSummary => {
    const g = ganks.filter((k) => k.ganker_team === team);
    const v = visits.filter((x) => x.jungler_team === team);
    const iv = invades.filter((x) => x.jungler_team === team);
    return {
      gank_kills: g.length,
      ganks_on_lanes: Array.from(new Set(g.map((k) => k.lane))).sort(),
      lane_visits_proxy: v.length,
      visits_with_kill_proxy: v.filter((x) => x.kill_within_window).length,
      invade_windows: iv.length,
      invade_kills: iv.reduce((n, x) => n + x.kills, 0),
      invade_deaths: iv.filter((x) => x.died).length,
    };
  };

  return {
    ganks,
    lane_visits: visits,
    invades,
    summary: { me: side(meTeam), enemy_jungler: side(enemyTeam) },
    caveat: JUNGLE_CAVEAT,
  };
}
