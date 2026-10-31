"""Integration tests against an isolated PHP server and MySQL-compatible database."""

import concurrent.futures
import http.cookiejar
import json
import os
import subprocess
import unittest
import urllib.error
import urllib.request
import uuid
from pathlib import Path


BASE = os.environ.get("GLA_TEST_URL", "http://127.0.0.1:8765")
MYSQL = os.environ.get("GLA_TEST_MYSQL")
SCHEMA = Path(__file__).with_name("schema.sql")
if BASE not in {"http://127.0.0.1:8765", "http://127.0.0.1:8766"} or not MYSQL:
    raise RuntimeError("Tests require the isolated local server and GLA_TEST_MYSQL client path.")


def sql(query):
    return subprocess.check_output([
        MYSQL, "--no-defaults", "--host=127.0.0.1", "--port=13307",
        "--user=root", "--batch", "--skip-column-names", "gla_mirror_validation",
        "--execute=" + query,
    ], text=True).strip()


class Client:
    def __init__(self):
        self.cookies = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cookies))
        status, result, self.headers = self.request("GET")
        assert status == 200
        self.token = result["token"]

    def request(self, method, payload=None, headers=None):
        request = urllib.request.Request(
            BASE + "/api/form.php",
            method=method,
            data=None if payload is None else payload.encode(),
            headers=headers or {},
        )
        try:
            response = self.opener.open(request, timeout=15)
        except urllib.error.HTTPError as error:
            response = error
        with response:
            raw = response.read()
            result = json.loads(raw) if raw else {}
            return response.status, result, response.headers

    def post(self, payload, token=None):
        return self.request("POST", json.dumps(payload), {
            "Content-Type": "application/json",
            "X-CSRF-Token": self.token if token is None else token,
        })


def payload(**overrides):
    return {
        "submission_id": str(uuid.uuid4()), "form_type": "enquiry",
        "name": "Local Validation", "email": "validation@example.test",
        "phone": "+91 9876543210", "program": "MBA",
        "specialization": "Online MBA - Finance Management",
        "source_path": "/program/online-mba/", "consent": True, "website": "",
    } | overrides


class FormTests(unittest.TestCase):
    def setUp(self):
        sql("TRUNCATE TABLE form_submissions")
        self.client = Client()

    def count(self):
        return int(sql("SELECT COUNT(*) FROM form_submissions"))

    def test_session_cookie(self):
        cookie = self.client.headers["Set-Cookie"]
        self.assertIn("HttpOnly", cookie)
        self.assertIn("SameSite=Strict", cookie)
        self.assertEqual(len(self.client.token), 64)

    def test_enquiry_persists_fields(self):
        status, result, _ = self.client.post(payload())
        self.assertEqual(status, 201)
        self.assertTrue(result["saved"])
        self.assertEqual(self.count(), 1)
        row = sql("SELECT CONCAT(form_type,'|',name,'|',email,'|',phone,'|',program,'|',specialization,'|',consent,'|',source_path) FROM form_submissions")
        self.assertEqual(row, "enquiry|Local Validation|validation@example.test|+91 9876543210|MBA|Online MBA - Finance Management|1|/program/online-mba/")

    def test_contact_persists_fields(self):
        data = payload(form_type="contact", company="Example Company", country="India",
                       state="Uttar Pradesh", city="Mathura", message="Please contact me.")
        status, result, _ = self.client.post(data)
        self.assertEqual(status, 201)
        self.assertTrue(result["saved"])
        self.assertEqual(sql("SELECT CONCAT(company,'|',country,'|',state,'|',city,'|',message) FROM form_submissions"),
                         "Example Company|India|Uttar Pradesh|Mathura|Please contact me.")

    def test_hero_form_persists_alternate_and_district(self):
        data = payload(form_layout="hero", alternate_phone="+91 9123456780",
                       state="Uttar Pradesh", city="Mathura")
        self.assertEqual(self.client.post(data)[0], 201)
        self.assertEqual(sql("SELECT CONCAT(alternate_phone,'|',state,'|',city) FROM form_submissions"),
                         "+91 9123456780|Uttar Pradesh|Mathura")

    def test_invalid_hero_district_and_alternate(self):
        for changes in [
            {"alternate_phone": "invalid"},
            {"alternate_phone": "1" * 16},
            {"form_layout": "invalid"},
            {"form_layout": "hero", "state": "Uttar Pradesh", "city": ""},
            {"form_layout": "hero", "state": "Uttar Pradesh", "city": "Invalid District"},
        ]:
            with self.subTest(changes=changes):
                self.assertEqual(self.client.post(payload(**changes))[0], 422)
        self.assertEqual(self.count(), 0)

    def test_duplicate_retry_does_not_insert_twice(self):
        data = payload()
        self.assertEqual(self.client.post(data)[0], 201)
        status, result, _ = self.client.post(data)
        self.assertEqual(status, 200)
        self.assertTrue(result["saved"])
        self.assertEqual(self.count(), 1)

    def test_invalid_csrf(self):
        self.assertEqual(self.client.post(payload(), token="invalid")[0], 403)
        self.assertEqual(self.count(), 0)

    def test_invalid_or_missing_fields(self):
        for changes in [
            {"name": ""}, {"email": "not-an-email"}, {"phone": "123"},
            {"phone": "1" * 16}, {"program": "invalid"}, {"consent": False},
            {"form_type": "login"}, {"submission_id": "bad-id"},
            {"source_path": "https://outside.example"}, {"name": ["array"]},
            {"website": "bot.example"}, {"source_path": "/../private"},
            {"form_type": "contact", "company": ""},
        ]:
            with self.subTest(changes=changes):
                self.assertEqual(self.client.post(payload(**changes))[0], 422)
        self.assertEqual(self.count(), 0)

    def test_unicode_length_boundary(self):
        name = "\u0938" * 100
        self.assertEqual(self.client.post(payload(name=name))[0], 201)
        self.assertEqual(self.client.post(payload(name=name + "\u0938"))[0], 422)
        self.assertEqual(self.count(), 1)

    def test_message_length_boundary(self):
        self.assertEqual(self.client.post(payload(message="x" * 3000))[0], 201)
        self.assertEqual(self.client.post(payload(message="x" * 3001))[0], 422)

    def test_prepared_insert(self):
        name = "O'Neil'); DROP TABLE form_submissions; --"
        self.assertEqual(self.client.post(payload(name=name))[0], 201)
        self.assertEqual(sql("SELECT name FROM form_submissions"), name)
        self.assertEqual(self.count(), 1)

    def test_rate_limit(self):
        for _ in range(5):
            self.assertEqual(self.client.post(payload())[0], 201)
        status, result, headers = self.client.post(payload())
        self.assertEqual(status, 429)
        self.assertFalse(result["saved"])
        self.assertEqual(headers["Retry-After"], "600")
        self.assertEqual(self.count(), 5)

    def test_parallel_requests_respect_limit(self):
        def submit(_):
            return Client().post(payload())[0]
        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
            statuses = list(pool.map(submit, range(6)))
        self.assertEqual(statuses.count(201), 5)
        self.assertEqual(statuses.count(429), 1)
        self.assertEqual(self.count(), 5)

    def test_invalid_request_formats(self):
        headers = {"Content-Type": "application/json", "X-CSRF-Token": self.client.token}
        self.assertEqual(self.client.request("POST", "{invalid", headers)[0], 400)
        self.assertEqual(self.client.request("POST", "[]", headers)[0], 400)
        self.assertEqual(self.client.request("POST", "x" * 16385, headers)[0], 413)
        self.assertEqual(self.client.request("POST", "text", {"X-CSRF-Token": self.client.token})[0], 415)
        self.assertEqual(self.client.request("PUT")[0], 405)
        self.assertEqual(self.count(), 0)

    def test_storage_failure_is_not_success(self):
        sql("DROP TABLE form_submissions")
        try:
            status, result, _ = self.client.post(payload())
            self.assertEqual(status, 503)
            self.assertFalse(result["saved"])
            self.assertNotIn("password", json.dumps(result).lower())
        finally:
            sql(SCHEMA.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
