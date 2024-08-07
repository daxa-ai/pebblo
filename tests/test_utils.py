from pebblo.utils import get_confidence_score_label


def test_get_confidence_score_label():
    assert get_confidence_score_label(1.0) == "HIGH"
    assert get_confidence_score_label(0.4) == "MEDIUM"
    assert get_confidence_score_label(0.2) == "LOW"
