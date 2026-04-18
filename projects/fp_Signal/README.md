# Signal

A personal agent that pulls deep-layer AI/tech news from curated sources, synthesizes it with an LLM, and emails me a daily digest.

Built as the final project for OIM3640 (Spring 2026, Babson College).

See [`proposal.md`](proposal.md) for goals, MVP scope, and stretch goals.

## Status

Under active development. Building iteratively, one source at a time.

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env   # then fill in the real values
python main.py
```