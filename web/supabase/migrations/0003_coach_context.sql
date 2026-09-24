-- Store the deterministic coach fact-sheet (buildContext output) per match.
--
-- The AI recap is generated ON DEMAND (a button), not during fetch. To build
-- the recap we need the grounded context (overview, matchup, pivotal moments +
-- situations, inflections + situations). Rather than re-fetch the raw
-- match+timeline from Riot every time a recap is requested, we compute the
-- context once at fetch time (deterministic, no LLM) and store it here. The
-- recap button then only needs an LLM call — no Riot round-trips.
--
-- `summary` (the generated markdown recap) lives in the existing
-- matches.summary column and is written when the recap is first generated, so
-- viewing it later never regenerates it.

alter table public.matches add column if not exists coach_context jsonb;
