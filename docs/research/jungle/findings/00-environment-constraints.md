# Environment constraints & how we solved them

**Status: RESOLVED (2026-09-24).** This file originally recorded that the study
could not reach stat sites or search engines. That is no longer true. Read the
"Solution" section before reporting a fetch failure.

## The original problem

Run 1's research agents burned most of their budget fighting access walls:

| Target | Symptom |
|---|---|
| Google, Bing, DuckDuckGo, Brave | CAPTCHA / bot challenge |
| op.gg, u.gg, lolalytics, leagueofgraphs | HTTP 403 |

Two independent causes were conflated:

1. **Datacenter IP.** The container runs on Hostinger (`187.77.192.226`,
   AS47583) — a cloud/hosting ASN. Bot-management vendors (Cloudflare,
   Google) score datacenter IPs as high-risk by default.
2. **Wrong tool.** Plain `curl` sends a bare TLS/JA3 fingerprint and no JS
   execution. Modern bot walls fingerprint the *client*, not just the IP, so
   even a clean residential IP gets challenged with bare `curl`.

> **Important:** a VPS is *also* a datacenter IP. Moving the study to the
> existing `/srv/hermes` VPS would NOT fix this — it is the same ASN class.
> Only a **residential** IP changes the reputation score.

## The solution: a 3-tier fetch layer

`tools/fetch_page.py` escalates until it gets real (unblocked) content:

| Tier | Method | Good for |
|---|---|---|
| 1 | direct `curl` + browser UA | sites with light/no bot management |
| 2 | `r.jina.ai` reader proxy (free, renders JS → Markdown) | most Cloudflare-fronted sites, search engines |
| 3 | Playwright + real Chromium | heavy JS challenges, SPA data |

The fetcher also **detects bot-wall pages by content** (Cloudflare "Just a
moment", "Performing security verification", Captcha markers) and treats them
as failures rather than returning garbage. This is the critical bit: several
routes return **HTTP 200 with a challenge page**, so status code alone lies.

### Verified reachability from the container (2026-09)

| Source | Tier that works | Notes |
|---|---|---|
| **lolalytics** | 1 (direct!) | 630 KB SSR HTML, data embedded; best granular win-rate source |
| **u.gg** | 2 / 3 | full champion stats, patch-current |
| **op.gg** | 2 / 3 | champion tier + build data |
| **DuckDuckGo** (`html/` endpoint) | 1 (direct) | search + snippets |
| **Bing** | 2 | search |
| **LoL Wiki** | MediaWiki API (no `/en-us`) | timings, mechanics |
| **Riot primary sources** | direct | dev blogs, patch notes, Data Dragon |
| **arXiv / OpenAlex / Crossref** | direct | academic work |
| Google | ✗ all tiers | CAPTCHA persists; use Bing/DDG instead |
| leagueofgraphs | ✗ all tiers | hard Cloudflare; **redundant** — u.gg + lolalytics cover the same stats |

### How to use it

```bash
# human / agent inspection
python3 tools/fetch_page.py "https://lolalytics.com/lol/graves/build/?lane=jungle" --verbose

# from study code
from fetch_page import fetch
res = fetch(url)            # auto-escalates
if res.ok(): use(res.text)
```

## Residual limits (be honest about these)

- **Google is unusable.** Bing and DDG cover ~all needs; don't waste budget on Google.
- **leagueofgraphs is unusable** and unnecessary. Don't target it.
- **JS-rendered SPAs** (u.gg, op.gg) need tier 2/3; tier 1 returns a shell.
  Always check `len(text)` — a 20 KB "success" on a stats page is usually a shell.
- **Rate limits still apply.** Escalating to a browser is expensive (~4 s/page).
  Batch politely; don't hammer.
- **No API keys are required** for the free tiers. If we later add a paid search
  API (Serper/Tavily/Brave) or a residential proxy, wire it in as tier 0.

## If a site stops working

Do **not** conclude "research is blocked." Test the tiers explicitly:

```bash
for t in direct jina browser; do
  echo "--- $t ---"
  python3 tools/fetch_page.py "<url>" --tier "$t" --verbose 2>&1 | head -3
done
```

Record the new result in this file. Escalate to a residential proxy only if a
*source we actually need* fails all three tiers.
