import re
from datetime import date, timedelta
from pathlib import Path

ARCHIVE_DIR = Path(__file__).parent / ".." / ".." / "docs"
KEEP_DAYS = 14

_DATE_RE = re.compile(r"^(daily|weekly)-(\d{4}-\d{2}-\d{2})\.html$")

_BACK_LINK = (
    '<p style="font-size:13px;margin-bottom:16px;">'
    '<a href="./index.html" style="color:#888;text-decoration:none;">← Back to archive</a>'
    "</p>\n  "
)


def _inject_back_link(html: str) -> str:
    return re.sub(r"(<body[^>]*>)", r"\1\n  " + _BACK_LINK, html, count=1)


def _list_archive_files() -> list[tuple[date, str, Path]]:
    entries = []
    for f in ARCHIVE_DIR.iterdir():
        m = _DATE_RE.match(f.name)
        if not m:
            continue
        try:
            d = date.fromisoformat(m.group(2))
            entries.append((d, m.group(1), f))
        except ValueError:
            pass
    entries.sort(key=lambda x: x[0], reverse=True)
    return entries


def _clean_old(today: date) -> None:
    cutoff = today - timedelta(days=KEEP_DAYS)
    for d, _, path in _list_archive_files():
        if d < cutoff:
            path.unlink()


def _rebuild_index() -> None:
    entries = _list_archive_files()

    if not entries:
        rows_html = '<p style="color:#888;font-size:14px;padding:16px 0;">No digests yet.</p>'
    else:
        rows = ""
        for d, mode, path in entries:
            label = "日报" if mode == "daily" else "周报"
            rows += f"""
        <tr>
          <td style="padding:10px 0; border-bottom:1px solid #eee;">
            <a href="./{path.name}" style="font-size:15px;font-weight:600;color:#1a1a1a;text-decoration:none;">
              {d.isoformat()}
            </a>
            <span style="font-size:13px;color:#888;margin-left:10px;">{label}</span>
          </td>
        </tr>"""
        rows_html = f'<table width="100%" cellpadding="0" cellspacing="0">{rows}</table>'

    index_html = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>Signal · Archive</title></head>
<body style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;max-width:640px;margin:0 auto;padding:20px;color:#1a1a1a;">
  <h2 style="border-bottom:2px solid #1a1a1a;padding-bottom:8px;">Signal &mdash; Archive</h2>
  <p style="color:#888;font-size:13px;margin-bottom:16px;">Last {KEEP_DAYS} days of digests</p>
  {rows_html}
  <p style="color:#ccc;font-size:11px;margin-top:24px;">Signal &mdash; built for OIM3640</p>
</body>
</html>"""

    (ARCHIVE_DIR / "index.html").write_text(index_html, encoding="utf-8")


def save(html: str, mode: str, run_date: date) -> None:
    ARCHIVE_DIR.mkdir(exist_ok=True)
    filename = f"{mode}-{run_date.isoformat()}.html"
    (ARCHIVE_DIR / filename).write_text(_inject_back_link(html), encoding="utf-8")
    _clean_old(run_date)
    _rebuild_index()
    print(f"Archived to docs/{filename}")
