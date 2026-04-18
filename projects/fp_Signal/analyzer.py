import json
import os
from openai import OpenAI

SYSTEM_PROMPT = """You are a strict content curator for a personal AI/tech digest.

KEEP (productivity-relevant):
- New tools, frameworks, SDKs, libraries (agent frameworks, AI coding tools, MCP servers)
- Claude Code / Cursor / Copilot skills or new MCP integrations
- Newly released models, API features, product launches
- Fast-rising GitHub projects
- Practical how-tos or tutorials that lead to building something
- Interesting new AI websites or services

DISCARD (not useful):
- Pricing, cost comparisons, token economics
- Pure discussion threads, rants, philosophy, "will AI replace X" debates
- Business news: funding rounds, acquisitions, leadership changes
- Policy, regulation, ethics debates
- Security vulnerabilities / CVEs (unless critical AI infrastructure)
- Retrospectives or outdated recaps

Rules:
- Return 5-7 items max. Fewer is fine. If nothing qualifies, return an empty list — never pad.
- why_it_matters must be ≤25 words, concrete: say what it IS, what it DOES, why it's useful.
- No filler phrases like "this reflects a growing trend" or "this is significant because".
- Return ONLY valid JSON, no markdown fences."""

USER_TEMPLATE = """Here are today's candidate stories. Filter and rank them. Return JSON only.

Candidates:
{candidates}

Return format:
{{
  "items": [
    {{"title": "...", "url": "...", "why_it_matters": "..."}}
  ]
}}"""


def analyze(stories: list[dict]) -> list[dict]:
    client = OpenAI(
        api_key=os.environ["DEEPSEEK_API_KEY"],
        base_url="https://api.deepseek.com",
    )

    candidates = "\n".join(
        f"{i+1}. {s['title']} — {s['url']}"
        for i, s in enumerate(stories)
    )

    response = client.chat.completions.create(
        model="deepseek-chat",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": USER_TEMPLATE.format(candidates=candidates)},
        ],
        temperature=0.2,
    )

    raw = response.choices[0].message.content
    data = json.loads(raw)
    return data.get("items", [])
