# Axis 1 — How games are actually decided in solo queue

> **Research run 2** (2026-09-24/25). Full rewrite of the provisional run-1 file.
> Question: in LoL solo queue, *what actually decides games* — is it snowball-driven
> or closer to a coin flip, and how much predictive weight does the early game
> carry versus the late game?
>
> **Source discipline:** every claim is cited with a source + date. Unsourced claims
> are marked `confidence: Low`. Critical claims carry ≥2 independent sources where
> available. Patch-dependent facts are dated and marked **PERISHABLE**.
>
> **Patch context:** this file was compiled against the **patch 16.x** era
> (LoLalytics served "Patch 16.19" on 2026-09-25). **Atakhan, Blood Roses and
> Feats of Strength were REMOVED in patch 26.1 (2026)** and are *not* live
> mechanics — treat run-1 prose that leans on them with suspicion.
> See [`03-objective-value.md`](03-objective-value.md) for the objective-removal detail.

---

## TL;DR (headline findings)

1. **Outcome is weak-to-moderate, not decided, in the first ~15 minutes.** Riot's own
   professional win-probability model lists *gold %*, team XP, towers, dragons/soul,
   Herald, Baron/Elder timers and players-alive as its features — and public demos of
   it sit near 50/50 early, only becoming confident late. Early state is a *signal*,
   not a verdict.
2. **First Blood is worth only ~55–58% win rate; First Turret ~70%** — measured by
   Riot, patch 14.24 → 25.S1.2 (2024-2025). Substantial, but nowhere near "the game
   is over."
3. **Snowballing and comebacks are a *designed equilibrium*, not a runaway.** Riot
   explicitly ships "anti-snowball" levers (bounty gold, comeback XP, chained
   objective compensation) and peer-reviewed work models the balance explicitly.
4. **ML papers that claim 95–97% accuracy are almost certainly using end-of-game
   state (data leakage)** and should not be read as "games are decided early."
   Careful real-time work lands at **~81.6% accuracy by 60–80% elapsed game time**,
   with early-game discrimination close to chance.
5. **Solo-queue-specific measured curves (X gold @ 15 min → Y% win rate) remain the
   biggest gap.** No public, rank-banded, patch-stamped number was found this run.

---

## 1. What the actual win condition *is*

LoL is a **single terminal objective** game: you win by destroying the enemy Nexus
(standard Summoner's Rift rules). Everything else — kills, gold, objectives, towers —
is instrumental. This sounds trivial but it drives the analysis: any statistic is
only predictive **to the extent it moves the probability of reaching the Nexus first.**

- **Terminal condition:** enemy Nexus destroyed (or enemy surrender / remake).
- **Instrumental resources:** gold, XP, tempo, map control, objective buffs — all
  translate to win probability *indirectly*.

There is no shared-clock "score" win condition on Summoner's Rift. This is why the
research question is really *"how much does a given mid-game state shift the
probability of the terminal event."*

*Confidence: High (game rules). Tier: Established.*

---

## 2. Early lead → win: what is actually measured

### 2.1 Riot's own objective-win-rate numbers (measured)

Riot's **"/dev: How the Season 1 Changes Landed"** (published **2025-02-07**) gives a
"Percent Win Rate after Claiming Each Objective" table — but **only for First Blood and
First Turret**:

| Objective | Patch 14.24 | Patch 25.S1.2 |
|---|---|---|
| First Blood | **57.6%** | **55.4%** |
| First Turret | **70.4%** | **70.3%** |

Riot's conclusion: *"these metrics haven't substantially changed from 14.24, so game
pacing and overall snowballing are in roughly the same place as before Season 1."*

Source: [Riot /dev — How the Season 1 Changes Landed](https://www.leagueoflegends.com/en-us/news/dev/dev-how-the-season-1-changes-landed/) (published 2025-02-07; fetched 2026-09-25).
**PERISHABLE** (patch-tied). **Rank band: not stated by Riot** — likely all-ranks
internal telemetry; treat as non-solo-queue-specific. Confidence: Medium (primary
Riot statement, but rank band and sample size unpublished). Tier: Primary.

**Read:** First Blood moving the needle only ~55% means the *first kill is close to
noise*. First Turret at ~70% is much stronger — it bundles plate gold, lane
dominance, and map access, so it is a *better early-game proxy for real advantage*
than kills. **Drakes, Voidgrubs, Herald, Baron and Atakhan were NOT in that table.**

> Cross-check (independent, different era): Riot has repeatedly framed first blood /
> first tower as *small* early swings they deliberately de-weighted by removing their
> bonus gold in Season 2025. Same source, above. This is corroboration of direction,
> not of the exact number.

### 2.2 How much of the outcome is predictable *when*? (measured, across studies)

The cleanest way to answer "early vs late" is to compare **prediction accuracy as a
function of how much of the game has elapsed.** The studies that report this:

| Study | Data | Predicts from | Accuracy | Notes |
|---|---|---|---|---|
| arXiv 2108.02799 (2021) | Ranked LoL, champion-mastery DNN | **Before the game** (post-draft) | **75.1%** | Champion mastery alone predicts 3-in-4 games **before gameplay starts** |
| ICITR 2024 — "Kills or Turrets" | Early-game features | **First 10 min** | **74.4%** | Probabilistic SVM + RNN; authors note late-game "significant snowballing" |
| ICPEGE 2026 — "Evolution of the Model" | 39→23 features, mid-game | **Mid-game** | **76.37–76.47%** (AUC 0.8435) | **"Economic ratio and difference features have the highest predictive power"** |
| arXiv 2309.02449 (2023) | In-game state, LightGBM | **60–80% elapsed time** | **81.62%** | Best on the mid/late window; *early* models were worst |
| IEEE GEM 2022 — "Snowball Effect Perspectives" | Riot API time series, 76 position features, LSTM/GRU/RNN | **Real-time (end-state)** | **>91%** | Real-time "advantageous team" classification |
| CHBR 2025 — deep-learning KPIs | **154,000 games** (Riot API), NN | (end-state) | **97%** | Top KPI order: **turrets lost > bounty > turrets destroyed > damage taken > dragons** |

Sources:
- [arXiv:2108.02799](https://arxiv.org/abs/2108.02799) (2021-08; fetched 2026-09-25)
- [10.1109/icitr64794.2024.10857792](https://doi.org/10.1109/icitr64794.2024.10857792) (ICITR 2024; abstract via OpenAlex, fetched 2026-09-25)
- [10.1109/icpege67691.2026.11451276](https://doi.org/10.1109/icpege67691.2026.11451276) (ICPEGE 2026; abstract via OpenAlex, fetched 2026-09-25)
- [arXiv:2309.02449](https://arxiv.org/abs/2309.02449) (2023-09; fetched 2026-09-25)
- [10.1109/gem56474.2022.10017891](https://doi.org/10.1109/gem56474.2022.10017891) (IEEE GEM 2022; abstract via OpenAlex, fetched 2026-09-25)
- [10.1016/j.chbr.2025.100718](https://doi.org/10.1016/j.chbr.2025.100718) (*Computers in Human Behavior Reports* 2025; abstract via OpenAlex, fetched 2026-09-25)

**Interpretation — three reads, all defensible:**
1. **Early is genuinely weak:** 74–76% after the *first 10 minutes to mid-game* is
   well short of certainty. And the arXiv 2309.02449 model was *worst* early, only
   reaching 81.6% by ~70% game time.
2. **But early is NOT a coin flip:** a *pre-game* (draft-only) model already hits
   **75.1%** (arXiv 2108.02799). So ~¾ of the variance is tied to things knowable
   before the game even starts — **matchmaking and champion mastery** — not to
   in-game snowballing. This is an important nuance the "everything is a coin flip"
   framing misses.
3. **Mid-game economy is the single best mid-game predictor** (ICPEGE 2026:
   "economic ratio and difference features have the highest predictive power").
   Consistent with Riot's WP model using *gold %* as a core feature.

**The 97% figure is not evidence of early decisiveness.** CHBR 2025's 97% and GEM
2022's >91% are **full-game / end-state** predictions, and include late-game state as
features — classic leakage. `confidence: Low` as evidence about *early* decidedness.

### 2.2b Beware leakage-inflated "95–97%" claims

Several ML papers report suspiciously high win-prediction accuracy:
- *Acta Infologica* 2024 — [10.26650/acin.1180583](https://doi.org/10.26650/acin.1180583)
- *Applied Sciences* 2025 — [10.3390/app15105241](https://doi.org/10.3390/app15105241)

These are `confidence: Low` **as evidence that games are decided early.** High accuracy
in win-prediction papers almost always means the feature set included late/end-of-game
state (gold difference, towers remaining, inhibitors) — a *leaky* predictor that is
useless as an early-game signal. Do not cite them as "the game is over early."

### 2.4 The unresolved conflict: DotA 2 says early is decisive

- **IEEE Transactions on Games 2019** ([10.1109/tg.2019.2948469](https://doi.org/10.1109/tg.2019.2948469))
  reportedly claimed **~85% accuracy after just 5 minutes** in professional DotA 2.

This is **far more early-decisive than any LoL figure** found. It is a *different game*
and a *different epoch*. **Unreconciled.** Flagged as a genuine conflict; do not treat
either figure as universal.

---

## 3. Snowball vs comeback: a designed equilibrium

### 3.1 Riot ships explicit anti-snowball levers

From the same Riot /dev (2025-02-07): Riot lists deliberate anti-snowball changes —
*"early homeguards, increasing XP range, and removing the gold from First Blood & First
Turret"* — and introduced comeback levers elsewhere. Riot's stated post-season-1
reading was that pacing and snowballing were **unchanged**, i.e. these levers roughly
offset the new snowball sources. Source: Riot /dev (2025-02-07), as above.
Confidence: Medium. Tier: Primary.

### 3.2 Academic modelling of comeback mechanics

- **IEEE TVCG 2016** ([10.1109/tvcg.2016.2598415](https://doi.org/10.1109/tvcg.2016.2598415))
  — treats snowballing and comebacks as a **designed balance** rather than a runaway
  process.
- **Electronics 2025** ([10.3390/electronics14071445](https://doi.org/10.3390/electronics14071445))
  — explicitly models **comeback behaviour via the bounty system**.

Both are `confidence: Medium`, tier: Primary (peer-reviewed journals). Neither gives a
clean solo-queue "gold-lead → win%" curve, but together they establish that
**comebacks are a first-class, modelled mechanic**, not an anomaly.

---

## 4. Riot's win-probability model: what Riot itself treats as decisive

Riot's public **Win Probability** feature (Worlds 2023; previously "Win Expectancy")
is an **xgboost** model trained on **professional games since patch 10.4**,
continuously retrained. Per Riot's product lead ("Riot JPham"), its features are:

- Game time
- **Gold percentage** (a player's share of total game gold) — note: *share*, not raw diff
- Total team XP
- Number of players alive
- Tower kills
- Dragon kills (incl. whether a team holds **dragon soul**)
- Herald trinket in inventory
- Inhibitor respawn timers
- Baron buff expiry timers / players with Baron active
- Elder buff expiry timers / players with Elder active

Sources:
- [Esports.net summary of Riot JPham](https://www.esports.net/news/lol/riot-games-explains-win-probability-for-lol-worlds-2023/) (published 2025-02-02; fetched 2026-09-25)
- [LoL Esports Dev Diary — Win Probability powered by AWS](https://lolesports.com/article/dev-diary-win-probability-powered-by-aws-at-worlds/blt0)

Confidence: Medium (secondary summary of a Rioter; the model is *pro-play*, not solo
queue). Tier: Primary (Riot design artefact) / Secondary (the write-up).

**Read:** Riot's own model treats **objectives and structures, plus gold/XP share and
players-alive**, as the predictive signals — not kills per se. It is trained on *pro*
games, so its weights do **not** transfer cleanly to solo queue, where coordination
and objective discipline are lower.

---

## 5. Why late game is decisive (mechanistic reasons)

These are causal/mechanical arguments from game design, marked `confidence: Low` where
unsourced, and **PERISHABLE** where patch-specific:

- **Death timers scale with both champion level and game time**, so late-game picks
  convert to Nexus pressure far more reliably than early picks. LoL Wiki: base respawn
  wait (BRW) ranges **10s (lvl 1) → 52.5s (lvl 18)**, then a *Time Increase Factor*
  multiplies it — rising **~0.425% per 30s between 15–30 min**, **~0.3% between 30–45 min**,
  and **~1.45% after 45 min**, capped at **+50%**. Result: a **max death timer of 78.75s
  at 55 min, level 18**. Source: [LoL Wiki — Death](https://wiki.leagueoflegends.com/en-us/Death)
  (via MediaWiki API; fetched 2026-09-25). **PERISHABLE** (formula is patch-tunable).
  Confidence: High for the formula, `confidence: Low` for the *strategic* inference.
- **Objective stacking compounds**: dragons → soul → Elder, grubs → lane pressure,
  Baron → inhibitor damage (see [`03-objective-value.md`](03-objective-value.md)).
- **Gold/XP compounding + item breakpoints** mean a lead converts super-linearly into
  combat power (`confidence: Low` — mechanistic, unsourced at this run).
- **Comeback levers** (bounty gold, comeback XP, shutdowns) mean an *early* lead can
  be cashed back in the mid game — the equilibrium in §3.

---

## 5b. How much is decided *before* the game even starts

This is the under-appreciated half of the answer, and it reframes the "coin flip"
debate:

- **A draft-only model predicts 75.1% of ranked games before gameplay begins**
  (arXiv 2108.02799, 2021). Source: [arXiv:2108.02799](https://arxiv.org/abs/2108.02799)
  (fetched 2026-09-25). Confidence: Medium. Tier: Primary.
- **Riot explicitly engineers matchmaking toward ~50% win rates.** Riot's
  *"Dev: Matchmaking in 2024"* states their aim for new players is *"a ~50% winrate"*
  (they reported ~46% at the time), and that they **narrowed the MMR gap between teams
  from 2 divisions to 1** and worked on autofill balance. Source:
  [Riot /dev — Matchmaking in 2024](https://www.leagueoflegends.com/en-us/news/dev/dev-matchmaking-in-2024/) (fetched 2026-09-25). Confidence: Medium. Tier: Primary.

**Synthesis:** solo queue games are *designed* to be close (matched MMR → near-50%
priors), and champion mastery alone moves that 50% prior to ~75% correct pre-game.
So a large share of "who wins" is set by **who is on your team and what they can play**,
not by a mid-game snowball. The coach's edge therefore lives in the *in-game decisions
that shift the remaining ~25%* — and, at scale, in things players control: champion
pool mastery and role competence (see Axis 8/9).

---

## 6. What this means for the coach (product implications)

1. **Do not frame reviews as "you lost at the first death."** First Blood ≈ 55–58% win
   rate (Riot, patch 14.24–25.S1.2). Single early kills are near-noise.
2. **Weight repeatable structural decisions** — objective control, tempo, converting
   leads, and *not throwing* mid-game leads — because the mid/late game is where win
   probability actually swings (arXiv 2309.02449).
3. **Flag "lead conversion," not "lead creation."** First Turret (~70%) is the better
   early-game proxy than First Blood, so tower/lane-pressure outcomes deserve more
   weight than kill counts.
4. **Treat comebacks as expected, not exceptional** — bounty/comeback systems are
   designed in, so a coach should look for *specific throw patterns*, not assume an
   early lead is safe.

---

## 7. Confidence summary, conflicts & gaps

**Confidence:**
- Win condition is the Nexus — **High** (game rules).
- First Blood ≈ 55–58%, First Turret ≈ 70% win rate — **Medium** (Riot-published,
  but rank band/sample size unpublished; PERISHABLE).
- Early state weakly predictive, late state decisive — **Medium–High**
  (a *table* of 6 studies now agrees; ~74–76% from first-10-min/mid-game vs
  81.6% at 60–80% elapsed time vs >91–97% full-game).
- Much of the outcome is set **pre-game** (draft/mastery/matchmaking) — **Medium**
  (one 75.1% draft-only model + Riot's ~50%-engineered matchmaking).
- Snowball/comeback equilibrium is designed — **Medium** (Riot + 2 peer-reviewed papers).
- Mid-game **economy** is the top mid-game predictor — **Medium–High**
  (ICPEGE 2026 "economic ratio and difference features have the highest predictive
  power" + Riot WP model uses gold % + CHBR 2025's turret/bounty KPIs).

**Conflicts:**
- DotA 2 "85% after 5 min" (IEEE ToG 2019) vs LoL "~81.6% only at 60–80% game time"
  (arXiv 2309.02449) — **unreconciled.** Different game, different epoch; the DotA 2
  figure was **not verified at primary source this run** (`confidence: Low`).
- Full-game accuracy claims (91–97%) vs early-game claims (74–76%) are *not* a real
  conflict — they measure different windows. Compare like-for-like only.

**Gaps (unmeasured / unfound this run):**
- **No solo-queue-specific, rank-banded "gold diff @ 15 min → win%" curve.** Stat
  sites (lolalytics/u.gg/op.gg) were reachable but do not expose this curve as a
  first-class page; leagueofgraphs (which historically had it) is Cloudflare-blocked
  on all tiers (re-tested 2026-09-25). **This remains the single most valuable
  missing number for the product.**
- Riot's objective table covers only First Blood / First Turret — **no measured
  per-objective win rates** (drakes, soul, grubs, Herald, Baron) found.
- No measured **surrender/remake** share of games, which caps how much of "how games
  end" is a Nexus race versus a vote.
- Most win-prediction literature is **pro play or DotA 2**, not LoL solo queue; rank
  band, region and patch are almost never reported in the abstracts.
- Search engines were **unusable this run** (DDG/Bing/Mojeek served bot challenges or
  empty result pages from the datacenter IP). All findings above come from **direct**
  fetches of Riot primary docs, arXiv/OpenAlex/Crossref, and LoL Wiki.

---

### Sources (all fetched 2026-09-25 unless noted)

| # | Source | Date | Type |
|---|---|---|---|
| 1 | Riot /dev — How the Season 1 Changes Landed | 2025-02-07 | Primary |
| 2 | Riot /dev — Matchmaking in 2024 | 2024 | Primary |
| 3 | Esports.net — Riot Games explains Win Probability | 2025-02-02 | Secondary |
| 4 | LoL Esports Dev Diary — Win Probability (AWS) | 2023 | Primary |
| 5 | arXiv:2309.02449 — LoL Real-Time Result Prediction | 2023-09 | Preprint |
| 6 | arXiv:2108.02799 — Outcome prediction from champion experience | 2021-08 | Preprint |
| 7 | ICITR 2024 — Kills or Turrets (10.1109/icitr64794.2024.10857792) | 2024 | Peer-reviewed |
| 8 | ICPEGE 2026 — Evolution of the Model (10.1109/icpege67691.2026.11451276) | 2026 | Peer-reviewed |
| 9 | IEEE GEM 2022 — Win Prediction from the Snowball Effect Perspectives | 2022 | Peer-reviewed |
| 10 | CHBR 2025 — Deep learning KPIs (10.1016/j.chbr.2025.100718) | 2025 | Peer-reviewed |
| 11 | IEEE ToG 2019 — 10.1109/tg.2019.2948469 | 2019 | Peer-reviewed |
| 12 | IEEE TVCG 2016 — 10.1109/tvcg.2016.2598415 | 2016 | Peer-reviewed |
| 13 | Electronics 2025 — 10.3390/electronics14071445 | 2025 | Peer-reviewed |
| 14 | Acta Infologica 2024 — 10.26650/acin.1180583 | 2024 | Peer-reviewed (flagged leaky) |
| 15 | Applied Sciences 2025 — 10.3390/app15105241 | 2025 | Peer-reviewed (flagged leaky) |

> **Note on run-1 vs run-2:** run 1's provisional file asserted "~81.6% at 60–80%
> game time" and DotA 2 "85% after 5 min". Run 2 re-fetched the arXiv abstract
> directly — 81.62%/60–80% **confirmed**. The DotA 2 figure was **not** verifiable at
> primary source this run; treat as `confidence: Low`. Run 2 also corrected run 1's
> implied "early is a pure coin flip": a **draft-only model already hits 75.1%**, so
> early in-game state is weak *given* the pre-game state, but the pre-game state is
> itself strongly informative.
>
> **Freshness:** compiled on **patch 16.19** (LoLalytics, 2026-09-25). Riot's own
> table is stamped **patch 14.24 → 25.S1.2**. All objective/mechanic facts are
> **PERISHABLE** — re-verify per patch. Atakhan / Feats of Strength / Blood Roses were
> **removed in patch 26.1 (2026)** and are not live.
