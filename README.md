# vod-review

AI VOD review for League of Legends — jungle-first. Pull your match timeline from the
Riot API, reconstruct a structured "story" of each game, and aggregate it into a
**leak profile** of your recurring mistakes (first-clear speed, death patterns,
overstaying, objective control). Benchmark against pro solo-queue junglers.

## Setup

1. Get a **Development API key** at https://developer.riotgames.com (free, works immediately for personal use).
2. Install deps:
   ```bash
   python3 -m venv venv && source venv/bin/activate
   pip install -r requirements.txt
   ```
3. Export your key (never hardcode it):
   ```bash
   export RIOT_API_KEY="your-key-here"
   ```

## Fetch your matches

```bash
python fetch_match.py --name YourSummoner --tag NA1 --region na1 --count 20
```

- `--name` / `--tag` — your RiotID (`name#TAG` → pass them split, or pass `--name "name#TAG"`).
- `--region` — platform (e.g. `na1`, `euw1`, `kr`, `ph2`).
- `--count` — how many recent matches to fetch (each match = 2 API calls).
- Output lands in `./data/<match_id>.json` — one structured story per match.

## Leak profile (`trends.py`)

Aggregate the fetched matches into recurring-pattern metrics:

```bash
python trends.py --data data --champion Graves
```

- `--champion` — only include games on this champion (essential: a Graves profile vs a
  Sejuani profile are different playstyles).
- `--role` — filter by role (e.g. `JUNGLE`).
- `--overstay-gold` — unspent-gold threshold for the "overstayed" flag (default `1000`).
- `--json` — emit raw JSON instead of the human-readable report.

Reported metrics: first-clear speed (time to 6 camps), CS/min, deaths/game, kill
participation, death-timing distribution, overstay rate, and objective control
(dragon/herald/baron secured by your team vs. by your smite).

## Pro benchmark roster (`pros.json`)

Fetch pro junglers' solo-queue games with the same script (they're on the live servers):

```bash
python fetch_match.py --name vinaka       --tag KR1 --region kr   --count 100   # Kanavi
python fetch_match.py --name JUGKlNG      --tag kr  --region kr   --count 100   # Canyon
python fetch_match.py --name "LFT Sheiden" --tag PHL1 --region ph2 --count 100  # Sheiden
```

Names/tags live in `pros.json`. To get enough same-champion games for a meaningful
benchmark you need large pulls (pros don't play Graves every game), so expect rate-limit
slowdowns — the script auto-backs-off on `429`.

## Verifying data infill

Before trusting `trends.py`, spot-check one file:

```bash
python -c "import json,glob; d=json.load(open(sorted(glob.glob('data/*.json'))[0])); print(d['champion'], '| first_clear:', d['first_clear_min'], '| snapshots:', len(d['snapshots']), '| deaths:', len(d['deaths']), '| objectives:', len(d['objectives']))"
```

Working output looks like: `Graves | first_clear: 3.4 | snapshots: 45 | deaths: 5 | objectives: 4`.
If `first_clear` is `None` or `snapshots` is empty, the fetch didn't capture data.

## Data shape

Each `data/<match_id>.json` contains:

```json
{
  "champion": "Graves", "role": "JUNGLE", "participant_id": 5, "team_id": 100,
  "win": true, "duration_min": 28.4, "opponent_champion": "LeeSin",
  "stats": { "kills": 8, "deaths": 3, "assists": 9, "total_cs": 180, "gold": 9000 },
  "first_clear_min": 3.4,
  "snapshots": [ { "min": 3.5, "level": 4, "total_gold": 1400, "current_gold": 1200,
                   "cs": 24, "jungle_cs": 6, "x": 8000, "y": 7000 } ],
  "deaths": [ { "min": 3.8, "killer_id": 9, "x": 7000, "y": 7000, "current_gold": 1100 } ],
  "objectives": [ { "min": 6.0, "type": "DRAGON", "sub": "EARTH_DRAGON",
                    "team": 100, "mine": true } ]
}
```

## Roadmap

- [x] Fetch matches + timeline, condense into structured JSON
- [x] Leak detection (`trends.py`) — first-clear speed, death patterns, overstaying, objective control
- [x] Champion filter (`--champion`) — basic champion normalization
- [x] Power-spike + economy metrics — level timing, AD@10/20min, gold/min, farming-vs-fighting ratio, item-spike detection, damage taken/min
- [ ] Pro solo-queue benchmarking — diff your profile against the `pros.json` roster
- [ ] Champion archetype layer (farming-carry vs. utility vs. gank junglers)
- [ ] Moment detection — flag pivotal in-game moments (lost objectives, overstays, spike gaps)
- [ ] LLM grounding layer — turn the JSON into a natural-language coaching review
- [ ] Output formats (markdown report / web UI)

See [`VISION.md`](VISION.md) for the long-term direction ("speedrun VOD review").
