from datetime import datetime
from typing import List, Optional, Union
from uuid import UUID

from pydantic import BaseModel, Field


class Metadata(BaseModel):
    createdAt: datetime
    modifiedAt: datetime

    class Config:
        arbitrary_types_allowed = True


class LoaderMetadata(BaseModel):
    name: str
    sourcePath: str
    sourceType: str
    sourceSize: int
    sourceFiles: Optional[list] = []
    lastModified: Optional[datetime]


class AiDataModel(BaseModel):
    data: Optional[Union[list, str]]
    entityCount: int
    entities: dict
    topicCount: int
    topics: dict


class AiDocs(BaseModel):
    id: Optional[str]
    doc: str
    sourceSize: int
    fileOwner: str
    sourcePath: str
    loaderSourcePath: str
    lastModified: Optional[datetime]
    entityCount: Optional[int]
    entities: Optional[dict]
    topicCount: Optional[int]
    topics: Optional[dict]
    authorizedIdentities: list


class FrameworkInfo(BaseModel):
    name: Optional[str]
    version: Optional[str]


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
    createdAt: datetime


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


class AiModel(BaseModel):
    name: str
    vendor: Optional[str]


class Chain(BaseModel):
    name: Optional[str]
    vectorDbs: Optional[List[VectorDB]] = []
    model: Optional[AiModel]


class RetrievalContext(BaseModel):
    retrieved_from: str
    doc: str
    vector_db: str
    entityCount: Optional[int]
    entities: Optional[dict]
    topicCount: Optional[int]
    topics: Optional[dict]


class RetrievalData(BaseModel):
    prompt: AiDataModel
    response: AiDataModel
    prompt_time: str
    user: str
    linked_groups: list[str] = []


class AiApp(BaseModel):
    metadata: Metadata
    name: str
    description: Optional[str]
    owner: str
    pluginVersion: Optional[str]
    instanceDetails: Optional[InstanceDetails]
    framework: Optional[FrameworkInfo]
    lastUsed: datetime
    pebbloServerVersion: Optional[str]
    pebbloClientVersion: Optional[str]
    chains: Optional[List[Chain]]
    retrievals: Optional[List[RetrievalData]] = []


class Summary(BaseModel):
    findings: int
    findingsEntities: int
    findingsTopics: int
    totalFiles: int
    filesWithFindings: int
    dataSources: int
    owner: str
    createdAt: datetime


class TopFindings(BaseModel):
    fileName: str
    fileOwner: str
    sourceSize: int
    findingsEntities: int
    findingsTopics: int
    findings: int
    authorizedIdentities: list


class Snippets(BaseModel):
    snippet: str
    sourcePath: str
    fileOwner: str
    authorizedIdentities: list


class DataSource(BaseModel):
    name: str
    sourcePath: str
    sourceType: str
    sourceSize: int
    totalSnippetCount: int
    displayedSnippetCount: int
    findingsSummary: list
    findingsDetails: Optional[list]
    # snippets: Optional[List[Snippets]]


class LoadHistory(BaseModel):
    loadId: UUID
    reportName: str
    findings: int
    filesWithFindings: int
    generatedOn: datetime


class ReportModel(BaseModel):
    name: str
    description: Optional[str]
    framework: Optional[FrameworkInfo] = Field(default_factory=FrameworkInfo)
    reportSummary: Optional[Summary]
    loadHistory: Optional[dict]
    topFindings: Optional[List[TopFindings]]
    instanceDetails: Optional[InstanceDetails]
    dataSources: Optional[List[DataSource]]
    pebbloServerVersion: Optional[str]
    pebbloClientVersion: Optional[str]


class LoaderAppListDetails(BaseModel):
    name: str
    topics: int
    entities: int
    owner: Optional[str]
    loadId: Optional[str]


class LoaderAppModel(BaseModel):
    applicationsAtRiskCount: int
    findingsCount: int
    documentsWithFindingsCount: int
    dataSourceCount: int
    appList: List[LoaderAppListDetails]
    findings: list
    documentsWithFindings: list
    dataSource: list


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


class RetrievalAppDetails(BaseModel):
    name: str
    description: Optional[str]
    framework: Optional[FrameworkInfo] = Field(default_factory=FrameworkInfo)
    instanceDetails: Optional[InstanceDetails]
    pebbloServerVersion: Optional[str]
    pebbloClientVersion: Optional[str]
    retrievals: list[RetrievalData] = []
    activeUsers: dict = {}
    vectorDbs: dict = {}
    documents: dict = {}


class LoaderDocs(BaseModel):
    pb_id: Optional[str]
    content_checksum: str
    source_path: str
    loader_source_path: str
    entity_count: Optional[int]
    entities: Optional[dict]
    topic_count: Optional[int]
    topics: Optional[dict]


class LoaderDocResponseModel(BaseModel):
    docs: List[LoaderDocs] = []
    message: Optional[str] = None


class DiscoverAIAppsResponseModel(BaseModel):
    pebblo_server_version: Union[str, None] = None
    message: Optional[str] = None


class PromptResponseModel(BaseModel):
    retrieval_data: Union[RetrievalData, None] = None
    message: Optional[str] = None
