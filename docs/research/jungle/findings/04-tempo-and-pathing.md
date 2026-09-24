# Axis 4 — Tempo & pathing theory

> **Status: fresh research 2026-09-24.** Live patch at time of writing:
> Riot display **26.19** / Data Dragon **16.19.1**. Every mechanical claim is
> tagged with source + date; patch-tunable facts are **dated and marked
> perishable**. Unsourced claims are tagged `confidence: Low`.
> Tooling: all fetches via `tools/fetch_page.py` (see `00-environment-constraints.md`).
>
> **Purpose of this axis.** Axes 1–3 establish *what* wins games and *which*
> objectives matter. This axis answers the mechanical question underneath them:
> **what is "tempo", how do you measure it, what makes one path better than
> another, how do you optimise the first clear, and how does tempo become win
> probability?** The dividing line throughout is **DURABLE theory** (true across
> patches, safe to coach in 2026 and 20.26) vs **PATCH-SPECIFIC routes**
> (numbers that expire on the next jungle tune).

---

## 0. Headline answers (TL;DR)

1. **Tempo has a hard, citable definition — and it is time, not speed.**
   The LoL Wiki defines it as *"the time advantage (in seconds) of one team or
   player reaching and successfully completing an objective first"*, explicitly
   tied to **respawn timers, item prices, recall timers, out-of-combat
   movement speed, and time-to-kill of minion waves and monsters**
   [LoL Wiki: Snowball §Qualities, accessed 2026-09-24]. *Confidence: High —
   primary wiki, definitional.*
2. **"Faster clear" ≠ "good tempo".** The strongest 2026 source on the topic is
   blunt: *"Fast pathing is meaningless if it only delivers you to the wrong
   side of the map earlier… A jungler with good tempo reaches the important
   decision before the game closes the option. A jungler with fake tempo arrives
   quickly to a dead play."* [RiftLab, "Jungle Tempo Review", updated
   2026-07-15, accessed 2026-09-24]. *Confidence: Medium–High (independent
   publisher, aligns with the wiki definition).*
3. **Tempo is a currency that expires.** *"Gold waits in your inventory; tempo
   evaporates the moment you stop spending it"* — a fast clearer who never
   converts windows into objectives/ganks "finishes the game with nothing"
   [disciplinedjungler.com/guides/jungle-tempo, accessed 2026-09-24].
   *Confidence: Medium (single editorial source; concept also supported by
   §2/§5 below).*
4. **The durable driver of first-clear strength is the camp-respawn cycle, not
   raw clear speed.** Camps respawn on fixed timers; a jungler who clears a
   cycle faster gets back to the *next* cycle sooner, and a jungler who *is
   ahead* clears faster still — a compounding loop the Wiki calls **camp
   recycling** [LoL Wiki: Jungling §Camp recycling, accessed 2026-09-24].
   *Confidence: High.*
5. **Hard, patch-dated clear data now exists.** Patch **26.19** measured full
   clear times from **3,366 ranked games**: fastest **Ivern 2:43**, then
   **Zyra 2:54, Udyr 2:55**; a large cluster clears in **2:56–2:59**, reaching
   **26–28 jungle CS at 4:00** [lolrecommender.com/jungle-clear-times, patch
   26.19, accessed 2026-09-24]. **Perishable** — re-measure every patch.
6. **The honest gap: there is no public, gold-controlled, tempo→win-probability
   number.** Riot has never published solo-queue win rate as a function of
   jungle tempo/clear lead (consistent with Axis 3's finding that Riot's only
   published after-objective win rates are First Blood and First Turret). Treat
   all "tempo wins X% of games" claims as **confidence: Low** unless a raw
   sample is shown. See §5 and §8.

---

## 1. What "tempo" IS — the durable definition

### 1.1 The primary definition

The LoL Wiki frames the whole game as *resource acquirement* + *map tempo*, and
defines tempo precisely as a **time advantage**:

> *"**Tempo** refers to the time advantage (in seconds) of one team or player
> reaching and successfully completing an objective first. Tempo is therefore
> very closely tied to respawn timers, item prices, recall timers for shopping
> and regeneration, out-of-combat movement speed, and time-to-kill of minion
> waves and monsters."*
> — [LoL Wiki: Snowball §Qualities, accessed 2026-09-24]

Three things this definition locks in, and they are **durable**:

- **Tempo is relative and temporal.** It is a *difference* in seconds between
  you and the opponent, not an absolute farm count.
- **Tempo is asymmetric information/option pressure.** Whoever reaches a
  decision first forces the other to *respond*.
- **Tempo has known mechanical levers** (the five listed): respawn timers, item
  prices, recall timing, out-of-combat MS, and TTK of minions/monsters. Every
  coaching heuristic in §2–§4 reduces to moving one of those five.

### 1.2 The coaching definition (independent, convergent)

Dignitas's jungle guide arrives at the same idea from the decision side:

> *"Tempo is key to the jungle role… By controlling the speed at which
> [decisions resolve], you are the primary X-factor for your team."*
> — [Dignitas, "Controlling Tempo: A Jungler's Guide", 2020-07-06, accessed
> 2026-09-24]

And the modern independent source states it as **"usable time"**:

> *"Tempo is usable time. Whenever you're free to act and your opponent isn't,
> you hold tempo, and everything a jungler does either earns it, spends it, or
> wastes it. Fast clears, clean resets, and skipped deaths earn it. Objectives,
> deep wards, and ganks convert it into permanent advantages; hovering converts
> it into nothing."*
> — [disciplinedjungler.com/guides/jungle-tempo, accessed 2026-09-24]

**Convergence note:** a wiki (encyclopaedic), a pro-org guide (2020), and a
2026 coaching site define tempo with the same three ingredients — *time
advantage*, *freedom to act first*, *conversion into a concrete advantage*.
That triple is the **durable core**. *Confidence: High* (three independent
sources agreeing on the concept; none patch-specific).

### 1.3 What tempo is NOT (durable anti-patterns)

- **Not raw clear speed.** See the RiftLab quote, §0.2.
- **Not farm/CS totals.** CS is a *proxy* for tempo earned, not tempo itself.
- **Not measured in gold.** Gold is *resource acquirement* (the other half of
  the Wiki's dichotomy). Gold is stored; tempo is spent.
- **Hovering is tempo spent for zero conversion** — the canonical waste
  [disciplinedjungler.com, 2026].

---

## 2. How tempo is MEASURED

Tempo itself is a latent quantity; in a VOD-review product you measure
**observable proxies** that each map to one of the five levers in §1.1.

### 2.1 Durable measurement framework (recommended for the platform)

| Proxy (what you can log) | Maps to lever | Why it indicates tempo | Durability |
| --- | --- | --- | --- |
| **Camp-respawn cycle timing** — time you clear camp N vs when it respawns | respawn timers | If clear-time ≤ respawn-ish window you stay "on cycle"; drift = lost tempo | Durable principle; *numbers* perishable |
| **Jungle CS at a fixed clock (e.g. 4:00, 7:00, 10:00)** | TTK of monsters | Direct output of clear efficiency at a comparable instant | Durable metric; thresholds perishable |
| **Recall/reset timing after a clear or fight** | recall timers, item prices | Reaching a spend-point and re-entering map earlier = tempo lead | Durable |
| **Time-to-first-objective** (first drake/grub/Herald contact) | respawn timers + MS | "First to complete an objective" is the literal Wiki definition | Durable; spawn times perishable |
| **Out-of-combat MS uptime / path straightness** | out-of-combat MS | Wandering between plays burns the very currency being banked | Durable |
| **Conversion events per tempo window** — did a window produce a kill/objective/ward/invade? | (conversion) | Separates *real* from *fake* tempo (§0.2) | Durable |

### 2.2 The "usable seconds" metric

The cleanest operationalisation available: **count seconds in which you can act
and the enemy jungler cannot.** The disciplined-jungler framing makes this the
unit of account — *"That window is the product every clean clear
manufactures"* [disciplinedjungler.com, accessed 2026-09-24]. *Confidence:
Medium* — the framing is well-reasoned and matches the wiki definition, but no
source publishes a tool that literally counts these seconds; the platform would
be building it.

### 2.3 What is NOT a valid measure

- **Absolute clear time in a vacuum** (see §4 — it only matters relative to the
  opponent and to what the extra seconds *buy*).
- **KDA / kills.** A kill is a *conversion*, not a measure of tempo.
- **Total gold at 15.** That is resource acquirement; a low-tempo jungler can
  still be wealthy if a lane fed them.

---

## 3. What separates STRONG from WEAK pathing

Pathing = the sequence and direction of camp clears, routed so that the jungler
ends up positioned for what matters. The Wiki states the durable basis:

> *"The structure of the map… naturally leads to that resource acquirement
> being done in desired **paths**, formally called **pathing**, as some camps
> are closer to each other and/or some camps may be prioritized over others…
> Because the jungler can only be situated close to one half of the map at a
> time, this pathing also determines which lanes or objectives are within their
> more immediate sphere of influence. **Minimizing the time and resources spent
> clearing camps is imperative** for a jungler to have priority over further
> camps, fights, other objectives, and general pressuring of the enemy team."*
> — [LoL Wiki: Jungling §Basis, accessed 2026-09-24]

### 3.1 The durable discriminator: **where the path ENDS, not how fast it runs**

The single most important modern insight, and it is **durable**:

> *"Good pathing should connect clear speed to what became available afterward:
> lane pressure, invade options, objective setup, or reset quality. A jungler
> with good tempo reaches the important decision before the game closes the
> option. A jungler with fake tempo arrives quickly to a dead play."*
> — [RiftLab, updated 2026-07-15, accessed 2026-09-24]

**Strong path = ends on a live option** (a gankable lane, a contestable
objective, or a safe reset). **Weak path = ends on a dead play** (a lane that
is ungankable, an objective the enemy already secured, or an over-extended
position). Speed is only a *multiplier* on top of that.

### 3.2 Strong vs weak — a durable checklist

| Dimension | Strong | Weak | Durability |
| --- | --- | --- | --- |
| **Endpoint** | Ends where a play is *live* (gank/objective/reset) | Ends in a dead zone | Durable |
| **Lane coupling** | Paths toward lanes that *gave* info — pushing lane for river contest, protecting collapse-risk weak-side | Ignores lane states; auto-pilots a memorised route | Durable (RiftLab 2026-07-15) |
| **Opponent tracking** | Reacts to enemy jungler's revealed position; paths to punish commitment | Farms into the enemy jungler's strength; no crossmap | Durable |
| **Cycle integrity** | Camps cleared in an order that re-synch with respawns (camp recycling) | Leaves scattered half-camps → permanently "off cycle" | Durable |
| **Objective alignment** | Is where the next objective spawns with a recall *before* it | Arrives late, no items, forced to contest weak | Durable (timing numbers perishable) |
| **Risk of reset** | Observes leash-range/patience, doesn't reset a camp | Resets camps, loses all tempo on that camp | Durable (mechanics) |

### 3.3 Two durable pathing failure modes

1. **Fake tempo** (a.k.a. "fast to the wrong place"): arrives early at a play the
   enemy doesn't care about, or that is already over [RiftLab 2026-07-15].
2. **Tempo that never converts**: banks windows then hovers/recalls without
   spending them; "potential that never converts is just time spent"
   [disciplinedjungler.com, 2026].
3. **Forcing a gank that costs you the cycle.** The 2026 BoostRoom pathing
   guide names *"the most common jungle trap: forcing a gank that costs you two
   camps and the entire game"*, and roots the whole problem in
   *"your route doesn't match the game state"* [BoostRoom, "Jungle Pathing
   2026", published 2026-04-12, accessed 2026-09-24]. This is the concrete form
   of "tempo spent for nothing" — a gank that doesn't convert burns camps you
   can never re-farm, permanently dropping you off the respawn cycle.
   *Confidence: Medium (single editorial source, but the mechanism follows
   directly from the durable camp-recycling loop in §1.1/§4).*

### 3.4 Two durable camp-respawn facts that constrain all routing

- **Respawn is per-camp and starts only after the camp is *fully* cleared.**
  *"After a camp has been completely cleared, it will remain empty for an amount
  of time specific to that camp… then all of the monsters will reappear."*
  [LoL Wiki: Monster §Camp respawn, accessed 2026-09-24]. → Leaving a camp
  half-cleared delays its own respawn *and* wastes time; every camp must be
  finished to enter the cycle. *Confidence: High.*
- **An accurate enemy respawn timer requires vision at the moment of clearing.**
  You cannot read the opponent's cycle without having seen the camp die
  [LoL Wiki: Monster, accessed 2026-09-24]. → Denying vision of your clear
  *is* a tempo play (the opponent can't path-deny what they can't time).
  *Confidence: High.*

---

## 4. First-clear optimisation

### 4.1 Durable principles

- **The first camp always hits level 2.** *"Clearing the first camp of the game
  will always level up the jungler to level 2"* (assuming no other XP source),
  so the opening choice is about *routing*, not about whether you hit L2
  [LoL Wiki: Jungling §Camp recycling, accessed 2026-09-24]. *Confidence: High.*
- **Some camps are skippable for level breakpoints.** Small monsters such as
  **Mini Krug** and **Lesser Raptors** have "exceptionally low" bounties and may
  not be needed to hit a breakpoint [LoL Wiki: Jungling, accessed 2026-09-24].
  → skipping them can *buy tempo* for the same level. This is the durable basis
  of every "skip smalls" first-clear trick. *Confidence: High.*
- **Leash is optional, not automatic.** *"Regardless, this strategy is not
  always optimal"* — a leash costs the laner tempo (they arrive to lane late),
  which the jungler must be able to repay [LoL Wiki: Jungling, accessed
  2026-09-24]. *Confidence: Medium–High.*
- **Optimise for the cycle, not the clear.** The point of a fast first clear is
  that *"a cycle for [the camps] to respawn and be cleared again sooner"* opens
  up [LoL Wiki: Jungling §Camp recycling, accessed 2026-09-24].
- **Do not reset camps.** Fighting outside **leash range** makes monsters lose
  patience, regen damage, and run home — losing the entire camp's tempo
  [LoL Wiki: Jungling §General combat, accessed 2026-09-24]. *Confidence: High.*
- **Kiting between autos** (moving away before the monster's wind-up lands,
  then retaliating) is a durable clear-time/HP optimisation; ranged champions
  do it more consistently [LoL Wiki: Jungling, accessed 2026-09-24].
  *Confidence: High.*

### 4.2 Patch-specific first-clear numbers (PERISHABLE — dated)

**Measurement standard.** Clear time = measured **full clear**; CS benchmark =
**jungle CS at 4:00**; sample = **3,366 ranked games** on patch **26.19**.
Source: [lolrecommender.com/jungle-clear-times, patch 26.19, accessed
2026-09-24].

| Rank | Champion | Full clear | Jungle CS @ 4:00 | Games measured |
| --- | --- | --- | --- | --- |
| 1 | **Ivern** | **2:43** | 26 | 27 (30d) |
| 2 | **Zyra** | **2:54** | 28 | 30 (30d) |
| 3 | **Udyr** | **2:55** | 28 | 157 (30d) |
| 4+ (cluster) | 9 champions | **2:56–2:59** | 28 | 13–183 each (30d) |

**Interpretation (durable reading of perishable data):** the *spread* between
the fastest clear (2:43) and the large mid-cluster (2:56–2:59) is only
**~13–16 seconds**. That is the size of the first-clear edge in patch 26.19 —
enough to reach a river/objective *first* (tempo), **not** enough to win a game
by itself. This directly supports §0.4/§3.1: the edge is only as good as the
play it's spent on. **Re-measure every patch**; champion identities and times
shift with jungle tuning.

> ⚠️ **Perishable.** Champion names, times, CS-at-4:00, and the 3,366-game
> sample are valid **only for patch 26.19 (2026-09-24)**. Treat as an example
> of how to benchmark, not a standing tier list.

### 4.3 Durable first-clear decision rule (patch-agnostic)

> *Clear in the direction of your **first win condition**, take every camp that
> the win condition's timing allows, skip smalls whose bounty you don't need
> for the breakpoint, and **arrive at the objective/lane with items already
> bought** (recall completed). If no win condition is reachable, path for
> **cycle integrity** and information, not for a dead play.*

---

## 5. How tempo converts into WIN PROBABILITY

### 5.1 The durable conversion chain

Tempo does not win games directly; it wins them through **conversion events**.
The causal chain (durable, supported across sources):

```
fast clean clear  →  tempo window (usable seconds)
                  →  a LIVE option (gank / invade / objective / reset)
                  →  a conversion (kill, camp stolen, objective, area control)
                  →  resource lead (gold/XP/buffs)
                  →  map control (vision, tempo again)   →  higher win prob.
```

The Wiki's **active snowballing** section is the canonical statement of the
resource side: *"Entire teams… may take an opportunity that arises from their
lead in tempo in order to gain a lead in resources through kills and
objectives. Tempo and resource leads can be accelerated by pressuring the enemy
team with even more kills and objectives, therefore creating a snowball."*
[LoL Wiki: Snowball §Active snowballing, accessed 2026-09-24]. *Confidence:
High* for the *mechanism*; **no win-rate number is attached by that source.**

Notably, the Wiki names the jungler's invade as a first-class snowball: *"The
jungler consistently taking away camps from the enemy counterpart during
invades, thus leaving them at a deficit"* [LoL Wiki: Snowball, accessed
2026-09-24]. Invading is thus a **tempo→resource conversion**, not just a map
action.

### 5.2 The honest state of the evidence (read before coaching this)

- **There is no published, gold-controlled number of the form "tempo lead of X
  seconds ⇒ +Y% win rate."** This is consistent with Axis 3, which found Riot's
  only published *after-objective* solo-queue win rates are First Blood and
  First Turret, and that no drake/grub/Herald/Baron win rates are published.
  *Confidence: High* (negative finding, cross-checked against Axis 3).
- **Any "tempo wins X%" figure you meet should be treated as `confidence: Low`**
  unless the poster shows sample size, rank band, patch, and gold-controlled
  baseline.
- **What IS defensible:** tempo→resource conversion is *mechanically* true
  (you cannot take an objective you arrived late to; you cannot gank a lane you
  are not near), and resource leads are directionally linked to win rate. The
  chain in §5.1 is a *mechanism argument*, not a measured elasticity.

### 5.3 Practical conversion rules (durable, coachable)

- **Every tempo window must be named.** If the review can't say which
  conversion event the window produced, the window was *wasted* (fake tempo).
- **Arrive with items.** A tempo lead spent before a recall is often weaker than
  a slightly later arrival with a completed item (item prices are an explicit
  tempo lever in §1.1).
- **Trade, don't always contest.** Since 2026 Riot has deliberately de-emphasised
  contesting every objective (Axis 3, [Riot 26.1 Notes, 2026-01-07]) — "concede
  and crossmap" is a *tempo conversion* (you convert your window into a
  different objective), not a tempo loss.

---

## 6. DURABLE vs PATCH-SPECIFIC — the split, in one table

| Claim | Verdict | Source | Date |
| --- | --- | --- | --- |
| Tempo = time advantage (seconds) to reach/complete an objective first | **DURABLE** | LoL Wiki: Snowball | accessed 2026-09-24 |
| Tempo's levers: respawn timers, item prices, recall timers, out-of-combat MS, TTK of minions/monsters | **DURABLE** | LoL Wiki: Snowball | accessed 2026-09-24 |
| Good pathing ends on a *live* option; speed is secondary | **DURABLE** | RiftLab | updated 2026-07-15 |
| Fast clear ≠ win (fake-tempo failure) | **DURABLE** | RiftLab; disciplinedjungler | 2026-07-15 / accessed 2026-09-24 |
| Tempo is a currency that expires if unconverted | **DURABLE** | disciplinedjungler | accessed 2026-09-24 |
| First camp always gives L2 | **DURABLE** | LoL Wiki: Jungling | accessed 2026-09-24 |
| Small monsters (Mini Krug/Lesser Raptor) skippable for breakpoints | **DURABLE (as principle)** | LoL Wiki: Jungling | accessed 2026-09-24 |
| Camp spacing / which camps are adjacent → optimal routes | **DURABLE (structure), numbers perishable** | LoL Wiki: Jungling | accessed 2026-09-24 |
| Skilled players see camp respawn info 60s (buff camps) / 10s (small camps) early | **PATCH-TUNABLE (mechanical)** | LoL Wiki: Jungling | accessed 2026-09-24 |
| Full clear times: Ivern 2:43, Zyra 2:54, Udyr 2:55; cluster 2:56–2:59; 26–28 CS @4:00 | **PATCH-SPECIFIC — 26.19 only** | lolrecommender (3,366 games) | 2026-09-24 |
| First-clear edge ≈ 13–16s (derived from the above spread) | **PATCH-SPECIFIC (derived)** | derived from 26.19 data | 2026-09-24 |
| Atakhan / Feats of Strength economy | **REMOVED 26.1 — do not coach** | Riot 26.1; Axis 3 | 2026-01-07 |

---

## 7. Patch-specific route theory — how to keep it fresh (PERISHABLE)

The following is **not durable** and must be regenerated each patch:

1. **Re-measure clear times** (lolrecommender / dpm.lol / u.gg) → update the
   §4.2 table. Any mid-cluster champion within ~2:55±3s can be treated as
   "fast enough" for the same tempo play.
2. **Re-check camp spawn/respawn constants** on the LoL Wiki `Jungling` page —
   these are periodically tuned and the coach must not hard-code them.
3. **Re-check objective spawn/despawn times** (Axis 3 owns the canonical table:
   grubs 8:00, Herald 15:00, Baron 20:00, drake 5:00, live patch 26.x).
4. **Re-verify what is live** — Atakhan/Feats/Blood Roses were removed in 26.1
   and must not appear in any pathing gameplan.

---

## 8. Gaps, confidence, and follow-ups

**High-confidence (durable, multi-source or primary):**
- Tempo = time advantage to objective-first + its five levers (§1.1).
- Pathing quality is endpoint-first, speed-second (§3.1).
- First camp → L2; skippable smalls; leash is optional; don't reset camps (§4.1).
- Clear-speed spread in 26.19 is small (~13–16s) (§4.2).

**Medium-confidence:**
- "Tempo is a currency that expires" / "usable seconds" as the unit of account
  (§2.2, §5.1) — single strong editorial source; convergent with the wiki
  definition but not independently measured.

**Low-confidence / gaps the study should flag:**
- **No paper or primary source quantifies tempo→win-rate elasticity.** This is
  the single biggest gap in the axis. If the platform wants it, it must be
  *measured in-house* (e.g., correlate "tempo windows converted" with win rate
  across the platform's VOD corpus).
- **No academic source was found** specifically modelling jungle pathing as an
  optimisation problem in this run (budget-limited; arXiv/OpenAlex not searched
  for this axis).
- **Champion-specific first-clear routes** (per-champion camp orders) were not
  enumerated — out of scope for theory axis; belongs to a champion-pool axis.
- **RiftLab's own methodology limits** are self-declared ("reviewed against the
  published methodology and source-data limits") — treat its qualitative claims
  as expert opinion, not measurement.

**Follow-ups recommended:**
1. Build an in-house "tempo-window conversion rate" metric from the VOD corpus
   (windows created vs windows converted) — this is the axis's missing number.
2. Snapshot §4.2 each patch into a dated appendix so the platform can show
   *how* the clear-time meta moves, turning perishable data into durable
   trend insight.

---

## Sources

| # | Source | Type | Date | Accessed |
| --- | --- | --- | --- | --- |
| 1 | LoL Wiki — **Snowball** (tempo definition; active snowballing) | Primary wiki | living page | 2026-09-24 |
| 2 | LoL Wiki — **Jungling** (pathing, camp recycling, leash, respawn timers, combat) | Primary wiki | living page | 2026-09-24 |
| 3 | LoL Wiki — **Terminology** (#Pathing) | Primary wiki | living page | 2026-09-24 |
| 4 | Dignitas — "Controlling Tempo: A Jungler's Guide" | Pro-org guide | 2020-07-06 | 2026-09-24 |
| 5 | disciplinedjungler.com — "What Is Jungle Tempo" | Independent coaching | undated | 2026-09-24 |
| 6 | RiftLab — "Jungle Tempo Review: Where Fast Clears Still Fail" | Independent analyst | updated 2026-07-15 | 2026-09-24 |
| 7 | lolrecommender.com — "LoL Jungle Clear Times" (3,366 ranked games) | Stat aggregator | patch 26.19 | 2026-09-24 |
| 8 | Riot Games — Patch **26.1** Notes (Atakhan/Feats removal context) | Riot primary | 2026-01-07 | (via Axis 3) |
| 9 | BoostRoom — "Jungle Pathing 2026: Clears, Timings & First Ganks" | Editorial guide | 2026-04-12 | 2026-09-24 |
| 10 | LoL Wiki — **Monster** (§Camp respawn mechanics) | Primary wiki | living page | 2026-09-24 |
