# Signal

A personal agent that pulls deep-layer AI/tech news from curated sources, synthesizes it with an LLM, and emails me a daily digest.

Built as the final project for OIM3640 (Spring 2026, Babson College).

See [`proposal.md`](proposal.md) for goals, MVP scope, and stretch goals.

## Status

**Phase 2 complete** — DeepSeek-filtered digest with per-item analysis  
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
| `RECIPIENT_EMAIL` | Where to deliver the digest |
| `DEEPSEEK_API_KEY` | DeepSeek API key from [platform.deepseek.com](https://platform.deepseek.com) |

## How it works (Phase 2)

1. Hits the HN Algolia API (`search_by_date`) for stories in the last 24h with ≥ 30 points
2. Keyword-filters to AI-related titles (word-boundary matching for short terms like `ai`, `llm`, `rag`)
3. Passes all candidates to DeepSeek (`deepseek-chat`) via the OpenAI-compatible API
4. DeepSeek picks 5–7 items that are actually useful (new tools, releases, tutorials) and discards noise (pricing debates, funding news, philosophy threads)
5. Each pick gets a ≤25-word `why_it_matters` note
6. Renders as HTML email and sends via Gmail SMTP SSL
