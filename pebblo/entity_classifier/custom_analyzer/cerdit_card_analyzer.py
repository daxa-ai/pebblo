from typing import List, Tuple

from presidio_analyzer import Pattern
from presidio_analyzer.predefined_recognizers.credit_card_recognizer import (
    CreditCardRecognizer,
)


class ExtendedCreditCardRecognizer(CreditCardRecognizer):
    """
    Extends the Credit Card Recognizer by adding support for additional credit card types.
    """

    # Define supported card patterns (can use the regex you provided)
    ADDITIONAL_PATTERNS = [
        Pattern("Amex Card", r"\b3[47][0-9]{13}\b", 0.5),
        Pattern("BCGlobal", r"\b(6541|6556)[0-9]{12,15}\b", 0.5),
        Pattern("Carte Blanche Card", r"\b389[0-9]{11}\b", 0.5),
        Pattern("Diners Club", r"\b3(?:0[0-5]|[68][0-9])[0-9]{11}\b", 0.5),
        Pattern(
            "Discover",
            r"\b65[4-9][0-9]{13}|\b64[4-9][0-9]{13}|\b6011[0-9]{12}|\b(622(?:12[6-9]|1[3-9][0-9]|[2-8][0-9]{3}|9[01][0-9]|92[0-5])[0-9]{10})\b",
            0.5,
        ),
        Pattern("Insta Payment", r"\b63[7-9][0-9]{13}\b", 0.5),
        Pattern("JCB Card", r"\b(?:2131|1800|35\d{3})\d{11}\b", 0.5),
        Pattern("KoreanLocalCard", r"\b9[0-9]{15}\b", 0.5),
        Pattern("Laser Card", r"\b(6304|6706|6709|6771)[0-9]{12,15}\b", 0.5),
        Pattern(
            "Maestro Card", r"\b(5018|5020|5038|6304|6759|6761|6763)[0-9]{8,15}\b", 0.5
        ),
        Pattern(
            "Mastercard",
            r"\b5[1-5][0-9]{14}\b|\b2(22[1-9][0-9]{12}|2[3-9][0-9]{13}|[3-6][0-9]{14}|7[0-1][0-9]{13}|720[0-9]{12})\b",
            0.5,
        ),
        Pattern("Solo Card", r"\b(6334|6767)[0-9]{12,15}\b", 0.5),
        Pattern(
            "Switch Card",
            r"\b(4903|4905|4911|4936|6333|6759)[0-9]{12,15}\b|\b564182[0-9]{10,13}\b|\b633110[0-9]{10,13}\b",
            0.5,
        ),
        Pattern("Union Pay", r"\b62[0-9]{14,17}\b", 0.5),
        Pattern("Visa Card", r"\b4[0-9]{12}(?:[0-9]{3})?\b", 0.5),
        # Pattern(
        #     "All Credit Cards (weak)",
        #     r"\b((4\d{3})|(5[0-5]\d{2})|(6\d{3})|(1\d{3})|(3\d{3}))[- ]?(\d{3,4})[- ]?(\d{3,4})[- ]?(\d{3,5})\b",  # noqa: E501
        #     0.3,
        # ),
    ]
    # Define keywords related to credit cards
    CONTEXT = [
        "credit",
        "credit_card",
        "card" "debit",
        "Visa",
        "Mastercard",
        "Amex",
        "Discover",
        "JCB",
        "Diners Club",
        "Carte Blanche",
        "Insta Payment",
        "Maestro",
        "UnionPay",
        "BCGlobal",
        "KoreanLocalCard",
        "credit",
        "card",
        "cc ",
        "diners",
        "instapayment",
    ]

    def __init__(self):
        # Call the base class constructor
        super().__init__(
            supported_entity="CREDIT_CARD",  # The entity you are identifying
            patterns=self.ADDITIONAL_PATTERNS,  # Add the extended patterns
            context=self.CONTEXT,
        )

    def validate_result(self, pattern_text: str) -> bool:  # noqa D102
        sanitized_value = self.__sanitize_value(pattern_text, self.replacement_pairs)
        checksum = self.__luhn_checksum(sanitized_value)

        return checksum

    @staticmethod
    def __luhn_checksum(sanitized_value: str) -> bool:
        def digits_of(n: str) -> List[int]:
            return [int(dig) for dig in str(n)]

        digits = digits_of(sanitized_value)
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        checksum = sum(odd_digits)
        for d in even_digits:
            checksum += sum(digits_of(str(d * 2)))
        return checksum % 10 == 0

    @staticmethod
    def __sanitize_value(text: str, replacement_pairs: List[Tuple[str, str]]) -> str:
        for search_string, replacement_string in replacement_pairs:
            text = text.replace(search_string, replacement_string)
        return text
