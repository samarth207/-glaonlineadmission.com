#!/usr/bin/env python3
"""Create a static, blog-free copy of glaonline.com."""

from __future__ import annotations

import concurrent.futures
import argparse
import hashlib
import html
import json
import os
import posixpath
import re
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from collections import deque
from html.parser import HTMLParser
from pathlib import Path


ORIGIN = "https://glaonline.com"
HOST = urllib.parse.urlparse(ORIGIN).netloc
DESTINATION = Path(__file__).resolve().parent
WORKERS = 6
ASSET_EXTENSIONS = {
    ".avif", ".css", ".csv", ".doc", ".docx", ".eot", ".gif", ".ico",
    ".jpeg", ".jpg", ".js", ".json", ".m4a", ".m4v", ".map", ".mov",
    ".mp3", ".mp4", ".mpeg", ".ogg", ".otf", ".pdf", ".png", ".ppt",
    ".pptx", ".svg", ".ttf", ".txt", ".webm", ".webp", ".woff", ".woff2",
    ".xls", ".xlsx", ".xml", ".zip",
    ".vtt",
}
URL_ATTRIBUTES = {
    "src", "poster", "data-src", "data-original", "data-lazy-src",
    "data-background", "data-bg", "data-image",
}
SKIP_SCHEMES = {"data", "javascript", "mailto", "tel", "blob"}

seen: set[str] = set()
seen_lock = threading.Lock()
page_queue: deque[str] = deque()
asset_queue: deque[str] = deque()
missing_urls: set[str] = set()


def is_blog_url(url: str) -> bool:
    parts = urllib.parse.urlparse(url).path.lower().split("/")
    return any(part == "blog" or part == "blogs" for part in parts)


def normalized_url(value: str, base: str) -> str | None:
    absolute = urllib.parse.urljoin(base, value.strip())
    parsed = urllib.parse.urlsplit(absolute)
    if parsed.scheme.lower() not in {"http", "https"} or not parsed.netloc:
        return None
    if parsed.netloc.lower() == "wserver:8022" and parsed.path.startswith("/glaonline/"):
        return urllib.parse.urlunsplit(("https", HOST, parsed.path[len("/glaonline"):], parsed.query, ""))
    return urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, parsed.path or "/", parsed.query, ""))


def relative_path(url: str, current_file: Path) -> str:
    target = resource_path(url)
    relative = os.path.relpath(target, current_file.parent).replace(os.sep, "/")
    return urllib.parse.quote(relative, safe="/._-")


def resource_path(url: str) -> Path:
    parsed = urllib.parse.urlsplit(url)
    path = urllib.parse.unquote(parsed.path or "/")
    path = posixpath.normpath("/" + path.lstrip("/"))
    suffix = Path(path).suffix.lower()
    if parsed.netloc != HOST:
        if not suffix:
            suffix = ".css" if parsed.netloc in {"fonts.googleapis.com", "fonts.cdnfonts.com"} else ".js"
            path += suffix
        if parsed.query:
            path = path[:-len(suffix)] + "__" + hashlib.sha256(parsed.query.encode()).hexdigest()[:12] + suffix
        path = "/_external/" + parsed.netloc.replace(":", "_") + path
    elif path.endswith("/") or not suffix:
        path = path.rstrip("/") + "/index.html"
    return DESTINATION.joinpath(*path.lstrip("/").split("/"))


def is_asset_url(url: str) -> bool:
    return Path(urllib.parse.urlsplit(url).path).suffix.lower() in ASSET_EXTENSIONS


def enqueue(url: str, kind: str) -> None:
    parsed = urllib.parse.urlsplit(url)
    if is_blog_url(url):
        return
    if parsed.netloc == HOST and parsed.path.startswith("/backoffice/"):
        return
    with seen_lock:
        if url in seen:
            return
        seen.add(url)
    if kind == "page":
        page_queue.append(url)
    else:
        asset_queue.append(url)


def save_response(url: str, body: bytes) -> Path:
    destination = resource_path(url)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(body)
    return destination


def fetch(url: str) -> tuple[str, bytes, str] | None:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (compatible; GLAOfflineMirror/1.0)"},
    )
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                return url, response.read(), response.headers.get_content_type()
        except urllib.error.HTTPError as exc:
            if exc.code == 404:
                missing_urls.add(url)
                print(f"MISSING upstream (404) {url}")
                return None
            if exc.code not in {429, 500, 502, 503, 504} or attempt == 2:
                print(f"FAILED {url}: HTTP {exc.code}")
                return None
            time.sleep(2**attempt)
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            if attempt == 2:
                print(f"FAILED {url}: {exc}")
                return None
            time.sleep(2**attempt)
    return None


def css_rewrite(body: bytes, url: str, destination: Path) -> bytes:
    text = body.decode("utf-8", "replace")
    text = re.sub(
        r"@import\s+url\(['\"]?https://fonts\.googleapis\.com/?['\"]?\)\s*;",
        "",
        text,
        flags=re.IGNORECASE,
    )
    comments: list[str] = []

    def hide_comment(match: re.Match[str]) -> str:
        comments.append(match.group(0))
        return f"__CSS_COMMENT_{len(comments) - 1}__"

    text = re.sub(r"/\*.*?\*/", hide_comment, text, flags=re.DOTALL)

    def replace(match: re.Match[str]) -> str:
        raw = match.group(2).strip().strip("\"'")
        if not raw or raw.startswith("#"):
            return match.group(0)
        target_url = normalized_url(raw, url)
        if not target_url or is_blog_url(target_url):
            return match.group(0)
        parsed = urllib.parse.urlsplit(target_url)
        if parsed.netloc == HOST or is_asset_url(target_url) or parsed.netloc in {
            "fonts.googleapis.com", "fonts.cdnfonts.com", "fonts.gstatic.com",
        }:
            enqueue(target_url, "asset")
            local = relative_path(target_url, destination)
            return match.group(1) + local + match.group(3)
        return match.group(0)

    text = re.sub(r"(url\(\s*)([^)]*?)(\s*\))", replace, text, flags=re.IGNORECASE)
    def replace_import(match: re.Match[str]) -> str:
        target_url = normalized_url(match.group(3), url)
        if not target_url or is_blog_url(target_url):
            return match.group(0)
        parsed = urllib.parse.urlsplit(target_url)
        enqueue(target_url, "asset")
        local = relative_path(target_url, destination)
        return match.group(1) + match.group(2) + local + match.group(4)

    text = re.sub(r"(@import\s+)([\"'])([^\"']+)([\"'])", replace_import, text, flags=re.IGNORECASE)
    for index, comment in enumerate(comments):
        text = text.replace(f"__CSS_COMMENT_{index}__", comment)
    return text.encode("utf-8")


class HTMLRewriter(HTMLParser):
    def __init__(self, page_url: str, output_file: Path) -> None:
        super().__init__(convert_charrefs=False)
        self.page_url = page_url
        self.output_file = output_file
        self.output: list[str] = []
        self.in_style = False
        self.in_script = False

    def _rewrite_url(self, value: str, kind: str) -> str:
        if value.strip().lower().startswith(tuple(f"{scheme}:" for scheme in SKIP_SCHEMES)):
            return value
        target_url = normalized_url(value, self.page_url)
        if not target_url:
            return value
        if is_blog_url(target_url):
            return "#blog-content-excluded"

        parsed = urllib.parse.urlsplit(target_url)
        if kind == "page":
            if parsed.netloc != HOST:
                if is_asset_url(target_url):
                    enqueue(target_url, "asset")
                    return relative_path(target_url, self.output_file)
                return value
            if is_asset_url(target_url):
                enqueue(target_url, "asset")
            else:
                enqueue(target_url, "page")
        else:
            if parsed.netloc != HOST and not is_asset_url(target_url) and parsed.netloc not in {
                "cdn.jsdelivr.net", "fonts.googleapis.com", "fonts.cdnfonts.com",
            }:
                return value
            enqueue(target_url, "asset")

        local = relative_path(target_url, self.output_file)
        fragment = urllib.parse.urlsplit(value).fragment
        if fragment:
            local += "#" + urllib.parse.quote(fragment, safe="!$&'()*+,;=:@/?-._~")
        return local

    def _attributes(self, tag: str, attrs: list[tuple[str, str | None]]) -> str:
        attr_map = dict(attrs)
        rel = (attr_map.get("rel") or "").lower().split()
        result = ["<", tag]
        for name, value in attrs:
            if value is None:
                result.extend((" ", name))
                continue
            rewritten = value
            if name in URL_ATTRIBUTES:
                rewritten = self._rewrite_url(value, "asset")
            elif name == "style":
                rewritten = css_rewrite(
                    value.encode("utf-8"), self.page_url, self.output_file,
                ).decode("utf-8")
            elif name == "srcset":
                candidates = []
                for candidate in value.split(","):
                    bits = candidate.strip().split()
                    if bits:
                        bits[0] = self._rewrite_url(bits[0], "asset")
                        candidates.append(" ".join(bits))
                rewritten = ", ".join(candidates)
            elif name in {"href", "xlink:href"}:
                if not (tag == "link" and {"dns-prefetch", "preconnect"} & set(rel)):
                    is_resource = tag == "link" and bool(
                        {"stylesheet", "icon", "preload", "manifest", "mask-icon"} & set(rel)
                    )
                    rewritten = self._rewrite_url(value, "asset" if is_resource else "page")
            elif name == "action" or name == "formaction":
                rewritten = "#"
            elif tag == "meta" and name == "content" and (
                attr_map.get("property", "").lower() in {"og:image", "og:video"}
                or attr_map.get("name", "").lower() in {"twitter:image"}
            ):
                rewritten = self._rewrite_url(value, "asset")
            result.extend((" ", name, '="', html.escape(rewritten, quote=True), '"'))
        result.append(">")
        return "".join(result)

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.output.append(self._attributes(tag, attrs))
        if tag == "style":
            self.in_style = True
        elif tag == "script":
            self.in_script = True

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.output.append(self._attributes(tag, attrs)[:-1] + " />")

    def handle_endtag(self, tag: str) -> None:
        self.output.append(f"</{tag}>")
        if tag == "style":
            self.in_style = False
        elif tag == "script":
            self.in_script = False

    def handle_data(self, data: str) -> None:
        if self.in_style:
            data = css_rewrite(data.encode("utf-8"), self.page_url, self.output_file).decode("utf-8")
        elif self.in_script:
            for value in re.findall(r"""["']((?:https?:)?//[^"'<> \r\n]+)""", data):
                url = normalized_url(value, self.page_url)
                if url and urllib.parse.urlsplit(url).netloc == HOST and is_asset_url(url):
                    enqueue(url, "asset")
        self.output.append(data)

    def handle_entityref(self, name: str) -> None:
        self.output.append(f"&{name};")

    def handle_charref(self, name: str) -> None:
        self.output.append(f"&#{name};")

    def handle_comment(self, data: str) -> None:
        self.output.append(f"<!--{data}-->")

    def handle_decl(self, decl: str) -> None:
        self.output.append(f"<!{decl}>")

    def unknown_decl(self, data: str) -> None:
        self.output.append(f"<![{data}]>")

    def rewritten(self, source: str) -> bytes:
        self.feed(source)
        self.close()
        return "".join(self.output).encode("utf-8")


def get_sitemap_pages() -> list[str]:
    result = fetch(ORIGIN + "/sitemap.xml")
    if not result:
        raise RuntimeError("Could not retrieve the site's sitemap.")
    _, body, _ = result
    root = ET.fromstring(body)
    urls = [
        element.text.strip()
        for element in root.iter()
        if element.tag.endswith("loc") and element.text and element.text.strip()
    ]
    return sorted({url for url in urls if urllib.parse.urlparse(url).netloc == HOST and not is_blog_url(url)})


def main(reuse_assets: bool = False) -> None:
    pages = get_sitemap_pages()
    for url in pages:
        enqueue(url, "page")
    print(f"Starting with {len(pages)} sitemap pages (blog URLs excluded).")

    completed = 0
    failures = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=WORKERS) as executor:
        while page_queue or asset_queue:
            batch: list[tuple[str, str]] = []
            while page_queue and len(batch) < WORKERS:
                batch.append((page_queue.popleft(), "page"))
            while asset_queue and len(batch) < WORKERS:
                asset_url = asset_queue.popleft()
                if reuse_assets and is_asset_url(asset_url):
                    cached_file = resource_path(asset_url)
                    if cached_file.exists() and Path(urllib.parse.urlsplit(asset_url).path).suffix.lower() != ".css":
                        continue
                batch.append((asset_url, "asset"))
            if not batch:
                continue
            responses = executor.map(fetch, [url for url, _ in batch])
            for (requested_url, kind), result in zip(batch, responses):
                completed += 1
                if result is None:
                    if requested_url not in missing_urls:
                        failures += 1
                    continue
                url, body, content_type = result
                destination = save_response(url, body)

                if content_type == "text/html" and kind == "page" and urllib.parse.urlsplit(url).netloc == HOST:
                    source = body.decode("utf-8", "replace")
                    from tools.prepare_site import hydrate_events
                    source = hydrate_events(source, url)
                    rewritten = HTMLRewriter(url, destination).rewritten(source)
                    destination.write_bytes(rewritten)
                elif content_type == "text/css":
                    destination.write_bytes(css_rewrite(body, url, destination))

                if completed % 25 == 0:
                    print(f"Fetched {completed} resources; queued pages={len(page_queue)}, assets={len(asset_queue)}")

    print(
        f"Finished: {completed - failures - len(missing_urls)} resources fetched, "
        f"{len(missing_urls)} upstream 404s, {failures} other failures."
    )
    print(f"Open {DESTINATION / 'index.html'} or run: python -m http.server 8000")
    manifest = {
        "source": ORIGIN,
        "urls": {url: str(resource_path(url).relative_to(DESTINATION)).replace(os.sep, "/") for url in sorted(seen)},
        "upstream_missing": sorted(missing_urls),
        "transfer_failures": failures,
    }
    (DESTINATION / "tools" / "mirror-manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8",
    )
    if failures:
        raise SystemExit(1)
    from tools.prepare_site import prepare
    prepare()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--reuse-assets",
        action="store_true",
        help="reuse already downloaded non-CSS assets while refreshing pages and stylesheets",
    )
    main(reuse_assets=parser.parse_args().reuse_assets)
