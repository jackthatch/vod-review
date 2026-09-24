# Axis 2 — Causal impact of jungle play on win rate

> Compiled from the first research run (2026-09-24); findings salvaged from
> sub-agent summary output. **This axis is the least complete of the three** —
> the numeric sources (stat sites) were all blocked, so it is mostly a
> *method/gap* record rather than an evidence base. Re-run with better access.

## What we could verify

Riot explicitly states that **gold difference was "the single best metric we had
at describing the overall game state at any particular time,"** but built the Win
Probability model because **gold difference alone ignores dragons, XP, and *who
holds* the gold** — i.e. raw gold under-describes the true win state, and
objectives/XP add real signal
[lolesports.com — Dev Diary: Win Probability Powered by AWS](https://lolesports.com/article/dev-diary-win-probability-powered-by-aws-at-worlds/blt0)
(accessed 2026-09-24, confidence: Medium, tier: Primary).
Notably, Riot flags **Win Probability Added (WPA)** — quantifying the win-value of
individual actions — as *future work*, which is precisely the metric this product
would want and which does not yet exist publicly.

> ⚠️ Caveats: the WP model is trained on **professional** play since patch 10.4,
> and Riot states WP "isn't meant to predict". So it is design/feature evidence,
> not a measured solo-queue correlation.

## What we could NOT verify (the gap)

**No sources found** (all blocked from this container) for the numeric claims that
matter most to this axis:

- first-blood / first-drake **win-rate correlation** percentages
- jungle **KP% vs CS/min** win correlation
- **deaths per 10 minutes** as a negative predictor
- **smite / objective-control** win deltas
- jungler **gold or XP lead** → win rate

Candidate sources to seed a re-run: op.gg / u.gg / lolalytics jungle stat pages,
leagueofgraphs "first blood / first dragon win rate" rankings, Riot balance blogs,
and one tier-A analyst breakdown.

> Conflicts noted: none surfaced.
> Gaps: essentially all numeric, as listed above.

## Why this matters for the coach

The product's core premise — that jungle decisions move win probability — is
**consistent with Riot's own model design** (objectives, XP, and gold *distribution*
are win-state features) but is **not yet backed by solo-queue numbers** from this
study. Until it is, the coach's confidence claims should be framed as
"expert-grounded," not "data-proven."
