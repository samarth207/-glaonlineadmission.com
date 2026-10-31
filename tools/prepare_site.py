"""Prepare the public mirror for glaonlineadmission.com, including dynamic listings."""

from __future__ import annotations

import datetime
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

from bs4 import BeautifulSoup, Comment, Tag


ROOT = Path(__file__).resolve().parents[1]
TARGET = "https://glaonlineadmission.com"
SOURCE = "https://glaonline.com"


def hydrate_events(source: str, url: str) -> str:
    soup = BeautifulSoup(source, "lxml")
    listing = soup.select_one(".showEventsAanNewsClass")
    if listing is None:
        return source
    endpoint = next(
        (name for name in [
            "showStudentEngagementDataAjax", "showOrientationDataAjax",
            "showConvocationDataAjax",
        ] if name in source),
        None,
    )
    if endpoint is None:
        return source
    type_ids = soup.select_one("#current_event_type_ids")
    base_path = soup.select_one("#current_base_path")
    params = {
        "batch": "", "year_search": "", "month": "", "limit": "200",
        "event_type_ids": type_ids.get("value", "") if type_ids else "",
        "base_path": base_path.get("value", "") if base_path else urllib.parse.urlsplit(url).path.strip("/"),
    }
    fragments = []
    for page in range(30):
        params["page"] = str(page)
        request = urllib.request.Request(
            SOURCE + "/events/" + endpoint,
            data=urllib.parse.urlencode(params).encode(),
            headers={"User-Agent": "Mozilla/5.0", "Referer": url, "X-Requested-With": "XMLHttpRequest"},
        )
        with urllib.request.urlopen(request, timeout=30) as response:
            result = response.read().decode("utf-8")
        if not result and endpoint == "showConvocationDataAjax":
            print(f"Source convocation endpoint returned no body; checking shared event API: {url}")
            request.full_url = SOURCE + "/events/showStudentEngagementDataAjax"
            with urllib.request.urlopen(request, timeout=30) as response:
                result = response.read().decode("utf-8")
        fragment, separator, total = result.rpartition("###")
        if not separator or not total.strip().isdigit():
            raise RuntimeError(f"Invalid event-listing response for {url}")
        if not fragment.strip() or "Data not available" in fragment:
            break
        fragments.append(fragment)
        if int(total) < 200:
            break
    else:
        raise RuntimeError(f"Event listing exceeded pagination bound for {url}")

    listing.clear()
    parsed = BeautifulSoup("".join(fragments), "html.parser")
    for child in list(parsed.contents):
        listing.append(child)
    print(f"Captured dynamic event listing: {url} ({len(listing.find_all('a'))} links)")
    return str(soup)


def parse_fragment(text: str) -> list:
    return list(BeautifulSoup(text, "html.parser").contents)


def local_reference(value: str, page: Path) -> str:
    parsed = urllib.parse.urlsplit(value)
    if parsed.hostname not in {"glaonline.com", "www.glaonline.com", "glaonlineadmission.com"}:
        return value
    path = urllib.parse.unquote(parsed.path or "/")
    target = ROOT.joinpath(*path.lstrip("/").split("/"))
    if path.endswith("/") or target.is_dir() or not target.suffix:
        target /= "index.html"
    relative = os.path.relpath(target, page.parent).replace(os.sep, "/")
    return urllib.parse.quote(relative, safe="/._-") + ("#" + parsed.fragment if parsed.fragment else "")


def make_form(form_id: str, specialization: str) -> Tag:
    template = "hero-form.html" if form_id == "banner-enquiry" else "enquiry-form.html"
    soup = BeautifulSoup((ROOT / "tools" / template).read_text(encoding="utf-8"), "html.parser")
    form = soup.form
    form["id"] = form_id
    form.select_one('[name="specialization"]')["value"] = specialization
    if form_id == "banner-enquiry":
        states = json.loads((ROOT / "siteassets" / "districts.json").read_text(encoding="utf-8"))
        select = form.select_one('[name="state"]')
        for state in states:
            option = soup.new_tag("option", value=state["name"])
            option.string = state["name"]
            select.append(option)
    if form_id == "dialog-enquiry":
        consent = form.select_one(".local-consent")
        for element in parse_fragment(
            '<label>State (optional)<input type="text" name="state" maxlength="100"></label>'
            '<label>City (optional)<input type="text" name="city" maxlength="100"></label>'
            '<label class="local-field-wide">Message (optional)<textarea name="message" maxlength="3000" rows="3" placeholder="How can we help you?"></textarea></label>'
        ):
            consent.insert_before(element)
    return form


def prepare_page(page: Path) -> dict[str, str]:
    source = page.read_text(encoding="utf-8")
    source = re.sub(r"https?://(?:www\.)?glaonline\.com(?=[/'\"#?\s<]|$)", TARGET, source)
    source = source.replace("//glaonline.com", "//glaonlineadmission.com")
    source = re.sub(
        r"(?<!\d)(?:\+91[- ]?)?(?:9568536853|7617595602|7617595603|8439954905)(?!\d)",
        "+91 93113 81814",
        source,
    )
    soup = BeautifulSoup(source, "lxml")
    for link in soup.select('a[href^="tel:"]'):
        link["href"] = "tel:+919311381814"
        if link.get("aria-label") and re.search(r"\d{5}", link["aria-label"]):
            link["aria-label"] = "Call +91 93113 81814"
    for item in soup.find_all("li"):
        calls = item.select('a[href^="tel:"]')
        if len(calls) > 1:
            for duplicate in calls[1:]:
                duplicate.decompose()
            for text in calls[0].find_all(string=True):
                if "+91 93113 81814" in text:
                    text.replace_with(text.rstrip(", "))
    if page == ROOT / "index.html":
        faculty = soup.select_one("section.faculty_sec")
        wrapper = faculty.select_one(".full_touch") if faculty else None
        if wrapper:
            # Repair source markup as the browser does: only the faculty container is hidden.
            anchor = faculty
            for child in list(wrapper.children):
                if isinstance(child, Tag) and child.name == "div" and "container" in child.get("class", []):
                    continue
                child.extract()
                anchor.insert_after(child)
                anchor = child
    brochure = re.search(r"""var fileURL\s*=\s*["']([^"']+\.pdf)["']""", source)
    previous_brochure = soup.select_one("[data-brochure]")
    brochure_path = (
        urllib.parse.urlsplit(brochure.group(1)).path if brochure
        else previous_brochure.get("data-brochure", "") if previous_brochure else ""
    )
    for comment in soup.find_all(string=lambda node: isinstance(node, Comment)):
        if any(key in comment for key in ["glaonline", "LoadRegistrationForm", "nopaperforms", "api-registration"]):
            comment.extract()

    for credit in list(soup.select(".design_dev")):
        credit.decompose()
    for author in soup.find_all("meta", attrs={"name": "author"}):
        author.decompose()

    for item in list(soup.select(".accordion-item")):
        heading = item.select_one(".accordion-header")
        if heading and heading.get_text(strip=True) == "What is the LMS Portal link?":
            item.decompose()
        elif heading and heading.get_text(strip=True) == "How can I apply for an online course?":
            answer = item.select_one(".accordion-body")
            answer.clear()
            for child in parse_fragment(
                '<p>Visit <a href="/index.html">glaonlineadmission.com</a> and select '
                '<a href="/contact-us/index.html#contact_form" data-open-enquiry="">Apply Now</a>. '
                'Choose your program and submit your contact details. Our admissions team will '
                'contact you with guidance on eligibility, required documents and the next steps. '
                'This website collects admissions enquiries; it does not provide an application '
                'login or collect registration fees.</p>'
            ):
                answer.append(child)

    for text in list(soup.find_all(string=True)):
        if not isinstance(text, Comment) and text.parent.name not in {"script", "style"}:
            updated = re.sub(
                r"(?<![\w.-])(?:www\.)?glaonline\.com(?![\w.-])",
                "glaonlineadmission.com",
                str(text),
                flags=re.IGNORECASE,
            )
            if updated != str(text):
                text.replace_with(updated)

    for anchor in list(soup.find_all("a")):
        if anchor.get_text(" ", strip=True).lower() == "student login" or anchor.get("href") == "#blog-content-excluded":
            container = anchor.parent if anchor.parent.name == "li" else anchor
            container.decompose()
            continue
        is_brochure = anchor.get_text(" ", strip=True).lower() == "download brochure"
        is_enquiry = (
            urllib.parse.urlsplit(anchor.get("href", "")).hostname == "apply.glaonline.com"
            or anchor.get_text(" ", strip=True).lower() == "apply now"
            or "modal-link2" in anchor.get("class", [])
        )
        if is_enquiry or is_brochure:
            anchor["href"] = "/contact-us/index.html#contact_form"
            anchor["data-open-enquiry"] = ""
            anchor["aria-label"] = "Request a program brochure" if is_brochure else "Open admissions enquiry form"
            if is_brochure and brochure_path:
                anchor["data-brochure"] = brochure_path
            anchor.attrs.pop("target", None)
            anchor.attrs.pop("onclick", None)
    for obsolete_modal in list(soup.select("#custom-modal, #custom-modal2")):
        obsolete_modal.decompose()

    for tag in list(soup.find_all(["script", "iframe", "link", "meta"])):
        if tag.parent is None:
            continue
        src = tag.get("src", "")
        text = tag.get_text()
        old_script = any(key in text for key in [
            "LoadRegistrationForm", "nopaperforms", "enquire/enquire_", "enquire/spelisation",
            "cms_page/save_contact", "showStudentEngagementDataAjax",
            "showOrientationDataAjax", "showConvocationDataAjax", "searchBtn",
            "showProgramDataAjax", "googletagmanager.com", "$('.numbers').keyup",
        ])
        if tag.name == "script" and (old_script or any(key in src for key in [
            "api-registration.js", "recaptcha", "sweetalert2", "nopaperforms", "googletagmanager",
        ])):
            tag.decompose()
        elif tag.name == "iframe" and "googletagmanager.com" in src:
            parent = tag.parent if tag.parent.name == "noscript" else tag
            parent.decompose()
        elif tag.name == "meta" and tag.get("name", "").lower() in {
            "google-site-verification", "msvalidate.01",
        }:
            tag.decompose()
        elif tag.name == "link" and {"preconnect", "dns-prefetch"} & set(tag.get("rel", [])):
            tag.decompose()

    for tag in soup.find_all(True):
        if tag.name == "link" and "preload" in tag.get("rel", []) and tag.get("src"):
            tag["href"] = tag.attrs.pop("src")
            tag["as"] = tag.get("as") or "image"
        for attribute in ["src", "href", "poster", "data-src", "data-original", "data-background", "data-bg"]:
            if tag.get(attribute):
                tag[attribute] = local_reference(tag[attribute], page)
        if tag.get("style"):
            tag["style"] = re.sub(
                r"url\(['\"]?([^)'\"\s]+)['\"]?\)",
                lambda match: "url('" + local_reference(match.group(1), page) + "')",
                tag["style"],
            )
        # The initial HTML mirror lowercased SVG names; XML SVG names are case-sensitive.
        if tag.find_parent("svg") is not None or tag.name == "svg":
            for lower, proper in {
                "viewbox": "viewBox", "gradientunits": "gradientUnits",
                "gradienttransform": "gradientTransform", "preserveaspectratio": "preserveAspectRatio",
            }.items():
                if lower in tag.attrs:
                    tag[proper] = tag.attrs.pop(lower)
            tag.name = {"lineargradient": "linearGradient", "radialgradient": "radialGradient",
                        "clippath": "clipPath"}.get(tag.name, tag.name)

    heading = soup.find("h1")
    specialization = heading.get_text(" ", strip=True)[:160] if heading and len(page.relative_to(ROOT).parts) > 3 and "program" in page.parts else ""
    banner = soup.select_one("#reg-form")
    if banner:
        banner.clear()
        banner.append(make_form("banner-enquiry", specialization))

    existing_dialog = soup.select_one("#admission-enquiry")
    if existing_dialog:
        existing_dialog.decompose()
    dialog = soup.new_tag("dialog", id="admission-enquiry", attrs={
        "class": "local-enquiry-dialog", "aria-label": "Admissions enquiry",
    })
    close = soup.new_tag("button", attrs={
        "type": "button", "class": "local-enquiry-close", "data-close-enquiry": "",
    })
    close.string = "Close"
    dialog.append(close)
    dialog.append(make_form("dialog-enquiry", specialization))
    soup.body.append(dialog)

    contact = soup.select_one("#contact_form")
    if contact:
        contact["data-local-form"] = "contact"
        contact["action"] = "/api/form.php"
        for tag in list(contact.select(".g-recaptcha, .captcha_error, [name=prev_url]")):
            tag.decompose()
        for field in contact.select("input:not([type=hidden]), select, textarea"):
            field["aria-label"] = field.get("placeholder") or field.get("name", "").capitalize()
            if "validation_required" in field.get("class", []):
                field["required"] = ""
            if field.get("name") == "phone":
                field["type"] = "tel"
                field["maxlength"] = "20"
                field["pattern"] = r"\+?[0-9 \(\)\-]{7,20}"
            elif field.get("name") == "email":
                field["type"] = "email"
                field["maxlength"] = "254"
            elif field.get("name") in {"name", "state", "country", "city"} and field.name == "input":
                field["maxlength"] = "100"
            elif field.get("name") == "company":
                field["maxlength"] = "150"
            elif field.get("name") == "message":
                field["maxlength"] = "3000"
        original = contact.select_one("#contact_submit")
        if original:
            original.name = "button"
            original.attrs.pop("href", None)
            original["type"] = "submit"
        for element in list(contact.select(".local-consent, .local-honeypot, .local-form-status, noscript")):
            element.decompose()
        additions = make_form("unused", "")
        for selector in [".local-consent", ".local-honeypot", ".local-form-status", "noscript"]:
            contact.append(additions.select_one(selector))

    search = soup.select_one("#desktop_global_search")
    if search:
        search["method"] = "get"
        search["action"] = "#"
        search_input = search.select_one('[name="search"]')
        search_input.attrs.pop("method", None)
        old_results = soup.select_one("#local-search-results")
        if old_results:
            old_results.decompose()
        results = soup.new_tag("div", id="local-search-results", attrs={
            "class": "local-search-results", "aria-live": "polite",
        })
        search.insert_after(results)

    listing = soup.select_one(".showEventsAanNewsClass")
    if listing:
        listing["data-local-events"] = ""
        if not listing.find_all(recursive=False) and page.parent.name == "convocation":
            notice = soup.new_tag("p")
            notice.string = "The live event listing is currently unavailable. Browse the archived ceremony:"
            listing.append(notice)
            archive = soup.new_tag("a", href="/convocation/14th-convocation-ceremony/index.html")
            archive.string = "14th Convocation Ceremony"
            listing.append(archive)
        for child in listing.find_all(recursive=False):
            text = child.get_text(" ", strip=True)
            date = re.search(r"(\d{1,2})[ ./-]([A-Za-z]+|\d{1,2})[ ,./-]+(\d{4})", text)
            if date:
                try:
                    month = int(date.group(2)) if date.group(2).isdigit() else datetime.datetime.strptime(date.group(2)[:3], "%b").month
                    child["data-month"] = str(month)
                    child["data-year"] = date.group(3)
                except ValueError as error:
                    raise RuntimeError(f"Unrecognized event date in {page}: {date.group(0)}") from error
        for button in soup.select("#loadMoreBtn"):
            button.decompose()

    for track in soup.select('track[src$="captions-en.vtt"]'):
        track.decompose()

    if page == ROOT / "privacy-policy" / "index.html" and not soup.select_one("#local-form-privacy"):
        notice = soup.new_tag("div", id="local-form-privacy", attrs={"class": "terms_wraper"})
        for child in parse_fragment(
            "<h4>Admissions enquiries on glaonlineadmission.com</h4>"
            "<p>Contact and admissions enquiry forms on this website store the details you submit, "
            "your consent, the source page and submission time in our MySQL database so our team can "
            "respond to your request. A hashed network address is stored to limit abusive submissions. "
            "An essential, HTTP-only session cookie protects form submissions. "
            "These forms do not submit your details to the original site's registration widgets. "
            "External maps, videos and portal links are provided by their respective services and "
            "remain subject to those services' privacy policies. To request access, correction or "
            "deletion of an enquiry, use the contact details on this page.</p>"
        ):
            notice.append(child)
        soup.select_one(".terms-page .col-lg-10").insert(0, notice)

    relative = page.relative_to(ROOT).as_posix()
    route = "/" if relative == "index.html" else "/" + relative.removesuffix("index.html")
    canonical = soup.find("link", rel="canonical")
    if canonical:
        canonical["href"] = TARGET + route
    else:
        soup.head.append(soup.new_tag("link", rel="canonical", href=TARGET + route))
    og_url = soup.find("meta", property="og:url")
    if og_url:
        og_url["content"] = TARGET + route
    for meta in soup.find_all("meta"):
        if (meta.get("property") or meta.get("name")) in {"og:image", "twitter:image"}:
            image = meta.get("content", "")
            parsed = urllib.parse.urlsplit(image)
            if parsed.netloc:
                path = parsed.path
            else:
                target = (page.parent / urllib.parse.unquote(parsed.path)).resolve()
                path = "/" + target.relative_to(ROOT).as_posix()
            meta["content"] = TARGET + path
    for structured in soup.find_all("script", attrs={"type": "application/ld+json"}):
        structured.string = structured.get_text().replace(
            TARGET + "/assets/images/logo.png",
            TARGET + "/siteassets/images/green-logo.png",
        )
        data = json.loads(str(structured.string))
        if isinstance(data, dict) and isinstance(data.get("contactPoint"), dict):
            data["contactPoint"]["telephone"] = "+919311381814"
            structured.string = json.dumps(data, indent=2, ensure_ascii=False)
    for duplicate in list(soup.select('link[href$="local-site.css"], script[src$="local-site.js"]')):
        duplicate.decompose()
    soup.head.append(soup.new_tag("link", rel="stylesheet", href="/siteassets/css/local-site.css"))
    soup.body.append(soup.new_tag("script", src="/siteassets/js/local-site.js", defer=""))

    page.write_text(str(soup), encoding="utf-8")
    main = soup.find("main") or soup.select_one(".main") or soup.body
    clean = BeautifulSoup(str(main), "html.parser")
    for tag in clean.select("script, style, nav, header, footer, form, dialog, .mobile-menu-wrapper"):
        tag.decompose()
    return {
        "path": route,
        "title": soup.title.get_text(" ", strip=True) if soup.title else route,
        "text": clean.get_text(" ", strip=True)[:20000],
    }


def prepare() -> None:
    pages = sorted(page for page in ROOT.rglob("*.html") if "_external" not in page.parts and "tools" not in page.parts)
    index = [prepare_page(page) for page in pages]
    (ROOT / "siteassets" / "search-index.json").write_text(json.dumps(index, ensure_ascii=False), encoding="utf-8")
    urls = "".join(f"<url><loc>{TARGET}{entry['path']}</loc></url>" for entry in index)
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        + urls + "</urlset>", encoding="utf-8",
    )
    (ROOT / "robots.txt").write_text(
        f"User-agent: *\nDisallow: /api/\nDisallow: /tools/\nSitemap: {TARGET}/sitemap.xml\n", encoding="utf-8",
    )
    script_patches = {
        "custom.js": [
            ('if (mobileView.matches) {',
             'if (mobileView.matches && document.querySelector(".apply_btn_button:not([data-open-enquiry])") && document.querySelector(".banner_form")) {'),
            ('bannerForm.style.visibility = "visible";',
             'if (bannerForm) bannerForm.style.visibility = "visible";'),
            ('observer.observe(counterSection);',
             'if (counterSection) observer.observe(counterSection);'),
            ('// initial state\nvideo.muted = true;\nsoundBtn.innerHTML = "🔇";',
             'if (video instanceof HTMLVideoElement && soundBtn) {\nvideo.muted = true;\nsoundBtn.innerHTML = "🔇";'),
            ('soundBtn.innerHTML = video.muted ? "🔇" : "🔊";\n});',
             'soundBtn.innerHTML = video.muted ? "🔇" : "🔊";\n});\n}'),
            ("$('.modal-link').on('click', function() {",
             "$('.modal-link:not([data-open-enquiry])').on('click', function() {"),
            ("$('.modal-link2').on('click', function() {",
             "$('.modal-link2:not([data-open-enquiry])').on('click', function() {"),
        ],
        "home.js": [
            ("const player = new Vimeo.Player(iframe);\n    const playBtn = document.getElementById('playPauseBtn');",
             "const playBtn = document.getElementById('playPauseBtn');\n    if (!iframe || !playBtn) return;\n    const player = new Vimeo.Player(iframe);"),
        ],
        "inner-page.js": [
            ('var target = $(hash);\n        $("html,body")',
             'var target = $(hash);\n        if (!target.length) return;\n        $("html,body")'),
            ('a[href*="#"]:not([href="#"])',
             'a[href*="#"]:not([href="#"]):not([data-open-enquiry])'),
            ("// Initialize Swiper (or use your existing initialization)\n  var Homeswiper",
             "// Initialize Swiper (or use your existing initialization)\n  if (!document.querySelector('.students-learners')) return;\n  var Homeswiper"),
            ('var swiper = new Swiper(".faculty_slider", {',
             'if (!document.querySelector(".faculty_slider")) return;\n    var swiper = new Swiper(".faculty_slider", {'),
            ('const iframe = document.getElementById("youtubeVideo");\n\n    // Show popup',
             'const iframe = document.getElementById("youtubeVideo");\n    if (!modal || !closeBtn || !iframe) return;\n\n    // Show popup'),
        ],
    }
    for name in ["custom.js", "inner-page.js", "home.js"]:
        path = ROOT / "siteassets" / "js" / name
        text = path.read_text(encoding="utf-8-sig")
        text = re.sub(
            r'window\.location\.origin\s*\+\s*"/"\s*\+\s*window\.location\.pathname\.split\("/"\)\[1\]\s*\+\s*"/"',
            'window.location.origin + "/"', text,
        )
        text = text.replace('vimeoScript.src = "https://player.vimeo.com/api/player.js";',
                            'vimeoScript.src = BASE_URL + "_external/player.vimeo.com/api/player.js";')
        text = text.replace(
            'if (mobileView.matches && document.querySelector(".apply_btn_button") && document.querySelector(".banner_form")) {',
            'if (mobileView.matches) {',
        )
        for before, after in script_patches[name]:
            if after in text:
                continue
            if before not in text:
                raise RuntimeError(f"Shared script patch no longer matches: {name}: {before[:60]}")
            text = text.replace(before, after, 1)
        path.write_text(text, encoding="utf-8")
    stylesheet = ROOT / "siteassets" / "css" / "inner-page.css"
    text = stylesheet.read_text(encoding="utf-8")
    text = re.sub(
        r"background:\s*url\([^)]*(?:feature_blog_icon|arrow-yellow)\.svg\)\s*no-repeat;",
        "", text,
    )
    stylesheet.write_text(text, encoding="utf-8")
    obsolete_registration = ROOT / "siteassets" / "js" / "api-registration.js"
    if obsolete_registration.exists():
        obsolete_registration.unlink()
    print(f"Prepared {len(pages)} pages for {TARGET}; Student Login navigation removed.")


if __name__ == "__main__":
    prepare()
