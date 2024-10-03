"""AI(Apps) Model Class"""

from typing import Dict, List, Optional, Union
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field


class Metadata(BaseModel):
    createdAt: str
    modifiedAt: str
    model_config = ConfigDict(arbitrary_types_allowed=True)


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
    createdAt: Optional[str] = None


class FrameworkInfo(BaseModel):
    name: Optional[str] = None
    version: Optional[str] = None


class AiBaseApp(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    owner: str
    description: Optional[str] = None
    pluginVersion: Optional[str] = None
    lastUsed: str
    metadata: Metadata
    instanceDetails: Optional[InstanceDetails] = None
    framework: Optional[FrameworkInfo] = Field(default_factory=FrameworkInfo)
    policyViolations: Optional[
        List[Dict]
    ] = []  # list of policy id, title and other details
    pebbloServerVersion: Optional[str] = None
    pebbloClientVersion: Optional[str] = None
    clientVersion: Optional[FrameworkInfo] = None
    model_config = ConfigDict(arbitrary_types_allowed=True, use_enum_values=True)


class AiModel(BaseModel):
    name: str
    vendor: Optional[str] = None


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
    pkgInfo: Optional[PackageInfo] = []


class Chain(BaseModel):
    name: Optional[str] = None
    vectorDbs: Optional[List[VectorDB]] = []
    model: Optional[AiModel] = None


class AiDataModel(BaseModel):
    data: Optional[Union[list, str]] = None
    entityCount: int
    entities: dict
    entityDetails: Optional[dict] = {}
    topicCount: Optional[int] = 0
    topics: Optional[dict] = {}
    topicDetails: Optional[dict] = {}


class RetrievalContext(BaseModel):
    retrievedFrom: str
    doc: str
    vectorDb: str


class RetrievalData(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    appName: Optional[str] = None
    prompt: AiDataModel
    response: AiDataModel
    context: list[RetrievalContext]
    promptTime: str
    user: str
    userId: Optional[str] = None
    linkedGroups: list[str] = []


class AiUser(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    appName: List
    metadata: Metadata
    userAuthGroup: Optional[List] = []
    documentsAccessed: Optional[List] = []
    lastUsed: str


class AiApp(AiBaseApp):
    chains: Optional[List[Chain]] = []
    retrievals: Optional[list] = []
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
    lastModified: Optional[str] = None


class AiDataLoader(AiBaseApp):
    loaders: Optional[List[LoaderMetadata]] = []
    runId: Optional[str] = None
    # documents: Optional[List[UUID]] = [] # list of doc ids, TODO: need confirmation
    docEntities: Optional[Dict] = {}
    docTopics: Optional[Dict] = {}
    documents: Optional[List[str]] = []
    documentsWithFindings: Optional[List[str]] = []


class AiDataSource(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    runId: Optional[str] = None
    appName: str
    loadId: str
    metadata: Metadata
    sourcePath: str
    sourceSize: int
    sourceType: str
    loader: str


class AiDocument(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    runId: Optional[str] = None
    appName: str
    loadId: str
    dataSourceId: str
    loaderSourcePath: str
    metadata: Metadata
    sourcePath: str
    sourceSize: int
    lastIngested: str
    owner: str
    userIdentities: Optional[List[str]] = []
    topics: Optional[dict] = {}
    entities: Optional[dict] = {}


class AiSnippet(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    runId: Optional[str] = None
    appName: str
    loadId: str
    dataSourceId: str
    dataSourceName: str
    documentId: str
    metadata: Metadata
    doc: Optional[str] = None
    checksum: Optional[str] = None
    sourcePath: str
    loaderSourcePath: str
    lastModified: Optional[str] = None
    entities: dict
    topics: dict
    entityDetails: Optional[dict] = {}
    topicDetails: Optional[dict] = {}
    policyViolations: Optional[List[dict]] = []
    # label_feedback: Optional[List[LabelFeedback]] = []


class Summary(BaseModel):
    findings: int
    findingsEntities: int
    findingsTopics: int
    totalFiles: int
    filesWithFindings: int
    dataSources: int
    owner: str
    createdAt: str


class LoadHistory(BaseModel):
    loadId: str
    reportName: str
    findings: int
    filesWithFindings: int
    generatedOn: str


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


class TopFindings(BaseModel):
    fileName: str
    fileOwner: str
    dataSource: Optional[str] = None
    sourceSize: int
    findingsEntities: int
    findingsTopics: int
    findings: int
    authorizedIdentities: list


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


class ReportModel(BaseModel):
    name: str
    description: Optional[str] = None
    framework: Optional[FrameworkInfo] = Field(default_factory=FrameworkInfo)
    reportSummary: Optional[Summary] = None
    loadHistory: Optional[dict] = None
    topFindings: Optional[List[TopFindings]] = None
    instanceDetails: Optional[InstanceDetails] = None
    dataSources: Optional[List[DataSource]] = None
    pebbloServerVersion: Optional[str] = None
    pebbloClientVersion: Optional[str] = None
    clientVersion: Optional[dict] = None
    snippets: Optional[list] = []
