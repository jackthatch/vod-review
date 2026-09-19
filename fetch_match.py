#!/usr/bin/env python3
"""
fetch_match.py — pull your LoL match history + timeline via the Riot API,
condense it into a structured, LLM/analysis-ready JSON per match.

Usage:
    export RIOT_API_KEY=*** \
    python fetch_match.py --name "YourName" --tag "NA1" --region na1 --count 5

Output: JSON per match under ./data/<match_id>.json
"""
import argparse
import json
import os
import sys
import time
from urllib.parse import quote

import requests

# match-v5 uses regional routing; summoner-v4 uses platform routing
REGION_ROUTING = {
    "na1": "americas", "br1": "americas", "la1": "americas",
    "la2": "americas", "oc1": "americas",
    "euw1": "europe", "eun1": "europe", "tr1": "europe", "ru": "europe",
    "kr": "asia", "jp1": "asia",
    "sg2": "sea", "tw2": "sea", "vn2": "sea", "ph2": "sea",
}


class Riot:
    def __init__(self, api_key, region):
        self.key = api_key
        self.platform = region
        self.region = REGION_ROUTING.get(region, region)
        self.platform_host = f"https://{self.platform}.api.riotgames.com"
        self.region_host = f"https://{self.region}.api.riotgames.com"

    def _get(self, host, path):
        r = requests.get(f"{host}{path}", headers={"X-Riot-Token": self.key})
        if r.status_code == 429:  # rate limit — back off
            time.sleep(int(r.headers.get("Retry-After", 1)))
            return self._get(host, path)
        r.raise_for_status()
        return r.json()

    def puuid(self, name, tag):
        if "#" in name:
            name, tag = name.split("#", 1)
        p = self._get(
            self.region_host,
            f"/riot/account/v1/accounts/by-riot-id/{quote(name)}/{quote(tag)}",
        )
        return p["puuid"]

    def match_ids(self, puuid, count):
        return self._get(
            self.region_host,
            f"/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count={count}",
        )

    def match(self, match_id):
        return self._get(self.region_host, f"/lol/match/v5/matches/{match_id}")

    def timeline(self, match_id):
        return self._get(
            self.region_host, f"/lol/match/v5/matches/{match_id}/timeline"
        )


def _opponent(match, me):
    for p in match["info"]["participants"]:
        if p["teamId"] != me["teamId"] and p.get("lane") == me.get("lane"):
            return p["championName"]
    return "?"


def _gold_at(snapshots, t_min):
    """current_gold of the last snapshot at or before t_min (minutes)."""
    best = None
    for s in snapshots:
        if s["min"] <= t_min:
            best = s["current_gold"]
        else:
            break
    return best


def condense(match, timeline, puuid):
    """Turn raw match+timeline into a structured, analysis-ready dict."""
    info = match["info"]
    participants = info["participants"]
    me = next(p for p in participants if p["puuid"] == puuid)
    my_id = me["participantId"]
    my_team = me["teamId"]

    fi = timeline["info"]["frameInterval"]  # ms per frame
    frames = timeline["info"]["frames"]
    duration_min = round(fi * len(frames) / 60000, 1)

    # per-frame snapshot of MY state (every ~30–60s)
    snapshots = []
    for i, f in enumerate(frames):
        pf = f["participantFrames"].get(str(my_id))
        if not pf:
            continue
        snapshots.append({
            "min": round(i * fi / 60000, 1),
            "level": pf["level"],
            "total_gold": pf["totalGold"],
            "current_gold": pf["currentGold"],  # gold in pocket (unspent)
            "cs": pf["minionsKilled"] + pf["jungleMinionsKilled"],
            "jungle_cs": pf["jungleMinionsKilled"],
            "x": pf["position"]["x"],
            "y": pf["position"]["y"],
        })

    deaths, kills, objectives = [], [], []

    # Events may be top-level (older API) or embedded per-frame (current API).
    events = timeline["info"].get("events")
    if events is None:
        events = []
        for f in frames:
            events.extend(f.get("events", []))

    for ev in events:
        t = ev["timestamp"] / 60000.0  # minutes
        et = ev["type"]
        if et == "CHAMPION_KILL":
            pos = ev.get("position", {})
            if ev.get("victimId") == my_id:
                deaths.append({
                    "min": round(t, 1),
                    "killer_id": ev.get("killerId"),
                    "x": pos.get("x"), "y": pos.get("y"),
                    "current_gold": _gold_at(snapshots, t),
                })
            elif ev.get("killerId") == my_id:
                kills.append({
                    "min": round(t, 1),
                    "victim_id": ev.get("victimId"),
                    "x": pos.get("x"), "y": pos.get("y"),
                })
        elif et == "ELITE_MONSTER_KILL":
            objectives.append({
                "min": round(t, 1),
                "type": ev.get("monsterType"),
                "sub": ev.get("monsterSubType"),
                "team": ev.get("killerTeamId"),
                "mine": ev.get("killerId") == my_id,
            })

    # first full clear: first frame where I've taken 6 jungle camps
    first_clear = None
    for s in snapshots:
        if s["jungle_cs"] >= 6:
            first_clear = s["min"]
            break

    total_cs = me.get("totalMinionsKilled", 0) + me.get("neutralMinionsKilled", 0)

    return {
        "match_id": match["metadata"]["matchId"],
        "champion": me["championName"],
        "role": me.get("role", "?"),
        "participant_id": my_id,
        "team_id": my_team,
        "win": me["win"],
        "duration_min": duration_min,
        "opponent_champion": _opponent(match, me),
        "stats": {
            "kills": me["kills"],
            "deaths": me["deaths"],
            "assists": me["assists"],
            "total_cs": total_cs,
            "gold": me.get("goldEarned", 0),
        },
        "first_clear_min": first_clear,
        "snapshots": snapshots,
        "deaths": deaths,
        "kills": kills,
        "objectives": objectives,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", required=True)
    ap.add_argument("--tag", required=True, help="RiotID tagline (after the #)")
    ap.add_argument("--region", required=True)
    ap.add_argument("--count", type=int, default=5)
    ap.add_argument("--out", default="data")
    args = ap.parse_args()

    key = os.environ.get("RIOT_API_KEY")
    if not key:
        # fall back to loading .env from the script directory
        try:
            from dotenv import load_dotenv
            load_dotenv()
            key = os.environ.get("RIOT_API_KEY")
        except ImportError:
            pass
    if not key:
        sys.exit("Set RIOT_API_KEY env var first (developer.riotgames.com)")

    riot = Riot(key, args.region)
    puuid = riot.puuid(args.name, args.tag)
    print(f"PUUID: {puuid}")

    ids = riot.match_ids(puuid, args.count)
    for mid in ids:
        match = riot.match(mid)
        tl = riot.timeline(mid)
        story = condense(match, tl, puuid)

        os.makedirs(args.out, exist_ok=True)
        path = os.path.join(args.out, f"{mid}.json")
        with open(path, "w") as f:
            json.dump(story, f, indent=2)
        print(f"saved {path} — {story['champion']} "
              f"{story['stats']['kills']}/{story['stats']['deaths']}/"
              f"{story['stats']['assists']} "
              f"({'W' if story['win'] else 'L'}, {story['duration_min']}min)")


if __name__ == "__main__":
    main()
