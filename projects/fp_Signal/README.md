# Signal

A personal agent that pulls deep-layer AI/tech news from curated sources, synthesizes it with an LLM, and emails me a daily digest.

Built as the final project for OIM3640 (Spring 2026, Babson College).

See [`proposal.md`](proposal.md) for goals, MVP scope, and stretch goals.

## Status

**Phase 1 complete** — Hacker News fetch + HTML email via Gmail SMTP  
Phase 2 — DeepSeek analysis (next)  
Phase 3 — Additional sources (GitHub Trending, arXiv, blogs, Product Hunt)  
Phase 4 — GitHub Actions cron

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env   # fill in real values
python main.py
```

## Environment variables

| Variable | Description |
|---|---|
| `GMAIL_ADDRESS` | Your Gmail address used to send |
| `GMAIL_APP_PASSWORD` | [Gmail App Password](https://myaccount.google.com/apppasswords) (not your regular password) |
| `TO_EMAIL` | Where to deliver the digest |

## How it works (Phase 1)

1. Hits the HN Algolia API (`search_by_date`) for stories in the last 24 hours with ≥ 50 points
2. Filters to AI-related titles using keyword matching (word-boundary for short terms like `ai`, `llm`, `rag`)
3. Renders results as a simple HTML email sorted by score
4. Sends via Gmail SMTP SSL
