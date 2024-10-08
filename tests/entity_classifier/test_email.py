import unittest

from presidio_analyzer import AnalyzerEngine


class TestEmailRecognizer(unittest.TestCase):
    def setUp(self):
        # Set up an instance of the EmailRecognizer
        self.analyzer = AnalyzerEngine()

    def test_basic_email(self):
        # Basic email detection
        text = "My email is john.doe@example.com."
        results = self.analyzer.analyze(text, entities=["EMAIL_ADDRESS"], language="en")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].entity_type, "EMAIL_ADDRESS")
        self.assertEqual(results[0].start, 12)
        self.assertEqual(results[0].end, 32)

    def test_email_with_numbers(self):
        # Email with numbers in the username
        text = "Contact me at jane123@example.com."
        results = self.analyzer.analyze(text, entities=["EMAIL_ADDRESS"], language="en")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].entity_type, "EMAIL_ADDRESS")
        self.assertEqual(results[0].start, 14)
        self.assertEqual(results[0].end, 33)

    def test_email_with_subdomain(self):
        # Email with a subdomain
        text = "My work email is john.doe@mail.company.com."
        results = self.analyzer.analyze(text, entities=["EMAIL_ADDRESS"], language="en")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].entity_type, "EMAIL_ADDRESS")
        self.assertEqual(results[0].start, 17)
        self.assertEqual(results[0].end, 42)

    def test_email_with_special_characters(self):
        # Email with special characters
        text = "My email is john.doe+alias@example.com."
        results = self.analyzer.analyze(text, entities=["EMAIL_ADDRESS"], language="en")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].entity_type, "EMAIL_ADDRESS")
        self.assertEqual(results[0].start, 12)
        self.assertEqual(results[0].end, 38)

    def test_email_with_multiple_dots(self):
        # Email with multiple dots in the domain part
        text = "Send the report to reports@sub.example.co.uk."
        results = self.analyzer.analyze(text, entities=["EMAIL_ADDRESS"], language="en")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].entity_type, "EMAIL_ADDRESS")
        self.assertEqual(results[0].start, 19)
        self.assertEqual(results[0].end, 44)

    def test_multiple_emails(self):
        # Text with multiple emails
        text = "Emails: alice@example.com, bob@example.org."
        results = self.analyzer.analyze(text, entities=["EMAIL_ADDRESS"], language="en")
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].entity_type, "EMAIL_ADDRESS")
        self.assertEqual(results[0].start, 8)
        self.assertEqual(results[0].end, 25)
        self.assertEqual(results[1].entity_type, "EMAIL_ADDRESS")
        self.assertEqual(results[1].start, 27)
        self.assertEqual(results[1].end, 42)

    def test_invalid_email_missing_at_symbol(self):
        # Invalid email (missing '@' symbol)
        text = "This is not a valid email: john.doeexample.com."
        results = self.analyzer.analyze(text, entities=["EMAIL_ADDRESS"], language="en")
        self.assertEqual(len(results), 0)

    def test_invalid_email_missing_domain(self):
        # Invalid email (missing domain part)
        text = "Invalid email: john.doe@."
        results = self.analyzer.analyze(text, entities=["EMAIL_ADDRESS"], language="en")
        self.assertEqual(len(results), 0)

    def test_invalid_email_missing_username(self):
        # Invalid email (missing username part)
        text = "Invalid email: @example.com."
        results = self.analyzer.analyze(text, entities=["EMAIL_ADDRESS"], language="en")
        self.assertEqual(len(results), 0)

    def test_email_with_context(self):
        # Email with context words like 'email' present
        text = "Please contact me at email: john.doe@example.com."
        results = self.analyzer.analyze(text, entities=["EMAIL_ADDRESS"], language="en")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].entity_type, "EMAIL_ADDRESS")
        self.assertEqual(results[0].start, 28)
        self.assertEqual(results[0].end, 48)

    def test_email_with_trailing_punctuation(self):
        # Email with trailing punctuation like comma or period
        text = "My email is john.doe@example.com, contact me soon."
        results = self.analyzer.analyze(text, entities=["EMAIL_ADDRESS"], language="en")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].entity_type, "EMAIL_ADDRESS")
        self.assertEqual(results[0].start, 12)
        self.assertEqual(results[0].end, 32)

    def test_invalid_email_with_special_characters(self):
        # Invalid email with special characters in the wrong places
        text = "Invalid email: john.doe@exam#ple.com."
        results = self.analyzer.analyze(text, entities=["EMAIL_ADDRESS"], language="en")
        self.assertEqual(len(results), 0)
