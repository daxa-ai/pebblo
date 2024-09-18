# Pebblo Entity Classifier

`Pebblo entity classifier` is designed to automatically scan your loader source files and pinpoint sensitive entities within the files. By highlighting these entities, it assists in ensuring compliance, data security, and privacy protection within your data processing pipeline.  
Integrating it enhances risk mitigation and regulatory adherence while streamlining sensitive data handling.

Pebblo Entity Classifier harnesses the power of the `Presidio Analyzer` python library for accurate entity classification.  
Leveraging Presidio's robust features and capabilities, we ensure precise identification of entities within textual data.  
Additionally, our solution welcomes contributions from the open-source community, encouraging collaborative efforts to improve its functionality and reliability.

# Entities Supported By Pebblo Entity Classifier

Below is the list of `entities` supported by Pebblo -

1. US Social Security Number
1. US Passport Number
1. US Driver's License
1. US Credit Card Number
1. US Bank Account Number
1. IBAN Code
1. US ITIN
1. IP Address
1. GitHub Access Token
1. Slack Access Token
1. AWS Access Key
1. AWS Secret Key
1. Private Key
1. DSA Private Key
1. Encrypted Private Key
1. Elliptic Curve Private Key
1. OpenSSH Private Key
1. RSA Private Key
1. Google Account Private Key
1. Github Fine Grained Token
1. Azure Client Secret Key


User can get details of classified entities for their loader source files in Pebblo report.  
Different sections of Pebblo report such as , `Top Files with Most Findings`, `Data Source Findings Table` and `Snippets` helps to get overview of pebblo entity classifier output for user's Rag application.

For more details refer - [Reports](reports.md)

<img referrerpolicy="no-referrer-when-downgrade" src="https://static.scarf.sh/a.png?x-pxid=64a603c5-db24-48b3-bbaa-0e5ca775e1cf" />
