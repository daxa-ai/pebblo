"""AI(Apps) Model Class"""

from typing import Dict, List, Optional, Union
from uuid import uuid4

from pydantic import BaseModel, Field


class Metadata(BaseModel):
    createdAt: str
    modifiedAt: str

    class Config:
        arbitrary_types_allowed = True


class InstanceDetails(BaseModel):
    type: Optional[str]
    host: Optional[str]
    path: Optional[str]
    runtime: Optional[str]
    ip: Optional[str]
    language: Optional[str]
    languageVersion: Optional[str]
    platform: Optional[str]
    os: Optional[str]
    osVersion: Optional[str]
    createdAt: Optional[str]


class FrameworkInfo(BaseModel):
    name: Optional[str]
    version: Optional[str]


class AiBaseApp(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    description: Optional[str]
    pluginVersion: Optional[str]
    lastUsed: str
    metadata: Metadata
    instanceDetails: Optional[InstanceDetails]
    framework: Optional[FrameworkInfo] = Field(default_factory=FrameworkInfo)
    policyViolations: Optional[
        List[dict]
    ] = []  # list of policy id, title and other details
    pebbloServerVersion: Optional[str] = None
    pebbloClientVersion: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True
        use_enum_values = True


class AiModel(BaseModel):
    name: str
    vendor: Optional[str]


class PackageInfo(BaseModel):
    projectHomePage: Optional[str]
    documentationUrl: Optional[str]
    pypiUrl: Optional[str]
    licenceType: Optional[str]
    installedVia: Optional[str]
    location: Optional[str]


class VectorDB(BaseModel):
    name: Optional[str] = None
    version: Optional[str] = None
    location: Optional[str] = None
    embeddingModel: Optional[str] = None
    pkgInfo: Optional[PackageInfo]


class Chain(BaseModel):
    name: Optional[str]
    vectorDbs: Optional[List[VectorDB]] = []
    model: Optional[AiModel]


class AiDataModel(BaseModel):
    data: Optional[Union[list, str]]
    entityCount: int
    entities: dict
    topicCount: Optional[int] = None
    topics: Optional[dict] = None

    def dict(self, **kwargs):
        kwargs["exclude_none"] = True
        return super().dict(**kwargs)


class RetrievalContext(BaseModel):
    retrieved_from: str
    doc: str
    vector_db: str


class RetrievalData(BaseModel):
    prompt: AiDataModel
    response: AiDataModel
    context: list[RetrievalContext]
    prompt_time: str
    user: str
    linked_groups: list[str] = []


class AiApp(AiBaseApp):
    chains: Optional[List[Chain]] = []
    retrievals: Optional[List[RetrievalData]] = []
    entities: Optional[Dict] = {}
    topics: Optional[Dict] = {}
    documents: Optional[List[str]] = []  # list of doc ids, TODO: need confirmation
    users: List[str] = []


class LoaderMetadata(BaseModel):
    name: str
    sourcePath: str
    sourceType: str
    sourceSize: int
    sourceFiles: Optional[list] = []
    lastModified: Optional[str]


class AiDataLoader(AiBaseApp):
    loaders: Optional[List[LoaderMetadata]] = []
    # documents: Optional[List[UUID]] = [] # list of doc ids, TODO: need confirmation
    docEntities: Optional[Dict] = {}
    docTopics: Optional[Dict] = {}
    documents: Optional[List[str]] = []
    documentsWithFindings: Optional[List[str]] = []
