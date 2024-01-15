"""
Copyright (c) 2023 Cloud Defense, Inc. All rights reserved.

These are all enums related to Inspector.
"""
from enum import Enum


class ConfidenceScore(Enum):
    Topic = "0.60"
    NER = "0.80"


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


class Topics(Enum):
    HARMFUL_ADVICE = "Harmful Advice"
    MEDICAL_ADVICE = "Medical Advice"


class InspectorConfig(Enum):
    input_max_len = 512  # Word Length
