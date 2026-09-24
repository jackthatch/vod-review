# Jungle Playbook — domain knowledge base

This is the **domain-knowledge layer** for vod-review. It captures how the jungle
role actually works — playstyle archetypes, champion buckets, the decision
frameworks, and the recurring leaks — so the product's detection, benchmarking,
and AI coaching are grounded in expert understanding rather than generic advice.

**Why jungle-first:** the role is the most decision-dense and least-understood in
solo queue, and a leak caught here compounds across the whole map. We build depth
for one role before widening.

**Status of facts:**
- Sections 1, 3, 5, 6, 7 are **durable** (role logic, archetypes, decision
  frameworks) — these don't rotate with patches.
- Section 2 (the clock) and champion tiers **drift every ~2 weeks**; the numbers
  below were read from the LoL wiki in **2026-05** and must be **verified against
  live data**, never hardcoded as permanent truth. The product's rule still holds:
  *detection deterministic, explanation generative*.
- Section 8 is the bridge: which Riot API signal supplies which concept. It is
  deliberately a *candidate list* to be validated against real timelines later.

---

## 1. What the jungle role actually is

The jungle is a **tempo and resource-allocation role**, not a lane. There is no
fixed opponent and no wave to manage; instead you compete with the enemy jungler
over a *finite, shared* pool of camps and convert **time + information** into
advantage somewhere on the map.

Core mental model:

- **Everything is a trade.** Every camp, gank, objective, and recall costs you
  something else (time, a camp, a lane's safety). Good jungling = consistently
  choosing the highest-value trade available to you, not the most exciting one.
- **Tempo is the currency.** "Tempo" = being ahead on the clock — already
  cleared, already recalled, already arrived while the enemy is still finishing a
  camp or walking. Tempo lets you *dictate*; losing it forces you to *react*.
- **You are the early-game engine.** Pre-15 min the jungler sets the pace: first
  blood, first drake, grubs, herald, and tower plates all route through you.
- **Information is power.** Tracking the enemy jungler (via buff timers, ward
  info, lane-arrival patterns) turns coin-flips into knowns.
- **Your lanes are resources.** Lane state (pushed / frozen / even), summoner
  spells, and matchup kill potential decide which gank is worth the walk.

**The three questions every jungle decision answers:**

1. What do I gain? (gold, XP, tempo, objective, kill, pressure)
2. What do I give up? (a camp, tempo, another lane's safety)
3. What does the enemy jungler gain while I do this?

Frame every review moment against these three.

---

## 2. The jungle clock (spawn / respawn timings)

The beats that structure a jungle game. *(Read from the LoL wiki, 2026-05 —
verify before trusting; these shift with patches.)*

| Camp / objective | First spawn | Respawn | Notes |
|---|---|---|---|
| Red Brambleback (red buff) | 0:55 | 5:00 | buff camp |
| Blue Sentinel (blue buff) | 0:55 | 5:00 | buff camp |
| Wolves (Greater Murk Wolf) | 0:55 | 2:15 | small camp |
| Raptors | ~0:55 | 2:15 | small camp |
| Gromp | 1:07 | 2:15 | small camp |
| Krugs | 1:07 | 2:15 | small camp |
| Rift Scuttler (scuttle) | 2:55 | 2:30 | first contested point; top + bottom river |
| Elemental Drake | 5:00 | 5:00 | 4th drake → Dragon Soul |
| Elder Dragon | after a team's 4th drake | 6:00 | spawns once later dragons are done |
| Voidgrubs | 8:00 | — | despawns 14:45 (14:55 if in combat); no longer respawns |
| Rift Herald | 15:00 | — | despawns 19:45 (19:55 if in combat) |
| Baron Nashor | 20:00 | 6:00 | one of three forms |

> **Patch note (2026):** **Atakhan was removed in patch 26.1 (2026)**, along with
> Blood Roses and Feats of Strength; Baron spawns at 20:00 and first-blood (100g) /
> first-turret (300g) gold was restored. Verify against the live patch before
> relying on any row above. Source: [Riot Patch 26.1](https://www.leagueoflegends.com/en-us/news/game-updates/patch-26-1-notes/).

**Why these matter for review:**

- **Buff camps respawn every 5:00** → tracking the enemy's buff timers is the
  single best predictor of where they are. "Their blue came up at 7:00, so
  they'll be top-side around 7:00–7:30."
- **Non-buff camps 2:15** → a full clear "resets" roughly every 2:15; the whole
  game is a rhythm of clear → gank/objective → recall → clear.
- **Scuttle at 2:55** is the first fight for map control → **first-clear speed
  decides it**. This is why time-to-6-camps is the headline jungle benchmark.
- **The objective beats** (5:00 / 8:00 / 15:00 / 20:00) are the tempo anchors:
  winning junglers arrive *before* the beat with items and vision, losers arrive
  late or concede without trading.

---

## 3. Playstyle archetypes (the buckets)

Almost every jungle champion maps to one or two of these. **The archetype
defines what "good" means** — a carry *should* have high CS and gold share; a
tank *should* have low CS and high kill participation. Benchmarking across
archetypes produces inverted, wrong advice. (This is why the tool normalizes by
champion/archetype.)

### A. Farming carry (power-farm / scaling)
- **Win condition:** out-scale, hit item spikes, carry teamfights with damage.
- **Traits:** fast, healthy clears; often weak early 1v1s *relative to gankers*;
  wants farm, not charity ganks.
- **Champions:** Graves, Kindred, Karthus, Lillia, Bel'Veth, Master Yi, Hecarim,
  Udyr (bruiser-carry).
- **Success looks like:** high CS/min, high gold/min, early item spikes, high
  damage share, low deaths/10, kills converted into objectives.
- **Coaching focus:** *don't over-gank*; protect the clear rhythm; fight only at
  spikes; convert leads into objectives rather than chasing kills.

### B. Early-game gank / skirmish (tempo & aggression)
- **Win condition:** snowball before falling off; create pressure, get lanes
  ahead, end early.
- **Traits:** strong early duels/ganks; scales down; needs early leads to matter.
- **Champions:** Lee Sin, Elise, Xin Zhao, Rek'Sai, Rengar, Kha'Zix, Jarvan, Vi,
  Nidalee.
- **Success looks like:** high KP%, early kill participation, good gank→kill
  conversion, first blood, plate/objective conversion.
- **Coaching focus:** pick *high-percentage* ganks; don't fall behind on farm;
  turn pressure into towers/objectives, not just kills.

### C. Tank / engage / utility
- **Win condition:** enable carries, frontline, force fights on your terms,
  control vision and objectives.
- **Traits:** durable, CC-heavy, lower damage, low economy needs.
- **Champions:** Sejuani, Zac, Maokai, Amumu, Rammus, Nunu, Skarner, Poppy.
- **Success looks like:** high KP%, high assist share, strong engage/peel, high
  damage taken, low deaths/10, good objective control.
- **Coaching focus:** engage *timing* and angle, peeling the carry, objective
  setup, and not soaking farm the carries need.

### D. Assassin / pick
- **Win condition:** delete priority targets, create picks, snowball off kills.
- **Traits:** burst, mobility, single-target; fragile when behind.
- **Champions:** Kha'Zix, Rengar, Evelynn, Kayn (Shadow), Talon.
- **Success looks like:** high kill share, flank/engage timing, low deaths/10.
- **Coaching focus:** wait for key cooldowns before diving; target selection;
  don't take even fights while behind.

### E. Objective-control / tempo
- **Win condition:** dominate the clock and neutral objectives; win smite fights.
- **Champions:** Nunu, Ivern, Udyr.
- **Success looks like:** high objective/smite rate, strong tempo, counter-jungle.
- **Coaching focus:** objective timing, smite discipline, vision control.

### F. Bruiser / fighter
- **Win condition:** win skirmishes, play front-to-back, deal durable damage.
- **Champions:** Vi, Hecarim, Wukong, Viego, Xin Zhao, Jarvan.
- **Success looks like:** skirmish win rate, balanced damage + survivability.
- **Coaching focus:** fight selection, dive timing.

> **Hybrids are the norm.** Nidalee is carry *and* early-game; Jarvan is gank
> *and* tank; Hecarim is carry *and* bruiser. A champion can belong to two
> buckets — the benchmark should weight toward its primary.

---

## 4. Champion → archetype (working map)

A first pass to seed the archetype layer. **To be validated against live data**
(champion pick/win rates and stat distributions) and extended.

| Archetype | Champions |
|---|---|
| Farming carry | Graves, Kindred, Karthus, Lillia, Bel'Veth, Master Yi, Hecarim, Udyr |
| Early gank / skirmish | Lee Sin, Elise, Xin Zhao, Rek'Sai, Rengar, Kha'Zix, Jarvan, Vi, Nidalee, Nunu |
| Tank / engage | Sejuani, Zac, Maokai, Amumu, Rammus, Skarner, Poppy, Nunu |
| Assassin / pick | Kha'Zix, Rengar, Evelynn, Kayn, Talon |
| Objective / tempo | Nunu, Ivern, Udyr |
| Bruiser / fighter | Vi, Hecarim, Wukong, Viego, Xin Zhao, Jarvan |

---

## 5. Per-archetype success metrics

The metrics the tool should compute, and the *shape* they should take per
archetype. This is what the radar / benchmark normalizes against.

| Metric | Carry | Gank | Tank | Assassin |
|---|---|---|---|---|
| CS/min | **high** | med | low | med |
| Gold/min | **high** | med | low | med |
| KP% | low–med | **high** | **high** | med–high |
| First-clear speed | **low (fast)** | med | med | low |
| Deaths / 10min | low | med | low | low |
| Damage share | **high** | med | low | high |
| Objective / smite rate | med | med | **high** | med |
| Vision score | med | med | **high** | low–med |
| Item-spike timing | **early** | — | — | early |

Reading the table is the whole point: **6.5 CS/min is excellent on a tank and
mediocre on a Graves.** Any absolute number without archetype context is noise.

---

## 6. Decision frameworks

### 6.1 Gank vs farm
A gank is worth it when `P(kill) × value > cost` (2+ camps of gold/XP + lost
tempo + risk of being counter-ganked). Inputs:
- **Lane state:** is the target's wave favorable (gankable) or are they safe
  under tower? Does our laner have CC/setup and health?
- **Kill potential:** do we have the damage + CC for the 2v1/3v2? Are enemy
  summoners down?
- **Cost:** the walk costs camps; a failed gank costs tempo *and* invites the
  enemy jungler to take your camps.
- **Heuristic:** gank lanes with kill pressure and setup; don't burn tempo on a
  lost lane unless it's a numbers dive.

### 6.2 Pathing & clear
- Level-1 path is chosen by: which lane to impact first, the **2:55 scuttle**, and
  camp respawns.
- Common opens: **full clear → gank/scuttle**, or **3–4 camps → gank → reset**.
- **Vertical jungling:** if the enemy jungler shows top, take their bot-side camps.
- **Backtracking/idle time is the #1 efficiency leak** — a good clear is a loop,
  not a zigzag. First-clear speed is the headline benchmark.

### 6.3 Objective sequencing
- **5:00 drake vs 8:00 grubs:** decide by drake type value, whether the fight is
  winnable, lane prio (who can rotate), and whether you can *trade* (take the
  opposite side instead).
- **Grubs → plates/tower pressure.** Great with pushing lanes or a top-side lead.
- **Herald (15:00) → tower pressure/tempo.** Take with numbers.
- **Soul stakes:** the 4th drake grants Dragon Soul — treat the 3rd/4th as
  high-stakes; a soul point is worth over-committing for.
- **Baron / Atakhan (20:00):** game-ending objectives — set vision and shove
  waves *before* the beat.
- **Key principle: an objective you can't win should be TRADED, not forced.**
  "Concede and take the opposite objective / towers" is frequently correct. The
  review must not label a deliberate concede as a mistake.

### 6.4 Tempo & recall
- **Recall after clearing/scoring** to reset and spend. Never sit on 1,500g+ in
  the field — that is the classic **overstay** leak (the tool flags it).
- **Recall timing around objective spawns:** be back with items *before* drake.
- **Wasting tempo** looks like: doing a scuttle while drake spawns, or finishing
  a camp while a free kill sits available.

### 6.5 Vision
- **Control ward** in the defensible river quadrant; objective vision ~60s before
  spawn.
- **Deep wards** in the enemy jungle to track clears.
- **Sweep before objectives**, deny enemy vision.
- Vision is the cheapest way to convert a coin-flip objective into a known win.

### 6.6 Teamfights by archetype
- **Carry:** front-to-back, kite, position behind the frontline, fight at spikes.
- **Engage tank:** initiate from a good *angle*, not a 1-for-1 dive; then peel.
- **Assassin:** flank and wait for key cooldowns (CC/peel used) before diving the
  carry.
- **Bruiser:** front-to-back; dive when the moment is right.

### 6.7 Tracking the enemy jungler
- **Buff timers (5:00)** predict their position.
- **Lane arrival:** a laner arriving late or low HP means the jungler ganked or
  is nearby.
- **Clear counting:** a jungler who started top is bottom-side by ~3:00.
- **Deny information:** don't show on the map unnecessarily.

---

## 7. Common leaks (what the product should catch)

The recurring, coachable mistakes, in rough order of how often they cost games:

1. **Overstaying** — dying while holding unspent gold (farm/back-timing leak).
2. **Slow / inefficient first clear** — loses scuttle and early tempo.
3. **Objective timers ignored** — not prepped, not traded, not contested with
   numbers.
4. **Not tracking the enemy jungler** — avoidable ganks and invade deaths.
5. **Ganking a lost lane** / low-percentage ganks.
6. **Over-ganking as a carry** — CS/min collapses, spikes get delayed.
7. **Under-ganking as a gank jungler** — farming while the clock runs out.
8. **Conceding objectives without trading** — giving soul/baron for nothing.
9. **Dying in the enemy jungle** — invade deaths with no escape plan.
10. **Bad recall timing** — recalling as drake spawns, or sitting on gold.
11. **Not converting kills into objectives/towers** — kills without pressure.
12. **Poor vision setup before objectives** — fighting blind.

---

## 8. Mapping knowledge → Riot API data

The bridge from the concepts above to computable signals. **Candidate list** —
each must be validated against real timelines (see `KNOWN_ISSUES.md` #4).

| Concept | Riot API signal | How |
|---|---|---|
| CS/min, gold/min | `totalMinionsKilled` + `neutralMinionsKilled`, `totalGold`/frame | per-frame snapshot deltas |
| First-clear speed | `jungleMinionsKilled` per frame | time until ≥6 (or 9) camps |
| Kill participation | `kills`+`assists` / team kills | from `CHAMPION_KILL` events |
| Objective control / smite | `ELITE_MONSTER_KILL` + `killerId` | did *I* secure it |
| Drake soul stakes | count drakes per team | 4th drake = soul point |
| Deaths / 10min + locations | `CHAMPION_KILL` `victimId` + `position` | classify via `location_label()` → invade deaths |
| Overstay | `currentGold` at death frame | unspent gold held |
| Power spikes | AD jumps / `ITEM_PURCHASED` events | item-completion timing |
| Tempo | `xp` / `level` / `totalGold` curves | compare pace vs baseline |
| Pathing efficiency | `position` per frame | idle/backtrack detection |
| Vision | `WARD_PLACED` / `WARD_KILLED` (partial) | no vision score in timeline |
| Counter-jungle | position in enemy half + `jungleMinionsKilled` | approximate |

**Known gaps to hedge on** (documented in `VISION.md`): exact **wave state**,
**summoner-spell cooldowns**, and true **vision score** are not in the timeline.
Anything that depends on them must be hedged, never asserted.
