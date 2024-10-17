"""
Module to store Configuration parameters for the Pebblo topic classifier,
including model paths, confidence score, and minimum text length.
"""

# Confidence score
TOPIC_CONFIDENCE_SCORE = 0.60

# Minimum length of input text in characters
TOPIC_MIN_TEXT_LENGTH = 16

# Topics to exclude from the classification results
TOPICS_TO_EXCLUDE = ["NORMAL_TEXT"]

# Model paths
TOKENIZER_PATH = "daxa-ai/pebblo-classifier-v2"
CLASSIFIER_PATH = "daxa-ai/pebblo-classifier-v2"

# Specific model version to use. Revision can be any identifier allowed by
# git e.g. branch name, a tag name, or a commit id
#MODEL_REVISION = "5fbbe83dee7ef72c61a8173c4ccf27b19788fc2e"  # Pebblo classifier V8
MODEL_REVISION = "a9a3816784cd6f5feb5a515e9536de78d64d6d49"