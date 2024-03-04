mock_input_text1_all_entity_false = """
    Sachin's SSN is <US_SSN>.
    ITIN number <US_ITIN>
    His AWS Access Key is: <AWS_ACCESS_KEY>.
    And Github Token is: <GITHUB_TOKEN>
"""

mock_input_text1_all_entity_true = """
    Sachin's SSN is <US_SSN>.
    ITIN number <US_ITIN>
    His AWS Access Key is: <AWS_ACCESS_KEY>.
    And Github Token is: <GITHUB_TOKEN>
"""

mock_input_text2_all_entity_false = """
    Content
    "Wipros board on Friday, January 12 announced an interim dividend of Re 1 per equity share of the face value of Rs 2 each, i.e., a 50 per cent payout for the current financial year along with financial results for the October-December period of the company for the financial year ending March 2024."
    "Roberts reminded the board of the scheduled retreat coming up in three months, and provided a drafted retreat schedule. The board provided feedback on the agenda and the consensus was that, outside of making a few minor changes, the committee should move forward as planned. No board action required."
    "Claims: An adaptive pacing system for implantable cardiac devices, comprising a pulse generator, multiple sensing electrodes, a microprocessor-based control unit, a wireless communication module, and memory for dynamically adjusting pacing parameters based on real-time physiological data.  The system of claim 1, wherein the adaptive pacing algorithms include rate-responsive pacing based on physical activity.  The system of claim 1, further comprising an external monitoring system for remote data access and modification of pacing parameters."
    "Sachin's SSN is <US_SSN>. His passport ID is 5484880UA.  
    Sachin's driver's license number is S9998888.  
    Sachin's bank account number is 70048841700216300.  
    His American express credit card number is <CREDIT_CARD>.  
    His UK IBAN Code is <IBAN_CODE>.  
    ITIN number <US_ITIN>. 
    Azure client secret : c4cb6f91-15a7-4e6d-a824-abcdef012345.  
    AWS Access Key is: <AWS_ACCESS_KEY> 
    AWS Secret Key is : <AWS_SECRET_KEY>
    Github Token is: <GITHUB_TOKEN> 
    Google API key: zaCELgL0imfnc8mVLWwsAawjYr4Rx-Af50DDqtlx 
    Slack Token is: <SLACK_TOKEN> 
    Azure Client Secret - c4cb6f91-15a7-4e6d-a824-abcdef012345 
    Slack Token - <SLACK_TOKEN> 
    Google API key- KLzaSyB_tWrbmfWx8g2bzL7Vhq7znuTUn0JPKmY"
"""

mock_input_text2_all_entity_true = """
    Content
    "<PERSON> board on <DATE_TIME> announced an interim dividend of Re 1 per equity share of the face value of Rs 2 each, i.e., a 50 per cent payout for <DATE_TIME> along with financial results for the <DATE_TIME> period of the company for <DATE_TIME>."
    "<PERSON> reminded the board of the scheduled retreat coming up in <DATE_TIME>, and provided a drafted retreat schedule. The board provided feedback on the agenda and the consensus was that, outside of making a few minor changes, the committee should move forward as planned. No board action required."
    "Claims: An adaptive pacing system for implantable cardiac devices, comprising a pulse generator, multiple sensing electrodes, a microprocessor-based control unit, a wireless communication module, and memory for dynamically adjusting pacing parameters based on real-time physiological data.  The system of claim 1, wherein the adaptive pacing algorithms include rate-responsive pacing based on physical activity.  The system of claim 1, further comprising an external monitoring system for remote data access and modification of pacing parameters."
    "<PERSON>'s SSN is <US_SSN>. His passport ID is 5484880UA.  
    <PERSON>'s driver's license number is <NRP>.  
    <PERSON>'s bank account number is 70048841700216300.  
    His <NRP> express credit card number is <CREDIT_CARD>.  
    His UK IBAN Code is <IBAN_CODE>.  
    ITIN number <US_ITIN>. 
    Azure client secret : c4cb6f91-15a7-4e6d-a824-abcdef012345.  
    AWS Access Key is: <AWS_ACCESS_KEY> 
    AWS Secret Key is : <AWS_SECRET_KEY>
    Github Token is: <GITHUB_TOKEN> 
    Google API key: <PERSON><PERSON> is: <SLACK_TOKEN> 
    Azure Client Secret - c4cb6f91-15a7-4e6d-a824-abcdef012345 
    <PERSON> - <SLACK_TOKEN> 
    Google API key- KLzaSyB_tWrbmfWx8g2bzL7Vhq7znuTUn0JPKmY"
"""

mock_negative_data_all_entity_true = """
    <PERSON>'s SSN is 222-85.
    His AWS Access Key is: AKIPT4PDORIRTV6PH.
    And <PERSON> is: ghpu657yiujgwfrtigu3ver238765tyuhygvtrder6t7gyvhbuy5e676578976tyghy76578uygfyfgcyturtdf
"""

mock_negative_data_all_entity_false = """
    Sachin's SSN is 222-85.
    His AWS Access Key is: AKIPT4PDORIRTV6PH.
    And Github Token is: ghpu657yiujgwfrtigu3ver238765tyuhygvtrder6t7gyvhbuy5e676578976tyghy76578uygfyfgcyturtdf
"""
