# Axis 2 — Causal impact of jungle play on win rate

> Study run **2026-09-24** (re-run; the previous provisional version was
> overwritten). Question: **which jungle behaviours correlate most strongly with
> winning** — kill participation %, CS/min, early deaths, objective participation,
> gank conversion rate — and **which of those correlations are plausibly causal?**
>
> Compiled by a sub-agent for the jungle research study. Every number below carries
> its source, rank band and patch. Unsourced claims are marked `confidence: Low`.
> Sections flagged **[partial]** are incomplete and say so.

---

## 0. Correlation vs causation — read this first

Three levels of claim are kept distinct throughout:

1. **Correlation** — the stat co-varies with winning across a population of games.
2. **Confounded correlation** — the stat co-varies with winning *partly because
   winning causes the stat*. This is the dominant failure mode for jungle stats:
   - **CS/min** falls in losing games (losing team loses map access; camps are
     stolen/contested) → high CS/min partly *reflects* a won game.
   - **Kill participation %** rises when a team is winning fights → a winning team
     simply has more kills to participate in.
   - **Objective participation** is inflated by winning teams, who take objectives
     because they are ahead.
   - **Gold difference** is as much an outcome as a cause.
3. **Plausibly causal** — behaviour *chosen before* the outcome, with a mechanism:
   **early deaths**, **gank execution**, **first-objective contests**.

**This axis is dominated by confounded signals**, and the best-quality sources say
so explicitly.

- Peer-reviewed JQAS, *Smart kills and worthless deaths* (2020; logistic-regression
  win model calibrated on **millions** of ranked LoL games): the authors find that
  **"regular kills [and] deaths do not nearly explain"** outcome, whereas actions
  *weighted by their change in an estimated in-game win probability* correlate
  almost perfectly with team performance. **The raw KDA box score is a poor proxy
  for contribution.** [JQAS 2020, doi:10.1515/jqas-2019-0096] (confidence: Medium,
  tier: Peer-reviewed primary).
- A role-aware ML study of professional LoL concluded the **difference in influence
  between roles on the outcome is negligible**, overall accuracy ≈ **86%** — no
  single role dominates. [Springer SNCS 2023, doi:10.1007/s42979-022-01660-6]
  (confidence: Low — abstract partly garbled; tier: Peer-reviewed primary).
- Modern jungle-analytics site **Junglepedia** states outright that its *playstyle*
  win rates are **inflated by selection bias**, because the classification uses
  **outcome-based signals** (high CS at benchmarks for "farming", early kills for
  "ganking") which "*inherently filter for games that are already going well… a
  'farming' game requires hitting a high CS benchmark, excluding games where the
  jungler was invaded, died early, or pathed poorly.*" It also notes that **Riot
  only provides positional data once per minute outside kill events**, so **failed
  ganks cannot be measured accurately** and "ganking" games are defined only by
  *successful* early kills. [junglepedia.lol/tierlist](https://www.junglepedia.lol/tierlist)
  (accessed 2026-09-24; confidence: High for the *methodology statement*, tier:
  Established). This single note is the most important citation on this axis.

---

## 1. Source access notes (this run, 2026-09-24)

- **lolalytics works via tier-1 direct.** `…/lol/tierlist/?lane=jungle&tier=platinum_plus`
  → 283 KB SSR HTML; page self-reports **Patch 16.19**, Emerald+ ranked solo/duo,
  **3,128,787 champions analysed** (`/lol/graves/build/?lane=jungle`: Graves jungle
  **50.69% WR**, 27,019 games, rank 28/77). Note the **patch-string mismatch** in
  the ecosystem this run: lolalytics prints `16.19` while u.gg / jungler.gg /
  lolstats print `26.x` — see §7.
- **DuckDuckGo `html/` was CAPTCHA-challenged on the direct tier** (contra the
  2026-09 note in `00-environment-constraints.md`); `lite.duckduckgo.com/lite/` via
  **jina** worked as a search backend. Bing `jina` returns mostly chrome/nav noise.
- **lolprofile.net** (which advertises a per-champion Kill-Participation table) is
  **Cloudflare-blocked on all three tiers** (403 + challenge).
- **jgtracker.com** (jungle gank-pattern tracker) returned **503 / Render wake
  interstitial** this run.
- **leaguemath.com** works via direct and held the best *raw match-population*
  analyses found (§§2–5). **junglepedia.lol** works via **jina**.

---

## 2. Kill participation % (KP)

### 2.1 Jungler KP rises with rank — but this measures *skill*, not win rate

leaguemath, *Kill participation by role* — **1,049,459 NA ranked solo-queue
matches, patches 5.3–5.8** (2015). KP = (kills+assists)/team kills, by league:

| League | Bronze | Silver | Gold | Platinum | Diamond | Master | Challenger |
|---|---|---|---|---|---|---|---|
| **Jungle KP** | 48.21% | 51.03% | 53.33% | 54.45% | 55.08% | 56.22% | 56.14% |
| Mid KP (ref) | 49.10% | 51.06% | 52.48% | 53.14% | 52.96% | 52.80% | 52.49% |
| Support KP (ref) | 50.16% | 52.27% | 54.30% | 55.45% | 56.30% | 57.77% | 57.85% |

[leaguemath.com/kill-participation-by-role](https://www.leaguemath.com/kill-participation-by-role)
(accessed 2026-09-24; confidence: Medium — old patch, very large n; tier: Primary
aggregate).

- Junglers have **higher KP than any role except support**, consistent with roaming.
- **Interpretation:** this is a **skill gradient** (better players rank up), *not* a
  measured "higher KP → higher win rate" curve. Note also that mid/adc KP **peaks at
  Master and slightly *falls* at Challenger**, and jungle KP plateaus above Gold —
  i.e. **past an optimum, more KP is not better** (grouping for every kill costs
  map-wide XP); the author explicitly wonders "if even higher KP would be better."
- **No current-patch source** giving a clean jungler KP-vs-winrate curve was found
  (§7 gap).

### 2.2 Community read (low confidence)

A r/summonerschool thread argues KP is **confounded**: *"You might have a low KP on
winning games because team is doing well,"* and a jungler can win by suppressing
the enemy jungler without high KP
[reddit r/summonerschool](https://www.reddit.com/r/summonerschool/comments/1d473hs/how_important_is_kill_participation_in_jungle/)
(confidence: Low, tier: Opinion).

---

## 3. CS/min — the counter-intuitive one (jungle farms LESS at higher ranks)

leaguemath, *You need to cs better; unless you play jungle, in which case you need
to gank more* — **415,860 NA ranked solo-queue matches, patch 5.5** (2015):

| League | Bronze | Silver | Gold | Platinum | Diamond | Master | Challenger |
|---|---|---|---|---|---|---|---|
| Jungle **cs/min** | **1.72** | 1.64 | 1.58 | 1.57 | 1.58 | 1.59 | **1.58** |
| Jungle **gold/min** | 346.62 | 348.95 | 350.04 | 351.92 | 356.42 | 361.93 | **363.16** |
| Jungle **wards/min** | 0.21 | 0.23 | 0.26 | 0.28 | 0.29 | 0.33 | **0.38** |
| (Top-lane cs/min, ref) | 4.70 | 5.12 | 5.46 | 5.69 | 5.86 | 5.99 | 6.05 |

[leaguemath.com/farm-and-wards-per-league-per-role](https://www.leaguemath.com/farm-and-wards-per-league-per-role)
(accessed 2026-09-24; confidence: Medium — old patch, large n; tier: Primary aggregate).

Author's read, verbatim: *"Skilled junglers quickly converge to some (optimal?) level
of farming, and stay there… climbing ranks depends on something other than what is
quantified in these simple statistics."*

**Interpretation:** the plainest counter-intuitive result in this axis.
- **Bronze junglers farm MORE cs/min than Challengers (1.72 vs 1.58) and still
  lose** → directly contradicts a naive "raise your jungle CS/min to climb" rule.
- Note that for **every other role cs/min rises monotonically with rank** — the
  jungle is the **exception**. Over-farming is a low-elo jungle leak (see also §5).
- The real gradients are **gold/min** (resource conversion, +17) and **wards/min**
  (≈**1.8×** from Bronze→Challenger) — the latter the author calls "a pretty
  staggering difference that highlights the importance of playing around vision."
- Caveat: averaged over all jungle champions, so farm-heavy vs gank-heavy champs
  wash out; 2015 data.

---

## 4. Deaths — raw KDA is weak

- **JQAS 2020** (§0): raw **deaths are a weak explanatory variable** for outcome;
  *win-probability-weighted* deaths are the strong signal.
- leaguemath jungler **deaths/min** (patch 5.3, **96,851** NA Diamond+ matches,
  2015) shows only a **~0.02 deaths/min spread** across the 10 most-played junglers
  (Rek'Sai 0.174 → Shaco 0.194); author: *"this table [does not] affect decision
  making that much."* Jungler gold/min at that rank spread 380 (Nidalee) → 342
  (Lee Sin) — note **Lee Sin, the most-picked jungler, had the lowest gold/min**,
  evidence that raw farm/gold under-credits playmaking picks.
  [leaguemath.com/kills-deaths-gold-per-min](https://www.leaguemath.com/kills-deaths-gold-per-min)
  (confidence: Medium, tier: Primary aggregate).
- **Caveat:** these are *champion-population* averages, not a deaths→winrate curve.
  The honest statement is: **raw death counts alone are a weak win predictor; the
  metric that matters is the win-probability cost of each death**, which no public
  dataset exposes (§7 gap).

---

## 5. Objective participation & first-objective correlations

leaguemath, *How to win at League of Legends* — patch **4.21** (2014), ranked games.
"% of the time the **winning** team also took the first *X*":

| First objective | Winners who took it first |
|---|---|
| First **Baron** | **50.06%** (coin flip) |
| First Blood | 59.78% |
| First Tower | 65.42% |
| First **Dragon** | **70.69%** |
| First Inhibitor | 79.28% |

[leaguemath.com/win-condition-analysis](https://www.leaguemath.com/win-condition-analysis)
(accessed 2026-09-24; confidence: Medium for the numbers; **Low for causal claims**;
tier: Primary aggregate).

**Interpretation:**
- **First drake (70.7%)** and **first tower (65.4%)** correlate far more strongly
  with winning than **first baron (50.1%)** and even **first blood (59.8%)**. For a
  jungler, an **early objective participation** signal is a stronger (if dated) win
  correlate than early kills.
- **Heavily confounded** — "winners did X", not "doing X wins". Cross-check below.
- Same article: **median wards placed barely differ** between winners (**54**) and
  losers (**52**), but losers have **far higher variance** (SD **25.7** vs **18.5**):
  *"placing just the right number of wards is best,"* not simply more wards.

**Cross-check / conflict (newer, better source):** Riot's own *"/dev: How the
Season 1 Changes Landed"* (2025-02-07) reports **First Blood = 57.6%** and
**First Turret = 70.4%** win rate after claiming the objective for **2025** patches
[Riot /dev](https://www.leagueoflegends.com/en-us/news/dev/dev-how-the-season-1-changes-landed/)
(confidence: Medium, tier: Primary; sourced via Axis 3 of this study).
- First Blood (57.6%, 2025) is **close to** leaguemath's 59.78% (2014) → mild
  cross-decade validation of ~57–60% for first blood.
- The tower figures differ (70.4% vs 65.42%): **definitions differ** ("win rate after
  claiming" vs "% of winners who took first") — do **not** conflate them.

---

## 6. Gank conversion rate **[partial]**

**No public dataset measures true gank conversion** (ganks that convert to
kills/plates/objectives). The best evidence is *why*:

- **Junglepedia** (method note, §0): Riot's API only exposes **positional data once
  per minute outside kill events**, so **failed ganks are invisible**; a "ganking"
  game is defined *only* by **successful early kills**. This is the definitive
  reason a real gank-conversion metric cannot be computed from public data.
  [junglepedia.lol/tierlist](https://www.junglepedia.lol/tierlist) (confidence: High
  for the constraint, tier: Established).
- **jungler.gg** pathing stats (patch **26.16**) give **starting-camp and route win
  rates** — a different thing from gank conversion, and confounded. Notable:
  highest-WR first camp **Blue side: Blue Sentinel 49.9%**; **Red side: Raptors
  50.6%**; most popular first camp both sides = **Blue Sentinel (~41–43%)**; side
  averages **Blue 49.84% / Red 50.97%** WR; a full-clear path
  `Red→Krugs→Raptors→Wolves→Gromp→Blue` = 9.2% popularity / **51.4%** WR vs
  `Blue→Gromp→Wolves→Raptors→Red→Gank-Top` = 5.5% / **51.3%** WR.
  [jungler.gg/jungle-stats](https://jungler.gg/jungle-stats) (confidence: Medium
  for the numbers; Low for causation; tier: Established.
- **junglepedia** also publishes **level-4 clear times** per champion (Diamond+
  solo queue), e.g. Sejuani 3:15, Vi 3:16, Lee Sin 3:19, Nidalee 3:23, Graves 3:23,
  Warwick 3:35, Poppy 3:40 — useful as *tempo* benchmarks (Axis 4), not win-rate
  drivers. [junglepedia.lol/champions/*](https://www.junglepedia.lol/champions/leesin)
  (confidence: Medium, tier: Established).

---

## 7. Synthesis — which behaviours correlate most strongly?

Ranked by strength of *evidence-supported* correlation found this run. **Every
jungle-specific quantitative figure found is 2014–2015 vintage** — the modern
numbers that would settle the axis were not reachable (see §8).

| Behaviour | Evidence of correlation with winning | Verdict |
|---|---|---|
| **First/early objectives (drake 70.7%, tower 65.4%)** | Strong (2014) + Riot 2025 (tower 70.4%) | Strong correlate; **confounded** (winning teams take them) |
| **Objective *participation* by the jungler** | Implied, not directly measured | Plausibly causal but **unquantified** |
| **KP %** | Rises with rank (48%→56%); no WR curve | **Skill proxy**, confounded; optimum not "max" |
| **Gold/min (resource conversion)** | Monotone with rank (346→363) | Plausible; confounded |
| **Wards/min** | ≈1.8× Bronze→Challenger; low *variance* best | Plausible; confounded |
| **CS/min (raw)** | **NEGATIVE with rank in jungle** (1.72→1.58) | **Not causal** — over-farming is a low-elo leak |
| **Raw deaths / KDA** | Weak (JQAS 2020; tiny champ spread) | Use WP-weighted deaths instead |
| **Raw first Baron** | None (50.06% ≈ coin flip) | Not causal |
| **Gank conversion rate** | **Not measurable publicly** (Junglepedia/Riot API limit) | Gap |

**Headline for the coach:** the two behaviours that most *look* like jungle
win-drivers (CS/min up, KP up) are **largely confounded or even inverted**, whereas
the strongest measurable win correlate available to a jungler — **participating in
early objectives** — is confounded by being ahead and has no clean causal estimate.
Framing any single jungle stat as "the thing that wins games" is not supported.

---

## 8. Gaps, conflicts & confidence

- **Gap — the big one:** no current-patch (16.x/26.x), solo-queue, *jungle-specific*
  statistic measuring **win rate as a function of** KP% / CS/min / deaths / gank
  conversion. lolalytics and u.gg expose champion and per-item win rates but **not**
  a per-player-metric win-rate curve; lolprofile (advertised a KP table) is
  Cloudflare-blocked; leagueofgraphs is hard-blocked; jgtracker was down.
- **Gap:** gank conversion rate — **structurally unmeasurable** from public data
  (Junglepedia; Riot exposes position only once/min outside kills).
- **Gap:** no deaths→winrate curve; no KP→winrate curve; both are skill-gradient
  proxies in the data that exist.
- **Conflict:** leaguemath first-tower 65.4% (2014) vs Riot first-turret 70.4%
  (2025) — different definitions and eras; unresolved (first-blood figures agree at
  ~57–60%).
- **Conflict:** naive lore says "farm more / get more kills"; JQAS 2020 and
  leaguemath both say **raw farm/KDA are weak win predictors** in the jungle.
- **Confidence overall: Low–Medium.** The *direction* of the counter-intuitive
  findings (raw CS/min is not a jungle win-driver; raw deaths are weak; early
  objectives > late; KP is confounded and has an optimum below max) is supported by
  ≥2 independent sources each. But all quantitative jungle-specific numbers are
  2014–2015, and the two most modern sources (Junglepedia, Riot 2025) are used
  mainly for *methodology* and *cross-checks*, not for a jungle win-rate curve.

> **Perishable.** All patches cited are historical. Re-verify on the live patch
> before shipping any threshold to the coach. Updated 2026-09-24.
