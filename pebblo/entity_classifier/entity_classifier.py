from presidio_analyzer import AnalyzerEngine
from presidio_analyzer.context_aware_enhancers import LemmaContextAwareEnhancer
from presidio_anonymizer import AnonymizerEngine

from pebblo.entity_classifier.custom_analyzer.cerdit_card_analyzer import (
    ExtendedCreditCardRecognizer,
)
from pebblo.entity_classifier.custom_analyzer.llm_analyzer import LLMRecognizer
from pebblo.entity_classifier.custom_analyzer.private_key_analyzer import (
    PrivateKeyRecognizer,
)
from pebblo.entity_classifier.utils.config import (
    ConfidenceScore,
    Entities,
    SecretEntities,
    entity_group_conf_mapping,
)
from pebblo.entity_classifier.utils.judge_entity import judge_results
from pebblo.entity_classifier.utils.result_validation import (
    is_not_part_of_decimal,
    validate_extracted_data,
)
from pebblo.entity_classifier.utils.utils import (
    add_custom_regex_analyzer_registry,
    get_entities,
)
from pebblo.log import get_logger
from pebblo.text_generation.text_generation import TextGeneration

logger = get_logger(__name__)


class EntityClassifier:
    def __init__(self):
        self.analyzer = AnalyzerEngine()
        self.anonymizer = AnonymizerEngine()
        self.entities = list(Entities.__members__.keys())
        self.entities.extend(list(SecretEntities.__members__.keys()))
        self.text_gen_obj = TextGeneration()
        self.custom_analyze()

    def custom_analyze(self):
        # Adding custom analyzer
        custom_registry = add_custom_regex_analyzer_registry()
        custom_registry.load_predefined_recognizers()
        self.analyzer = AnalyzerEngine(
            registry=custom_registry,
            context_aware_enhancer=LemmaContextAwareEnhancer(
                context_similarity_factor=float(
                    ConfidenceScore.EntityContextSimilarityFactor.value
                ),
                min_score_with_context_similarity=float(
                    ConfidenceScore.EntityMinScoreWithContext.value
                ),
            ),
        )
        pk_recognizer = PrivateKeyRecognizer()
        # Add the private key recognizer to the Presidio Analyzer
        self.analyzer.registry.add_recognizer(pk_recognizer)

        cc_recognizer = ExtendedCreditCardRecognizer()
        # Add the credit card recognizer to the Presidio Analyzer
        self.analyzer.registry.add_recognizer(cc_recognizer)

        llm_recognizer = LLMRecognizer()
        self.analyzer.registry.add_recognizer(llm_recognizer)

    # Function to check if two entities overlap based on their start and end positions
    def entities_overlap(self, entity1, entity2):
        return not (
            entity1.end <= entity2.start
            or entity2.end <= entity1.start
            and entity1.entity_type != entity2.entity_type
        )

    def analyze_response(
        self, input_text: str, anonymize_all_entities: bool = True
    ) -> tuple:
        """
        Analyze the given input text to detect and classify entities based on predefined criteria.

        Args:
            input_text (str): The text to be analyzed for detecting entities.
            anonymize_all_entities (bool): Flag to determine if all detected entities should be anonymized.
                                        (Currently not used in the function logic.)

        Returns:
            tuple: A tuple containing two lists:
                1. A list of detected non-overlapping entities.
                2. A list of tuples where each tuple contains a group of overlapping entities.
        """
        # Analyze the text to detect entities using the Presidio analyzer
        analyzer_results = self.analyzer.analyze(
            text=input_text, entities=self.entities, language="en"
        )
        # Initialize the list to hold the final classified entities
        non_overlapping_results = []
        overlapping_results = []

        # Temporary list to hold overlapping entities
        current_overlap_group = []

        # Sort entities by their start position to efficiently group overlaps
        sorted_analyzer_results = sorted(analyzer_results, key=lambda x: x.start)
        # Iterate through the sorted results to separate overlapping and non-overlapping entities
        for entity in sorted_analyzer_results:
            try:
                if is_not_part_of_decimal(
                    entity.entity_type, input_text, entity.start, entity.end
                ):
                    mapped_entity = None
                    # Map entity type to predefined entities if it exists in the Entities enumeration
                    if entity.entity_type in Entities.__members__:
                        mapped_entity = Entities[entity.entity_type].value
                    # Check if the entity type exists in SecretEntities enumeration
                    elif entity.entity_type in SecretEntities.__members__:
                        mapped_entity = SecretEntities[entity.entity_type].value

                    # Ensure the entity meets the confidence threshold and is in the desired entity list
                    if (
                        mapped_entity
                        and entity.score
                        >= float(entity_group_conf_mapping[mapped_entity][0])
                        and entity.entity_type in self.entities
                        and validate_extracted_data(
                            entity.entity_type, input_text[entity.start : entity.end]
                        )
                    ):
                        # If current_overlap_group is not empty, check if the entity overlaps with the last one in the group

                        if current_overlap_group and self.entities_overlap(
                            current_overlap_group[-1], entity
                        ):
                            # This code part checks if the overlapping entities are similar i.e both are names
                            # For examples Sarah vs Sarah Jonson
                            last_entity = current_overlap_group[-1]
                            if last_entity.entity_type == entity.entity_type:
                                non_overlapping_results.append(entity)
                            else:
                                # Entity overlaps, add to the current overlap group
                                current_overlap_group.append(entity)
                        else:
                            # If the overlap group has more than 1 entity, save it to overlapping results
                            if len(current_overlap_group) > 1:
                                overlapping_results.append(tuple(current_overlap_group))
                            elif len(current_overlap_group) == 1:
                                # Single entity in the group, add it to non-overlapping results
                                non_overlapping_results.append(current_overlap_group[0])

                            # Start a new overlap group with the current entity
                            current_overlap_group = [entity]

            except Exception as ex:
                import traceback

                logger.warning(
                    f"Error in analyze_response in entity classification. {str(ex)}"
                )
                logger.warning(traceback.format_exc())
        # Handle the last overlap group after the loop
        if len(current_overlap_group) > 1:
            overlapping_results.append(tuple(current_overlap_group))
        elif len(current_overlap_group) == 1:
            non_overlapping_results.append(current_overlap_group[0])

        # Logging the final results for debugging
        overlapping_results_new = judge_results(
            input_text, overlapping_results, self.text_gen_obj
        )

        non_overlapping_results.extend(overlapping_results_new)
        # Return both non-overlapping entities and overlapping groups
        return list(set(non_overlapping_results))

    def anonymize_response(
        self, analyzer_results: list, input_text: str
    ) -> (list, str):
        # Returns anonymized output
        anonymized_text = self.anonymizer.anonymize(
            text=input_text, analyzer_results=analyzer_results
        )

        return anonymized_text.items, anonymized_text.text

    @staticmethod
    def _sort_analyzed_data(data: list) -> list:
        """
        This function sort analyzed response data based on its start position
        """
        # Convert input data into dictionary structure
        analyzed_data = [
            {
                "entity_type": entry.entity_type,
                "start": entry.start,
                "end": entry.end,
                "score": entry.score,
            }
            for entry in data
        ]
        analyzed_data.sort(key=lambda x: x["start"])
        return analyzed_data

    @staticmethod
    def _sort_anonymized_data(data: list) -> list:
        """
        This function sort anonymized response data based on its start position
        """
        # Convert input data into dictionary structure
        anonymized_data = [
            {"entity_type": entry.entity_type, "start": entry.start, "end": entry.end}
            for entry in data
        ]

        # Sort data based on start
        anonymized_data.sort(key=lambda x: x["start"])
        return anonymized_data

    @staticmethod
    def update_anonymized_location(
        start: int, end: int, location_count: int
    ) -> (str, int):
        """
        As we are replacing < with &lt; and > with &gt; respectively in the anonymized text, to make we need to
        adjust the location to match the updated text. Since the length difference between &lt; and <, as well as
        between &gt; and > is 3 characters each, we add a total of 6 i.e., (3 + 3) to the end_location to account for
        the increased length after the replacements.
        """
        location = f"{start+location_count}_{end+location_count+6}"
        location_count += 6
        return location, location_count

    def get_analyzed_entities_response(
        self, data: list, anonymized_response: list = None
    ) -> list:
        # Returns entities with its location i.e. start to end and confidence score

        analyzed_data = self._sort_analyzed_data(data)
        if anonymized_response:
            anonymized_response = self._sort_anonymized_data(anonymized_response)

        response = []
        location_count = 0
        for index, value in enumerate(analyzed_data):
            try:
                mapped_entity = None
                if value["entity_type"] in Entities.__members__:
                    mapped_entity = Entities[value["entity_type"]].value
                elif value["entity_type"] in SecretEntities.__members__:
                    mapped_entity = SecretEntities[value["entity_type"]].value

                location = f"{value['start']}_{value['end']}"
                if anonymized_response:
                    anonymized_data = anonymized_response[index]
                    if anonymized_data["entity_type"] == value["entity_type"]:
                        location, location_count = self.update_anonymized_location(
                            anonymized_data["start"],
                            anonymized_data["end"],
                            location_count,
                        )
                response.append(
                    {
                        "entity_type": value["entity_type"],
                        "location": location,
                        "confidence_score": value["score"],
                        "entity_group": entity_group_conf_mapping[mapped_entity][1],
                    }
                )
            except Exception:
                pass
        return response

    def presidio_entity_classifier_and_anonymizer(
        self, input_text: str, anonymize_snippets: bool = False
    ) -> (dict, int, str, dict):
        """
        Perform classification on the input data and return a dictionary with the count of each entity group.
        And also returns plain input text as anonymized text output
        :param input_text: Input string / document snippet
        :param anonymize_snippets: Flag whether to anonymize snippets in report.
        :return: entities: containing the entity group Name as key and its count as value.
                 total_count: Total count of entity groupsInput text in anonymized form.
                 anonymized_text: Input text in anonymized form.
                 entity_details: Entities with its details such as location and confidence score.
        Example:

        input_text = " My SSN is 222-85-4836.
        ITIN number 993-77 0690
        And AWS Access Key is: AKIAQIPT4PDORIRTV6PH."
        response:
        entities = {'aws-access-key': 1, 'us-itin': 1, 'us-ssn': 1}
        total_count = 3
        anonymized_text = "My SSN is &lt;US_SSN&gt;.
        ITIN number &lt;US_ITIN&gt;
        And AWS Access Key is: &lt;AWS_ACCESS_KEY&gt;."
        My phone number is +91 8087611243
        """
        entities = {}
        total_count = 0
        try:
            logger.debug("Presidio Entity Classifier and Anonymizer Started.")

            analyzer_results = self.analyze_response(input_text)
            if anonymize_snippets:  # If Document snippet needs to be anonymized
                anonymized_response, anonymized_text = self.anonymize_response(
                    analyzer_results, input_text
                )
                input_text = anonymized_text.replace("<", "&lt;").replace(">", "&gt;")
                entities_response = self.get_analyzed_entities_response(
                    analyzer_results, anonymized_response
                )
            else:
                entities_response = self.get_analyzed_entities_response(
                    analyzer_results
                )
            entities, entity_details, total_count = get_entities(
                self.entities, entities_response
            )
            logger.debug("Presidio Entity Classifier and Anonymizer Finished")
            logger.debug(f"Entities: {entities}")
            logger.debug(f"Entity Total count: {total_count}")
            return entities, total_count, input_text, entity_details
        except Exception as e:
            logger.error(
                f"Presidio Entity Classifier and Anonymizer Failed, Exception: {e}"
            )
            return entities, total_count, input_text
