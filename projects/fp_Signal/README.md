# Signal

A personal agent that pulls deep-layer AI/tech news from curated sources, synthesizes it with an LLM, and emails me a daily digest.

Built as the final project for OIM3640 (Spring 2026, Babson College).

See [`proposal.md`](proposal.md) for goals, MVP scope, and stretch goals.

## Status

**Phase 3a complete** — GitHub Trending added as second source  
Phase 3b — arXiv cs.AI RSS  
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

## How it works (Phase 3a)

1. **Hacker News** — Algolia API, last 24h, ≥ 30 pts, AI keyword filter
2. **GitHub Trending** — scrapes daily + weekly trending, filters by AI keywords in name/description; falls back to all trending if < 5 match
3. All candidates merged and passed to **DeepSeek** (`deepseek-chat`) via OpenAI-compatible API
4. DeepSeek picks 5–7 items that are productivity-relevant (new tools, releases, fast-rising repos, tutorials) and discards noise
5. Each pick gets a ≤25-word `why_it_matters` note; email shows source label and appropriate metadata (HN pts / GitHub stars)
