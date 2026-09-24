# Axis 9 — Champion-pool effects on win rate

> Study run **2026-09-24**. Question: **does champion-pool breadth help or hurt a
> jungler?** Sub-questions: one-trick vs flexible pool; the champion *mastery
> curve* (win rate as a function of games played on a champion); and how pool size
> relates to rank / win rate. Quantified wherever a public source exposes numbers.
>
> Compiled by a sub-agent for the jungle research study. Every number carries its
> source, rank band and patch. Unsourced claims are marked `confidence: Low`.
> Sections flagged **[partial]** are incomplete and say so.

**Perishable-fact warning.** All win rates below are patch-, rank- and
region-band-specific and drift week to week. Data captured **2026-09-24, patch
26.19** (lolalytics/u.gg render the Riot game-version string `16.19`; `26.19` is
the marketing patch of the 2026 season). Atakhan + Feats of Strength do **not**
exist in patch 26.1+ (removed). Do not quote these numbers after the next patch
without re-pulling.

---

## 0. TL;DR (headline)

1. **Mastery, not breadth, is the dominant measurable effect — and it is large.**
   Across **7 jungle champions**, lolalytics' "best players" cohort (every player
   ≥**50 games on the champion**, Diamond IV+, averaged Grandmaster) beats the
   champion population by **+3.2 to +7.2 pp**, mean **+4.98 pp** on the same
   patch, same rank band (§1.2). *(Source: lolalytics champion pages, 2026-09-24,
   Emerald+, patch 26.19.)* **confidence: High** for the numbers; **Medium** for
   causal reading (see confounds, §1.3).
2. **The elite-main win rate is roughly champion-independent (~55–57%), while the
   population win rate tracks meta strength (50.3–52.9%).** Dedicated mains pull
   *every* jungler to a similar ~56% level; the champion only sets the *starting*
   point. The mastery *delta* is therefore **largest for weak-in-meta champions**
   (Kha'Zix +7.15, Hecarim +6.70) and **smallest for strong ones** (Amumu +3.17).
   §1.2.
3. **Games-on-champion alone is a weak predictor once you are already a dedicated
   main.** Within the Graves top-50 mains leaderboard (all ≥50 games), the
   correlation between games-on-champion and win rate is **negative
   (r = −0.39)**: the 250+-game mains averaged **58.6%**, the <60-game cohort
   **69.9%**. Player rank / smurf status dominates raw grind volume. §2.3.
   *(confidence: Medium — one champion, n=50, 7-day window, heavily selected.)*
4. **Breadth is not free, but "wide pool = bad" is only Medium-confidence.** The
   public data that survives this environment's access walls strongly supports
   *"mastery is worth ~+5 pp"*; the *"wide pool hurts"* claim is a coaching
   consensus inferred from the within-champion curve, **not** a measured
   across-champion experiment (§3). No public dataset maps **pool size N → rank**
   (§4). **confidence: Medium / Low respectively.**
5. **[partial] A clean public games-played-vs-winrate *bucket table* was not
   recoverable this run.** League of Graphs (the classic source) is blocked; the
   reachable aggregators' SSR HTML exposes the mastery *cohort* (via the 50-game
   gate) but not the bucket curve. §2 is built from the gate + deltas, explicitly
   labelled as inference.

---

## 1. Within-champion mastery: the quantified gap (lolalytics)

### 1.1 Access & method

All figures pulled live **2026-09-24** from
`https://lolalytics.com/lol/<champion>/build/?lane=jungle` via tier-1 `direct`
(full 587–683 KB SSR HTML, no JS shell). Rank band **Emerald+, ranked solo/duo,
patch 26.19.** Two numbers are read per champion:

- **Population win rate** — the champion's win rate across all Emerald+ jungle
  players ("…has a 5X.XX% win rate in Emerald+ on Patch 16.19…").
- **Best-players win rate** — lolalytics' "Best on <Champion>" cohort ("…best
  <Champion> players have a 5X.XX% win rate…").

The best-players cohort is defined verbatim on every page (2026-09-24):
> "Analyzing 3,443 games played by the top 611 Graves players worldwide over the
> last 7 days… **Maximum 50 summoners are used per region with a minimum of
> Diamond IV and 50 games played on <Champion> to be eligible.**"

So **every player in the "best" cohort has ≥50 competitive games on that
champion** — it is a *mastery-filtered* sample. *(confidence: High.)*

### 1.2 The 7-champion table (Emerald+, jungle, patch 26.19, captured 2026-09-24)

| Champion | Population WR | Best-players WR | **Δ (pp)** | Best-cohort sample | Role rank |
|---|---:|---:|---:|---|---:|
| Kha'Zix | 50.36% | **57.51%** | **+7.15** | 4,055 games / 497 players | 17/77 |
| Hecarim | 50.33% | **57.03%** | **+6.70** | 4,985 games / 490 players | 26/77 |
| Graves | 50.69% | **56.03%** | **+5.34** | 3,443 games / 611 players | 28/77 |
| Nidalee | 52.61% | **56.93%** | **+4.32** | 3,499 games / 370 players | 3/77 |
| Sejuani | 52.89% | **57.01%** | **+4.12** | 2,517 games / 310 players | 28/77 |
| Elise | 52.58% | **56.61%** | **+4.03** | 3,478 games / 404 players | 14/77 |
| Amumu | 51.96% | **55.13%** | **+3.17** | 2,019 games / 263 players | 52/77 |

**Means:** population **51.63%**, best-players **56.61%**, **mean Δ = +4.98 pp.**
Best-players WR range **55.13–57.51%**; population WR range **50.33–52.89%**.

*(Source: lolalytics champion pages, jungle, Emerald+, patch 26.19, accessed
2026-09-24. confidence: High — direct read of published values.)*

### 1.3 Interpretation & confounds (read before quoting)

The headline pattern is clean and consistent across 7 champions: **dedicated,
≥50-game mains win ~5 pp more than the champion's general population.** Two
structural reads matter:

- **Elite-main win rate is ~champion-independent.** Every champion's best cohort
  lands in a **2.4 pp band (55.1–57.5%)**, while population rates spread more and
  track meta strength. Dedicated mastery appears to lift *every* jungler to a
  broadly similar ceiling.
- **The delta is larger for weaker champions.** Kha'Zix (+7.2) and Hecarim
  (+6.7) — both ~50.3% in the population — are pulled hardest; Amumu (+3.2) has
  the least headroom. This is the quantitative shape of the common claim *"mains
  keep a weak champion viable."*

**Confounds (why this is NOT a clean "50 games → +5 pp" causal estimate):**
1. **Rank confound** — the cohort averages **Grandmaster** (Graves page) vs an
   Emerald+ population baseline. Higher rank wins for reasons beyond mastery.
2. **Selection / "best-of" filter** — it is the *top ~50 per region*, an extreme
   upper tail, not a random 50-game sample. This inflates the mean.
3. **Simpson / composition** — lane matchups, ban exposure, meta drift.

Honest claim: **"the best, most-experienced mains of a champion beat that
champion's average population by ~+5 pp (range +3 to +7 across 7 junglers)"** —
an *upper bound* on the personal mastery effect, not the effect itself. The
within-player curve (§2) is what would isolate it. *(confidence: High the gap
exists; Medium causal.)*

---

## 2. The champion mastery curve (win rate vs games played) — [partial]

The textbook curve plots **win rate on the champion (y)** vs **games played on
that champion (x)**: low on first pick, crossing ~50% after a few games, then
flattening in the low-mid 50s. We could not recover the exact public bucket table
this run (access notes below), so this section gives the **methodology, the
inferred shape, and the one directly-measured sub-pattern we did extract.**

### 2.1 Access note (this run, 2026-09-24)

| Source | Status | Why |
|---|---|---|
| **League of Graphs** (classic bucket source) | ✗ all tiers | hard Cloudflare (`00-environment-constraints.md`) |
| lolalytics champion SSR | ✓ but **no bucket table** | exposes the 50-game *gate*, not the curve |
| lolalytics **leaderboard** page | ✓ **direct** | per-player games + win rate (used in §2.3) |
| u.gg champion page | jina partial | returned nav/title only, no experience buckets |
| op.gg champion page | ✗ | jina served the tier-list page, not the champion stats |
| metasrc.com champion page | ✗ | HTTP 403 (bot wall), all tiers |
| deeplol.gg champion page | ✗ | JS SPA shell (~6 KB), no SSR stats |

### 2.2 Inferred shape (lower bound, not a bucket read)

Two facts pin the curve's slope:
- The eligibility gate is **≥50 games** — lolalytics' own threshold for "a main."
- The ≥50-game cohort beats the population by **~+5 pp** (§1.2).

If the curve flattened before 50 games, a 50-game filter would not separate so
cleanly from the population. Therefore **the curve is still rising meaningfully
through at least ~50 games** — a **lower bound on the slope**. *(confidence:
Medium — inference from the gate + delta, not a direct read.)*

**[partial] — the exact bucket values (1–5 / 6–25 / 26–50 / 51–100 / 100+ games)
were not fetched. Do not cite bucket numbers until a source is retrieved and
dated. Next pull: League of Graphs via Wayback (see §6).**

### 2.3 Directly measured: games vs win rate *among already-dedicated mains*

The one place lolaIytics exposes raw per-player **games-on-champion + win rate**
is its champion **leaderboard** (tier-1 direct). We parsed the full
**Graves top-50 mains** leaderboard (2026-09-24, ≥50 games, >50% WR, Diamond IV+,
last 90 days):

- **Mean win rate 64.34%**, median **65.28%** (min 50.00, max 90.48).
- **Mean games 116**, **median 72** (min 50, max 360).
- **Pearson r(games-on-champion, win rate) = −0.389.**
- Bucketed by games: **<60 games → 69.9%** (n=13); **60–119 → 64.4%** (n=22);
  **120–249 → 59.9%** (n=9); **250+ → 58.6%** (n=6).

**Reading (and its trap).** Within a cohort that is *already* all dedicated mains,
**more games does NOT mean higher win rate — the correlation is negative.** The
likely drivers are **rank selection** (the leaderboard weights solo-queue rank
first; top-rank players play fewer games on any one champion) and **smurfs**
(several 50–90-game entries post 70–90% WR). *This is not evidence that grinding a
champion hurts.* It is evidence that **once you are a committed main, raw volume
is a weak predictor — skill/rank dominates.** *(confidence: Medium — single
champion, n=50, 7-day window, heavily selected; do not generalize widely.)*

Leaderboard ranking rule, verbatim (lolalytics, 2026-09-24):
> "…all players ranked Diamond IV and above, greater than 50% Graves win rate
> with at least 50 Graves games in the last 90 days. All players are ranked…
> according to their solo queue rank, Graves win rate and number of Graves games
> played **weighted in that same order of priority**."

---

## 3. Pool breadth: one-trick vs flexible

### 3.1 The conventional model (confidence: Medium)

Standard coaching consensus:
- **One-trick / narrow pool (1–2):** highest within-champion win rate, fastest
  mastery accumulation, but **ban/counter/meta-nerf vulnerable** — a one-trick
  banned or hard-countered loses the entire mastery edge.
- **Broad pool (≥5):** ban/counter-resistant, but each pick sits below its mastery
  asymptote → lower average per-game win rate.
- **Stated optimum: ~2–3 champions** — enough redundancy to survive a ban or
  counter, concentrated enough to stay high on each curve.

This is a **within-champion curve argument** (§2), not a measured pool-size
experiment. **confidence: Medium (consensus), Low (as measured causal effect).**

### 3.2 What the data does and does not support

- **Supported:** mastery is worth a lot (mean **+4.98 pp**, §1.2). A pool built to
  reach the mastery asymptote on each pick captures that; a pool too wide to do so
  leaves it on the table.
- **Not supported by this run's data:** any direct *"pool size 5 vs pool size 2 →
  Δwin rate"* measurement. No reachable aggregator publishes per-player pool size.
- **Counter-signal to naive one-tricking:** §2.3 shows more games on one champion
  does not monotonically raise win rate among mains — so "just one-trick and
  grind" is not a free lunch; the ceiling is set by skill/rank.

### 3.3 Ban & counter exposure — the cost side of a narrow pool

Each lolalytics champion page lists worst matchups + ban data. For **Graves
jungle** (Emerald+, 2026-09-24): *"countered most by **Rammus, Elise & Zyra**"*
(page text, accessed 2026-09-24) — note two of the three are themselves jungle
counters, i.e. a one-trick Graves eats those matchups every time they appear. A
2–3 champion pool diversifies exactly this exposure. *(confidence: Medium —
mechanism clear; magnitude not quantified this run.)*

---

## 4. Pool size vs rank

**No clean public dataset mapping "pool size N → rank band" was located this
run.** What *is* observable runs the other way:

- Aggregators gate their mains leaderboards at **Diamond IV+** (§1.1, §2.3): the
  high-mastery cohorts they publish are drawn from higher ranks. Rank and champion
  commitment **co-vary**; causality is unresolved.
- Mechanically, higher-rank players reach a champion's mastery asymptote in fewer
  games, which *permits* a wider viable pool — an inference, not a measured
  "pool width → win rate" effect.
- §2.3's negative games↔WR correlation inside the elite cohort is consistent with
  **elite players succeeding without champion-spamming** — again pointing to skill
  as the driver rather than pool width.

**confidence: Low. [partial] — flagged gap (§6).**

---

## 5. Academic / third-party literature

OpenAlex + arXiv searches (2026-09-24) surfaced adjacent work but **nothing that
isolates champion-pool breadth → win rate**:

- *E-Sports Player Performance Metrics for Predicting the Outcome of League of
  Legends Matches Considering Player Roles* — SN Computer Science, **2023**
  (doi:10.1007/s42979-022-01660-6). Role-aware outcome prediction.
- *Using Collaborative Filtering to Recommend Champions in League of Legends* —
  arXiv **2020** (doi:10.48550/arxiv.2006.10191). Champion recommendation.
- *Applications of Linear and Ensemble-Based ML for Predicting Winning Teams in
  LoL* — Applied Sciences, **2025** (doi:10.3390/app15105241).
- *Grinding to a Halt: Effects of Long Play Sessions on Player Performance* —
  CHI-adjacent, **2023** (doi:10.1145/3573382.3616073) — session length, not pool.

**No peer-reviewed paper on champion-pool breadth → win rate was found this run.**
*(confidence: Medium that this is a real gap rather than a search-coverage gap —
search engines were largely unusable from this IP this run; see §6.)*

**Search-access note:** Bing (jina) returned only a JS shell; Bing RSS returned
irrelevant results; DuckDuckGo `html/` and `lite/` served CAPTCHA/landing pages;
Mojeek returned nothing. **This run's evidence is therefore direct-fetch based
(lolalytics + Academic APIs), not search-engine based.**

---

## 6. Gaps & next pulls

1. **[partial] Exact games-played-vs-winrate buckets** — try the **Wayback
   Machine** League of Graphs champion page (`champions/stats/<champ>`, snapshots
   exist e.g. 2026-04-11) and confirm whether the bucket table is in the HTML or
   JS-only. Replace §2's inference with a dated table.
2. **Second independent OTP source** — capture u.gg / op.gg "top players" for one
   champion to make §1 a two-source critical claim (u.gg jina was partial this
   run; retry browser tier).
3. **Rank-band sensitivity** — re-pull §1.2 at Gold and Diamond to test whether
   the ~+5 pp gap is rank-dependent.
4. **Pool-size instrument** — none exists publicly; would require Riot API
   sampling of per-player champion spread vs win rate (out of scope this run).
5. **Confirm the `16.19` vs `26.19` patch label** on lolalytics before publishing
   externally.

---

*Sources accessed 2026-09-24 via `tools/fetch_page.py` (lolalytics = tier-1
direct SSR HTML; u.gg = jina partial; OpenAlex/arXiv = direct APIs). Patch 26.19
(= game version 16.19). Champion page game-count headers (e.g. Graves ~27,019
games) are secondary and not independently verified. This file is a living
document; sections marked [partial] are explicitly incomplete.*
