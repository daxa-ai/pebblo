# Topic Classifier

This is Topic Classifier. 
Currently, we are supporting following Topics:
1. Normal Advice
2. Medical Advice
3. Harmful Advice
4. Board Meeting
5. Consulting Agreement
6. Customer List
7. Enterprise License Agreement
8. Executive Severance Agreement
9. Financial Report
10. Internal Use Only
11. Loan And Security Agreement
12. Merger Agreement
13. Patent Application Fillings
14. Price List
15. Employee Agreement
16. Enterprise Agreement
17. Sexual Content
18. Sexual Incident Report
    
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
