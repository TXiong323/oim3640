# Signal

A personal agent that pulls deep-layer AI/tech news from curated sources, synthesizes it with an LLM, and emails me a daily digest.

Built as the final project for OIM3640 (Spring 2026, Babson College).

See [`proposal.md`](proposal.md) for goals, MVP scope, and stretch goals.

## Status

**Phase 3b complete** — arXiv cs.AI + cs.CL added as third source  
Phase 3c — Anthropic / OpenAI blog RSS  
Phase 3d — Product Hunt  
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
| `RECIPIENT_EMAIL` | Where to deliver the digest |
| `DEEPSEEK_API_KEY` | DeepSeek API key from [platform.deepseek.com](https://platform.deepseek.com) |

## How it works (Phase 3b)

1. **Hacker News** — Algolia API, last 24h, ≥ 30 pts, AI keyword filter
2. **GitHub Trending** — scrapes daily + weekly trending, filters by AI keywords in name/description; falls back to all trending if < 5 match
3. **arXiv** — parses `cs.AI` and `cs.CL` RSS feeds, keyword-filters to ≤ 20 practitioner-relevant papers (agents, tools, reasoning, RAG, etc.)
4. All candidates merged (~45 total) and passed to **DeepSeek** (`deepseek-chat`) via OpenAI-compatible API
5. DeepSeek picks 5–7 items across all three sources; discards noise (pricing, politics, pure theory, games/entertainment)
6. Each pick gets a ≤40-char Chinese `why_it_matters` note (technical terms stay in English)
7. Email shows source label + appropriate metadata per source (HN: pts/comments; GitHub: stars; arXiv: authors/category)
