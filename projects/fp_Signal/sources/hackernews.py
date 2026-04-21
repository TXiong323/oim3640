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
MIN_POINTS_SHOW_HN = 20


def _is_ai_related(title: str) -> bool:
    if _WORD_PATTERN.search(title):
        return True
    lower = title.lower()
    return any(kw in lower for kw in _SUBSTRING_KEYWORDS)


def _build_item(h: dict, source: str) -> dict:
    hn_id = h["objectID"]
    return {
        "source": source,
        "title": h.get("title", ""),
        "url": h.get("url") or f"https://news.ycombinator.com/item?id={hn_id}",
        "metadata": {
            "points": h.get("points", 0),
            "comments": h.get("num_comments", 0),
            "hn_url": f"https://news.ycombinator.com/item?id={hn_id}",
        },
    }


def fetch(hours_back: int = 24) -> list[dict]:
    cutoff = int(time.time()) - hours_back * 3600
    params = {
        "tags": "story",
        "numericFilters": f"points>={MIN_POINTS},created_at_i>{cutoff}",
        "hitsPerPage": 200,
    }
    resp = requests.get(API_URL, params=params, timeout=10)
    resp.raise_for_status()

    stories = [
        _build_item(h, "hn")
        for h in resp.json().get("hits", [])
        if _is_ai_related(h.get("title", ""))
    ]
    stories.sort(key=lambda s: s["metadata"]["points"], reverse=True)
    return stories


def fetch_show_hn(hours_back: int = 24) -> list[dict]:
    cutoff = int(time.time()) - hours_back * 3600
    params = {
        "tags": "show_hn",
        "numericFilters": f"points>={MIN_POINTS_SHOW_HN},created_at_i>{cutoff}",
        "hitsPerPage": 200,
    }
    resp = requests.get(API_URL, params=params, timeout=10)
    resp.raise_for_status()

    stories = [
        _build_item(h, "show_hn")
        for h in resp.json().get("hits", [])
        if _is_ai_related(h.get("title", ""))
    ]
    stories.sort(key=lambda s: s["metadata"]["points"], reverse=True)
    return stories
