# Axis 7 — Counter-jungling, invades, and vertical jungling

> **Status: Run-2 research (2026-09-24).** Every mechanical claim is verified
> against primary sources where possible; every statistic carries **number +
> sample size (where known) + rank band (where known) + patch + source + date**.
> Claims that are *analyst/game-theory consensus* rather than *measured* are
> explicitly labelled **[CONSENSUS]**. Claims with no citable source are labelled
> `confidence: Low`.
> Tooling: all fetches via `tools/fetch_page.py` (see `00-environment-constraints.md`).
> Patch context: **Atakhan + Feats of Strength were REMOVED in patch 26.1** — not live.

---

## 0. Headline answers (TL;DR)

1. **There is no public, measured "invade win rate" dataset.** We searched the
   major stat aggregators (lolalytics, u.gg, op.gg, leagueofgraphs) and the
   academic literature (OpenAlex). No site publishes an "invades attempted →
   invades converted / win rate" statistic at any rank band, the same way no
   site publishes gank conversion (see Axis 5). **Every specific invade-success
   percentage you read online is unmeasured.** This is the most important
   finding of Axis 7.
2. **What is measured is the *value of a camp*** — the atomic unit of a
   counter-jungle — and the mechanics that govern whether it can be safely
   taken. First-clear camps carry roughly **80–90 gold and 95–120 XP for the
   large monster** (Blue/Red = 90g/95xp; Gromp = 80g/120xp) [LoL Wiki: monster
   pages, accessed 2026-09-24]. A stolen camp therefore denies both gold *and*
   tempo (respawn timers), not just gold.
3. **Riot has repeatedly *nerfed* counter-jungling as a strategy**, which is
   strong indirect evidence that unfettered counter-jungling is high-impact:
   a penalty for attacking monsters on the enemy half of the map was added in
   Preseason 2023 (V12.22) and removed in V13.5 after being "deemed excessive";
   small monsters now die automatically when the large one is killed, which the
   wiki notes "alleviates counter-jungling" [LoL Wiki: Jungling §History,
   accessed 2026-09-24].
4. **Invading converts on the same preconditions as ganking: information +
   priority + duel power + escape.** The analyst consensus (and the wiki) is
   that invading is gated on **knowing where the enemy jungler is** and on
   **lane priority on the side you enter** — not on a generic "invasions are
   good" heuristic [LoLGuide: Counter-Jungling Guide; LoL Wiki: Jungling]. **[CONSENSUS]**
5. **The dominant failure mode is the collapse.** Because both invading and
   counter-jungling "can become an explosive cause for fighting, as laners come
   to… assist the jungler in a skirmish to try to ambush them," an unscouted
   invade risks losing the 1v2/2v2 *plus* the camps you came for *plus* the
   tempo to reach your own respawning camps [LoL Wiki: Jungling §Invading]. **[CONSENSUS]**
6. **Vertical jungling is the lowest-variance form of the play.** When each
   jungler takes the opposite side of the map, both lose roughly equal value and
   neither has to contest a 1v1 for it — it is a *tempo-neutralizing* answer to
   being invaded, not a winning play [LoL Wiki: Terminology §Vertical Jungling;
   LoLGuide]. **[CONSENSUS]**

---

## 1. Definitions (primary source)

All three terms are defined by Riot's official wiki. These definitions matter for
measurement because they draw the line between *information-gathering* invades
(cheap, common, low-risk) and *camp-stealing* counter-jungles (the play with the
real gold/tempo swing).

**Invading** — *"the act of walking into the enemy half of the jungle with the
intent of gaining information, and if done by a jungler, potentially stealing
away camps. Invading can severely impact the ability of the enemy jungler to
cycle their own camp, and the ally team can utilize the information gained from
invading for various decisions and strategies themselves."*
[LoL Wiki: Jungling §Invading, page id 7920, wikitext accessed 2026-09-24]

**Counter-jungling** — *"the act of invading with the express intent of stealing
away camps to cover a known deficit."* The wiki's canonical example: if the enemy
jungler cleared your Raptors, you clear one of theirs to *equalize*. This framing
is important — the wiki defines counter-jungling as a **compensating play**
against a known loss, not as a proactive snowball tool.
[LoL Wiki: Jungling §Invading]

**Vertical jungling** — *"A style of jungling mainly seen in higher elo and
competitive play where the de facto jungle border between both teams' jungles is
the middle lane rather than the river. Instead of the red side owning the first &
second quadrants with the blue side owning the third & fourth, one team will own
the first & fourth quadrants as well as the southeast (Drake) river, and the
other will own the second & third quadrants plus the northwest (Baron) river."*
[LoL Wiki: Terminology §Vertical Jungling (page id 52954), accessed 2026-09-24]

**Terminology (colloquial)** — *"Invade" = to go into the enemy's territory,
particularly their jungle; "Counter jungle" = to slay the neutral creeps in the
enemy's side of the jungle, depriving the enemy team of buffs, gold and
experience.* [LoL Wiki: Terminology §I/§C, accessed 2026-09-24]

Note the wiki explicitly attributes vertical jungling to **high-elo and
competitive play** — a signal that it is a *coordination-dependent* pattern, not
a default solo-queue opening.

`confidence: High` (primary/authoritative wiki definitions, verbatim this run).

---

## 2. Is there measured data on invade / counter-jungle win rate?

**Short answer: no, not in public aggregators, and not in the literature.**

- **Stat aggregators.** Searches of DuckDuckGo for "counter jungling win rate"
  and "jungle invade success rate data" return **champion tier lists and
  counter-pick tools** (u.gg jungle tier list, counterstats.net), not an
  invade-statistic page. lolalytics/u.gg/op.gg surface per-champion win rates,
  CS/min, gold, objectives — none expose "invades attempted/converted". The
  metric does not exist in the free public tier lists we can reach
  [DDG lite, searched 2026-09-24].
- **Academic literature.** OpenAlex search `jungle invade League of Legends`
  returns **603 works**, but the top hits are esports-culture, winner-prediction
  and gender-studies papers (e.g. *"Machine Learning Models on MOBA Gaming:
  League of Legends Winner Prediction," 2023, cited 7×*) — **none models invade
  or counter-jungle behaviour**. There is no peer-reviewed dataset of invade
  outcomes [OpenAlex API, searched 2026-09-24].
- **Riot does not publish it either.** Riot's public win-probability / stat
  surfaces are built on gold, XP, objectives and timers — not on invade counts or
  camp-steal events (see Axis 5 for the same point about ganks).

> **Consequence for the coach:** any "invades win X% of the time" claim must be
> treated as **analyst folklore** unless a sample size is shown. Do not display
> fabricated invade statistics. The measurable quantities are the *downstream*
> ones: **enemy jungle CS denied, gold/XP differential vs the enemy jungler, and
> tempo (camp respawn timing)** — see §7.

`confidence: High` (negative result, reproduced across two independent search
surfaces — aggregators + academic index; searched 2026-09-24).

---

## 3. The risk/reward model: what a camp steal is actually worth

A counter-jungle is best modelled as a **trade of variance for value**. The
value side is concrete and measurable; the risk side is a probability of losing a
much larger amount.

### 3.1 Value side (measured — camp bounties)

Per-camp gold/XP for the **large monster** (the killer receives full bounty):

| Camp | Gold | XP (large) | Respawn after clear |
|---|---|---|---|
| Blue Sentinel | **90g** | 95 xp | 5:00 |
| Red Brambleback | **90g** | 95 xp | 5:00 |
| Gromp | **80g** | 120 xp | 2:15 |
| Crimson Raptor (large) | **35g** | 20 xp | 2:15 |

Sources: [LoL Wiki: Blue Sentinel / Red Brambleback / Gromp / Raptor camp monster
pages, infobox + patch history, accessed 2026-09-24]. Blue/Red gold was raised to 90g
from 80g in **V13.5**; Gromp to 80g from 70g in V13.5. XP values current as of
the V14.10 monster-XP rework listing. **These numbers are patch-perishable** —
re-verify each patch.

Small monsters in the camp add further gold/XP, so a full camp steal is worth
more than the above table alone. **Caveat:** a jungler with a jungle companion
item (Gustwalker/Mosstomper/Scorchclaw) gets **bonus XP from large monsters,
greatly increased for the first large monster kill of the game** — so denying the
enemy their *first* large camp denies disproportionately more XP than a raw
bounty table implies [LoL Wiki: Monster §Rewards, accessed 2026-09-24].

**Analyst estimate of per-camp value:** *"denies 50–100 gold per camp… Done
correctly, you can be 2 levels ahead of the enemy jungler by 15 minutes."*
[LoLGuide: Counter-Jungling Guide, accessed 2026-09-24]. The 50–100g band is
**not a measured statistic** — it is analyst guidance with no sample size.
**The "2 levels ahead by 15 min" claim is unmeasured** → `confidence: Low`.

### 3.2 Risk side (the costs that make the EV negative when unscouted)

Counter-stacking against the value:
- **Death / collapse.** Losing the invade can cost your life *and* the camps, and
  spawn a lane collapse. Both invading and counter-jungling are named by the wiki
  as "an explosive cause for fighting" [LoL Wiki: Jungling §Invading]. **[CONSENSUS]**
- **Tempo loss.** Dying on an invade means you cannot reach your own respawning
  camps on time; the wiki frames invading as a threat to "the ability of the
  enemy jungler to **cycle their own camp**" — the same damage applies to you if
  the invade fails. Camp respawn timers (Blue/Red 5:00, small camps ~2:15) mean a
  failed invade can cost *two* camp cycles, not one [LoL Wiki: Jungling /
  monster pages].
- **Give-away / gift camps.** Because the game auto-kills the remaining lesser
  monsters 10s after the large monster dies, and the camp timer only starts when
  **all** monsters are dead, an invader who leaves one small monster alive
  *denies the camp from respawning* — a tactic analysts recommend *against the
  enemy*, and one that can be used against you [LoL Wiki: Monster §Camp respawn;
  LoLGuide]. **[CONSENSUS]**

### 3.3 The asymmetry

The EV of a counter-jungle is roughly:

```
EV ≈ P(enemy elsewhere) × (+camp value)
   − P(detected & collapsed) × (death + lost tempo + camps + lane cost)
```

Because the collapse term includes a death *and* multi-camp tempo loss *and*
potentially a lane swing, a single missed read can wipe out several successful
invades' worth of value. This is why the analyst rule is **"if any of the four
conditions [below] is missing, do not invade."** [LoLGuide]. **[CONSENSUS]**

`confidence: Medium` for the structure (the camp bounties are primary; the
probability terms are unmeasured).

---

## 4. Conditions under which invading pays off

The most consistently cited analyst checklist (LoLGuide: Counter-Jungling Guide,
accessed 2026-09-24) requires **all four** of:

1. **Lane priority** — your laners can rotate first if a fight starts.
2. **Vision control** — you know where the enemy jungler is.
3. **Duel power** — you win the 1v1 if you're caught in the jungle.
4. **Escape routes** — you can leave if the collapse comes.

**The "golden rule": never counter-jungle on the same side the enemy jungler is
on.** See them top → take their bot side; see them bot → take their top side.
[LoLGuide]. **[CONSENSUS]**

Concrete windows analysts recommend:
- **Enemy shows on the opposite side** (e.g. ganks top at 3:30 → take their bot
  side; "you have at least 30 seconds before they can get to you") [LoLGuide].
- **After a won scuttle fight** — "both junglers are low and have used
  summoners"; the loser "cannot contest because they are low HP or dead"
  [LoLGuide].
- **When you have pushed mid/sidelanes** and can rotate with the jungler
  [LoLGuide].

**Camph priority order (analyst):** buffs > big monsters (Gromp/Wolves/Raptors) >
Krugs. Taking Red/Blue denies both the buff *and* the large-monster XP
[LoLGuide]. **[CONSENSUS]**

**Mechanical support for the "information first" framing (primary):** the wiki
defines invading primarily as an **information** play, and camp-respawn rules make
*information* mechanically valuable: if a camp is cleared **outside of vision**,
"it is not possible to know that an enemy has recently been at that location,"
and a generic cached-accurate timer only appears 60s (buffs) / 10s (small camps)
before respawn [LoL Wiki: Jungling §Respawning timers; Monster §Camp level]. That
means a *scouted* steal hands the enemy an accurate respawn timer, while a
*stealth* steal does not — a real asymmetry in the reward structure.
`confidence: High` (mechanics), `confidence: Medium` (tactical conditions are
analyst consensus).

---

## 5. Failure modes

1. **Getting collapsed on.** The #1 listed risk. Laners "come to scare or fend
   off the invaders on their own or assist the jungler in a skirmish to try to
   ambush them" [LoL Wiki: Jungling §Invading]. Analyst framing: *"If you are
   alone and caught, you die."* [LoLGuide]. **[CONSENSUS]**
2. **Losing tempo / failing to cycle your own camps.** A failed (or even a slow
   successful) invade delays your own clear; the enemy jungler who is farming
   their own camps gains a tempo advantage. Reddit r/Jungle_Mains threads
   describe exactly this pattern — being invaded, losing tempo, and missing gank
   windows [r/Jungle_Mains, e.g. "Keep getting invaded and laners lose lane,"
   viewed via DDG snippet 2026-09-24 — **community opinion, not data**].
   `confidence: Low` (community anecdote).
3. **Giving up camps / "gift" camps.** If you invade and the enemy jungler simply
   takes your camps on the other side (a *vertical* swap), you have traded even
   value — you gain nothing unless your camp was worth more or you gained
   information/tempo from it. Overstaying converts a winning trade into a loss.
4. **The tilted-jungler rebound.** Analysts note a counter-jungled jungler
   "will often force desperate ganks to catch up" — sometimes this *succeeds* and
   converts into a lane kill, partially offsetting the steal [LoLGuide].
   **[CONSENSUS, unmeasured]**
5. **Level-1/invade-for-invade risk.** Level-1 five-man invades are popular in
   solo queue but the community framing (r/Jungle_Mains "Why is everyone obsessed
   with Lv 1 invades") suggests returns are inconsistent; no measured data found
   [community, 2026-09-24]. `confidence: Low`.

**Rule of thumb (analyst):** *take 2–3 camps max and leave* — "2 stolen camps +
escape > 4 stolen camps + death" [LoLGuide]. **[CONSENSUS]**

---

## 6. Vertical jungling (the low-variance branch)

Vertical jungling is when the two junglers take opposite sides of the map rather
than contesting one side [LoL Wiki: Terminology §Vertical Jungling].

- **Mechanically it is a tempo-neutralizing trade, not a winning play.** Analyst
  framing (LoLGuide): *"When the enemy jungler invades your top side jungle, you
  do not run across the map to contest. Instead, you walk into their bottom side
  jungle and take their camps. You both lose the same value, but you are safe."*
  **[CONSENSUS]**
- **It is the standard *answer* to being invaded** — the wiki's own definition of
  counter-jungling is framed as equalizing a known deficit by stealing the
  mirror-side camp [LoL Wiki: Jungling §Invading].
- **Resets at scuttle**, after which both junglers return to their own sides;
  the information gained from the enemy's pathing is then used to predict their
  next rotation [LoLGuide]. **[CONSENSUS]**
- **Attribution to high elo / competitive** is itself evidence it is a
  coordination-dependent pattern that relies on all four lanes reading the map
  the same way [LoL Wiki: Terminology].

`confidence: Medium` (definition is primary; the "safest form" characterisation
is analyst consensus).

---

## 7. Mechanical / design history relevant to counter-jungling

Riot's design history is the best *indirect* evidence about counter-jungling's
power, because Riot repeatedly nerfed it:

- **Preseason 2023 (V12.22):** alongside small monsters dying automatically
  ("which alleviates counter-jungling"), Riot shipped **"an additional penalty
  for junglers who attack monsters on the enemy half of the map… meant to be
  another step in alleviating counter-jungling."** It was **removed in V13.5**
  after being "deemed excessive." [LoL Wiki: Jungling §History, accessed
  2026-09-24]. This is direct Riot action against counter-jungling as a
  dominant strategy — and a reversal when it over-corrected.
- **V13.5:** Blue and Red bounty raised to 90g (from 80g); Gromp to 80g (from
  70g). Larger camp bounties raise the *reward* side of a successful steal
  [LoL Wiki: monster pages].
- **V14.10:** monster XP schedule reworked [LoL Wiki: monster pages].
- **V25.17:** native **respawn timers for all non-epic, non-buff camps** added to
  the client — giving every player better tempo information for counter-jungle
  tracking [LoL Wiki: Jungling §History].
- **Patch 25.09 (2025):** jungle is **auto-assigned Smite and only one Smite is
  allowed per team** [Riot: Patch 25.09 Notes, official news post, verified
  2026-09-24]. This constrains smite-fight outcomes around buffs/objectives —
  relevant to invade/swapling contest math.
- **V26.01 (2026):** Gromp initial spawn reduced to 1:07 from 1:42
  [LoL Wiki: Gromp page]. Camp-spawn timing changes reshape level-1 invade and
  first-clear pathing; **perishable**.

`confidence: High` for the patch-history facts (primary wiki + Riot notes);
`confidence: Low` for any inference that these changes *prove* a specific win-rate
impact — Riot did not publish measurement.

---

## 8. What the coach should flag (metric implications)

Given the absence of a measured invade stat, the coach should track the
**downstream, measurable** proxies rather than a nonexistent "invade win rate":

| Signal | What it means | Data availability |
|---|---|---|
| Enemy-jungle CS stolen / CS denied to enemy jungler | Direct value of counter-jungling | Inferable from CS-vs-enemy-jungler diff |
| Gold/XP differential vs enemy jungler @10 / @15 | The real payoff of a steal (or the cost of a failed one) | lolalytics/u.gg per-champion stats |
| Death-on-invade + subsequent camp-timer miss | The "collapse" failure mode | Match timeline events |
| Camp respawn timing vs your arrival | Tempo discipline after an invade | Timeline + respawn constants (Blue/Red 5:00, small ~2:15) |
| Lane priority on the invaded side at the time of entry | Precondition check for "should you have invaded" | Wave state at invade timestamp |

**Phrasing rule for the coach:** never say "your invade failed" — say *"you
invaded with [no priority / no vision / no duel advantage] and were collapsed
on, costing you [N] camps of tempo."* The precondition checklist (§4) is the
reviewable artefact, not a success percentage.

---

## 9. Source list

| # | Source | Type | Date accessed | Confidence |
|---|---|---|---|---|
| 1 | LoL Wiki (wiki.leagueoflegends.com) — *Jungling*, page id 7920 (wikitext via MediaWiki API) | Primary/authoritative | 2026-09-24 | High |
| 2 | LoL Wiki — *Terminology*, page id 52954 (Vertical Jungling, Invade, Counter jungle) | Primary/authoritative | 2026-09-24 | High |
| 3 | LoL Wiki — *Monster* (rewards, camp respawn, camp level) | Primary/authoritative | 2026-09-24 | High |
| 4 | LoL Wiki — *Blue Sentinel*, *Red Brambleback*, *Gromp* monster pages (bounty/XP/respawn) | Primary/authoritative | 2026-09-24 | High |
| 5 | Riot Games — *Patch 25.09 Notes* (leagueoflegends.com) | Primary (Riot) | 2026-09-24 | High |
| 6 | LoLGuide (lol.jycsd.com) — *Counter-Jungling Guide* | Analyst/third-party | 2026-09-24 | Medium (opinion, no sample sizes) |
| 7 | OpenAlex API — search `jungle invade League of Legends` (603 works, none on invade outcomes) | Academic index | 2026-09-24 | High (negative result) |
| 8 | DuckDuckGo lite — searches for invade/counter-jungle win-rate stats | Search surface | 2026-09-24 | High (negative result) |
| 9 | r/Jungle_Mains threads (tempo/invade anecdotes, via DDG snippets; direct reddit fetch blocked 403) | Community opinion | 2026-09-24 | Low |
| 10 | Semantic Scholar API — search `jungle pathing League of Legends` | Academic index | 2026-09-24 | Low (rate-limited / no relevant hits) |

### Research-access notes (transparency)

- **reddit.com direct fetch → HTTP 403** ("blocked by network security"); we only
  saw Reddit content via DuckDuckGo result snippets. Community claims are
  therefore cited at snippet fidelity only → `confidence: Low`.
- **nonagames.com counter-clear guide → HTTP 410 Gone** (sign-in wall).
- **Semantic Scholar API** returned a non-JSON response (rate-limit) on this
  run; the OpenAlex negative result (§2) stands independently.
- **No analyst source found that published a sample size** for any invade /
  counter-jungle outcome — the precondition checklist in §4 is *consensus*, not
  measurement, and is labelled accordingly.

---

## 10. Open gaps / follow-ups

- **No measured invade dataset exists publicly.** If the product can log game
  timelines, *we* could build the first one: sample games where a champion is in
  the enemy jungle pre-5:00 and measure the gold/XP swing + win rate. That would
  turn §4 from consensus into measured data.
- **Camp bounty table is patch-perishable.** Re-verify Blue/Red/Gromp (and pull
  Raptor/Wolf/Krug) each patch; small-monster bounties not yet captured.
- **Vertical-jungling win rate** is unmeasured; the wiki's "high elo/competitive"
  attribution is a clue but not data.
- **Cross-reference Axis 4 (tempo/pathing)** — the tempo cost of a failed invade
  is the same currency Axis 4 models; the two axes should share a tempo metric.
