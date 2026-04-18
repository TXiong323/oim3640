from datetime import datetime, timezone, timedelta
import feedparser
import requests
from bs4 import BeautifulSoup

DAYS_BACK = 7

_HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; signal-digest/1.0)"}


def _cutoff() -> datetime:
    return datetime.now(timezone.utc) - timedelta(days=DAYS_BACK)


def _parse_rss_date(entry) -> datetime | None:
    for attr in ("published_parsed", "updated_parsed"):
        t = getattr(entry, attr, None)
        if t:
            try:
                return datetime(*t[:6], tzinfo=timezone.utc)
            except Exception:
                pass
    return None


def _fetch_openai() -> list[dict]:
    feed = feedparser.parse("https://openai.com/blog/rss.xml")
    cutoff = _cutoff()
    results = []
    for entry in feed.entries:
        pub = _parse_rss_date(entry)
        if pub and pub < cutoff:
            continue
        title = entry.get("title", "").strip()
        url = entry.get("link", "").strip()
        if not title or not url:
            continue
        published = pub.strftime("%b %d") if pub else ""
        results.append({
            "source": "openai",
            "title": title,
            "url": url,
            "metadata": {"published": published},
        })
    return results


def _fetch_anthropic() -> list[dict]:
    resp = requests.get(
        "https://www.anthropic.com/news",
        headers=_HEADERS,
        timeout=15,
    )
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    cutoff = _cutoff()
    results = []
    seen: set[str] = set()

    for a in soup.select("a[href^='/news/']"):
        href = a.get("href", "")
        if not href or href in seen:
            continue
        seen.add(href)

        title_tag = a.select_one("h2, h3")
        title = title_tag.get_text(strip=True) if title_tag else ""
        if not title:
            continue

        time_tag = a.select_one("time")
        published_str = time_tag.get_text(strip=True) if time_tag else ""

        # Parse the date to enforce the 7-day window
        pub = None
        if published_str:
            for fmt in ("%b %d, %Y", "%B %d, %Y"):
                try:
                    pub = datetime.strptime(published_str, fmt).replace(tzinfo=timezone.utc)
                    break
                except ValueError:
                    pass
        if pub and pub < cutoff:
            continue

        published_short = pub.strftime("%b %d") if pub else published_str[:6]
        url = "https://www.anthropic.com" + href
        results.append({
            "source": "anthropic",
            "title": title,
            "url": url,
            "metadata": {"published": published_short},
        })

    return results


def fetch() -> list[dict]:
    results = []
    try:
        results += _fetch_anthropic()
    except Exception as e:
        print(f"  [blogs] Anthropic fetch failed: {e}")
    try:
        results += _fetch_openai()
    except Exception as e:
        print(f"  [blogs] OpenAI fetch failed: {e}")
    return results
