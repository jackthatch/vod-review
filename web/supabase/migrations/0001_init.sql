-- vod-review schema
-- Run this in the Supabase SQL editor (or via supabase db push).
-- Creates tables + Row Level Security for user accounts and preferences.

-- Profiles: one row per user, keyed to Supabase Auth.
create table if not exists public.profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  email text,
  riot_id text,          -- e.g. "jugking#fines" or null until set
  riot_name text,        -- game name (before the #)
  riot_tag text,         -- tagline (after the #)
  riot_region text,      -- e.g. "na1"
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

-- Preferences: one row per user. Maps to the CLI flags in the Python backend.
create table if not exists public.preferences (
  id uuid primary key references auth.users(id) on delete cascade,
  role text not null default 'JUNGLE',            -- --role
  main_champions text[] not null default '{}',    -- --champion (array)
  comparison_targets text[] not null default '{}',-- pros.json roster subset
  overstay_gold integer not null default 1000,    -- --overstay-gold
  contest_range integer not null default 3000,    -- --range
  objective_window integer not null default 30,   -- --window
  spike_gap_min real not null default 6.0,        -- --gap-min
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

-- Matches: processed game results written by the Python backend (service role).
create table if not exists public.matches (
  id text primary key,                  -- match_id from Riot
  user_id uuid references auth.users(id) on delete cascade,
  champion text,
  role text,
  win boolean,
  duration_min real,
  kda text,                             -- "k/d/a" for quick display
  moments jsonb,                        -- ranked pivotal moments from moments.py
  summary text,                         -- LLM narrative (later)
  fetched_at timestamptz not null default now()
);

-- RLS: users can only read/write their own rows.
alter table public.profiles enable row level security;
alter table public.preferences enable row level security;
alter table public.matches enable row level security;

create policy "profiles_select_own" on public.profiles
  for select using (auth.uid() = id);
create policy "profiles_insert_own" on public.profiles
  for insert with check (auth.uid() = id);
create policy "profiles_update_own" on public.profiles
  for update using (auth.uid() = id);

create policy "preferences_select_own" on public.preferences
  for select using (auth.uid() = id);
create policy "preferences_insert_own" on public.preferences
  for insert with check (auth.uid() = id);
create policy "preferences_update_own" on public.preferences
  for update using (auth.uid() = id);

create policy "matches_select_own" on public.matches
  for select using (auth.uid() = user_id);
create policy "matches_insert_own" on public.matches
  for insert with check (auth.uid() = user_id);
create policy "matches_update_own" on public.matches
  for update using (auth.uid() = user_id);

-- Trigger to auto-create a profile row on signup.
create or replace function public.handle_new_user()
returns trigger as $$
begin
  insert into public.profiles (id, email)
  values (new.id, new.email)
  on conflict (id) do nothing;
  insert into public.preferences (id)
  values (new.id)
  on conflict (id) do nothing;
  return new;
end;
$$ language plpgsql security definer;

drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created
  after insert on auth.users
  for each row execute procedure public.handle_new_user();
