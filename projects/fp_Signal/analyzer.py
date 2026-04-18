import json
import os
from openai import OpenAI

SYSTEM_PROMPT = """You are a strict content curator for a personal AI/tech digest.

Candidates come from three sources: Hacker News (HN), GitHub Trending (GITHUB), and arXiv (ARXIV).
Apply the same judgment to all three.

KEEP (productivity-relevant):
- New tools, frameworks, SDKs, libraries (agent frameworks, AI coding tools, MCP servers)
- Claude Code / Cursor / Copilot skills or new MCP integrations
- Newly released models, API features, product launches
- Fast-rising GitHub repos that are genuinely useful or novel
- Practical how-tos or tutorials that lead to building something
- Interesting new AI websites or services
- arXiv papers that introduce a new method, tool, or reproducible technique useful to practitioners

DISCARD (not useful):
- Pricing, cost comparisons, token economics
- Pure discussion threads, rants, philosophy, "will AI replace X" debates
- Business news: funding rounds, acquisitions, leadership changes
- Policy, regulation, ethics debates
- Security vulnerabilities / CVEs (unless critical AI infrastructure)
- Retrospectives or outdated recaps
- Generic "awesome-X" lists with no new content
- Games, game engines, game development tools (unless it's a general AI framework that happens to use a game as demo)
- Entertainment-focused AI apps (AI-generated art for its own sake, AI voice acting toys, etc.)
- Purely theoretical arXiv papers with no practical application
- Anything not directly useful to a developer/programmer

Rules:
- Return 5-7 items max. Fewer is fine. If nothing qualifies, return an empty list — never pad.
- why_it_matters must be written in Chinese (≤40 Chinese characters), concrete: say what it IS, what it DOES, why it's useful.
- Keep product names, tool names, and proper nouns in their original English (e.g. Claude Code, MCP, SDK, API, agent, LLM, framework, repo, UI — do NOT translate these).
- Example of good why_it_matters: "Claude Code 的 Android 逆向分析 skill，把 AI 编程能力扩展到安全分析领域。"
- Example of bad why_it_matters: "这反映了一个新兴趋势..." or "Claude 代码的安卓反向工程技能..."
- No filler phrases. Be specific and direct.
- The "title" field in your response must be the exact original title — do not append URLs or modify it.
- Return ONLY valid JSON, no markdown fences."""

USER_TEMPLATE = """Here are today's candidates. Filter and rank them. Return JSON only.

Candidates:
{candidates}

Return format:
{{
  "items": [
    {{"title": "...", "url": "...", "why_it_matters": "..."}}
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
