"""
Copyright (c) 2024 Cloud Defense, Inc. All rights reserved.
"""

from enum import Enum


class ConfidenceScoreLabel(Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


def get_confidence_score_label(confidence_score):
    if float(confidence_score) >= 0.8:
        return ConfidenceScoreLabel.HIGH.value
    elif 0.4 <= float(confidence_score) < 0.8:
        return ConfidenceScoreLabel.MEDIUM.value
    else:
        return ConfidenceScoreLabel.LOW.value
