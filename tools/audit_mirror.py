"""Check required local resources, hosting migration, and excluded content."""

import json
import re
import urllib.parse
from pathlib import Path

from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[1]


def audit():
    failures = []
    checked = 0
    remote_embeds = set()
    pages = [p for p in ROOT.rglob("*.html") if not {"tools", "_external"} & set(p.parts)]

    def check(value, source):
        nonlocal checked
        value = value.strip()
        if not value or value.startswith(("#", "data:", "mailto:", "tel:", "javascript:", "blob:")):
            return
        parsed = urllib.parse.urlsplit(value)
        if parsed.netloc and parsed.hostname != "glaonlineadmission.com":
            return
        path = urllib.parse.unquote(parsed.path)
        if not path:
            return
        target = ROOT / path.lstrip("/") if path.startswith("/") else source.parent / path
        if path.endswith("/") or target.is_dir() or not target.suffix:
            target /= "index.html"
        checked += 1
        if not target.is_file():
            failures.append(f"Missing resource: {source.relative_to(ROOT)} -> {value}")

    for page in pages:
        text = page.read_text(encoding="utf-8")
        soup = BeautifulSoup(text, "lxml")
        if not soup.title or not soup.title.get_text(strip=True):
            failures.append(f"Missing title: {page.relative_to(ROOT)}")
        if not soup.find("script", src=re.compile(r"jquery\.min\.js$")):
            failures.append(f"Missing jQuery: {page.relative_to(ROOT)}")
        if not soup.find("link", href=re.compile(r"style\.css$")):
            failures.append(f"Missing core stylesheet: {page.relative_to(ROOT)}")
        if re.search(r"https?://(?:www\.)?glaonline\.com(?:[/\"'#?]|$)|apply\.glaonline\.com|nopaperforms|Student Login", text):
            failures.append(f"Legacy hosting/login/form reference: {page.relative_to(ROOT)}")
        if soup.find("a", href=re.compile("blog-content-excluded")):
            failures.append(f"Excluded blog link remains: {page.relative_to(ROOT)}")
        if len(soup.select("#admission-enquiry")) != 1:
            failures.append(f"Incorrect enquiry dialog count: {page.relative_to(ROOT)}")
        for form in soup.select("[data-local-form]"):
            if form.get("action") != "/api/form.php" or not form.select_one('[name="consent"]'):
                failures.append(f"Unwired local form: {page.relative_to(ROOT)}")
        for form in soup.find_all("form"):
            if form.get("id") != "desktop_global_search" and not form.get("data-local-form"):
                failures.append(f"Legacy form is not wired: {page.relative_to(ROOT)}")
        for tag in soup.find_all(True):
            if tag.name == "iframe" and tag.get("src", "").startswith("https://"):
                remote_embeds.add(tag["src"])
            for name in ["href", "src", "poster", "data-src", "data-original", "data-bg", "data-background", "data-brochure"]:
                if tag.get(name):
                    check(tag[name], page)
            if tag.get("srcset") and not tag["srcset"].startswith("data:"):
                for candidate in tag["srcset"].split(","):
                    if candidate.strip():
                        check(candidate.strip().split()[0], page)
            if tag.get("style"):
                for value in re.findall(r"url\(\s*[\"']?([^\"')]+)", tag["style"]):
                    check(value, page)
            if tag.name == "meta" and (tag.get("property") or tag.get("name")) in {"og:image", "twitter:image"}:
                check(tag.get("content", ""), page)
            if tag.name == "script" and tag.get("type") == "application/ld+json":
                for value in re.findall(r'"(https://glaonlineadmission\.com/[^"]+)"', tag.get_text()):
                    if Path(urllib.parse.urlsplit(value).path).suffix:
                        check(value, page)
    for stylesheet in ROOT.rglob("*.css"):
        text = re.sub(r"/\*.*?\*/", "", stylesheet.read_text(encoding="utf-8"), flags=re.DOTALL)
        for value in re.findall(r"url\(\s*[\"']?([^\"')]+)", text):
            if value.startswith(("http:", "https:", "//")):
                failures.append(f"Unmirrored CSS resource: {stylesheet.relative_to(ROOT)} -> {value}")
            check(value, stylesheet)
    for file in ROOT.rglob("*"):
        if file.is_file() and "blog" in [part.lower() for part in file.relative_to(ROOT).parts]:
            failures.append(f"Downloaded blog route: {file.relative_to(ROOT)}")
        if file.is_file() and file.suffix in {".png", ".webp", ".jpg", ".pdf", ".js", ".css", ".woff", ".woff2"}:
            with file.open("rb") as stream:
                start = stream.read(100).lstrip().lower()
            if start.startswith((b"<!doctype html", b"<html")):
                failures.append(f"HTML received instead of asset: {file.relative_to(ROOT)}")
    files = [p for p in ROOT.rglob("*") if p.is_file() and "tools" not in p.parts and "__pycache__" not in p.parts]
    return {
        "pages": len(pages), "files": len(files),
        "bytes": sum(p.stat().st_size for p in files),
        "local_references_checked": checked,
        "failures": sorted(set(failures)),
        "online_only_embeds": sorted(remote_embeds),
    }


if __name__ == "__main__":
    result = audit()
    print(json.dumps(result, indent=2))
    if result["failures"]:
        raise SystemExit(1)
