mock_input_text1_all_entity_false = """
Sachin's SSN is &lt;US_SSN&gt;.
ITIN number &lt;US_ITIN&gt;
His AWS Access Key is: &lt;AWS_ACCESS_KEY&gt;.
And Github Token is: &lt;GITHUB_TOKEN&gt;
"""

mock_input_text1_all_entity_true = """
&lt;PERSON&gt;'s SSN is &lt;US_SSN&gt;.
ITIN number &lt;US_ITIN&gt;
His AWS Access Key is: &lt;AWS_ACCESS_KEY&gt;.
And &lt;PERSON&gt; is: &lt;GITHUB_TOKEN&gt;
"""

mock_input_text2_all_entity_false = """
Content
"Wipros board on Friday, January 12 announced an interim dividend of Re 1 per equity share of the face value of Rs 2 each, i.e., a 50 per cent payout for the current financial year along with financial results for the October-December period of the company for the financial year ending March 2024."
"Roberts reminded the board of the scheduled retreat coming up in three months, and provided a drafted retreat schedule. The board provided feedback on the agenda and the consensus was that, outside of making a few minor changes, the committee should move forward as planned. No board action required."
"Claims: An adaptive pacing system for implantable cardiac devices, comprising a pulse generator, multiple sensing electrodes, a microprocessor-based control unit, a wireless communication module, and memory for dynamically adjusting pacing parameters based on real-time physiological data.  The system of claim 1, wherein the adaptive pacing algorithms include rate-responsive pacing based on physical activity.  The system of claim 1, further comprising an external monitoring system for remote data access and modification of pacing parameters."
"Sachin's SSN is &lt;US_SSN&gt;. His passport ID is 5484880UA.  
Sachin's driver's license number is S9998888.  
Sachin's bank account number is 70048841700216300.  
His American express credit card number is &lt;CREDIT_CARD&gt;.  
His UK IBAN Code is &lt;IBAN_CODE&gt;.  
ITIN number &lt;US_ITIN&gt;. 
Azure client secret : c4cb6f91-15a7-4e6d-a824-abcdef012345.  
AWS Access Key is: &lt;AWS_ACCESS_KEY&gt; 
AWS Secret Key is : &lt;AWS_SECRET_KEY&gt;
Github Token is: &lt;GITHUB_TOKEN&gt; 
Google API key: zaCELgL0imfnc8mVLWwsAawjYr4Rx-Af50DDqtlx 
Slack Token is: &lt;SLACK_TOKEN&gt; 
Azure Client Secret - c4cb6f91-15a7-4e6d-a824-abcdef012345 
Slack Token - &lt;SLACK_TOKEN&gt; 
Google API key- KLzaSyB_tWrbmfWx8g2bzL7Vhq7znuTUn0JPKmY"
"""

mock_input_text2_all_entity_true = """
"&lt;PERSON&gt; board on &lt;DATE_TIME&gt; announced an interim dividend of Re 1 per equity share of the face value of Rs 2 each, i.e., a 50 per cent payout for &lt;DATE_TIME&gt; along with financial results for the &lt;DATE_TIME&gt; period of the company for &lt;DATE_TIME&gt;."
"&lt;PERSON&gt; reminded the board of the scheduled retreat coming up in &lt;DATE_TIME&gt;, and provided a drafted retreat schedule. The board provided feedback on the agenda and the consensus was that, outside of making a few minor changes, the committee should move forward as planned. No board action required."
"Claims: An adaptive pacing system for implantable cardiac devices, comprising a pulse generator, multiple sensing electrodes, a microprocessor-based control unit, a wireless communication module, and memory for dynamically adjusting pacing parameters based on real-time physiological data.  The system of claim 1, wherein the adaptive pacing algorithms include rate-responsive pacing based on physical activity.  The system of claim 1, further comprising an external monitoring system for remote data access and modification of pacing parameters."
"&lt;PERSON&gt;'s SSN is &lt;US_SSN&gt;. His passport ID is 5484880UA.  
&lt;PERSON&gt;'s driver's license number is &lt;NRP&gt;.  
&lt;PERSON&gt;'s bank account number is 70048841700216300.  
His &lt;NRP&gt; express credit card number is &lt;CREDIT_CARD&gt;.  
His UK IBAN Code is &lt;IBAN_CODE&gt;.  
ITIN number &lt;US_ITIN&gt;. 
Azure client secret : c4cb6f91-15a7-4e6d-a824-abcdef012345.  
AWS Access Key is: &lt;AWS_ACCESS_KEY&gt; 
AWS Secret Key is : &lt;AWS_SECRET_KEY&gt;
Github Token is: &lt;GITHUB_TOKEN&gt; 
Google API key: &lt;PERSON&gt;&lt;PERSON&gt; is: &lt;SLACK_TOKEN&gt; 
Azure Client Secret - c4cb6f91-15a7-4e6d-a824-abcdef012345 
&lt;PERSON&gt; - &lt;SLACK_TOKEN&gt; 
Google API key- KLzaSyB_tWrbmfWx8g2bzL7Vhq7znuTUn0JPKmY"
"""

mock_negative_data_all_entity_true = """
&lt;PERSON&gt;'s SSN is 222-85.
His AWS Access Key is: AKIPT4PDORIRTV6PH.
And &lt;PERSON&gt; is: ghpu657yiujgwfrtigu3ver238765tyuhygvtrder6t7gyvhbuy5e676578976tyghy76578uygfyfgcyturtdf
"""

mock_negative_data_all_entity_false = """
Sachin's SSN is 222-85.
His AWS Access Key is: AKIPT4PDORIRTV6PH.
And Github Token is: ghpu657yiujgwfrtigu3ver238765tyuhygvtrder6t7gyvhbuy5e676578976tyghy76578uygfyfgcyturtdf
"""
