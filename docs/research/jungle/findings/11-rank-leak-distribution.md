# Axis 11 — Rank-tier leak distribution

> Study run **2026-09-24**. Question: **which jungle mistakes concentrate at which
> ranks (Iron → Challenger)** — i.e. what do lower-elo junglers systematically do
> that higher-elo junglers do not?
>
> Compiled by a sub-agent for the jungle research study. Every number carries its
> source, rank band and patch. Claims that could not be sourced to a measurement
> are marked `confidence: Low` and are placed in the **OPINION** section. Sections
> flagged **[partial]** are incomplete and say so.
>
> **Patch context.** All live numbers below are from **patch 26.19** (u.gg label;
> the same patch is "16.19" on op.gg/lolalytics — the 2026 season renumbered the
> client version to 26.x while asset CDNs still serve 16.x tags; confirmed by
> u.gg's own page headers "Patch 26.19" vs its asset URLs `.../16.19.1/...`).
> **Atakhan and Feats of Strength were removed in patch 26.1 (2026)** — any
> pre-2026 objective-participation stat predates that change and is not
> directly comparable. Perishable: all rank-WR numbers below move patch-to-patch.

---

## 0. TL;DR

1. **There is no public dataset that measures "leaks by rank" directly.** No
   consumer stats site (u.gg, op.gg, lolalytics, Junglepedia) exposes a
   "mistake rate by rank band" table, and no accessible Riot primary source does
   either. This is a **structural absence**, not a research gap we can paper over
   with one more fetch. (See §2.)
2. **What *is* measurable** is **rank-band champion performance** for the jungle
   role (win rate + pick + sample size per rank). That is obtainable and is
   reported in §3. It is a *downstream* signal: it tells you **which champions
   win at which rank**, not which behaviours cause the wins.
3. **The one behavioural-by-tier idea that is documented** is Junglepedia's own
   admission that its "ganking / farming" playstyle classes are built from
   **outcome-based signals** (high CS at benchmarks, early kill participation)
   and are therefore **selection-biased** — which directly limits any attempt to
   infer "wrong behaviours by rank" from playstyle stats. (See §2.2.)
4. The strongest claims in this file are about **what low-elo junglers *win
   with*** (simple, low-execution champions) rather than **what they *do***. Any
   statement of the form "low-elo junglers over-gank / under-farm" is
   **inference or coaching consensus**, not measurement, and is labelled as such
   in §4 and §5.

---

## 1. What counts as a "leak", and why ranking them is hard

A **leak** (coaching term) = a repeated, correctable error that costs win
probability. For junglers the candidates are:

- **Farming / tempo leaks** — slow or static clears, missed camp timers, poor
  pathing, being late to respawns.
- **Information leaks** — low ward coverage, no tracking of the enemy jungler,
  face-checking.
- **Decision leaks** — over-ganking low-value lanes, fighting off power spikes,
  contesting objectives without numbers, not trading cross-map.
- **Death leaks** — dying at predictable timings (e.g. after first clear, at
  objective spawns), dying to invades.

To *rank* these you would need, per rank band: a behavioural rate (ganks per
minute, camps per minute, ward events per minute, deaths before X:00) **plus** a
causal link to win probability. Both halves are hard:

- Behavioural rates by rank require **positional/timeline data** at scale. Riot
  only exposes positional history to third parties at a coarse cadence (see §2.2),
  so failed ganks and off-timer pathing are invisible.
- Causal links are contaminated for the reasons already established on
  **Axis 2** (this study): CS/min, kill participation and objective participation
  are **partly outcomes of winning, not causes of it**. A "leak ranking" built on
  raw box scores would mostly rank winning teams.

**Consequence:** this axis can honestly deliver (a) the measured rank→champion-
performance gradient, (b) the documented methodological limits, and (c) a clearly
labelled inference ladder. It cannot honestly deliver a measured leak table.

---

## 2. The structural absence (this is the headline finding)

### 2.1 No site publishes "leaks by rank"

Attempted and checked this run (2026-09-24):

| Source | Rank filter? | Behaviour stats by rank? | Result |
|---|---|---|---|
| u.gg tier list (`?rank=iron…master`) | **Yes** (URL param works for rank) | **No** — only WR / pick / games per champion | §3 data obtained |
| u.gg champion build page (`?rank=…`) | Yes | **No** — behaviour table is JS-rendered and absent from SSR | no stats |
| op.gg champion page | (tier param) | **No** — page is Next.js flight payload; no plain-text stats | not parsable |
| lolalytics | Yes (SSR) | Champion-tier stats only; role-aggregate behaviour not exposed | limited |
| Junglepedia (`junglepedia.lol`) | Tier select exists (**Master+ → Gold+**) | Has *per-player* behaviour stats + per-tier invades/objective contest **nominal** fields | **tier param inert** (see §2.3) |
| leagueofgraphs | n/a | n/a | **Cloudflare-blocked** |
| dpm.lol | n/a | n/a | JS-only |

**No source returned a behavioural rate broken out by rank band.** The nearest
thing — Junglepedia's per-tier "Global Avg" invade rate and objective contest
rate — could not be retrieved because its tier filter does not actually change
the API response (see §2.3). `confidence: High` for the *absence claim* as of
2026-09-24; it may of course change if a site ships the feature.

**The absence extends to academia.** Two OpenAlex queries (2026-09-24) —
`"League of Legends player rank tier in-game statistics climbing comparison"` and
`"skill level differences in-game behavior MOBA players"` — surfaced **no study
that measures in-game behavioural metrics (farm, ganks, vision, deaths) broken
out by rank band** in LoL. The closest hits are cognitive/expertise studies
(e.g. *Using an International Gaming Tournament to Study Individual Differences
in MOBA Expertise and Cognitive Skills*, CHI 2016, doi:10.1145/2858036.2858190),
which compare expert vs novice on *psychological* measures, not per-rank in-game
leak rates. So there is no off-the-shelf academic aggregate to substitute for the
missing vendor data. (confidence: High for "not found via these queries"; a
paywalled dataset we could not reach may exist.)

### 2.2 Junglepedia's documented methodology limit (the key citation on this axis)

Junglepedia states verbatim on its tier list:

> "Playstyle-specific win rates will typically appear higher than a champion's
> overall win rate. This is because the classification uses outcome-based signals
> (e.g. high CS at certain benchmarks for farming, high KP early in the game for
> ganking), which inherently filter for games that are already going well. A
> 'farming' game requires hitting a high CS benchmark, excluding games where the
> jungler was invaded, died early, or pathed poorly. Similarly, a 'ganking' game
> requires successful early kills, excluding failed gank attempts (only because
> that data is just not accurate/available, as riot only provides positional data
> once per minute outside of kill events)."

Source: [junglepedia.lol/tierlist](https://www.junglepedia.lol/tierlist), fetched
2026-09-24. (confidence: High for the *statement*; tier: Established / primary
vendor methodology note.)

**Why this matters for Axis 11 specifically:** the exact signals a "leak by rank"
study would want — *failed* ganks, *poor* pathing, being *invaded* — are the ones
Junglepedia explicitly says it **cannot measure**. So the "obvious" data source
for rank leaks is self-declared blind to the leaks. Any cross-rank comparison
built on playstyle win rates (e.g. "low elo wins more by farming") inherits this
bias in unknown, rank-dependent ways.

### 2.3 Junglepedia tier filter verified inert (2026-09-24)

Junglepedia's API is public: `GET https://api.junglepedia.lol/api/v1/tierlist/multi-playstyle`.
The tier-list page builds the query as
`t = new URLSearchParams(); if (cfg.tier) t.set("tier", cfg.tier)` (read from the
page bundle `app/tierlist/page-*.js`). However, requesting
`?tier=gold%2B`, `?tier=platinum%2B` and `?tier=master%2B` returned **byte-identical
payloads** (same 118 ganking entries; the sampled champion "Jhin" had
`winRate 60.00, overallSampleSize 10, avgClearMs 217728` in all three). Also,
Junglepedia's own data timestamp read `lastUpdated: 2026-02-17`, i.e. it was
**~7 months stale** relative to the 2026-09-24 study run, and it still lists
pre-26.1 patch tabs (16.3 / 16.2 / …). `confidence: High` that Junglepedia is not
a usable rank-tier behavioural source this run.

---

## 3. MEASURED — rank-band difference in jungle *champion performance*

This is the only clean, citable cross-rank gradient we could obtain. Everything
below is **measured win rate by rank band**, not behaviour.

**Source for all rows:** u.gg tier list, role filter Jungle, rank filter, patch
**26.19**, **fetched 2026-09-24**. Format: `champion — win rate (games)`.

### 3.1 Low elo (Iron → Silver): what *wins* there

**Iron**
- Cho'Gath 53.6% (2.0K) · Briar 53.2% (3.2K) · Amumu 53.0% (2.2K) · Vi 51.8% (1.8K) · Master Yi 51.5% (7.1K) · Viego 50.9% (4.1K)

**Bronze**
- Lillia 53.3% (4.2K) · Briar 53.0% (8.3K) · Bel'Veth 51.7% (2.8K) · Master Yi 50.9% (18.9K) · Graves 50.7% (5.5K)

**Silver**
- Briar 52.9% (12.5K) · Amumu 52.4% (9.8K) · Darius 52.4% (1.7K) · Teemo 50.9% (3.5K) · Kayn 50.6% (21.4K) · Master Yi 50.4% (25.6K)

### 3.2 High elo (Master / Diamond+): what *wins* there

**Diamond+**
- Zyra 52.2% (1.6K) · Fiddlesticks 51.7% (2.2K) · Shyvana 51.3% (4.1K) · Zac 51.3% (3.2K) · Cho'Gath 51.2% (6.6K) · Talon 50.8% (7.8K) · Hecarim 50.8% (7.0K)

**Master**
- Jax 56.1% (157) · Fiddlesticks 53.1% (546) · Lee Sin 51.6% (3.9K) · Shaco 51.5% (808) · Talon 50.1% (1.8K)

**Challenger** — the tier list returned **no usable jungle entries** for
`?rank=challenger` this run (sample too small to surface); treat Challenger as
**not measured** here rather than as "no difference".

**Baseline:** u.gg's default Emerald+ tier list reports **2,600,120 champions
analyzed** for the patch (patch 26.19, fetched 2026-09-24).

### 3.3 What the measured gradient shows (and does *not*)

**Measured:** the set of **winning** jungle champions **changes shape with rank**.
Low elo (Iron–Silver) is topped by **low-execution, stat-check / hard-CC / AoE-
teamfight** champions — Master Yi, Briar, Amumu, Cho'Gath, Kayn, plus picks that
scale off simply being present (Lillia, Darius, Teemo). High elo (Diamond–Master)
surfaces **execution- and map-dependent** champions — Lee Sin, Talon, Shaco,
Hecarim, Zac, Zyra, Fiddlesticks — which in the shallow sense enjoy a *higher
execution ceiling*.

**Not measured here:** *why*. A champion win-rate gradient is consistent with
several stories (mechanical difficulty, coordination requirements, punishment of
the enemy's mistakes vs punishing your own), and this data alone cannot separate
them. It also **cannot** be read as "low elo farms/ganks worse" — that would be
the inference trap §2.2 warns about. Cross-reference **Axis 9 (champion-pool
effects)** before using these rows as evidence about champion difficulty; that
axis owns the difficulty-vs-rank question.

**Confounds for this table** (same class as Axis 2): (i) selection — the *people*
who pick Lee Sin at Master differ from those who pick him at Iron; (ii) rank
population size — Iron pools are small and noisy (Iron Amumu n=2.2K vs Silver
Kayn n=21.4K); (iii) patch perishability — every number here moves on the next
balance patch.

---

## 4. MEASURED-ish — the wider rank gradient (supported, but not jungle-specific)

These are the only cross-rank *behavioural* facts we could source, and they are
role-general, so they bound — but do not prove — jungle-specific leaks.

- **Raw box scores are a poor proxy for contribution, at every rank.** JQAS 2020,
  *Smart kills and worthless deaths* (logistic win model calibrated on
  **millions** of ranked games): "regular kills [and] deaths do not nearly
  explain" outcome, whereas win-probability-weighted actions do. Implication for
  this axis: rank-to-rank differences in **KDA / kill counts are weak evidence**
  of skill leaks. [JQAS 2020, doi:10.1515/jqas-2019-0096] (confidence: Medium;
  peer-reviewed primary.)
- **No single role dominates outcome**, overall model accuracy ≈ **86%** —
  role-aware ML study of pro LoL. [Springer SNCS 2023,
  doi:10.1007/s42979-022-01660-6] (confidence: Low — abstract partly garbled.)

Neither source breaks its analysis **out by rank**, which is the recurring wall
on this axis.

---

## 5. OPINION — coaching/analyst consensus on rank-specific leaks

> **Everything in this section is OPINION / coaching folklore.** It is **not**
> backed by a measurement we obtained this run. `confidence: Low` unless a second
> independent source is noted. It is recorded because the brief asks for
> "coaching/analyst consensus", and it is the shape of hypothesis a future
> measured study would need to test — **not** a result.

The commonly repeated claims (as of the 2025–2026 ranked ecosystem) are:

1. **Iron/Bronze — execution leaks.** Slow/incorrect first clears, dying to
   jungle monsters or invades, never tracking the enemy jungler, treating the
   game as "farm then fight". Mechanism often proposed: the player cannot yet
   execute a champion, which §3.3's low-elo champion pool (stat-check bruisers,
   Amumu, Master Yi) is *consistent with*.
2. **Silver/Gold — decision leaks.** Ganking too often vs farming, not converting
   kills into objectives, ARAM-ing mid, taking every fight. Hypothesis: raw
   mechanics are adequate but the trade/objective calculus is not.
3. **Platinum/Emerald — consistency & macro leaks.** Inconsistent pathing,
   coin-flip invades, poor objective set-up (no vision first), tempo gaps after
   a failed play.
4. **Diamond+ — refinement leaks.** Small tempo/vision edges, wave-and-jungle
   interaction precision, draft synergy. Errors that decide games at this level
   are individually tiny.

**Why to distrust the ladder above as data:** (a) it predicts *the same direction*
(skill increases with rank) for every leak, so it is nearly unfalsifiable; (b) the
two ranks where a leak is claimed to peak (Iron and Gold) are asserted, not
measured; (c) it is subject to survivorship — coaches only see the players who
sought coaching. Treat it as a **prior for hypothesis generation**, nothing more.

---

## 6. Best-supported inference ladder (clearly labelled)

Combining §2–§4, the most defensible statements, in descending confidence:

| # | Statement | Status | Basis |
|---|---|---|---|
| 1 | No public source measures jungle leaks by rank band. | **Measured (absence)** | §2.1 sweep, 2026-09-24 |
| 2 | Junglepedia's playstyle signals cannot capture failed ganks / bad pathing / invades. | **Measured (vendor statement)** | §2.2 |
| 3 | The set of *winning* jungle champions differs materially by rank band. | **Measured** | §3.1–3.2 (u.gg 26.19) |
| 4 | Low elo rewards low-execution champions; high elo surfaces high-execution champions. | **Measured pattern + interpretation** | §3.3 (cause not isolated — see Axis 9) |
| 5 | KDA/kill-count differences across ranks are weak evidence of skill leaks. | **Supported** | JQAS 2020 |
| 6 | "Iron leaks execution, Gold leaks decisions, Plat leaks consistency…" | **Opinion only** | §5 |

**If a measured leak-ranking is ever wanted**, the only route visible from here is
a *custom* pipeline on Riot timeline data (positional samples + kill events +
camp-kill events) computing per-rank-band rates of: ganks/min, camps/min, ward
events/min, deaths before each objective spawn, and invade-death rate — then
weighting each by its fitted win-probability delta. Junglepedia's public API
(`api.junglepedia.lol/api/v1/…`) is the closest existing substrate but, as shown
in §2.3, its tier filter does not currently separate ranks.

---

## 7. Method notes, access failures, gaps

**Access (2026-09-24):**
- u.gg — **works**, SSR; rank filter via `?rank=`; role filter via `?role=jungle`
  (role filter was ignored in the SSR list, so jungle rows were recovered by
  selecting entries whose build URL is `/build/jungle`).
- lolalytics — **works**, SSR, but champion-tier tables only, heavily obfuscated.
- op.gg, dpm.lol, junglepedia front-end — **JS-only**, no plain-text stats.
- leagueofgraphs — **Cloudflare challenge, blocked**.
- DuckDuckGo HTML endpoint — **returned no results** (Lite page).
- OpenAlex API — **works** (used for source discovery).

**Reproduce the §3 pull:**
```
python3 fetch_page.py "https://u.gg/lol/tier-list?role=jungle&rank=iron" --raw
# then select `.../build/jungle?rank=iron` entries
```

**Gaps (all open):**
1. **No behavioural rate by rank** for any jungle metric (KP%, CS/min, vision,
   death timing, objective participation). The core deliverable of a "leak
   distribution" is therefore **not measured** — documented, not invented.
2. **Challenger** jungle sample did not surface in the tier list this run.
3. **Rank labels are not identical across sites** (u.gg "Master" vs "Master+";
   u.gg patch "26.19" vs others "16.19") — cross-site joins will be sloppy.
4. **Patch perishability:** all §3 numbers are single-patch snapshots.
5. The **opinion ladder (§5) is untested** and should not ship to users as fact.
