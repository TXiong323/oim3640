import re
from collections import defaultdict
from pathlib import Path

from archiver import ARCHIVE_DIR

_URL_RE = re.compile(r'<a href="(https?://[^"]+)"')
_ARCHIVE_GLOB = ["daily-*.html", "weekly-*.html"]


def get_historical_urls() -> dict[str, int]:
    """Return {url: count} for all story URLs seen in existing archive files."""
    counts: dict[str, int] = defaultdict(int)
    for pattern in _ARCHIVE_GLOB:
        for path in sorted(ARCHIVE_DIR.glob(pattern)):
            try:
                html = path.read_text(encoding="utf-8")
                for url in _URL_RE.findall(html):
                    counts[url] += 1
            except Exception:
                pass
    return dict(counts)
