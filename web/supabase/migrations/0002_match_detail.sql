-- Add op.gg-style display detail to matches.
-- `detail` is a jsonb blob: { level, kills, deaths, assists, cs, gold, items[],
--   trinket, game_mode, queue, multi_kills[], participants[] }
-- Written by the Python backend (fetch_match.match_detail), read by the web UI.

alter table public.matches add column if not exists detail jsonb;
