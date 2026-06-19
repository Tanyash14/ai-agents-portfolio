# Bonus — World Cup 2026 Live Insights Agent

A half-day mini-project: pull real, live FIFA World Cup 2026 data and generate
structured, LLM-powered daily insight reports — recap, upset alerts, and
standings notes.

Built as a fast follow to Week 1, reusing the same "structured LLM output"
pattern (Pydantic schema + prompt) applied to a different, fun, trending
data source.

## Why this exists
- Proves you can plug a real public API/data source into an LLM pipeline quickly
- Reinforces Week 1 skills (structured outputs) on new data
- Good "I built this in a day" portfolio piece / LinkedIn post material
- Not a substitute for the core 7-week DE-focused projects — this is a speed/initiative showcase

## Data source
[`openfootball/worldcup.json`](https://github.com/openfootball/worldcup.json) — free,
public domain (CC0), no API key required. Updated roughly daily by the maintainer
(not second-by-second live, but real and current).

```bash
curl https://raw.githubusercontent.com/openfootball/worldcup.json/master/2026/worldcup.json
```

## What it does
1. Fetches the live match JSON (fixtures + results)
2. Computes group standings via a small ETL aggregation (no LLM needed — deterministic
   math shouldn't go through an LLM, this is an important design lesson)
3. Sends recent match results to an LLM with a Pydantic-enforced JSON schema to generate:
   - A daily headline
   - Per-match insight (summary, upset flag, storyline)
   - A standings implications note

## Setup
```bash
pip install pydantic ollama
ollama pull llama3.1
ollama serve   # in a separate terminal
```

## Run
```bash
python worldcup_insights.py
```

## Design notes (the actual lesson here)
- **Not everything should go through an LLM.** Standings math is deterministic —
  computed with plain Python. Only the *interpretive* part (is this an upset? what's
  the storyline?) goes to the LLM. This is a real production pattern: use code for
  what code does well, LLMs for judgment/language tasks.
- Same Pydantic structured-output pattern as Week 1 — proof you can reuse a pattern
  across domains, which is exactly what "AI-native engineer" means in practice.
