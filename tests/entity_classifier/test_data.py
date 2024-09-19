input_text1 = """
Sachin's SSN is 222-85-4836.
ITIN number 993-77 0690
His AWS Access Key is: AKIAQIPT4PDORIRTV6PH.
And Github Token is: ghp_hgu657yiujgwfrtigu3ver238765tyuhygvtrder6t7gyvhbuy5e676578976tyghy76578uygfyfgcyturtdf
"""

input_text2 = """
Content
"Wipros board on Friday, January 12 announced an interim dividend of Re 1 per equity share of the face value of Rs 2 each, i.e., a 50 per cent payout for the current financial year along with financial results for the October-December period of the company for the financial year ending March 2024."
"Roberts reminded the board of the scheduled retreat coming up in three months, and provided a drafted retreat schedule. The board provided feedback on the agenda and the consensus was that, outside of making a few minor changes, the committee should move forward as planned. No board action required."
"Claims: An adaptive pacing system for implantable cardiac devices, comprising a pulse generator, multiple sensing electrodes, a microprocessor-based control unit, a wireless communication module, and memory for dynamically adjusting pacing parameters based on real-time physiological data.  The system of claim 1, wherein the adaptive pacing algorithms include rate-responsive pacing based on physical activity.  The system of claim 1, further comprising an external monitoring system for remote data access and modification of pacing parameters."
"Sachin's SSN is 222-85-4836. His passport ID is 5484880UA.
Sachin's driver's license number is S9998888.
Sachin's bank account number is 70048841700216300.
His American express credit card number is 371449635398431.
His UK IBAN Code is AZ96AZEJ00000000001234567890.
ITIN number 993-77 0690.
AWS Access Key is: AKIAQIPT4PDORIRTV6PH
AWS Secret Key is : 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
Github Token is: ghp_hgu657yiujgwfrtigu3ver238765tyuhygvtrder6t7gyvhbuy5e676578976tyghy76578uygfyfgcyturtdf
Google API key: zaCELgL0imfnc8mVLWwsAawjYr4Rx-Af50DDqtlx
Slack Token is: xoxp-7676545380258-uygh
Slack Token - xoxb-3204014939555-4519358291237-TTIf0243T8YFSAGEVr1wBrWE
Google API key- KLzaSyB_tWrbmfWx8g2bzL7Vhq7znuTUn0JPKmY"
My IP Address - 10.55.60.61
Azure client_secret is de1d4a2d-d9fa-44f1-84bb-4f73c004afda
"""

negative_data = """
Sachin's SSN is 222-85.
His AWS Access Key is: AKIPT4PDORIRTV6PH.
And Github Token is: ghpu657yiujgwfrtigu3ver238765tyuhygvtrder6t7gyvhbuy5e676578976tyghy76578uygfyfgcyturtdf
"""

tf_test_data = """
variable "client_secret" {
}

# We strongly recommend using the required_providers block to set the
# Azure Provider source and version being used
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.x"
    }
  }
}

# Configure the Microsoft Azure Provider
provider "azurerm" {
  features {}

  client_id       = "00000000-0000-0000-0000-000000000000"
  client_secret   = "1131a1fc-8cee-4f3c-9b2f-6808f66f72a4"
  tenant_id       = "10000000-0000-0000-0000-000000000000"
  subscription_id = "20000000-0000-0000-0000-000000000000"
}
"""
