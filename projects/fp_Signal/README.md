# Signal

A personal agent that pulls deep-layer AI/tech news from curated sources, synthesizes it with an LLM, and emails me a daily digest.

Built as the final project for OIM3640 (Spring 2026, Babson College).

See [`proposal.md`](proposal.md) for goals, MVP scope, and stretch goals.

## Status

**Phase 3 complete** — all sources added (HN, Show HN, GitHub, Blogs, YouTube, Product Hunt)  
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
| `PRODUCTHUNT_CLIENT_ID` | From [api.producthunt.com/v2/oauth/applications](https://api.producthunt.com/v2/oauth/applications) |
| `PRODUCTHUNT_CLIENT_SECRET` | Same app registration page |

## How it works (Phase 3d)

**Sources (6):**
1. **Hacker News** — Algolia API, ≥ 30 pts, AI keyword filter
2. **Show HN** — Algolia `show_hn` tag, ≥ 20 pts, AI keyword filter; surfaces builder projects
3. **GitHub Trending** — scrapes daily + weekly, AI keyword filter
4. **Anthropic + OpenAI blogs** — scrapes Anthropic news page + OpenAI RSS, last 7 days
5. **YouTube** — RSS feeds for Matt Wolfe, Matthew Berman, Fireship (AI-filtered), Theo (t3.gg); per-channel error isolation
6. **Product Hunt** — GraphQL API v2, `artificial-intelligence` topic, sorted by votes; requires `PRODUCTHUNT_CLIENT_ID` + `PRODUCTHUNT_CLIENT_SECRET`

**Modes:**
- `python main.py daily` — 24h window, 3–7 picks, subject: `Signal · 日报 · Apr 17`
- `python main.py weekly` — 7d window, 10–20 picks, subject: `Signal · 周报 · Apr 11 – Apr 17`
- Default (no arg): daily

**Pipeline:**
1. All sources fetched with the appropriate time window
2. Candidates merged (~30–90 total depending on mode) and passed to **DeepSeek** (`deepseek-chat`)
3. DeepSeek filters for a vibe-coder audience (YouTube = highest priority; discard academic papers, low-level tools, business news, games)
4. Each pick gets a 60–100 char Chinese `why_it_matters` covering: what it is + what you can do + why useful
5. `display_title` normalizes GitHub owner capitalization (openai/ → OpenAI /)
6. Weekly email: 100–150 char Chinese summary at top, items grouped by source (📺 YouTube / 🐙 GitHub / 📰 Articles)
