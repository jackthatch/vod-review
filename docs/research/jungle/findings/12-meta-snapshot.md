# Axis 12 — Current jungle meta snapshot (**PATCH-DATED — PERISHABLE**)

> ## ⚠️ PERISHABLE SNAPSHOT — READ FIRST
> **Patch: Riot marketing `26.19` / game-version `16.19`** (the two labels are the
> *same live patch* — §0.1). **Patch 26.19 went live 2026-09-23; this snapshot was
> captured 2026-09-24 (UTC) — i.e. ~1 day into the patch**, so win-rate deltas are
> still settling and move daily for the first week.
> **Rank band: Emerald+ (ranked Solo/Duo, GLOBAL).**
>
> This axis is a **dated photograph, not an invariant**. Every win/pick/ban number
> below drifts within days of the next patch (and often within the same patch as
> player behaviour adjusts). **Do not quote any figure here after the next patch
> drops.** Re-pull and overwrite this file each patch. All numbers were true at the
> capture timestamp only.
>
> Compiled by a sub-agent for the jungle research study. Every number carries its
> source + capture date. Unsourced / single-source claims are flagged
> `confidence: Low/Medium`. Sections flagged **[partial]** are incomplete.

---

## 0. Header facts

### 0.1 The patch-label discrepancy (both labels, explicitly)

Two live sites print **different strings for the identical live patch**, and the
study task flagged this in advance:

| Site | Rendered patch string | URL | Capture date |
|---|---|---|---|
| lolalytics | **`16.19`** | lolalytics.com/lol/tierlist/?lane=jungle | 2026-09-24 |
| u.gg | **`26.19`** | u.gg/lol/tier-list?role=jungle | 2026-09-24 |
| LoL Wiki (primary patch page) | **`V26.19`**, release **2026-09-23** | wiki.leagueoflegends.com | 2026-09-24 |

`16.19` is the **Riot *game-version* string** (the value in the client / Data
Dragon); `26.19` is the **2026-season *marketing* patch number**. Both refer to
the **same live patch**. Where this file writes "patch 26.19" it means the live
patch ≡ lolalytics' `16.19`. *(Sources: lolalytics page title prints `16.19`,
u.gg page title prints `Patch 26.19`, LoL Wiki patch page `V26.19`; all
2026-09-24. Reported rather than silently reconciled.)* **confidence: High** that
the labels differ and denote the same patch.

### 0.2 What is NOT in the game right now

**Atakhan and Feats of Strength were REMOVED in patch 26.1 (2026).** They do
**not** exist in 26.19. Do not treat them as live objectives in any analysis that
builds on this snapshot. *(Patch-26.1 removal; consistent with Axes 0/3.)*
**confidence: High.**

### 0.3 Method / access note

- lolalytics tier list rendered **server-side** and was read directly at
  `?lane=jungle&tier=emerald_plus`. The rendered table shows the **top 20**
  champions by lolalytics' composite tier score at the default filters (Min Lane%
  = 2, Min Games = 100, Min Pick% = 0). **§3 (weakest picks) is therefore derived
  from the same top-20 window and labelled [partial].**
- lolalytics "average Emerald+ win rate" baseline at capture: **51.38%** (so a
  50% champion is *below* the band average; read win rates relative to 51.38%,
  not 50%). Emerald+ champions analysed: **3,128,787** games.
- u.gg's parallel page at the same band (Emerald+) reported **2,600,120 champions
  analysed**, "Last Updated: 4 hours ago" *(capture 2026-09-24)* — a second site
  confirming the same **26.19 / Emerald+** framing (its per-champion rows are
  JS-rendered and were not extractable this run; used for label corroboration).
- lolalytics tier score weighs **win rate + PBI index + best-player statistics**,
  not win rate alone — hence the rank order is *not* pure win-rate order (e.g.
  Rammus has the **highest** win rate on the board at 55.02% but sits at rank
  **#14**).

---

## 1. TL;DR (headline)

*All figures **patch 26.19 (≡16.19), Emerald+, GLOBAL, captured 2026-09-24**,
unless stated. Source: lolalytics jungle tier list unless stated.*

1. **Top-3 by composite tier at Emerald+ are Wukong (S+, 53.58% W), Talon (S+,
   51.98% W), Nidalee (S, 52.58% W).** Wukong is the #1 pick in the tier model
   but is *not* the highest win-rate champion (§2, §3).
2. **Highest raw win rate on the board = Rammus 55.02%** (pick 2.14%, ban 4.48%,
   A tier, 6,690 games) — a classic low-pick sleeper, ranked only #14 because of
   its low presence. **Skarner 53.27%** (pick 1.09%, ban 0.25%, only 3,424 games)
   is the strongest *tier-model* low-presence outlier. Both are small-sample
   relative to the pool → win rate is **Medium** confidence as a stable signal.
3. **Presence leaders (pick+ban) at Emerald+:** **Lee Sin** (pick 13.37%, ban
   19.08%) and **Sylas** (pick 7.98%, ban 19.32%) are the most-contested junglers;
   Sylas and Lee Sin are the two highest-ban champions in the top 20.
4. **Weakest performers in the top-20 window:** **Kha'Zix (50.35% W, 8.89% P),
   Lee Sin (50.64% W, 13.37% P), Ekko (51.11% W), Kayn (51.28% W)** — all *below*
   the 51.38% Emerald+ band average. High-popularity picks (Lee Sin, Kha'Zix,
   Kayn) sitting under the band average is the headline "popular-but-underperforming"
   signal. §3 **[partial]**.
5. **Jungle-relevant patch changes landed *this patch* (26.19):** buffs to
   **Elise, Kha'Zix, Lillia** and Rumble's monster damage; nerfs to **Master Yi,
   Nocturne, Poppy**'s jungle tools (full list §4). The win-rate deltas shown on
   the board (Rammus +2.45, Briar +2.23, Shaco +2.12, …) are week-over-week
   movements, **not** the same as the patch-note list — read them separately.

---

## 2. Top junglers — Emerald+, patch 26.19/16.19, captured 2026-09-24

**Source: lolalytics.com/lol/tierlist/?lane=jungle&tier=emerald_plus**, direct SSR
read, 2026-09-24. Band average Win = **51.38%**. Columns: lolalytics Tier, Win%,
Pick%, Ban%, Games. (The number after Win% on lolalytics is a win-delta vs the
prior patch — shown in §1.5 only.)

| # | Champion | Tier | Win % | Pick % | Ban % | Games |
|---|---|---|---|---|---|---|
| 1 | **Wukong** | S+ | **53.58** | 5.93 | 3.90 | 18,559 |
| 2 | **Talon** | S+ | **51.98** | 6.08 | 10.16 | 19,017 |
| 3 | **Nidalee** | S | **52.58** | 3.17 | 2.61 | 9,906 |
| 4 | **Sylas** | S | 51.69 | 7.98 | **19.32** | 24,980 |
| 5 | **Skarner** | S | 53.27 | 1.09 | 0.25 | 3,424 |
| 6 | **Cho'Gath** | S- | 53.18 | 6.56 | 4.64 | 20,519 |
| 7 | **Shaco** | S- | 52.88 | 4.18 | 17.31 | 13,088 |
| 8 | **Master Yi** | S- | 52.56 | 6.58 | 14.76 | 20,586 |
| 9 | **Lee Sin** | A+ | 50.64 | **13.37** | 19.08 | 41,825 |
| 10 | **Jax** | A+ | 52.27 | 0.94 | 9.98 | 2,927 |
| 11 | **Ekko** | A+ | 51.11 | 4.13 | 2.13 | 12,916 |
| 12 | **Zac** | A+ | 52.72 | 3.02 | 1.16 | 9,444 |
| 13 | **Shyvana** | A+ | 53.14 | 4.71 | 5.64 | 14,726 |
| 14 | **Rammus** | A | **55.02** | 2.14 | 4.48 | 6,690 |
| 15 | **Rek'Sai** | A | 52.51 | 1.35 | 0.65 | 4,230 |
| 16 | **Kayn** | A | 51.28 | 6.70 | 4.69 | 20,977 |
| 17 | **Elise** | A | 52.51 | 2.87 | 1.55 | 8,988 |
| 18 | **Darius** | A | 51.73 | 0.66 | 12.14 | 2,051 |
| 19 | **Briar** | A | 52.87 | 4.31 | 8.44 | 13,483 |
| 20 | **Kha'Zix** | A- | 50.35 | 8.89 | 4.89 | 27,822 |

*All rows: source lolalytics jungle tier list, Emerald+, patch 26.19/16.19,
captured 2026-09-24. **confidence: High** for the numbers as rendered; the
tier-model *ordering* is lolalytics' own composite, not a pure win-rate sort.*

**Readings of this table**

- **Highest win rates (≥52.5%):** Rammus 55.02, Wukong 53.58, Skarner 53.27,
  Cho'Gath 53.18, Shyvana 53.14, Shaco 52.88, Briar 52.87, Zac 52.72, Nidalee
  52.58, Master Yi 52.56, Rek'Sai 52.51, Elise 52.51.
- **Below band-average win rate (<51.38%):** Kha'Zix 50.35, Lee Sin 50.64, Ekko
  51.11, Kayn 51.28.
- **Presence (pick+ban) leaders:** Lee Sin 32.45, Sylas 27.30, Shaco 21.49,
  Master Yi 21.34, Talon 16.24, Kha'Zix 13.78, Shyvana 10.35.
- **Near-zero presence outliers (sample-size caveat):** Skarner (1.09% P / 0.25%
  B), Darius (0.66% P), Jax (0.94% P), Rek'Sai (1.35% P). Small pick rates ⇒
  noisier win rates ⇒ **confidence: Medium** individually.
- **Week-over-week win-delta movers (lolalytics Win column):** up — Rammus
  +2.45, Briar +2.23, Shaco +2.12, Jax +2.00, Master Yi +1.93, Shyvana +1.88,
  Wukong +1.83 pp; also positive Kayn +1.66, Darius +1.51, Sylas +1.40, Cho'Gath
  +1.35, Skarner +1.32, Lee Sin +1.24, Ekko +1.24, Zac +1.24. *(These are observed
  live-patch movements, not patch-note buffs — §4.)* **confidence: High** for the
  rendered deltas, **Low** for causal attribution.

---

## 3. Strongest vs weakest right now — the aggregate read **[partial]**

**Strongest (composite).** On lolalytics' weighted tier score at Emerald+ the
**S / S+ band is Wukong, Talon, Nidalee, Sylas, Skarner** (rank 1–5). On **raw win
rate** the leaders are **Rammus (55.02)**, **Wukong (53.58)**, **Skarner
(53.27)**. The two readings agree on **Wukong** as the standout; they disagree on
Rammus (highest WR but low presence) — lolalytics discounts low-presence spikes.
**confidence: High** for the numbers; **Medium** for which single champion is
"the strongest" (tier model vs raw WR diverge by design).

**Weakest in the measured window [partial].** Within the top-20 view, the four
champions *below* the 51.38% band average are **Kha'Zix (50.35% W, 8.89% P),
Lee Sin (50.64% W, 13.37% P), Ekko (51.11% W), Kayn (51.28% W)**. Kha'Zix and Lee
Sin carry meaningful pick rates *and* sit under the band average — the clearest
"popular but underperforming in this band" flags. **Caveat:** this is the
**top-20 by tier**, not the whole jungle pool; champions ranked #21+ (lower tiers)
are not captured here. Do not read "Kha'Zix is the worst jungler" — read "the
four highest-tiered entries below the band average are these." **confidence:
Medium [partial]**.

---

## 4. Current jungle-relevant patch changes (patch 26.19)

**Source: LoL Wiki `V26.19` wiki-text, retrieved 2026-09-24** (patch released
**2026-09-23**). The patch was a **champion-balance patch with NO jungle-camp /
jungle-system / Smite changes** — the only item changes were two *support* quest
items (Runic Compass, World Atlas), and the only Game change was the Top-lane
Quest Teleport cooldown (420→390s). All jungle impact this patch is therefore
**indirect, via champion ability changes to junglers**.

**Jungle-relevant champion changes in 26.19**

| Champion | Change | Direction for jungle | Note |
|---|---|---|---|
| **Elise** | Spider Queen base dmg **12→14** (→44 at rank 4, from 42); Skittering Frenzy bonus AS **60–120% → 70–130%** | **Buff** | gank/duel damage |
| **Kha'Zix** | Unseen Threat base dmg **17→22** (→141 from 136); Evolved Spike Racks slow **2→2.25s**; Evolved Wings bonus range **200→300** | **Buff** | clear + isolation dmg |
| **Lillia** | Base armor **22→24**; Lilting Lullaby sleep **2→2.5s** | **Buff** | clear durability + gank CC |
| **Rumble** | Overheated monster-cap damage **65–150 → 90–175**; but Overheated bonus AS **50–130% → 30–100%** | **Mixed (jungle-clear dmg up)** | jungle Rumble |
| **Master Yi** | Alpha Strike on-hit CDR **no longer reduced by ability haste** | **Nerf** | sustained DPS/tempo |
| **Nocturne** | Paranoia cooldown **140–90s → 160–100s** | **Nerf** | ult availability |
| **Poppy** | Hammer Shock monster-cap damage **85–225 → 70–210** | **Nerf (jungle clear)** | jungle Poppy clear speed |
| **Vi** | Base AD **63→61**, AD growth **3.5→3.9**, Blast Shield health ratio **12%→10%** | **Nerf-ish (early)** | jungler |
| **Volibear** | Relentless Storm: AS per stack AP ratio **3%→4% per 100 AP**, max-stack too; **new** Lightning Claws damage also scales **+20% bonus AD** | **Buff (flex)** | jungle/top |

*Source: LoL Wiki V26.19, retrieved 2026-09-24. Champions changed by 26.19 that
are not jungle-relevant and omitted: Aatrox, Aphelios, Aurora, Camille, Draven,
Fiora, Lucian, Nasus, Renata Glasc (bugfix), Renekton (bugfix), Ryze, Taliyah,
Yone (bugfix), Yunara (bugfix), Nunu & Willump (bugfix).* **confidence: High** for
the listed changes (primary wiki transcription).

> **Do not conflate §2's win-deltas with §4's buffs/nerfs.** §2's numbers are
> observed week-over-week movements on the live patch; §4 is the documented
> ability-change list. Note the *tension* worth watching next patch: **Kha'Zix —
> buffed in 26.19 but currently the lowest win rate in the top-20 (50.35%)**; and
> **Master Yi — nerfed, yet still S- (52.56%)**, suggesting the nerf has not yet
> moved its Emerald+ win rate in this early-patch window. **confidence: Low** for
> any causal read (1-day-into-patch data).

---

## 5. Provenance & regeneration

| Field | Value |
|---|---|
| Live patch | **26.19** (Riot) ≡ **16.19** (game version / lolalytics); released **2026-09-23** |
| Capture date | **2026-09-24** (UTC) — ~1 day into patch 26.19 |
| Rank band | **Emerald+**, ranked Solo/Duo, GLOBAL |
| Primary stat source | lolalytics.com/lol/tierlist/?lane=jungle&tier=emerald_plus (direct SSR) — top 20, avg WR 51.38%, 3,128,787 games |
| Corroborating stat source | u.gg/lol/tier-list?role=jungle (Emerald+, Patch 26.19, 2,600,120 games, "updated 4h ago") — label/band corroboration only |
| Patch-notes source | LoL Wiki MediaWiki API `V26.19` (released 2026-09-23) |
| Fetcher | tools/fetch_page.py (direct + jina tier) + browser DOM read |

**To regenerate this axis next patch:** re-read the lolalytics jungle tier list
(Emerald+ and at least one more band, e.g. Diamond+ and Platinum+), re-pull u.gg
for a second stat source + the `26.x` label, and re-transcribe the LoL Wiki
`V26.x` patch page for jungle-relevant changes; **overwrite this file wholesale.
Never append — the snapshot must match one patch exactly.**

### Gaps / next-pull TODOs
- **[gap]** Only the **top-20** lolalytics rows were extractable (default view);
  the full jungle pool (#21+) and a true *bottom-of-tier* list were not captured
  → "weakest jungler" is [partial].
- **[gap]** u.gg per-champion rows are JS-rendered behind Cloudflare and were not
  extracted this run; per-champion **win/pick/ban is single-sourced (lolalytics)**.
- **[gap]** No Diamond+ / Platinum+ band captured this run to show rank-sensitivity.
- **[gap]** Patch notes transcribed from LoL Wiki (secondary). Riot's own
  leagueoflegends.com patch page returned HTTP 400 to this fetcher; consider the
  official page next run for a fully primary source.
