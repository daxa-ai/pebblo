# Topic Classifier

The Pebblo Topic Classifier now offers a streamlined set of document categories: Harmful, Financial, Corporate Documents, and Medical. This update aims to simplify classification, improve precision, and enhance performance by focusing on these key areas.

## Current Supported Topics
The classifier now supports the following four topics:

1. Harmful
1. Financial
1. Corporate Documents
1. Medical

## How to use

```
from pebblo.topic_classifier.topic_classifier import TopicClassifier

text =  "Your sample text here."
topic_classifier_obj = TopicClassifier()
topics, total_topic_count, topic_details = topic_classifier_obj.predict(text)
print(f"Topic Response: {topics}")
print(f"Topic Count: {total_topic_count}")
print(f"Topic Details: {topic_details}")
```


## Accessing the Previous Classifier
The older classifier version supports the following detailed topics:
1. Medical Advice
1. Harmful Advice
1. Board Meeting
1. Consulting Agreement
1. Customer List
1. Enterprise Agreement
1. Executive Severance Agreement
1. Financial Report
1. Loan And Security Agreement
1. Merger Agreement
1. Patent Application Fillings
1. Price List
1. Employee Agreement
1. Sexual Content
1. Sexual Incident Report
1. Internal Product Roadmap Agreement
    
### How to Switch to the Previous Classifier Version
To use this broader class set, make the following modifications in topic_classifier/config.py

```
# Model paths
TOKENIZER_PATH = "daxa-ai/pebblo-classifier"
CLASSIFIER_PATH = "daxa-ai/pebblo-classifier"

# Specify the model version to revert to the previous classifier
MODEL_REVISION = "5fbbe83dee7ef72c61a8173c4ccf27b19788fc2e"
```
