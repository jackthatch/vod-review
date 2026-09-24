# Jungle Research Study — how games are won and lost

A **long-running research program** to build an evidence base on how League of
Legends games are actually won and lost, focused on the **jungle role**. This is
the input that will eventually steer the AI coach: what to look for, what
correlates with winning, and which decisions matter most.

- **Method:** the `deep-research` skill (parallel fan-out, multi-source
  validation, confidence tracking, cited reports).
- **Output:** cited findings appended to [`jungle-study.md`](jungle-study.md);
  per-axis raw notes in [`findings/`](findings/).
- **Cadence:** on demand — one axis (or a small batch) per research run, appended.
  See **[`ONE-SHOT-RUN.md`](ONE-SHOT-RUN.md)** to knock out the whole study in a
  single pass.
- **Source discipline:** every claim cited; critical claims need 2+ independent
  sources or `confidence: Low`. Patch-specific facts must be dated.

## Why this exists

`docs/jungle-playbook.md` captures **durable domain knowledge** (archetypes,
frameworks, leaks). This study goes further: it **sources and validates** the
claims — does high CS/min actually correlate with jungle win rate? How much does
first-drake control matter? Where do rank-tier leaks concentrate? — so the coach
is grounded in evidence, not just expertise.

## Axis backlog

Status: ☐ planned · ◐ in progress · ☑ done (notes filed)

**All 12 axes complete as of Run 2 (2026-09-24).** Axis 12 is perishable — re-run
it each patch (`study_state.py goal 12`).

### Win/loss mechanics
- ☑ 1. How games are actually decided in solo queue (win conditions; snowball vs
      coin-flip; the relative weight of early vs late game). → [`findings/01`](findings/01-how-games-are-decided.md)
- ☑ 2. Causal impact of jungle play on win rate (what jungle behaviours
      correlate most with winning — data from stat sites/analysts). → [`findings/02`](findings/02-jungle-impact-on-winrate.md)
- ☑ 3. Objective value: drakes (incl. soul), Voidgrubs, Herald, Baron — measured
      win-rate impact and correct prioritisation. → [`findings/03`](findings/03-objective-value.md)

### Jungle macro
- ☑ 4. Tempo & pathing theory (advanced clear/route theory; tempo as win driver). → [`findings/04`](findings/04-tempo-and-pathing.md)
- ☑ 5. Gank theory: when ganks convert, which lanes, expected value. → [`findings/05`](findings/05-gank-theory.md)
- ☑ 6. Vision & information advantage in the jungle; ward economy. → [`findings/06`](findings/06-vision-and-information.md)
- ☑ 7. Counter-jungling, invades, and vertical jungling — risk/reward. → [`findings/07`](findings/07-counterjungling-invades.md)

### Archetype & champion
- ☑ 8. Win-rate drivers per jungle archetype (carry vs gank vs tank) — what
      separates good from great players on each. → [`findings/08`](findings/08-archetype-winrate-drivers.md)
- ☑ 9. Champion-pool effects on win rate; one-trick vs flexible pools. → [`findings/09`](findings/09-champion-pool-effects.md)

### Improvement & review
- ☑ 10. What actually improves solo-queue players fastest (review methods,
      coaching evidence, deliberate practice). → [`findings/10`](findings/10-how-players-improve.md)
- ☑ 11. Rank-tier leak distribution — which mistakes concentrate at which ranks. → [`findings/11`](findings/11-rank-leak-distribution.md)

### Meta & data
- ☑ 12. Current jungle meta snapshot (dated): top champions, tier lists, and
      what the data says. **PERISHABLE — re-verify per patch.** → [`findings/12`](findings/12-meta-snapshot.md)

**Synthesis:** consolidated findings and the coach-design implications live in
[`jungle-study.md`](jungle-study.md) §Run 2.

## Tools

- **`tools/fetch_page.py`** — 3-tier resilient fetcher (direct → r.jina.ai →
  Playwright). **Use this for every web fetch in this study.** Plain `curl`
  fails from this container; see
  [`findings/00-environment-constraints.md`](findings/00-environment-constraints.md)
  for the full access matrix (what works, what doesn't, and why).

```bash
python3 tools/fetch_page.py "<url>" --verbose     # inspect
```

## Method notes

- Run via the `deep-research` skill: scope → parallel axes → synthesis →
  cited report.
- Hermes fans out at most 3 sub-agents at once — batch larger sets.
- **Date every patch-dependent finding.** The meta drifts; mark freshness.
- Prefer primary data (Riot/official stats, op.gg/u.gg/lolalytics aggregates,
  Riot dev communications) over opinion pieces; flag analyst opinion as such.
- **Fetch through `tools/fetch_page.py`, never bare `curl`** — and check
  `len(text)`; a small "success" on a stats page is usually a JS shell or a
  bot-wall page served with HTTP 200.

## Relation to the product

`VISION.md` (mission) → `docs/jungle-playbook.md` (durable knowledge) →
**this study** (validated evidence) → **the coach's prompts & metrics**.
