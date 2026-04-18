# AI Usage Log

This file tracks how AI tools were used in building Signal, per OIM3640 requirements.

## Phase 1 — HN fetch + Gmail send

**Tool:** Claude Code (claude-sonnet-4-6)

**What I asked it to do:**
- Read `proposal.md` and propose a file structure
- Implement Phase 1 end-to-end: HN Algolia fetch, HTML email formatter, Gmail SMTP sender, and `main.py` entry point

**What it produced:**
- `sources/hackernews.py` — fetches stories from HN Algolia API, filters by AI keywords and score ≥ 50, last 24 hours
- `email_sender.py` — builds HTML email and sends via Gmail SMTP_SSL
- `main.py` — orchestrates the pipeline
- Supporting files: `.gitignore`, `.env.example`, `requirements.txt`

**My judgment calls:**
- Keyword list in `hackernews.py` — reviewed and adjusted the list manually
- Email HTML layout — approved the template as-is
- File structure — accepted Claude's proposal without changes

**Prompting notes:**
- Gave Claude explicit phasing instructions and told it to keep code simple and readable
- Told it to avoid framework-style abstractions for a student project
