"""
World Cup 2026 Live Insights Agent
-----------------------------------
Pulls real, public-domain World Cup 2026 match data (no API key needed),
classifies/summarizes it with an LLM using structured output, and prints
a daily insights report: results recap, upset alerts, and group standings.

Data source: https://github.com/openfootball/worldcup.json (CC0, public domain)
Note: data is updated ~daily by the maintainer, not second-by-second live.
"""

import json
import urllib.request
from collections import defaultdict
from datetime import datetime
from typing import Optional

from pydantic import BaseModel

DATA_URL = "https://raw.githubusercontent.com/openfootball/worldcup.json/master/2026/worldcup.json"


# ---------- Step 1: Fetch real data ----------

def fetch_worldcup_data() -> dict:
    """Pull the latest World Cup 2026 match data. No API key required."""
    with urllib.request.urlopen(DATA_URL, timeout=10) as response:
        return json.loads(response.read().decode())


# ---------- Step 2: Process into something useful ----------

def get_played_matches(data: dict) -> list[dict]:
    """Only matches that have a final score."""
    return [m for m in data["matches"] if "score" in m and "ft" in m.get("score", {})]


def get_upcoming_matches(data: dict, limit: int = 5) -> list[dict]:
    """Matches without a score yet, in schedule order."""
    return [m for m in data["matches"] if "score" not in m][:limit]


def build_group_standings(played: list[dict]) -> dict:
    """
    Compute simple group standings (W/D/L/Points/GD) from played matches.
    This is a real small ETL transform — flat match list -> aggregated table.
    """
    table = defaultdict(lambda: {"played": 0, "won": 0, "drawn": 0, "lost": 0,
                                   "gf": 0, "ga": 0, "points": 0})

    for m in played:
        group = m.get("group")
        if not group:
            continue
        t1, t2 = m["team1"], m["team2"]
        s1, s2 = m["score"]["ft"]

        table[(group, t1)]["played"] += 1
        table[(group, t2)]["played"] += 1
        table[(group, t1)]["gf"] += s1
        table[(group, t1)]["ga"] += s2
        table[(group, t2)]["gf"] += s2
        table[(group, t2)]["ga"] += s1

        if s1 > s2:
            table[(group, t1)]["won"] += 1
            table[(group, t1)]["points"] += 3
            table[(group, t2)]["lost"] += 1
        elif s2 > s1:
            table[(group, t2)]["won"] += 1
            table[(group, t2)]["points"] += 3
            table[(group, t1)]["lost"] += 1
        else:
            table[(group, t1)]["drawn"] += 1
            table[(group, t2)]["drawn"] += 1
            table[(group, t1)]["points"] += 1
            table[(group, t2)]["points"] += 1

    return table


def find_recent_results(played: list[dict], n: int = 5) -> list[dict]:
    """Most recent N played matches, sorted by date."""
    return sorted(played, key=lambda m: m["date"], reverse=True)[:n]


# ---------- Step 3: Structured LLM output (reuses Week 1 pattern) ----------

class MatchInsight(BaseModel):
    """Structured output schema for one match — same pattern as the
    log-classification schema from Week 1."""
    match: str
    result_summary: str
    is_upset: bool
    storyline: str


class DailyReport(BaseModel):
    date: str
    headline: str
    match_insights: list[MatchInsight]
    standings_note: str


def build_llm_prompt(recent: list[dict], standings_summary: str) -> str:
    """Construct the prompt — same structured-output pattern as Week 1's
    log parser, just pointed at a different domain."""
    matches_text = "\n".join(
        f"- {m['team1']} {m['score']['ft'][0]}-{m['score']['ft'][1]} {m['team2']} "
        f"({m.get('group', 'Knockout')}, {m['date']})"
        for m in recent
    )
    return f"""You are a sports data analyst. Given these recent World Cup 2026 results,
produce a structured daily report.

Recent results:
{matches_text}

Group standings context:
{standings_summary}

For each match, note:
- A one-line result summary
- Whether it was an "upset" (a lower-ranked or less-favored team won/drew unexpectedly)
- A one-sentence storyline (injuries, streaks, rivalries, etc. if inferable)

Also write one overall headline for the day and a note on standings implications.

Respond ONLY with valid JSON matching this schema:
{{
  "date": "...",
  "headline": "...",
  "match_insights": [
    {{"match": "...", "result_summary": "...", "is_upset": true/false, "storyline": "..."}}
  ],
  "standings_note": "..."
}}
"""


# ---------- Step 4: Wire it together (call your LLM of choice here) ----------

def generate_report_with_ollama(prompt: str, model: str = "llama3.1") -> Optional[DailyReport]:
    """
    Example using local Ollama. Swap this for the OpenAI client if you'd
    rather use gpt-4o-mini -- same prompt, different call.
    """
    import ollama
    response = ollama.chat(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        format="json",
    )
    raw = response["message"]["content"]
    return DailyReport.model_validate_json(raw)


def main():
    print("Fetching live World Cup 2026 data...")
    data = fetch_worldcup_data()

    played = get_played_matches(data)
    upcoming = get_upcoming_matches(data)
    recent = find_recent_results(played, n=5)
    standings = build_group_standings(played)

    print(f"\n{len(played)} matches played so far. {len(upcoming)} upcoming shown.\n")

    # Simple standings printout (no LLM needed for this part --
    # deterministic data shouldn't go through an LLM)
    print("=== Sample Group Standings ===")
    groups_seen = set()
    for (group, team), stats in sorted(standings.items()):
        if group in groups_seen and list(standings.keys()).index((group, team)) > 4:
            continue
        groups_seen.add(group)
        print(f"{group:10} {team:20} P{stats['played']} "
              f"W{stats['won']} D{stats['drawn']} L{stats['lost']} "
              f"Pts:{stats['points']}")

    standings_summary = "\n".join(
        f"{group} - {team}: {s['points']} pts" for (group, team), s in list(standings.items())[:10]
    )

    prompt = build_llm_prompt(recent, standings_summary)

    print("\n=== Generating LLM Daily Report ===")
    print("(requires `ollama pull llama3.1` and `ollama serve` running locally)")
    try:
        report = generate_report_with_ollama(prompt)
        print(json.dumps(report.model_dump(), indent=2))
    except Exception as e:
        print(f"LLM call skipped/failed ({e}). Here's the raw prompt that would be sent:\n")
        print(prompt)


if __name__ == "__main__":
    main()
