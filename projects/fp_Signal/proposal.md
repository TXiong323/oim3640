# Proposal: Signal

A personal agent that extracts signal from the noise of AI/tech news.

## What I'm building

A personal daily briefing system that pulls from a curated set of AI/tech sources, passes the raw items through an LLM for synthesis and analysis, and emails me a digest every morning. Built for myself as the first user; any multi-user version is a stretch goal.

## Why

I spend too much time scrolling for signal in the AI space. Twitter, HN, newsletters, and YouTube all overlap, and most of what surfaces is shallow — "OpenAI released X," "here's a ChatGPT prompt that changes everything," etc. What I actually want is the next layer down: interesting GitHub projects picking up momentum, new Skills or SDKs from Anthropic/OpenAI, emerging tools and sites, research worth skimming, and patterns across all of this that I'd otherwise miss.

A personal agent that triages this for me each morning is genuinely useful and a natural extension of what I already know: Flask and API work from MP3, Python scripting, and the end-to-end deployment experience from the OpenClaw project.

## MVP

A Python script, scheduled via GitHub Actions, that runs every morning and emails me one digest.

**Sources (5, fixed):**
- GitHub Trending, filtered by `ai`, `llm`, `agents`, `mcp` topics
- Hacker News via the Algolia API, filtered by AI keywords and a score threshold
- arXiv `cs.AI` and `cs.CL` new submissions (RSS)
- Anthropic and OpenAI official blogs (RSS)
- Product Hunt AI category

**Pipeline:**
1. Fetch raw items from each source
2. Deduplicate and rank (simple weighted scoring across sources)
3. Pass the top ~10 items to the Claude API for synthesis
4. The prompt pushes for specific details, cross-item patterns, and "why this matters" — not generic "this reflects a growing trend" filler
5. Render as HTML email and send via Gmail SMTP

**Infrastructure:**
- Scheduled as a GitHub Actions cron workflow (daily, ~7am ET)
- Secrets stored in GitHub repo secrets, not in code
- `.env.example` in the repo, real `.env` gitignored

## Stretch goals

1. **Weekly deep-dive** — a Saturday email that synthesizes the week's items into a longer trend analysis: what's actually emerging, what's hype, what's worth trying hands-on.
2. **Topic configurability** — a YAML config where I define topics and keywords, and the system adapts source queries accordingly. This is the bridge to the multi-user version.
3. **Multi-user version** — a minimal Flask signup page where anyone can register, configure their own topics and email, and subscribe to their own digest.
4. **Read-later queue** — items I flag from the email get saved to a structured store I can come back to.

## What I don't know yet

- **Source quirks.** GitHub Trending has no official API (need to pick between scraping and an unofficial wrapper); Product Hunt requires OAuth; arXiv RSS format I haven't worked with before.
- **Ranking heuristic.** HN points, GitHub stars, and arXiv recency aren't directly comparable. I'll start with a simple weighted scheme and tune it against my own taste.
- **Prompting for depth.** Getting the LLM to produce genuine analysis instead of vague trend-speak is the part most likely to take real iteration. I expect several rounds of prompt tweaking.
- **GitHub Actions cron.** I've used Actions for CI but not for scheduled jobs. Need to read up on the `schedule:` trigger and how secrets behave in that context.
- **Email rendering.** Gmail SMTP to my own inbox should be straightforward, but HTML rendering across mail clients is famously fragile. Might start plain-text and layer HTML on once the pipeline works.