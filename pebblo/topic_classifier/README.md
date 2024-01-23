# Topic Classifier

This is Topic Classifier. 
Currently, we are supporting following Topics:
1. Normal Advice
2. Medical Advice
3. Harmful Advice
4. Board Meeting
5. Consulting Agreement
6. Customer List
7. Distribution/Partner Agreement
8. Enterprise License Agreement
9. Executive Severance Agreement
10. Financial Report
11. Internal Use Only
12. Loan And Security Agreement
13. Merger Agreement
14. NDA
15. Patent Application Fillings
16. Price List
17. Secret Sauce
18. Security Breach
19. Settlement Agreement
20. Sexual Harassment
21. Employee Agreement
22. Enterprise Agreement
    
## How to use

```
from pebblo.topic_classifier.topic_classifier import TopicClassifier

text =  "Your sample text here."
topic_classifier_obj = TopicClassifier()
topics, total_topic_count = topic_classifier_obj.predict(text)
print(f"Topic Response: {topics}")
print(f"Topic Count: {total_topic_count}")
```
