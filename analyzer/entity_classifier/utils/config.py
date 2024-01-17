"""
Copyright (c) 2024 Cloud Defense, Inc. All rights reserved.
"""
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


class SecretEntities(Enum):
    GITHUB_TOKEN = "Github Token"
    SLACK_TOKEN = "Slack Token"
    # SLACK_TOKEN = "Slack Token V2"
    AWS_ACCESS_KEY = "AWS Access Key"
    AWS_SECRET_KEY = "AWS Secret Key"
    AZURE_KEY_ID = "Azure Key ID"
    AZURE_CLIENT_SECRET = "Azure Client Secret"
    GOOGLE_API_KEY = "Google API Key"


class ConfidenceScore(Enum):
    Entity = "0.80"
