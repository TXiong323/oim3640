# AI Usage Log

This file tracks how AI tools were used in building Signal, per OIM3640 requirements.

## Phase 2 — DeepSeek filtering + per-item analysis

**Tool:** Claude Code (claude-sonnet-4-6)

**What I asked it to do:**
- Add DeepSeek API integration to filter candidates and generate `why_it_matters` notes
- Lower HN score threshold from 50 → 30 to get more candidates
- Update email template to show DeepSeek's one-line rationale per item
- Handle the empty-result case ("nothing worth reading today")

**What it produced:**
- `analyzer.py` — calls DeepSeek `deepseek-chat` via OpenAI-compatible SDK, returns filtered JSON list
- Updated `email_sender.py` — shows `why_it_matters` in italic gray below each title
- Updated `main.py` — fetch → analyze → merge metadata → send
- System prompt encodes INTERESTED / NOT INTERESTED categories with explicit rules

**My judgment calls:**
- Reviewed and approved the INTERESTED/NOT INTERESTED lists in the system prompt
- Set temperature=0.2 for consistent filtering behavior
- Capped why_it_matters at 25 words to keep email scannable

---

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
