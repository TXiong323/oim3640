import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import date

SOURCE_LABEL = {
    "hn": "Hacker News",
    "show_hn": "Show HN",
    "github": "GitHub Trending",
    "anthropic": "Anthropic blog",
    "openai": "OpenAI blog",
    "youtube": "YouTube",
    "producthunt": "Product Hunt",
}

# Weekly grouping order
_GROUPS = [
    ("📺 YouTube 视频",  lambda s: s["source"] == "youtube"),
    ("🚀 Product Hunt 新品", lambda s: s["source"] == "producthunt"),
    ("🐙 GitHub 项目",   lambda s: s["source"] == "github"),
    ("📰 文章 / 博客",    lambda s: s["source"] in ("hn", "show_hn", "anthropic", "openai")),
]


def _meta_line(story: dict) -> str:
    source = story.get("source", "")
    meta = story.get("metadata", {})
    label = SOURCE_LABEL.get(source, source)

    if source in ("hn", "show_hn"):
        pts = meta.get("points", 0)
        comments = meta.get("comments", 0)
        hn_url = meta.get("hn_url", story["url"])
        return (
            f'{pts} pts &middot; {comments} comments &middot; '
            f'<a href="{hn_url}" style="color:#aaa;">discuss</a> &middot; {label}'
        )
    elif source == "producthunt":
        votes = meta.get("votes", 0)
        return f'{votes} votes &middot; {label}'
    elif source == "github":
        lang = meta.get("language", "")
        stars_today = meta.get("stars_today", 0)
        stars_total = meta.get("stars_total", 0)
        parts = []
        if stars_today:
            parts.append(f"+{stars_today:,} stars today")
        if stars_total:
            parts.append(f"{stars_total:,} total")
        if lang:
            parts.append(lang)
        parts.append(label)
        return " &middot; ".join(parts)
    elif source in ("anthropic", "openai"):
        published = meta.get("published", "")
        parts = [published, label] if published else [label]
        return " &middot; ".join(parts)
    elif source == "youtube":
        channel = meta.get("channel", "")
        published = meta.get("published", "")
        parts = []
        if channel:
            parts.append(channel)
        if published:
            parts.append(published)
        parts.append(label)
        return " &middot; ".join(parts)
    return label


def _story_row(i: int, s: dict) -> str:
    why = s.get("why_it_matters", "")
    why_html = (
        f'<br><em style="font-size:13px;color:#666;line-height:1.5;">{why}</em>'
        if why else ""
    )
    meta_html = _meta_line(s)
    return f"""
        <tr>
          <td style="padding:12px 0; border-bottom:1px solid #eee; vertical-align:top;">
            <span style="color:#bbb;font-size:12px;">{i}.&nbsp;</span>
            <a href="{s['url']}" style="font-size:15px;font-weight:600;color:#1a1a1a;text-decoration:none;">{s['title']}</a>
            {why_html}
            <br><span style="font-size:12px;color:#aaa;">{meta_html}</span>
          </td>
        </tr>"""


# Display name for each source in the summary line
_SOURCE_DISPLAY = {
    "hn": "HN",
    "show_hn": "Show HN",
    "github": "GitHub",
    "anthropic": "Blogs",
    "openai": "Blogs",
    "youtube": "YouTube",
    "producthunt": "Product Hunt",
}
# Deduplicated order for summary line
_SOURCE_ORDER = ["hn", "show_hn", "youtube", "producthunt", "github", "anthropic", "openai"]


def _sources_label(active_sources: set[str]) -> str:
    seen: set[str] = set()
    parts = []
    for src in _SOURCE_ORDER:
        if src in active_sources:
            label = _SOURCE_DISPLAY[src]
            if label not in seen:
                seen.add(label)
                parts.append(label)
    return " + ".join(parts) if parts else "multiple sources"


def _daily_body(stories: list[dict], candidate_count: int, active_sources: set[str]) -> str:
    if not stories:
        return '<p style="color:#555;font-size:15px;padding:20px 0;">Nothing worth reading today. Check back tomorrow.</p>'
    rows = "".join(_story_row(i, s) for i, s in enumerate(stories, 1))
    src_label = _sources_label(active_sources)
    return f"""
  <p style="color:#888;font-size:12px;">
    {len(stories)} picks from {candidate_count} candidates &middot; {src_label} &middot; last 24h
  </p>
  <table width="100%" cellpadding="0" cellspacing="0">{rows}</table>"""


def _weekly_body(stories: list[dict], candidate_count: int, summary: str, active_sources: set[str]) -> str:
    if not stories:
        return '<p style="color:#555;font-size:15px;padding:20px 0;">Nothing worth reading this week.</p>'

    summary_html = ""
    if summary:
        summary_html = f"""
  <div style="background:#f7f7f7;border-left:3px solid #1a1a1a;padding:12px 16px;margin:16px 0;font-size:14px;line-height:1.7;color:#333;">
    {summary}
  </div>"""

    group_html = ""
    counter = 1
    for group_title, predicate in _GROUPS:
        group_stories = [s for s in stories if predicate(s)]
        if not group_stories:
            continue
        rows = "".join(_story_row(counter + j, s) for j, s in enumerate(group_stories))
        counter += len(group_stories)
        group_html += f"""
  <h3 style="font-size:14px;font-weight:700;color:#555;margin:24px 0 4px;">{group_title}（{len(group_stories)} 个）</h3>
  <table width="100%" cellpadding="0" cellspacing="0">{rows}</table>"""

    src_label = _sources_label(active_sources)
    return f"""
  <p style="color:#888;font-size:12px;">
    {len(stories)} picks from {candidate_count} candidates &middot; {src_label} &middot; last 7d
  </p>
  {summary_html}
  {group_html}"""


def build_html(
    stories: list[dict],
    candidate_count: int = 0,
    mode: str = "daily",
    summary: str = "",
    active_sources: set[str] | None = None,
) -> str:
    if active_sources is None:
        active_sources = set()
    today = date.today().strftime("%B %d, %Y")

    if mode == "weekly":
        body = _weekly_body(stories, candidate_count, summary, active_sources)
    else:
        body = _daily_body(stories, candidate_count, active_sources)

    return f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;max-width:640px;margin:0 auto;padding:20px;color:#1a1a1a;">
  <h2 style="border-bottom:2px solid #1a1a1a;padding-bottom:8px;">
    Signal &mdash; AI/Tech Digest &middot; {today}
  </h2>
  {body}
  <p style="color:#ccc;font-size:11px;margin-top:24px;">Signal &mdash; built for OIM3640</p>
</body>
</html>"""


def send(subject: str, html_body: str) -> None:
    gmail = os.environ["GMAIL_ADDRESS"]
    password = os.environ["GMAIL_APP_PASSWORD"]
    to_addr = os.environ["RECIPIENT_EMAIL"]

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = gmail
    msg["To"] = to_addr
    msg.attach(MIMEText(html_body, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(gmail, password)
        server.sendmail(gmail, to_addr, msg.as_string())
    print(f"Email sent to {to_addr}")
