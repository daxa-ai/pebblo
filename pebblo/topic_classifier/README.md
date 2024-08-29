# Topic Classifier

This is Topic Classifier. 
Currently, we are supporting following Topics:
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
