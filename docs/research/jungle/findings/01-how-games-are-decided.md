# Axis 1 — How games are actually decided in solo queue

> Compiled from the first research run (2026-09-24). Sub-agent findings salvaged
> from summary output; **not yet independently verified by the coordinator.**
> Note the environment constraint: aggregate solo-queue stat sites were blocked,
> so the strongest numbers here are academic, and they skew **pro play**.

## The evidence says early leads are *weakly* predictive of the final result

Riot's own public **Win Probability** tool is an xgboost model over game time,
**gold %** (a player's share of total gold), total team XP, players alive, tower
kills, **dragon kills including whether a team holds soul**, Herald, and
Baron/Elder timers, trained on **professional** games since **patch 10.4**
[esports.net / Riot JPham](https://www.esports.net/news/lol/riot-games-explains-win-probability-for-lol-worlds-2023/) (accessed 2026-09-24, confidence: Medium, tier: Established).

Independent academic work on real-time prediction reports only **~81.6% accuracy
at 60–80% elapsed game time, with roughly coin-flip discrimination early** —
i.e. early state is a poor predictor of the eventual winner
[arXiv 2309.02449](https://arxiv.org/abs/2309.02449) (confidence: Medium, tier: Primary).

There is a genuine **conflict** in the literature: a DotA 2 professional model
claimed **85% accuracy after just 5 minutes**
[IEEE ToG 2019](https://doi.org/10.1109/tg.2019.2948469) (confidence: Medium, tier: Primary),
which is far more early-decisive than the LoL figures. The two are different games
and different epochs, but the discrepancy is unresolved.

## Snowball vs comeback is a *designed* equilibrium, not one-sided

Peer-reviewed work treats snowballing and comebacks as a designed balance rather
than a runaway process [IEEE TVCG 2016](https://doi.org/10.1109/tvcg.2016.2598415)
(confidence: Medium, tier: Primary), and comeback behaviour via the **bounty
system** has been modelled directly [Electronics 2025](https://doi.org/10.3390/electronics14071445)
(confidence: Medium, tier: Primary).

## Beware inflated accuracy claims

Several ML papers report suspiciously high **95–97%** win-prediction accuracy
[Acta Infologica 2024](https://doi.org/10.26650/acin.1180583),
[Applied Sciences 2025](https://doi.org/10.3390/app15105241) (confidence: Low, tier: Primary).
These likely include late/end-game state as features (leakage), and should **not**
be taken as evidence that games are decided early.

> Conflicts noted: DotA 2 "85% after 5 min" (IEEE ToG 2019) vs LoL "~50% early /
> 81.6% late" (arXiv 2309.02449) — unreconciled.
> Gaps: **No sources found** for a solo-queue-specific "X gold at 15 min → Y%
> win rate" curve. op.gg/u.gg/lolalytics/leagueofgraphs all 403'd. Most
> win-prediction literature is pro-play or DotA 2, not LoL solo queue.

## Why this matters for the coach

If early leads are only weakly predictive, the product should **not** frame a
review around "you lost the game at the first death." It should weight *repeatable
structural decisions* (objective control, tempo, not throwing leads) rather than
assuming the first snowball decided everything. **This is a hypothesis to keep
testing** — the solo-queue curve is still unmeasured.
