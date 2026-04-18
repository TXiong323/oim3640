import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import date


def build_html(stories: list[dict]) -> str:
    today = date.today().strftime("%B %d, %Y")
    rows = ""
    for i, s in enumerate(stories, 1):
        rows += f"""
        <tr>
          <td style="padding:10px 0; border-bottom:1px solid #eee; vertical-align:top;">
            <span style="color:#888;font-size:12px;">{i}.</span>
            <a href="{s['url']}" style="font-size:15px;font-weight:600;color:#1a1a1a;text-decoration:none;">
              {s['title']}
            </a><br>
            <span style="font-size:12px;color:#888;">
              {s['points']} pts &middot;
              {s['comments']} comments &middot;
              <a href="{s['hn_url']}" style="color:#888;">discuss</a> &middot;
              {s['source']}
            </span>
          </td>
        </tr>"""

    html = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;max-width:640px;margin:0 auto;padding:20px;color:#1a1a1a;">
  <h2 style="border-bottom:2px solid #1a1a1a;padding-bottom:8px;">
    Signal &mdash; AI/Tech Digest &middot; {today}
  </h2>
  <p style="color:#555;font-size:13px;">
    {len(stories)} AI-related stories from Hacker News (last 24h, &ge;50 pts), sorted by score.
  </p>
  <table width="100%" cellpadding="0" cellspacing="0">
    {rows}
  </table>
  <p style="color:#aaa;font-size:11px;margin-top:20px;">Signal &mdash; built for OIM3640</p>
</body>
</html>"""
    return html


def send(subject: str, html_body: str) -> None:
    gmail = os.environ["GMAIL_ADDRESS"]
    password = os.environ["GMAIL_APP_PASSWORD"]
    to_addr = os.environ["TO_EMAIL"]

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = gmail
    msg["To"] = to_addr
    msg.attach(MIMEText(html_body, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(gmail, password)
        server.sendmail(gmail, to_addr, msg.as_string())
    print(f"Email sent to {to_addr}")
