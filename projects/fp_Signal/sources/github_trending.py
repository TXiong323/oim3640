import re
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://github.com/trending"
TIMEFRAMES = ["daily", "weekly"]

AI_KEYWORDS = [
    "ai", "llm", "llms", "gpt", "rag", "mcp", "agent", "agents",
    "openai", "anthropic", "deepseek", "mistral", "llama", "gemini", "claude",
    "machine learning", "neural", "transformer", "diffusion", "embedding",
    "copilot", "chatbot", "fine-tun", "inference",
]

MIN_CANDIDATES = 5


def _is_ai_related(text: str) -> bool:
    lower = text.lower()
    return any(kw in lower for kw in AI_KEYWORDS)


def _parse_stars(text: str) -> int:
    text = text.strip().replace(",", "").replace(" ", "")
    if "k" in text.lower():
        return int(float(text.lower().replace("k", "")) * 1000)
    try:
        return int(text)
    except ValueError:
        return 0


def _scrape(timeframe: str) -> list[dict]:
    resp = requests.get(
        BASE_URL,
        params={"since": timeframe},
        headers={"User-Agent": "Mozilla/5.0 (compatible; signal-digest/1.0)"},
        timeout=15,
    )
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    repos = []
    for article in soup.select("article.Box-row"):
        name_tag = article.select_one("h2 a")
        if not name_tag:
            continue
        full_name = name_tag.get("href", "").strip("/")
        if not full_name:
            continue

        desc_tag = article.select_one("p")
        description = desc_tag.get_text(strip=True) if desc_tag else ""

        lang_tag = article.select_one("[itemprop='programmingLanguage']")
        language = lang_tag.get_text(strip=True) if lang_tag else ""

        # Stars today (shown as "N stars today" in the footer span)
        stars_today = 0
        for span in article.select("span"):
            t = span.get_text(strip=True)
            if "stars today" in t or "star today" in t:
                stars_today = _parse_stars(t.split()[0])
                break

        # Total stars
        stars_total = 0
        star_link = article.select_one("a[href$='/stargazers']")
        if star_link:
            stars_total = _parse_stars(star_link.get_text(strip=True))

        repos.append({
            "full_name": full_name,
            "description": description,
            "language": language,
            "stars_today": stars_today,
            "stars_total": stars_total,
            "timeframe": timeframe,
        })
    return repos


def fetch() -> list[dict]:
    seen: set[str] = set()
    all_repos: list[dict] = []

    for tf in TIMEFRAMES:
        for r in _scrape(tf):
            if r["full_name"] not in seen:
                seen.add(r["full_name"])
                all_repos.append(r)

    # Filter to AI-related by name or description
    filtered = [
        r for r in all_repos
        if _is_ai_related(r["full_name"]) or _is_ai_related(r["description"])
    ]

    # Fall back to all trending if too few match
    pool = filtered if len(filtered) >= MIN_CANDIDATES else all_repos

    results = []
    for r in pool:
        owner_repo = r["full_name"]
        desc = f" — {r['description']}" if r["description"] else ""
        results.append({
            "source": "github",
            "title": f"{owner_repo}{desc}",
            "url": f"https://github.com/{owner_repo}",
            "metadata": {
                "stars_today": r["stars_today"],
                "stars_total": r["stars_total"],
                "language": r["language"],
                "timeframe": r["timeframe"],
            },
        })

    return results
