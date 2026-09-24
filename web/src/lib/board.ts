// board.ts — full-board game-state extractor (Layer 1 of the coach pipeline).
//
// Port of board.py: extract_board() + situation_at(). Ingests raw match +
// timeline and keeps EVERY player (all 10) across frames, plus the full event
// stream — what game-state reasoning needs (the me-only Story isn't enough to
// judge a macro decision like "Baron with your TP toplaner in the side wave").
//
// situation_at() emits a deterministic fact-sheet at a timestamp to ground the
// LLM coach (Layer 2). All facts are computed; nothing is guessed.

import type {
  RiotEvent,
  RiotMatch,
  RiotTimeline,
} from "@/lib/riot-types";

// --- constants -------------------------------------------------------------

// Summoner spell IDs (Data Dragon).
const FLASH_ID = 4;
const TELEPORT_ID = 12;
const SMITE_ID = 11;

// Objective monster types (timeline `monsterType`).
export const BARON = "BARON_NASHOR";
export const DRAGON = "DRAGON";
const RIFT_HERALD = "RIFTHERALD";
const VOID_GRUBS = "HORDE";
const ATKHAN = "ATKHAN";
export const ELDER = "ELDER_DRAGON";

// Friendly display names for objective monster enums, so the coach/UI say
// "Void Grubs" rather than the raw enum "HORDE".
const MONSTER_NAMES: Record<string, string> = {
  [VOID_GRUBS]: "Void Grubs",
  [DRAGON]: "Dragon",
  [RIFT_HERALD]: "Rift Herald",
  [BARON]: "Baron Nashor",
  [ATKHAN]: "Atakhan",
  [ELDER]: "Elder Dragon",
};
const DRAGON_SUB_NAMES: Record<string, string> = {
  EARTH_DRAGON: "Earth Drake",
  FIRE_DRAGON: "Fire Drake",
  WATER_DRAGON: "Ocean Drake",
  AIR_DRAGON: "Cloud Drake",
  HEXTECH_DRAGON: "Hextech Drake",
  CHEMTECH_DRAGON: "Chemtech Drake",
};

/** Human-friendly objective name; prefers the dragon sub-type when present. */
export function monsterLabel(
  monster: string | null | undefined,
  sub?: string | null,
): string {
  if (sub && DRAGON_SUB_NAMES[sub]) return DRAGON_SUB_NAMES[sub];
  if (monster && MONSTER_NAMES[monster]) return MONSTER_NAMES[monster];
  return monster || "objective";
}

// Approximate map-center coordinates of objective pits (map units).
export const OBJECTIVE_POS: Record<string, { x: number; y: number }> = {
  [BARON]: { x: 4993, y: 10461 },
  [DRAGON]: { x: 9866, y: 4414 },
  [RIFT_HERALD]: { x: 4993, y: 10461 },
  [VOID_GRUBS]: { x: 6652, y: 9690 },
  [ATKHAN]: { x: 8184, y: 6608 },
  [ELDER]: { x: 9866, y: 4414 },
};

// --- types -----------------------------------------------------------------

export interface BoardEvent {
  min: number;
  type: string;
  x: number | null;
  y: number | null;
  killer?: number | null;
  victim?: number | null;
  assists?: number[];
  kill_type?: string | null;
  monster?: string | null;
  sub?: string | null;
  team?: number | null;
  building?: string | null;
  tower?: string | null;
  lane?: string | null;
  item_id?: number | null;
  participant?: number | null;
  ward?: string | null;
  level?: number | null;
  skill?: number | null;
}

export interface PlayerInfo {
  champion: string;
  team: number;
  role: string;
  is_me: boolean;
  summoners: (number | undefined)[];
  has_flash: boolean;
  has_tp: boolean;
  has_smite: boolean;
}

export interface PlayerFrame {
  x: number;
  y: number;
  gold: number | null;
  unspent: number | null;
  level: number | null;
  xp: number | null;
  cs: number;
}

export interface Board {
  match_id: string;
  duration_min: number;
  frame_interval: number;
  me_id: number;
  players: Record<number, PlayerInfo>;
  snapshots: { min: number; players: Record<number, PlayerFrame> }[];
  events: BoardEvent[];
}

// --- extraction ------------------------------------------------------------

function normEvent(ev: RiotEvent): BoardEvent {
  const t = ev.timestamp / 60000.0;
  const pos = ev.position ?? {};
  const e: BoardEvent = {
    min: Math.round(t * 10) / 10,
    type: ev.type,
    x: pos.x ?? null,
    y: pos.y ?? null,
  };
  switch (ev.type) {
    case "CHAMPION_KILL":
      e.killer = ev.killerId ?? null;
      e.victim = ev.victimId ?? null;
      e.assists = ev.assistingParticipantIds ?? [];
      break;
    case "CHAMPION_SPECIAL_KILL":
      e.killer = ev.killerId ?? null;
      e.kill_type = ev.killType ?? null;
      break;
    case "ELITE_MONSTER_KILL":
      e.monster = ev.monsterType ?? null;
      e.sub = ev.monsterSubType ?? null;
      e.team = ev.killerTeamId ?? null;
      e.killer = ev.killerId ?? null;
      break;
    case "BUILDING_KILL":
      e.building = ev.buildingType ?? null;
      e.tower = ev.towerType ?? null;
      e.lane = ev.laneType ?? null;
      e.team = ev.teamId ?? null;
      e.killer = ev.killerId ?? null;
      break;
    case "ITEM_PURCHASED":
    case "ITEM_DESTROYED":
    case "ITEM_SOLD":
    case "ITEM_UNDO":
      e.participant = ev.participantId ?? null;
      e.item_id = ev.itemId ?? null;
      break;
    case "WARD_PLACED":
      e.participant = ev.creatorId ?? null;
      e.ward = ev.wardType ?? null;
      break;
    case "WARD_KILLED":
      e.participant = ev.killerId ?? null;
      e.ward = ev.wardType ?? null;
      break;
    case "LEVEL_UP":
      e.participant = ev.participantId ?? null;
      e.level = ev.level ?? null;
      break;
    case "SKILL_LEVEL_UP":
      e.participant = ev.participantId ?? null;
      e.skill = ev.skillSlot ?? null;
      break;
  }
  return e;
}

export function extractBoard(
  match: RiotMatch,
  timeline: RiotTimeline,
  puuid: string,
): Board {
  const participants = match.info.participants;
  const me = participants.find((p) => p.puuid === puuid);
  if (!me) throw new Error(`puuid ${puuid} not found in match`);

  const ti = timeline.info;
  const frameInterval = ti.frameInterval ?? 60000;
  const frames = ti.frames ?? [];

  // roster: one entry per participant (1..10)
  const players: Record<number, PlayerInfo> = {};
  for (const p of participants) {
    const s1 = p.summoner1Id;
    const s2 = p.summoner2Id;
    const sums = new Set([s1, s2].filter((v): v is number => v != null));
    players[p.participantId] = {
      champion: p.championName,
      team: p.teamId,
      role: p.teamPosition || p.individualPosition || p.lane || "?",
      is_me: p.puuid === puuid,
      summoners: [s1, s2],
      has_flash: sums.has(FLASH_ID),
      has_tp: sums.has(TELEPORT_ID),
      has_smite: sums.has(SMITE_ID),
    };
  }

  // events: embedded per-frame in current API, top-level in older responses
  const rawEvents: RiotEvent[] = ti.events ?? [];
  for (const f of frames) if (f.events) rawEvents.push(...f.events);
  const events = rawEvents.map(normEvent);

  // snapshots: every frame, every player
  const snapshots: Board["snapshots"] = [];
  frames.forEach((f, i) => {
    const fp: Record<number, PlayerFrame> = {};
    for (const [pidStr, pf] of Object.entries(f.participantFrames ?? {})) {
      const pid = Number(pidStr);
      fp[pid] = {
        x: pf.position.x,
        y: pf.position.y,
        gold: pf.totalGold ?? null,
        unspent: pf.currentGold ?? null,
        level: pf.level ?? null,
        xp: pf.xp ?? null,
        cs: (pf.minionsKilled ?? 0) + (pf.jungleMinionsKilled ?? 0),
      };
    }
    snapshots.push({
      min: Math.round((i * frameInterval) / 6000) / 10,
      players: fp,
    });
  });

  return {
    match_id: match.metadata.matchId,
    duration_min: Math.round((frameInterval * frames.length) / 6000) / 10,
    frame_interval: frameInterval,
    me_id: me.participantId,
    players,
    snapshots,
    events,
  };
}

// --- situation builder (Layer 2) ------------------------------------------

export function dist(
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

function snapAt(board: Board, minute: number) {
  let best: Board["snapshots"][number] | null = null;
  for (const s of board.snapshots) {
    if (s.min <= minute) best = s;
    else break;
  }
  return best;
}

export function lane(x: number | null, y: number | null): string {
  if (x == null || y == null) return "unknown";
  if (y > 11500 && x < 9000) return "top";
  if (y < 3300 && x > 5800) return "bot";
  if (x < 1500 || y < 1500) return "base";
  if (x > 13300 || y > 13300) return "enemy_base";
  if (3000 < x && x < 11800 && Math.abs(x - y) < 2600) return "mid";
  return "jungle";
}

function respawnEstimate(level: number, gameMin: number): number {
  const base = 6 + Math.max(level, 1) * 2.5;
  const late = Math.min(20, gameMin * 0.3);
  return Math.min(60.0, base + late);
}

function deathTimes(board: Board): Record<number, number> {
  const deaths: Record<number, number> = {};
  for (const ev of board.events) {
    if (ev.type === "CHAMPION_KILL" && ev.victim != null) {
      deaths[ev.victim] = ev.min;
    }
  }
  return deaths;
}

export interface Situation {
  minute: number;
  gold_diff: number;
  dragon_counts: Record<number, number>;
  objectives: Record<string, unknown>;
  players: Record<string, unknown>[];
}

export function situationAt(board: Board, minute: number): Situation {
  const snap = snapAt(board, minute);
  const players = board.players;
  const meTeam = players[board.me_id].team;
  const gameMin = board.duration_min;

  const gold: Record<number, number> = { 100: 0, 200: 0 };
  if (snap) {
    for (const [pid, ps] of Object.entries(snap.players)) {
      const team = players[Number(pid)].team;
      gold[team] += ps.gold ?? 0;
    }
  }
  const myGold = gold[meTeam] ?? 0;
  const enGold = gold[300 - meTeam] ?? 0;
  const goldDiff = myGold - enGold;

  const objectives: Record<string, unknown> = {};
  const dragonCounts: Record<number, number> = { 100: 0, 200: 0 };
  for (const ev of board.events) {
    if (ev.type !== "ELITE_MONSTER_KILL" || ev.min > minute) continue;
    const m = ev.monster;
    const team = ev.team;
    if (m === DRAGON || m === ELDER) {
      if (team != null && team in dragonCounts) dragonCounts[team] += 1;
    }
    if (m) {
      objectives[m] = { last_taken_min: ev.min, team, sub: ev.sub };
    }
  }

  const deaths = deathTimes(board);
  const fed = new Set<number>();
  if (snap) {
    const ranked = Object.entries(snap.players).sort(
      (a, b) => (b[1].gold ?? 0) - (a[1].gold ?? 0),
    );
    ranked.slice(0, 3).forEach(([pid]) => fed.add(Number(pid)));
  }

  const playerStatus: Record<string, unknown>[] = [];
  for (const pid of Object.keys(players)
    .map(Number)
    .sort((a, b) => a - b)) {
    const pl = players[pid];
    const ps = (snap?.players[pid] as PlayerFrame | undefined) ?? ({} as PlayerFrame);
    const x = ps.x;
    const y = ps.y;
    const lvl = ps.level;
    const lastDeath = deaths[pid];
    const respawn = respawnEstimate(lvl ?? 9, gameMin) / 60.0;
    const likelyDead =
      lastDeath != null && minute - lastDeath < respawn;
    playerStatus.push({
      participant_id: pid,
      champion: pl.champion,
      team: pl.team,
      role: pl.role,
      is_me: pl.is_me,
      lane: lane(x, y),
      x,
      y,
      gold: ps.gold,
      level: lvl,
      fed: fed.has(pid),
      has_tp: pl.has_tp,
      likely_dead: likelyDead,
      last_death_min: lastDeath ?? null,
      dist_baron: dist({ x, y }, OBJECTIVE_POS[BARON]),
      dist_dragon: dist({ x, y }, OBJECTIVE_POS[DRAGON]),
    });
  }

  return {
    minute,
    gold_diff: goldDiff,
    dragon_counts: dragonCounts,
    objectives,
    players: playerStatus,
  };
}
