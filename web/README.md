# vod-review web

Next.js (App Router) + TypeScript frontend for vod-review. Talks to Supabase
(Postgres + Auth) for user accounts, saved preferences, and processed match
results. Deploys to Vercel free tier.

The Python backend (`fetch_match.py`, `trends.py`, `moments.py`) lives at the repo
root and is a separate runtime — it writes processed matches into Supabase for
this frontend to display.

## Setup

```bash
npm install
cp .env.example .env.local   # fill in Supabase URL + anon key
npm run dev
```

## Environment variables

| Var | Purpose | Where |
|---|---|---|
| `SUPABASE_URL` | Supabase project URL | server-side (Secret) |
| `SUPABASE_ANON_KEY` | anon key | server-side (Secret) |

Both are **server-side only** (no `NEXT_PUBLIC_` prefix). Auth is done via server
actions, so no Supabase value is exposed to the browser. Set both as regular
(Secret) env vars in the Vercel dashboard for production. The `service_role` key
and DB password are **backend-only** — never put them in Vercel.

## Database

Apply the schema in `supabase/migrations/0001_init.sql` via the Supabase SQL
editor. It creates:

- `profiles` — one row per user (Riot ID, region)
- `preferences` — role, main champions, comparison targets, thresholds
- `matches` — processed games (champion, KDA, ranked moments) written by the backend

All three use Row Level Security (users see only their own rows), plus a trigger
to auto-create profile/preference rows on signup.

## Structure

```
src/
  app/
    login/page.tsx        magic-link email login
    auth/callback/route.ts  exchanges code for session
    dashboard/page.tsx      main view: Riot ID + prefs + recent games
    actions.ts             server actions (save prefs, save Riot ID)
  components/
    PreferencesForm.tsx    role/champions/targets/thresholds
    RiotIdForm.tsx         summoner#TAG
    MatchList.tsx          recent games
  lib/
    supabase/{client,server,middleware}.ts
    types.ts
  proxy.ts                 session-refresh middleware (Next 16 proxy convention)
```
