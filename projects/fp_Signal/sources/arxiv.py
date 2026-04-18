import re
import feedparser

FEEDS = [
    ("http://arxiv.org/rss/cs.AI", "cs.AI"),
    ("http://arxiv.org/rss/cs.CL", "cs.CL"),
]

MAX_CANDIDATES = 20

AI_KEYWORDS = [
    "agent", "agents", "llm", "llms", "tool", "tools", "code", "coding",
    "reasoning", "multimodal", "rag", "retrieval", "fine-tun", "instruction",
    "benchmark", "inference", "mcp", "function call", "chain-of-thought",
    "planning", "workflow", "autonomous", "copilot", "assistant",
]

_ARXIV_ID_RE = re.compile(r"arxiv\.org/abs/([\d.]+)")


def _extract_id(url: str) -> str:
    m = _ARXIV_ID_RE.search(url)
    return m.group(1) if m else url


def _format_authors(entry) -> str:
    tags = getattr(entry, "tags", [])
    authors = []
    for t in tags:
        if hasattr(t, "label") and t.label:
            authors.append(t.label)

    # feedparser puts authors in entry.author or entry.authors
    if not authors:
        raw = getattr(entry, "author", "")
        if raw:
            authors = [a.strip() for a in raw.split(",")]

    if not authors:
        return ""
    if len(authors) <= 2:
        return ", ".join(authors)
    return f"{authors[0]}, {authors[1]} et al."


def _is_relevant(title: str, summary: str) -> bool:
    text = (title + " " + summary).lower()
    return any(kw in text for kw in AI_KEYWORDS)


def fetch() -> list[dict]:
    seen: set[str] = set()
    candidates: list[dict] = []

    for feed_url, category in FEEDS:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries:
            arxiv_id = _extract_id(entry.get("link", ""))
            if arxiv_id in seen:
                continue
            seen.add(arxiv_id)

            title = entry.get("title", "").replace("\n", " ").strip()
            summary = entry.get("summary", "")
            link = entry.get("link", "")

            if not _is_relevant(title, summary):
                continue

            authors = _format_authors(entry)
            candidates.append({
                "source": "arxiv",
                "title": title,
                "url": link,
                "metadata": {
                    "authors": authors,
                    "category": category,
                },
            })

            if len(candidates) >= MAX_CANDIDATES:
                break
        if len(candidates) >= MAX_CANDIDATES:
            break

    return candidates
