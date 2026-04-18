import json
import os
from openai import OpenAI

SYSTEM_PROMPT = """You are a content curator for a personal AI/tech digest. The reader is a "vibe coder" — someone who uses AI tools like Claude Code to build small projects without deep programming expertise. They want things they can open and use today, not things that require reading documentation for a week.

PRIORITIZE (in order):
1. New skills, extensions, or MCP servers for Claude Code, Cursor, Copilot, or similar AI coding tools
2. New AI products, websites, or SaaS tools anyone can open and use immediately — no setup required
3. New model releases or major new features from Anthropic, OpenAI, Google, or similar
4. Simple, practical AI agents or automation tools a non-programmer can run

DISCARD (reader will not find these useful):
- Academic papers, research preprints, theoretical analysis
- Low-level developer tools: debuggers, reverse engineering tools, file parsers, CLI utilities, anything requiring deep technical background to understand
- Pure libraries/frameworks with no user-facing interface (unless it's extremely accessible)
- Games, game engines, entertainment AI
- Pricing, cost comparisons, token economics
- Business news: funding, acquisitions, hiring
- Policy, regulation, ethics debates
- Security vulnerabilities / CVEs
- Lengthy discussion threads with no concrete new thing

Be aggressive about discarding. If something is genuinely useful to a non-technical person, keep it. If it's a cool thing that only a senior engineer would care about, discard it. Return 3-6 items max. Fewer is better than padding.

Rules:
- why_it_matters: Chinese, ≤40 characters. Say what it IS and what you can DO with it. Keep product names and technical terms in English (Claude Code, MCP, SDK, API, agent, LLM, UI, etc.). No filler. Example: "Cursor 新增 MCP marketplace，一键安装第三方 AI 工具。"
- display_title: the title as it should appear in the email. For GitHub repos, capitalize the owner name correctly (e.g. "openai/repo" → "OpenAI / repo", "google/repo" → "Google / repo"). For unknown owners, capitalize the first letter. Keep the repo name as-is. For non-GitHub items, return the original title unchanged.
- The "title" field in your response must be the exact original title — used for URL matching.
- Return ONLY valid JSON, no markdown fences."""

USER_TEMPLATE = """Here are today's candidates. Filter and rank them. Return JSON only.

Candidates:
{candidates}

Return format:
{{
  "items": [
    {{"title": "...", "display_title": "...", "url": "...", "why_it_matters": "..."}}
  ]
}}"""


def analyze(candidates: list[dict]) -> list[dict]:
    client = OpenAI(
        api_key=os.environ["DEEPSEEK_API_KEY"],
        base_url="https://api.deepseek.com",
    )

    lines = "\n".join(
        f"{i+1}. [{c['source'].upper()}] title: {c['title']}\n    url: {c['url']}"
        for i, c in enumerate(candidates)
    )

    response = client.chat.completions.create(
        model="deepseek-chat",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": USER_TEMPLATE.format(candidates=lines)},
        ],
        temperature=0.2,
    )

    raw = response.choices[0].message.content
    data = json.loads(raw)
    return data.get("items", [])
