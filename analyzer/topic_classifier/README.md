# Topic Classifier

This is Topic Classifier. 
Currently, we are supporting following Topics:
1. Medical Advice
2. Harmful Advice
    
## How to use

```
from analyzer.topic_classifier.topic_classifier import TopicClassifier

text =  "I'm Wolfgang, residing in Berlin."
topic_classifier_obj = TopicClassifier(text)
restricted_topics, total_topic_count = topic_classifier_obj.topic_classifier()
print(f"Topic Response: {restricted_topics}")
print(f"Topic Count: {total_topic_count}")
```
