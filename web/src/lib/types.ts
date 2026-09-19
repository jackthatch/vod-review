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

export type Match = {
  id: string;
  champion: string;
  role: string;
  win: boolean;
  duration_min: number;
  kda: string;
  moments: Moment[] | null;
  summary: string | null;
  fetched_at: string;
};
