#!/usr/bin/env python3
"""
test_poll_bot.py — exercise poll_bot's core logic with a mock Supabase store
(no service_role key needed) against real Riot data.

Run: RIOT_API_KEY=... python test_poll_bot.py
"""
import os
import sys

import poll_bot
from fetch_match import Riot


class MockStore:
    """Stand-in for SupabaseStore — no network, in-memory."""

    def __init__(self):
        self.matches = {}  # user_id -> set of match ids

    def subscribers(self):
        return [
            {"id": "u1", "riot_name": "jugking", "riot_tag": "fines",
             "riot_region": "na1", "riot_id": "jugking#fines"},
        ]

    def processed_match_ids(self, user_id):
        return self.matches.get(user_id, set())

    def upsert_matches(self, user_id, payloads):
        self.matches.setdefault(user_id, set())
        for p in payloads:
            self.matches[user_id].add(p["id"])
        return len(payloads)


def main():
    key = os.environ.get("RIOT_API_KEY")
    if not key:
        print("Set RIOT_API_KEY env var.", file=sys.stderr)
        sys.exit(1)

    riot = Riot(key, "na1")
    store = MockStore()

    subs = store.subscribers()
    print(f"Subscribers: {len(subs)}")

    user = subs[0]
    riot.set_region(user["riot_region"])

    # Pass 1 — should process new games
    n1, payloads = poll_bot.process_user(store, riot, user, count=5, dry_run=False)
    print(f"\nPass 1: {n1} new games processed")
    assert n1 > 0, "expected some new games on first pass"

    # Inspect a payload
    p = payloads[0]
    print(f"  sample payload keys: {sorted(p.keys())}")
    print(f"  sample: {p['champion']} {p['kda']} W={p['win']} {p['duration_min']}min")
    print(f"  moments: {len(p['moments'])} flagged")
    assert "moments" in p and isinstance(p["moments"], list)
    assert p["kda"] and p["champion"] and p["id"]

    # Pass 2 — should process ZERO new games (all now known)
    n2, _ = poll_bot.process_user(store, riot, user, count=5, dry_run=False)
    print(f"\nPass 2: {n2} new games (expect 0 — dedup works)")
    assert n2 == 0, "dedup failed: second pass should find nothing new"

    print("\n✓ poll_bot pipeline works end-to-end (fetch → diff → condense → moments → write)")


if __name__ == "__main__":
    main()
