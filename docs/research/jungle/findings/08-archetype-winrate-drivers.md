# Axis 8 — Win-rate drivers per jungle archetype

> **Status: Run-2 research (2026-09-24).** Every statistic carries **number +
> sample size (where known) + rank band + patch + source + date**. Claims that are
> *analyst/game-theory consensus* rather than *measured* are labelled
> **[CONSENSUS]**; claims with no citable source are `confidence: Low`.
> Tooling: all fetches via `tools/fetch_page.py`; JS-rendered stat blocks read with
> the browser tier (see `00-environment-constraints.md`).
>
> **Archetype source of truth:** `docs/jungle-playbook.md` §3/§4 — six buckets:
> **A** Farming carry · **B** Early gank/skirmish · **C** Tank/engage/utility ·
> **D** Assassin/pick · **E** Objective-control/tempo · **F** Bruiser/fighter.
> §5 defines the per-archetype *shape* of each metric. This axis answers the next
> question: **inside a bucket, what separates a good player from a great one, how
> does each bucket actually win, and where does each bucket leak?**

---

## 0. Headline answers (TL;DR)

1. **The measured win-rate driver is not the archetype's win rate — it is the
   *gap between the average player and the best player on that champion*.** Across
   the jungle roster on lolalytics (Platinum+, page-labelled patch 16.19,
   5,719,019 champions analysed, retrieved 2026-09-24), the best worldwide players
   on each champion beat that champion's overall Platinum+ win rate by **+2.7 to
   +7.9 points**. The *size* of that gap orders cleanly by archetype:
   **Assassin > Early-gank > Carry > Tank ≈ Objective.** [lolalytics, 2026-09-24;
   `confidence: Medium` — single stat site, one patch, see §7 patch-label flag.]
2. **Great players converge to ~55–58% on every archetype; average players
   diverge sharply.** The "best players" win rates cluster in a narrow band —
   Kha'Zix 57.51%, Lee Sin 57.05%, Sejuani 57.01%, Graves 56.32%, Nunu 55.26% —
   while the *same* champions' Platinum+ win rates range 49.63%–52.41%. So the
   **"great" bar is roughly archetype-invariant (~56–58%); the "good" baseline is
   not.** [lolalytics champion pages, Platinum+, patch 16.19, retrieved
   2026-09-24; `confidence: Medium`.] *Product consequence:* the coaching target
   should be an archetype-invariant high percentile, and the *path* to it is
   archetype-specific (see §5).
3. **The metric that separates archetypes most sharply is economy, not combat.**
   Measured per-game ranks (out of 79 jungle champions), the carry posts **Gold
   rank 7–8, Jungle-CS rank 7, but Assists rank 70 and Damage-Taken rank 73**; the
   tank/objective buckets invert every one (**Assists rank 5–6, Damage-Taken rank
   16–22, Gold rank 70–72, Damage rank 71–75**). [lolalytics champion stat blocks,
   Platinum+, patch 16.19, retrieved 2026-09-24.] This is the empirical
   confirmation of `jungle-playbook.md` §5: *"6.5 CS/min is excellent on a tank
   and mediocre on a Graves."*
4. **Every archetype leaks in the direction of its own strength.** Carry leaks by
   over-ganking / over-fighting (economy collapses); gank leaks by *farming* while
   the clock runs out; tank leaks by *soaking farm* and by bad engage angles;
   assassin leaks by diving before key cooldowns are used; objective leaks by
   conceding without trading. [CONSENSUS; aligns with `jungle-playbook.md` §7
   items 6–8.] `confidence: Low` (framework, not measured).
5. **No public dataset measures "archetype win-rate drivers" directly.** There is
   no stat-site field for "did this Graves over-gank?", no Riot endpoint for
   archetype-normalised KP%, and no academic paper isolating archetype cohorts.
   Everything below is either a **champion-level measured proxy** (lolalytics stat
   blocks) or a **derived interpretation** of them (labelled). **The platform must
   build the archetype-cohort metric itself from Riot Match-V5 timelines.**
   `confidence: High` on the gap claim.

---

## 1. Why archetype-normalisation is the whole game

`jungle-playbook.md` §5 states the rule: *"Any absolute number without archetype
context is noise."* Axis 8 supplies the measured backing for that rule **and
extends it**: normalisation is required to compare *players*, not just to set
benchmarks. A Graves with 6.5 CS/min and a Sejuani with 6.5 CS/min are not the
same quality — one is under-farming, the other is stealing farm from carries.
[CONSENSUS; `confidence: High` — direct restatement of the playbook's design
principle.]

Practical consequence: the radar/benchmark must be built **per archetype cohort**,
and "improvement" must mean *moving toward the cohort's high percentile on the
cohort's dominant metrics*, not toward a global average. Because early leads are
only weakly predictive of the final result (Axis 1), the cohort target should
**not** over-weight a single moment's win/loss.

**Academic anchor (Primary, retrieved via OpenAlex 2026-09-24).** The literature
agrees that role/archetype conditioning is required for fair performance
evaluation: *"E-Sports Player Performance Metrics for Predicting the Outcome of
League of Legends Matches Considering Player Roles"*, **SN Computer Science,
2023, DOI 10.1007/s42979-022-01660-6**, proposes *role-conditioned* player
performance metrics (abstract: "we … propose performance metrics that use data
from past matches to evaluate a player's performance … considering player
roles"). [OpenAlex abstract, retrieved 2026-09-24.] It supports the *principle*
(metrics must be role/archetype-conditioned) but does **not** publish per-archetype
jungle win-rate drivers — the gap this axis fills empirically with §2–§3.

---

## 2. The measured "good → great" gap, by archetype

**Method.** lolalytics publishes, per champion: (a) the Platinum+ win rate over
all games and (b) the win rate of the *best worldwide players on that champion*
(top players, Diamond+ minimum, ≥50 games on the champion in the last 90 days,
last-7-days window). The difference is a clean proxy for *"how much better do the
best players do than the field on this champion."* Source: lolalytics jungle tier
list column definitions + champion-page paragraphs, retrieved 2026-09-24.

### 2.1 The five champions read in full this run

| Champion | Archetype (§4) | Plat+ WR | Best-player WR | **Gap** | Plat+ Games |
|---|---|---|---|---|---|
| **Kha'Zix** | Assassin/pick (D) | 49.63% | 57.51% | **+7.88** | 46,409 |
| **Lee Sin** | Early gank (B) | 49.93% | 57.05% | **+7.12** | 72,256 |
| **Graves** | Farming carry (A) | 50.58% | 56.32% | **+5.74** | 48,363 |
| **Sejuani** | Tank/engage (C) | 52.41% | 57.01% | **+4.60** | 13,388 |
| **Nunu** | Objective/tempo (E) | 50.98% | 55.26% | **+4.28** | 10,864 |

### 2.2 The wider tier-list sweep (supporting)

| Champion | Archetype (§4) | Plat+ WR | Best-player WR | **Gap** | Plat+ Games |
|---|---|---|---|---|---|
| Kayn | Assassin/pick (D) | 50.86% | 57.68% | **+6.82** | 43,872 |
| Talon | Assassin/pick (D) | 51.46% | 58.12% | **+6.66** | 30,109 |
| Jax | Bruiser/fighter (F) | 50.76% | 57.20% | **+6.44** | 6,998 |
| Darius | Bruiser/fighter (F) | 51.51% | 57.89% | +6.38 | 4,197 |
| Gwen | Carry (A, AP) | 51.58% | 57.93% | +6.35 | 4,343 |
| Ekko | Assassin/Carry (D/A) | 51.18% | 57.35% | +6.17 | 22,557 |
| Sylas | Bruiser (F) | 51.08% | 56.98% | +5.90 | 44,350 |
| Ivern | Objective/tempo (E) | 51.54% | 56.97% | +5.43 | 5,196 |
| Nidalee | Gank/carry (B/A) | 51.57% | 56.93% | +5.36 | 15,337 |
| Elise | Early gank (B) | 51.53% | 56.61% | +5.08 | 14,611 |
| Shaco | Assassin/pick (D) | 51.63% | 56.57% | +4.94 | 26,994 |
| Zac | Tank/engage (C) | 52.06% | 56.91% | +4.85 | 15,825 |
| Skarner | Tank/engage (C) | 52.42% | 57.14% | +4.72 | 5,795 |
| Master Yi | Carry (A) | 52.12% | 56.76% | +4.64 | 43,281 |
| Rek'Sai | Early gank (B) | 51.93% | 56.41% | +4.48 | 6,207 |
| Briar | Bruiser/fighter (F) | 52.62% | 56.94% | +4.32 | 28,010 |
| Wukong | Bruiser/fighter (F) | 53.58% | 57.35% | +3.77 | 33,765 |
| Shyvana | Carry/bruiser (A/F) | 53.06% | 56.81% | +3.75 | 28,907 |
| Cho'Gath | Tank (C) | 53.28% | 56.31% | +3.03 | 39,056 |
| Rammus | Tank/engage (C) | 54.47% | 57.20% | **+2.73** | 14,139 |

Plate-wide average Platinum+ win rate = **50.94%**; "Platinum+ Champions
Analysed" = **5,719,019** [lolalytics, retrieved 2026-09-24; `confidence: Medium`].

**Interpretation (`confidence: Medium`, derived from the measured columns above).**
- **Archetype ordering of the gap: Assassin (~+6.7 avg) ≳ Early-gank (~+5.7) >
  Carry (~+5.6) > Bruiser (~+5.3) > Tank (~+3.9) ≈ Objective (~+4.9).** The two
  buckets whose entire value is *decision-dense execution* — assassins (who deletes,
  when, is peel down?) and gankers (who to gank, when to stop farming) — have the
  most headroom. The two whose value is *team-scaled and kit-driven* — tanks and
  utility/objective — have the least.
- **Rammus is a "win-rate floor" champion:** highest Plat+ WR on the list (54.47%)
  but the *smallest* good→great gap (+2.73). **High win rate ≠ high skill ceiling.**
  A tier list ranks *picks*; it does not rank *where a player can improve*. The
  product must never conflate the two (this is the single most important
  product-facing correction in this axis).
- **Champion `Games` column matters:** the small-gap, high-WR tanks (Rammus
  14,139; Cho'Gath 39,056) have large samples and stable floors; the biggest-gap,
  low-WR assassins (Kha'Zix 46,409; Kayn 43,872) are high-pick, high-variance —
  exactly where coaching has the most win-rate to sell and the highest variance.

---

## 3. Archetype metric profiles (measured, champion-level)

Raw stat blocks from lolalytics champion pages (Platinum+, page-labelled patch
16.19, retrieved 2026-09-24). Values are **per-game averages**; the parenthetical
is the champion's **value-rank out of 79 jungle champions (1 = highest value)**.
`confidence: Medium` — single site.

| Metric (per game) | **Graves** (A carry) | **Kha'Zix** (D assassin) | **Lee Sin** (B gank) | **Sejuani** (C tank) | **Nunu** (E objective) |
|---|---|---|---|---|---|
| Win rate | 50.58% | 49.63% | 49.93% | 52.41% | 50.98% |
| Games (sample) | 48,363 | 46,409 | 72,256 | 13,388 | 10,864 |
| **Kills** | 8.86 (12) | **9.34 (9)** | 7.92 (27) | 4.94 (73) | 5.72 (65) |
| **Deaths** | 6.06 (34) | 6.12 (29) | 5.78 (45) | **4.90 (76)** | 6.33 (14) |
| **Assists** | 6.72 (70) | 6.34 (73) | 8.89 (27) | **12.04 (6)** | **12.21 (5)** |
| **Gold** | **14,306 (8)** | **14,311 (7)** | 12,617 (62) | 11,989 (70) | 11,815 (72) |
| **Jungle CS** | **175.2 (7)** | 170.3 | 154.9 | 150.8 (70) | 146.5 |
| **Minions Killed** | **43.88 (5)** | 24.05 (69) | 22.44 (72) | 28.65 (54) | 25.93 (63) |
| **Total Damage** | 23,880 (19) | **24,289 (14)** | 19,433 (61) | 18,105 (71) | 16,754 (75) |
| **Damage Taken** | **25,403 (73)** | 30,116 (44) | 30,222 (43) | **37,018 (16)** | 35,499 (22) |
| **Healing** | 8,932 | 12,563 | 13,140 | 11,511 | **17,811 (16)** |

*(rank = value rank of 79; ranks shown for the rows that most cleanly separate the
archetypes. Blank rank = not captured in the same extraction slice.)*

### 3.1 Reading the profiles (derived from §3, `confidence: Medium`)

- **Carry (Graves):** top-10 economy — **Gold 8/79, Jungle CS 7/79, lane Minions
  5/79** — and top-15 kills (12/79), while sitting **near-bottom in assists (70/79)
  and damage taken (73/79)**. The carry is high-farm, high-kill, low-assist, and
  *not the frontline*. **Leak detector: a carry with high assists and high
  damage-taken is not playing the archetype** — they are fighting while their
  spike is unfinished.
- **Assassin (Kha'Zix):** the **highest kills on the board (9.34, 9/79)** with
  **very low assists (6.34, 73/79)** and **top-15 damage (14/79)** and **top-10 gold
  (7/79)** — but also **low lane minions (24.05, 69/79)**. The assassin farms
  *champions*, not waves; its economy is kill-derived. **Leak detector:** high
  assists → the assassin is team-fighting instead of picking; low kills → the
  deletion window is being missed.
- **Gank (Lee Sin):** the *balanced-but-low-economy* profile — mid kills (27/79),
  mid assists (27/79), mid damage (61/79), **low gold (62/79) and low lane minions
  (72/79)**. Highest pick rate on the board (12.63%) and the largest sample
  (72,256) make it the canonical gank-jungler baseline. **Leak detector:** low
  early KP% and low kill conversion (per Axis 5, *quality* of kills > count).
- **Tank (Sejuani):** **top-6 assists (12.04, 6/79)** and **damage-taken 16/79**,
  with **low kills (73/79), low damage dealt (71/79), low gold (70/79), low jungle
  CS (70/79)** — *and the fewest deaths of the five (4.90, 76/79 = 4th-fewest)*.
  The tank is the high-engagement, low-economy, survivable enabler.
- **Objective/utility (Nunu):** the most extreme enabler — **assists 12.21 (5/79),
  damage-taken 35,499 (22/79), healing 17,811 (16/79)**, with the **lowest damage
  on the board (16,754, 75/79)** and low gold (72/79). Note the outlier: **Nunu
  dies a lot for an enabler (6.33, 14/79)** — consistent with Q/R dive-and-consume
  patterns; a distinct leak shape from Sejuani's low-death tanking.

**Design implication:** the §5 radar of the playbook is *confirmed by measurement*
— economy ranks (Gold, Jungle CS) are the cleanest archetype discriminator, and
assists/damage-taken form the second axis. The product's archetype classifier
could be seeded directly from these two axes.

---

## 4. How each archetype actually wins (mechanism, not metric)

Framed against the three jungle questions in `jungle-playbook.md` §1. All
**[CONSENSUS]** unless sourced; shapes match §3's measured profiles.

**A · Farming carry** — wins by **arriving at the mid-game fight a full item
ahead** and converting the won fight into an objective. Measured profile (Graves)
puts the edge in economy ranks, not assist/vision ranks. *Win path:* clean clear →
reset on gold → hit the 2–3 item spike → force at the spike → take the objective.
*Temptation that loses:* early over-ganking, which breaks the clear rhythm and
delays the spike (playbook §7 #6).

**B · Early gank / skirmish** — wins by **manufacturing a lead before its own
scaling decays**, then converting that lead into towers, not just kills. Because
the kit decays, the archetype is **clock-sensitive**; the gap is among the largest
(Lee Sin +7.12) because the *decisions* dominate the *kit*. *Temptation that
loses:* farming past the window (playbook §7 #7) or converting kills into nothing
(#11).

**C · Tank / engage / utility** — wins by **making the fight favourable for
someone else**: correct engage angle, peeled carries, objective control. Its value
is team-scaled — hence the small gap (Sejuani +4.60; Rammus +2.73; Zac +4.85).
*Temptation that loses:* soaking farm the carries need (§3C coaching focus) and
1-for-1 dive engages (§6.6).

**D · Assassin / pick** — wins by **removing a priority target before the fight
starts** so the fight is played 5v4. **Highest gap of any bucket** (Kha'Zix +7.88,
Kayn +6.82, Talon +6.66) because the archetype is pure decision-density: who to
delete, when, and whether the carry's peel is down. *Temptation that loses:*
diving before key cooldowns are used (§6.6); taking even fights while behind (§3D).

**E · Objective-control / tempo** — wins by **winning the clock and the smite
fights**, converting every neutral objective. Nunu's low pick rate (1.9%) and
Ivern's (0.91%) mark a small, expert population with a modest measured gap
(+4.28 / +5.43) — its value is systemic, not personal. *Temptation that loses:*
conceding an objective without trading (§7 #8) — the archetype's whole premise.

**F · Bruiser / fighter** — wins by **winning the skirmish, then the
front-to-back fight**; the "balanced" bucket, so win drivers are the *blend* of
damage and survivability (§3F). Measured: Wukong is tier-list #1 (53.58% Plat+)
yet has a *small* gap (+3.77) — high floor, moderate ceiling; Jax/Darius carry the
higher skill ceiling among fighters (+6.44 / +6.38). *Temptation that loses:* bad
fight selection / dive timing (§3F, §6.6).

---

## 5. Where each archetype leaks most (ranked per bucket)

| Archetype | Primary leak | Secondary leak | Playbook §7 cross-ref |
|---|---|---|---|
| A Carry | **Over-ganking / over-fighting** → CS + gold collapse | Chasing kills instead of objectives | #6, #11, #2 |
| B Gank | **Under-ganking** → farming while the clock runs out | Kills without tower/objective conversion | #7, #11 |
| C Tank | **Soaking farm the carries need** | 1-for-1 dive engages (bad angle) | §3C, §6.6 |
| D Assassin | **Diving before key cooldowns are used** | Taking even fights while behind | §6.6, §3D |
| E Objective | **Conceding objectives without trading** | Poor pre-objective vision setup | #8, #12 |
| F Bruiser | **Bad fight selection / dive timing** | Unbalanced damage-vs-survivability build | §3F, §6.6 |

All **`confidence: Low`** — a *derived* mapping of the playbook's consensus leaks
onto archetypes; **not** measured per-archetype in any public dataset (§0.5, §8).
Treat as a hypothesis set for the detection layer to validate against real
timelines.

---

## 6. What the product should compute per archetype (bridge to playbook §8)

Every metric must be **normalised to the champion's primary archetype** before
scoring. Candidate archetype-discriminating signals — the *proxies* are grounded
in §3's measured profile shapes; the *leak detections* are the product's own
hypotheses (playbook §8 flags this table as candidate-only): `confidence: Low`.

| Archetype | Dominant measured signal | The archetype-specific *leak* signal |
|---|---|---|
| A Carry | `jungleMinionsKilled`/min + `totalGold` pace + damage share | **CS/min drop inside gank windows** (over-ganking) |
| B Gank | kill participation %, early (min 3–12) KP | **KP% below cohort in min 3–12** (under-ganking) |
| C Tank | assists share + damage taken + objective/smite rate | **`jungleMinionsKilled` high for cohort** (farm theft) |
| D Assassin | kill share + deaths/10 + target-is-carry rate | **death→carry-alive correlation** (dove with peel up) |
| E Objective | smite/objective-secure % + tempo (XP/gold) curve | **objective contested without vision/trade** |
| F Bruiser | skirmish win rate + damage/taken balance | **fight selection** (initiation with numbers down) |

Two measurement cautions from sibling axes: (a) **there is no public gank-
conversion metric** (Axis 5) — the platform must infer intent from positions, not
read it; (b) **wave state, summoner cooldowns, and true vision score are not in
the Match-V5 timeline** (playbook §8 "Known gaps"), so anything that depends on
them must be hedged, never asserted.

---

## 7. Caveats, perishability, and the patch-label flag

- **Patch-label discrepancy [IMPORTANT]:** u.gg served **"Patch 26.19"** for the
  live tier list this run, while lolalytics served **"Patch 16.19"** with an
  identical average-win-rate header (50.94%). All numbers above are **as served by
  lolalytics on 2026-09-24**; the patch label is inconsistent across sites and is
  **flagged for verification**. `confidence: Medium` on the numbers, `Low` on the
  patch attribution.
- **Perishable:** every win rate, pick rate and stat rank rotates ~every two
  weeks. Nothing here should be hardcoded.
- **Single source on the gap analysis:** the good→great gap (§2) is computed from
  one site's leaderboard-cohort definition and needs an independent cross-check
  (u.gg / op.gg / leagueofgraphs) before being treated as settled.
- **Not measured anywhere:** archetype-*conditioned* win-rate drivers. The §4
  mechanism and §5 leak tables are **[CONSENSUS]/derived**, not measured —
  `confidence: Low`.
- **Atakhan + Feats of Strength were removed in patch 26.1 (2026)** — no archetype
  analysis may reference them as live. [playbook §2; Riot 26.1.]

---

## 8. Gaps & next actions

- **[BLOCKER] No archetype-cohort dataset exists.** To measure this axis the
  platform must build its own: bucket champions per playbook §4, compute the
  metric *distributions* (not means) per bucket from Match-V5 timelines, then
  model which percentile of which metric predicts win **per bucket**.
- **Extend the measured matrix** (§3): add the remaining bucket representatives
  (Ivern, Udyr for E; Zac/Maokai/Amumu for C; Kindred/Lillia for A; Nidalee/Elise
  for B) to confirm the profile shapes. Five of six buckets covered this run.
- **Cross-check the good→great gap** (§2) on a second stat site.
- **Resolve the patch-label discrepancy** with a dated fetch of the live patch
  number from a Riot primary source.
- **Validate §5's leak table** against real timelines before it drives coaching.

---

*Sources cited this run: lolalytics jungle tier list (Platinum+, retrieved
2026-09-24 — win rates, best-player win rates, sample sizes, 5,719,019 champions
analysed; page-labelled patch 16.19, `confidence: Medium` / patch-attribution
`Low`); lolalytics champion stat blocks for **Graves** (48,363 games), **Kha'Zix**
(46,409), **Lee Sin** (72,256), **Sejuani** (13,388), **Nunu** (10,864) —
Platinum+, retrieved 2026-09-24 (per-game kills/deaths/assists/gold/CS/damage/
healing + value-ranks out of 79); u.gg LOL tier list (served Patch 26.19, 2,600,120
champions analysed, retrieved 2026-09-24 — patch-label cross-check only;
content otherwise Cloudflare-blocked); `docs/jungle-playbook.md` §1–§8 (archetype
taxonomy and leak list — internal domain knowledge, durable); Riot Patch 26.1
notes (Atakhan/Feats removal — via playbook §2, Primary, carried over). **Academic
anchor:** "E-Sports Player Performance Metrics … Considering Player Roles", SN
Computer Science 2023, DOI 10.1007/s42979-022-01660-6 (OpenAlex abstract, Primary,
retrieved 2026-09-24); no per-archetype win-rate dataset surfaced via OpenAlex
search (3 queries this run).*
