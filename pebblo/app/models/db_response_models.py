"""AI(Apps) Model Class"""

from typing import List, Optional, Union

from pydantic import BaseModel, Field

from pebblo.app.models.db_models import FrameworkInfo, InstanceDetails, RetrievalData


class LoaderDocs(BaseModel):
    pb_id: Optional[str] = None
    pb_checksum: str
    source_path: str
    loader_source_path: str
    entity_count: Optional[int] = None
    entities: Optional[dict] = {}
    topic_count: Optional[int] = None
    topics: Optional[dict] = {}


class LoaderDocResponseModel(BaseModel):
    docs: List[LoaderDocs] = []
    message: Optional[str] = None


class AiClassificationData(BaseModel):
    entities: dict
    topics: Optional[dict] = {}


class RetrievalResponse(BaseModel):
    prompt: AiClassificationData
    response: AiClassificationData


class PromptResponseModel(BaseModel):
    retrieval_data: Union[RetrievalResponse, None] = None
    message: Optional[str] = None


class RetrievalAppDetails(BaseModel):
    name: str
    description: Optional[str] = None
    framework: Optional[FrameworkInfo] = Field(default_factory=FrameworkInfo)
    instanceDetails: Optional[InstanceDetails] = None
    pebbloServerVersion: Optional[str] = None
    pebbloClientVersion: Optional[str] = None
    clientVersion: Optional[dict] = {}
    total_prompt_with_findings: int = 0
    retrievals: list[RetrievalData] = []
    activeUsers: dict = {}
    vectorDbs: dict = {}
    documents: dict = {}


class RetrievalAppListDetails(BaseModel):
    name: str = ""
    owner: str = ""
    retrievals: list[RetrievalData] = []
    active_users: list[str] = []
    vector_dbs: list[str] = []
    documents: list[str] = []


class RetrievalAppList(BaseModel):
    appList: list = []
    retrievals: list = []
    activeUsers: dict = {}
    violations: list = []
    promptDetails: list = []
    total_prompt_with_findings: int = 0
