# ONE-SHOT RUN — knock out the whole jungle study in a single pass

**Trigger phrase:** `run the jungle study` (or "one-shot the jungle research").

This file is the canonical procedure. Follow it top to bottom; do not improvise
the batching or the sub-agent contract — both were tuned after run 1 failed.

---

## 0. Preconditions (verify, don't assume)

```bash
cd docs/research/jungle
python3 tools/fetch_page.py "https://lolalytics.com/lol/graves/build/?lane=jungle" --verbose 2>&1 | head -3
python3 tools/study_state.py status
python3 tools/study_state.py verify
```

- If the fetch comes back `blocked=True` on **every** tier, stop and re-read
  [`findings/00-environment-constraints.md`](findings/00-environment-constraints.md).
  Do **not** report "research is blocked" — test the tiers explicitly first.
- `status` tells you what is pending. `verify` flags provisional/missing/thin files.

## 1. The loop (this is the whole run)

```
while pending axes remain:
    batch = study_state.py next          # <= 3 axes (Hermes concurrency cap)
    delegate_task(tasks=[ one task per axis ])   # PARALLEL, one axis per sub-agent
    for each completed axis:
        if findings file missing/thin -> salvage the substance from the
                                         sub-agent summary and write the file
    study_state.py verify                # gate: every axis in the batch must pass
```

**12 axes ÷ 3 = 4 batches.** Run them sequentially (batch N+1 only after batch N
verifies). Do not try to launch all 12 at once — the concurrency cap will silently
drop them.

## 2. Sub-agent contract (copy this into each `delegate_task` task)

> **Goal:** Research the axis "<TITLE>" for a League of Legends jungle-role
> improvement platform. <AXIS GOAL STRING from `study_state.py goal <N>`>
>
> **Deliverable:** Write your findings to `<DELIVERABLE PATH>` (e.g.
> `docs/research/jungle/findings/04-tempo-and-pathing.md`). **Write the file
> early and update it as you go** — do not save all writing for the end.
>
> **Hard rules:**
> 1. **Cite every claim.** Prefix each with a source and date. Mark unsourced
>    claims `confidence: Low`.
> 2. **Fetch web pages only via** `docs/research/jungle/tools/fetch_page.py`
>    (`python3 fetch_page.py "<url>" --raw`). Plain `curl` is blocked from this
>    container. Prefer lolalytics, u.gg, op.gg, LoL Wiki (MediaWiki API), Riot
>    primary sources, arXiv/OpenAlex. Google is unusable — use Bing/DuckDuckGo.
> 3. **Date patch-dependent facts** and mark them perishable.
>    Atakhan + Feats of Strength were REMOVED in patch 26.1 — not live.
> 4. **Numbers beat prose.** If a measured value exists, give the number, the
>    sample size, the rank band and the patch. No invented statistics, ever.
> 5. **Budget your iterations.** Aim to have the file written within your first
>    ~60% of tool calls; refine after. A partial written file beats a perfect
>    unwritten one.
> 6. Finish with a short summary: what you found, confidence, and any gaps.
>
> **Toolsets:** `web`, `terminal`, `file`, `browser`, `search`.
> **Language:** English.

## 3. Verification gates (do not skip)

After each batch:

```bash
python3 tools/study_state.py verify     # must not mention this batch's axes
```

- File **missing** → salvage from the sub-agent's returned summary and write it.
- File **thin (<400 B)** → the agent ran out of budget; salvage or re-run that one axis.
- Findings that contradict an earlier axis → note it in both files; do not
  silently overwrite.

## 4. Synthesis (after all 12 axes pass)

1. Write the consolidated, cited narrative into [`jungle-study.md`](jungle-study.md):
   how games are won/lost, the jungle's causal role, the highest-leverage
   decisions, and what the coach should therefore flag.
2. Flag every finding the **coach** should consume (metrics, thresholds,
   "conceded vs contested" phrasing rules).
3. Update the axis checkboxes in [`README.md`](README.md) to ☑.
4. Commit and push: `git -C <repo> add -A docs/research/jungle && git commit && git push`.
5. Report to the user: axes completed, headline findings, biggest uncertainties.

## 5. Refresh mode (patch drift)

Axis 12 (meta snapshot) is perishable. To refresh only it:

```bash
python3 tools/study_state.py goal 12     # re-research just this axis
```

Re-run that axis, update findings/12, bump the "as of patch" date, recommit.

## Known failure modes (from run 1)

| Failure | Cause | Mitigation |
|---|---|---|
| Sub-agents return findings but write no file | iteration cap | contract rule 5; orchestrator salvages |
| "Research is blocked" | bare `curl` + datacenter IP | always use `fetch_page.py`; test tiers before concluding |
| Silent garbage | HTTP 200 + bot-wall page | fetcher detects by content; check `len(text)` |
| Missing numbers | stat sites unreachable | solved by fetch layer — lolalytics/u.gg/op.gg all work |
| Wasted budget on Google | Google CAPTCHAs all tiers | use Bing/DuckDuckGo |
