"""AI(Apps) Model Class"""

from typing import List, Optional, Union

from pydantic import BaseModel


class LoaderDocs(BaseModel):
    pb_id: Optional[str]
    pb_checksum: str
    source_path: str
    loader_source_path: str
    entity_count: Optional[int]
    entities: Optional[dict]
    topic_count: Optional[int]
    topics: Optional[dict]


class LoaderDocResponseModel(BaseModel):
    docs: List[LoaderDocs] = []
    message: Optional[str] = None


class AiClassificationData(BaseModel):
    entities: dict
    topics: Optional[dict] = None


class RetrievalResponse(BaseModel):
    prompt: AiClassificationData
    response: AiClassificationData


class PromptResponseModel(BaseModel):
    retrieval_data: Union[RetrievalResponse, None] = None
    message: Optional[str] = None
