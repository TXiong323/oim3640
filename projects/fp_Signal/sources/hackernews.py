import re
import time
import requests

API_URL = "https://hn.algolia.com/api/v1/search_by_date"

_WORD_BOUNDARY_KEYWORDS = [
    "ai", "llm", "gpt", "rag", "mcp", "llama",
]
_SUBSTRING_KEYWORDS = [
    "openai", "anthropic", "deepseek", "mistral", "gemini", "claude",
    "machine learning", "neural", "transformer", "diffusion",
    "fine-tun", "embedding", "inference", "copilot", "chatbot", "agent",
]

_WORD_PATTERN = re.compile(
    r"\b(" + "|".join(re.escape(k) for k in _WORD_BOUNDARY_KEYWORDS) + r")\b",
    re.IGNORECASE,
)

MIN_POINTS = 30
HOURS_BACK = 24


def _is_ai_related(title: str) -> bool:
    if _WORD_PATTERN.search(title):
        return True
    lower = title.lower()
    return any(kw in lower for kw in _SUBSTRING_KEYWORDS)


def fetch() -> list[dict]:
    cutoff = int(time.time()) - HOURS_BACK * 3600
    params = {
        "tags": "story",
        "numericFilters": f"points>={MIN_POINTS},created_at_i>{cutoff}",
        "hitsPerPage": 200,
    }
    resp = requests.get(API_URL, params=params, timeout=10)
    resp.raise_for_status()
    hits = resp.json().get("hits", [])

    stories = []
    for h in hits:
        title = h.get("title", "")
        if not _is_ai_related(title):
            continue
        hn_id = h["objectID"]
        stories.append({
            "source": "hn",
            "title": title,
            "url": h.get("url") or f"https://news.ycombinator.com/item?id={hn_id}",
            "metadata": {
                "points": h.get("points", 0),
                "comments": h.get("num_comments", 0),
                "hn_url": f"https://news.ycombinator.com/item?id={hn_id}",
            },
        })

    stories.sort(key=lambda s: s["metadata"]["points"], reverse=True)
    return stories
