# Proposal: Signal

A personal agent that extracts signal from the noise of AI/tech news.

*This is the final proposal, updated after the project was built. The original proposal set the direction; this version reflects the system that actually shipped.*

## What I built

A personal daily briefing system that pulls from a curated set of AI/tech sources, passes the raw items through an LLM for synthesis and filtering, and emails me a digest every morning. A longer weekly version runs on Sundays. All past digests are archived to a public GitHub Pages site with a 14-day retention window. The entire system runs unattended on GitHub Actions — I do not have to do anything to receive the emails.

## Why

I spend too much time scrolling for signal in the AI space. Twitter, HN, newsletters, and YouTube all overlap, and most of what surfaces is shallow — "OpenAI released X," "here's a ChatGPT prompt that changes everything," etc. What I actually want is the next layer down: interesting GitHub projects picking up momentum, new Skills or SDKs from Anthropic/OpenAI, emerging tools and sites, and patterns across all of this that I'd otherwise miss.

A personal agent that triages this for me each morning is genuinely useful, and it's a natural extension of what I already know: Flask and API work from MP3, Python scripting, and the end-to-end deployment experience from my OpenClaw project.

## What shipped

**Five content sources, fetched every run:**

1. Hacker News — via the Algolia API, filtered by AI keywords in the title, minimum score threshold. Both regular stories and Show HN are included.
2. GitHub Trending — daily and weekly lists scraped and merged, filtered by AI-related topics and keywords.
3. YouTube — native RSS feeds from four channels I chose (Matt Wolfe, Matthew Berman, Fireship, Theo t3.gg).
4. Product Hunt — GraphQL API v2 with client-credentials OAuth, filtered to the Artificial Intelligence topic.
5. Anthropic and OpenAI official blog RSS feeds.

**LLM-based filtering and synthesis:**

- All candidates from all sources are pooled, deduplicated, and scored for "how many days has this item already been seen in past digests" by scanning the archive.
- The full pool (typically 30–60 items per day) is passed to DeepSeek-chat, which applies my personal taste criteria: prioritize tools that a non-professional developer ("vibe coder") can actually use, avoid games/academic papers/pricing discussions/pure philosophy pieces, and explicitly prefer new items over items that already appeared in recent digests.
- DeepSeek returns 5–7 picks for the daily email and 15–20 for the weekly, each with a short Chinese explanation and a display-ready normalized title.
- The weekly digest additionally contains a 100–150 character synthesis paragraph at the top, pointing out the real themes of the week (not generic "AI is evolving fast" filler).

**Delivery:**

- HTML email via Gmail SMTP, grouped by source in the weekly version.
- HTML archive written to `/docs/` on every run, published via GitHub Pages at <https://TXiong323.github.io/oim3640/>. 14-day retention; older files are deleted automatically. Each archived page links back to the index.

**Automation:**

- GitHub Actions cron: daily at 7am ET, weekly on Sunday at 9am ET.
- All credentials live in GitHub repo secrets.
- The workflow commits the updated `docs/` folder back to the repo so the archive stays in sync.

## What I didn't build (and why)

**Multi-user / SaaS version.** The original stretch goal was a Flask signup page where anyone could configure their own topics and subscribe. I deliberately dropped this from scope. Between a realistic 11-day build window, the need to ship a polished MVP for demo day, and evaluation criteria that explicitly reward "a simple project you deeply understand over a complex one you can't explain," a half-finished multi-user system would have weakened the project. The single-user version is genuinely working and genuinely useful to me, and that's the stronger story.

**arXiv source.** Pulled from Phase 3 after testing the first two sources. Academic papers did not match the vibe-coder use case — too dense, too detached from anything I would actually use. Dropping it made the filtered email noticeably more useful.

**X (Twitter) source.** Evaluated and skipped. The official API is $200/month, and free alternatives are unreliable or maintenance-heavy. Not worth the tradeoff for a student project.

## What I didn't know when I started

- **Source quirks.** GitHub Trending has no official API and required HTML scraping. Product Hunt uses GraphQL with OAuth and required registering an application and handling client-credentials auth. YouTube RSS is undocumented but works on a simple URL pattern. Each source had its own gotcha.
- **Prompt iteration takes real work.** Getting DeepSeek to produce genuine analysis in Chinese, avoid "this reflects a growing trend" filler, normalize GitHub owner names to their canonical capitalization, and actively prefer fresh items over stale ones — each of these required a specific prompt change and a round of testing.
- **GitHub Actions paths.** My course repo has all final projects under `projects/<project_name>/`, but GitHub Actions only recognizes `.github/workflows/` at the repo root. GitHub Pages similarly only accepts `/` or `/docs` as publishable folders. Both required moving files to the right place and routing the workflow to run in the right working directory.
- **Secret hygiene.** Writing the `.env` setup and `.gitignore` was straightforward, but I made sure to verify (manually) that `.env` was never staged before the first push.

## Lessons

- Starting with the thinnest end-to-end slice (HN → email, and nothing else) paid off. I had a working pipeline receiving real email inside the first hour, and every new source was a small extension of something already working.
- Multiple small feedback rounds on the LLM filter produced a much better system than trying to write the perfect prompt upfront. After the first email arrived, it was immediately obvious that raw score-sorting was useless; the fix (delegating ranking to the LLM with a written taste profile) emerged from seeing what I actually disliked about the first output.
- AI tools are most useful when I'm specific about what I don't want, not just what I do. "No games, no pricing discussions, no academic papers, no philosophy" did more to improve the output than any amount of positive description.