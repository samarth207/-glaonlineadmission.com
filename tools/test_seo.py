"""Run with python -m unittest tools.test_seo after preparing the website."""

import json
import unittest
import urllib.parse
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

from bs4 import BeautifulSoup

from tools.seo import ALIASES, BRAND, TARGET, apply_seo, canonical_route, route_for


ROOT = Path(__file__).resolve().parents[1]


class SeoTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pages = {}
        for path in ROOT.rglob("*.html"):
            if {"tools", "_external", ".git"} & set(path.parts):
                continue
            cls.pages[route_for(path, ROOT)] = (
                path, BeautifulSoup(path.read_text(encoding="utf-8"), "lxml")
            )
        cls.canonical_pages = {route: pair for route, pair in cls.pages.items() if route not in ALIASES}

    def test_unique_metadata(self):
        for selector in ["title", 'meta[name="description"]']:
            values = []
            for route, (_, soup) in self.canonical_pages.items():
                with self.subTest(route=route, selector=selector):
                    tags = soup.select(selector)
                    self.assertEqual(len(tags), 1)
                    value = tags[0].get("content") or tags[0].get_text(" ", strip=True)
                    self.assertTrue(value)
                    values.append(value)
                    if selector != "title":
                        self.assertLessEqual(len(value), 180)
            self.assertFalse({text: count for text, count in Counter(values).items() if count > 1})

    def test_canonical_and_social_consistency(self):
        for route, (_, soup) in self.pages.items():
            with self.subTest(route=route):
                url = TARGET + canonical_route(route)
                self.assertEqual(len(soup.select('link[rel="canonical"]')), 1)
                self.assertEqual(soup.select_one('link[rel="canonical"]')["href"], url)
                self.assertEqual(soup.select_one('meta[property="og:url"]')["content"], url)
                for key in ["og:title", "twitter:title"]:
                    self.assertEqual(soup.find("meta", attrs={"property" if key.startswith("og:") else "name": key})["content"],
                                     soup.title.get_text(" ", strip=True))
                self.assertEqual(soup.html["lang"], "en-IN")
                self.assertIn("max-image-preview:large", soup.select_one('meta[name="robots"]')["content"])

    def test_headings_and_partner_identity(self):
        for route, (_, soup) in self.pages.items():
            with self.subTest(route=route):
                self.assertEqual(len(soup.find_all("h1")), 1)
                self.assertNotIn("d-none", soup.h1.get("class", []))
                note = soup.select_one("#admissions-partner-disclosure")
                self.assertIn("independent authorized admissions partner", note.get_text())
                self.assertIn("not a university-operated website", note.get_text())
                hero = soup.main.find("section", class_=["home_banner", "progrm_banner", "common-sec"], recursive=False)
                if hero:
                    elements = list(soup.main.find_all(recursive=False))
                    breadcrumb = soup.select_one("#local-breadcrumbs")
                    guidance = soup.select_one("#local-admissions-guidance")
                    for addition in [breadcrumb, guidance]:
                        if addition:
                            self.assertGreater(elements.index(addition), elements.index(hero))
                guidance = soup.select_one("#local-admissions-guidance")
                if guidance:
                    self.assertIsNotNone(guidance.select_one(".local-guidance-panel h2"))
                    self.assertEqual(len(guidance.select(".local-seo-links a")), 4)
                    sibling = guidance.find_next_sibling()
                    if soup.main.find("footer", recursive=False):
                        self.assertEqual(sibling.name, "footer")
                    else:
                        self.assertIsNone(sibling)
                        self.assertIsNotNone(guidance.find_next("footer"))
                    self.assertIsNone(soup.select_one("#local-breadcrumbs + #local-admissions-guidance"))
                self.assertIsNotNone(note.select_one(".local-partner-label"))
                self.assertNotIn("student login", str(soup).lower())
                self.assertFalse(soup.select('header a[href^="mailto:"], .mobile-menu a[href^="mailto:"]'))
        self.assertEqual(self.pages["/"][1].h1.find_parent("section")["id"], "admissions-introduction")

    def test_structured_identity_and_courses(self):
        for route, (_, soup) in self.pages.items():
            with self.subTest(route=route):
                scripts = soup.select('script[type="application/ld+json"]')
                self.assertEqual(len(scripts), 1)
                data = json.loads(str(scripts[0].string))
                self.assertEqual(data["@context"], "https://schema.org")
                graph = data["@graph"]
                ids = [node["@id"] for node in graph]
                self.assertEqual(len(ids), len(set(ids)))
                organization = next(node for node in graph if node["@type"] == "Organization")
                self.assertEqual(organization["name"], BRAND)
                self.assertNotIn("parentOrganization", organization)
                self.assertNotIn("address", organization)
                self.assertNotIn("sameAs", organization)
                self.assertEqual(organization["contactPoint"]["email"], "admissions@glaonlineadmission.com")
                for node in graph:
                    if node["@type"] == "Course":
                        self.assertEqual(node["provider"]["name"], "GLA University")
                        self.assertEqual(node["provider"]["url"], "https://www.gla.ac.in/")
                        self.assertNotIn("offers", node)
                        self.assertTrue(node["name"])

    def test_breadcrumbs_and_program_list(self):
        for route, (_, soup) in self.pages.items():
            graph = json.loads(str(soup.select_one('script[type="application/ld+json"]').string))["@graph"]
            with self.subTest(route=route):
                crumbs = [node for node in graph if node["@type"] == "BreadcrumbList"]
                if route != "/":
                    self.assertEqual(len(crumbs), 1)
                    entries = crumbs[0]["itemListElement"]
                    links = soup.select("#local-breadcrumbs a")
                    self.assertEqual([link.get_text() for link in links], [entry["name"] for entry in entries])
                    self.assertEqual(entries[-1]["item"], TARGET + canonical_route(route))
                    self.assertEqual([entry["position"] for entry in entries], list(range(1, len(entries) + 1)))
                if route in {"/program/", "/program/undergraduate/", "/program/postgraduate/"}:
                    listing = next(node for node in graph if node["@type"] == "ItemList")
                    self.assertEqual(len(listing["itemListElement"]), 5 if route == "/program/" else 3 if "undergraduate" in route else 2)

    def test_sitemap_and_search_index(self):
        sitemap = ET.parse(ROOT / "sitemap.xml")
        urls = [entry.text for entry in sitemap.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc")]
        expected = {TARGET + route for route in self.canonical_pages}
        self.assertEqual(len(urls), len(set(urls)))
        self.assertEqual(set(urls), expected)
        index = json.loads((ROOT / "siteassets" / "search-index.json").read_text(encoding="utf-8"))
        self.assertEqual({entry["path"] for entry in index}, set(self.canonical_pages))
        self.assertNotIn("glaonline.com", str(index))
        self.assertTrue(all("blog" not in url for url in urls))

    def test_internal_links_use_canonical_routes(self):
        for route, (path, soup) in self.pages.items():
            for link in soup.find_all("a", href=True):
                parsed = urllib.parse.urlsplit(link["href"])
                if parsed.scheme or parsed.netloc or not parsed.path:
                    continue
                target = ROOT / parsed.path.lstrip("/") if parsed.path.startswith("/") else path.parent / urllib.parse.unquote(parsed.path)
                if target.is_dir():
                    target /= "index.html"
                if target.is_file() and target.suffix == ".html":
                    with self.subTest(route=route, link=link["href"]):
                        self.assertEqual(parsed.path, canonical_route(route_for(target.resolve(), ROOT)))

    def test_existing_forms_and_contacts(self):
        for route, (_, soup) in self.pages.items():
            with self.subTest(route=route):
                self.assertEqual(len(soup.select("#admission-enquiry")), 1)
                for form in soup.select("[data-local-form]"):
                    self.assertEqual(form["action"], "/api/form.php")
                    self.assertIsNotNone(form.select_one('[name="consent"]'))
                self.assertTrue(soup.select('a[href="tel:+919311381814"]'))
        self.assertIsNotNone(self.pages["/contact-us/"][1].select_one(
            'a[href="mailto:admissions@glaonlineadmission.com"]'))
        procedure = self.pages["/admission/admission-procedure/"][1].main.get_text(" ", strip=True)
        self.assertNotIn("Login Credential", procedure)
        self.assertIn("Complete University Registration", procedure)

    def test_images_and_crawl_rules(self):
        for route, (_, soup) in self.pages.items():
            with self.subTest(route=route):
                self.assertFalse(soup.select("img:not([alt])"))
                self.assertFalse(soup.select('meta[name="keywords"]'))
                sources = {image.get("src") for image in soup.find_all("img")}
                for preload in soup.select('link[rel="preload"][as="image"]'):
                    if "uploads/home/banner_images/" in preload.get("href", ""):
                        self.assertIn(preload["href"], sources)
        robots = (ROOT / "robots.txt").read_text()
        for path in ["/api/", "/tools/", "/.git/"]:
            self.assertIn(f"Disallow: {path}", robots)
        self.assertNotIn("Disallow: /siteassets/", robots)
        rules = (ROOT / ".htaccess").read_text()
        self.assertIn("R=301", rules)
        self.assertIn("/program/online-$1/", rules)
        self.assertIn("THE_REQUEST", rules)

    def test_generation_is_idempotent(self):
        def snapshot(soup):
            return {
                "title": str(soup.title),
                "metadata": sorted(str(tag) for tag in soup.find_all("meta")),
                "canonical": str(soup.select_one('link[rel="canonical"]')),
                "schema": json.loads(str(soup.select_one('script[type="application/ld+json"]').string)),
                "body": str(soup.body),
            }

        for route, (path, soup) in self.pages.items():
            with self.subTest(route=route):
                candidate = BeautifulSoup(str(soup), "lxml")
                before = snapshot(candidate)
                apply_seo(candidate, path, ROOT)
                self.assertEqual(snapshot(BeautifulSoup(str(candidate), "lxml")), before)


if __name__ == "__main__":
    unittest.main()
