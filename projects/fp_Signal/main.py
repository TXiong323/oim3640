from dotenv import load_dotenv
load_dotenv()

import sys
from datetime import date, timedelta
from sources import hackernews, github_trending, blogs, youtube, producthunt
import analyzer
import archiver
import dedup
import email_sender


def _build_stories(picks: list[dict], meta_index: dict) -> list[dict]:
    stories = []
    for pick in picks:
        c = meta_index.get(pick["url"], {})
        stories.append({
            "source": c.get("source", ""),
            "title": pick.get("display_title") or pick["title"],
            "url": pick["url"],
            "why_it_matters": pick.get("why_it_matters", ""),
            "seen_before": pick.get("seen_before", 0),
            "metadata": c.get("metadata", {}),
        })
    return stories


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "daily"
    if mode not in ("daily", "weekly"):
        print(f"Unknown mode '{mode}'. Use: daily | weekly")
        sys.exit(1)

    hours_back = 24 if mode == "daily" else 7 * 24

    print(f"Mode: {mode} ({hours_back}h window)")

    print("Fetching Hacker News...")
    hn_items = hackernews.fetch(hours_back=hours_back)
    print(f"  {len(hn_items)} candidates")

    print("Fetching Show HN...")
    show_hn_items = hackernews.fetch_show_hn(hours_back=hours_back)
    print(f"  {len(show_hn_items)} candidates")

    print("Fetching GitHub Trending...")
    gh_items = github_trending.fetch()
    print(f"  {len(gh_items)} candidates")

    print("Fetching Anthropic + OpenAI blogs...")
    blog_items = blogs.fetch()
    print(f"  {len(blog_items)} candidates")

    print("Fetching YouTube...")
    yt_items = youtube.fetch(hours_back=hours_back)
    print(f"  {len(yt_items)} candidates")

    print("Fetching Product Hunt...")
    try:
        ph_items = producthunt.fetch(hours_back=hours_back)
        print(f"  {len(ph_items)} candidates")
    except Exception as e:
        print(f"  Product Hunt failed: {e}")
        ph_items = []

    candidates = hn_items + show_hn_items + gh_items + blog_items + yt_items + ph_items
    print(f"Total candidates: {len(candidates)}")

    active_sources = {c["source"] for c in candidates}

    history = dedup.get_historical_urls()
    for c in candidates:
        c["seen_count"] = history.get(c["url"], 0)

    headline_stories = []
    if mode == "daily":
        # Build a 7-day pool for the headlines section by extending HN/ShowHN window.
        # Blogs already cover 7 days; GitHub/YT/PH from the 24h fetch are included as-is.
        print("Fetching 7-day HN pool for headlines...")
        hn_7d = hackernews.fetch(hours_back=7 * 24)
        show_hn_7d = hackernews.fetch_show_hn(hours_back=7 * 24)
        print(f"  {len(hn_7d) + len(show_hn_7d)} HN candidates (7d)")

        seen_urls: set[str] = set()
        candidates_7d: list[dict] = []
        for c in hn_7d + show_hn_7d + gh_items + blog_items + yt_items + ph_items:
            if c["url"] not in seen_urls:
                seen_urls.add(c["url"])
                candidates_7d.append(c)
        for c in candidates_7d:
            c["seen_count"] = history.get(c["url"], 0)

        print("Analyzing headlines with DeepSeek...")
        headline_result = analyzer.analyze_headlines(candidates_7d)
        headline_picks = headline_result["items"]
        print(f"  {len(headline_picks)} headline picks")

        meta_index_7d = {c["url"]: c for c in candidates_7d}
        headline_stories = _build_stories(headline_picks, meta_index_7d)

        # Exclude headline URLs from today's fresh candidates
        headline_urls = {s["url"] for s in headline_stories}
        candidates = [c for c in candidates if c["url"] not in headline_urls]

    print("Analyzing with DeepSeek...")
    result = analyzer.analyze(candidates, mode=mode)
    picks = result["items"]
    summary = result["summary"]
    print(f"  {len(picks)} picks after filtering")

    meta_index = {c["url"]: c for c in candidates}
    stories = _build_stories(picks, meta_index)

    if mode == "weekly":
        today = date.today()
        week_start = today - timedelta(days=6)
        date_range = f"{week_start.strftime('%b %d')} – {today.strftime('%b %d, %Y')}"
        subject = f"Signal · 周报 · {date_range}"
    else:
        subject = f"Signal · 日报 · {date.today().strftime('%b %d, %Y')}"

    html = email_sender.build_html(
        stories,
        candidate_count=len(candidates),
        mode=mode,
        summary=summary,
        active_sources=active_sources,
        headline_stories=headline_stories,
    )
    email_sender.send(subject, html)
    archiver.save(html, mode, date.today())


if __name__ == "__main__":
    main()
