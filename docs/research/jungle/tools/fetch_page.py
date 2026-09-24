#!/usr/bin/env python3
"""
fetch_page.py — resilient page fetcher for the jungle research study.

The study runs on a datacenter IP (Hostinger AS47583) where plain `curl` is
blocked by Cloudflare/Google bot management. Raw requests fail even for
perfectly public pages. This module gives the study a 3-tier fetch strategy
so it never depends on a single route:

    Tier 1  direct HTTP (curl/requests, browser UA)   -> fast, works for friendly sites
    Tier 2  r.jina.ai reader proxy                    -> free, renders JS, returns Markdown
    Tier 3  Playwright + real Chromium                -> full browser, defeats most JS challenges

Usage (module):
    from fetch_page import fetch
    res = fetch("https://lolalytics.com/lol/graves/build/?lane=jungle")
    print(res.tier, res.status, len(res.text)); print(res.text[:500])

Usage (CLI):
    python3 fetch_page.py <url> [--tier auto|direct|jina|browser] [--raw] [--json]

Exit codes: 0 = got content, 1 = all tiers failed.

Verified reachability from the container (2026-09):
    OK   u.gg        (jina, browser)
    OK   op.gg       (jina, browser)
    OK   lolalytics  (browser)
    OK   DuckDuckGo  (jina)   -- search
    OK   Bing        (jina)   -- search
    FAIL Google      (captcha on every tier)
    FAIL leagueofgraphs (hard Cloudflare; redundant -- u.gg/lolalytics cover it)

Never logs or echoes credentials. Read-only fetcher.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass, asdict
from typing import Optional

BROWSER_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

# Signatures that mean "we were served a bot wall, not the real page".
BLOCK_MARKERS = (
    "just a moment",
    "performing security verification",
    "security service to protect against malicious bots",
    "enable javascript and cookies to continue",
    "are you a robot",
    "unusual traffic",
    "verify you are human",
    "cf-browser-verification",
    "attention required! | cloudflare",
)


@dataclass
class FetchResult:
    url: str
    tier: str
    status: int
    text: str
    blocked: bool = False
    error: Optional[str] = None

    def ok(self) -> bool:
        return bool(self.text) and not self.blocked and (self.status == 0 or self.status < 400)


def _looks_blocked(text: str) -> bool:
    low = text.lower()
    return any(m in low for m in BLOCK_MARKERS)


def _via_direct(url: str, timeout: int = 20) -> FetchResult:
    try:
        out = subprocess.run(
            ["curl", "-sSL", "--max-time", str(timeout), "-A", BROWSER_UA,
             "-H", "Accept-Language: en-US,en;q=0.9", "-w", "\n__HTTP__%{http_code}", url],
            capture_output=True, text=True, timeout=timeout + 10,
        )
        body = out.stdout
        status = 0
        if "__HTTP__" in body:
            body, _, code = body.rpartition("__HTTP__")
            status = int(code.strip() or 0)
        blocked = _looks_blocked(body)
        return FetchResult(url, "direct", status, body, blocked)
    except Exception as e:  # noqa: BLE001
        return FetchResult(url, "direct", 0, "", False, f"{type(e).__name__}: {e}")


def _via_jina(url: str, timeout: int = 45) -> FetchResult:
    try:
        out = subprocess.run(
            ["curl", "-sSL", "--max-time", str(timeout),
             "-H", "X-Return-Format: markdown", f"https://r.jina.ai/{url}"],
            capture_output=True, text=True, timeout=timeout + 10,
        )
        body = out.stdout
        blocked = _looks_blocked(body)
        # r.jina.ai returns 200 even when upstream was blocked; rely on markers.
        return FetchResult(url, "jina", 200 if body else 0, body, blocked)
    except Exception as e:  # noqa: BLE001
        return FetchResult(url, "jina", 0, "", False, f"{type(e).__name__}: {e}")


def _via_browser(url: str, timeout: int = 40) -> FetchResult:
    try:
        from playwright.sync_api import sync_playwright
    except Exception as e:  # noqa: BLE001
        return FetchResult(url, "browser", 0, "", False, f"playwright unavailable: {e}")
    try:
        with sync_playwright() as p:
            b = p.chromium.launch(args=[
                "--no-sandbox", "--disable-blink-features=AutomationControlled",
            ])
            ctx = b.new_context(user_agent=BROWSER_UA, locale="en-US",
                                viewport={"width": 1440, "height": 900})
            ctx.add_init_script(
                "Object.defineProperty(navigator,'webdriver',{get:()=>undefined})"
            )
            pg = ctx.new_page()
            r = pg.goto(url, wait_until="domcontentloaded", timeout=timeout * 1000)
            pg.wait_for_timeout(3500)  # let JS/challenge settle
            body = pg.inner_text("body")
            status = r.status if r else 0
            b.close()
        return FetchResult(url, "browser", status, body, _looks_blocked(body))
    except Exception as e:  # noqa: BLE001
        return FetchResult(url, "browser", 0, "", False, f"{type(e).__name__}: {e}")


def fetch(url: str, tier: str = "auto", verbose: bool = False) -> FetchResult:
    """Fetch `url`, escalating through tiers until real (unblocked) content comes back."""
    order = {
        "auto": [_via_direct, _via_jina, _via_browser],
        "direct": [_via_direct],
        "jina": [_via_jina],
        "browser": [_via_browser],
    }[tier]

    attempts: list[FetchResult] = []
    for fn in order:
        res = fn(url)
        attempts.append(res)
        if verbose:
            print(f"  [{res.tier}] status={res.status} len={len(res.text)} "
                  f"blocked={res.blocked} err={res.error}", file=sys.stderr)
        if res.ok():
            return res
    # nothing clean — return the richest attempt for inspection
    best = max(attempts, key=lambda r: len(r.text))
    best.error = best.error or "all tiers blocked or empty"
    return best


def main() -> int:
    ap = argparse.ArgumentParser(description="3-tier resilient page fetcher")
    ap.add_argument("url")
    ap.add_argument("--tier", default="auto", choices=["auto", "direct", "jina", "browser"])
    ap.add_argument("--raw", action="store_true", help="print full text, else first 2000 chars")
    ap.add_argument("--json", action="store_true", help="emit JSON result object")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    res = fetch(args.url, tier=args.tier, verbose=args.verbose)
    if args.json:
        d = asdict(res)
        d["text"] = d["text"][:2000]
        d["ok"] = res.ok()
        print(json.dumps(d, indent=2))
    else:
        if not res.ok():
            print(f"[FAIL] tier={res.tier} status={res.status} "
                  f"blocked={res.blocked} err={res.error}", file=sys.stderr)
        print(res.text if args.raw else res.text[:2000])
    return 0 if res.ok() else 1


if __name__ == "__main__":
    raise SystemExit(main())
