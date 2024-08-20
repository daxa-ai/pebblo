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
    owner: str
    description: Optional[str]
    pluginVersion: Optional[str]
    lastUsed: str
    metadata: Metadata
    instanceDetails: Optional[InstanceDetails]
    framework: Optional[FrameworkInfo] = Field(default_factory=FrameworkInfo)
    policyViolations: Optional[
        List[Dict]
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
    pkgInfo: Optional[PackageInfo] = []


class Chain(BaseModel):
    name: Optional[str]
    vectorDbs: Optional[List[VectorDB]] = []
    model: Optional[AiModel]


class AiDataModel(BaseModel):
    data: Optional[Union[list, str]]
    entityCount: int
    entities: dict
    topicCount: Optional[int] = 0
    topics: Optional[dict] = {}

    def dict(self, **kwargs):
        kwargs["exclude_none"] = True
        return super().dict(**kwargs)


class RetrievalContext(BaseModel):
    retrieved_from: str
    doc: str
    vector_db: str


class RetrievalData(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    app_name: Optional[str]
    prompt: AiDataModel
    response: AiDataModel
    context: list[RetrievalContext]
    prompt_time: str
    user: str
    linked_groups: list[str] = []


class AiUser(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    metadata: Metadata
    userAuthGroup: Optional[List]
    documentsAccessed: Optional[List] = []
    lastUsed: str


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


class AiDataSource(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    app_name: str
    metadata: Metadata
    sourcePath: str
    sourceType: str
    loader: str


class AiDocument(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    appId: str
    dataSourceId: str
    loaderSourcePath: str
    metadata: Metadata
    sourcePath: str
    lastIngested: str
    owner: str
    userIdentities: Optional[List[str]] = []
    topics: Optional[dict] = {}
    entities: Optional[dict] = {}


class AiSnippet(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    appId: str
    dataSourceId: str
    documentId: str
    metadata: Metadata
    doc: Optional[str] = None
    checksum: Optional[str] = None
    sourcePath: str
    loaderSourcePath: str
    lastModified: Optional[str] = str
    entities: dict
    topics: dict
    policyViolations: Optional[List[dict]] = []
    # label_feedback: Optional[List[LabelFeedback]] = []


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
