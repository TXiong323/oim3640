from dotenv import load_dotenv
load_dotenv()

import sys
from datetime import date, timedelta
from sources import hackernews, github_trending, blogs, youtube, producthunt
import analyzer
import archiver
import dedup
import email_sender


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

    # Track which sources actually have items (for the summary line)
    active_sources = {c["source"] for c in candidates}

    # Cross-day dedup: annotate each candidate with how many times it's been seen
    history = dedup.get_historical_urls()
    for c in candidates:
        c["seen_count"] = history.get(c["url"], 0)

    print("Analyzing with DeepSeek...")
    result = analyzer.analyze(candidates, mode=mode)
    picks = result["items"]
    summary = result["summary"]
    print(f"  {len(picks)} picks after filtering")

    meta_index = {c["url"]: c for c in candidates}
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
    )
    email_sender.send(subject, html)
    archiver.save(html, mode, date.today())


if __name__ == "__main__":
    main()
