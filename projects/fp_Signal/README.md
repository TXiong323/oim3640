# Signal

A personal agent that pulls deep-layer AI/tech news from curated sources, synthesizes it with an LLM, and emails me a daily digest.

Built as the final project for OIM3640 (Spring 2026, Babson College).

See [`proposal.md`](proposal.md) for goals, MVP scope, and stretch goals.

## Status

**Phase 3c complete** — Anthropic + OpenAI blogs added; vibe-coder filtering  
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

## How it works (Phase 3c)

1. **Hacker News** — Algolia API, last 24h, ≥ 30 pts, AI keyword filter
2. **GitHub Trending** — scrapes daily + weekly, filters by AI keywords; falls back to all trending if < 5 match
3. **Anthropic blog** — scrapes `anthropic.com/news`, last 7 days
4. **OpenAI blog** — RSS feed, last 7 days
5. All candidates merged (~30 total) and passed to **DeepSeek** (`deepseek-chat`)
6. DeepSeek filters for a vibe-coder audience: prioritizes usable tools, new model releases, MCP/Claude Code skills; discards academic papers, low-level dev tools, business news, games
7. Returns 3–6 picks; each gets a ≤40-char Chinese `why_it_matters` (technical terms in English) and a `display_title` with normalized brand capitalization
8. Email shows source + metadata per type (HN: pts/comments; GitHub: stars; blogs: date)
