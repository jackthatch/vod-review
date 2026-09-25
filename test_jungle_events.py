#!/usr/bin/env python3
"""Smoke-test jungle_events.py against a synthetic but targeted fixture.

No Riot key in this environment, so we build a timeline engineered to trigger
each detector exactly once and assert the classification:

  * a converted gank by the BLUE jungler (kill in mid, victim died in lane)
  * a converted COUNTER-gank by the RED jungler (both junglers present)
  * a lane visit by the blue jungler with no kill (attempt proxy)
  * an invade window: the RED jungler inside the BLUE half's jungle
"""

import board
import jungle_events as je

TEAM_BLUE, TEAM_RED = 100, 200

CHAMPIONS = ["Graves", "Jax", "Ahri", "Jinx", "Thresh",
             "LeeSin", "Darius", "Syndra", "Caitlyn", "Nautilus"]
ROLES = ["JUNGLE", "TOP", "MIDDLE", "BOTTOM", "UTILITY",
         "JUNGLE", "TOP", "MIDDLE", "BOTTOM", "UTILITY"]

# Coordinates (verified against board._lane / jungle_events._half):
BLUE_JUNGLE_OWN = (8000, 4000)   # x+y=12000 -> blue half; _lane -> "jungle"
RED_JUNGLE_OWN = (6000, 9500)    # x+y=15500 -> red  half; _lane -> "jungle"
MID = (7000, 7000)               # _lane -> "mid"
TOP = (3000, 13000)              # _lane -> "top"
BOT = (12000, 3000)              # _lane -> "bot"

N_FRAMES = 10


def make_match():
    parts = []
    for i in range(10):
        team = TEAM_BLUE if i < 5 else TEAM_RED
        parts.append({
            "participantId": i + 1,
            "puuid": f"puuid-{i+1}",
            "championName": CHAMPIONS[i],
            "teamId": team,
            "teamPosition": ROLES[i],
            "summoner1Id": 12 if ROLES[i] == "TOP" else 4,
            "summoner2Id": 11 if ROLES[i] == "JUNGLE" else 6,
            "kills": 1, "deaths": 1, "assists": 2,
        })
    return {"metadata": {"matchId": "NA1_JE1"}, "info": {"participants": parts}}


def _pos(pid, minute):
    """Frame position for a participant at a given minute (engineered)."""
    role = ROLES[pid - 1]
    if role == "TOP":
        return TOP
    if role == "BOTTOM":
        return BOT
    if role == "UTILITY":
        return BOT
    if role == "MIDDLE":
        return MID
    # junglers
    if pid == 1:                      # blue jungler, Graves
        return TOP if minute == 2 else BLUE_JUNGLE_OWN
    if pid == 6:                      # red jungler, LeeSin
        return BLUE_JUNGLE_OWN if minute == 1 else RED_JUNGLE_OWN
    return BLUE_JUNGLE_OWN


def make_frame(i):
    pf = {}
    for pid in range(1, 11):
        x, y = _pos(pid, i)
        pf[str(pid)] = {
            "participantId": pid,
            "position": {"x": x, "y": y},
            "totalGold": 3000 + i * 500 + pid * 10,
            "currentGold": 200 + i * 50,
            "level": 4 + i,
            "xp": 1000 + i * 500,
            "minionsKilled": 20 + i * 5,
            "jungleMinionsKilled": 6 if ROLES[pid - 1] == "JUNGLE" else 0,
        }
    return {"participantFrames": pf, "events": []}


def make_timeline():
    frames = [make_frame(i) for i in range(N_FRAMES)]
    # minute 4: converted gank by BLUE jungler (Graves, pid 1) onto red mid (pid 8)
    frames[4]["events"] = [
        {"timestamp": 4 * 60000, "type": "CHAMPION_KILL", "killerId": 1, "victimId": 8,
         "assistingParticipantIds": [], "position": {"x": MID[0], "y": MID[1]}},
    ]
    # minute 6: counter-gank — RED jungler (LeeSin, pid 6) kills blue mid (pid 3),
    # blue jungler (pid 1) assists => both junglers present
    frames[6]["events"] = [
        {"timestamp": 6 * 60000, "type": "CHAMPION_KILL", "killerId": 6, "victimId": 3,
         "assistingParticipantIds": [1], "position": {"x": MID[0], "y": MID[1]}},
    ]
    return {"info": {"frameInterval": 60000, "frames": frames}}


def main():
    b = board.extract_board(make_match(), make_timeline(), "puuid-1")
    res = je.detect(b)

    ganks = res["ganks"]
    assert len(ganks) == 2, ganks

    # the blue jungler's gank (minute 4, no counter-gank)
    g_blue = next(g for g in ganks if g["ganker_team"] == TEAM_BLUE)
    assert g_blue["min"] == 4.0, g_blue
    assert g_blue["lane"] == "mid", g_blue
    assert g_blue["victim_champion"] == "Syndra", g_blue
    assert g_blue["counter_gank"] is False, g_blue

    # the red jungler's counter-gank (minute 6, both junglers involved)
    g_red = next(g for g in ganks if g["ganker_team"] == TEAM_RED)
    assert g_red["min"] == 6.0, g_red
    assert g_red["counter_gank"] is True, g_red

    # lane visit proxy: blue jungler sat in top at minute 2, no kill followed
    visits = [v for v in res["lane_visits"] if v["jungler_team"] == TEAM_BLUE]
    assert len(visits) == 1, res["lane_visits"]
    assert visits[0]["lane"] == "top", visits[0]
    assert visits[0]["min"] == 2.0, visits[0]
    assert visits[0]["kill_within_window"] is False, visits[0]

    # invade: red jungler inside blue half's jungle at minute 1
    iv = [w for w in res["invades"] if w["jungler_team"] == TEAM_RED]
    assert len(iv) == 1, res["invades"]
    assert iv[0]["start_min"] == 1.0, iv[0]
    # blue jungler never crossed into red jungle
    assert not [w for w in res["invades"] if w["jungler_team"] == TEAM_BLUE]

    s = res["summary"]
    assert s["me"]["gank_kills"] == 1, s
    assert s["me"]["lane_visits_proxy"] == 1, s
    assert s["me"]["invade_windows"] == 0, s
    assert s["enemy_jungler"]["gank_kills"] == 1, s
    assert s["enemy_jungler"]["invade_windows"] == 1, s
    assert "caveat" in res and "PROXY" in res["caveat"]

    print("jungle_events.py smoke test PASSED")
    import json
    print(json.dumps(s, indent=2, default=str))


if __name__ == "__main__":
    main()
