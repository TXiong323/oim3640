import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import date


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
            hn_meta = ""
            if s.get("points"):
                hn_meta = f"""
                <br><span style="font-size:12px;color:#aaa;">
                  {s['points']} pts &middot; {s.get('comments', 0)} comments &middot;
                  <a href="{s['hn_url']}" style="color:#aaa;">discuss</a>
                </span>"""
            rows += f"""
        <tr>
          <td style="padding:12px 0; border-bottom:1px solid #eee; vertical-align:top;">
            <span style="color:#bbb;font-size:12px;">{i}.&nbsp;</span>
            <a href="{s['url']}" style="font-size:15px;font-weight:600;color:#1a1a1a;text-decoration:none;">
              {s['title']}
            </a>
            {why_html}
            {hn_meta}
          </td>
        </tr>"""
        body = f"""
  <p style="color:#888;font-size:12px;">
    {len(stories)} picks from {candidate_count} candidates &middot; Hacker News last 24h
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
