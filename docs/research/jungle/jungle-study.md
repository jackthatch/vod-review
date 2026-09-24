# Jungle Study — findings log

> **Long-running study.** Each run appends to this document. Citations inline;
> confidence High / Medium / Low; source tiers Primary / Established / Low.
> Per-axis raw notes live in [`findings/`](findings/). Study design:
> [`README.md`](README.md). Execution procedure:
> [`ONE-SHOT-RUN.md`](ONE-SHOT-RUN.md). Tooling limits that shape every run:
> [`findings/00-environment-constraints.md`](findings/00-environment-constraints.md).

---

## Run log

| Run | Date | Axes covered | Status |
| --- | --- | --- | --- |
| 1 | 2026-09-24 | 1, 2, 3 | partial — findings salvaged from iteration-capped agents; numeric stat-site data blocked |
| 2 | 2026-09-24 | **1–12 (all)** | **complete** — 12/12 axes written, sourced, verified; stat-site access solved |

---

# Run 2 (2026-09-24) — COMPLETE STUDY SYNTHESIS

**Patch context:** Riot marketing `26.19` / game-version `16.19` (same live patch;
the two labels coexist — see §A6). Live 2026-09-23, captured 2026-09-24.
**Atakhan, Blood Roses and Feats of Strength were REMOVED in patch 26.1 (2026)**
and are *not* live mechanics.

All 12 axes were researched in a single batched run. What follows is the
cross-cutting synthesis; the evidence and citations live in
[`findings/01`](findings/01-how-games-are-decided.md) …
[`findings/12`](findings/12-meta-snapshot.md).

---

## A. The five cross-cutting conclusions

### A1. Confounding is the dominant trap in jungle stats — most "jungle KP%/CS/min correlates with winning" claims are partly backwards.
The strongest sources say this explicitly and independently. **CS/min falls in
losing games** (lost map access ⇒ fewer camps); **KP% rises when you're winning**
(a winning team simply has more kills to participate in); **objective
participation is inflated by being ahead**; **gold difference is as much an
outcome as a cause**. The peer-reviewed JQAS study *Smart kills and worthless
deaths* (2020) finds raw K/D are weak win predictors — the signal is the
**win-probability swing** of an action, not its count.
→ **Coach rule: never say "your CS/min was low, therefore you played badly."
Frame confounded stats as *symptoms to look behind*, not causes.** A
[findings/02](findings/02-jungle-impact-on-winrate.md), [06](findings/06-vision-and-information.md)

### A2. The metrics the community coaches with are largely *unmeasured* in public data.
There is **no public dataset** for **gank conversion rate** (ganks attempted →
converted), **invade success rate**, or **leaks by rank**. Riot does not track
ganks as a first-class stat; its win-probability model uses gold share, team XP,
objectives and timers only. Every specific "gank success %" you read online is
unverified folklore unless a sample size is shown.
→ **Coach rule: the product's own Riot-timeline pipeline can build these
datasets for the first time — and must, because coaching on unmeasured metrics is
coaching on vibes.** A [findings/05](findings/05-gank-theory.md), [07](findings/07-counterjungling-invades.md), [11](findings/11-rank-leak-distribution.md)

### A3. Early game is a *signal*, not a verdict — and Riot designs against runaway snowball.
Riot's only published objective win-rate numbers: **First Blood 57.6% → 55.4%**
and **First Turret 70.4% → 70.3%** (patches 14.24 → 25.S1.2). First blood is
close to noise; **first tower is the far better early proxy**. Prediction accuracy
runs ~75% pre-game, ~76% mid-game, and only ~82% at 60–80% elapsed — the game is
*not* decided in the first 15 minutes. Riot explicitly ships anti-snowball levers
(bounty gold, comeback XP).
→ **Coach rule: don't catastrophise a first death, and don't call a game over at
15 minutes. Weight the mid-game decision points higher.** A [findings/01](findings/01-how-games-are-decided.md), [03](findings/03-objective-value.md)

### A4. The single largest measured effect is **mastery**, not pool breadth or raw volume.
Across 7 jungle champions, players with **≥50 games on the champion** (Diamond+)
beat that champion's population win rate by **+3.2 to +7.2 pp, mean +4.98 pp**.
Elite-main win rate is roughly **champion-independent (~55–57%)**, while
population win rate tracks meta strength — i.e. **mastery pulls every champion to
a similar ceiling; the meta only sets the starting point.** Critically, **high
pick win rate ≠ high skill ceiling** (Rammus posts one of the highest win rates
but one of the *smallest* good→great gaps; Kha'Zix the reverse).
→ **Coach rule: champion-improvement framing should target the good→great gap,
not chase the tier list. Depth on a champion beats breadth of pool.** A [findings/08](findings/08-archetype-winrate-drivers.md), [09](findings/09-champion-pool-effects.md)

### A5. The product-design evidence base (learning science) is the strongest, most actionable material in the study.
This is **not** patch-dependent and won't expire:
- **Deliberate practice explains only ~26%** of game-performance variance
  (Macnamara 2014 meta) — raw hours are a weak lever; *structured* practice is the lever.
- **Feedback is the top intervention but can actively harm** (Kluger & DeNisi 1996:
  >⅓ of feedback interventions *lowered* performance; harm rises as attention shifts
  from task → self). Feedback framing is not cosmetic — it is causal.
- **Video review only works with a questioning / self-explanation loop** — passive
  watching does not transfer.
- **Unaided self-review is weak** (people are poor self-assessors) — which is
  precisely the gap an AI reference standard fills.
- **Spacing + retrieval practice** are the best-evidenced techniques (Donoghue &
  Hattie 2021: mean d≈0.56, N≈169k).
- **Tilt** measurably degrades play; review framing must reduce, not induce, it.
→ **This directly dictates how the coach must be built** (see §C). A [findings/10](findings/10-how-players-improve.md)

---

## B. Jungle-specific: what the evidence supports

| Claim | Status | Evidence |
| --- | --- | --- |
| Early objectives correlate most with winning (first drake ~70.7%, first tower 65.4%, first blood ~59.8%) | Measured (2024–25 era) | [03](findings/03-objective-value.md), [02](findings/02-jungle-impact-on-winrate.md) |
| First Baron alone ≈ 50% ⇒ **coin flip**; Baron matters via *conversion*, not the buff | Measured (patch 4.21, cross-checked vs Riot 2025) | [02](findings/02-jungle-impact-on-winrate.md) |
| **Jungle CS/min *falls* with rank** (Bronze 1.72 → Challenger 1.58) — jungle is the only role where it isn't monotone with rank; over-farming is a *low-elo leak* | Measured (415,860 NA games) | [02](findings/02-jungle-impact-on-winrate.md) |
| **Vision score is a weak, lagging, confounded proxy** — a purpose-built warding model (WARDS, Springer 2020) *out-performed Riot's vision score* at predicting winners | Measured | [06](findings/06-vision-and-information.md) |
| Defensible vision levers = **placement quality + denial**, not ward count | Measured (vision-score rules) | [06](findings/06-vision-and-information.md) |
| **Tempo is time, not speed** — "where a path *ends*, not how fast it runs"; fast to a dead play is fake tempo | Definitional (wiki primary + 2 sources) | [04](findings/04-tempo-and-pathing.md) |
| First-clear spread across champions is only **~13–16 s**; full clears 2:43–2:59 (3,366 games, 26.19) | Measured — **PERISHABLE** | [04](findings/04-tempo-and-pathing.md) |
| Camp value (counter-jungle unit): large monster **80–90 g / 95–120 XP** | Measured | [07](findings/07-counterjungling-invades.md) |
| Riot has **repeatedly nerfed** counter-jungling ⇒ indirect evidence it's high-impact | Inference from patch history | [07](findings/07-counterjungling-invades.md) |
| Archetype good→great gap ordering: **Assassin ≳ Gank > Carry > Bruiser > Tank ≈ Objective** | Measured (lolalytics, single site) | [08](findings/08-archetype-winrate-drivers.md) |

**Live meta snapshot (perishable, Emerald+, patch 26.19, 2026-09-24):** top tier
Wukong (53.58% W), Talon, Nidalee, Sylas (**19.32% ban**), Skarner; highest raw
win rate Rammus 55.02%; presence leaders Lee Sin / Sylas; 26.19 buffed Elise,
Kha'Zix, Lillia and nerfed Master Yi, Nocturne, Poppy, Vi. → [12](findings/12-meta-snapshot.md)

---

## C. What this means for the coach (actionable design rules)

1. **Lead with *decisions*, not stats.** The confounded metrics (CS/min, KP%,
   vision score) must never be presented as verdicts. Surface the decisions that
   are plausibly causal: early deaths, first-objective contests, tempo choices,
   gank/invade *preconditions*.
2. **Weight the mid-game.** Don't frame the first death or a 15-minute deficit as
   decisive — prediction only becomes confident late.
3. **Questioning loop, not a verdict feed.** Learning science says passive
   consumption doesn't transfer. The recap should ask/decompose ("here was the
   decision point; here was the alternative and its cost"), not just assert grades.
4. **Task-level, not ego-level feedback.** >⅓ of feedback interventions backfire
   when feedback becomes about the *self*. Keep the language about the *play*.
5. **Give the objective reference standard.** Unaided self-review is weak; the AI's
   value is supplying the standard the player can't produce alone.
6. **Champion-improvement framing targets the good→great gap, not the tier list.**
7. **Never state a number the pipeline didn't compute** — Riot doesn't publish it,
   and the public "conversion rates" for ganks/invades are folklore.
8. **Reduce tilt, don't induce it.** Emotional framing in a recap is a performance
   variable, not a stylistic choice.

---

## D. Biggest evidence gaps (honest)

1. **No solo-queue, rank-banded "gold diff @ 15 → win%" curve** — the single most
   valuable missing number for the product. No accessible site exposes it.
2. **No measured gank-conversion / invade-success dataset** exists publicly. The
   product must build these from Riot Match-V5 timelines itself.
3. **No measured per-role vision/warding numbers** (control-ward counts, vision↔win
   coefficients with sample sizes).
4. **No "leaks by rank" dataset** — only downstream champion-performance-by-rank.
5. **Patch-label discrepancy** (`16.19` vs `26.19`) is unresolved and cross-site;
   all live numbers are single-patch perishable snapshots.
6. **leagueofgraphs** (historically the canonical per-objective source) remains
   hard-Cloudflare-blocked on all fetch tiers.

---

## Run 1 — historical record (superseded by Run 2)

Run 1 covered axes 1–3 only. Its findings were salvaged from sub-agents that hit
their iteration caps *without writing files*, so they were provisional. Its
substantive conclusions (early leads weakly predictive; Soul ≈ Baron is design
intent not measurement; Atakhan/Feats removal in 26.1; Riot's First Blood/Turret
numbers) were carried forward and **re-verified in Run 2**. Its main limitation —
stat-site access blocked from the container — was **solved** before Run 2 (see
[`findings/00-environment-constraints.md`](findings/00-environment-constraints.md)).
