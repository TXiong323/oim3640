from dotenv import load_dotenv
load_dotenv()

from datetime import date
from sources import hackernews
import email_sender


def main():
    print("Fetching Hacker News...")
    stories = hackernews.fetch()
    print(f"  Found {len(stories)} AI-related stories")

    if not stories:
        print("No stories found — skipping email.")
        return

    subject = f"Signal: AI/Tech Digest — {date.today().strftime('%b %d, %Y')}"
    html = email_sender.build_html(stories)
    email_sender.send(subject, html)


if __name__ == "__main__":
    main()
