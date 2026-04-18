from dotenv import load_dotenv
load_dotenv()

from datetime import date
from sources import hackernews
import analyzer
import email_sender


def main():
    print("Fetching Hacker News...")
    candidates = hackernews.fetch()
    print(f"  {len(candidates)} AI-related candidates")

    print("Analyzing with DeepSeek...")
    picks = analyzer.analyze(candidates)
    print(f"  {len(picks)} picks after filtering")

    # Merge DeepSeek picks with HN metadata (points, comments, hn_url)
    hn_index = {s["url"]: s for s in candidates}
    stories = []
    for pick in picks:
        meta = hn_index.get(pick["url"], {})
        stories.append({
            "title": pick["title"],
            "url": pick["url"],
            "why_it_matters": pick.get("why_it_matters", ""),
            "points": meta.get("points", 0),
            "comments": meta.get("comments", 0),
            "hn_url": meta.get("hn_url", pick["url"]),
        })

    subject = f"Signal: AI/Tech Digest — {date.today().strftime('%b %d, %Y')}"
    html = email_sender.build_html(stories, candidate_count=len(candidates))
    email_sender.send(subject, html)


if __name__ == "__main__":
    main()
