"""
Copyright (c) 2024 Cloud Defense, Inc. All rights reserved.

These are all enums related to Regex Patterns.
"""

regex_secrets_patterns = {
    "github-token": r"""\b((?:ghp|gho|ghu|ghs|ghr)_[a-zA-Z0-9]{36,255})\b""",
    "slack-token": r"""(xoxb|xoxp|xapp|xoxa|xoxr)\-[0-9]{10,13}\-[a-zA-Z0-9\-]*""",
    # "Slack Token V2": r"""xox[baprs]-([0-9a-zA-Z]{10,48})?""",
    "aws-access-key": r"""\b((?:AKIA|ABIA|ACCA|ASIA)[0-9A-Z]{16})\b""",
    "aws-secret-key": r"""\b([A-Za-z0-9+/]{40})[ \r\n'"\x60]""",
    "azure-key-id": r"""(?i)(%s).{0,20}([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})""",
    "azure-client-secret": r"""\b(?i)(%s).{0,20}([a-z0-9_\.\-~]{34})\b""",
    "google-api-key": r"""(?i)(?:youtube)(?:.|[\n\r]){0,40}\bAIza[0-9A-Za-z\-_]{35}\b""",
}
