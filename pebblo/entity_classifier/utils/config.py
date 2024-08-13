"""
Copyright (c) 2024 Cloud Defense, Inc. All rights reserved.
"""

from enum import Enum

secret_entities_context_mapping = {
    "github-token": ["github", "github_token", "git"],
    "slack-token": ["slack", "slack token", "slack_token"],
    "aws-access-key": ["aws_access_key", "aws_key", "access", "id", "api"],
    "aws-secret-key": ["aws_secret_key", "secret"],
    "azure-key-id": ["azure_key", "azure_key_id", "azure_id", "key"],
    "azure-client-secret": ["azure_client_secret", "client", "secret"],
    "google-api-key": ["google_api_key", "google_key", "google"],
}


class Entities(Enum):
    # PII
    US_SSN = "us-ssn"
    US_PASSPORT = "us-passport-number"
    US_DRIVER_LICENSE = "us-drivers-license"

    # Financial
    CREDIT_CARD = "credit-card-number"
    US_BANK_NUMBER = "us-bank-account-number"
    IBAN_CODE = "iban-code"
    US_ITIN = "us-itin"


class SecretEntities(Enum):
    GITHUB_TOKEN = "github-token"
    SLACK_TOKEN = "slack-token"
    AWS_ACCESS_KEY = "aws-access-key"
    AWS_SECRET_KEY = "aws-secret-key"
    AZURE_KEY_ID = "azure-key-id"
    AZURE_CLIENT_SECRET = "azure-client-secret"
    GOOGLE_API_KEY = "google-api-key"


class PIIGroups(Enum):
    Identification = "pii-identification"
    Financial = "pii-financial"
    Secrets = "secrets_and_tokens"


entity_group_conf_mapping = {
    # Identification
    Entities.US_SSN.value: (0.8),
    Entities.US_PASSPORT.value: (0.4),
    Entities.US_DRIVER_LICENSE.value: (0.4),
    # Financial
    Entities.US_ITIN.value: (0.8),
    Entities.CREDIT_CARD.value: (0.8),
    Entities.US_BANK_NUMBER.value: (0.4),
    Entities.IBAN_CODE.value: (0.8),
    # Secret
    SecretEntities.GITHUB_TOKEN.value: (0.8),
    SecretEntities.SLACK_TOKEN.value: (0.8),
    SecretEntities.AWS_ACCESS_KEY.value: (0.45),
    SecretEntities.AWS_SECRET_KEY.value: (0.8),
    SecretEntities.AZURE_KEY_ID.value: (0.8),
    SecretEntities.AZURE_CLIENT_SECRET.value: (0.8),
    SecretEntities.GOOGLE_API_KEY.value: (0.8),
}


class ConfidenceScore(Enum):
    Entity = "0.8"  # based on this score entity output is finalized
    EntityMinScore = "0.45"  # It denotes the pattern's strength
    EntityContextSimilarityFactor = (
        "0.35"  # It denotes how much to enhance confidence of match entity
    )
    EntityMinScoreWithContext = "0.4"  # It denotes minimum confidence score
