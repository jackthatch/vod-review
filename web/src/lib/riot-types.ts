// riot-types.ts — minimal type surface for the Riot match-v5 / timeline
// payloads consumed by condense.ts and riot.ts.
//
// Riot returns far more than this; only the fields we read are modeled.
// Nullable fields are declared optional to match Riot's habit of omitting
// nulls from JSON.

export interface RiotPosition {
  x: number;
  y: number;
}

export interface RiotDamageStats {
  totalDamageDone?: number;
  totalDamageDoneToChampions?: number;
  totalDamageTaken?: number;
}

export interface RiotChampionStats {
  attackDamage?: number;
}

export interface RiotParticipantFrame {
  level: number;
  xp?: number;
  totalGold: number;
  currentGold: number;
  goldPerSecond?: number;
  minionsKilled: number;
  jungleMinionsKilled: number;
  damageStats?: RiotDamageStats;
  championStats?: RiotChampionStats;
  position: RiotPosition;
}

export interface RiotFrame {
  participantFrames?: Record<string, RiotParticipantFrame>;
  events?: RiotEvent[];
}

export interface RiotEvent {
  timestamp: number;
  type: string;
  position?: Partial<RiotPosition>;
  victimId?: number;
  killerId?: number;
  monsterType?: string;
  monsterSubType?: string;
  killerTeamId?: number;
}

export interface RiotParticipant {
  puuid: string;
  participantId: number;
  teamId: number;
  championName: string;
  teamPosition?: string;
  individualPosition?: string;
  lane?: string;
  role?: string;
  win: boolean;
  kills: number;
  deaths: number;
  assists: number;
  goldEarned?: number;
  totalMinionsKilled?: number;
  neutralMinionsKilled?: number;
  champLevel?: number;
  item0?: number;
  item1?: number;
  item2?: number;
  item3?: number;
  item4?: number;
  item5?: number;
  item6?: number;
  pentaKills?: number;
  quadraKills?: number;
  tripleKills?: number;
  doubleKills?: number;
  riotIdGameName?: string;
  summonerName?: string;
}

export interface RiotInfo {
  participants: RiotParticipant[];
  queueId?: number;
  gameMode?: string;
}

export interface RiotMatch {
  metadata: { matchId: string };
  info: RiotInfo;
}

export interface RiotTimelineInfo {
  frameInterval: number;
  frames: RiotFrame[];
  events?: RiotEvent[];
}

export interface RiotTimeline {
  info: RiotTimelineInfo;
}
