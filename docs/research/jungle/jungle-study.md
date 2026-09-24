# Jungle Study — findings log

> **Long-running study.** Each run appends to this document. Citations inline;
> confidence High / Medium / Low; source tiers Primary / Established / Low.
> Per-axis raw notes live in [`findings/`](findings/). Study design:
> [`README.md`](README.md). See [`findings/00-environment-constraints.md`](findings/00-environment-constraints.md)
> for the tooling limits that shape how runs must be executed.

---

## Run log

| Run | Date | Axes covered | Status |
| --- | --- | --- | --- |
| 1 | 2026-09-24 | 1 (how games are decided), 2 (jungle impact on win rate), 3 (objective value) | partial — findings filed, numeric stat-site data blocked |

---

## Run 1 — Key findings

**1. Early leads are only *weakly* predictive of the final result.** Riot's own
Win-Probability model is trained on far more than gold — gold *share*, team XP,
objectives, and timers — because gold difference alone "under-describes" the win
state [lolesports Dev Diary](https://lolesports.com/article/dev-diary-win-probability-powered-by-aws-at-worlds/blt0)
(Primary). Academic work finds only **~81.6%** accuracy *late* and roughly
coin-flip discrimination early [arXiv 2309.02449](https://arxiv.org/abs/2309.02449)
(Primary). *Implication:* the coach should not frame a loss as "the first death
decided it."

**2. Objectives are win-state features, and Riot treats Soul ≈ Baron.** Riot's WP
model includes dragon kills (incl. soul), Herald, Baron and Elder timers, and
patch 26.1 states *"Claiming Dragon Soul is just as impactful as taking Baron
Nashor"* [Riot Patch 26.1](https://www.leagueoflegends.com/en-us/news/game-updates/patch-26-1-notes/)
(Primary). But this is **design intent, not a measured win-rate equivalence**.

**3. The 2026 direction de-emphasises teamfighting over objectives.** Atakhan +
Feats of Strength + Blood Roses were **removed in patch 26.1 (2026)** specifically
because they made the game "extremely objective-focused"; Riot wants more
splitting/sieging, and restored first-blood/first-turret gold
[Riot 2026 Season One preview](https://www.leagueoflegends.com/en-us/news/dev/dev-2026-season-one-gameplay-preview/)
(Primary). *Implication:* the "concede and trade" principle in VISION now has a
Riot-stated design rationale.

**4. Riot publishes occasional objective win-rate numbers.** The Season 1 landing
post gave First Blood **57.6% → 55.4%** and First Turret **70.4% → 70.3%** win
rate after claiming [Riot /dev](https://www.leagueoflegends.com/en-us/news/dev/dev-how-the-season-1-changes-landed/)
(Primary). These are the only *solo-queue-ish* win-rate-after-objective figures
found so far.

**5. The study has a large, honest evidence gap.** No solo-queue numeric win rates
were obtainable for drakes/grubs/Herald/Baron, nor for jungle KP%/CS-min/
deaths-per-10 correlations — every stat site blocked automated access from this
container (`findings/00-environment-constraints.md`).

## Run 1 — Gaps & next actions

- **Access:** establish a way to read stat sites (op.gg/u.gg/lolalytics/
  leagueofgraphs) — via a proxy, the VPS, or any official API. This unblocks
  *most* of axes 2 and 3.
- **Re-run deeper:** axes 1–3 were iteration-capped mid-research; a focused,
  source-seeded re-run would complete them.
- **Next axes** (see backlog): 4 (tempo/pathing), 5 (gank EV), 6 (vision/wards),
  8 (archetype win-rate drivers).

## Caveats on this run

Findings were compiled by the coordinator from sub-agent outputs **after the
sub-agents hit their iteration caps without writing files** — so treat them as
**provisional** until re-verified. All Riot-sourced mechanics should be re-checked
against the live patch before being relied upon.
