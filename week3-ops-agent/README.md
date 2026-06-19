# Week 3 — Data Pipeline Ops Agent

An agent that monitors **real Airflow DAG runs**, diagnoses failures using your Week 1
log-classification logic + Week 2 RAG knowledge base, and takes (initially mocked, later
real) remediation actions.

## Problem it solves
When a pipeline fails at 3am, an engineer has to: check Airflow UI → read logs → check
Slack/runbooks for past similar failures → decide whether to re-run, escalate, or fix
manually. This agent automates the diagnosis step and recommends (or takes) the right action.

## What it does
- Polls Airflow's REST API for failed/retrying DAG runs (use a local Airflow via
  `astro dev start` or `docker-compose`, or the public demo instance)
- For each failure: pulls the task log, classifies the error (reuses Week 1 logic),
  searches your Week 2 knowledge base for similar past incidents/runbook entries
- Reasons over both signals (ReAct-style: observe → think → act) to decide: auto-retry,
  page someone, or just log it as known/benign
- Executes the decided action via Airflow API (trigger re-run) or a mocked
  Slack/PagerDuty call
- Logs its reasoning chain so you can audit *why* it made each decision

## Why this is a strong resume project for a Data Engineer
This is the actual job description language from 2026 postings: "design autonomous agents
capable of reasoning, planning, and task execution" + "integrate LLMs, APIs, databases, and
external tools into agent workflows" — except applied to YOUR domain (pipeline ops) instead
of a generic customer-support bot. It demonstrates you can extend infrastructure you already
understand, not just call an LLM API.

## Status
🔲 Day 1: Agent patterns — ReAct, planning, tool use (theory + small demo)
🔲 Day 2: LangGraph basics — build a 2-node graph
🔲 Day 3: MCP fundamentals — wrap the Airflow API call as an MCP tool
🔲 Day 4: Build the diagnosis loop (observe failure → classify → retrieve similar past cases)
🔲 Day 5: Add the action layer (retry/escalate/log) + persistent state across runs
🔲 Day 6: Diagram the agent graph, README, GitHub

## Setup options for a local Airflow
- Easiest: `pip install apache-airflow` + `airflow standalone` (single command, local SQLite)
- More realistic: Astronomer's `astro dev start` (Docker-based, closer to production setups)
- If you have access to a real non-prod Airflow instance at work, even better — just don't
  commit any real credentials or proprietary DAG logic to the public repo

