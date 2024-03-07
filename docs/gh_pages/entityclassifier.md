# Pebblo Entity Classifier  
  
`Pebblo entity classifier` is designed to automatically scan your loader source files and pinpoint sensitive entities within the files.  By highlighting these entities, it assists in ensuring compliance, data security, and privacy protection within your data processing pipeline.  
Integrating it enhances risk mitigation and regulatory adherence while streamlining sensitive data handling.  
  
Pebblo Entity Classifier harnesses the power of the `Presidio Analyzer` python library for accurate entity classification.  
Leveraging Presidio's robust features and capabilities, we ensure precise identification of entities within textual data.  
Additionally, our solution welcomes contributions from the open-source community, encouraging collaborative efforts to improve its functionality and reliability.  
  
# Entities Supported By Pebblo Entity Classifier  
  
Below is the list of `entities` supported by Pebblo -  
  
  1. US Social Security Number  
  2. US Passport Number  
  3. US Driver's License  
  4. US Credit Card Number  
  5. US Bank Account Number  
  6. IBAN Code  
  7. US ITIN  
  8. Github Access Token  
  9. Slack Access Token  
10. AWS Access Key  
11. AWS Secret Key   
  
  
User can get details of classified entities for their loader source files in Pebblo report.  
Different sections of Pebblo report such as , `Top Files with Most Findings`, `Data Source Findings Table` and `Snippets`  helps to get overview of pebblo entity classifier output for user's Rag application.  
  
For more details refer - [Reports](reports.md)