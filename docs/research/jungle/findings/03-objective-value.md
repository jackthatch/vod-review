# Axis 3 — Objective value and prioritisation

> **Status: re-run research (2026-09-24), supersedes the provisional Run-1 notes.**
> Every mechanical claim is verified against the **live patch** (Riot display
> **26.19** / Data Dragon **16.19.1**, accessed 2026-09-24) via the LoL Wiki
> MediaWiki API and Riot patch notes; every statistic carries number + source +
> date + patch. Unsourced claims are marked `confidence: Low`.
> Tooling: all fetches via `tools/fetch_page.py` (see `00-environment-constraints.md`).

---

## 0. Headline answers (TL;DR)

1. **The objective set changed in 2026.** **Atakhan, Blood Roses and Feats of
   Strength were REMOVED in patch 26.1** — they are **not live** and must not be
   coached as if they were. Riot's stated reason: Atakhan "contributed to an
   extremely objective-focused game" [Riot Patch 26.1 Notes, 2026-01-07].
2. **Baron Nashor returns to a 20:00 spawn** (it had been pushed late in 2025),
   and Rift Herald despawns at 19:45 to hand the pit over to him
   [LoL Wiki: Rift Herald / Baron Nashor, accessed 2026-09-24].
3. **Riot's only published *win-rate-after-objective* numbers are First Blood and
   First Turret** — **57.6% → 55.4%** and **70.4% → 70.3%** (patches 14.24 →
   25.S1.2). **Riot has never published solo-queue win rates for drakes, Dragon
   Soul, Voidgrubs, Rift Herald or Baron.** Re-verified verbatim from the Riot
   landing post this run.
4. **Real, gold-controlled per-objective win-rate data DOES exist** — but from
   independent analysts, not Riot (§3). Best figure: **6 Voidgrubs ≈ +19.7% WR
   vs 2 drakes ≈ +17% WR** at even gold (split 1 2025) → grubs *slightly* better
   then; **26.1 later nerfed grubs**, so treat as directional not current.
5. **"Dragon Soul ≈ Baron" is *design intent*, not a measurement.** Use it to
   argue *time commitment*, not equivalence of win probability.
6. **Riot's 2026 direction deliberately de-emphasises teamfighting over every
   objective** — the coach should not assume every objective must be contested;
   "concede and trade" now has an explicit Riot rationale.

---

## 1. Verified current objective set + spawn timings (live patch 26.x)

Timings from the **LoL Wiki MediaWiki API** (`wiki.leagueoflegends.com/api.php`,
`action=parse&prop=wikitext`), accessed **2026-09-24**; cross-checked against
Riot patch 26.1 notes (2026-01-07). Confidence: **High** (two independent sources).

| Objective | Spawn | Repeat / despawn | Notes |
| --- | --- | --- | --- |
| **Elemental Drake** (pit) | **5:00** | respawns **5:00** after each kill; random element until Rift Shift | After 2nd drake slain / 3rd determined → Elemental Rift; that element repeats thereafter. [LoL Wiki: Dragon pit] |
| **Elder Dragon** | after a team's **4th drake** | respawn **6:00** | "most powerful of all dragons"; buff "meant to rival Baron". [LoL Wiki: Elder Dragon] |
| **Voidgrubs** | **8:00** | **one camp per game**; despawns **14:45** (14:55 if in combat) | Camp of **3** grubs. Gold/XP **cut in 26.1**. [LoL Wiki: Voidgrub camp; Riot 26.1] |
| **Rift Herald** | **15:00** (same pit slot as grubs) | **one per game**; despawns **19:45** (19:55 if in combat) | Baron replaces her at 20:00. [LoL Wiki: Rift Herald] |
| **Baron Nashor** | **20:00** | respawn **6:00** | Spawn timer moved **25:00 → 20:00 in patch 26.1**. [LoL Wiki: Baron Nashor; Riot 26.1] |
| ~~Atakhan~~ | — | **REMOVED** | Removed in 26.1. [Riot 26.1] |
| ~~Blood Roses~~ | — | **REMOVED** | Removed with Atakhan in 26.1. [Riot 26.1] |
| ~~Feats of Strength~~ | — | **REMOVED** | Removed in 26.1; first-blood (100g) / first-turret (300g) gold **restored** as replacements. [Riot 26.1] |

**Spawn-flow sanity check (baron pit):** grubs 8:00 → despawn 14:45 → Herald
15:00 → despawn 19:45 → Baron 20:00. Dragon pit runs on its own 5-min cycle from
5:00. Confidence: **High**.

### How 26.1 changed objective *value*, not just timing

Riot patch 26.1 (2026-01-07) reworked epic-monster rewards wholesale
[source: Riot 26.1 Notes, verified this run]:

- **Epic monsters ~10–30% more durable** (late elemental drakes slowed further),
  paired with a **Smite buff** (600/900/1200 → 600/1000/1400) so junglers aren't
  disproportionately penalised. Riot's goal: raise the *risk* of taking neutrals
  to "the danger level of pushing for turrets."
- **Most epic monsters no longer reward "simply being around when it dies"** →
  reduces the value of hovering as a non-slayer and rewards the actual killer.
- **Voidgrubs (26.1):** gold **20 local + 50 global (210g) → 30 local (90g)**;
  experience **75 + 2%/level → 65 (195 for 3)**; mites' AD/HP sharply cut. Net:
  grubs are **structurally weaker as a gold/XP objective** in 2026.
- **Rift Herald (26.1):** min level 6→9; HP/armour rebuilt; **eye cooldown 8→6 and
  no longer reduced on-hit** ("more solo-able… junglers can claim it by
  themselves"); gold shifted from *nearby champions* to **100g to the killer**;
  mercenary charge damage **2500–3000 → 3000**. Riot frames Herald as "a valuable
  objective due to its ability to knock down turrets."
- **Baron (26.1):** spawn 25m→20m; gold reduced; experience made **global and
  comeback-oriented**; buff power preserved as "a meaningful game-ender"; shred
  re-added (0.5 armour/MR per second to nearby enemies). Riot's own punchline:
  *"You thought pro teams were done throwing the game at 20 minute objective
  fights? Think again!"*
- **Dragon Soul / epic-monster time:** Riot states *"Claiming Dragon Soul is just
  as impactful as taking Baron Nashor, so we want the time commitment for doing so
  to be comparable."* — **design intent, not measured equivalence.**
  Confidence: **Medium** (single primary source; no win-rate data attached).

---

## 2. Riot-published win-rate-after-objective numbers

**These are the ONLY objective win-rate numbers Riot has ever published.** They
are *gold-priority* objectives, not neutral monsters. Re-verified **verbatim**
this run from the Riot landing post (browser tier).

> **"Percent Win Rate after Claiming Each Objective"**
>
> | Objective | Patch 14.24 | Patch 25.S1.2 |
> | --- | --- | --- |
> | **First Blood** | **57.6%** | **55.4%** |
> | **First Turret** | **70.4%** | **70.3%** |

Riot's own conclusion: *"these metrics haven't substantially changed from 14.24,
so game pacing and overall snowballing are in roughly the same place as before
Season 1."* The post also confirms Season 1 **removed** the gold from First Blood
& First Turret (later **restored in 26.1**).
Source: [Riot /dev: How the Season 1 Changes Landed](https://www.leagueoflegends.com/en-us/news/dev/dev-how-the-season-1-changes-landed/),
Season 1 2025 landing post (compares patch 14.24 → 25.S1.2). Confidence: **High**
(read directly from Riot's page). Tier: **Primary**.

> **Correction carried forward:** Run 1's claim that Riot's table contained
> drakes/grubs/Herald/Baron/Atakhan is **wrong**. The table had **only** First
> Blood and First Turret.

---

## 3. Real per-objective win-rate data (independent analysts)

Riot publishes none, so the only quantitative per-objective win rates come from
third-party analyses. Two high-effort sources surfaced this run — both **gold-
controlled** (i.e. they isolate objective value from "the winning team gets the
objectives" confounding):

### 3a. MachineLoling — "Real Objective Values, First Split 2025" (published 2025-06-26)

**Method:** 8 million **diamond+** games (NA, EUW, EUN, KR, VN), split 1 2025;
win-probability computed **at the point where gold, dragon and grub leads are held
at zero**, so the deltas are closer to causal than raw site win rates.
Source: [machineloling.com](https://machineloling.com/2025/06/26/real-objective-values-first-split-2025-grubs-or-drakes/).
Confidence: **Medium** (large sample but independent analyst; author admits some
input estimates are rough). Tier: **Established**.

| Objective | Measured win-rate effect (even gold) | Notes |
| --- | --- | --- |
| **1 dragon** | **+8.0% WR** | 0-grub-lead games |
| **2 dragons** | **+16.9% WR** | 0-grub-lead games |
| **First 3 Voidgrubs** (~5 min) | **+3.9% WR** (gold only) | ~219g early gold |
| **Second 3 Voidgrubs** (~15 min) | **+2.7% WR** (gold only) | ~219g mid gold |
| **6-grub passive** | **+11.0% WR** | Touch of the Void structural value |
| **All 6 grubs (total)** | **≈ 19.7% WR** | 17.6% direct + ~2.1% from plate pressure |
| **Feats of Strength** | **≈ +4% WR** | **removed in 26.1** |
| **Atakhan** | **≈ +15% WR** | **removed in 26.1** |
| **First Blood (100g, ~5 min)** | **≈ 1.7% WR** | gold-equivalent |
| **First Turret (300g, ~15 min)** | **≈ 3.0% WR** | gold-equivalent |

**Author's headline:** *"For the record, that's 19.7% WR for 6 grubs vs 17% WR
for 2 dragons. **Grubs were better split 1**."* And on Feats: *"feats FELT more
important than the 4% WR they actually gave."*
**Caveats:** measured **pre-26.1**; Riot has since **cut grub gold by ~57% and
grub XP**, so the grub figure is **stale/directional only** for the live patch.
Atakhan/Feats rows are historical (features now deleted).

### 3b. Dennis Lin — "EarlyEdge: Tempo vs Value Objective Analysis" (published 2024-12-07)

**Method:** 16,606 **professional** team-level games (Oracle's Elixir, 2024 meta);
tests whether tempo objectives (grubs/Heralds) or value objectives (dragons/soul)
correlate more with wins. Source: [dennlin.github.io/early-edge](https://dennlin.github.io/early-edge/).
Confidence: **Medium** (clean methodology; pro-play only, so not directly
transferable to solo queue). Tier: **Established**.

Win rate by objective combination:

| Voidgrubs | Heralds | Dragon Soul | Dragons | Win rate |
| --- | --- | --- | --- | --- |
| 0 | 0 | False | 2 | **21%** |
| 0 | 1 | True | 4 | **88%** |
| 3 | 1 | False | 4 | **83%** |
| 6 | 1 | True | 5 | **100%** |

Correlation matrix (Pearson): **Heralds ↔ towers 0.32**, **Voidgrubs ↔ towers
0.22**, **Dragon Soul ↔ total dragons 0.71**, **Dragon Soul ↔ towers 0.38**.
**Finding:** tempo objectives drive *immediate map control / tower destruction*;
dragon soul matters most in **long** games. Pro teams with 3 grubs + 1 Herald but
**no soul** still won **83%** — tempo-alone can be decisive.

### 3c. Dragon-soul win rates by element (older, low confidence)

| Souls (Plat+), ranked | Source | Date | Confidence |
| --- | --- | --- | --- |
| Chemtech **89.4%**, Hextech **88.8%**, Mountain **88.2%**, Cloud **87.5%**, Ocean **86.6%**, Infernal **86.4%** | procomps.gg blog quoting **leagueofgraphs** | 2022-08; **pre-2026 soul reworks** | **Low** (aggregator citing aggregator; outdated) |

**Interpretation:** souls cluster tightly (86–89%), so *which* soul is far less
important than *reaching* soul at all — drake element is a marginal tiebreaker,
**not** a reason to throw a game.

> **No recent (2025–2026) per-objective solo-queue win rates were obtainable from
> first-party stat sites.** leagueofgraphs — the canonical source for drake and
> objective win rates — is hard-Cloudflare-blocked from this datacenter IP on all
> three fetch tiers (re-verified 2026-09-24). lolalytics has no global objective
> page. This is a genuine, honest gap — **do not fabricate numbers**.

---

## 4. Pro / model evidence that objectives are outcome drivers

- Riot's **lolesports Win-Probability model** (with AWS) lists **dragon kills
  (incl. soul), Herald trinket, Baron and Elder timers** among its predictive
  features — evidence Riot treats objectives as win-state features, though **no
  per-objective coefficients are published**
  [lolesports Dev Diary](https://lolesports.com/article/dev-diary-win-probability-powered-by-aws-at-worlds/blt0).
  Confidence: **Medium**, tier Primary.
- Academic win-prediction work finds **~81.6% accuracy only late-game** and
  near-coin-flip discrimination early ([arXiv 2309.02449](https://arxiv.org/abs/2309.02449))
  — being ahead on objectives early does **not** lock the result. Confidence:
  **Medium**, tier Primary. *(Axis-1 relevant; cited so the coach does not
  over-weight an early objective lead.)*

---

## 5. Correct prioritisation (synthesis for the coach)

> **Reasoned prioritisation from the verified mechanics + measured data above, not
> a single measured ranking.** Overall `confidence: Medium`. Each line cites its basis.

**Tier 1 — game-ending, contest-worthy:**
- **Baron Nashor (20:00+).** Riot preserves its "meaningful game-ender" buff while
  making it a *comeback lever* via global XP; 26.1 made the fight longer and more
  lethal to the *attacking* team. Basis: Riot 26.1.
- **Dragon Soul / Elder.** Riot states Soul ≈ Baron in impact and staged timings
  so reaching either costs comparable time; souls sit in the 86–89% band. Basis:
  Riot 26.1 + §3c.

**Tier 2 — structural/tempo, take when the trade is good:**
- **Rift Herald (15:00, despawn 19:45).** Riot calls it "valuable… ability to knock
  down turrets"; 26.1 made the eye **more solo-able** and moved gold to the
  killer. Best correlation with towers in pros (0.32). Strong **solo-jungler
  tempo/plate** objective. Basis: Riot 26.1 + §3b.
- **Voidgrubs (8:00, despawn 14:45).** **Value substantially cut in 26.1** (gold
  210g→90g, XP cut). Historically very strong (6 grubs ≈ 19.7% WR split 1 2025)
  but that figure pre-dates the nerf — now a **tower-pressure/tempo** objective,
  not a gold one. Do **not** over-invest. Basis: Riot 26.1 + §3a.
- **Elemental Drakes (early–mid).** Individually modest (+8% per drake at even
  gold — §3a); the real payoff is the **4th-drake soul**. Play for soul, not
  drake #1. Basis: §3a + wiki Rift Shift.

**Tier 3 — do not force:**
- Contested fights **over every objective**. Riot's explicit 2026 goal is to move
  *away* from "teamfighting over neutral objectives" toward **splitting and
  sieging** [Riot /dev: 2026 Season One Gameplay Preview, 2025-12-01].
  **Conceding an objective to take towers/plates on the far side is often correct.**

### Priority cheat-sheet

```
20:00+  Baron / Soul / Elder   → game-ending; contest with numbers & vision
15:00   Rift Herald            → solo-able tempo; knock towers, take plates
8:00    Voidgrubs (→14:45)     → tempo only; value cut in 26.1, low gold
5:00+   Elemental drakes       → play for the SOUL (4th), not drake #1
any     "every objective"      → REPLACE with trade-evaluation (Riot 2026 direction)
```

**Removed-objective rule (critical):** When reviewing any VOD from before 26.1
(2025 season), Atakhan / Feats of Strength / Blood Roses *did* exist — coach them
in their historical context (Atakhan was worth ~+15% WR and Feats ~+4% — §3a).
**From 26.1 onward they are gone**; a review that tells a player to "fight for
Atakhan" or "secure Feats" is **wrong**. Confidence: **High** (Riot 26.1,
2026-01-07).

---

## 6. Gaps & next actions

- **No Riot win-rate numbers for neutral monsters.** Only First Blood / First
  Turret exist. **Gap: unquantified by Riot** for drake, soul, grubs, Herald, Baron.
  (Third-party gold-controlled figures in §3 fill this, at Medium confidence.)
- **leagueofgraphs blocked** (hard Cloudflare, all tiers, verified 2026-09-24) —
  the best first-party source for per-objective win rates is unreachable.
  **Action:** wire a residential proxy (tier 0) or a paid stats API.
- **Grub value figures are pre-26.1 and now stale** (grub gold/XP were cut).
  **Action:** re-run a MachinLoling-style gold-controlled analysis on a **26.x**
  dataset to get current grub/drake/herald/Baron deltas.
- **§3c soul figures are 2022-era** and pre-date all soul reworks.
  **Action:** re-pull current soul win rates once a reachable source is found.
- **No measured Baron-vs-Soul equivalence** exists — Riot's claim is intent only.
  `confidence: Low`.

## Sources (all accessed 2026-09-24 unless noted)

1. Riot Patch **26.1** Notes — https://www.leagueoflegends.com/en-us/news/game-updates/patch-26-1-notes/ (published 2026-01-07)
2. Riot /dev: **2026 Season One Gameplay Preview** — https://www.leagueoflegends.com/en-us/news/dev/dev-2026-season-one-gameplay-preview/ (published 2025-12-01)
3. Riot /dev: **How the Season 1 Changes Landed** — https://www.leagueoflegends.com/en-us/news/dev/dev-how-the-season-1-changes-landed/ (Season 1 2025; patches 14.24 → 25.S1.2)
4. **LoL Wiki** MediaWiki API (wikitext): `Dragon pit`, `Elder Dragon`, `Voidgrub camp`, `Rift Herald`, `Baron Nashor` — https://wiki.leagueoflegends.com/api.php
5. **MachineLoling** — Real Objective Values, First Split 2025 (2025-06-26) — https://machineloling.com/2025/06/26/real-objective-values-first-split-2025-grubs-or-drakes/
6. **Dennis Lin — EarlyEdge** — Tempo vs Value Objective Analysis (2024-12-07) — https://dennlin.github.io/early-edge/
7. **lolesports Dev Diary** — Win Probability powered by AWS — https://lolesports.com/article/dev-diary-win-probability-powered-by-aws-at-worlds/blt0
8. **arXiv 2309.02449** — win-probability modelling — https://arxiv.org/abs/2309.02449
9. **procomps.gg** blog (quoting leagueofgraphs soul win rates, 2022-08) — https://hub.procomps.gg/2022/08/dragon-soul-win-rates-which-dragon-is-the-strongest/
10. **Riot Data Dragon** `versions.json` (live = 16.19.1) — https://ddragon.leagueoflegends.com/api/versions.json
