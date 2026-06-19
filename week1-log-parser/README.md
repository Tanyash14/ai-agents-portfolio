# Week 1 — Smart Log Parser

Turn raw, messy application logs into structured, classified, summarized incident reports
using an LLM with structured outputs.

## Problem it solves
Engineers waste time manually scanning logs to find what actually went wrong. This tool
reads raw log lines, classifies each into an error category, and produces a daily incident
summary.

## What it does
- Ingests a log file (plain text, one or more lines per event)
- For each error-level event, calls an LLM to classify severity + category + likely cause
- Returns structured JSON (not free text) per event
- Produces a daily rollup summary: top error categories, anomaly count, suggested priority

## Status
🔲 Day 1: Tokens/context/pricing exploration
🔲 Day 2: First prompts + API setup
🔲 Day 3: Structured outputs (Pydantic schema)
🔲 Day 4: Ingestion + classification pipeline
🔲 Day 5: Summarization + anomaly flagging
🔲 Day 6: Polish + docs

## Setup
```bash
pip install -r requirements.txt
```

## Usage
```bash
python parse_logs.py sample_logs.txt
```
