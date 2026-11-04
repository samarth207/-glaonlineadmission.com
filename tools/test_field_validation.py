"""Validation-only API tests; use a PHP server with a nonexistent GLA_DB_CONFIG."""

import http.cookiejar
import json
import unittest
import urllib.error
import urllib.request
import uuid


class FieldValidationTests(unittest.TestCase):
    def setUp(self):
        self.client = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar())
        )
        with self.client.open("http://127.0.0.1:8765/api/form.php") as response:
            self.token = json.load(response)["token"]

    def submit(self, **changes):
        data = {
            "submission_id": str(uuid.uuid4()), "form_type": "enquiry",
            "name": "Validation Test", "email": "user+admissions@example.com",
            "phone": "+91 9876543210", "program": "MBA",
            "consent": True, "source_path": "/", **changes,
        }
        request = urllib.request.Request(
            "http://127.0.0.1:8765/api/form.php", data=json.dumps(data).encode(),
            headers={"Content-Type": "application/json", "X-CSRF-Token": self.token},
        )
        try:
            response = self.client.open(request)
        except urllib.error.HTTPError as error:
            response = error
        with response:
            return response.status, json.load(response)

    def test_invalid_email(self):
        for email in ["", "user@", "user@example", ".user@example.com",
                      "user..name@example.com", "user@example..com", "user@-example.com"]:
            with self.subTest(email=email):
                status, result = self.submit(email=email)
                self.assertEqual(status, 422)
                self.assertEqual(result["field"], "email")

    def test_invalid_phones(self):
        for field in ["phone", "alternate_phone"]:
            for phone in ["123", "0000000000", "1111111111", "+4412345678901234",
                          "123456abc", "++44 7700900123", "0123456789"]:
                with self.subTest(field=field, phone=phone):
                    status, result = self.submit(**{field: phone})
                    self.assertEqual(status, 422)
                    self.assertEqual(result["field"], field)
        self.assertEqual(self.submit(phone="")[0], 422)

    def test_valid_formats_reach_configuration_check(self):
        for phone in ["9876543210", "+91 98765 43210", "+44 7700 900123",
                      "+1 (202) 555-0123", "+123456789012345"]:
            with self.subTest(phone=phone):
                status, result = self.submit(phone=phone, alternate_phone="")
                self.assertEqual(status, 503)
                self.assertIn("not configured", result["message"])
        self.assertEqual(self.submit(alternate_phone="+44 7700 900123")[0], 503)
        self.assertEqual(self.submit(email=" user@example.co.uk ")[0], 503)


if __name__ == "__main__":
    unittest.main()
