"""
Copyright (c) 2023 Cloud Defense, Inc. All rights reserved.

These are all enums related to Regex Patterns.
"""

regex_secrets_patterns = {
    "Azure Key ID": r"""(?i)(%s).{0,20}([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})""",
    "Azure Client Secret": r"""(?i)(%s).{0,20}([a-z0-9_\.\-~]{34})""",
    "Auth0 API Token": r"""(?i)(?:auth0)(?:.|[\n\r]){0,40}\b(ey[a-zA-Z0-9._-]+)\b""",
    "Auth0 OAuth Client ID": r"""(?i)(?:auth0)(?:.|[\n\r]){0,40}\b([a-zA-Z0-9_-]{32,60})\b""",
    "AWS API ID": r"""\b((?:AKIA|ABIA|ACCA|ASIA)[0-9A-Z]{16})\b""",
    "AWS API Secret": r"""\b([A-Za-z0-9+/]{40})[ \r\n'"\x60]""",
    "Github Token": r"""\b((?:ghp|gho|ghu|ghs|ghr)_[a-zA-Z0-9]{36,255})\b""",
    "Github Private Key": r"""(?i)(?:github)(?:.|[\n\r]){0,40}(-----BEGIN RSA PRIVATE KEY-----\s[A-Za-z0-9+\/\s]*\s
    ----END RSA PRIVATE KEY-----)""",
    "Gitlab API Key": r"""(?i)(?:gitlab)(?:.|[\n\r]){0,40}\b([a-zA-Z0-9\-=_]{20,22})\b""",
    "Gitlab API Key V2": r"""\b(glpat-[a-zA-Z0-9\-=_]{20,22})\b""",
    "Okta API Token": r"""00[a-zA-Z0-9_-]{40}""",
    "Private Key": r"""/(?i)-----\s*?BEGIN[ A-Z0-9_-]*?PRIVATE KEY\s*?-----[\s\S]*?----\s*?END[ A-Z0-9_-]*? 
    PRIVATE KEY\s*?-----/gm""",
    "Slack Token": r"""(xoxb|xoxp|xapp|xoxa|xoxr)\-[0-9]{10,13}\-[a-zA-Z0-9\-]*""",
    "Slack Token V2": r"""xox[baprs]-([0-9a-zA-Z]{10,48})?""",
    "Youtube/Google API Key": r"""(?i)(?:youtube)(?:.|[\n\r]){0,40}\bAIza[0-9A-Za-z\-_]{35}\b""",
}
