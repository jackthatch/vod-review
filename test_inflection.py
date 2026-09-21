#!/usr/bin/env python3
"""Smoke-test inflection.py against a hand-built board (same shape as
board.extract_board output). Exercises all four detectors with a synthetic
scenario, then asserts each fires at the expected timestamp."""

import json

import inflection
from board import OBJECTIVE_POS

TEAM_BLUE, TEAM_RED = 100, 200


def _player(pid, team, role, is_me=False):
    return {
        "champion": f"Champ{pid}",
        "team": team,
        "role": role,
        "is_me": is_me,
        "summoners": [11, 4] if role == "JUNGLE" else [4, 6],
        "has_flash": True,
        "has_tp": role == "TOP",
        "has_smite": role == "JUNGLE",
    }


def make_board():
    roles = {1: "JUNGLE", 2: "TOP", 3: "MID", 4: "BOTTOM", 5: "UTILITY",
             6: "JUNGLE", 7: "TOP", 8: "MID", 9: "BOTTOM", 10: "UTILITY"}
    players = {pid: _player(pid, TEAM_BLUE if pid <= 5 else TEAM_RED,
                            roles[pid], is_me=(pid == 1))
               for pid in range(1, 11)}

    # 8 frames at 60s = 0..7 min. Positions are hand-placed to trigger detectors.
    # Default: everyone farms mid-ish; overrides move "me" (pid 1) around.
    dragon = OBJECTIVE_POS["DRAGON"]

    def snap(minute, me_pos, me_unspent, near_pit=None):
        players_frame = {}
        for pid in range(1, 11):
            x, y, unspent = 7000, 7000, 300 + pid * 10
            if near_pit and pid in near_pit:
                x, y = dragon["x"], dragon["y"]
            players_frame[pid] = {
                "x": x, "y": y, "gold": 3000 + int(minute) * 500,
                "unspent": unspent, "level": 3 + int(minute),
                "xp": 1000, "cs": 20 + int(minute) * 5,
            }
        players_frame[1] = {"x": me_pos[0], "y": me_pos[1], "gold": 3500,
                            "unspent": me_unspent, "level": 4, "xp": 1200, "cs": 25}
        return {"min": minute, "players": players_frame}

    snapshots = [
        snap(0, (7000, 7000), 200),          # me mid
        snap(1, (4000, 12000), 500),         # me rotated top (mid -> top)
        snap(2, (4000, 12000), 800),         # me still top
        snap(3, (1000, 1000), 100),          # me recalled to base, spent 700g
        snap(4, (12000, 3000), 150),         # me rotated bot (base -> bot)
        snap(5, (dragon["x"], dragon["y"]), 300, near_pit={1, 3, 4, 5}),
        snap(6, (dragon["x"], dragon["y"]), 400, near_pit={1, 3, 4, 5}),
        snap(7, (7000, 7000), 500),          # me back mid
    ]

    events = [
        # a teamfight: kill with 3 assists at 2min
        {"min": 2.0, "type": "CHAMPION_KILL", "killer": 1, "victim": 6,
         "assists": [3, 4, 5], "x": 4000, "y": 12000},
        # dragon secured by blue at 5.5min (contest detected via near_pit frames)
        {"min": 5.5, "type": "ELITE_MONSTER_KILL", "monster": "DRAGON",
         "sub": "FIRE_DRAGON", "team": TEAM_BLUE, "killer": 1,
         "x": dragon["x"], "y": dragon["y"]},
    ]

    return {
        "match_id": "NA1_999",
        "duration_min": 7.0,
        "frame_interval": 60000,
        "me_id": 1,
        "players": players,
        "snapshots": snapshots,
        "events": events,
    }


def main():
    bd = make_board()
    ips = inflection.analyze(bd)

    by_type = {}
    for ip in ips:
        by_type.setdefault(ip["type"], []).append(ip)

    # objective contest: 4 champs near dragon from frame 5 (5.0min), secured 5.5
    assert "objective_contest" in by_type, f"missing objective_contest in {ips}"
    oc = by_type["objective_contest"][0]
    assert oc["min"] == 5.0, f"contest should start at 5.0min, got {oc['min']}"
    assert oc["objective"] == "DRAGON"

    # teamfight: kill at 2min with 3 assists
    assert "teamfight" in by_type, f"missing teamfight in {ips}"
    tf = by_type["teamfight"][0]
    assert tf["min"] == 2.0 and tf["participants"] == 5

    # rotations: only tactical lane moves count (base trips excluded)
    rots = by_type.get("rotation", [])
    assert len(rots) == 1, f"expected 1 tactical rotation, got {rots}"
    assert (rots[0]["from"], rots[0]["to"]) == ("mid", "top")

    # recall: me at base with unspent dropping 800 -> 100 at 3min
    recalls = by_type.get("recall_buy", [])
    assert len(recalls) == 1, f"expected 1 recall, got {recalls}"
    assert recalls[0]["min"] == 3.0 and recalls[0]["gold_spent"] == 700

    # chronological ordering
    mins = [ip["min"] for ip in ips]
    assert mins == sorted(mins), "inflection points must be chronological"

    print("inflection.py smoke test PASSED")
    print(f"\n--- {len(ips)} inflection points ---")
    print(inflection.report(bd, ips))


if __name__ == "__main__":
    main()
