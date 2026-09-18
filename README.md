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
- [ ] **Pro solo-queue benchmarking** — pull games from a `pros.json` roster of pro junglers
  (Kanavi, Canyon, Sheiden, …), compute the same metrics, and diff against your own.
- [ ] **Champion-focus layer** — normalize by champion (and later archetype), so benchmarks
  compare *your Graves* vs. *pro Graves*, not Graves vs. Sejuani. Metrics like clear speed,
  economy, and gank frequency are playstyle-dependent and must be champion-aware.
