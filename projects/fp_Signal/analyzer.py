import json
import os
from openai import OpenAI

SYSTEM_PROMPT = """You are a content curator for a personal AI/tech digest. The reader is a "vibe coder" — someone who uses AI tools like Claude Code to build small projects without deep programming expertise. They want things they can open and use today, not things requiring deep technical knowledge.

Sources include: Hacker News (HN), Show HN (SHOW_HN), GitHub Trending (GITHUB), Anthropic blog (ANTHROPIC), OpenAI blog (OPENAI), YouTube videos (YOUTUBE), and Product Hunt (PRODUCTHUNT).

SOURCE PRIORITY:
1. YOUTUBE — human-curated expert content, highest signal. Keep if the video is about something new and usable.
2. PRODUCTHUNT — real user-facing AI tools and websites, core value of this digest. Prioritize highly.
3. ANTHROPIC / OPENAI blog posts — official releases, high reliability.
4. SHOW_HN — builders showing their own AI projects; often overlooked gems.
5. GITHUB — fast-rising repos, especially ones with a UI or that are plug-and-play.
6. HN — good for discovering new products and tutorials.

KEEP (vibe-coder relevant):
- New skills, extensions, or MCP servers for Claude Code, Cursor, Copilot, or similar AI coding tools
- New AI products, websites, or SaaS tools anyone can open and use immediately
- New model releases or major new features from Anthropic, OpenAI, Google, etc.
- Simple AI agents or automation tools a non-programmer can actually run
- YouTube tutorials or demos of any of the above

DISCARD:
- Academic papers, research preprints, benchmarks, theoretical analysis
- Low-level developer tools: debuggers, reverse engineering, file parsers, CLI utilities, anything needing deep technical background
- Pure libraries/frameworks with no user-facing interface
- Games, game engines, entertainment AI
- Pricing, cost comparisons, token economics
- Business news: funding, acquisitions, hiring
- Policy, regulation, ethics debates
- Security vulnerabilities / CVEs
- Lengthy discussion threads with no concrete new thing

Be aggressive. If it needs a senior engineer to appreciate it, discard it.

WRITING RULES for why_it_matters:
- Write in Chinese, 60–100 characters.
- Cover three dimensions: ① 这是什么 ② 能用来做什么 ③ 为什么对 vibe coder 有用
- Keep product names and technical terms in English (Claude Code, MCP, SDK, API, agent, LLM, UI, etc.)
- No filler. No "这反映了..." or "这标志着..."
- Bad example: "Claude Code 记忆插件，自动记录上下文。"
- Good example: "Claude Code 的记忆扩展插件，自动保存你跟 AI 的对话历史并在新会话里复用，不用每次都重新解释项目背景，对长期项目特别省事。"

DISPLAY TITLE:
- For GitHub repos: capitalize the owner correctly (openai/ → OpenAI /, google/ → Google /, anthropic/ → Anthropic /; unknown owners: capitalize first letter).
- For all other items: return the original title unchanged.

FRESHNESS AND REPEAT DETECTION (seen_count field on each candidate):
Freshness is a core selection criterion — the digest must bring new information every day.
- seen_count=0: first appearance, normal priority. All else equal, prefer these.
- seen_count>=1: the item appeared in a previous digest. Only include it if there is a concrete, describable new development (a new release, a version bump, a major update). If nothing has concretely changed, skip it — even if it has high votes or stars. "Still popular" is not a reason to re-include.
- seen_count>=3: skip unless there is a genuinely significant update. The bar is very high.
- seen_count>=5: always skip, no exceptions.

Source freshness guidance (soft targets, not hard rules):
- Product Hunt top products tend to stay at the top for days — cap at ~3 PH items per digest to prevent the same products dominating every day.
- GitHub Trending and Show HN change daily — prefer 2–3 GitHub picks and 1–2 from HN/Show HN when quality is comparable.
- YouTube and official blog posts are typically new each day — keep them if relevant.
- The goal is that a reader who reads every day should get genuinely new information each time, not see the same 5 products recycled.

In your response, copy the seen_count value into a "seen_before" field on each item.

Return ONLY valid JSON, no markdown fences."""

_DAILY_USER = """Today's candidates. Pick the best 3–7 for a daily digest. Return JSON only.

Candidates:
{candidates}

Format:
{{
  "items": [
    {{"title": "...", "display_title": "...", "url": "...", "why_it_matters": "...", "seen_before": 0}}
  ]
}}"""

_WEEKLY_USER = """This week's candidates. Pick the best 10–20 for a weekly digest. Return JSON only.

Also write a 100–150 Chinese character weekly summary (summary field) that identifies the real story of the week — what actually shipped, what trends are real, what's worth paying attention to. Be specific. No "本周 AI 圈很热闹" filler.

Candidates:
{candidates}

Format:
{{
  "summary": "...",
  "items": [
    {{"title": "...", "display_title": "...", "url": "...", "why_it_matters": "...", "seen_before": 0}}
  ]
}}"""

_HEADLINES_SYSTEM = """You are selecting "Top Headlines of the Week" for an AI/tech digest — a pinned section that highlights the single most significant AI industry events of the past 7 days.

INCLUDE ONLY items that meet ALL of these criteria:
1. Official release by a major AI company: OpenAI, Anthropic, Google/DeepMind, Meta, Microsoft, Apple, or xAI
2. Core product announcement: a new model, new model version, new SDK, new official agent capability, or new flagship API feature
3. Developer-level significance: something a developer would immediately say changes how they build or work — Codex CLI, Claude Code, GPT-4o, Gemini 2.0 level significance

EXPLICITLY EXCLUDE — do not include under any circumstances:
- Third-party tools, plugins, wrappers, or GitHub repos built on top of AI models
- Product Hunt launches by individual developers or startups
- Research papers, preprints, or benchmarks
- Community projects, tutorials, blog posts, or opinion pieces
- Incremental updates, minor patches, or price changes
- Funding rounds, acquisitions, partnerships, or business news
- HN discussion threads unless the URL is the official company announcement

FRESHNESS NOTE: Items published 2–7 days ago are still valid for this section. The purpose is to keep major events visible for the full week after they ship.

WRITING RULES for why_it_matters:
- Write in Chinese, 60–100 characters
- Cover: ① 这是什么 ② 为什么重要/能做什么
- Keep product names and technical terms in English
- No filler phrases like "这反映了..." or "这标志着..."

DISPLAY TITLE:
- Return the original title unchanged for all items.

Return the seen_count value as "seen_before" on each item.

If there are no items that genuinely meet the threshold, return an empty items list. Do NOT fill the list with second-tier content.

Return ONLY valid JSON, no markdown fences."""

_HEADLINES_USER = """From the past 7 days of candidates, select at most 3 that qualify as major official releases from big AI companies. Return them newest-first (most recent publication date first). Return JSON only.

Candidates:
{candidates}

Format:
{{
  "items": [
    {{"title": "...", "display_title": "...", "url": "...", "why_it_matters": "...", "seen_before": 0}}
  ]
}}"""


def _make_client() -> OpenAI:
    return OpenAI(
        api_key=os.environ["DEEPSEEK_API_KEY"],
        base_url="https://api.deepseek.com",
    )


def _format_candidates(candidates: list[dict]) -> str:
    return "\n".join(
        f"{i+1}. [{c['source'].upper()}] title: {c['title']}\n"
        f"    url: {c['url']}\n"
        f"    seen_count: {c.get('seen_count', 0)}"
        for i, c in enumerate(candidates)
    )


def analyze(candidates: list[dict], mode: str = "daily") -> dict:
    client = _make_client()
    lines = _format_candidates(candidates)
    template = _WEEKLY_USER if mode == "weekly" else _DAILY_USER

    response = client.chat.completions.create(
        model="deepseek-chat",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": template.format(candidates=lines)},
        ],
        temperature=0.2,
    )

    raw = response.choices[0].message.content
    data = json.loads(raw)
    return {
        "items": data.get("items", []),
        "summary": data.get("summary", ""),
    }


def analyze_headlines(candidates: list[dict]) -> dict:
    """Select up to 3 major big-tech release items from a 7-day candidate pool."""
    if not candidates:
        return {"items": []}

    client = _make_client()
    lines = _format_candidates(candidates)

    response = client.chat.completions.create(
        model="deepseek-chat",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": _HEADLINES_SYSTEM},
            {"role": "user", "content": _HEADLINES_USER.format(candidates=lines)},
        ],
        temperature=0.1,
    )

    raw = response.choices[0].message.content
    data = json.loads(raw)
    return {"items": data.get("items", [])}
