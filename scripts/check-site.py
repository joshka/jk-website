#!/usr/bin/env python3
"""Check built internal links, fragment targets, media bytes, and manual completeness."""

import argparse
from html.parser import HTMLParser
import json
import os
from pathlib import Path
from urllib.parse import unquote, urljoin, urlparse


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.ids = set()
        self.duplicate_ids = set()
        self.links = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            if attrs["id"] in self.ids:
                self.duplicate_ids.add(attrs["id"])
            self.ids.add(attrs["id"])
        for key in ("href", "src", "poster"):
            if attrs.get(key):
                self.links.append(attrs[key])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", default=os.environ.get("ASTRO_BASE_PATH", "/jk"))
    args = parser.parse_args()
    root = Path(__file__).resolve().parent.parent
    dist = root / "dist"
    pages = {path.relative_to(dist).as_posix(): Page(path.read_text()) for path in dist.rglob("*.html")}
    base = args.base.rstrip("/") + "/"
    problems = []
    for name, page in pages.items():
        for identifier in page.duplicate_ids:
            problems.append(f"{name}: duplicate fragment target {identifier}")
        url = "https://site.invalid" + base + (name[:-10] if name.endswith("index.html") else name)
        for link in page.links:
            destination = urlparse(urljoin(url, link))
            if destination.netloc != "site.invalid" or destination.scheme not in ("http", "https"):
                continue
            path = unquote(destination.path)
            if not path.startswith(base):
                problems.append(f"{name}: link escapes configured base: {link}")
                continue
            path = path[len(base):]
            if not path or path.endswith("/"):
                path += "index.html"
            if not (dist / path).is_file():
                problems.append(f"{name}: missing target {link}")
            elif destination.fragment and path in pages and unquote(destination.fragment) not in pages[path].ids:
                problems.append(f"{name}: missing fragment {link}")
    for path in (dist / "assets").rglob("*"):
        if path.is_file() and path.suffix in (".png", ".gif", ".mp4", ".webp"):
            header = path.read_bytes()[:100]
            valid = {".png": header.startswith(b"\x89PNG\r\n\x1a\n"),
                     ".gif": header.startswith((b"GIF87a", b"GIF89a")),
                     ".mp4": header[4:8] == b"ftyp",
                     ".webp": header.startswith(b"RIFF") and header[8:12] == b"WEBP"}
            if not valid[path.suffix]:
                problems.append(f"{path.relative_to(dist)}: invalid media bytes or LFS pointer")
    coverage = json.loads((root / "src/data/manual-coverage.json").read_text())
    media = json.loads((root / "src/data/manual-media.json").read_text())
    expected = {scenario["id"] for scenario in coverage["scenarios"]}
    recorded = {scenario["id"] for scenario in media["scenarios"]}
    if expected != recorded:
        problems.append(f"Recording coverage differs: missing={sorted(expected - recorded)}, extra={sorted(recorded - expected)}")
    for chapter in coverage["chapters"]:
        if f"manual/{chapter['slug']}/index.html" not in pages:
            problems.append(f"Missing manual chapter: {chapter['slug']}")
    if problems:
        raise SystemExit("\n".join(problems))
    print(f"Checked {len(pages)} pages, {len(recorded)} recordings, all internal links and media bytes.")


if __name__ == "__main__":
    main()
