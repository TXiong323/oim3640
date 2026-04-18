from datetime import datetime, timezone, timedelta
import feedparser

# Add or remove channels here
CHANNELS = [
    ("Matt Wolfe",      "UChpleBmo18P08aKCIgti38g"),
    ("Matthew Berman",  "UCawZsQWqfGSbCI5yjkdVkTA"),
    ("Fireship",        "UCsBjURrPoezykLs9EqgamOA"),
    ("Theo (t3.gg)",    "UCbRP3c757lWg9M-U7TyEkXA"),
]

# Fireship covers many topics — only keep AI-related videos
FIRESHIP_KEYWORDS = [
    "ai", "claude", "gpt", "llm", "cursor", "agent", "openai",
    "anthropic", "copilot", "deepseek", "gemini", "mcp", "vibe",
]
FIRESHIP_NAME = "Fireship"

RSS_URL = "https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"


def _is_fireship_relevant(title: str) -> bool:
    lower = title.lower()
    return any(kw in lower for kw in FIRESHIP_KEYWORDS)


def _parse_date(entry) -> datetime | None:
    for attr in ("published_parsed", "updated_parsed"):
        t = getattr(entry, attr, None)
        if t:
            try:
                return datetime(*t[:6], tzinfo=timezone.utc)
            except Exception:
                pass
    return None


def fetch(hours_back: int = 24) -> list[dict]:
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours_back)
    results = []

    for channel_name, channel_id in CHANNELS:
        url = RSS_URL.format(channel_id=channel_id)
        try:
            feed = feedparser.parse(url)
            if feed.get("status", 200) >= 400:
                print(f"  [youtube] {channel_name}: HTTP {feed.get('status')} — skipping")
                continue
        except Exception as e:
            print(f"  [youtube] {channel_name}: fetch error — {e}")
            continue

        for entry in feed.entries:
            pub = _parse_date(entry)
            if pub and pub < cutoff:
                continue

            title = entry.get("title", "").strip()
            link = entry.get("link", "").strip()
            if not title or not link:
                continue

            if channel_name == FIRESHIP_NAME and not _is_fireship_relevant(title):
                continue

            published = pub.strftime("%b %d") if pub else ""
            results.append({
                "source": "youtube",
                "title": title,
                "url": link,
                "metadata": {
                    "channel": channel_name,
                    "published": published,
                },
            })

    return results
