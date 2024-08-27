from datetime import datetime
from typing import List, Optional, Union
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class Metadata(BaseModel):
    createdAt: datetime
    modifiedAt: datetime
    model_config = ConfigDict(arbitrary_types_allowed=True)


class LoaderMetadata(BaseModel):
    name: str
    sourcePath: str
    sourceType: str
    sourceSize: int
    sourceFiles: Optional[list] = []
    lastModified: Optional[datetime] = None


class AiDataModel(BaseModel):
    data: Optional[Union[list, str]] = None
    entityCount: int
    entities: dict
    entityDetails: Optional[dict] = {}
    topicCount: Optional[int] = None
    topics: Optional[dict] = {}
    topicDetails: Optional[dict] = {}


class AiDocs(BaseModel):
    id: Optional[str] = None
    doc: str
    sourceSize: int
    fileOwner: str
    sourcePath: str
    loaderSourcePath: str
    lastModified: Optional[datetime] = None
    entityCount: Optional[int] = None
    entityDetails: Optional[dict] = {}
    entities: Optional[dict] = {}
    topicCount: Optional[int] = None
    topicDetails: Optional[dict] = {}
    topics: Optional[dict] = {}
    authorizedIdentities: list


class FrameworkInfo(BaseModel):
    name: Optional[str] = None
    version: Optional[str] = None


class InstanceDetails(BaseModel):
    type: Optional[str] = None
    host: Optional[str] = None
    path: Optional[str] = None
    runtime: Optional[str] = None
    ip: Optional[str] = None
    language: Optional[str] = None
    languageVersion: Optional[str] = None
    platform: Optional[str] = None
    os: Optional[str] = None
    osVersion: Optional[str] = None
    createdAt: datetime


class PackageInfo(BaseModel):
    projectHomePage: Optional[str] = None
    documentationUrl: Optional[str] = None
    pypiUrl: Optional[str] = None
    licenceType: Optional[str] = None
    installedVia: Optional[str] = None
    location: Optional[str] = None


class VectorDB(BaseModel):
    name: Optional[str] = None
    version: Optional[str] = None
    location: Optional[str] = None
    embeddingModel: Optional[str] = None
    pkgInfo: Optional[PackageInfo] = None


class AiModel(BaseModel):
    name: str
    vendor: Optional[str] = None


class Chain(BaseModel):
    name: Optional[str] = None
    vectorDbs: Optional[List[VectorDB]] = []
    model: Optional[AiModel] = None


class RetrievalContext(BaseModel):
    retrieved_from: str
    doc: str
    vector_db: str


class AiClassificationData(BaseModel):
    entities: dict
    topics: Optional[dict] = {}


class RetrievalData(BaseModel):
    prompt: AiDataModel
    response: AiDataModel
    context: list[RetrievalContext]
    prompt_time: str
    user: str
    linked_groups: list[str] = []


class AiApp(BaseModel):
    metadata: Metadata
    name: str
    description: Optional[str] = None
    owner: str
    pluginVersion: Optional[str] = None
    instanceDetails: Optional[InstanceDetails] = None
    framework: Optional[FrameworkInfo] = None
    lastUsed: datetime
    pebbloServerVersion: Optional[str] = None
    pebbloClientVersion: Optional[str] = None
    clientVersion: Union[FrameworkInfo, None] = None
    chains: Optional[List[Chain]] = []
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
    entityDetails: Optional[dict] = {}
    topicDetails: Optional[dict] = {}
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
    findingsDetails: Optional[list] = []
    # snippets: Optional[List[Snippets]]


class LoadHistory(BaseModel):
    loadId: UUID
    reportName: str
    findings: int
    filesWithFindings: int
    generatedOn: datetime


class ReportModel(BaseModel):
    name: str
    description: Optional[str] = None
    framework: Optional[FrameworkInfo] = Field(default_factory=FrameworkInfo)
    reportSummary: Optional[Summary] = None
    loadHistory: Optional[dict] = {}
    topFindings: Optional[List[TopFindings]] = []
    instanceDetails: Optional[InstanceDetails] = None
    dataSources: Optional[List[DataSource]] = []
    pebbloServerVersion: Optional[str] = None
    pebbloClientVersion: Optional[str] = None
    clientVersion: Optional[dict] = {}


class LoaderAppListDetails(BaseModel):
    name: str
    topics: int
    entities: int
    owner: Optional[str] = None
    loadId: Optional[str] = None


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
    promptDetails: list = []
    total_prompt_with_findings: int = 0


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


class DiscoverAIAppsResponseModel(BaseModel):
    pebblo_server_version: Union[str, None] = None
    message: Optional[str] = None


class RetrievalResponse(BaseModel):
    prompt: AiClassificationData
    response: AiClassificationData


class PromptResponseModel(BaseModel):
    retrieval_data: Union[RetrievalResponse, None] = None
    message: Optional[str] = None


class PromptGovResponseModel(BaseModel):
    entities: dict
    entityCount: int
    message: Optional[str] = None
