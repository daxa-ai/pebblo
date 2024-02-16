from pydantic import BaseModel, Field
from typing import Optional, List, Union
from datetime import datetime
from uuid import UUID


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
    doc: str
    sourceSize: int
    fileOwner: str
    sourcePath: str
    loaderSourcePath: str
    lastModified: Optional[datetime]
    entityCount: int
    entities: dict
    topicCount: int
    topics: dict


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


class AiApp(BaseModel):
    metadata: Metadata
    name: str
    description: Optional[str]
    owner: str
    pluginVersion: Optional[str]
    instanceDetails: Optional[InstanceDetails]
    framework: Optional[FrameworkInfo]
    lastUsed: datetime


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


class Snippets(BaseModel):
    snippet: str
    sourcePath: str
    fileOwner: str


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
