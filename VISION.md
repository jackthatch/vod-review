# vod-review — Product Vision

This document captures the long-term direction for the product. It is intentionally
aspirational — not everything here is built. It exists so that incremental work
(fetch → condense → aggregate → coach) has a clear north star.

---

## The core problem

A 30–40 minute League game usually comes down to a **handful of moments**: a lost
objective, a bad fight, a mistimed recall, a missed level spike. Watching the whole
VOD to find them is slow and exhausting, so most players don't. They queue again
carrying the same leak.

## The promise

> Come home from a loss, and within **60 seconds** know exactly which 2–3 moments
> decided the game — and *why* — without watching a full replay.

---

## North-star feature: "Speedrun VOD Review"

Instead of a timeline you scrub through, the product surfaces a **short list of
pivotal moments** ranked by impact.

### Example (the scenario that motivates this)

> *Close game that went wrong somewhere and I'm not sure why.*

The product says:

> **Lost Baron fight at 30:12 → enemy sieged and ended.**
>
> - You were **level 16 vs their jungler's level 17** — down ~300 XP from skipping
>   the 28:00 gromp/wolves cycle to hover mid.
> - You went in holding **1,850g unspent** (no item spike since 24:00).
> - It was a **50/50 smite** — not a micro error, but a **bad fight choice**: your
>   team had no vision on their TP flank, and the correct play was to trade Baron
>   for the bot inhibitor they were already pushing.

The key insight the product must produce: **was this a micro issue, a macro
decision error, or just variance (a 50/50 you should statistically take)?**

### The three questions every "moment" must answer

1. **What happened?** — the objective / fight / death, with a timestamp.
2. **Why did we lose it?** — was I underleveled, unspent-gold, out of position,
   or was it a fair coin-flip that went the other way?
3. **What was the alternative?** — the better play (trade, rotate, back, give it).

---

## How the pieces fit (build path)

1. **Fetch** (`fetch_match.py`) — pull raw match + timeline from Riot. ✅ done
2. **Condense** — turn raw JSON into a per-game "story" with rich snapshots
   (gold, XP, damage, AD, position) and events (deaths, kills, objectives). ✅ done
3. **Aggregate** (`trends.py`) — turn many stories into a *leak profile*: recurring
   patterns across games. ✅ done (first-clear, power-spikes, farming-vs-fighting,
   overstaying, objective control)
4. **Benchmark** — diff your profile against pro solo-queue junglers (`pros.json`)
   to answer "is my 8.0 CS/min actually bad, or normal for this champ?" — next
5. **Moment detection** — algorithmically flag pivotal moments in a single game:
   - objective lost where you had smite up but didn't/weren't there
   - death while holding >N unspent gold (overstay)
   - teamfight you joined while underleveled vs your opposite number
   - power-spike timing gaps (first item landed 2 min later than your average)
6. **Coach layer (LLM grounding)** — turn flagged moments + context into the
   natural-language review above. The JSON is already LLM-ready; the LLM is the
   *last* step, not the whole product.

### Design principle: detection is deterministic, explanation is generative

- **What/why/where** (moments, stats, deltas) → computed from the data, reproducible.
- **Interpretation** (was it a bad fight vs a 50/50, what was the better play) →
  LLM, grounded in the computed facts.

This keeps the product honest: the LLM never hallucinates a stat because the stats
are pre-computed and passed in as context.

---

## To do next — game-state reasoning (the "coach" layer)

**Goal:** surface key inflection points with timestamps, and judge whether a play
was good or bad using full game-state context — e.g. "Baron with your TP toplaner
in the side wave is fine; Baron while your fed ADC is stuck in a side wave away
from the play is not."

Four layers, built bottom-up:

1. **Game-state extractor (`board.py`)** — ingest raw match + timeline and keep the
   FULL board (all 10 players' position/gold/level/items per frame + every event),
   not just "you". Deterministic. ✅ done (+ synthetic smoke test)
2. **Situation builder (`situation_at`)** — given a timestamp, emit a concise
   fact-sheet (who's where, who's fed, objective status, death timers, TP) that
   grounds the LLM. ✅ done
3. **Inflection-point detection (`inflection.py`)** — flag *decisions* on the full
   board: objective contests (when champions converge on a pit, not just who wins
   it), teamfights, cross-map rotations, recalls. Deterministic, chronological
   decision timeline. ✅ done (+ synthetic smoke test)
4. **LLM coach** — feed situation + inflection point to OpenRouter; answer
   what happened / good-or-bad-and-why / the better play. ← next

### Data reality (design around these)

| Fact | Available? |
|---|---|
| Positions/gold/XP/levels (all 10 players) | ✅ timeline frames |
| Item purchases (who's fed) | ✅ `ITEM_PURCHASED` events |
| Objectives, turrets, deaths | ✅ timeline events |
| Wave state | ⚠️ infer from position + minion deltas |
| Vision | ⚠️ partial (`WARD_PLACED`/`WARD_KILLED`) |
| Summoner cooldowns (is TP actually up?) | ❌ not in timeline |

Known gaps to hedge on in the LLM prompt: **TP cooldown** (we know they *have* TP,
not whether it's ready) and **exact wave state**. *(Corrects an earlier note:
`ITEM_PURCHASED` events ARE present in the timeline.)*

---

## Champion select & team-comp analysis (next feature idea)

*Status: idea — partly feasible now, one hard blocker (pick order) documented
below so we don't design around a hole.*

A second feedback axis, orthogonal to the per-game VOD review: help the player
understand **drafting and matchups**, not just in-game decisions. Three related
ideas, with very different feasibility:

### 1. Team-comp analyzer (deterministic — doable now)

The full 10-player roster is already in `detail.participants` (champion + role).
With Data Dragon's `champion.json` (per-champion `tags` + `stats.attackrange`) we
can classify a comp deterministically: ranged vs melee, front-line/engage
presence, waveclear, magic vs physical damage split, hard-CC count.

Concrete output: *"Graves into 5 ranged"* — your team has no front line and no
engage, so the enemy kites you to death. Flag it as a **comp-diff** so the player
knows the loss was partly structural, not pure execution. Same "detection is
deterministic" principle, applied to the draft instead of the game.

### 2. Counterplay / matchup advice (LLM — doable now, extend the coach)

The coach already receives the full roster. Add a matchup-aware section to the
prompt: for your champion vs. your jungle counterpart (and the 1–2 enemy carries),
give concrete micro advice — e.g. *Graves into Sylas: E sideways to dodge E2
(the chains), hold W to space him off melee range, don't let him farm passive
autos off you.* The LLM has this champion knowledge; we just pass the matchup
pairs as grounded context (same pattern as `situationAt`).

### 3. Pick-order analysis (the hard part — likely NOT possible)

"Did I blind-pick Graves into a counter?" requires knowing *when* in the draft
each champion was locked. **MATCH-V5 does not expose pick order** — we get the
final comp and `info.teams[].bans`, but not the draft sequence. The Live Client
Data API exposes champ-select *live* (`/lol-champ-select/v1/session`) but only
during the draft, not post-game. Replay `.rofl` files may contain it but are
version-locked and not worth parsing.

Honest scope: we can analyze the **resulting comp** (ideas 1–2), but not **when
a pick happened**. Any "you should have picked X instead" advice would be guessing
at the draft sequence — don't ship that unless a draft-order source appears.

### Data reality for this axis

| Fact | Available? |
|---|---|
| Final team comp (10 champs + roles) | ✅ `detail.participants` |
| Bans (per team, in order) | ✅ `info.teams[].bans` (ranked queues) |
| Champion range/tags/role | ✅ Data Dragon `champion.json` `tags` + `stats.attackrange` |
| Pick/draft order (who locked when) | ❌ not in MATCH-V5 |
| Live champ-select state | ⚠️ Live Client Data API only, during draft |

### Where it slots in

A **pre-game / draft lens** layered on the same pipeline. Either a standalone
"matchup difficulty" line per game on the dashboard, or a separate draft analyzer
that ingests a (hypothetical or real) comp and scores it. Lower lift than the
coach layer: idea 1 is a Data Dragon lookup + a classifier, idea 2 is a prompt
extension.

---

## Architecture decision: cloud-first, local companion later

**Decision (2026-09):** ship the cloud service first, add a local companion app only
after the cloud product is proven.

### Why cloud-first

Match history is **public data** — anyone with a Riot API key can fetch any
player's matches from their Riot ID (`name#tag` → puuid → match list → timeline).
No OAuth, no RSO login, no local agent, no key-sharing with the player. The
existing `fetch_match.py` + `trends.py` pipeline already runs headless on a server,
so the "cloud reviews your games" model is the *same code we already have* pointed
at more accounts.

### The hard boundary: text vs. video

| Layer | Where it runs | Why |
|---|---|---|
| Analysis + highlights (the writeup) | ☁️ Cloud | MATCH-V5 is public, cloud-friendly |
| Auto-generated video clips | 💻 Local only | Replay API (`127.0.0.1:2999`) requires the *player's own* game client running a replay |

A cloud computer cannot run someone's replay and record clips — the Replay API is
localhost-only. So **text/data highlights are cloud; video clips are a local
companion feature for later.**

### Cloud subscription model

Players subscribe and provide their Riot ID. A cloud bot:

1. **Polls** each subscriber's match history on a cadence (see "no webhook" below).
2. Diffs new matches against what it has already processed.
3. Runs `condense` + `trends` + moment-detection.
4. Produces a **session summary** of findings, delivered at the end of each play
   session (Discord/DM/email/dashboard).

### "No webhook" constraint (must design around)

The Tournament API has server callbacks, but only for tournament-code games. For
normal solo-queue there is **no "game finished" push**. The bot must **poll**.
Implications:

- "End of session" = "next poll after their last game" — inherent few-minute latency.
- A session "ended" vs. "paused" is indistinguishable; key off "no new games for N
  minutes."
- Polling many subscribers × rate limits is the scaling constraint. Dev key (20
  req/s, 100 req/2min) is fine for a handful of beta users; a production key
  (one per product, higher limits) is required at scale, with match-ID caching.

### Riot ToS constraints

- Free tier required if monetized.
- No betting/gambling.
- No MMR/ELO calculators ("ranked-ladder replacement" is off-limits; "jungle leak
  profile" is fine).

### Local companion app (later phase)

Once the cloud findings are well-fleshed-out, a local companion can:
- Auto-record clips of flagged moments via the Replay API (`EnableReplayApi=1`).
- Guide/instruct the user through the findings interactively.
- Provide the richer live data (`wardScore`, exact `playeritems`, full event stream)
  that the Live Client Data API exposes but the remote MATCH-V5 API doesn't.

The cloud bot is a strict superset of the personal-use tool; the local companion is
a *different* runtime (needs the game client), so it's deferred deliberately.

---

## Open questions to resolve later

- **Smite/objective presence** — can we tell from `x/y` position + objective event
  whether the player was *in range* of the objective? Data Dragon's `map11.png`
  minimap + snapshot `x/y` makes this mappable (unlike pure timeline data).
- **50/50 classification** — how do we label a fight as "statistically correct to
  take" vs "bad decision"? Needs win-probability or expected-value model.
- **Vision** — MATCH-V5 timeline has no ward data, BUT the Live Client Data API
  exposes `wardScore` and trinket `playeritems` during live games. Post-game vision
  analysis is limited; live/replay vision is possible via the local client.
- **Item detection** — MATCH-V5 has no item-purchase events, so we infer from AD
  jumps (current heuristic). The Live Client Data API exposes exact `playeritems`
  + `ItemPurchased` events, and Data Dragon `item.json` maps IDs to names.
- **Micro vs macro** — cleanly separating "you clicked wrong" (micro) from "you
  chose wrong" (macro) from "nothing you could do" (variance) is the hard part.
  Probably needs the LLM layer, not pure heuristics.

---

## Non-goals (for now)

- Live/in-game overlay (post-game only initially)
- Full replay rendering (we describe moments, not re-render them)
- Team/roster management features
