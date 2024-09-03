import re
from typing import List, Optional

from presidio_analyzer import (
    EntityRecognizer,
    Pattern,
    PatternRecognizer,
    RecognizerResult,
)
from presidio_analyzer.nlp_engine import NlpArtifacts

from pebblo.entity_classifier.custom_analyzer.calculate_entropy import (
    is_high_entropy_secret,
)
from pebblo.log import get_logger

logger = get_logger(__name__)


class PrivateKeyRecognizer(PatternRecognizer):
    """Recognize Private key using regex.

    :param patterns: List of patterns to be used by this recognizer
    :param context: List of context words to increase confidence in detection
    :param supported_language: Language this recognizer supports
    :param supported_entity: The entity this recognizer can detect
    """

    PATTERNS = [
        Pattern(
            "PRIVATE_KEY",
            r"(?<=BEGIN PRIVATE KEY-----)[\s\S]{10,}?(?=-----END PRIVATE KEY)",
            0.5,
        ),
        Pattern(
            "DSA_PRIVATE_KEY",
            r"(?<=BEGIN DSA PRIVATE KEY-----)[\s\S]{10,}?(?=-----END DSA PRIVATE KEY)",
            0.5,
        ),
        Pattern(
            "ELLIPTIC_CURVE_PRIVATE_KEY",
            r"(?<=BEGIN EC PRIVATE KEY-----)[\s\S]{10,}?(?=-----END EC PRIVATE KEY)",
            0.5,
        ),
        Pattern(
            "ENCRYPTED_PRIVATE_KEY",
            r"(?<=BEGIN ENCRYPTED PRIVATE KEY-----)[\s\S]{10,}?(?=-----END ENCRYPTED PRIVATE KEY)",
            0.5,
        ),
        Pattern(
            "OPENSSH_PRIVATE_KEY",
            r"(?<=BEGIN OPENSSH PRIVATE KEY-----)[\s\S]{10,}?(?=-----END OPENSSH PRIVATE KEY)",
            0.5,
        ),
        Pattern(
            "RSA_PRIVATE_KEY",
            r"(?<=BEGIN RSA PRIVATE KEY-----)(.)[\s\S]{10,}?(?=-----END RSA PRIVATE KEY)",
            0.5,
        ),
    ]

    CONTEXT = []

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        context: Optional[List[str]] = None,
        supported_language: str = "en",
        supported_entity: str = "PRIVATE_KEY",
    ):
        patterns = patterns if patterns else self.PATTERNS
        context = context if context else self.CONTEXT
        super().__init__(
            supported_entity=supported_entity,
            patterns=patterns,
            context=context,
            supported_language=supported_language,
        )
        self.google_keywords = [
            "gsuite-group-api-only",
            "https://accounts.google.com/o/oauth2/auth",
            "googleapis.com",
            "https://oauth2.googleapis.com/token",
            "gsuite-group-api-only.iam.gserviceaccount.com",
        ]

    def analyze(
        self,
        text: str,
        entities: List[str] = [],
        nlp_artifacts: Optional[NlpArtifacts] = None,
        regex_flags: Optional[int] = None,
    ) -> List[RecognizerResult]:
        """
        Analyzes text to detect PII using regular expressions or deny-lists.

        :param text: Text to be analyzed
        :param entities: Entities this recognizer can detect
        :param nlp_artifacts: Output values from the NLP engine
        :param regex_flags: regex flags to be used in regex matching
        :return:
        """
        results = []

        if self.patterns:
            pattern_result = self.__analyze_patterns(
                text, [re.MULTILINE | re.IGNORECASE]
            )
            results.extend(pattern_result)

        return results

    def __analyze_patterns(
        self, text: str, flags: int = None
    ) -> List[RecognizerResult]:
        """
        Evaluate all patterns in the provided text.

        Including words in the provided deny-list

        :param text: text to analyze
        :param flags: regex flags
        :return: A list of RecognizerResult
        """
        flags = flags if flags else self.global_regex_flags
        results = []
        for pattern in self.patterns:
            matches = re.finditer(pattern.regex, text, re.MULTILINE | re.IGNORECASE)
            # matches = re.finditer(pattern.regex, text, re.DOTALL)

            for matchNum, match in enumerate(matches, start=1):
                start, end = match.span()
                current_match = text[start:end]
                range_text = text[start - 200 : end + 200]
                # Check if any of the keywords exist within the range
                keyword_found = any(
                    keyword in range_text for keyword in self.google_keywords
                )

                # Determine the entity type based on keyword presence
                if keyword_found:
                    pattern.name = "GOOGLE_PRIVATE_KEY"

                # Skip empty results
                if current_match == "":
                    continue

                score = pattern.score

                validation_result = self.validate_result(current_match)
                description = self.build_regex_explanation(
                    self.name,
                    pattern.name,
                    pattern.regex,
                    score,
                    validation_result,
                    flags,
                )
                pattern_result = RecognizerResult(
                    entity_type=pattern.name,
                    start=start,
                    end=end,
                    score=score,
                    analysis_explanation=description,
                    recognition_metadata={
                        RecognizerResult.RECOGNIZER_NAME_KEY: self.name,
                        RecognizerResult.RECOGNIZER_IDENTIFIER_KEY: self.id,
                    },
                )

                if validation_result is not None:
                    if validation_result:
                        pattern_result.score = EntityRecognizer.MAX_SCORE
                    else:
                        pattern_result.score = EntityRecognizer.MIN_SCORE

                invalidation_result = self.invalidate_result(current_match)
                if invalidation_result is not None and invalidation_result:
                    pattern_result.score = EntityRecognizer.MIN_SCORE

                if pattern_result.score > EntityRecognizer.MIN_SCORE:
                    results.append(pattern_result)

                # Update analysis explanation score following validation or invalidation
                description.score = pattern_result.score

        results = EntityRecognizer.remove_duplicates(results)
        return results

    def invalidate_result(self, pattern_text: str) -> bool:
        """
        Check if the pattern text cannot be validated as a Private_Key entity.

        :param pattern_text: Text detected as pattern by regex
        :return: True if invalidated
        """
        if is_high_entropy_secret(pattern_text) and len(pattern_text) > 100:
            return False
        return True
