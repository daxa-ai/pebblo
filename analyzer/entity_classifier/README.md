# Entity Classifier

This is Presidio based Entity Classifier
Currently we are supporting following Entities:
1. US SSN
2. US Passport number
3. US Drivers License
4. Credit card number
5. US Bank Account Number
6. IBAN code
7. US ITIN
    
## How to use

```
from rag.analyzer.entity_classifier.entity_classifier import EntityClassifier

text = <Input Data>
entity_classifier_obj = EntityClassifier(text)
restricted_entity_groups, total_entity_count = entity_classifier_obj.presidio_entity_classifier()
print(f"Entity Group: {restricted_entity_groups}")
print(f"Entity Count: {total_entity_count}")
```
