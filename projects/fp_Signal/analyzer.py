import json
import os
from openai import OpenAI

SYSTEM_PROMPT = """You are a content curator for a personal AI/tech digest. The reader is a "vibe coder" — someone who uses AI tools like Claude Code to build small projects without deep programming expertise. They want things they can open and use today, not things requiring deep technical knowledge.

Sources include: Hacker News (HN), GitHub Trending (GITHUB), Anthropic blog (ANTHROPIC), OpenAI blog (OPENAI), and YouTube videos (YOUTUBE).

SOURCE PRIORITY:
1. YOUTUBE — human-curated expert content, highest signal. Keep if the video is about something new and usable.
2. ANTHROPIC / OPENAI blog posts — official releases, high reliability.
3. GITHUB — fast-rising repos, especially ones with a UI or that are plug-and-play.
4. HN — good for discovering new products and tutorials.

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

Return ONLY valid JSON, no markdown fences."""

_DAILY_USER = """Today's candidates. Pick the best 3–7 for a daily digest. Return JSON only.

Candidates:
{candidates}

Format:
{{
  "items": [
    {{"title": "...", "display_title": "...", "url": "...", "why_it_matters": "..."}}
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
    {{"title": "...", "display_title": "...", "url": "...", "why_it_matters": "..."}}
  ]
}}"""


def analyze(candidates: list[dict], mode: str = "daily") -> dict:
    client = OpenAI(
        api_key=os.environ["DEEPSEEK_API_KEY"],
        base_url="https://api.deepseek.com",
    )

    lines = "\n".join(
        f"{i+1}. [{c['source'].upper()}] title: {c['title']}\n    url: {c['url']}"
        for i, c in enumerate(candidates)
    )

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
