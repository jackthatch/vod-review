// coach.ts — Layer 4: the AI coach (OpenRouter).
//
// Port of coach.py. Ties the deterministic pipeline (condense -> moments ->
// board -> inflection) to an LLM and produces a grounded markdown review:
// overview, key points, deciding moments, review plan, and better decisions.
//
// Every stat fed to the LLM is computed here from the Riot timeline; the LLM
// only interprets, so it can't hallucinate a number.

import type { Moment } from "@/lib/types";
import type { Story } from "@/lib/condense";
import { monsterLabel, situationAt, type Board } from "@/lib/board";
import { analyze as analyzeInflections } from "@/lib/inflection";
import { detect as detectJungleEvents } from "@/lib/jungle_events";
import { analyze as analyzeMoments } from "@/lib/moments";

const OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions";
const DEFAULT_MODEL = process.env.OPENROUTER_MODEL || "anthropic/claude-sonnet-4";

// Which stats the coach may treat as causal evidence vs. mere symptoms.
// Derived from docs/research/jungle/ (Axes 2, 3, 5, 6, 7). Fed to the LLM so it
// cannot present a confounded metric as a verdict.
const STAT_RELIABILITY = {
  use_as_causal: [
    "early deaths (chosen before the outcome, with a mechanism)",
    "first-objective contests (who was committed, numbers, position)",
    "tempo / pathing choices",
    "gank and invade preconditions (vision, priority, duel strength)",
  ],
  confounded_do_not_grade: {
    cs_per_min:
      "falls in a lost game (lost map access); in the JUNGLE it also FALLS with " +
      "rank — over-farming is a low-elo leak",
    kill_participation: "rises because a winning team has more kills to join",
    vision_score:
      "ward-lifetime provided + denied, so winners score higher by construction; " +
      "a purpose-built model beat it at predicting winners",
    gold_diff: "as much an outcome as a cause",
  },
  unmeasured_in_public_data: [
    "gank conversion rate",
    "invade success rate",
    "leaks by rank",
  ],
  reference_effect_sizes: {
    first_blood_win_rate: "~57.6% -> 55.4% (Riot, patches 14.24 -> 25.S1.2)",
    first_turret_win_rate: "~70.4% -> 70.3% (Riot, same period)",
    first_baron_alone: "~50% (coin flip) — Baron matters via conversion",
    mastery_effect: "50+ games on a champion: mean +4.98pp over population",
  },
};

// --- context assembly ------------------------------------------------------

function opponentId(board: Board): number | null {
  const me = board.players[board.me_id];
  for (const [pid, pl] of Object.entries(board.players)) {
    if (pl.team !== me.team && pl.role === me.role) return Number(pid);
  }
  for (const [pid, pl] of Object.entries(board.players)) {
    if (pl.team !== me.team && pl.has_smite) return Number(pid);
  }
  return null;
}

function levelCurve(
  board: Board,
  pid: number,
  atMinutes: number[] = [10, 20],
): Record<number, Record<string, number | null>> {
  const out: Record<number, Record<string, number | null>> = {};
  for (const t of atMinutes) {
    let best: Board["snapshots"][number]["players"][number] | null = null;
    for (const s of board.snapshots) {
      if (s.min <= t) {
        const ps = s.players[pid];
        if (ps) best = ps;
      } else break;
    }
    out[t] = best
      ? { level: best.level, cs: best.cs, gold: best.gold, xp: best.xp }
      : { level: null, cs: null, gold: null, xp: null };
  }
  return out;
}

function trimSituation(sit: ReturnType<typeof situationAt>) {
  const players = (sit.players as Record<string, unknown>[])
    .slice(0, 10)
    .map((p) => {
      const keep = [
        "participant_id",
        "champion",
        "team",
        "role",
        "is_me",
        "lane",
        "location",
        "gold",
        "level",
        "fed",
        "has_tp",
        "likely_dead",
        "near_baron",
        "near_dragon",
      ];
      const o: Record<string, unknown> = {};
      for (const k of keep) if (k in p) o[k] = p[k];
      return o;
    });
  return {
    minute: sit.minute,
    gold_diff: sit.gold_diff,
    dragon_counts: sit.dragon_counts,
    players,
  };
}

export interface CoachContext {
  match_id: string;
  overview: Record<string, unknown>;
  matchup: Record<string, unknown>;
  objectives: Record<string, unknown>[];
  deaths: Record<string, unknown>[];
  pivotal_moments: Record<string, unknown>[];
  inflections: Record<string, unknown>[];
  jungle_events: Record<string, unknown>;
  stat_reliability: Record<string, unknown>;
}

export function buildContext(
  story: Story,
  board: Board,
  topMoments = 4,
  topInflections = 6,
  opts: {
    overstay_gold: number;
    range_units: number;
    window_sec: number;
    gap_min: number;
  } = { overstay_gold: 1000, range_units: 3000, window_sec: 30, gap_min: 6.0 },
): CoachContext {
  const meId = board.me_id;
  const me = board.players[meId];
  const oppId = opponentId(board);

  const s = story.stats;
  const dur = story.duration_min || 1.0;
  const overview: Record<string, unknown> = {
    champion: story.champion,
    role: story.role,
    result: story.win ? "win" : "loss",
    duration_min: story.duration_min,
    opponent: story.opponent_champion,
    kda: `${s.kills}/${s.deaths}/${s.assists}`,
    cs: s.total_cs,
    cs_per_min: Math.round((s.total_cs / dur) * 10) / 10,
    gold: s.gold,
    gold_per_min: Math.round(s.gold / dur),
    first_clear_min: story.first_clear_min,
    kp: null,
    champ_damage_ratio: null,
  };

  // kill participation: (my kills + assists) / team kills
  let teamKills = 0;
  for (const ev of board.events) {
    if (ev.type === "CHAMPION_KILL" && ev.killer != null) {
      const kteam = board.players[ev.killer]?.team;
      if (kteam === me.team) teamKills++;
    }
  }
  const myKp = s.kills + s.assists;
  overview.kp = teamKills ? Math.round((100.0 * myKp) / teamKills) : null;

  // farming-vs-fighting split from the last snapshot
  const lastSnap = story.snapshots[story.snapshots.length - 1];
  if (lastSnap) {
    const td = lastSnap.total_damage ?? 0;
    const tdc = lastSnap.damage_to_champions ?? 0;
    overview.champ_damage_ratio = td ? Math.round((100.0 * tdc) / td) / 10 : null;
  }

  const matchup: Record<string, unknown> = {};
  if (oppId != null) {
    matchup.opponent_champion = board.players[oppId].champion;
    matchup.me = levelCurve(board, meId);
    matchup.opponent = levelCurve(board, oppId);
  }

  const objectives = story.objectives.map((o) => ({
    min: o.min,
    monster: monsterLabel(o.type, o.sub),
    sub: o.sub,
    team: o.team === me.team ? "mine" : "enemy",
    smited_by_me: o.mine,
  }));

  const deaths = story.deaths.map((d) => ({
    min: d.min,
    gold_held: d.current_gold,
  }));

  const rankedMoments = analyzeMoments(story, opts, board);
  const pivotalMoments = rankedMoments.slice(0, topMoments).map((m: Moment) => {
    const entry: Record<string, unknown> = {
      min: m.min,
      type: m.type,
      detail: m.detail,
      score: m.score,
      situation: trimSituation(situationAt(board, m.min)),
    };
    if (m.contest) entry.contest = m.contest;
    return entry;
  });

  const inflections = analyzeInflections(board).slice(0, topInflections).map(
    (ip: Moment) => ({
      min: ip.min,
      type: ip.type,
      detail: ip.detail,
      situation: trimSituation(situationAt(board, ip.min)),
    }),
  );

  // jungle behaviour (ganks / lane presence / invades) — computed from this
  // timeline. Gank kills + invade windows are measured; lane visits are a proxy
  // (Riot samples positions once per minute).
  const je = detectJungleEvents(board);

  return {
    match_id: board.match_id,
    overview,
    matchup,
    objectives,
    deaths,
    pivotal_moments: pivotalMoments,
    inflections,
    jungle_events: {
      summary: je.summary,
      ganks: je.ganks,
      invades: je.invades,
      lane_visits: je.lane_visits,
      caveat: je.caveat,
    },
    stat_reliability: STAT_RELIABILITY,
  };
}

// --- LLM -------------------------------------------------------------------

const SYSTEM_PROMPT = `You are a high-ELO League of Legends coach reviewing a single
solo-queue game from the perspective of the jungler (the "player"). You are given
a deterministic fact-sheet computed from the Riot timeline — every number in it is
accurate; never invent or contradict a number that is given to you. If a fact is
missing (e.g. summoner cooldowns, exact wave state), hedge rather than assert.
Never quote raw map coordinates or distances (no "units", no x/y) — refer to
places by name: "mid lane", "your red buff", "at Dragon pit", "in the river".

EVIDENCE RULES (from a research study of how LoL games are actually won — these
are not optional):

1. CONFOUNDED STATS ARE NEVER VERDICTS. The 'stat_reliability' block lists the
   metrics that are partly CAUSED BY winning rather than causes of it. CS/min,
   kill participation, vision score and raw gold difference all fall in this
   bucket — e.g. CS/min drops in a lost game because you lose map access, and in
   the JUNGLE CS/min actually FALLS as rank rises, so over-farming is a low-elo
   leak, not a win driver. Never write "your CS/min was low, therefore you played
   badly", never grade the player on these, and never use them as the reason a
   game was lost. Use them only as symptoms and say what might lie behind them.
2. EARLY GAME IS A SIGNAL, NOT A VERDICT. First blood is worth only ~55-58% win
   rate and first tower ~70%, and first Baron alone is a coin flip — Baron and
   objectives matter through what you CONVERT them into. Do not frame a first
   death, or a deficit at 15 minutes, as decisive. Weight MID-GAME decision
   points and objective conversions higher.
3. GANK AND INVADE "SUCCESS RATES" ARE UNMEASURED IN PUBLIC DATA — Riot does not
   track ganks. Cite ONLY the gank/invade numbers in the fact-sheet (they are
   computed from this timeline). The lane-visit fields are a PROXY limited by
   Riot's once-per-minute position sampling: failed ganks are not directly
   observable, so hedge them explicitly and never imply a failed gank is known.
4. TASK-LEVEL, NOT EGO-LEVEL. Feedback aimed at the PERSON damages performance —
   over a third of feedback interventions reduce it. Talk only about the PLAY.
   Never about the player's talent, rank, or worth. Not "you're bad at
   tracking" but "this path walked into a blind spot".
5. QUESTION, DON'T ONLY ASSERT. Passive verdicts don't transfer to improvement.
   For the biggest moments, name the decision point, the information available,
   and the fork the player faced, so they can see the alternative themselves.
6. SPECIFIC OVER GENERAL. Depth on one champion is the largest measured driver of
   jungle win rate — bigger than pool breadth. Favour concrete, repeatable
   actions over generic advice.
7. REDUCE TILT. Framing changes performance. Be direct and honest, never harsh;
   end on the single highest-leverage thing to work on.

Your job is to write a concise, actionable review in Markdown with exactly these
sections:

## Game overview
3-5 sentences: the shape of the game, who carried/inted, and the single most
important narrative thread. Reference the player's KDA and the matchup (you may
state CS/gold as CONTEXT, never as a grade).

## Key points
A short bullet list (4-6) of the highest-signal facts: early decisions, the
jungle-events summary (ganks/invades — hedged), objective control and what it was
converted into, level/gold vs. the enemy jungler, death timing. Each bullet states
the fact AND why it mattered. Do not include confounded stats as "key points".

## Deciding moments
For each pivotal moment given, one short paragraph answering three questions:
1. What happened (timestamp + event) and what the player could see at that moment.
2. Why it went the way it did (underleveled, unspent gold, out of position,
   bad fight choice, or just a 50/50 that went the wrong way).
3. The alternative — the better play the player should have made instead.

## Review plan
A prioritized list (top 3) of the specific moments to actually rewatch in the
replay, in order of importance, each with a one-line "what to look for" and a
one-line "why this matters to your long-term improvement".

## Decisions to change
A short list of the concrete decisions the player made that were wrong, each
paired with the decision they should have made instead, phrased as
"Instead of X, you should have Y."

For objective moments (contested_objective / objective_contest), use the
'contest' block when present instead of raw distances. 'team_committed: false'
means the team conceded (few allies at the pit) — that is often the CORRECT
play, not a mistake, so do NOT flag it as an error by default. Judge it against
context: a large gold deficit, allies dead, or a soul point you can't win all
justify giving an objective up. Only call it a mistake when contesting was
actually viable (numbers even/up AND you were in position), or when the team
could have PREPPED better — shoving side waves first and setting up vision so
the objective fight is winnable. If 'soul_point' is true, treat it as
high-stakes. When you discuss wave/lane pressure, hedge: we infer it from player
positions, not exact wave states.

Be direct and specific. Use the player's champion name and the timestamps given.
Do not pad. Total output should be under ~700 words.`;

function buildUserPrompt(ctx: CoachContext): string {
  return (
    "Here is the deterministic fact-sheet for this game:\n\n" +
    JSON.stringify(ctx, null, 2) +
    "\n\nWrite the review now."
  );
}

export async function generateSummary(
  ctx: CoachContext,
  apiKey: string,
  model: string = DEFAULT_MODEL,
): Promise<string> {
  const res = await fetch(OPENROUTER_URL, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${apiKey}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      model,
      messages: [
        { role: "system", content: SYSTEM_PROMPT },
        { role: "user", content: buildUserPrompt(ctx) },
      ],
      max_tokens: 1600,
    }),
  });

  if (!res.ok) {
    const body = await res.text().catch(() => "");
    throw new Error(`OpenRouter ${res.status}: ${body.slice(0, 300)}`);
  }

  const data = (await res.json()) as {
    choices: { message: { content: string } }[];
  };
  return data.choices[0].message.content;
}

export { DEFAULT_MODEL, OPENROUTER_URL };
