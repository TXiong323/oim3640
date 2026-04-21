# AI Usage Log

This document records how I used AI tools to build Signal. The course requires documenting significant AI usage: what I asked, what the AI generated, what I did with it, and what I learned. This file is written honestly — it describes how the project was actually built, including the moments where AI outputs were wrong or mismatched my intent and I had to push back.

I used **Claude (claude.ai) for planning, prompt writing, and troubleshooting**, and **Claude Code for actually writing the code**. This two-tool split was itself something I learned: Claude in the browser is a good collaborator for thinking through decisions, but Claude Code is much better at writing code because it can run the code, see the errors, and iterate — which saves me from copy-pasting stack traces back and forth.

---

## Phase 0 — Scoping the project

**What I asked:**

I started by describing the idea in plain Chinese: a system that emails me a daily digest of deep AI/tech content — not just "OpenAI released X," but things like new GitHub projects, new Claude/OpenAI Skills, emerging tools. I wasn't sure what the right MVP was, which sources to use, or whether to even build for multiple users.

**What the AI suggested:**

Claude pushed back on several of my initial assumptions:

- Daily cadence: Claude pointed out that AI content isn't high-quality every day, and that a "daily highlights + weekly deep-dive" split would be more realistic than a daily deep-dive.
- Source selection: Instead of "Google search," Claude suggested specific APIs and RSS feeds — Hacker News via Algolia, arXiv RSS, GitHub Trending, Anthropic/OpenAI blogs, Product Hunt.
- Hosting: GitHub Actions cron instead of a DigitalOcean server. Reason: free, zero-maintenance, version-controlled, secrets built in.

**What I did with it:**

I accepted all three recommendations. The GitHub Actions suggestion saved me significant time — I had just finished tearing down a DigitalOcean deployment for OpenClaw and didn't want another server. I also agreed to the "daily + weekly" split, though I ended up building both as full digests rather than one highlights / one deep-dive.

**What I learned:**

The thing I would have gotten wrong on my own was the hosting choice. I would have reached for a cloud VM out of habit. Using Claude as a planning partner is most valuable for choices like this — where the right answer depends on knowing the ecosystem, not just knowing my goal.

---

## Phase 1 — First end-to-end slice

**What I asked:**

I asked Claude to plan an MVP and then to hand me a concrete prompt I could paste into Claude Code. My instruction was "don't over-engineer, pick the smallest thing that actually works end-to-end."

**What the AI suggested:**

Claude wrote a multi-phase plan: Phase 1 = just Hacker News → Gmail SMTP → verify I receive the email. No LLM, no other sources, no scheduling. Phase 2 = add LLM filtering. Phase 3 = add remaining sources. Phase 4 = deploy to Actions.

**What I did with it:**

I pushed back once: I asked whether I should just build the whole thing in one shot, since "it'll be faster." Claude's argument was that if something breaks when all five sources plus the LLM plus SMTP plus Actions are all wired up at once, I won't know which layer broke. I accepted this and agreed to the phased plan.

Claude Code then built Phase 1. First real email arrived within the first hour. This was motivating — turning a description into a working system in under an hour gave me confidence the rest would also work.

**What I learned:**

Building the thin end-to-end slice first is much better than building each component to "completion" in isolation. The first email revealed several things I wouldn't have noticed by looking at code — for example, that pure score-sorting on Hacker News produces bad results (the top item was "Measuring Claude 4.7's tokenizer costs," which I don't care about). That observation directly shaped Phase 2.

---

## Phase 2 — LLM-based filtering

**What I asked:**

After the first Phase 1 email, I sent Claude a screenshot and said: "Item 2 is useless to me. I don't care about pricing. I want tools and products and new releases, not philosophy."

**What the AI suggested:**

Claude reframed the problem: the issue wasn't the source (HN was fine) but the ranking. Raw score-sort mixes "new useful tool" with "trending pricing debate." The fix was to lower the score threshold (so more candidates pass through), then have an LLM re-rank with a written taste profile.

Claude wrote a prompt telling DeepSeek what I cared about (new tools, new Skills, working products, trending GitHub projects) and what I didn't care about (pricing, philosophy, politics, vaporware). It also required the LLM to return structured JSON with a one-sentence `why_it_matters` field per selected item.

**What I did with it:**

I accepted the design. I also switched the LLM choice from Claude API to DeepSeek API because I'd already topped up a DeepSeek account and it was cheaper. Claude pointed out that for this task the quality gap is small and I should start a new API key per project for isolation and tracking — good advice I followed.

The second email arrived and looked noticeably better.

**What I learned:**

The most important thing to communicate to an LLM isn't what you want — it's what you don't want. A one-line "what I don't care about" list did more to improve the output than any amount of positive description. I applied this lesson to every subsequent prompt iteration.

---

## Phase 3 — Adding sources, iterating on output

This was the longest phase. I did not accept AI suggestions wholesale; I pushed back frequently as each source shipped and I saw the output.

### Phase 3a — GitHub Trending

Claude Code added GitHub Trending by scraping the public HTML page (no API exists). The first output included a Genome Evolution AI agent project and some ML engineering tools. I liked this direction — actionable new projects.

### Phase 3b — Output formatting, first serious pushback

After 3a, the email was functional but cluttered. I told Claude to make two changes: drop the URL from the title (it was being appended like "Title — https://...") and translate the `why_it_matters` explanations to Chinese (easier for me to scan quickly).

**What went wrong:**

Claude overcorrected and also translated the metadata line — "stars today" became "今日 stars," "comments" became "评论," "discuss" became "讨论." This looked weird because those short English words are universally understood and didn't need translation.

**What I did:**

I sent a direct message: "你搞什么飞机？" ("What are you doing?"). I told Claude to revert the metadata translation and only keep the Chinese explanations. I listed exactly what to keep in English (pts, comments, discuss, Hacker News) and what to translate (the explanation sentence only).

**What I learned:**

When an LLM overcorrects, it's often because my instruction was under-specified. "Make it Chinese" is ambiguous. "Translate the explanation to Chinese but keep metadata labels in English" is specific. I got better at writing prompts that distinguished "change X" from "don't touch Y."

### Phase 3c — Dropping arXiv, reframing the user profile

I had originally planned to add arXiv cs.AI as a source. After seeing the first few emails, I realized the problem wasn't that I needed more sources — it was that the LLM didn't know what kind of user I was.

**What I asked Claude:**

"I'm not a programmer. I use Claude Code to make small things. I'm a vibe coder, not a research engineer. Academic papers are too dense for me."

**What the AI suggested:**

Claude suggested skipping arXiv entirely. It then rewrote the LLM prompt to describe me explicitly: "user profile: vibe coder, not an engineer, uses Claude Code to build small tools, prefers things that can be used immediately." The prompt also gave an ordered priority list (Claude Code skills > new AI products > big-lab releases > simple agents) and a clearer do-not-pick list (academic papers, low-level devtools, frameworks without UI, games, business news, security CVEs).

**What I did with it:**

I accepted this. The output quality jumped. The next email included the Claude Code memory plugin, an Android CLI tool, Claude Opus 4.7, and an OpenAI agents SDK — all things I could actually imagine using.

**What I learned:**

Filtering quality isn't about the LLM — it's about how accurately the prompt describes the end user. The prompt before this phase was trying to describe what content was "good." After this phase, the prompt described *who* it was selecting for. The second framing is much more productive.

### Phase 3d — YouTube source

I asked if YouTube creators could be added. Claude confirmed YouTube has native RSS per channel (no API key, free). It also warned me that X/Twitter would be expensive ($200/month for the official API) and suggested skipping it. I agreed.

Claude suggested four channels (Matt Wolfe, Matthew Berman, Fireship, Theo t3.gg) and identified their channel IDs by searching the web for them. Claude Code wired them in.

One detail: Fireship covers more than just AI, so its feed needed a keyword filter. Claude Code added this unprompted — I only noticed when reviewing the diff.

### Phase 3e — Product Hunt + Show HN

The last sources. Product Hunt uses GraphQL with OAuth, which required registering a Product Hunt application. Claude walked me through what to fill in the registration form (name: "Signal", redirect URI: `https://localhost` — the HTTP version was rejected by their validator). Show HN was a trivial variant of the existing HN code.

---

## Phase 4 — Deployment to GitHub Actions

**What I asked:**

After Phase 3 was complete, I asked Claude to write the GitHub Actions workflows for daily and weekly runs.

**What went wrong:**

Claude Code put the workflow files in `projects/fp_Signal/.github/workflows/`. I pushed and waited, but the Actions tab showed "Get started with GitHub Actions" — no workflows detected.

**What I learned and fixed:**

Claude explained the problem: GitHub Actions only detects `.github/workflows/` at the repo root, not in subdirectories. This is undocumented behavior I would not have guessed. I had Claude Code move the workflow files to the repo root and keep `working-directory: projects/fp_Signal` in the workflow YAML so commands still ran in the right place.

A similar issue hit GitHub Pages later: the Pages settings UI only lets you publish from `/` (root) or `/docs`, not from a subdirectory. I had to move the archive output from `projects/fp_Signal/archive/` to `/docs/` at the repo root, and update the archiver accordingly.

**What I learned:**

Both of these are the kind of "the tool has an opinion and won't tell you" problems where AI is much faster than me. Without Claude, I would have spent hours on Stack Overflow before finding the GitHub Pages path restriction. With Claude I knew within a minute that I needed to restructure.

---

## Phase 5 — Archive, retention, cross-day deduplication

Three additions after deployment:

**Archive (public HTML version of the emails).** I asked for a GitHub Pages site showing the past two weeks of digests. Claude Code built `archiver.py` with a 14-day retention rule — each run writes `daily-YYYY-MM-DD.html` and regenerates `index.html`, and deletes files whose filename date is older than 14 days. Claude suggested parsing the date from the filename rather than using file modification time, because git changes mtime on every checkout and that would break retention. That was a detail I would not have thought of.

**Small code review I did myself.** Claude Code's first version of `archiver.py` had `ARCHIVE_DIR = Path(__file__).parent / ".." / ".." / "docs"` — functional but non-canonical (it would print an ugly path). I caught this, asked Claude why not call `.resolve()` on it, Claude agreed, and I had Claude Code make the one-line fix. Small example, but worth noting: reading the code is still my job, even when an AI wrote it.

**Cross-day deduplication.** After a couple of days of auto-runs, I noticed the same items appearing day after day, because high-vote Product Hunt products stay high-vote. I asked Claude to add a `seen_count` per candidate, computed by scanning archive HTML. Claude Code wrote `dedup.py` for this, and Claude updated the LLM prompt to prefer fresh items and only keep repeats if there's "genuinely new progress."

**First implementation mistake:** Claude's first version tagged items with `已出现 1 天` after one day, which was visual noise — one day old is barely "seen before." I pushed back: only show the badge for 2+ days. Claude Code adjusted.

**What I learned:**

Once the system was running in production, the feedback loop changed. I wasn't reviewing code output anymore — I was reviewing actual emails over multiple days. Some problems (like "too much repetition of the same items") only show up after the system has been running for a while. That's a kind of QA I couldn't have done upfront.

---

## Broader reflection

**Where AI was most valuable.** Planning decisions (hosting, phased build order, source selection), structural issues (workflow file paths, GitHub Pages constraints), and prompt iteration. Claude's ability to look at my screenshot of a bad email and propose a specific prompt change was the single highest-leverage loop in the whole project.

**Where AI was least valuable.** Judgments about my personal taste. I had to push back on several drafts that were technically correct but didn't match what I actually wanted — over-translated metadata, too-short explanations, a "1 day seen" badge that was noise. None of these were bugs the AI could have caught. I had to see the output and say "no, that's wrong."

**Where I was wrong and AI was right.** At least three times — when Claude suggested phased development instead of one-shot building, when Claude pushed back on expanding to a multi-user SaaS version before finishing the single-user MVP, and when Claude warned me that paying $200/month for the Twitter API was a bad tradeoff. In each case I initially wanted the bigger, more ambitious version; Claude's argument for staying focused was correct and I would have regretted the alternative.

**Biggest skill I developed.** Writing better prompts. Specifically: describing users, not content. "I want X" produces worse output than "this person wants X because of Y." The LLM prompt in `analyzer.py` now reads more like a user persona than a filter specification, and the output quality is much better for it.

**What I would do differently next time.** Start the AI_USAGE.md on day one and update it as I go, not at the end. Right now this document is reconstructed from memory and from my chat logs, which takes extra work and risks missing small-but-important moments.