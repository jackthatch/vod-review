"use server";

import { createClient } from "@/lib/supabase/server";
import { revalidatePath } from "next/cache";
import type { Preferences } from "@/lib/types";
import { Riot } from "@/lib/riot";
import { condense, type Story } from "@/lib/condense";
import { analyze } from "@/lib/moments";
import { extractBoard } from "@/lib/board";
import { buildContext, generateSummary } from "@/lib/coach";

export async function savePreferences(input: Preferences) {
  const supabase = await createClient();
  const {
    data: { user },
  } = await supabase.auth.getUser();
  if (!user) {
    return { error: "Not authenticated" };
  }

  const { error } = await supabase
    .from("preferences")
    .upsert({ id: user.id, ...input, updated_at: new Date().toISOString() });

  if (error) {
    return { error: error.message };
  }

  revalidatePath("/dashboard");
  return { ok: true };
}

export async function saveRiotId(riotId: string) {
  const supabase = await createClient();
  const {
    data: { user },
  } = await supabase.auth.getUser();
  if (!user) {
    return { error: "Not authenticated" };
  }

  // Parse "name#TAG" into its parts.
  let name = riotId.trim();
  let tag = "";
  const hash = name.indexOf("#");
  if (hash !== -1) {
    tag = name.slice(hash + 1).trim();
    name = name.slice(0, hash).trim();
  }

  const { error } = await supabase
    .from("profiles")
    .upsert({
      id: user.id,
      riot_id: riotId.trim() || null,
      riot_name: name || null,
      riot_tag: tag || null,
      updated_at: new Date().toISOString(),
    });

  if (error) {
    return { error: error.message };
  }

  revalidatePath("/dashboard");
  return { ok: true };
}

// Send a magic-link email. `origin` is passed from the client so the redirect
// works on any deployment URL (production, preview, localhost).
export async function signInWithEmail(email: string, origin: string) {
  const supabase = await createClient();
  const { error } = await supabase.auth.signInWithOtp({
    email,
    options: {
      emailRedirectTo: `${origin}/auth/callback`,
    },
  });
  if (error) {
    return { error: error.message };
  }
  return { ok: true };
}

export async function signOut() {
  const supabase = await createClient();
  await supabase.auth.signOut();
}

// Shape a condensed Story into the `matches` row the web app reads.
// `summary` is intentionally NOT included: the AI recap is generated on demand
// (generateRecap) and we don't want a re-fetch to clobber a saved recap.
function matchPayload(
  story: Story,
  moments: ReturnType<typeof analyze>,
  coachContext: ReturnType<typeof buildContext> | null,
) {
  const s = story.stats;
  return {
    id: story.match_id,
    champion: story.champion,
    role: story.role,
    win: story.win,
    duration_min: story.duration_min,
    kda: `${s.kills}/${s.deaths}/${s.assists}`,
    moments, // jsonb — list of ranked moment dicts
    coach_context: coachContext, // jsonb — deterministic fact-sheet for the recap
    detail: story.detail, // jsonb — items, roster, cs/gold, queue
  };
}

// On-demand "fetch + analyze my latest games". Runs server-side: resolves the
// user's Riot ID + region + preference thresholds, pulls match + timeline from
// the Riot API, condenses each game, flags moments, builds the deterministic
// coach context, and upserts the results. NO LLM call here — the AI recap is a
// separate on-demand action (see generateRecap).
export async function fetchAndAnalyze(count = 3): Promise<{
  error?: string;
  count?: number;
  warnings?: string[];
}> {
  const supabase = await createClient();
  const {
    data: { user },
  } = await supabase.auth.getUser();
  if (!user) {
    return { error: "Not authenticated" };
  }

  const { data: profile } = await supabase
    .from("profiles")
    .select("riot_name, riot_tag, riot_region")
    .eq("id", user.id)
    .single();

  const { data: prefs } = await supabase
    .from("preferences")
    .select("*")
    .eq("id", user.id)
    .single();

  const name = profile?.riot_name;
  const tag = profile?.riot_tag;
  const region = profile?.riot_region || "na1";
  if (!name || !tag) {
    return { error: "Set your Riot ID first (summoner#TAG)." };
  }

  const apiKey = process.env.RIOT_API_KEY;
  if (!apiKey) {
    return {
      error:
        'Server is missing "RIOT_API_KEY". Set it in Vercel → Settings → ' +
        "Environment Variables (as a Secret), then redeploy.",
    };
  }

  // Cap the request small to stay inside serverless timeouts (each game = 2
  // Riot calls; no LLM here, so this is fast).
  const capped = Math.max(1, Math.min(Math.floor(count), 5));

  const opts = {
    overstay_gold: prefs?.overstay_gold ?? 1000,
    range_units: prefs?.contest_range ?? 3000,
    window_sec: prefs?.objective_window ?? 30,
    gap_min: prefs?.spike_gap_min ?? 6.0,
  };

  const riot = new Riot(apiKey, region);
  const warnings: string[] = [];
  let payloads: ReturnType<typeof matchPayload>[];
  try {
    const puuid = await riot.puuid(name, tag);
    const ids = await riot.matchIds(puuid, capped);

    payloads = [];
    for (const mid of ids) {
      const match = await riot.match(mid);
      const tl = await riot.timeline(mid);
      const story = condense(match, tl, puuid);

      // Deterministic coach fact-sheet (no LLM) — stored so the recap button
      // doesn't need to re-fetch Riot data later.
      let board: ReturnType<typeof extractBoard> | null = null;
      let coachContext: ReturnType<typeof buildContext> | null = null;
      try {
        board = extractBoard(match, tl, puuid);
        coachContext = buildContext(story, board, 4, 6, opts);
      } catch (e) {
        console.error(`coach context failed for ${mid}:`, e);
        warnings.push(`Analysis context failed for one game.`);
      }

      // Enrich moment detection with the full board (contest context for
      // objectives: who was at the pit, soul stakes, etc.).
      const moments = analyze(story, opts, board);

      payloads.push(matchPayload(story, moments, coachContext));
    }
  } catch (e) {
    return { error: e instanceof Error ? e.message : "Fetch failed" };
  }

  const { error } = await supabase
    .from("matches")
    .upsert(payloads.map((p) => ({ ...p, user_id: user.id })));

  if (error) {
    return { error: error.message };
  }

  revalidatePath("/dashboard");
  return {
    count: payloads.length,
    warnings: warnings.length ? warnings : undefined,
  };
}

// On-demand AI recap for a single match. Reads the stored coach context, calls
// the LLM once, and persists the result in matches.summary so viewing it later
// never regenerates it. Returns the saved recap.
export async function generateRecap(matchId: string): Promise<{
  error?: string;
  summary?: string;
}> {
  const supabase = await createClient();
  const {
    data: { user },
  } = await supabase.auth.getUser();
  if (!user) {
    return { error: "Not authenticated" };
  }

  const { data: row } = await supabase
    .from("matches")
    .select("id, summary, coach_context")
    .eq("id", matchId)
    .eq("user_id", user.id)
    .single();

  if (!row) {
    return { error: "Match not found." };
  }
  // Already generated — return the saved recap (no LLM call, no refetch).
  if (row.summary) {
    return { summary: row.summary as string };
  }

  const apiKey = process.env.OPENROUTER_API_KEY;
  if (!apiKey) {
    return {
      error:
        "Server is missing OPENROUTER_API_KEY. Set it in Vercel → Settings → " +
        "Environment Variables, then redeploy.",
    };
  }

  if (!row.coach_context) {
    return {
      error:
        "No saved analysis for this game — click “Fetch latest games” first, " +
        "then generate the recap.",
    };
  }

  let summary: string;
  try {
    summary = await generateSummary(
      row.coach_context as Parameters<typeof generateSummary>[0],
      apiKey,
    );
  } catch (e) {
    return { error: e instanceof Error ? e.message : "Recap failed" };
  }

  const { error } = await supabase
    .from("matches")
    .update({ summary })
    .eq("id", matchId)
    .eq("user_id", user.id);
  if (error) {
    return { error: error.message };
  }

  revalidatePath("/dashboard");
  return { summary };
}

