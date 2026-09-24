// condense.ts — turn raw Riot match + timeline JSON into a structured,
// analysis-ready "story" per match.
//
// Port of condense() / match_detail() / _opponent() / _gold_at() /
// _participant_items() from fetch_match.py. Pure JSON transformation.

import type { MatchDetail, Participant } from "@/lib/types";
import type {
  RiotEvent,
  RiotFrame,
  RiotMatch,
  RiotParticipant,
  RiotTimeline,
} from "@/lib/riot-types";

// Per-frame snapshot of MY state (every ~30–60s).
export type Snapshot = {
  min: number;
  level: number;
  xp: number | null;
  total_gold: number;
  current_gold: number; // gold in pocket (unspent)
  gold_per_second: number | null;
  cs: number;
  jungle_cs: number;
  total_damage: number | null;
  damage_to_champions: number | null;
  damage_taken: number | null;
  attack_damage: number | null;
  x: number;
  y: number;
};

export type Death = {
  min: number;
  killer_id: number | null;
  x: number | null;
  y: number | null;
  current_gold: number | null;
};

export type Kill = {
  min: number;
  victim_id: number | null;
  x: number | null;
  y: number | null;
};

export type Objective = {
  min: number;
  type: string | null;
  sub: string | null;
  team: number | null;
  mine: boolean;
  x: number | null;
  y: number | null;
};

export type Story = {
  match_id: string;
  champion: string;
  role: string;
  participant_id: number;
  team_id: number;
  win: boolean;
  duration_min: number;
  opponent_champion: string;
  stats: {
    kills: number;
    deaths: number;
    assists: number;
    total_cs: number;
    gold: number;
  };
  first_clear_min: number | null;
  snapshots: Snapshot[];
  deaths: Death[];
  kills: Kill[];
  objectives: Objective[];
  detail: MatchDetail;
};

const QUEUE_NAMES: Record<number, string> = {
  400: "Normal Draft",
  420: "Ranked Solo/Duo",
  430: "Normal Blind",
  440: "Ranked Flex",
  450: "ARAM",
  700: "Clash",
  900: "ARURF",
  1020: "One For All",
  1700: "Arena",
};

function pos(p: RiotParticipant): string {
  return p.teamPosition || p.individualPosition || p.lane || "";
}

function opponent(match: RiotMatch, me: RiotParticipant): string {
  const myPos = pos(me);
  for (const p of match.info.participants) {
    if (p.teamId !== me.teamId && pos(p) === myPos) {
      return p.championName;
    }
  }
  return "?";
}

/** current_gold of the last snapshot at or before tMin (minutes). */
function goldAt(snapshots: Snapshot[], tMin: number): number | null {
  let best: number | null = null;
  for (const s of snapshots) {
    if (s.min <= tMin) best = s.current_gold;
    else break;
  }
  return best;
}

/** Final item build (items 0..5) and trinket (item6) for a participant. */
function participantItems(p: RiotParticipant): [number[], number | null] {
  const items = [p.item0, p.item1, p.item2, p.item3, p.item4, p.item5].filter(
    (it): it is number => it != null,
  );
  return [items, p.item6 ?? null];
}

/** Extract the op.gg-style display detail for a match. */
export function matchDetail(match: RiotMatch, meId: number): MatchDetail {
  const me = match.info.participants.find((p) => p.participantId === meId);
  if (!me) {
    throw new Error(`participant ${meId} not found in match`);
  }

  const [mainItems, trinket] = participantItems(me);

  const participants: Participant[] = match.info.participants.map((p) => {
    const [pItems, pTrinket] = participantItems(p);
    return {
      participant_id: p.participantId,
      champion: p.championName,
      team: p.teamId,
      role: p.teamPosition || p.individualPosition || "?",
      kills: p.kills ?? 0,
      deaths: p.deaths ?? 0,
      assists: p.assists ?? 0,
      level: p.champLevel ?? null,
      gold: p.goldEarned ?? 0,
      cs: (p.totalMinionsKilled ?? 0) + (p.neutralMinionsKilled ?? 0),
      items: pItems,
      trinket: pTrinket,
      is_me: p.participantId === meId,
      summoner: p.riotIdGameName || p.summonerName || null,
    };
  });

  const multi: string[] = [];
  if (me.pentaKills) multi.push("penta");
  if (me.quadraKills) multi.push("quadra");
  if (me.tripleKills) multi.push("triple");
  if (me.doubleKills) multi.push("double");

  const qid = match.info.queueId;

  return {
    level: me.champLevel ?? null,
    kills: me.kills ?? 0,
    deaths: me.deaths ?? 0,
    assists: me.assists ?? 0,
    cs: (me.totalMinionsKilled ?? 0) + (me.neutralMinionsKilled ?? 0),
    gold: me.goldEarned ?? 0,
    items: mainItems,
    trinket,
    game_mode: match.info.gameMode ?? null,
    queue: qid != null ? (QUEUE_NAMES[qid] ?? `Queue ${qid}`) : null,
    multi_kills: multi,
    participants,
  };
}

/** Turn raw match + timeline into a structured, analysis-ready Story. */
export function condense(
  match: RiotMatch,
  timeline: RiotTimeline,
  puuid: string,
): Story {
  const info = match.info;
  const me = info.participants.find((p) => p.puuid === puuid);
  if (!me) {
    throw new Error(`puuid ${puuid} not found in match`);
  }
  const myId = me.participantId;
  const myTeam = me.teamId;

  const fi = timeline.info.frameInterval; // ms per frame
  const frames = timeline.info.frames;
  const durationMin = Math.round((fi * frames.length) / 6000) / 10;

  // Per-frame snapshot of MY state.
  const snapshots: Snapshot[] = [];
  frames.forEach((f: RiotFrame, i: number) => {
    const pf = f.participantFrames?.[String(myId)];
    if (!pf) return;
    const ds = pf.damageStats ?? {};
    const cs = pf.championStats ?? {};
    snapshots.push({
      min: Math.round((i * fi) / 6000) / 10,
      level: pf.level,
      xp: pf.xp ?? null,
      total_gold: pf.totalGold,
      current_gold: pf.currentGold,
      gold_per_second: pf.goldPerSecond ?? null,
      cs: pf.minionsKilled + pf.jungleMinionsKilled,
      jungle_cs: pf.jungleMinionsKilled,
      total_damage: ds.totalDamageDone ?? null,
      damage_to_champions: ds.totalDamageDoneToChampions ?? null,
      damage_taken: ds.totalDamageTaken ?? null,
      attack_damage: cs.attackDamage ?? null,
      x: pf.position.x,
      y: pf.position.y,
    });
  });

  // Events may be top-level (older API) or embedded per-frame (current API).
  const events: RiotEvent[] = timeline.info.events ?? [];
  for (const f of frames) {
    if (f.events) events.push(...f.events);
  }

  const deaths: Death[] = [];
  const kills: Kill[] = [];
  const objectives: Objective[] = [];

  for (const ev of events) {
    const t = ev.timestamp / 60000.0; // minutes
    const et = ev.type;
    if (et === "CHAMPION_KILL") {
      const p = ev.position ?? {};
      if (ev.victimId === myId) {
        deaths.push({
          min: Math.round(t * 10) / 10,
          killer_id: ev.killerId ?? null,
          x: p.x ?? null,
          y: p.y ?? null,
          current_gold: goldAt(snapshots, t),
        });
      } else if (ev.killerId === myId) {
        kills.push({
          min: Math.round(t * 10) / 10,
          victim_id: ev.victimId ?? null,
          x: p.x ?? null,
          y: p.y ?? null,
        });
      }
    } else if (et === "ELITE_MONSTER_KILL") {
      const p = ev.position ?? {};
      objectives.push({
        min: Math.round(t * 10) / 10,
        type: ev.monsterType ?? null,
        sub: ev.monsterSubType ?? null,
        team: ev.killerTeamId ?? null,
        mine: ev.killerId === myId,
        x: p.x ?? null,
        y: p.y ?? null,
      });
    }
  }

  // First full clear: first frame where I've taken 6 jungle camps.
  let firstClear: number | null = null;
  for (const s of snapshots) {
    if (s.jungle_cs >= 6) {
      firstClear = s.min;
      break;
    }
  }

  const totalCs = (me.totalMinionsKilled ?? 0) + (me.neutralMinionsKilled ?? 0);

  return {
    match_id: match.metadata.matchId,
    champion: me.championName,
    role: me.teamPosition || me.individualPosition || me.role || "?",
    participant_id: myId,
    team_id: myTeam,
    win: me.win,
    duration_min: durationMin,
    opponent_champion: opponent(match, me),
    stats: {
      kills: me.kills,
      deaths: me.deaths,
      assists: me.assists,
      total_cs: totalCs,
      gold: me.goldEarned ?? 0,
    },
    first_clear_min: firstClear,
    snapshots,
    deaths,
    kills,
    objectives,
    detail: matchDetail(match, myId),
  };
}
