import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import date

SOURCE_LABEL = {
    "hn": "Hacker News",
    "github": "GitHub Trending",
}


def _meta_line(story: dict) -> str:
    source = story.get("source", "")
    meta = story.get("metadata", {})
    label = SOURCE_LABEL.get(source, source)

    if source == "hn":
        pts = meta.get("points", 0)
        comments = meta.get("comments", 0)
        hn_url = meta.get("hn_url", story["url"])
        return (
            f'{pts} pts &middot; {comments} comments &middot; '
            f'<a href="{hn_url}" style="color:#aaa;">讨论</a> &middot; {label}'
        )
    elif source == "github":
        lang = meta.get("language", "")
        stars_today = meta.get("stars_today", 0)
        stars_total = meta.get("stars_total", 0)
        parts = []
        if stars_today:
            parts.append(f"+{stars_today:,} 今日 stars")
        if stars_total:
            parts.append(f"{stars_total:,} 累计")
        if lang:
            parts.append(lang)
        parts.append(label)
        return " &middot; ".join(parts)
    return label


def build_html(stories: list[dict], candidate_count: int = 0) -> str:
    today = date.today().strftime("%B %d, %Y")

    if not stories:
        body = """
        <p style="color:#555;font-size:15px;padding:20px 0;">
          Nothing worth reading today. Check back tomorrow.
        </p>"""
    else:
        rows = ""
        for i, s in enumerate(stories, 1):
            why = s.get("why_it_matters", "")
            why_html = (
                f'<br><em style="font-size:12px;color:#888;">{why}</em>'
                if why else ""
            )
            meta_html = _meta_line(s)
            rows += f"""
        <tr>
          <td style="padding:12px 0; border-bottom:1px solid #eee; vertical-align:top;">
            <span style="color:#bbb;font-size:12px;">{i}.&nbsp;</span>
            <a href="{s['url']}" style="font-size:15px;font-weight:600;color:#1a1a1a;text-decoration:none;">
              {s['title']}
            </a>
            {why_html}
            <br><span style="font-size:12px;color:#aaa;">{meta_html}</span>
          </td>
        </tr>"""

        body = f"""
  <p style="color:#888;font-size:12px;">
    从 {candidate_count} 条候选中精选 {len(stories)} 条 &middot; HN + GitHub Trending &middot; 近 24 小时
  </p>
  <table width="100%" cellpadding="0" cellspacing="0">
    {rows}
  </table>"""

    html = f"""<!DOCTYPE html>
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
    return html


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
