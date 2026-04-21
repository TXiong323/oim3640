import os
from datetime import datetime, timezone, timedelta
import requests

TOKEN_URL = "https://api.producthunt.com/v2/oauth/token"
GQL_URL = "https://api.producthunt.com/v2/api/graphql"

# GraphQL query: AI topic posts, sorted by votes, with time filter
_QUERY = """
query($postedAfter: DateTime!, $first: Int!) {
  posts(
    topic: "artificial-intelligence"
    order: VOTES
    postedAfter: $postedAfter
    first: $first
  ) {
    edges {
      node {
        name
        tagline
        url
        votesCount
        createdAt
      }
    }
  }
}
"""


def _get_token() -> str:
    resp = requests.post(
        TOKEN_URL,
        json={
            "client_id": os.environ["PRODUCTHUNT_CLIENT_ID"],
            "client_secret": os.environ["PRODUCTHUNT_CLIENT_SECRET"],
            "grant_type": "client_credentials",
        },
        timeout=10,
    )
    resp.raise_for_status()
    return resp.json()["access_token"]


def fetch(hours_back: int = 24) -> list[dict]:
    token = _get_token()
    posted_after = (
        datetime.now(timezone.utc) - timedelta(hours=hours_back)
    ).strftime("%Y-%m-%dT%H:%M:%SZ")

    resp = requests.post(
        GQL_URL,
        json={"query": _QUERY, "variables": {"postedAfter": posted_after, "first": 20}},
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        timeout=15,
    )
    resp.raise_for_status()

    edges = resp.json().get("data", {}).get("posts", {}).get("edges", [])
    results = []
    for edge in edges:
        node = edge.get("node", {})
        name = node.get("name", "")
        tagline = node.get("tagline", "")
        url = node.get("url", "")
        votes = node.get("votesCount", 0)
        if not name or not url:
            continue
        results.append({
            "source": "producthunt",
            "title": f"{name} — {tagline}" if tagline else name,
            "url": url,
            "metadata": {
                "votes": votes,
                "tagline": tagline,
            },
        })

    return results
