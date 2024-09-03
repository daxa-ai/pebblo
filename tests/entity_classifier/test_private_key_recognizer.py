from pebblo.entity_classifier.custom_analyzer.private_key_analyzer import (
    PrivateKeyRecognizer,
)

# The secrets used in this file are taken from
# https://docs.gitguardian.com/secrets-detection/secrets-detection-engine/detectors/specifics/private_key_generic


def test_private_key_recognizer_no_match():
    # Test case where there is no private key in the text
    text = "This is a test string with no private key."
    recognizer = PrivateKeyRecognizer()
    results = recognizer.analyze(text, entities=["PRIVATE_KEY"])

    assert len(results) == 0

    # Test case with a string that looks like a private key but fails entropy check
    text = "-----BEGIN PRIVATE KEY-----\nAAAAAAAABBBBBBBB\n-----END PRIVATE KEY-----\n"
    recognizer = PrivateKeyRecognizer()
    results = recognizer.analyze(text)

    assert len(results) == 0


def test_private_key_recognizer__matche():
    # Test case with multiple private keys in the text
    text = """
        -----BEGIN PRIVATE KEY-----
KJICdQIBADALBgkqhkiG9w0BAQEEggJhMIICXQIBAAKBgQC7JHoJfg6yNzLMOWet
8Z49a4KD0dCspMAYvo2YAMB7/wdEycocujbhJ2n/seONi+5XqTqqFkM5VBl8rmkk
FPZk/7x0xmdsTPECSWnHK+HhoaNDFPR3j8jQhVo1laxiqcEhAHegi5cwtFosuJAv
SKAFKEvyD43si00DQnXWrYHAEQIDAQABAoGAAPy5SiYHiVErU3KR4Bg+pl4x75wM
FiRC0Cgz+frQPFQEBsAV9RuasyQxqzxrR0Ow0qncBeGBWbYE6WZhqtcLAI895b+i
+F4lbB4iD7T9QeIDMV/aIMXA81UO4cns1z4qDAHKeyLLrPQrJ/B4X7XC+egUWm5+
hr1qmyAMusyXIBECQQDJWZ8piluf4yrYfsJAn6hF5T4RjTztbqvO0GVG2McHY7Uj
NPSffhzHx/ll0fQEQji+OgydCCX8o3HZrgw5YfSJAkEA7e+rqdU5nO5ZG//PSEQb
tjLnRiTzBH/elQhtdZ5nF7pcpNTi4k13zutmKcWW4GK75azcRGJUhu1kDM7QYAOd
SQJAVNkYcifkvna7GmooL5VYEsQsqLbM4v0NF2TIGNfG3z1MGp75KrC5LhL97MNR
we2p/bd2k0HYyCKUGnf2nMPDiQJBAI75pwittSoE240EobUGIDTSz8CJsXIxuDmL
z+KOpdpPRR5TQmbEMEspjsFpFymMiuYPgmihQbO2cJl1qScY5OkCQQCJ6m5tcN8l
Xxg/SNpjEIv+qAyUD96XVlOJlOIeLHQ8kYE0C6ZA+MsqYIzgAreJk88Yn0lU/X0/
mu/UpE/BRTfs
-----END PRIVATE KEY-----
    """
    recognizer = PrivateKeyRecognizer()
    results = recognizer.analyze(text)

    assert len(results) == 1
    assert results[0].entity_type == "PRIVATE_KEY"

    text = """
    [
        {
    'text': '-----BEGIN RSA PRIVATE KEY----- MIIEpQIBAAKCAQEA0pj32LapDxsvsOdgVWzkZMdp/k7R+KJhuXLUxFTuRQFlBDcc mIPbkKzcJZO8pTXlRrqa4TiOLmdSM1AAW4cIX6xNYjO6V6Xx7wsXntg2YlYlN59e lbaj08VY59XRwTDNqBnINUVGdJKy2qxe/NUf0+vtp9Fbms4aKYyoP6G6zVUtVjLi vZzG8+3zEJlHJzTu5TTurqYLxPSIJCSxCFWuqcmiO7wFr/IdtzbygmI3D4dlCP51 azZ4PnXYVXBb6TeB0FYEC7kAlSMFbKVRkuRAyrLQbxJWJNQOMFRO4XRyaCEbZKtO 5ig6zt8An8ncfcNLgYAsvLOgpByq+kU/Ny98CwIDAQABAoIBAQDDQokqKdH965sA TscG7Xul5S7lV3dfLE+nfky/7G8vE+fxTJf64ObG8T78qEoUdDAsr//CKonJhIq2 gMqUElM1QbBOCOARPA9hL8uqv5VM/8pqFB3CeiDTzPptmdZtZS6JWb5DhgOZOhsS nRdFHOXxu6ISIw7oLYgcVgn5VZ65mTzN6yB7pKsYkbm0NcJcmLnfuGbpQEP3WmC9 X4wO7galKdHXuSxRdcJxCag2k0W7S4UAbp1tPmRAeDdOXqbGL7hu14rUZYtkiuRP 546GDvOv+meHpDJve1hZ20CH2kRVq4DC64prPNfRJ1exSd94vlhokWL6SzTXItwm L8TUnHeBAoGBAPTi6WqbVcL9Uy2qJA8fJg7oN4yQ/goOh+mlW3Fsdig0VsQjxWWI ftb/tDv6UyHw50Ms66gT+h4dWepFVFDPb38HAhoU/RvmNCHWd33Nmhd1qf2jOQiR Q9q2qJ0gFgKFlrbJNTOkaFni2UdJ7ySS937C2rdOm5GTOaCODl6M4UjRAoGBANwn sFdT/HeY2lx84+jMxrzVOeNUpelye9G+VYk5poIMBSXX4Qm0V4EhmBOA4dEGwfhR yW/p1TG0uzvOu2igUVx2YcaxUZMLBSny++awUcnAbIoN175vqS0zhGKfKgsK1ak3 /8P32zMm1vSz3ZR/+tzgcayWmOE8O1Cfw+Zks24bAoGBAIekjKAVTIrGIOWhYXnS yhTlwaclxOEzLUtY4W7RIh2g6BKascNMuN1EI8Q5IwUg2ChYYGvoLNmzblOadVqR m/OjoSFrUMu8VlIL5oITeW/XKAKq/3Nka05hcMIfvLFG57V1e/eP8JEhWzLmnAUJ NvfK3LU+YGNhRkFNjl4G8N6RAoGBAJMmA/uaqzjU9b6zyzGjDYLRkiucPHjYiGIc sddSrTRnDFnK/SMbYxFwftEqZ8Tqm2N6ZwViaZkbj7nd5+16mmcOyTOg+UErMHxl aHE8kK4k62cq8XTb9Vu8/1NbxyIyT7UXNOCrHdwGrc5JGmVTVT2k1tXgoraJJ6wv 3SR1UmjZAoGARV26w6VMQKV0Y4ntnSIoGYWO9/15gSe2H3De+IPs4LyOP714Isi+ 2JcO4QPvgRfd5I5FY6FTi7T0Gz2/DXHggv9DXM9Q2yXMhV+3tkTuNFeDwBw7qRGy mCwOcAwHJ6GtCNvBDlpot6SauHEKKpzQobtq7giIEU3aSYR2unNg4wA= -----END RSA PRIVATE KEY-----\n',
        },
        ]
    """
    results = recognizer.analyze(text)
    assert len(results) == 1
    assert results[0].entity_type == "RSA_PRIVATE_KEY"

    text = """
- text: >
-----BEGIN ENCRYPTED PRIVATE KEY-----
MIIBrTBXBgkqhkiG9w0BBQ0wSjApBgkqhkiG9w0BBQwwHAQIVdHyvepVyXMCAggA
MAwGCCqGSIb3DQIJBQAwHQYJYIZIAWUDBAEqBBAAKxt+HUbLXHuSH7tYxtgHBIIB
UD4ncOFKjrboKx+897QTEwH7U5QXAceMQSA6OSpP4RMqWzd+DSuQ2AhW9ny+JuhZ
cuayQvXkIOyk/LUCy1ilm3fhbN2+gKiH8ghJsZzeANnWBuX8d6e6aEMLPnv101Dm
MzSz/KIV+Sw7ltUDNGo6Admwoo4FFfS8EtTsHe2NkqgliEJigWuOOfZvle45BR6W
LWASXptVC3+dI+csKPlDQi5xgjv65MpEzjc9mmkcVxRxq5lDnZaz1o3q+MJjYlFU
ONzqGQC37TJ0+gjFK2ETBoV/G6c2iUXeNZB8DabT9PBKX6TbtaoYfCnJ/wkK9NOT
1vkJsK1CxOAUhZCH2U4OhcpVsKoRFOdIBl+NbdBR6k0gK6F0GwbpA6Vpfgub5hy2
kPp+kkrC+h8EctAlp++vIoJ/F6TAnn0G65c3AVYEk84RUTDgjDoci6u74KbpQ/md
vQ==
-----END ENCRYPTED PRIVATE KEY-----

    """
    results = recognizer.analyze(text)
    assert len(results) == 1
    assert results[0].entity_type == "ENCRYPTED_PRIVATE_KEY"

    text = """
            -----BEGIN EC PRIVATE KEY-----
Proc-Type: 4,ENCRYPTED DEK-Info: AES-128-CBC,FCB6666547226B90841E09335C97A1A2
WukpA3LSI6sWjJqCOTnalyS9DkgwKYcUqlYvYpVsPRNxIKoeQG6oTEuhwMbrrzv6
TFGo7YJA5JG+0rZ9G1wuSOyMdDBumSnF6o8iwZfBvXJRsD3mw+AGZx8lAnwtlynE
jcFOAkTkz4NKiNgydiCzCMQx8vdl5PVIQBYiegCGT0o=
-----END EC PRIVATE KEY-----
"""
    results = recognizer.analyze(text)
    assert len(results) == 1
    assert results[0].entity_type == "ELLIPTIC_CURVE_PRIVATE_KEY"

    text = """
            - text: >
    -----BEGIN DSA PRIVATE KEY-----
    MIIBvAIBAAKBgQDaqdgwD3YvYwgbWzs8RQQOm8RmPztSYMUrcM7KQtdJ111sTZ/x
    VAq84frCt/TEupAN5hUFkC+bpJ/diZixQgPvLKo6FVtBKy97HSpuZT8n2pUYZ9/4
    sBTR5YQtP9qExXUYO/yR+fZ+RE9w0TbSAtHW2YZHKnoowJAHdoEGMbaChQIVAK/q
    iXNHCha4xHnIdD2jT0OUs03fAoGBAMnCeTgO09r2GquRAQmGFAT/6IGMhux7KOC8
    QrW7jDaqAYLiuA45E3Ira584RF2rg0VhewxcdEMbqNzqCeSKk9OAmwXpJ1J8vCUR
    dRojGz0DYZHJbcspoGtZF1IF6Z3BoaggRcLX6/KYLbnzFZnBXV/+//gRTbm/V2ie
    BzCWE/qEAoGBANbrGxzVTTdTD8MaVtlOpjU3RqoGFHmFCd4lv0PIt2mjFsXO3Dt/
    6BMtJVREtb74WF0SUGmnpy6FTYoDb05j2LhH1IvCSkFT5hUK0WtAJ3NidJ6ARxxD
    z2QITWI1FTr1K9NbZdR6DoTxeKfV6wWbuLywlwoWYmLe6oAmq21Oft4XAhRcKcLk
    r2R/Rn1uchUL8ru0B2OVkg==
    -----END DSA PRIVATE KEY-----
"""
    results = recognizer.analyze(text)
    assert len(results) == 1
    assert results[0].entity_type == "DSA_PRIVATE_KEY"

    text = """
    -----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtZW
QyNTUxOQAAACC5Kfr8pxn01Ig5YbrvjKK4kC9JUgNbqOCtMY1OdlxqdwAAAKhGc/ELRnPx
CwAAAAtzc2gtZWQyNTUxOQAAACC5Kfr8pxn01Ig5YbrvjKK4kC9JUgNbqOCtMY1Odlxqdw
AAAED0iTCOptg2MzzJ2rgov84NjppkenTE2YmwQlUQCg/vN7kp+vynGfTUiDlhuu+MoriQ
L0lSA1uo4K0xjU52XGp3AAAAH3RoaWJhdWx0QHRoaWJhdWx0LUluc3Bpcm9uLTc1NzABAg
MEBQY=
-----END OPENSSH PRIVATE KEY----

"""

    results = recognizer.analyze(text)
    assert len(results) == 1
    assert results[0].entity_type == "OPENSSH_PRIVATE_KEY"

    text = """
            {
  "type": "service_account",
  "project_id": "gsuite-group-api-only",
  "private_key": "-----BEGIN PRIVATE KEY-----LS0tLS1CRUdJTiBQUklWQVRFIEtFWS0tLS0tIEtKSUNkUUlCQURBTEJna3Foa2l
HOXcwQkFRRUVnZ0poTUlJQ1hRSUJBQUtCZ1FDN0pIb0pmZzZ5TnpMTU9XZXQgOF
o0OWE0S0QwZENzcE1BWXZvMllBTUI3L3dkRXljb2N1amJoSjJuL3NlT05pKzVYc
VRxcUZrTTVWQmw4cm1rayBGUFprLzd4MHhtZHNUUEVDU1duSEsrSGhvYU5ERlBS
M2o4alFoVm8xbGF4aXFjRWhBSGVnaTVjd3RGb3N1SkF2IFNLQUZLRXZ5RDQzc2k
wMERRblhXcllIQUVRSURBUUFCQW9HQUFQeTVTaVlIaVZFclUzS1I0QmcrcGw0eD
c1d00gRmlSQzBDZ3orZnJRUEZRRUJzQVY5UnVhc3lReHF6eHJSME93MHFuY0JlR
0JXYllFNldaaHF0Y0xBSTg5NWIraSArRjRsYkI0aUQ3VDlRZUlETVYvYUlNWEE4
MVVPNGNuczF6NHFEQUhLZXlMTHJQUXJKL0I0WDdYQytlZ1VXbTUrIGhyMXFteUF
NdXN5WElCRUNRUURKV1o4cGlsdWY0eXJZZnNKQW42aEY1VDRSalR6dGJxdk8wR1
ZHMk1jSFk3VWogTlBTZmZoekh4L2xsMGZRRVFqaStPZ3lkQ0NYOG8zSFpyZ3c1W
WZTSkFrRUE3ZStycWRVNW5PNVpHLy9QU0VRYiB0akxuUmlUekJIL2VsUWh0ZFo1
bkY3cGNwTlRpNGsxM3p1dG1LY1dXNEdLNzVhemNSR0pVaHUxa0RNN1FZQU9kIFN
RSkFWTmtZY2lma3ZuYTdHbW9vTDVWWUVzUXNxTGJNNHYwTkYyVElHTmZHM3oxTU
dwNzVLckM1TGhMOTdNTlIgd2UycC9iZDJrMEhZeUNLVUduZjJuTVBEaVFKQkFJN
zVwd2l0dFNvRTI0MEVvYlVHSURUU3o4Q0pzWEl4dURtTCB6K0tPcGRwUFJSNVRR
bWJFTUVzcGpzRnBGeW1NaXVZUGdtaWhRYk8yY0psMXFTY1k1T2tDUVFDSjZtNXR
jTjhsIFh4Zy9TTnBqRUl2K3FBeVVEOTZYVmxPSmxPSWVMSFE4a1lFMEM2WkErTX
NxWUl6Z0FyZUprODhZbjBsVS9YMC8gbXUvVXBFL0JSVGZzIC0tLS0tRU5EIFBSS
VZBVEUgS0VZLS0tLS0K-----END PRIVATE KEY-----\n",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "universe_domain": "googleapis.com"
}
"""
    results = recognizer.analyze(text)
    assert len(results) == 1
    assert results[0].entity_type == "GOOGLE_PRIVATE_KEY"
