def get_entity_detection_prompt(text):
    SYSTEM_PROMPT = """You are a smart and intelligent Named Entity Recognition (NER) system.
    I will provide you the definition of the entities you need to extract,
    the sentence from where your extract the entities and the output format with examples
    """

    USER_PROMPT_1 = "Are you clear about your role?"

    ASSISTANT_PROMPT_1 = """Sure, I'm ready to help you with your NER task.
    Please provide me with the necessary information to get started."
    """

    GUIDELINES_PROMPT = (
        "Entity Definition:\n"
        "1. PERSON: Short name or full name of a person from any geographic region (e.g., 'John Doe', 'Mr. Rajeev Mishra'). Keywords like 'Mr.', 'Ms.', 'Dr.' can often precede or follow the entity.\n"
        "2. STREET_ADDRESS: Full or partial street address (e.g., '123 Main St', 'Apt 4B, 16th Ave'). Keywords include 'lives at', 'located at', 'street', 'avenue'.\n"
        "3. COMPANY_NAME: Name of any company or organization (e.g., 'Google', 'Acme Corp'). Nearby words might include 'works at', 'CEO of', 'joined'.\n"
        "4. DATE_OF_BIRTH: Date of birth in any format (e.g., '12th March 1980', '03/12/1980'). Keywords like 'born on', 'DOB', 'age' signal the presence of this entity.\n"
        "5. EMAIL: Any valid email address (e.g., 'john.doe@example.com'). Nearby keywords include 'email', 'contact', 'reach me at'.\n"
        "6. SSN: Social Security Number or equivalent (e.g., '123-45-6789'). Keywords like 'SSN', 'social security', 'tax ID' indicate this entity.\n"
        "7. BBAN: Basic Bank Account Number, which varies by country. Keywords like 'BBAN', 'bank details', 'account number' are typically nearby.\n"
        "8. PHONE_NUMBER: Any valid phone number (e.g., '+1-555-555-5555', '(555) 555-5555'). Keywords include 'phone', 'call', 'reach at'.\n"
        "9. API_KEY: Alphanumeric string, usually 32-64 characters long (e.g., 'ABCD1234EFGH5678'). Keywords include 'API key', 'access token', 'secret key'.\n"
        "10. SWIFT_BIC_CODE: An 8-11 character alphanumeric string (e.g., 'BOFAUS3N'). Keywords like 'SWIFT code', 'BIC', 'international payment' are common.\n"
        "11. DRIVER_LICENSE_NUMBER: Alphanumeric identifier (e.g., 'D1234567'). Keywords like 'driver’s license', 'DL number', 'ID card' may indicate its presence.\n"
        "12. CREDIT_CARD_NUMBER: A 16-digit number, often grouped (e.g., '4111 1111 1111 1111'). Keywords like 'credit card', 'card number', 'payment' are often nearby.\n"
        "13. IBAN: International Bank Account Number, up to 34 alphanumeric characters (e.g., 'DE89 3704 0044 0532 0130 00'). Keywords like 'IBAN', 'bank transfer' may accompany this.\n"
        "14. PASSPORT_NUMBER: Alphanumeric identifier (e.g., 'A12345678'). Keywords like 'passport', 'ID', 'travel document' suggest its presence.\n"
        "15. BANK_ROUTING_NUMBER: A nine-digit number (e.g., '021000021'). Keywords like 'routing number', 'bank transfer', 'ACH' may be found nearby.\n"
        "16. BANK_ACCOUNT_NUMBER: Numeric or alphanumeric string (e.g., '1234567890'). Keywords include 'account number', 'bank account', 'deposit'.\n"
        "17. ITIN: Individual Taxpayer Identification Number (e.g., '900-70-0000'). Keywords like 'ITIN', 'taxpayer ID', 'IRS' may suggest its presence.\n"
        "\n"
        "Output Format:\n"
        "{{'PERSON': [list of entities present], 'STREET_ADDRESS': [list of entities present], 'COMPANY_NAME': [list of entities present], 'DATE_OF_BIRTH': [list of entities present], 'EMAIL': [list of entities present], 'SSN': [list of entities present], 'BBAN': [list of entities present], 'PHONE_NUMBER': [list of entities present], 'API_KEY': [list of entities present], 'SWIFT_BIC_CODE': [list of entities present], 'DRIVER_LICENSE_NUMBER': [list of entities present], 'CREDIT_CARD_NUMBER': [list of entities present], 'IBAN': [list of entities present], 'PASSPORT_NUMBER': [list of entities present], 'BANK_ROUTING_NUMBER': [list of entities present], 'BANK_ACCOUNT_NUMBER': [list of entities present], 'ITIN': [list of entities present]}}\n"
        "If no entities are presented in any categories, keep it ''.\n"
        "\n"
        "Examples:\n"
        "1. Sentence: Mr. Jacob lives at 456 Oak Avenue, New York.\n"
        "Output: {{'PERSON': ['Mr. Jacob'], 'STREET_ADDRESS': ['456 Oak Avenue'], 'COMPANY_NAME': [''], 'DATE_OF_BIRTH': [''], 'EMAIL': [''], 'SSN': [''], 'BBAN': [''], 'PHONE_NUMBER': [''], 'API_KEY': [''], 'SWIFT_BIC_CODE': [''], 'DRIVER_LICENSE_NUMBER': [''], 'CREDIT_CARD_NUMBER': [''], 'IBAN': [''], 'PASSPORT_NUMBER': [''], 'BANK_ROUTING_NUMBER': [''], 'BANK_ACCOUNT_NUMBER': [''], 'ITIN': ['']}}\n"
        "\n"
        "2. Sentence: John Doe works at Acme Corp. His email is john.doe@example.com, and his SSN is 123-45-6789.\n"
        "Output: {{'PERSON': ['John Doe'], 'STREET_ADDRESS': [''], 'COMPANY_NAME': ['Acme Corp'], 'DATE_OF_BIRTH': [''], 'EMAIL': ['john.doe@example.com'], 'SSN': ['123-45-6789'], 'BBAN': [''], 'PHONE_NUMBER': [''], 'API_KEY': [''], 'SWIFT_BIC_CODE': [''], 'DRIVER_LICENSE_NUMBER': [''], 'CREDIT_CARD_NUMBER': [''], 'IBAN': [''], 'PASSPORT_NUMBER': [''], 'BANK_ROUTING_NUMBER': [''], 'BANK_ACCOUNT_NUMBER': [''], 'ITIN': ['']}}\n"
        "\n"
        "3. Sentence: Sarah received her passport number P12345678 on the 5th of October, 2023.\n"
        "Output: {{'PERSON': ['Sarah'], 'STREET_ADDRESS': [''], 'COMPANY_NAME': [''], 'DATE_OF_BIRTH': [''], 'EMAIL': [''], 'SSN': [''], 'BBAN': [''], 'PHONE_NUMBER': [''], 'API_KEY': [''], 'SWIFT_BIC_CODE': [''], 'DRIVER_LICENSE_NUMBER': [''], 'CREDIT_CARD_NUMBER': [''], 'IBAN': [''], 'PASSPORT_NUMBER': ['P12345678'], 'BANK_ROUTING_NUMBER': [''], 'BANK_ACCOUNT_NUMBER': [''], 'ITIN': ['']}}\n"
        "\n"
        "4. Sentence: You can reach me at my phone number +1-555-123-4567 or send an email to contact@company.com.\n"
        "Output: {{'PERSON': [''], 'STREET_ADDRESS': [''], 'COMPANY_NAME': [''], 'DATE_OF_BIRTH': [''], 'EMAIL': ['contact@company.com'], 'SSN': [''], 'BBAN': [''], 'PHONE_NUMBER': ['+1-555-123-4567'], 'API_KEY': [''], 'SWIFT_BIC_CODE': [''], 'DRIVER_LICENSE_NUMBER': [''], 'CREDIT_CARD_NUMBER': [''], 'IBAN': [''], 'PASSPORT_NUMBER': [''], 'BANK_ROUTING_NUMBER': [''], 'BANK_ACCOUNT_NUMBER': [''], 'ITIN': ['']}}\n"
        "\n"
        "5. Sentence: My bank account number is 1234567890, and the routing number is 021000021.\n"
        "Output: {{'PERSON': [''], 'STREET_ADDRESS': [''], 'COMPANY_NAME': [''], 'DATE_OF_BIRTH': [''], 'EMAIL': [''], 'SSN': [''], 'BBAN': [''], 'PHONE_NUMBER': [''], 'API_KEY': [''], 'SWIFT_BIC_CODE': [''], 'DRIVER_LICENSE_NUMBER': [''], 'CREDIT_CARD_NUMBER': [''], 'IBAN': [''], 'PASSPORT_NUMBER': [''], 'BANK_ROUTING_NUMBER': ['021000021'], 'BANK_ACCOUNT_NUMBER': ['1234567890'], 'ITIN': ['']}}\n"
        "Sentence: {}\n"
        "Output: "
    )
    GUIDELINES_PROMPT = GUIDELINES_PROMPT.format(text)
    messages = [
        # This line is commented because Gemma does not support system prompts
        # {"role": "assistant", "content": SYSTEM_PROMPT},
        {"role": "user", "content": SYSTEM_PROMPT + " " + USER_PROMPT_1},
        {"role": "assistant", "content": ASSISTANT_PROMPT_1},
        {"role": "user", "content": GUIDELINES_PROMPT},
    ]
    return messages


def get_judge_prompt(text, results):
    SYSTEM_PROMPT = """You are an expert in Named Entity Recognition (NER) evaluation.
    Your task is to assess the correctness of identified entities by comparing them with the given text.
    """

    USER_PROMPT_1 = "Are you clear about your role?"

    ASSISTANT_PROMPT_1 = """Yes, I understand my role.
    Please provide me with the text and the identified NER results for evaluation.
    """

    GUIDELINES_PROMPT = """
    **Evaluation Criteria:**
    1. **Contextual Accuracy:** Does the identified entity exist within the text in a meaningful way?
    2. **Entity Type Appropriateness:** Is the assigned entity type correct (e.g., a person is identified as PERSON)?
    3. **Keyword Association:** Even if contextual signals are weak, does the entity match expected keywords?

    **Output Format:**
    Return a JSON response in the format:
    ```
    {
        "entity_1": "Correct" / "Incorrect",
        "entity_2": "Correct" / "Incorrect",
        ...
    }
    ```
    Do not include explanations or extra text.
    """

    EXAMPLES_PROMPT = """
    **Example 1:**
    **Text:** "Barack Obama was born in Hawaii and served as the 44th President of the United States. His driving license was not issued."
    **NER Output:**
    ```
    {
        "person": ["Barack Obama"],
        "location": ["Hawaii", "United States"],
        "title": ["44th President"],
        "driving_license": ["not issued"]
    }
    ```
    **Expected JSON Response:**
    ```
    {
        "person": "Correct",
        "location": "Correct",
        "title": "Correct",
        "driving_license": "Incorrect"
    }
    ```

    **Example 2:**
    **Text:** "Passport ID: 331410736  GitHub Token: ghr_abcdef1234567890ghijklmnopqrstuvwxYZ IBAN Number: GB27GKPH81111877912857."
    **NER Output:**

    {
        "us-passport-number": ["331410736"],
        "github-token": ["ghr_abcdef1234567890ghijklmnopqrstuvwxYZ"],
        "iban-code": ["GB27GKPH81111877912857"],
        "us-drivers-license": ["331410736"]
    }

    **Expected JSON Response:**

    {
        "us-passport-number": "Correct",
        "github-token": "Correct",
        "iban-code": "Correct",
        "us-drivers-license": "Incorrect"
    }
    """

    FINAL_EVALUATION_PROMPT = f"""
    **Text to evaluate:**
    "{text}"

    **NER Output:**
    {results}

    **Provide the JSON Response in the required format:**
    """

    messages = [
        # {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": SYSTEM_PROMPT + " " + USER_PROMPT_1},
        {"role": "assistant", "content": ASSISTANT_PROMPT_1},
        {
            "role": "user",
            "content": GUIDELINES_PROMPT
            + " "
            + EXAMPLES_PROMPT
            + " "
            + FINAL_EVALUATION_PROMPT,
        },
        # {"role": "user", "content": EXAMPLES_PROMPT},
        # {"role": "user", "content": FINAL_EVALUATION_PROMPT},
    ]

    return messages
