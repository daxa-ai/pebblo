from enum import Enum


class Topics(Enum):
    """
    Enumeration of all possible topics
    """
    MEDICAL_ADVICE = "Medical Advice"
    HARMFUL_ADVICE = "Harmful Advice"


class ConfidenceScore(Enum):
    Topic = "0.60"
