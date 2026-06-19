# Week 2 — DE Knowledge Base Q&A Bot (RAG)

A RAG system over **your own data pipeline documentation** — dbt model docs, Airflow DAG
docstrings, runbooks, schema docs — so engineers can ask "why does fct_revenue depend on
stg_orders?" instead of grepping through YAML and Python files.

## Problem it solves
Data engineering knowledge is scattered across dbt `schema.yml` files, Airflow DAG
docstrings, Confluence pages, and tribal knowledge. New engineers (or you, six months from
now) waste hours tracing lineage and dependencies manually.

## What it does
- Ingests real DE artifacts: dbt `manifest.json`/model `.sql` + `.yml` files, Airflow DAG
  Python files (docstrings + task definitions), or markdown runbooks
- Chunks them in a way that respects structure (one chunk per dbt model, one per DAG task —
  not arbitrary character splits)
- Embeds + stores in ChromaDB
- Answers questions like "what does stg_orders feed into?" or "why did the revenue DAG fail
  last Tuesday?" by retrieving relevant docs + generating grounded answers
- Cites which file/model the answer came from (no hallucinated lineage)

## Why this is a strong resume project for a Data Engineer
This isn't a generic "chat with PDF" demo — it's RAG applied directly to dbt/Airflow
artifacts, which is exactly the "AI Data Engineer" skill gap postings describe: connecting
LLMs to existing pipeline infrastructure rather than building a toy chatbot.

## Status
🔲 Day 1: Embeddings + chunking theory — test on real dbt/Airflow files
🔲 Day 2: ChromaDB setup + basic retrieval
🔲 Day 3: Naive RAG end-to-end with citation of source file
🔲 Day 4: Hybrid search (keyword + vector) — important since model/table names need exact match too
🔲 Day 5: Build golden eval set: 15-20 real questions you'd actually ask about your pipelines
🔲 Day 6: Wrap in FastAPI, README, GitHub

## Data source options (pick what you have access to)
- Your real company dbt project (sanitize any sensitive info first) — best option
- Public dbt project: https://github.com/dbt-labs/jaffle-shop (great default if you don't
  have access to real dbt docs)
- Public Airflow example DAGs: https://github.com/apache/airflow/tree/main/airflow/example_dags

