# Signal

A personal agent that pulls deep-layer AI/tech news from curated sources, synthesizes it with an LLM, and emails me a daily digest.

Built as the final project for OIM3640 (Spring 2026, Babson College).

See [`proposal.md`](proposal.md) for goals, MVP scope, and stretch goals.

## Status

**Phase 4 complete** — GitHub Actions cron + archive system  

## Local development

```bash
pip install -r requirements.txt
cp .env.example .env   # fill in real values (see table below)
python main.py          # daily digest (default)
python main.py daily    # explicit daily
python main.py weekly   # weekly digest
```

## Automated runs via GitHub Actions

Two workflows run on a schedule:

| Workflow | Schedule | Command |
|---|---|---|
| `daily.yml` | Every day at 7:00 AM ET (11:00 UTC) | `python main.py daily` |
| `weekly.yml` | Every Sunday at 9:00 AM ET (13:00 UTC) | `python main.py weekly` |

Both support **manual trigger** via `workflow_dispatch` (Actions tab → select workflow → Run workflow).

**Required repo secrets** (Settings → Secrets and variables → Actions):

| Secret | Value |
|---|---|
| `GMAIL_ADDRESS` | Your Gmail address |
| `GMAIL_APP_PASSWORD` | Gmail App Password |
| `RECIPIENT_EMAIL` | Delivery address |
| `DEEPSEEK_API_KEY` | DeepSeek API key |
| `PRODUCTHUNT_CLIENT_ID` | Product Hunt OAuth client ID |
| `PRODUCTHUNT_CLIENT_SECRET` | Product Hunt OAuth client secret |

## Environment variables

| Variable | Description |
|---|---|
| `GMAIL_ADDRESS` | Your Gmail address used to send |
| `GMAIL_APP_PASSWORD` | [Gmail App Password](https://myaccount.google.com/apppasswords) (not your regular password) |
| `RECIPIENT_EMAIL` | Where to deliver the digest |
| `DEEPSEEK_API_KEY` | DeepSeek API key from [platform.deepseek.com](https://platform.deepseek.com) |
| `PRODUCTHUNT_CLIENT_ID` | From [api.producthunt.com/v2/oauth/applications](https://api.producthunt.com/v2/oauth/applications) |
| `PRODUCTHUNT_CLIENT_SECRET` | Same app registration page |

## Archive

Every run writes a timestamped HTML file to `archive/` and regenerates `archive/index.html`. Files older than 14 days are automatically deleted.

**Enable GitHub Pages** to browse the archive in a browser:

1. Go to **Settings → Pages**
2. Source: **Deploy from a branch**
3. Branch: `main` / Folder: `/docs`
4. Save

Your archive will be live at:
```
https://TXiong323.github.io/oim3640/
```

The index page lists all available digests; each digest links back to the index.

## How it works (Phase 4)

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
