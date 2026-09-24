# Axis 6 — Vision & information advantage in the jungle

> Study run **2026-09-24**. Question: how much do **vision economy**, **vision
> denial** and **information advantage** drive winning in solo queue, and what
> does it look like *specifically for the jungle role* — as distinct from support?
> Quantified where possible: ward counts, vision-score mechanics and
> correlations, ward placement impact, denial/counter-vision by role.
>
> Compiled by a sub-agent for the jungle research study. Every number carries its
> source, rank band and patch. Unsourced claims are marked `confidence: Low`.
> Sections flagged **[partial]** are incomplete and say so.

**Perishable-fact warning.** Ward/trinket numbers below are patch-sensitive.
Mechanics cited to **patch 26.x** unless noted; verify on the LoL Wiki before
quoting. Atakhan + Feats of Strength do **not** exist in patch 26.1+ (removed).

---

## 0. TL;DR (headline)

1. **Vision score is a weak, lagging proxy — not a clean win driver.** By
   construction it is ward-lifetime *provided* + ward-lifetime *denied* (§2), so a
   winning team keeps wards alive longer and kills more enemy wards: high vision
   score is partly *caused by* winning (same confounding as KP% / CS-min, Axis 2
   §0). A peer-reviewed study that tried to use it as a winner predictor found
   **Riot's vision score significantly *under-performed* a purpose-built warding
   model** (§5). Treat raw vision-score ↔ win-rate correlation as **confounded and
   low-fidelity**.
2. **The defensible win-relevant levers are *placement quality* and *denial*, not
   ward count.** Vision score's own rules *penalise* staleness (−50%), redundancy
   (−75%) and pointless placement (−100%), and reward denying *remaining* ward
   lifetime — i.e. it rewards exactly the behaviours that matter (deep,
   non-redundant, on enemy approach paths; early sweep). (§2)
3. **Jungle warding differs structurally from support warding** — junglers keep
   the free *Stealth Ward* trinket, buy Control Wards at full **75 g** (supports
   pay **40 g** post-quest and get a free slot), and place *deep/off-lane* rather
   than in the lane-support redundancy zone. The jungle's information product is
   **"where is the enemy jungler"**, not "is my laner in danger". (§4)
4. **[partial] No clean public "jungler vision-score X → win rate Y" dataset
   with a stated sample size was located this run.** The best quantitative
   evidence is academic (§5) plus mechanic-level reasoning (§2–§4). Marked below.

---

## 1. Source-access notes (this run, 2026-09-24)

- **LoL Wiki MediaWiki API works via tier-1 direct** — clean path:
  `https://wiki.leagueoflegends.com/api.php?action=query&prop=revisions&rvprop=content&rvslots=main&titles=<PAGE>&format=json&formatversion=2`
  (raw wikitext, no JS shell). The `/en-us/index.php?…&action=raw` form **404s**
  through the fetcher. Fetched OK: `Control Ward`, `Stealth Ward`, `Oracle Lens`,
  `Farsight Alteration`, `Vision score`, `Ward`, `Sight`, `World Atlas`,
  `Deep Ward`.
- **OpenAlex / Semantic Scholar work** via direct tier → found the academic
  anchors (§5). Springer chapter abstracts render; the WARDS OA PDF
  (portal.findresearcher.sdu.dk) is **Cloudflare-blocked** (challenge page).
- **Fails this run:** leagueofgraphs.com (Cloudflare 403 on all tiers),
  lite.duckduckgo.com (CAPTCHA challenge), reddit `.json` (403),
  op.gg / u.gg / dpm.lol champion pages (JS shells — **no vision metrics
  extractable**), Bing (returns generic, non-LoL results for ward queries).
  This is why §5's per-role numbers are thin — **not because they don't exist,
  but because the aggregators that hold them don't expose them to a scrape.**

---

## 2. What "vision score" actually measures (mechanics — HIGH confidence)

**Riot's own definition** (via Riot Cosantoir, LoL Wiki archive) and the Wiki
formula: [LoL Wiki, *Vision score*, accessed 2026-09-24; primary ref = Riot
Cosantoir board post] (confidence: **High** — primary source is Riot itself)

> **Vision Score = (1 point per minute of ward lifetime *provided*) + (1 point
> per minute of ward lifetime *denied*).**

Three sources feed it:
- **Ward lifetime provided** — each minute a ward survives yields up to 1 point,
  scored when the ward is destroyed or expires.
- **Ward lifetime denied** — killing an enemy ward grants **1 point per minute of
  *remaining* lifetime** (permanent wards counted as 1.5 min).
- **Vision mechanics** — Scryer's Bloom = **0.5 pt** per champion revealed; Rift
  Scuttler Speed Shrine = **1 pt**; sight-only abilities (Ashe Hawkshot, Kalista
  Sentinel, Quinn Heightened Senses) = **0.33 pt** per champion revealed.

**The "provided" score is penalised for bad wards** — this is the mechanism that
makes vision score a *quality* metric, and it is the most coach-relevant fact here:
- **Staleness:** −0% at 60 s unseen, worsening to **−50%** at 120 s unseen.
- **Redundancy:** −25% for 1 overlapping ally source, up to **−75%** at 3+.
  (Lane minions don't count as redundant if the ward is in brush.)
- **Safety:** wards near your own base score less (down to ~−50%).
- **Pointlessness:** a ward next to an allied structure / inside your base =
  **−100%** (zero score).
- **Baseline:** a ward killed quickly still scores as if it lived **20 s (0.33
  pt)** — spamming instantly-cleared wards is near-worthless.

**Implication for the coach:** *placement* (non-redundant, forward, on enemy
approach paths) is what the score rewards — not clicking the trinket. Deep, live,
non-redundant wards are the goal; ward-count inflation is a vanity metric.

---

## 3. Ward & trinket economy (patch 26.x — HIGH confidence, perishable)

All from LoL Wiki item pages, accessed 2026-09-24.

| Item | Cost | Sight radius | Health | Reward to killer | Notes |
|---|---|---|---|---|---|
| **Stealth Ward** (trinket) | **0 g** | 900 | 3 | **10 g** to enemy | Max **3** placed (shared w/ Totem); 90–120 s duration; visible **1 s** on placement |
| **Control Ward** | **75 g** (support: **40 g** post-quest) | 900 | 4 (regen 1/3 s after 6 s) | **30 g + 40 XP** | **Visible**, **disables** enemy wards/traps; lasts until killed |
| **Farsight Ward** (blue trinket) | 0 g | 500 (→800 on detect 3 s) | 1 | **15 g** | Doesn't count toward ward limit; lasts forever; self-destructs 3 s after spotting a champion |
| **Oracle Lens** (red trinket) | 0 g | 600→750 sweep | — | — | Reveals+disables wards; duration **8 s** (V26.01, up from 6); 2 charges; CD 160→100 s |

- **Placing a ward gives no gold; killing one does.** Attacking a *visible* ward (or
  pinging it) within **10 s** of placement grants **5 g** — removed from the ward's
  bounty. [LoL Wiki, *Ward*, accessed 2026-09-24]
- **Stealth Ward recharge:** V26.03 raised recharge to **210→90 s** (avg champ
  level) from 170→90 — a *nerf to early ward availability*; date this if quoting.
  [LoL Wiki, *Stealth Ward*, patch history]
- **Control-Ward asymmetry:** supports complete the Support Quest (World Atlas),
  after which Control Wards cost **40 g** and live in a **dedicated Role-Quest
  slot** (frees an inventory slot). **Junglers get neither discount nor slot.**
  [LoL Wiki, *Control Ward* / *World Atlas*, accessed 2026-09-24]
- **Deep Ward rune** (Domination slot 2): wards placed in the **enemy jungle** are
  "Deep" → +1 ward health, Stealth Wards last **30–45 s** longer, Totem Wards
  **30–120 s** longer; at lvl 9 the **river** also counts. Wiki strategy note:
  best on "a roaming role such as the **support** or (less so) the **jungler**."
  [LoL Wiki, *Deep Ward*, accessed 2026-09-24]

**Sight-range hierarchy** (so the coach can reason about who sees what):
champions/pets/turrets **1350** > minions **1200** > wards **900** > Farsight
**500**. [LoL Wiki, *Sight*, accessed 2026-09-24]

---

## 4. How the jungle's vision role differs from support's (structural)

Synthesis from the mechanics above + wiki strategy notes (confidence: **Medium**;
mechanic-backed, but the *strategic* framing is Wiki/analyst opinion):

| Dimension | Support | Jungler |
|---|---|---|
| Primary trinket | Trades Stealth Ward → **Oracle Lens** ("eventually supplanted in Support builds"; wiki strategy) | Keeps **Stealth Ward** for its own deep/off-lane coverage |
| Control-Ward cost | **40 g** post-quest | **75 g** full price |
| Control-Ward inventory | Separate **Role-Quest slot** | Uses a real item slot |
| Ward *placement zone* | Lane river pockets, objective pits, lane-support redundancy zone | **Deep enemy jungle, buff/objective approach paths, river** (Deep-Ward-style) |
| Dominant win-lever | Denial (sweeper) + objective/redundant vision | **Deep information on the enemy jungler's path** → tempo/gank/invade decisions |
| What vision *buys* | Lane safety, objective control | **Prediction of the enemy jungler**: enables counter-gank, invade, or free objective |

**The mechanism:** an enemy-jungler **sighting** is worth more than a lane-lantern
ward because it collapses the *opponent's* option space — a jungler seen entering a
quadrant can be counter-played on the far side of the map. This "who is where"
intel is the jungle's core information product and is structurally different from
the support's "is the laner in danger" product. (confidence: **Low–Medium** —
analyst consensus + mechanic reasoning, no dataset.)

**Structural note for the jungle coach:** because the jungler keeps the free
Stealth Ward and pays full price for Control Wards, the jungle's *cheapest*
vision lever is trinket placement on enemy-jungle approach paths, and its
*denial* lever is Oracle-Lens timing — the roles' economics actively push the
jungler toward "deny + deep", exactly the behaviours vision score rewards (§2).

---

## 5. Quantifying the win-rate link (academic evidence)

This is the strongest *quantified* evidence located. Note it is **not**
jungle-specific (no role-split vision dataset found) but it directly tests
whether vision metrics predict winning.

### 5.1 Vision score is a weak winner-predictor — peer-reviewed (2020)

- **Chitayat, Kokkinakis, Patra, Demediuk, Robertson, Olarewaju, Ursu, Kirman,
  Hook, Block, Drachen — "WARDS: Modelling the Worth of Vision in MOBA's"**,
  *Intelligent Computing (SAI 2020)*, Springer AISC vol. 1229, pp. 63–81,
  **doi:10.1007/978-3-030-52246-9_5**. (confidence: **High** — peer-reviewed
  primary; abstract read in full via Springer + SDU Pure.)
  - **Direct finding:** the authors "*examine the accuracy of LoL's vision score
    at predicting the overall game-winner*" and "*found our model [a novel
    warding model] **significantly outperformed LoL's vision score***" — not only
    for the overall winner but also for the *current game state* and for
    *short-term advantage/events*. They also trained a Neural Network to value
    wards in real-time.
  - **Interpretation:** Riot's single-number vision score is a **low-fidelity
    summary** of warding. A model that captures *where* and *when* wards are
    placed predicts outcomes materially better. This is the central citation for
    this axis: **do not treat vision score as a win driver**; treat placement
    context as the signal.
  - *Caveat:* the exact accuracy/F1 gap is in the full paper (paywalled; OA PDF
    Cloudflare-blocked this run). Numbers cited above are verbatim from the
    abstract, not invented.

### 5.2 Vision control is a *mechanism* in large-scale win-prediction ML (2025)

- **Hojaji, McIlroy, Dupuy, Pedroni, Toth, Campbell — "Deep learning techniques
  for identifying KPIs in League of Legends: Win prediction, map navigation, and
  vision control"**, *Computers in Human Behavior Reports*, **2025**,
  **doi:10.1016/j.chbr.2025.100718**. (confidence: **High** for the abstract;
  Gold OA, CC BY-NC-ND.)
  - **Sample:** dataset from **Riot's official API, 154,000 games**; neural
    network reached **97% accuracy** on match-outcome prediction.
  - **Top KPIs (in order):** "*reducing the number of turrets lost is the most
    important metric, followed by increasing bounty level and the number of
    turrets destroyed, reducing damage taken, and increasing the number of
    dragons killed.*" — **note vision score is *not* among the top-5 raw KPIs.**
  - **Vision's role:** "*higher-skilled players spend more time near key map
    objectives, which can be verified by **effective ward placement and overall
    vision control**.*" Vision is framed as an *enabling mechanism* for objective
    pressure, not as a top-line outcome driver.
  - **Interpretation for the coach:** vision is best coached as **positioning-to-
    enable-objectives + info on the enemy jungler**, not as "raise your vision
    score number". The ML ranking is a caution against over-weighting raw vision
    metrics.

### 5.3 Role-difference nulls and other ML baselines (context)

- **E-Sports Player Performance Metrics … Considering Player Roles**, *SN Computer
  Science* **2023**, **doi:10.1007/s42979-022-01660-6** (same study cited in Axis
  2): role-aware ML; "*the difference in the influence of the individual player
  roles on the outcome of the game … is negligible*"; prediction accuracy
  **86%**. (confidence: **Medium** — abstract only.) No role-split vision metric
  is reported.
- **Machine Learning Models on MOBA Gaming: LoL Winner Prediction**, *Acta
  Infologica* **2023**, **doi:10.26650/acin.1180583**: LoL winner prediction is
  feasible at high accuracy (**LightGBM 0.97, LogReg 0.96, SVM/GBC 0.95**);
  "key performance metrics and their impact" analysed. (confidence: **Medium** —
  abstract only; **no vision/ward-specific coefficient reported**.)

### 5.4 What remains unquantified (honest gap)

- **No public source located this run** gives, with a stated sample size and rank
  band: (a) average **vision score per role**, (b) average **Control-Ward
  purchases per role**, or (c) a **jungle-specific** vision-score → win-rate
  coefficient. The aggregators that hold such data (op.gg, u.gg, dpm.lol,
  leagueofgraphs) expose it only via JS/API and were not scrapeable here.
  **Any number of that shape must be rebuilt from Riot's Match-V5 API, not
  quoted from a blog.** (confidence: **High** that this is a gap.)

---

## 6. Coach takeaways (actionable, mechanic-backed)

1. **Do not grade the jungler on vision score.** Grade on **(i) deep-ward
   placement on enemy-jungle/approach paths, (ii) non-redundant placement,
   (iii) sweeper/denial timing before objectives** — the four things vision score
   rewards (§2) and the thing the WARDS model captured better than vision score
   (§5.1).
2. **Ward *timing* over ward *count*.** A ward that survives its full duration in
   a forward, non-redundant spot beats three wards dropping in the redundancy
   zone (which score ≤25–75% of value).
3. **Denial is first-class.** Killing an enemy ward scores 1 pt per minute of its
   *remaining* lifetime — so sweep **before** the ward is about to matter
   (objective setup), not after.
4. **Remember the jungle's economics:** free Stealth Ward trinket + 75 g Control
   Wards (no support discount) ⇒ the cheapest jungle vision is *trinket placement
   deep*, and the cheapest denial is *Oracle Lens on cooldown*. Coach around that.
5. **Tie vision to a decision:** the jungle's vision payoff is *information about
   the enemy jungler that changes a gank/invade/objective call*. "Ward for a
   reason" is the coaching line.

---

## Sources (all accessed 2026-09-24)

- LoL Wiki, *Vision score* — https://wiki.leagueoflegends.com/en-us/Vision_score (primary ref: Riot Cosantoir)
- LoL Wiki, *Control Ward* — https://wiki.leagueoflegends.com/en-us/Control_Ward
- LoL Wiki, *Stealth Ward* — https://wiki.leagueoflegends.com/en-us/Stealth_Ward
- LoL Wiki, *Oracle Lens* — https://wiki.leagueoflegends.com/en-us/Oracle_Lens
- LoL Wiki, *Farsight Alteration* — https://wiki.leagueoflegends.com/en-us/Farsight_Alteration
- LoL Wiki, *Ward* — https://wiki.leagueoflegends.com/en-us/Ward
- LoL Wiki, *Sight* — https://wiki.leagueoflegends.com/en-us/Sight
- LoL Wiki, *World Atlas* — https://wiki.leagueoflegends.com/en-us/World_Atlas
- LoL Wiki, *Deep Ward* — https://wiki.leagueoflegends.com/en-us/Deep_Ward
- Pedrassoli Chitayat et al., *WARDS: Modelling the Worth of Vision in MOBA's*, Springer AISC 1229 (2020), doi:10.1007/978-3-030-52246-9_5
- Hojaji et al., *Deep learning techniques for identifying KPIs in League of Legends*, Comput. Human Behav. Reports (2025), doi:10.1016/j.chbr.2025.100718
- *E-Sports Player Performance Metrics … Considering Player Roles*, SN Comput. Sci. (2023), doi:10.1007/s42979-022-01660-6
- *Machine Learning Models on MOBA Gaming: LoL Winner Prediction*, Acta Infologica (2023), doi:10.26650/acin.1180583
