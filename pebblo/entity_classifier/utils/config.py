"""
Copyright (c) 2024 Cloud Defense, Inc. All rights reserved.
"""
from enum import Enum

secret_entities_context_mapping = {
    "Github Token": ["github", "github_token"],
    "Slack Token": ["slack", "slack token", "slack_token"],
    "AWS Access Key": ["aws_access_key", "aws_key", "access", "id", "api"],
    "AWS Secret Key": ["aws_secret_key", "secret"],
    "Azure Key ID": ["azure_key", "azure_key_id", "azure_id", "key"],
    "Azure Client Secret": ["azure_client_secret", "client", "secret"],
    "Google API Key": ["google_api_key", "google_key", "google"],
}

ALL_ENTITIES = [
    "US_SSN",
    "US_PASSPORT",
    "US_DRIVER_LICENSE",
    "CREDIT_CARD",
    "US_BANK_NUMBER",
    "IBAN_CODE",
    "US_ITIN",
    "GITHUB_TOKEN",
    "SLACK_TOKEN",
    "AWS_ACCESS_KEY",
    "AWS_SECRET_KEY",
    "AZURE_KEY_ID",
    "AZURE_CLIENT_SECRET",
    "GOOGLE_API_KEY",
]


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
    Entity = "0.8"  # based on this score entity output is finalized
    EntityMinScore = "0.45"  # It denotes the pattern's strength
    EntityContextSimilarityFactor = (
        "0.35"  # It denotes how much to enhance confidence of match entity
    )
    EntityMinScoreWithContext = "0.4"  # It denotes minimum confidence score
