import unittest

from presidio_analyzer import AnalyzerEngine

from pebblo.entity_classifier.custom_analyzer.cerdit_card_analyzer import (
    ExtendedCreditCardRecognizer,
)


class TestExtendedCreditCardRecognizer(unittest.TestCase):
    def setUp(self):
        # Set up an instance of the ExtendedCreditCardRecognizer
        self.analyzer = AnalyzerEngine()
        self.recognizer = ExtendedCreditCardRecognizer()
        self.analyzer.registry.add_recognizer(self.recognizer)

    def test_visa_card(self):
        # Visa card number (no spaces/hyphens)
        text = "My card number is 4111111111111111."
        results = self.analyzer.analyze(text, entities=["CREDIT_CARD"], language="en")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].entity_type, "CREDIT_CARD")
        self.assertEqual(results[0].start, 18)
        self.assertEqual(results[0].end, 34)

    def test_visa_card_with_spaces(self):
        # Visa card number with spaces
        text = "My card number is 4111 1111 1111 1111."
        results = self.analyzer.analyze(text, entities=["CREDIT_CARD"], language="en")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].entity_type, "CREDIT_CARD")
        self.assertEqual(results[0].start, 18)
        self.assertEqual(results[0].end, 37)

    def test_mastercard_with_hyphens(self):
        # Mastercard number with hyphens
        text = "My card number is 5500-0000-0000-0004."
        results = self.analyzer.analyze(text, entities=["CREDIT_CARD"], language="en")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].entity_type, "CREDIT_CARD")
        self.assertEqual(results[0].start, 18)
        self.assertEqual(results[0].end, 37)

    def test_amex_card(self):
        # American Express card number
        text = "My Amex card number is 378282246310005."
        results = self.analyzer.analyze(text, entities=["CREDIT_CARD"], language="en")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].entity_type, "CREDIT_CARD")
        self.assertEqual(results[0].start, 23)
        self.assertEqual(results[0].end, 38)

    def test_diners_club_card(self):
        # Diners Club card number
        text = "My Diners Club card is 30569309025904."
        results = self.analyzer.analyze(text, entities=["CREDIT_CARD"], language="en")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].entity_type, "CREDIT_CARD")
        self.assertEqual(results[0].start, 23)
        self.assertEqual(results[0].end, 37)

    def test_jcb_card(self):
        # JCB card number
        text = "My JCB card number is 3530111333300000."
        results = self.analyzer.analyze(text, entities=["CREDIT_CARD"], language="en")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].entity_type, "CREDIT_CARD")
        self.assertEqual(results[0].start, 22)
        self.assertEqual(results[0].end, 38)

    def test_invalid_card(self):
        # Invalid card number
        text = "This is an invalid card number 1234567890123456."
        results = self.analyzer.analyze(text, entities=["CREDIT_CARD"], language="en")
        self.assertEqual(len(results), 0)

    def test_credit_card_with_context(self):
        # Credit card number with context words
        text = "The credit card number 4111111111111111 is valid."
        results = self.analyzer.analyze(text, entities=["CREDIT_CARD"], language="en")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].entity_type, "CREDIT_CARD")
        self.assertEqual(results[0].start, 23)
        self.assertEqual(results[0].end, 39)

    def test_validate_result_with_luhn_checksum(self):
        # Valid credit card number using Luhn checksum validation
        valid_card = "4111111111111111"
        result = self.recognizer.validate_result(valid_card)
        self.assertTrue(result)

    def test_validate_result_invalid_luhn_checksum(self):
        # Invalid credit card number using Luhn checksum validation
        invalid_card = "4111111111111112"
        result = self.recognizer.validate_result(invalid_card)
        self.assertFalse(result)
