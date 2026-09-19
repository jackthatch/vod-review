#!/usr/bin/env python3
"""
poll_bot.py — the cloud subscription bot.

Polls every subscriber's Riot match history on a cadence, diffs against what's
already processed, and writes new games (condensed + moment-flagged) into Supabase
for the web frontend to display.

This is the "no webhook" polling loop described in VISION.md. Run it on a cron /
scheduler on the backend host (VPS).

Usage:
    python poll_bot.py                     # one poll pass over all subscribers
    python poll_bot.py --count 20          # fetch last N matches per subscriber
    python poll_bot.py --dry-run           # print what would be written, no writes

Env vars:
    RIOT_API_KEY               — Riot development/production key
    SUPABASE_URL               — Supabase project URL
    SUPABASE_SERVICE_ROLE_KEY  — Supabase service_role key (backend-only)
"""
import argparse
import os
import sys

from dotenv import load_dotenv

import moments
from fetch_match import Riot, condense
from supabase_client import SupabaseStore

load_dotenv()


def kda_str(match):
    s = match["stats"]
    return f"{s['kills']}/{s['deaths']}/{s['assists']}"


def match_payload(story):
    """Shape a condensed story into the `matches` row the web app reads."""
    ms = moments.analyze(story)
    return {
        "id": story["match_id"],
        "champion": story["champion"],
        "role": story["role"],
        "win": story["win"],
        "duration_min": story["duration_min"],
        "kda": kda_str(story),
        "moments": ms,  # jsonb — list of ranked moment dicts
        "summary": None,  # LLM narrative comes later
    }


def process_user(store, riot, user, count, dry_run):
    user_id = user["id"]
    name, tag, region = user["riot_name"], user["riot_tag"], user["riot_region"]
    if not (name and tag and region):
        return 0, []

    try:
        puuid = riot.puuid(name, tag)
        ids = riot.match_ids(puuid, count)
    except Exception as e:
        print(f"  ! {name}#{tag}: fetch failed ({e})")
        return 0, []

    known = store.processed_match_ids(user_id) if not dry_run else set()
    new_ids = [m for m in ids if m not in known]

    written = 0
    payloads = []
    for mid in new_ids:
        try:
            match = riot.match(mid)
            tl = riot.timeline(mid)
            story = condense(match, tl, puuid)
            payloads.append(match_payload(story))
            written += 1
        except Exception as e:
            print(f"  ! {mid}: process failed ({e})")

    if payloads and not dry_run:
        store.upsert_matches(user_id, payloads)

    return written, payloads


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--count", type=int, default=20)
    ap.add_argument("--dry-run", action="store_true",
                    help="process but do not write to Supabase")
    args = ap.parse_args()

    riot = Riot(os.environ.get("RIOT_API_KEY") or _require("RIOT_API_KEY"),
                "na1")  # region is overridden per-user below

    if args.dry_run:
        # dry-run still needs a store for the subscriber list, but we skip writes
        store = SupabaseStore()
        subs = store.subscribers()
    else:
        store = SupabaseStore()
        subs = store.subscribers()

    if not subs:
        print("No subscribers with a Riot ID set.")
        return

    total = 0
    for user in subs:
        name = f"{user['riot_name']}#{user['riot_tag']}"
        region = user.get("riot_region") or "na1"
        riot.set_region(region)  # per-user platform routing
        n, _ = process_user(store, riot, user, args.count, args.dry_run)
        total += n
        print(f"{name} ({region}): {n} new game(s)")

    print(f"\nDone — {total} new game(s) total"
          + (" (dry run, nothing written)" if args.dry_run else ""))


def _require(var):
    print(f"Set {var} env var first.", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()
