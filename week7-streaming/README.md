# Week 7 — Live Viewing Events Pipeline (Streaming + Anomaly Detection)

A real-time streaming pipeline that ingests simulated "viewing events" (Netflix-style:
play, pause, buffer, stop events), processes them with Spark Structured Streaming on
Databricks, lands them in a Delta Lake table, and runs an LLM agent that watches
rolling metrics to flag anomalies (CDN issues, regional outages, bot traffic) in
near-real-time — reusing your Week 1 classification logic and Week 3 agent patterns.

## Business scenario
A streaming platform needs to catch problems within minutes, not in next-day batch
reports: a sudden drop in successful plays (possible CDN failure), a spike in buffer
events in one region (possible regional outage), or an unusual viewing pattern
(possible bot/fraud traffic). This pipeline simulates that real-time monitoring layer.

## Why this project matters for your resume
This is the project that explicitly covers the keywords most DE/AI postings (including
OpenAI's) call out by name: **Kafka, Spark Structured Streaming, Databricks, Delta
Lake, distributed processing, real-time/streaming systems** — none of your other
6 weeks touch streaming, so this closes that gap directly.

## Stack
- **Redpanda** (Kafka-compatible, much easier to run locally than real Kafka) — event ingestion
- **Spark Structured Streaming** — consume the stream, compute rolling-window aggregations
- **Databricks Community Edition** (free tier) — where the Spark job actually runs, since
  this is the real Databricks experience expected on a resume, not just local PySpark
- **Delta Lake** — the table format Databricks is built around; very resume-relevant on its own
- LLM anomaly agent — reuses Week 1's structured-output classification pattern and
  Week 3's agentic reasoning loop, applied to streaming metrics instead of logs

## What it does
1. A Python producer simulates viewing events (user_id, content_id, region, event_type:
   play/pause/buffer/stop, timestamp) and pushes them to a Redpanda topic
2. Spark Structured Streaming consumes the topic, computes rolling-window metrics per
   region (plays/min, buffer-rate/min, unique active users/min)
3. Aggregated metrics are written to a Delta table (the "current state" of the platform)
4. An LLM agent periodically reads the latest aggregated metrics, compares against
   recent baseline, and reasons about whether a deviation is a real incident worth
   flagging — not just a hardcoded threshold alert, but an explained judgment call
   (e.g. "buffer rate in EU-WEST is 3x baseline — likely CDN issue, recommend escalation"
   vs. "slight dip in APAC plays, within normal evening pattern, no action needed")
5. Flagged anomalies are logged with the agent's reasoning chain (audit trail)

## Status
🔲 Day 1: Streaming concepts from zero — what's a topic, partition, consumer group,
   why streaming differs from batch (taught inline, no prior Kafka knowledge assumed)
🔲 Day 2: Set up Redpanda locally (Docker), write Python producer simulating events
🔲 Day 3: Databricks Community Edition setup + Spark Structured Streaming consumer,
   write rolling aggregations to a Delta table
🔲 Day 4: Refine aggregation logic — proper windowing (tumbling/sliding windows),
   watermarking for late data
🔲 Day 5: Build the LLM anomaly agent — reads Delta table state, reasons over
   deviations, explains its flagging decisions (reuses Week 1 Pydantic schema pattern)
🔲 Day 6: Polish, architecture diagram (producer → Redpanda → Spark → Delta → agent),
   README, demo, push to GitHub

## Setup (high-level, detailed steps provided when we reach Day 1)
```bash
# Redpanda via Docker (Kafka-compatible, simpler local setup)
docker run -d --name redpanda -p 9092:9092 redpandadata/redpanda start

# Databricks Community Edition: free signup at
# https://community.cloud.databricks.com/
```

## Why a Netflix-style domain for a generic skill
Even if you don't end up applying specifically to Netflix, "real-time viewing/event
analytics" is immediately legible to any interviewer — streaming, ad-tech, fintech,
and IoT companies all have nearly identical pipeline shapes (ingest → window-aggregate
→ detect → alert). The domain choice doesn't narrow the project; it makes it concrete.

