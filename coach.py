#!/usr/bin/env python3
"""
coach.py — Layer 4: the AI coach.

Ties the deterministic pipeline (fetch -> condense -> board -> moments ->
inflection) to an LLM (OpenRouter) to produce a grounded, natural-language
VOD review for a single game:

  1. Game overview      — what happened, and the key points
  2. Deciding moments   — the 2-3 moments that decided the game
                          (what happened / why it went wrong / the alternative)
  3. Review plan        — what to actually watch, prioritized, and why
  4. Better decisions   — the calls you should have made vs. the ones you did

Design principle (VISION.md): detection is deterministic, explanation is
generative. Every stat and situation fed to the LLM is computed here from the
Riot timeline; the LLM only interprets, so it can never hallucinate a number.

Usage:
    export RIOT_API_KEY=... OPENROUTER_API_KEY=...
    python coach.py --name "YourName" --tag "NA1" --region na1 --count 3

    # review already-fetched raw JSON (from fetch_match.py --raw):
    python coach.py --raw-dir data/raw --match NA1_1234567890

Output: markdown review printed to stdout and saved to ./reviews/<match_id>.md
"""

import argparse
import json
import os
import sys
from urllib.parse import quote

import requests

import board as board_mod
import inflection as inflection_mod
import moments as moments_mod
from fetch_match import Riot, condense, REGION_ROUTING

# Default OpenRouter model for the coach. Strong reasoning + good prose.
DEFAULT_MODEL = "anthropic/claude-sonnet-4"

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


# ---------------------------------------------------------------------------
# Key loading (graceful: .env in the script dir works out of the box)
# ---------------------------------------------------------------------------

def _load_dotenv():
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass


def _require_env(name):
    val = os.environ.get(name)
    if not val:
        _load_dotenv()
        val = os.environ.get(name)
    if not val:
        sys.exit(f"Set {name} first (export {name}=...)")
    return val


# ---------------------------------------------------------------------------
# Context assembly — turn raw match+timeline into grounded facts for the LLM
# ---------------------------------------------------------------------------

def _fmt_time(minutes):
    """123.45 (min) -> '2:03'"""
    m = int(minutes)
    s = int(round((minutes - m) * 60))
    if s == 60:
        m, s = m + 1, 0
    return f"{m}:{s:02d}"


def _opponent_id(board):
    """Participant id of the enemy in my role (same teamPosition, other team)."""
    me = board["players"][board["me_id"]]
    for pid, pl in board["players"].items():
        if pl["team"] != me["team"] and pl["role"] == me["role"]:
            return pid
    # fallback: enemy jungler = the one with smite on the other team
    for pid, pl in board["players"].items():
        if pl["team"] != me["team"] and pl.get("has_smite"):
            return pid
    return None


def _level_curve(board, pid, at_minutes=(10, 20)):
    """Level + xp at given minutes for a participant (last snapshot <= t)."""
    out = {}
    snaps = board["snapshots"]
    for t in at_minutes:
        best = None
        for s in snaps:
            if s["min"] <= t:
                ps = s["players"].get(pid)
                if ps:
                    best = ps
            else:
                break
        if best:
            out[t] = {"level": best.get("level"), "cs": best.get("cs"),
                      "gold": best.get("gold"), "xp": best.get("xp")}
    return out


def build_context(match, timeline, puuid, top_moments=4, top_inflections=6,
                  overstay_gold=1000, range_units=3000):
    """Assemble the deterministic fact-sheet that grounds the LLM coach.

    Returns a dict that is JSON-serializable and reasonably compact.
    """
    bd = board_mod.extract_board(match, timeline, puuid)
    story = condense(match, timeline, puuid)  # me-only condensed view

    me_id = bd["me_id"]
    me = bd["players"][me_id]
    opp_id = _opponent_id(bd)

    # -- headline stats ------------------------------------------------
    s = story["stats"]
    dur = story["duration_min"] or 1.0
    overview = {
        "champion": story["champion"],
        "role": story["role"],
        "result": "win" if story["win"] else "loss",
        "duration_min": story["duration_min"],
        "opponent": story.get("opponent_champion"),
        "kda": f"{s['kills']}/{s['deaths']}/{s['assists']}",
        "cs": s["total_cs"],
        "cs_per_min": round(s["total_cs"] / dur, 1),
        "gold": s["gold"],
        "gold_per_min": round(s["gold"] / dur, 0),
        "first_clear_min": story.get("first_clear_min"),
        "kp": None,  # kill participation — computed below
    }

    # kill participation: (my kills + assists) / team kills
    my_kills = s["kills"] + s["assists"]
    team_kills = 0
    for pid, pl in bd["players"].items():
        if pl["team"] == me["team"]:
            # team kills come from the match participant list
            pass
    # simpler: total kills = sum of CHAMPION_KILL events by my team
    for ev in bd["events"]:
        if ev["type"] == "CHAMPION_KILL":
            killer = ev.get("killer")
            if killer is not None:
                kteam = bd["players"].get(killer, {}).get("team")
                if kteam == me["team"]:
                    team_kills += 1
    overview["kp"] = round(100.0 * my_kills / team_kills, 0) if team_kills else None

    # farming-vs-fighting split from the last snapshot
    last_snap = story["snapshots"][-1] if story["snapshots"] else {}
    td = last_snap.get("total_damage") or 0
    tdc = last_snap.get("damage_to_champions") or 0
    overview["champ_damage_ratio"] = round(100.0 * tdc / td, 1) if td else None

    # level / xp comparison vs opponent
    matchup = {}
    if opp_id is not None:
        my_curve = _level_curve(bd, me_id)
        op_curve = _level_curve(bd, opp_id)
        matchup = {
            "opponent_champion": bd["players"][opp_id]["champion"],
            "me": my_curve,
            "opponent": op_curve,
        }

    # -- objectives timeline -------------------------------------------
    objectives = []
    for o in story["objectives"]:
        objectives.append({
            "min": o["min"],
            "monster": board_mod.monster_label(o["type"], o.get("sub")),
            "sub": o.get("sub"),
            "team": "mine" if o.get("team") == me["team"] else "enemy",
            "smited_by_me": o.get("mine"),
        })

    # -- deaths timeline (compact) -------------------------------------
    deaths = [{"min": d["min"], "gold_held": d.get("current_gold")}
              for d in story["deaths"]]

    # -- pivotal moments (ranked) --------------------------------------
    ranked_moments = moments_mod.analyze(story, overstay_gold, range_units, 30, 6.0, bd)
    moments_out = []
    for m in ranked_moments[:top_moments]:
        # attach a full-board situation fact-sheet at each moment
        entry = {
            "min": m["min"],
            "type": m["type"],
            "detail": m["detail"],
            "score": m["score"],
            "situation": _trim_situation(board_mod.situation_at(bd, m["min"])),
        }
        if m.get("contest"):
            entry["contest"] = m["contest"]
        moments_out.append(entry)

    # -- inflection points (decisions) ---------------------------------
    inflections = inflection_mod.analyze(bd)
    inflections_out = []
    for ip in inflections[:top_inflections]:
        inflections_out.append({
            "min": ip["min"],
            "type": ip["type"],
            "detail": ip["detail"],
            "situation": _trim_situation(board_mod.situation_at(bd, ip["min"])),
        })

    return {
        "match_id": bd["match_id"],
        "overview": overview,
        "matchup": matchup,
        "objectives": objectives,
        "deaths": deaths,
        "pivotal_moments": moments_out,
        "inflections": inflections_out,
    }


def _trim_situation(sit, max_players=10):
    """Drop raw x/y from the situation fact-sheet (the LLM doesn't need them;
    keep lane, gold, level, fed, alive, distances)."""
    players = []
    for p in sit.get("players", [])[:max_players]:
        players.append({k: p[k] for k in
                        ("participant_id", "champion", "team", "role", "is_me",
                         "lane", "location", "gold", "level", "fed", "has_tp",
                         "likely_dead", "near_baron", "near_dragon") if k in p})
    return {
        "minute": sit.get("minute"),
        "gold_diff": sit.get("gold_diff"),
        "dragon_counts": sit.get("dragon_counts"),
        "players": players,
    }


# ---------------------------------------------------------------------------
# LLM coach
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """You are a high-ELO League of Legends coach reviewing a single
solo-queue game from the perspective of the jungler (the "player"). You are given
a deterministic fact-sheet computed from the Riot timeline — every number in it is
accurate; never invent or contradict a number that is given to you. If a fact is
missing (e.g. summoner cooldowns, exact wave state), hedge rather than assert.
Never quote raw map coordinates or distances (no "units", no x/y) — refer to
places by name: "mid lane", "your red buff", "at Dragon pit", "in the river".

Your job is to write a concise, actionable review in Markdown with exactly these
sections:

## Game overview
3-5 sentences: the shape of the game, who carried/inted, and the single most
important narrative thread. Reference the player's KDA/CS/gold and the matchup.

## Key points
A short bullet list (4-6) of the highest-signal facts: first-clear speed,
farming-vs-fighting split, level/gold vs. the enemy jungler, objective control,
death timing. Each bullet states the fact AND why it mattered.

## Deciding moments
For each pivotal moment given, one short paragraph answering three questions:
1. What happened (timestamp + event).
2. Why it went the way it did (underleveled, unspent gold, out of position,
   bad fight choice, or just a 50/50 that went the wrong way).
3. The alternative — the better play the player should have made instead.

## Review plan
A prioritized list (top 3) of the specific moments to actually rewatch in the
replay, in order of importance, each with a one-line "what to look for" and a
one-line "why this matters to your long-term improvement".

## Decisions to change
A short list of the concrete decisions the player made that were wrong, each
paired with the decision they should have made instead, phrased as
"Instead of X, you should have Y."

For objective moments (contested_objective / objective_contest), use the
`contest` block when present instead of raw distances. `team_committed: false`
means the team conceded (few allies at the pit) — that is often the CORRECT
play, not a mistake, so do NOT flag it as an error by default. Judge it against
context: a large gold deficit, allies dead, or a soul point you can't win all
justify giving an objective up. Only call it a mistake when contesting was
actually viable (numbers even/up AND you were in position), or when the team
could have PREPPED better — shoving side waves first and setting up vision so
the objective fight is winnable. If `soul_point` is true, treat it as
high-stakes. When you discuss wave/lane pressure, hedge: we infer it from player
positions, not exact wave states.

Be direct and specific. Use the player's champion name and the timestamps given.
Do not pad. Total output should be under ~700 words."""


def build_user_prompt(ctx):
    """Render the grounded fact-sheet as a compact JSON-ish block for the LLM."""
    return "Here is the deterministic fact-sheet for this game:\n\n" + \
        json.dumps(ctx, indent=2) + \
        "\n\nWrite the review now."


def call_llm(ctx, api_key, model=DEFAULT_MODEL, max_tokens=1600):
    """One OpenRouter chat completion. Returns the assistant text, or raises."""
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_user_prompt(ctx)},
        ],
        "max_tokens": max_tokens,
    }
    r = requests.post(
        OPENROUTER_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=120,
    )
    if r.status_code != 200:
        raise RuntimeError(f"OpenRouter {r.status_code}: {r.text[:300]}")
    data = r.json()
    return data["choices"][0]["message"]["content"]


def render_review(ctx, narrative):
    """Assemble the final markdown review (header + LLM narrative)."""
    ov = ctx["overview"]
    header = (
        f"# VOD review — {ov['champion']} ({ov['role']}) "
        f"{'WIN' if ov['result'] == 'win' else 'LOSS'}\n\n"
        f"**{ov['kda']}** · {ov['cs']} CS ({ov['cs_per_min']}/min) · "
        f"{ov['gold']}g · {ov['duration_min']}min · "
        f"vs {ov.get('opponent') or '?'}\n\n"
        f"---\n\n"
    )
    return header + narrative.strip() + "\n"


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _load_raw_or_fetch(riot, mid, raw_dir, puuid):
    """Return (match, timeline, puuid) — from raw dir if present, else fetch +
    persist to raw dir for cheap re-reviews."""
    raw_match_path = os.path.join(raw_dir, f"{mid}.match.json")
    raw_tl_path = os.path.join(raw_dir, f"{mid}.timeline.json")
    if os.path.exists(raw_match_path) and os.path.exists(raw_tl_path):
        with open(raw_match_path) as f:
            match = json.load(f)
        with open(raw_tl_path) as f:
            tl = json.load(f)
        if puuid is None:
            puuid = match["metadata"]["participants"][0]
        return match, tl, puuid

    match = riot.match(mid)
    tl = riot.timeline(mid)
    os.makedirs(raw_dir, exist_ok=True)
    with open(raw_match_path, "w") as f:
        json.dump(match, f)
    with open(raw_tl_path, "w") as f:
        json.dump(tl, f)
    return match, tl, puuid


def main():
    ap = argparse.ArgumentParser(description="AI VOD coach for a LoL match.")
    ap.add_argument("--name", help="your RiotID game name (e.g. 'YourName' or 'Name#TAG')")
    ap.add_argument("--tag", help="your RiotID tagline (after the #)")
    ap.add_argument("--region", default="na1",
                    help="platform region (na1, euw1, kr, ...)")
    ap.add_argument("--count", type=int, default=3,
                    help="how many recent matches to review (default 3)")
    ap.add_argument("--raw-dir", default="data/raw",
                    help="dir of raw match+timeline JSON from fetch_match.py --raw")
    ap.add_argument("--match", help="review a single match id (uses --raw-dir)")
    ap.add_argument("--out", default="reviews", help="output dir for .md reviews")
    ap.add_argument("--model", default=None,
                    help="OpenRouter model id (default: $OPENROUTER_MODEL or "
                         "anthropic/claude-sonnet-4)")
    ap.add_argument("--top-moments", type=int, default=4)
    ap.add_argument("--top-infs", type=int, default=6)
    ap.add_argument("--overstay-gold", type=int, default=1000)
    ap.add_argument("--range", type=int, default=3000)
    ap.add_argument("--print-only", action="store_true",
                    help="print to stdout but do not save to disk")
    args = ap.parse_args()

    riot_key = _require_env("RIOT_API_KEY")
    or_key = _require_env("OPENROUTER_API_KEY")

    # Model: explicit --model flag > OPENROUTER_MODEL env > default.
    model = args.model or os.environ.get("OPENROUTER_MODEL") or DEFAULT_MODEL

    # ---- resolve summoner (puuid) + match ids -----------------------------
    if args.match:
        # single-match review from raw dir (still need name/tag to mark is_me)
        match_ids = [args.match]
        puuid = None
        if args.name and args.tag:
            name, tag = args.name, args.tag
            if "#" in name:
                name, tag = name.split("#", 1)
            puuid = Riot(riot_key, args.region).puuid(name, tag)
    else:
        if not (args.name and args.tag):
            ap.error("need --name and --tag (or --match for a raw-dir review)")
        name, tag = args.name, args.tag
        if "#" in name:
            name, tag = name.split("#", 1)
        riot = Riot(riot_key, args.region)
        puuid = riot.puuid(name, tag)
        match_ids = riot.match_ids(puuid, args.count)

    riot = Riot(riot_key, args.region)
    os.makedirs(args.out, exist_ok=True)

    for mid in match_ids:
        match, tl, puuid = _load_raw_or_fetch(riot, mid, args.raw_dir, puuid)

        ctx = build_context(match, tl, puuid,
                            top_moments=args.top_moments,
                            top_inflections=args.top_infs,
                            overstay_gold=args.overstay_gold,
                            range_units=args.range)
        narrative = call_llm(ctx, or_key, model=model)
        review = render_review(ctx, narrative)

        print(review)
        print("=" * 72 + "\n")

        if not args.print_only:
            out_path = os.path.join(args.out, f"{mid}.md")
            with open(out_path, "w") as f:
                f.write(review)
            print(f"[saved {out_path}]\n")


if __name__ == "__main__":
    main()
