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

## Open questions to resolve later

- **Smite/objective presence** — can we tell from `x/y` position + objective event
  whether the player was *in range* of the objective? (needs map geometry)
- **50/50 classification** — how do we label a fight as "statistically correct to
  take" vs "bad decision"? Needs win-probability or expected-value model.
- **Vision** — Riot timeline has no ward/vision data. Is "no vision on their TP
  flank" inferable from anything, or is that out of scope?
- **Micro vs macro** — cleanly separating "you clicked wrong" (micro) from "you
  chose wrong" (macro) from "nothing you could do" (variance) is the hard part.
  Probably needs the LLM layer, not pure heuristics.

---

## Non-goals (for now)

- Live/in-game overlay (post-game only initially)
- Full replay rendering (we describe moments, not re-render them)
- Team/roster management features
