export type Preferences = {
  role: string;
  main_champions: string[];
  comparison_targets: string[];
  overstay_gold: number;
  contest_range: number;
  objective_window: number;
  spike_gap_min: number;
};

export type Profile = {
  id: string;
  email: string | null;
  riot_id: string | null;
  riot_name: string | null;
  riot_tag: string | null;
  riot_region: string | null;
};

export type Moment = {
  type: string;
  min: number;
  detail: string;
  score: number;
  [key: string]: unknown;
};

export type Participant = {
  participant_id: number;
  champion: string;
  team: number;
  role: string;
  kills: number;
  deaths: number;
  assists: number;
  level: number | null;
  gold: number;
  cs: number;
  items: number[];
  trinket: number | null;
  is_me: boolean;
  summoner: string | null;
};

export type MatchDetail = {
  level: number | null;
  kills: number;
  deaths: number;
  assists: number;
  cs: number;
  gold: number;
  items: number[];
  trinket: number | null;
  game_mode: string | null;
  queue: string | null;
  multi_kills: string[];
  participants: Participant[];
};

export type Match = {
  id: string;
  champion: string;
  role: string;
  win: boolean;
  duration_min: number;
  kda: string;
  moments: Moment[] | null;
  summary: string | null;
  coach_context?: Record<string, unknown> | null;
  detail: MatchDetail | null;
  fetched_at: string;
};
