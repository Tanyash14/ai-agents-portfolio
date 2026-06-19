# Week 4 — Custom SQL-Gen Model (Fine-tuning)

Fine-tune a small open model via QLoRA on text-to-SQL pairs written against **a real-looking
DE schema** (star schema: fact_orders, dim_customers, dim_products, etc. — or your actual
warehouse schema, sanitized).

## Problem it solves
Generic text-to-SQL models don't know your table names, join keys, or business logic
("active customer" might mean something specific to your company). Fine-tuning on
domain-specific pairs makes the model useful for *your* warehouse, not a generic demo schema.

## What it does
- Define a realistic star-schema warehouse (or use your actual one, sanitized)
- Build 100-300 (question, SQL) pairs covering common analyst questions against that schema
- Fine-tune a small open model (Qwen2.5-Coder 1.5B/7B or similar) with QLoRA on free Colab GPU
- Compare base model vs fine-tuned model on a held-out test set of questions
- Deploy the fine-tuned model locally via Ollama

## Why this is a strong resume project for a Data Engineer
Per 2026 hiring data, fine-tuning skill (LoRA/QLoRA) adds real comp premium on top of base
DE skills, specifically because most DE/AI hybrids never go past calling an API. Showing you
understand *when* fine-tuning beats prompting (and can actually do it) is a differentiator,
not just a checkbox.

## Status
🔲 Day 1: Fine-tuning theory — full FT vs LoRA vs QLoRA, when each makes sense
🔲 Day 2: Build the schema + generate/write text-to-SQL training pairs
🔲 Day 3: QLoRA fine-tuning run on Colab (free tier)
🔲 Day 4: Evaluate before/after on held-out questions, iterate on data quality
🔲 Day 5: Deploy fine-tuned model locally via Ollama
🔲 Day 6: README documenting tradeoffs observed (cost, accuracy gain, latency), GitHub

