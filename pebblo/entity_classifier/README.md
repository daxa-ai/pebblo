# Entity Classifier

This is Presidio based Entity Classifier

Currently, we are supporting following Entities:
1. US SSN
2. US Passport number
3. US Drivers License
4. Credit card number
5. US Bank Account Number
6. IBAN code
7. US ITIN

And following Secret Entities:
1. Github Token
2. Slack Token
3. AWS Access Key
4. AWS Secret Key

## How to use
Entity Classifier
```
from pebblo.entity_classifier.entity_classifier import EntityClassifier

text = <Input Data>
entity_classifier_obj = EntityClassifier()
entities, total_count, anonymized_text, entity_details = entity_classifier_obj.presidio_entity_classifier_and_anonymizer(text,anonymize_snippets)
print(f"Entity Group: {entity_groups}")
print(f"Entity Count: {total_entity_count}")
print(f"Anonymized Text: {anonymized_text}")
```
