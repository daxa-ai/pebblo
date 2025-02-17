"""
Module for topic classification using Pebblo, Hugging Face, and Bedrock/vLLM backends.
Defines the TopicClassifier class with methods for predicting topics and extracting them from the model's response.
"""

import os
import re
from typing import Any, Dict, List, Optional, Union

from boto3 import client as boto3_client
from huggingface_hub import login
from json_repair import repair_json
from litellm import completion

from pebblo.log import get_logger

logger = get_logger(__name__)

# Environment variables for backend configuration
BACKEND: str = os.getenv("BACKEND", "vllm")  # Default to "vllm" if not set
MODEL_NAME: str = os.getenv("MODEL_NAME", "daxa-ai/pebblo_classifier_v3")
API_BASE_URL: str = os.getenv("API_BASE_URL", "")
AWS_REGION: Optional[str] = os.getenv("AWS_DEFAULT_REGION")
AWS_ACCESS_KEY: Optional[str] = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY: Optional[str] = os.getenv("AWS_SECRET_ACCESS_KEY")


# Bedrock client initialization if using Bedrock backend
bedrock_client: Optional[Any] = None
if BACKEND.lower() == "bedrock":
    bedrock_client = boto3_client(
        service_name="bedrock-runtime",
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
    )


class SingletonMeta(type):
    """
    Thread-safe Singleton implementation.
    """

    _instances: Dict[type, Any] = {}

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class TextGeneration(metaclass=SingletonMeta):
    """
    Singleton class for text generation and topic classification.
    """

    def __init__(self) -> None:
        # Hugging Face login if token is provided
        huggingface_token: Optional[str] = os.getenv("HF_TOKEN")
        if huggingface_token:
            login(token=huggingface_token)

    def _call_vllm(self, message: List[Dict[str, Union[str, Any]]]) -> Dict[str, Any]:
        """
        Args:
           message (List[Dict[str, Union[str, Any]]]): List of messages for the LLM.
        Returns:
           Dict[str, Any]: Response from the vLLM API.
        """
        response = completion(
            model=f"hosted_vllm/{MODEL_NAME}",
            messages=message,
            temperature=0,
            api_base=API_BASE_URL,
        )
        return response.json()

    def _call_bedrock(
        self, message: List[Dict[str, Union[str, Any]]]
    ) -> Dict[str, Any]:
        """
        Args:
            message (List[Dict[str, Union[str, Any]]]): List of messages for the LLM.
        Returns:
            Dict[str, Any]: Response from the Bedrock API.
        """
        logger.info("In Bedrock")
        response = completion(
            model=f"{os.environ.get('MODEL_NAME')}",
            messages=message,
            temperature=0,
            custom_llm_provider="bedrock",
            aws_bedrock_client=bedrock_client,
        )
        logger.info("Out from Bedrock")
        return response.json()

    def generate(
        self, message: List[Dict[str, Union[str, Any]]], bool_return_json: bool = True
    ) -> Union[str, None]:
        """
        Args:
            message (List[Dict[str, Union[str, Any]]]): List of messages for the LLM.-            bool_return_json (bool): Whether to return repaired JSON.
        Returns:
            Union[str, None]: Generated text or error message.
        """
        try:
            if BACKEND.lower() == "bedrock":
                response = self._call_bedrock(message)
            else:
                response = self._call_vllm(message)
            # Extract text from the response
            text: str = (
                response.get("choices", [{}])[0].get("message", {}).get("content", "")
            )
            if bool_return_json:
                text = repair_json(text.replace("```json", "").replace("```", ""))
            return text
        except Exception as ex:
            logger.error(f"Error during generation: {ex}")
            return None

    def generate_classification(
        self, message: List[Dict[str, Union[str, Any]]]
    ) -> List[str]:
        """
        Args:
            message (List[Dict[str, Union[str, Any]]]): List of messages for the LLM.
        Returns:
           List[str]: List of classifications or ["Other"] on error.
        """
        try:
            if BACKEND.lower() == "bedrock":
                response = self._call_bedrock(message)
            else:
                response = self._call_vllm(message)

            # Extract and process classification from the response
            text: str = (
                response.get("choices", [{}])[0].get("message", {}).get("content", "")
            )
            classification_match = re.search(
                r"<CLASSIFICATION>(.*?)</CLASSIFICATION>", text, re.DOTALL
            )
            classification: str = (
                classification_match.group(1).strip()
                if classification_match
                else "Other"
            )

            if "class" in classification.lower():
                classification = re.findall(r"<CLASS>(.*?)</CLASS>", classification)
            if isinstance(classification, str) and "," in classification:
                classification = classification.split(",")
            return classification
        except Exception as ex:
            logger.error(f"Error during classification generation: {ex}")
            return ["Other"]
