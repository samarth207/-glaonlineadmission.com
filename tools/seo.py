"""SEO metadata and truthful admissions-partner identity for the public mirror."""

import json
import re
import urllib.parse
from pathlib import Path

from bs4 import BeautifulSoup, Tag


TARGET = "https://glaonlineadmission.com"
BRAND = "GLA Online Admissions"
PARTNER_DESCRIPTION = (
    "GLA Online Admissions is an independent authorized admissions partner for "
    "GLA University online programs, not a university-operated website."
)
COURSES = {
    "online-bba": ("BBA", "Bachelor of Business Administration", "Undergraduate"),
    "online-bca": ("BCA", "Bachelor of Computer Applications", "Undergraduate"),
    "online-bcom-hons": ("B.Com (Hons.)", "Bachelor of Commerce (Honours)", "Undergraduate"),
    "online-mba": ("MBA", "Master of Business Administration", "Postgraduate"),
    "online-mca": ("MCA", "Master of Computer Applications", "Postgraduate"),
}
ALIASES = {
    f"/program/{name.removeprefix('online-')}/": f"/program/{name}/"
    for name in COURSES
}
PAGE_META = {
    "/about-us/overview/": (
        "About GLA University Online Education | Admissions Guide",
        "Learn about GLA University's online education background and learner support. "
        "Explore degree information through an independent authorized admissions partner.",
        "About GLA University Online Education",
    ),
    "/": (
        "GLA Online Degree Admissions | MBA, MCA, BBA, BCA & B.Com",
        "Explore GLA University online degrees, fees and eligibility. Get admissions guidance "
        "for MBA, MCA, BBA, BCA and B.Com from an authorized independent partner.",
        "GLA University Online Degree Admissions",
    ),
    "/program/": (
        "GLA Online Degree Programs | UG & PG Admissions",
        "Compare GLA University online MBA, MCA, BBA, BCA and B.Com programs. Explore course "
        "details and request guidance from an independent admissions partner.",
        "GLA University Online Degree Programs",
    ),
    "/program/undergraduate/": (
        "GLA Online Undergraduate Degrees | BBA, BCA & B.Com",
        "Explore GLA University online BBA, BCA and B.Com undergraduate degrees. Review "
        "eligibility, course information and admissions guidance for students in India.",
        "GLA Online Undergraduate Degree Programs",
    ),
    "/program/postgraduate/": (
        "GLA Online Postgraduate Degrees | MBA & MCA",
        "Explore GLA University online MBA and MCA postgraduate degrees. Review "
        "specializations, course information and admissions guidance for graduates in India.",
        "GLA Online Postgraduate Degree Programs",
    ),
    "/admission/fee-structure/": (
        "GLA Online Course Fees | MBA, MCA, BBA, BCA & B.Com",
        "Review published GLA online degree fees, semester payments and additional charges. "
        "Confirm current fees and applicable benefits before applying.",
        "GLA Online Degree Fee Structure",
    ),
    "/admission/eligibility/": (
        "GLA Online Admission Eligibility | UG & PG Degrees",
        "Review eligibility information for GLA online undergraduate and postgraduate degrees. "
        "Request guidance on qualifications and required admission documents.",
        "GLA Online Degree Admission Eligibility",
    ),
    "/admission/admission-procedure/": (
        "How to Apply for GLA Online Degrees | Admissions Guidance",
        "Learn how to enquire about GLA University online degrees and prepare for admission. "
        "Our partner website provides guidance, not accounts or payment collection.",
        "How to Apply for GLA Online Degree Admission",
    ),
    "/admission/academic-calendar/": (
        "GLA Online Academic Calendar | Degree Study Schedule",
        "Browse published academic calendars for GLA online programs. Check the applicable "
        "batch calendar and confirm current dates with the university.",
        "GLA Online Academic Calendar",
    ),
    "/admission/evaluation-system/": (
        "GLA Online Evaluation System | Assessments & Exams",
        "Explore the published assessment and examination structure for GLA online degree "
        "programs. Confirm current evaluation requirements for your program.",
        "GLA Online Assessment and Evaluation System",
    ),
    "/contact-us/": (
        "Contact GLA Online Admissions | Independent Partner",
        "Contact an independent authorized GLA online admissions partner at +91 93113 81814 "
        "or admissions@glaonlineadmission.com for degree admission guidance.",
        "Contact GLA Online Admissions",
    ),
    "/faq/": (
        "GLA Online Degree FAQs | Admissions & Study Guidance",
        "Find answers about GLA online programs, eligibility, study and admissions. "
        "Request clarification from an independent authorized admissions partner.",
        "GLA Online Degree and Admissions FAQs",
    ),
    "/privacy-policy/": (
        "Admissions Enquiry Privacy Policy | GLA Online Admissions",
        "Read how this independent admissions website handles enquiry details, consent, "
        "essential cookies and requests concerning your personal information.",
        "Admissions Enquiry Privacy Policy",
    ),
    "/disclaimer/": (
        "Independent Admissions Partner Disclaimer | GLA Online",
        "Understand this website's independent admissions partner role, university information "
        "and limitations. Confirm current program details before making decisions.",
        "Independent Admissions Partner Disclaimer",
    ),
    "/terms-conditions/": (
        "Website Terms & Conditions | GLA Online Admissions",
        "Read the terms for using this independent GLA online admissions guidance website "
        "and its enquiry forms, information and external links.",
        "Website Terms and Conditions",
    ),
}


def route_for(page: Path, root: Path) -> str:
    relative = page.relative_to(root).as_posix()
    return "/" if relative == "index.html" else "/" + relative.removesuffix("index.html")


def canonical_route(route: str) -> str:
    return ALIASES.get(route, route)


def route_label(route: str) -> str:
    if route == "/":
        return "Home"
    slug = route.strip("/").split("/")[-1]
    return re.sub(r"[-_]+", " ", slug).strip().title()


def concise(text: str, limit: int = 170) -> str:
    return text if len(text) <= limit else text[:limit - 3].rsplit(" ", 1)[0].rstrip(".,;:") + "..."


def metadata(soup: BeautifulSoup, route: str) -> tuple[str, str, str]:
    route = canonical_route(route)
    if route in PAGE_META:
        return PAGE_META[route]
    parts = route.strip("/").split("/")
    if parts[0] == "program" and len(parts) >= 2 and parts[1] in COURSES:
        code, name, _ = COURSES[parts[1]]
        heading = f"GLA Online {code} - {name}"
        if len(parts) > 2:
            h1 = soup.find("h1")
            original = h1.get_text(" ", strip=True) if h1 else route_label(route)
            specialization = re.split(r"specialization in", original, flags=re.I)[-1].strip()
            specialization = re.sub(r"^GLA Online .*? - ", "", specialization)
            heading = f"GLA Online {code} - {specialization}"
        title = f"GLA Online {code} | Fees, Eligibility & Admissions"
        if len(parts) > 2:
            title = f"{heading} | Admissions"
        description = (
            f"Explore {heading}, course details, fees and eligibility. "
            "Request guidance from an independent authorized admissions partner."
        )
        return title, concise(description), heading
    h1 = soup.find("h1")
    heading = h1.get_text(" ", strip=True) if h1 else route_label(route)
    if parts[:2] == ["about-us", "leadership"]:
        person = soup.select_one("main h4")
        role = {"ceo": "CEO", "cfo": "CFO"}.get(parts[-1], route_label(route))
        heading = f"{person.get_text(' ', strip=True)} - {role}" if person else f"GLA University {role}"
    elif parts[0] == "testimonials" and len(parts) > 1:
        heading = f"GLA Online {route_label(route)} Testimonials"
    elif parts[0] == "student-engagement" and len(parts) == 2:
        heading = f"GLA Online {route_label(route)}"
    elif len(parts) > 1 and parts[0] in {
        "student-engagement", "orientation", "convocation", "engage-learn-celebrate", "mentor-details"
    }:
        detail = soup.select_one("main h2")
        heading = detail.get_text(" ", strip=True) if detail else route_label(route)
        date = re.search(r"\b\d{1,2}[. /-][A-Za-z]{3}[. ,/-]\d{2,4}\b", soup.main.get_text(" ", strip=True))
        if date:
            heading += f" ({date.group(0)})"
    title = f"{heading} | GLA Online"
    description = (
        f"Explore {heading} information for GLA University online learners. "
        "Browse this resource on our independent admissions guidance website."
    )
    return title, concise(description), heading


def set_meta(soup: BeautifulSoup, key: str, value: str) -> None:
    attribute = "property" if key.startswith("og:") else "name"
    for old in list(soup.find_all("meta", attrs={"name": key}) +
                    soup.find_all("meta", attrs={"property": key})):
        old.decompose()
    soup.head.append(soup.new_tag("meta", attrs={attribute: key, "content": value}))


def apply_seo(soup: BeautifulSoup, page: Path, root: Path) -> None:
    hero = soup.main.find("section", class_=["progrm_banner", "common-sec"], recursive=False)
    footer = soup.find("footer")
    if hero and footer and hero in footer.parents:
        # Malformed source pages put the remaining page inside the hero wrapper.
        wrapper = footer.parent
        anchor = hero
        moving = False
        for child in list(wrapper.children):
            if isinstance(child, Tag) and child.name == "section":
                moving = True
            if moving:
                child.extract()
                anchor.insert_after(child)
                anchor = child
    route = route_for(page, root)
    canonical = canonical_route(route)
    url = TARGET + canonical
    title, description, heading = metadata(soup, route)
    soup.html["lang"] = "en-IN"
    soup.title.string = title
    set_meta(soup, "description", description)
    set_meta(soup, "robots", "index, follow, max-image-preview:large")
    for old in list(soup.select('meta[name="keywords"], link[rel="canonical"]')):
        old.decompose()
    soup.head.append(soup.new_tag("link", rel="canonical", href=url))
    for key, value in {
        "og:type": "website", "og:url": url, "og:title": title,
        "og:description": description, "og:site_name": BRAND, "og:locale": "en_IN",
        "og:image": TARGET + "/siteassets/images/green-logo.png",
        "og:image:alt": "GLA University online programs",
        "twitter:card": "summary", "twitter:title": title,
        "twitter:description": description,
        "twitter:image": TARGET + "/siteassets/images/green-logo.png",
        "twitter:image:alt": "GLA University online programs",
    }.items():
        set_meta(soup, key, value)
    soup.h1.clear()
    soup.h1.string = heading
    if "d-none" in soup.h1.get("class", []) and route != "/":
        soup.h1["class"] = [
            value for value in soup.h1.get("class", []) if value != "d-none"
        ] + ["local-content-title"]
    if route == "/":
        # Replace the hidden source H1 with a visible, useful admissions introduction.
        soup.h1.decompose()
        old = soup.select_one("#admissions-introduction")
        if old:
            old.decompose()
        intro = soup.new_tag("section", id="admissions-introduction",
                             attrs={"class": "local-seo-intro"})
        intro.append(soup.new_tag("div", attrs={"class": "container"}))
        container = intro.div
        copy = soup.new_tag("div", attrs={"class": "local-seo-copy"})
        container.append(copy)
        label = soup.new_tag("span", attrs={"class": "local-seo-eyebrow"})
        label.string = "Learn online. Move forward."
        copy.append(label)
        h1 = soup.new_tag("h1")
        h1.string = heading
        copy.append(h1)
        p = soup.new_tag("p")
        p.string = (
            "Explore online MBA, MCA, BBA, BCA and B.Com programs from GLA University. "
            "Students and working professionals in India can compare programs and "
            "request guidance on eligibility, fees and admission documents."
        )
        copy.append(p)
        context = soup.new_tag("p", attrs={"class": "local-seo-context"})
        context.string = PARTNER_DESCRIPTION
        copy.append(context)
        container.append(BeautifulSoup(
            '<div class="local-seo-links" role="group" aria-label="Explore admissions">'
            '<a class="local-seo-primary" href="/program/">Explore degree programs</a>'
            '<a href="/admission/eligibility/">Check eligibility</a>'
            '<a href="/admission/fee-structure/">View published fees</a></div>', "html.parser").div)
        hero = soup.main.find("section", class_="home_banner", recursive=False)
        if hero:
            hero.insert_after(intro)
        else:
            soup.main.insert(0, intro)

    for old in list(soup.select("#admissions-partner-disclosure, #local-breadcrumbs")):
        old.decompose()
    old = soup.select_one("#local-admissions-guidance")
    if old:
        old.decompose()
    if canonical.startswith(("/program/", "/admission/")) or canonical in {
        "/contact-us/", "/privacy-policy/", "/terms-conditions/", "/disclaimer/"
    }:
        notice = soup.new_tag("aside", id="local-admissions-guidance",
                             attrs={"class": "container local-admissions-guidance",
                                    "aria-labelledby": "local-guidance-heading"})
        panel = soup.new_tag("div", attrs={"class": "local-guidance-panel"})
        notice.append(panel)
        copy = soup.new_tag("div", attrs={"class": "local-guidance-copy"})
        panel.append(copy)
        guidance_heading = soup.new_tag("h2", id="local-guidance-heading")
        guidance_heading.string = (
            "About this admissions website" if canonical in {
                "/privacy-policy/", "/terms-conditions/", "/disclaimer/"
            } else "Need admissions guidance?"
        )
        copy.append(guidance_heading)
        p = soup.new_tag("p")
        p.string = PARTNER_DESCRIPTION
        copy.append(p)
        if canonical.startswith(("/program/", "/admission/")):
            detail = soup.new_tag("p", attrs={"class": "local-seo-context"})
            detail.string = "Confirm current fees, eligibility and recognition with the university before applying."
            copy.append(detail)
        if canonical == "/contact-us/":
            detail = soup.new_tag("p", attrs={"class": "local-seo-context"})
            detail.string = "Campus addresses on this page describe GLA University locations, not this partner's office."
            copy.append(detail)
        links = BeautifulSoup(
            '<div class="local-seo-links" role="group" aria-label="Admissions resources">'
            '<a class="local-seo-primary" href="/contact-us/">Contact admissions</a>'
            '<a href="/program/">Explore programs</a>'
            '<a href="/admission/eligibility/">Eligibility</a>'
            '<a href="/admission/fee-structure/">Published fees</a></div>', "html.parser").div
        panel.append(links)
        footer = soup.main.find("footer", recursive=False)
        if footer:
            footer.insert_before(notice)
        else:
            soup.main.append(notice)
    if canonical == "/admission/admission-procedure/":
        replacements = {
            "Applying to GLA Online is quick, easy, and entirely online.":
                "Start with an admissions enquiry. University registration, document verification "
                "and fee payments take place through the university's process, not this partner website.",
            "Fill the Required Details": "Submit an Admissions Enquiry",
            "You will get Login Credential via Mail": "Speak with an Admissions Adviser",
            "Fill Registration Form": "Complete University Registration",
            "Pay Registration Fee": "Confirm University Fees and Payment Instructions",
            "Document Verification": "University Document Verification",
            "Pay Admission Fee": "Complete Admission through the University",
        }
        for text in list(soup.main.find_all(string=True)):
            value = str(text).strip()
            if value in replacements:
                text.replace_with(replacements[value])
    if canonical in {"/privacy-policy/", "/terms-conditions/", "/disclaimer/"}:
        content = soup.select_one(".terms-page")
        if content:
            for text in list(content.find_all(string=True)):
                if text.parent.name in {"script", "style"}:
                    continue
                value = str(text)
                value = value.replace("official website", "independent admissions partner website")
                value = re.sub(r"\bGLA Online(?: University)?\b(?! Admissions)", BRAND, value)
                if 'University (referred to as either "the University"' in value:
                    value = (
                        'Website operator (referred to as "We", "Us" or "Our" in this Disclaimer) '
                        'refers to GLA Online Admissions, an independent authorized admissions partner. '
                        'GLA University campus addresses are not the operator office address.'
                    )
                value = value.replace("the University", "the website operator")
                if value != str(text):
                    text.replace_with(value)
    footer = soup.find("footer")
    if footer:
        note = soup.new_tag("div", id="admissions-partner-disclosure",
                            attrs={"class": "local-partner-disclosure"})
        label = soup.new_tag("span", attrs={"class": "local-partner-label"})
        label.string = "Independent admissions partner"
        note.append(label)
        p = soup.new_tag("p")
        p.string = PARTNER_DESCRIPTION + (
            " Degree awards and admission decisions are made by GLA University. "
            "This website collects enquiries; it does not provide student accounts or collect fees. "
            "Confirm current fees, eligibility, recognition and admission dates with the university."
        )
        note.append(p)
        bottom = footer.select_one(".f_bottom")
        if bottom:
            bottom.insert_before(note)
        else:
            note["class"].append("container")
            footer.append(note)
        copyright_text = footer.select_one(".copy_right p")
        if copyright_text:
            copyright_text.string = "GLA Online Admissions. University names and marks belong to their respective owners."

    breadcrumbs = [{"@type": "ListItem", "position": 1, "name": "Home", "item": TARGET + "/"}]
    if route != "/":
        parts = canonical.strip("/").split("/")
        for i in range(1, len(parts) + 1):
            parent_route = "/" + "/".join(parts[:i]) + "/"
            if (root / parent_route.strip("/") / "index.html").is_file():
                course_slug = parent_route.strip("/").split("/")[-1]
                label = f"Online {COURSES[course_slug][0]}" if course_slug in COURSES else route_label(parent_route)
                if i == len(parts) and len(parts) > 2 and parts[0] == "program":
                    label = heading.split(" - ", 1)[-1]
                breadcrumbs.append({"@type": "ListItem", "position": len(breadcrumbs) + 1,
                                    "name": label, "item": TARGET + parent_route})
        nav = soup.new_tag("nav", id="local-breadcrumbs",
                           attrs={"aria-label": "Breadcrumb", "class": "container local-breadcrumbs"})
        ol = soup.new_tag("ol")
        for entry in breadcrumbs:
            li = soup.new_tag("li")
            a = soup.new_tag("a", href=urllib.parse.urlsplit(entry["item"]).path)
            a.string = entry["name"]
            if entry == breadcrumbs[-1]:
                a["aria-current"] = "page"
            li.append(a)
            ol.append(li)
        nav.append(ol)
        hero = soup.main.find("section", class_=["progrm_banner", "common-sec"], recursive=False)
        if hero:
            hero.insert_after(nav)
        else:
            soup.main.insert(0, nav)

    for a in soup.find_all("a", href=True):
        parsed = urllib.parse.urlsplit(a["href"])
        if parsed.scheme or parsed.netloc or not parsed.path:
            continue
        target = root / parsed.path.lstrip("/") if parsed.path.startswith("/") else page.parent / urllib.parse.unquote(parsed.path)
        if target.is_dir() or not target.suffix:
            target /= "index.html"
        target = target.resolve()
        if target.is_relative_to(root) and target.is_file() and target.suffix == ".html":
            a["href"] = canonical_route(route_for(target, root))
            if parsed.query:
                a["href"] += "?" + parsed.query
            if parsed.fragment:
                a["href"] += "#" + parsed.fragment
    for image in soup.find_all("img"):
        if not image.has_attr("alt"):
            image["alt"] = ""  # Missing source alternatives are decorative PDF icons.
        image["decoding"] = "async"
        if image.find_parent("footer"):
            image["loading"] = "lazy"
    image_sources = {image.get("src") for image in soup.find_all("img")}
    for preload in list(soup.select('link[rel="preload"][as="image"]')):
        href = preload.get("href", "")
        if "uploads/home/banner_images/" in href and href not in image_sources:
            preload.decompose()
    hero = soup.main.find("section", class_=["home_banner", "progrm_banner"], recursive=False)
    first_image = hero.find("img") if hero else None
    if first_image and "uploads/" in first_image.get("src", ""):
        first_image["loading"] = "eager"
        first_image["fetchpriority"] = "high"
        if not any(link.get("href") == first_image["src"]
                   for link in soup.select('link[rel="preload"][as="image"]')):
            soup.head.append(soup.new_tag("link", rel="preload", href=first_image["src"],
                                          attrs={"as": "image", "fetchpriority": "high"}))

    for old in list(soup.select('script[type="application/ld+json"]')):
        old.decompose()
    organization = {
        "@type": "Organization", "@id": TARGET + "/#organization", "name": BRAND,
        "url": TARGET + "/", "description": PARTNER_DESCRIPTION,
        "areaServed": "IN",
        "contactPoint": {"@type": "ContactPoint", "contactType": "admissions enquiries",
                         "telephone": "+919311381814", "email": "admissions@glaonlineadmission.com"},
    }
    website = {"@type": "WebSite", "@id": TARGET + "/#website", "url": TARGET + "/",
               "name": BRAND, "publisher": {"@id": organization["@id"]}, "inLanguage": "en-IN"}
    webpage = {"@type": "WebPage", "@id": url + "#webpage", "url": url, "name": title,
               "description": description, "inLanguage": "en-IN",
               "isPartOf": {"@id": website["@id"]}, "publisher": {"@id": organization["@id"]}}
    graph = [organization, website, webpage]
    if len(breadcrumbs) > 1:
        graph.append({"@type": "BreadcrumbList", "@id": url + "#breadcrumbs",
                      "itemListElement": breadcrumbs})
        webpage["breadcrumb"] = {"@id": url + "#breadcrumbs"}
    parts = canonical.strip("/").split("/")
    if parts[0] == "program" and len(parts) >= 2 and parts[1] in COURSES:
        _, _, level = COURSES[parts[1]]
        course = {"@type": "Course", "@id": url + "#course", "url": url, "name": heading,
                  "description": description, "inLanguage": "en", "educationalLevel": level,
                  "provider": {"@type": "CollegeOrUniversity", "name": "GLA University",
                               "url": "https://www.gla.ac.in/"}}
        graph.append(course)
        webpage["mainEntity"] = {"@id": course["@id"]}
    if canonical in {"/program/", "/program/undergraduate/", "/program/postgraduate/"}:
        courses = []
        for slug, (code, _, level) in COURSES.items():
            if canonical == "/program/undergraduate/" and level != "Undergraduate":
                continue
            if canonical == "/program/postgraduate/" and level != "Postgraduate":
                continue
            courses.append({"@type": "ListItem", "position": len(courses) + 1,
                            "name": f"GLA Online {code}", "url": TARGET + f"/program/{slug}/"})
        graph.append({"@type": "ItemList", "@id": url + "#programs", "itemListElement": courses})
        webpage["mainEntity"] = {"@id": url + "#programs"}
    structured = soup.new_tag("script", attrs={"type": "application/ld+json"})
    structured.string = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)
    soup.head.append(structured)
