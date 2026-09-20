#!/usr/bin/env python3
"""Smoke-test board.py against a synthetic match+timeline fixture.

There is no Riot API key in this environment, so this builds a minimal-but-
realistic fixture matching the documented MATCH-V5 schema and asserts the
extractor + situation builder run and produce sane output. The real-field-name
check still needs one live run (see board.py header).
"""

import json

import board

TEAM_BLUE, TEAM_RED = 100, 200

CHAMPIONS = ["Graves", "Jax", "Ahri", "Jinx", "Thresh",
             "LeeSin", "Darius", "Syndra", "Caitlyn", "Nautilus"]
ROLES = ["JUNGLE", "TOP", "MIDDLE", "BOTTOM", "UTILITY",
         "JUNGLE", "TOP", "MIDDLE", "BOTTOM", "UTILITY"]


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
            "summoner1Id": 12 if ROLES[i] == "TOP" else 4,   # top has TP
            "summoner2Id": 11 if ROLES[i] == "JUNGLE" else 6,  # jungle has smite
            "kills": 1, "deaths": 1, "assists": 2,
        })
    return {"metadata": {"matchId": "NA1_999"}, "info": {"participants": parts}}


def make_frame(i):
    pf = {}
    for pid in range(1, 11):
        team = TEAM_BLUE if pid <= 5 else TEAM_RED
        # put top laners in top lane (high y), bot laners in bot (low y)
        if ROLES[pid - 1] == "TOP":
            x, y = 3000, 13000
        elif ROLES[pid - 1] == "BOTTOM":
            x, y = 12000, 3000
        else:
            x, y = 7000, 7000
        pf[str(pid)] = {
            "participantId": pid,
            "position": {"x": x, "y": y},
            "totalGold": 3000 + i * 500 + pid * 10,
            "currentGold": 200 + i * 50,
            "level": 3 + i,
            "xp": 1000 + i * 500,
            "minionsKilled": 20 + i * 5,
            "jungleMinionsKilled": 6 if ROLES[pid - 1] == "JUNGLE" else 0,
        }
    return {"participantFrames": pf, "events": []}


def make_timeline():
    frames = [make_frame(i) for i in range(4)]
    # sprinkle a few events into the frames (current API embeds events per-frame)
    frames[1]["events"] = [
        {"timestamp": 90000, "type": "ITEM_PURCHASED", "participantId": 1, "itemId": 1055},
        {"timestamp": 95000, "type": "CHAMPION_KILL", "killerId": 1, "victimId": 6,
         "assistingParticipantIds": [3], "position": {"x": 7000, "y": 7000}},
    ]
    frames[2]["events"] = [
        {"timestamp": 150000, "type": "ELITE_MONSTER_KILL", "monsterType": "DRAGON",
         "monsterSubType": "FIRE_DRAGON", "killerTeamId": TEAM_BLUE, "killerId": 1,
         "position": {"x": 9866, "y": 4414}},
        {"timestamp": 160000, "type": "BUILDING_KILL", "buildingType": "TOWER_BUILDING",
         "towerType": "OUTER_TURRET", "laneType": "BOT_LANE", "teamId": TEAM_RED,
         "killerId": 4, "position": {"x": 12000, "y": 3000}},
    ]
    return {"info": {"frameInterval": 60000, "frames": frames}}


def main():
    match = make_match()
    tl = make_timeline()
    b = board.extract_board(match, tl, "puuid-1")

    assert b["match_id"] == "NA1_999"
    assert len(b["players"]) == 10
    assert b["me_id"] == 1
    assert b["players"][1]["is_me"] is True
    assert b["players"][2]["has_tp"] is True      # Jax (top) has TP
    assert b["players"][1]["has_smite"] is True   # Graves (jungle) has smite
    assert len(b["snapshots"]) == 4
    assert len(b["snapshots"][0]["players"]) == 10

    # events were flattened across frames
    kinds = [e["type"] for e in b["events"]]
    assert "ITEM_PURCHASED" in kinds
    assert "CHAMPION_KILL" in kinds
    assert "ELITE_MONSTER_KILL" in kinds
    assert "BUILDING_KILL" in kinds

    # situation fact-sheet at 3min
    sit = board.situation_at(b, 3.0)
    assert sit["dragon_counts"][TEAM_BLUE] == 1
    assert sit["dragon_counts"][TEAM_RED] == 0
    assert len(sit["players"]) == 10

    # the top laners should bucket to "top", bot laners to "bot"
    by_role = {p["role"]: p for p in sit["players"]}
    assert by_role["TOP"]["lane"] == "top"
    assert by_role["BOTTOM"]["lane"] == "bot"

    # the killed enemy jungler (pid 6, died at 1.6min) should be marked dead at
    # 1.8min (respawn ~20s), but back alive by 3.0min
    sit_early = board.situation_at(b, 1.8)
    p6_early = next(p for p in sit_early["players"] if p["participant_id"] == 6)
    assert p6_early["likely_dead"] is True
    p6_late = next(p for p in sit["players"] if p["participant_id"] == 6)
    assert p6_late["likely_dead"] is False

    print("board.py smoke test PASSED")
    print("\n--- sample situation_at(3.0) ---")
    print(json.dumps(sit, indent=2, default=str))


if __name__ == "__main__":
    main()
