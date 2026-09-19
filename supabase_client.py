#!/usr/bin/env python3
"""
supabase_client.py — server-side bridge between the Python backend and Supabase.

Uses the SERVICE ROLE key (backend-only, bypasses Row Level Security) so the
pipeline can read subscriber preferences and write processed matches for any
user. The anon key (used by the web frontend) must NOT be used here.

Env vars (set on the VPS / backend host, never committed):
    SUPABASE_URL            — project URL (https://xxxx.supabase.co)
    SUPABASE_SERVICE_ROLE_KEY — the secret service_role key

Usage (example):
    from supabase_client import SupabaseStore
    store = SupabaseStore()
    subs = store.subscribers()          # list of {id, riot_name, riot_tag, riot_region}
    store.upsert_matches(user_id, [match_dict, ...])
"""
import os

from dotenv import load_dotenv
from supabase import create_client

load_dotenv()


class SupabaseStore:
    def __init__(self, url=None, service_role_key=None):
        self.url = url or os.environ.get("SUPABASE_URL")
        self.key = service_role_key or os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
        if not self.url or not self.key:
            raise RuntimeError(
                "Set SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY env vars first "
                "(Supabase dashboard → Project Settings → API)."
            )
        self.client = create_client(self.url, self.key)

    # --- subscribers / preferences ---

    def subscribers(self):
        """All users with a Riot ID set (the bot's polling roster)."""
        rows = (
            self.client.table("profiles")
            .select("id, riot_name, riot_tag, riot_region, riot_id")
            .not_.is_("riot_name", "null")
            .execute()
        )
        return [r for r in rows.data if r.get("riot_name")]

    def preferences(self, user_id):
        row = (
            self.client.table("preferences")
            .select("*")
            .eq("id", user_id)
            .maybe_single()
            .execute()
        )
        return row.data

    # --- matches ---

    def processed_match_ids(self, user_id):
        """Set of match IDs already stored for a user (for diffing)."""
        rows = (
            self.client.table("matches")
            .select("id")
            .eq("user_id", user_id)
            .execute()
        )
        return {r["id"] for r in rows.data}

    def upsert_matches(self, user_id, matches):
        """Insert/update processed matches. `matches` is a list of dicts with an
        `id` key (Riot match_id) plus the summary fields the web app expects."""
        if not matches:
            return 0
        payload = [{**m, "user_id": user_id} for m in matches]
        res = self.client.table("matches").upsert(payload).execute()
        return len(res.data) if res.data else 0
