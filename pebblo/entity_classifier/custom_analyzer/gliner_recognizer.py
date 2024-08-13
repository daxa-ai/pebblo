import logging

from gliner import GLiNER
from presidio_analyzer import EntityRecognizer, RecognizerResult

logger = logging.getLogger()


class GlinerRecognizer(EntityRecognizer):
    """
    Custom recognizer that uses the GLiNER model for entity detection.
    """

    def __init__(self):
        ENTITIES = ["SECRET_KEY_TOKEN"]
        super().__init__(supported_entities=ENTITIES, supported_language="en")
        self.model = GLiNER.from_pretrained("urchade/gliner_mediumv2.1")
        # Initialize the GLiNER model

    def load(self):
        # GLiNER model might require loading resources. Initialize any here.
        pass

    def analyze(self, text, entities, nlp_artifacts=None):
        # Use GLiNER model to detect entities
        results = []

        # Get predictions from GLiNER
        predictions = self.model.predict_entities(text, self.supported_entities)
        for entity in predictions:
            entity_type = entity["label"]  # Get entity type from GLiNER
            start = entity["start"]  # Start position of the entity in the text
            end = entity["end"]  # End position of the entity in the text
            score = entity["score"]  # Confidence score from GLiNER

            # Append the detected entity result
            results.append(
                RecognizerResult(
                    entity_type=entity_type, start=start, end=end, score=score
                )
            )

        return results

    def validate_result(self, pattern_name, text, start, end):
        # Implement any additional validation if required
        return True
