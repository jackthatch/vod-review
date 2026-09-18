# vod-review

AI VOD review for League of Legends — pull your match timeline from the Riot API,
reconstruct a structured "story" of the game, and (next) feed it to an LLM for a
real coaching breakdown.

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

## Usage

```bash
python fetch_match.py --name YourSummoner --tag NA1 --region na1 --count 5
```

- `--name` / `--tag` — your RiotID (`name#TAG` → pass them split, or pass `--name "name#TAG"`).
- `--region` — platform (e.g. `na1`, `euw1`, `kr`).
- `--count` — how many recent matches to fetch.
- Output lands in `./data/<match_id>.json` — one condensed "story" per match.

## Roadmap

- [x] Fetch matches + timeline, condense into structured JSON
- [ ] LLM grounding layer — turn the JSON into a coaching review (lane phase, trading, mid/late game)
- [ ] Output formats (CLI text → web UI / markdown report)
- [ ] **Leak detection** — aggregate many of *your* games to surface recurring mistakes
  (overstaying on unspent gold, death timing/location clusters, CS deficits, vision gaps,
  missed objectives). Produces a longitudinal "leak profile" per player.
- [ ] **Pro VOD analysis** — ingest a corpus of pro matches, extract per-player metrics
  (CS/min, gold@10, recall/roam timing, objective participation, death avoidance), and
  compare players to surface the strategies + metrics that actually correlate with winning.
