# Environment constraints for the research study

**Discovered 2026-09-24, first research run.** This is the single most important
operational finding — it dictates *how* the long-running study must be conducted
from this container.

## What is blocked

- **Search engines:** Google, Bing (web), DuckDuckGo (HTML/Lite/API), Brave,
  Startpage, Ecosia, Mojeek, Qwant, Marginalia, Yandex — all returned
  CAPTCHA / 403 / redirects to automated access.
- **LoL stat sites:** op.gg, u.gg, lolalytics, leagueofgraphs, Mobalytics — all
  403 / Cloudflare.
- **Reddit:** JSON endpoints blocked.
- The sandbox IP is evidently flagged.

## What works

- **Riot primary sources:** `leagueoflegends.com` patch notes + `/dev` dev blogs,
  `lolesports.com` articles — fetch fine via `curl`/browser.
- **LoL Wiki MediaWiki API:** `https://wiki.leagueoflegends.com/en-us/api.php`
  (the `/en-us/` path works; the bare `/api.php` is Cloudflare-blocked). Great for
  objective/camp timings and mechanics.
- **Academic APIs:** OpenAlex, Crossref, arXiv, ar5iv — work.
- **Some WordPress REST APIs** (esports outlets) and **Bing News RSS** (headlines
  only).

## Implications for the study method

1. **Prefer direct primary sources over search.** Enumerate known URLs (Riot patch
   notes index, Riot `/dev` index, wiki pages, stat-site *APIs* if any) and fetch
   them directly, rather than search-then-click.
2. **Stat-site numeric win rates are effectively unavailable from here.** Treat
   "win rate of X" questions as gaps unless a primary or academic source states it.
   Options for later: a proxy, a local/VPS fetch, or Riot's own Data Dragon/API.
3. **Sub-agents must write their file FIRST** (or early), not last — they hit
   iteration caps otherwise. The first run produced findings that had to be
   salvaged from summaries because the file was never written.
4. **Budget iterations:** sub-agents spent ~50 calls mostly fighting blocked
   searches. Narrow, direct, source-listed tasks will be far more productive.

## Known-good direct sources (seed list)

- Riot patch notes: `https://www.leagueoflegends.com/en-us/news/game-updates/`
- Riot dev posts: `https://www.leagueoflegends.com/en-us/news/dev/`
- LoL Wiki API: `https://wiki.leagueoflegends.com/en-us/api.php?action=query&...`
- lolesports dev diaries: `https://lolesports.com/article/...`
- Riot /dev: "How the Season 1 Changes Landed" (2025-02-07) — has win-rate table
- Riot /dev: "2026 Season One Gameplay Preview" — current meta state
- Riot Patch 26.1 notes — Atakhan/Feats removal, Baron timing
- Riot Patch 25.09 notes — Voidgrub changes
