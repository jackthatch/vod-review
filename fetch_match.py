#!/usr/bin/env python3
"""
fetch_match.py — pull your LoL match history + timeline via the Riot API,
condense it into an LLM-ready "story" of the game.

Usage:
    export RIOT_API_KEY=RGAPI-xxxx
    python fetch_match.py --name "YourName" --tag "NA1" --region na1 --count 5

Output: JSON per match (raw + condensed) under ./data/<match_id>/
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
        self.platform = region          # e.g. na1
        self.region = REGION_ROUTING.get(region, region)  # e.g. americas
        self.platform_host = f"https://{self.platform}.api.riotgames.com"
        self.region_host = f"https://{self.region}.api.riotgames.com"

    def _get(self, host, path):
        r = requests.get(f"{host}{path}", headers={"X-Riot-Token": self.key})
        if r.status_code == 429:  # rate limit — back off
            retry = int(r.headers.get("Retry-After", 1))
            time.sleep(retry)
            return self._get(host, path)
        r.raise_for_status()
        return r.json()

    def puuid(self, name, tag):
        # RiotID uses tagline; strip '#' if the user passes "name#TAG"
        if "#" in name:
            name, tag = name.split("#", 1)
        p = self._get(
            self.platform_host,
            f"/riot/account/v1/accounts/by-riot-id/{quote(name)}/{quote(tag)}",
        )
        return p["puuid"]

    def match_ids(self, puuid, count):
        ids = self._get(
            self.region_host,
            f"/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count={count}",
        )
        return ids

    def timeline(self, match_id):
        return self._get(
            self.region_host, f"/lol/match/v5/matches/{match_id}/timeline"
        )

    def match(self, match_id):
        return self._get(
            self.region_host, f"/lol/match/v5/matches/{match_id}"
        )


def condense(match, timeline, puuid):
    """Turn raw match+timeline into a compact, LLM-friendly narrative."""
    # identify our participant index
    participants = match["info"]["participants"]
    me = next(p for p in participants if p["puuid"] == puuid)
    my_team = me["teamId"]
    duration_min = round(timeline["info"]["frameInterval"] *
                         len(timeline["info"]["frames"]) / 60000, 1)

    frames = timeline["info"]["frames"]
    events = []
    for ev in timeline["info"]["events"]:
        t = ev["timestamp"]  # ms
        minute = t // 60000
        sec = (t % 60000) // 1000
        ts = f"{minute:02d}:{sec:02d}"

        # only keep events that involve our team or objectives
        if ev["type"] == "CHAMPION_KILL":
            k = ev.get("killerId", 0)
            v = ev.get("victimId", 0)
            aid = ev.get("assistingParticipantIds", [])
            mine = k in (p["participantId"] for p in participants if p["teamId"] == my_team) or \
                   v in (p["participantId"] for p in participants if p["teamId"] == my_team)
            if mine:
                events.append(f"[{ts}] KILL — killer={k} victim={v} assists={aid}")
        elif ev["type"] == "ITEM_PURCHASED":
            pid = ev["participantId"]
            if pid == me["participantId"]:
                events.append(f"[{ts}] bought item {ev['itemId']}")
        elif ev["type"] == "SKILL_LEVEL_UP":
            if ev["participantId"] == me["participantId"]:
                events.append(f"[{ts}] leveled {ev['skillSlot']}")
        elif ev["type"] == "BUILDING_KILL":
            team = ev.get("teamId")
            if team in (my_team, None) or ev.get("killerId") in \
               [p["participantId"] for p in participants if p["teamId"] == my_team]:
                events.append(f"[{ts}] {ev['buildingType']} destroyed (team {team})")
        elif ev["type"] == "ELITE_MONSTER_KILL":
            events.append(f"[{ts}] {ev['monsterType']} killed by team {ev.get('killerTeamId')}")

    # my per-frame snapshot (position, gold, level, cs) every ~minute
    my_snapshots = []
    for i, f in enumerate(frames):
        pf = f["participantFrames"].get(str(me["participantId"]))
        if pf and i % 2 == 0:  # every ~60s
            my_snapshots.append({
                "min": i,  # approx minute
                "gold": pf["totalGold"],
                "level": pf["level"],
                "cs": pf["minionsKilled"] + pf["jungleMinionsKilled"],
                "x": pf["position"]["x"],
                "y": pf["position"]["y"],
            })

    return {
        "match_id": match["metadata"]["matchId"],
        "champion": me["championName"],
        "lane": me.get("lane", "?"),
        "role": me.get("role", "?"),
        "kda": f"{me['kills']}/{me['deaths']}/{me['assists']}",
        "cs": me.get("totalMinionsKilled", 0),
        "gold": me.get("goldEarned", 0),
        "win": me["win"],
        "duration_min": duration_min,
        "opponent_champion": _opponent(match, me),
        "events": events,
        "my_snapshots": my_snapshots,
    }


def _opponent(match, me):
    for p in match["info"]["participants"]:
        if p["teamId"] != me["teamId"] and p.get("lane") == me.get("lane"):
            return p["championName"]
    return "?"


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
        print(f"saved {path} — {story['champion']} {story['kda']} "
              f"({'W' if story['win'] else 'L'}, {story['duration_min']}min)")


if __name__ == "__main__":
    main()
