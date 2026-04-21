# Signal

A personal AI/tech daily briefing. Pulls from five curated sources, filters them through an LLM against a personal taste profile, and emails me a digest every morning. A longer weekly version runs on Sundays. All digests are archived to a public GitHub Pages site for 14 days.

Runs unattended on GitHub Actions. I don't do anything — the email just shows up.

**Live archive:** <https://TXiong323.github.io/oim3640/>

Built as the final project for OIM3640 (Spring 2026, Babson College).

---

## What it does

Every morning at 7am ET, GitHub Actions runs the system:

1. **Fetches** candidates from 5 sources (typically 30–60 items total)
2. **Deduplicates** and counts how many days each item has already appeared in past digests
3. **Filters** the whole pool through DeepSeek with my taste profile — prefer fresh items, prefer vibe-coder-friendly tools, skip games / academic papers / pricing debates
4. **Writes** a Chinese one-liner explanation for each selected item
5. **Emails** the digest via Gmail SMTP
6. **Archives** the same HTML to `docs/`, which is published via GitHub Pages
7. **Commits** the updated archive back to the repo

Weekly digests run Sunday at 9am ET, include a synthesis paragraph summarizing the week's real themes, and group items by source.

---

## Sources

| Source | How it's fetched |
| --- | --- |
| Hacker News (stories + Show HN) | Algolia search API, filtered by AI keywords in title |
| GitHub Trending (daily + weekly) | HTML scraping, filtered by AI topics |
| YouTube | Native channel RSS feeds — Matt Wolfe, Matthew Berman, Fireship, Theo t3.gg |
| Product Hunt (AI topic) | GraphQL API v2, client-credentials OAuth |
| Anthropic + OpenAI blogs | Official RSS |

---

## Local development

**Prerequisites:** Python 3.10+, a Gmail account with an app password, a DeepSeek API key, and a Product Hunt API application (free to register at <https://www.producthunt.com/v2/oauth/applications>).

```bash
cd projects/fp_Signal
pip install -r requirements.txt
cp .env.example .env
# Fill in the real values in .env
python main.py daily    # or: python main.py weekly
```

`main.py daily` fetches a 24-hour window; `main.py weekly` fetches 7 days and adds a synthesis paragraph. Both send an email and write an archive file to `../../docs/`.

### Required environment variables

| Variable | Purpose |
| --- | --- |
| `GMAIL_ADDRESS` | Sender Gmail address |
| `GMAIL_APP_PASSWORD` | Gmail app password (not your login password) |
| `RECIPIENT_EMAIL` | Where the digest is sent |
| `DEEPSEEK_API_KEY` | For the filter + synthesis step |
| `PRODUCTHUNT_CLIENT_ID` | Product Hunt API credentials |
| `PRODUCTHUNT_CLIENT_SECRET` | Product Hunt API credentials |

The real `.env` is gitignored. See `.env.example` for the template.

---

## Automated runs

The system runs on GitHub Actions without any servers of my own:

- `.github/workflows/signal-daily.yml` — daily at 11:00 UTC (7am ET)
- `.github/workflows/signal-weekly.yml` — Sundays at 13:00 UTC (9am ET)

Both workflows also support manual `workflow_dispatch` triggers from the Actions UI, which is how I test.

**To set this up on a fork:**

1. Go to **Settings → Secrets and variables → Actions** and add the six environment variables above as repo secrets.
2. Go to **Settings → Pages** and set Source = `Deploy from a branch`, Branch = `main`, Folder = `/docs`.
3. Trigger the daily workflow manually once to verify end-to-end.

The workflows have `contents: write` permission so they can commit the updated archive back to the repo.

---

## Archive

Every run writes an HTML copy of the email to `docs/` at the repo root:

- `docs/index.html` — landing page, lists everything in reverse chronological order
- `docs/daily-YYYY-MM-DD.html` — that day's daily digest
- `docs/weekly-YYYY-MM-DD.html` — that week's weekly digest

**14-day retention.** Every run also deletes archive files whose filename date is older than 14 days. `index.html` is regenerated from scratch so it always reflects the current contents of `docs/`.

The archive is public at <https://TXiong323.github.io/oim3640/>.

---

## Structure

```
projects/fp_Signal/
├── main.py              # Orchestrator: fetch → dedupe → filter → email → archive
├── analyzer.py          # DeepSeek call + prompt + JSON parsing
├── email_sender.py      # Gmail SMTP + HTML rendering
├── archive.py           # Write HTML to docs/, clean old files, rebuild index
├── sources/
│   ├── hackernews.py    # Algolia API + keyword filter
│   ├── github_trending.py  # HTML scrape of trending pages
│   ├── youtube.py       # RSS from 4 channels
│   ├── producthunt.py   # GraphQL + OAuth
│   └── blogs.py         # Anthropic + OpenAI RSS
├── requirements.txt
├── .env.example
├── proposal.md
└── AI_USAGE.md
```

Workflows live at the repo root (`.github/workflows/`) because GitHub Actions only recognizes workflow files at the root, not under a subdirectory.

---

## Acknowledgments

Built iteratively with Claude and Claude Code. See [`AI_USAGE.md`](AI_USAGE.md) for the full log of how AI tools were used at each stage of the project.