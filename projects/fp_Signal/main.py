from dotenv import load_dotenv
load_dotenv()

from datetime import date
from sources import hackernews, github_trending, blogs
import analyzer
import email_sender


def main():
    print("Fetching Hacker News...")
    hn_items = hackernews.fetch()
    print(f"  {len(hn_items)} candidates")

    print("Fetching GitHub Trending...")
    gh_items = github_trending.fetch()
    print(f"  {len(gh_items)} candidates")

    print("Fetching Anthropic + OpenAI blogs...")
    blog_items = blogs.fetch()
    print(f"  {len(blog_items)} candidates")

    candidates = hn_items + gh_items + blog_items
    print(f"Total candidates: {len(candidates)}")

    print("Analyzing with DeepSeek...")
    picks = analyzer.analyze(candidates)
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
            "metadata": c.get("metadata", {}),
        })

    subject = f"Signal: AI/Tech Digest — {date.today().strftime('%b %d, %Y')}"
    html = email_sender.build_html(stories, candidate_count=len(candidates))
    email_sender.send(subject, html)


if __name__ == "__main__":
    main()
