# Known Issues

Outstanding problems and desired changes for vod-review, tracked in one place.
Each entry: what's wrong now, what it should do, and any relevant notes. Add new
entries at the top of the "Open" list; move to "Resolved" with a date + commit
when fixed.

---

## Open

### 1. Missing static images in the game detail panel

**Status:** needs root-cause confirmation against the screenshot.

Some champion/item icons fail to load in the match detail / participants panel,
rendering as broken or blank images. Likely causes already spotted in the code
(to confirm which one(s) are actually firing):

- **Empty item slots render as `item/0.png`.** `condense.ts` →
  `participantItems()` filters with `it != null`, which **keeps item id `0`**
  (empty slots). `itemIcon(0)` → `https://ddragon.../img/item/0.png` → 404.
  The Python `_participant_items()` uses `[i for i in items if i]`, which drops
  `0` — the TS port diverged and now renders a broken icon for every empty slot.
- **Hardcoded Data Dragon version.** `ddragon.ts` pins `VERSION = "16.18.1"`.
  Any champion/item added in a later patch 404s. Old versions stay hosted, so
  this only bites new content — but it will silently break as patches ship.
- **Champion-name edge cases.** `championName` → DDragon filename is 1:1 for
  most champions, but a few (Renata, K'Sante, Nunu) may need a small alias map.

**Desired:** every champion + item icon resolves; empty slots are skipped, not
rendered.

**Notes:** need the screenshot to confirm which icons are actually missing
(champion portraits vs. item squares, and which ones).

---

### 2. Split the Riot ID input into three fields

**Status:** not started.

Currently `RiotIdForm.tsx` is a single `summoner#TAG` text box; the server
parses `name#TAG` and **region is not even in the form** (it silently defaults
to `na1` in `actions.ts`). Desired:

- A **region picklist** (`na1`, `euw1`, `eun1`, `kr`, `jp1`, `br1`, `la1`,
  `la2`, `oc1`, `tr1`, `ru`, `sg2`, `tw2`, `vn2`, `ph2`).
- A **name** text entry and a separate **tag** text entry, with a literal `#`
  rendered between them (e.g. `[NA] [jugking] # [mutt]`).
- `saveRiotId` (and `Profile`) already store `riot_name`, `riot_tag`,
  `riot_region` separately — the form just needs to send all three instead of a
  single parsed string.

**Desired:** `[Region ▾] jugking # mutt [Save]` — three explicit inputs, no
server-side string parsing, region is user-selectable.

---

### 3. Account switching must scope recent games to the current Riot account

**Status:** not started.

`matches` is keyed only by `user_id` (Supabase auth user), and RLS scopes reads
to `auth.uid() = user_id`. When a user changes their Riot ID to a *different
account*, the old account's games are still under the same `user_id`, so they
mix with the new account's games.

**Desired:** switching Riot accounts reloads the recent-games screen to show
**only** the currently selected player's matches.

**Approach (to confirm):** scope matches by the Riot identity, not just the
Supabase user — e.g. add a `puuid` (or `riot_name`/`riot_tag`) column to
`matches` and filter the dashboard query by the current profile's puuid. The
`puuid` is already resolved during fetch; it just isn't persisted on the row
today.

---

### 4. `board.py`/`inflection.py` field names unverified against live data

**Status:** open (blocked on a Riot dev key + live fetch).

`board.py`, `board.ts`, `inflection.py`, `inflection.ts` are built against the
*documented* MATCH-V5 schema and pass synthetic-fixture smoke tests, but have
not yet run against a real match. One live `fetch_match.py --count 1` + eyeball
is needed to confirm real field names (esp. per-frame `events` vs top-level
`events`) before trusting the coach layer end-to-end.

---

## Resolved

### AI recap moved off the fetch path → on-demand + cached (2026-09-24)

The LLM call used to run inline in `fetchAndAnalyze` (one call per match, up to
5) — a serverless-timeout risk and a silent-failure trap. Now:

- `fetchAndAnalyze` is **deterministic only** (condense + moments + build the
  coach fact-sheet, no LLM) — fast, no timeout risk.
- The recap is generated **on demand** via a "Get AI recap" button
  (`generateRecap` server action), then saved to `matches.summary` — viewing it
  later never regenerates.
- The deterministic fact-sheet is stored in `matches.coach_context` at fetch
  time so the recap button needs no Riot round-trips.

Requires migration `0003_coach_context.sql`. Existing rows fetched before this
change have no `coach_context` and must be re-fetched to enable the button.
