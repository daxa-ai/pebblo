from pebblo.entity_classifier.custom_analyzer.private_key_analyzer import (
    PrivateKeyRecognizer,
)


def test_private_key_recognizer_no_match():
    # Test case where there is no private key in the text
    text = "This is a test string with no private key."
    recognizer = PrivateKeyRecognizer()
    results = recognizer.analyze(text, entities=["PRIVATE_KEY"])

    assert len(results) == 0

    # Test case with a string that looks like a private key but fails entropy check
    text = "-----BEGIN PRIVATE KEY-----\nAAAAAAAABBBBBBBB\n-----END PRIVATE KEY-----\n"
    recognizer = PrivateKeyRecognizer()
    results = recognizer.analyze(text, entities=["PRIVATE_KEY"])

    assert len(results) == 0


def test_private_key_recognizer__matche():
    # Test case with multiple private keys in the text
    text = """

        "{\n"
        "  \"private_key\": \"-----BEGIN PRIVATE KEY-----\\nMIIEvQIBADANBgkqh\\n-----END PRIVATE KEY-----\\n\",\n"
        "  \"private_key\": \"-----BEGIN PRIVATE KEY-----\\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC0PdgHCVJv29M5\\nFaG0IX/8dyBgpB2IwIE7\\nZQia+XSYlrwDvwhqmiSG62Kdh719MzL7HBmV3SF0Oq3KzFJNmd4wzV8E4oOCwgXF\\nVJqfUE4L/gnO1oIsuP8JgvetRtaQ4ggNHtQrvWj6apnx+FNLSoBM1aO6fTb63JYg\\ngtsRYvgHYUJyjKR+9oa7vplNhJoM7ScfAMAYc+OKrOXAJNw/C1Si5bKRZ2vuNhR6\\nnKP//sMVYC5L1sGYsuHgGbP7ZHCBr+cDG2Me5kuOtc4WQYPagL3gpc9KCIHI4xnB\\nXFx8Ftv1AgMBAAECggEAVU8sL3BnF1CZcdxeM+7jL/CGaE3BvU0TZ09nCizpAbT7\\nLpOXi+E/Ix7qR11zmjrnjZ/63ULwQ6ixwhX487j8SbiWdsN1TVd10HIas+rqchbI\\nm3faWEdYrTWUynbYwagBNWIPBjXb/wisSJDZumv89MohhEedR2OsOqlFZzsvFVVL\\nGOT7s0ME64AmbD1z/1yV3LhD/E6Bo5zn/k/WD5c53ZYKph55UrGOzK9/cnrBnxM4\\nCI9YpfWBGB/XJA5kfz5MMCLeY82L2aUQ4ixcxzWgVOe83LC+6oPO/d79EhxuxV8J\\nbHMci0QV8jxrqvKS8iq0AlD+7dJ2F/+xFn52dKEXZQKBgQDXBGN8k6b1zS7ruJwC\\nuXiNRPg8iYQrPUzPrxd4A7+tjiAVQfznRHhvceSSRtsg3OPoH0jTkFKQSxDV3vXG\\ntkOnA2eczchlPj6qkH05oHEPxSZpdNaJdmMT7u6TBZWFNj4y/PCtvlz7o1uK9quX\\nt4rD308jbtH8hvFgBWVT1B3buwKBgQDWmJsVolDDn2mzMGxyiEIhb1LQEvPdCSV6\\nzWznA+v0ciQqTt2R0xVW+ZSaILcOl9w5nIwVD0vxemmu+UME0RP5RDjYoOr3A2nN\\n5dIknTd11zHbL3nwF2UxK6yYGYol1butNhqoDbqQet6M6RSuY8QvS3NU/JW8dUm3\\n5ommHU80DwKBgQCly2aDGr807Z/udw0lNKp2E+Ztl4Poa34c7l/kVM+qHdszSQyf\\nrzZGiMW83RH+hxTdWbIoIDLpvFgg8akGLmiAEaoFSM/q8VIU5xEILGTByj1SN5tt\\np3HCXwxrJXUjoK3ZVxymfBDqoA3oW0f41rgTTM+S/NLCK7NXXRHCz96uHQKBgFVM\\nf4iP5k571QX234R/CNpFZ8NxZSGc+xrfAMSq2GVn4Vw30Paf0sGpnxnMmzbfwhfc\\nVAoi9Grd35g/WBZYDPpt1bK18++PmcTP70HChEMA8L5RFsUKZ5yt4YLr0+/KDzmA\\nYgQewOOhE0krdJ8E5Pxvnz5O0C4C6PSCXIB88fidAoGALzvfTp4NWl7dEYd4m5p6\\n7ZSO4XRjKupnB99wUDVD5ayLqJsPJYblpzCvRYSHBewTzmvAk1RhLk27OaOXMZZm\\n+dcqVPsiniUtCV+ttnOUDXtkcr8IH87KYOQ0qo5E512UMknRwpkpy82zdS2OwSi8\\nEHQQ6lbUwK1H8JMDY6veRio=\\n-----END PRIVATE KEY-----\\n\",\n\n"
        "}\n\n"

    """
    recognizer = PrivateKeyRecognizer()
    results = recognizer.analyze(text, entities=["PRIVATE_KEY"])

    assert len(results) == 1
