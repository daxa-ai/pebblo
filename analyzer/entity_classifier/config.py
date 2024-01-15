from enum import Enum


class Entities(Enum):
    # PII
    US_SSN = "US SSN"
    US_PASSPORT = "US Passport number"
    US_DRIVER_LICENSE = "US Drivers License"

    # Financial
    CREDIT_CARD = "Credit card number"
    US_BANK_NUMBER = "US Bank Account Number"
    IBAN_CODE = "IBAN code"
    US_ITIN = "US ITIN"
