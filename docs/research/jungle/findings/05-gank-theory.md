# Axis 5 — Gank theory: when ganks convert

> **Status: Run-2 research (2026-09-24).** Every mechanical claim is
> verified against primary sources where possible; every statistic carries
> **number + sample size (where known) + rank band (where known) + patch + source +
> date**. Claims that are *analyst/game-theory consensus* rather than *measured*
> are explicitly labelled **[CONSENSUS]**. Claims with no citable source are
> labelled `confidence: Low`.
> Tooling: all fetches via `tools/fetch_page.py` (see `00-environment-constraints.md`).

---

## 0. Headline answers (TL;DR)

1. **No public dataset of "gank success rate" appears to exist.** We searched the
   academic literature (arXiv, OpenAlex, Semantic Scholar) and the major stat
   sites. There is **no published, queryable metric** of the form "ganks attempted
   → ganks converted" at any rank band. **Any specific gank-conversion percentage
   you read online is not a measured, reproducible statistic** — treat it as
   analyst folklore unless a sample size is shown. This is the single most
   important finding of Axis 5: **the metric everyone coaches with is unmeasured
   in public data.**
2. **Riot does not track or publish ganks as a first-class stat.** Its public
   Win-Probability model is built on gold share, team XP, objectives and timers —
   **not** on gank counts [lolesports Dev Diary, Primary]. Gank success is
   therefore inferred, not observed, in every public dataset.
3. **What *is* measured is the downstream proxy**: Riot's published
   **win-rate-after-First-Blood = 57.6% (14.24) → 55.4% (25.S1.2)** and
   **First Turret = 70.4% → 70.3%** — the closest thing to a measured "did an
   early kill matter?" number. Re-verified verbatim this run from Riot's
   public dev post (published **2025-02-07**) [Riot /dev "How the Season 1
   Changes Landed", Primary]. Riot explicitly adds that overall win rate by
   first-blood / first-turret / epic objective "haven't substantially changed
   from 14.24."
4. **Ganks convert on *preconditions*, not on desire.** The literature and the
   wiki both frame a gank as an *ambush that requires the target to be vulnerable*
   — the deciding variables are **wave state, target HP/mana, CC/gap-closer
   availability, summoner spells, and vision** [LoL Wiki: Jungling, accessed
   2026-09-24]. **[CONSENSUS]**
5. **Counter-gank risk is the dominant hidden cost.** Because the enemy jungler
   is also free-roaming in fog of war, an *unscouted* gank carries a tail risk of
   losing the 2v2 skirmish plus both buffs. The wiki names *counter-ganking* as
   the standard defensive answer [LoL Wiki: Jungling]. **[CONSENSUS]**

---

## 1. What a "gank" is (definition + why the definition matters for measurement)

**Definition (Primary, verified this run).** *"Ambushes against laners within the
lanes are called **ganks**… **Ganking** refers to the act of ambushing one or more
laners within their lane, with the intent of scoring takedowns."* The wiki stresses
the jungle's **fog of war** "heavily facilitates this," and that laners counter
ganks via "proper vision and zone control, or defend against them through… a
**counter-gank**." [LoL Wiki: Jungling, page id 7920, wikitext accessed 2026-09-24].

**Why this matters for EV modelling:** the wiki explicitly notes ganking is *not*
exclusive to junglers, that not all junglers should gank often ("farming junglers"
vs "ganking junglers"), and that the preferred ratio "differs from champion to
champion and even from one balance patch to another." [LoL Wiki: Jungling].
`confidence: High` (primary, but it is wiki-level, not Riot-published).

> **Consequence for the platform:** any gank-conversion metric must define what
> counts as an *attempt* (did the jungler path there *intending* a gank?, or just
> walk through?) and what counts as *conversion* (kill? kill-or-flash? kill-or-
> sums? "lane won"?). No public source defines these consistently — hence the
> absence of a headline number.

---

## 2. The gank equation — preconditions for conversion **[CONSENSUS]**

All of the following is **analyst/game-theory consensus** assembled from the wiki's
structural description plus standard coaching framing; it is **not** measured.
Mark each claim's confidence accordingly. Where the wiki supplies a structural
fact (fog of war, counter-gank) that is cited.

A gank converts when **all** of these line up; the probability of conversion is
roughly the product of the gateway variables, so one missing gate usually kills it:

| Gate | Why it gates conversion | Evidence tier |
| --- | --- | --- |
| **Wave state** (lane frozen near your tower / enemy pushed up / ally in position) | The target must be *reachable* by the time you arrive; if the lane is shoved to the enemy tower the gank turns into a dive. | [CONSENSUS]; `confidence: Low` (no measured source found) |
| **Target vulnerability** (low HP, no flash/Heal, immobile, no escape CC) | Ambush converts when the target cannot survive the burst window. | [CONSENSUS] `Low` |
| **Your kill threat** (CC + gap-closer + burst on the ganking champion) | Wiki: viable junglers are given "a mix of crowd control, gap closers, and burst damage" precisely so they can gank. | [LoL Wiki: Jungling] |
| **Vision denial** (approach path unwarded / enemy's flash-ward on cooldown) | Fog of war "heavily facilitates" ambush; wards are the primary counter. | [LoL Wiki: Jungling] |
| **No counter-gank** (enemy jungler known-elsewhere or you win the 2v2) | Counter-ganking is the standard defensive answer. | [LoL Wiki: Jungling] |
| **Timing** (a window where you are *not* giving up a higher-value play) | Opportunity cost — see §4. | [CONSENSUS] `Low` |

**Rule of thumb for coaching [CONSENSUS]:** a gank is a *conditional purchase* —
you are buying ~0–1 kills at the cost of your path tempo, camp respawns, and a
probability of a counter-gank loss. If any gate above is closed, the EV is
usually negative even when the gank "looks" good.

---

## 3. Lane selection **[CONSENSUS]**

No public dataset ranks lanes by *gank convertibility*. The following is standard
coaching consensus, not measurement:

- **Gank the lane that is already winning the 2v1/1v1** — a lane with an item/HP
  lead converts a gank far more reliably because the target must fight two behind
  players. `confidence: Low` (no measured source).
- **Prioritise lanes whose matchup snowballs** (kills convert to map pressure).
- **Avoid ganking a lane that is already losing hard** — you risk feeding a
  counter-gank and the target is often too tanky/leveled to burst.
- **Lane priority interacts with river/objective control** — ganking a lane with
  push is what lets you *then* walk to a river objective (see Axis 3 for objective
  value; Axis 4 for tempo).

**Directional measured anchor:** Riot's only published kill-adjacent win rate is
**First Blood → 57.6% (14.24) → 55.4% (25.S1.2)** and **First Turret → 70.4% →
70.3%** [Riot /dev "How the Season 1 Changes Landed", published 2025-02-07,
Primary, re-verified this run]. It says *an early kill is worth ~5–8 points of win
rate on average* — but it does **not** say it is worth that *because* of the gank;
First Blood includes solo kills and dives.

**Riot itself treats first-blood as noisy.** In the same post Riot agrees that
"First Blood felt too random, created too much pressure on individual players,"
and consequently replaced the First-Blood Feat with the **Feat of Warfare** (first
team to 3 champion kills) in **25.S1.2** [Riot /dev, Primary]. Reading: Riot does
not believe a *single* early kill reliably reflects a skill gap — which is a
warning against coaching "one gank = game won."

---

## 4. Timing windows **[CONSENSUS]**

Standard coaching windows (not measured):
- **Level-3 gank** after a 3-camp clear (~2:30–3:15) — jungler's first spike.
- **Level-6 gank** — ultimate available, much higher conversion.
- **Post-camp-respawn windows** — ganking while camps are down (free time) is
  cheaper than ganking while camps are up (opportunity cost).
- **Wave-crash windows** — gank as the enemy's wave crashes into your tower.
- **Pre-objective windows** — a successful gank 30–45s before drake/Herald enables
  the objective (links gank EV to objective value, Axis 3).

All `confidence: Low` (consensus; no measured public source located).

---

## 5. Expected value of a gank — a framework **[CONSENSUS / derived]**

No Riot-published EV formula exists. The standard analyst framework:

```
EV(gank) = P(kill) · V(kill + tempo)
         + P(no kill, sums burned) · V(sum advantage)
         − P(kill for enemy) · V(death + lost camps)
         − P(counter-gank loss) · V(2v2 loss + buffs)
         − opportunity_cost(camps skipped, path broken)
```

The accounting identity is uncontroversial; **the probabilities and the values are
not measured in any public source** — which is exactly why the metric is
unmeasured. For the platform, this framework should be treated as a *checklist of
terms*, not as a solver.

---

## 6. Counter-gank risk **[CONSENSUS, anchored in wiki]**

- The enemy jungler shares the same fog of war and can arrive at your gank's
  location on a similar clock. The wiki names **counter-ganking** as a primary
  defensive response to ganking [LoL Wiki: Jungling].
- Practical mitigation (consensus): track the enemy jungler's camps (if their
  camps are up, they are likely there, not on a gank), and gank only when the
  enemy jungler is *known* elsewhere.
- **Hidden asymmetry:** a failed gank is usually cheap (you walk away), but a
  *counter-ganked* gank can lose the 2v2, both buffs and a level — the fat tail is
  the risk, not the mean. `confidence: Low` (consensus; unmeasured).

---

## 7. Does gank success relate to winning? (the measured core)

**What is measured:**
- **First Blood → team win rate 57.6% (patch 14.24) → 55.4% (patch 25.S1.2)**
  [Riot /dev, Primary, re-verified]. Reading: an early kill correlates with ~55–58%
  win rate, i.e. **a meaningful but not decisive edge**.
- **First Turret → 70.4% → 70.3%** [same source]. Structural objectives correlate
  far more strongly than early kills.

**What is *not* measured:**
- Gank-attempt → conversion rate at any rank band: **not found**.
- Win-rate delta attributable specifically to *jungler ganks* vs solo kills/dives:
  **not found**.
- Any correlation between gank volume and win rate in public data: **not found**.

**Academic anchor #1 (Primary).** Early-game state is a weak predictor of the
final result: Riot's own WP model deliberately uses many features beyond gold
because gold difference "under-describes" the win state [lolesports Dev Diary];
academic prediction work finds only ~**81.6%** accuracy late and roughly
coin-flip discrimination early [arXiv 2309.02449]. **Implication:** a single
converted gank should not be narrated as "the play that won the game."

**Academic anchor #2 (Primary, verified this run) — the *quality* of a kill
matters more than the *count*.** Maymin, *"Smart kills and worthless deaths:
eSports analytics for League of Legends"*, **Journal of Quantitative Analysis in
Sports, 2020-09-21, DOI 10.1515/jqas-2019-0096**. Abstract (re-verified via the
Crossref API this run): the authors track every champion's location multiple
times per second and calibrate an in-game win-probability model, then find that
"individual actions conditioned on changes to estimated win probability correlate
almost perfectly to team performance: **regular kills and deaths do not nearly
explain as much as smart kills and worthless deaths**." **Implication for gank
theory:** a gank's value should be scored by the **win-probability swing it
produces**, not by whether it produced a kill — a 3-man collapse onto a fed
carry and a 3-man dive onto a 0/5 support are both "a gank," but only one is a
"smart kill." Code is open-sourced per the abstract.

---

## 8. Rank / patch perishability

- **Patch-dependent:** all jungle timers, camp gold/XP and gank-relevant champion
  tools change per patch. **Atakhan + Feats of Strength were REMOVED in patch 26.1
  (2026)** and must not be coached as live [Riot 26.1 Notes].
- **Perishable:** any gank-window number (level-3 clear time, camp respawn) is
  patch-locked and must be re-checked against the live patch before coaching.
- **Rank band:** no gank-conversion data exists *by rank* in any public source
  (this is the study's central evidence gap for this axis).

---

## 9. Gaps & next actions

- **[BLOCKER] No public gank-conversion dataset.** To measure this axis properly
  the platform would need its own Riot-API pipeline that timestamps player
  positions + intent + kills (i.e. build the metric, don't read it). Riot Match-V5
  does **not** expose "gank attempts."
- **Verify** Riot's First Blood / First Turret numbers against the current patch
  (they were last published for 14.24 → 25.S1.2 and may be stale).
- **Search** the pro-play literature ("Smart kills and worthless deaths", JQAS
  2020, DOI 10.1515/jqas-2019-0096) for kill-value modelling that could scaffold a
  gank-EV definition.
- **Search** the 2016 ASU thesis "Data Analysis of Jungle Pattern in League of
  Legends…" (keep.lib.asu.edu/items/135606) for any jungle-pattern statistics that
  touch gank frequency.

---

*Sources cited this run: LoL Wiki Jungling (MediaWiki API, pageid 7920, wikitext
accessed 2026-09-24); Riot /dev "How the Season 1 Changes Landed" (published
2025-02-07; First Blood 57.6%→55.4%, First Turret 70.4%→70.3%, re-verified
verbatim this run — Primary); Maymin, JQAS 2020-09-21, DOI
10.1515/jqas-2019-0096 (Crossref abstract re-verified this run — Primary);
lolesports Dev Diary (WP model, Primary, carried over); arXiv 2309.02449
(Primary, carried over). Search infrastructure attempted this run: arXiv API
(no "gank"+LoL results), OpenAlex API (14 "league of legends jungle" works, none
with gank-conversion data), Semantic Scholar API, Crossref API, Bing (RSS +
jina), DuckDuckGo (html + lite — CAPTCHA), Mojeek (content-type error) — **no
gank-conversion dataset surfaced in any of them.***
