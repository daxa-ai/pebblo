# Copyright (c) 2024 Daxa. All rights reserved.
from pydantic import BaseModel, Field
from typing import Optional, List, Union
from datetime import datetime


class Metadata(BaseModel):
    createdAt: datetime = datetime.now()
    modifiedAt: datetime = datetime.now()

    class Config:
        arbitrary_types_allowed = True


class LoaderMetadata(BaseModel):
    name: str
    sourcePath: str
    sourceType: str
    sourceFiles: Optional[list] = []
    lastModified: Optional[datetime] = datetime.now()


class AiDataModel(BaseModel):
    data: Optional[Union[list, str]]
    entityCount: int
    entities: dict
    topicCount: int
    topics: dict


class AiDocs(BaseModel):
    metadata: Metadata
    doc: str
    sourcePath: str
    loaderSourcePath: str
    lastModified: Optional[datetime]
    entityCount: int
    entities: dict
    topicCount: int
    topics: dict
    policyViolations: Optional[List[dict]] = []


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
    createdAt: datetime = datetime.now()


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
    findings_entities: int
    findings_topics: int
    totalFiles: int
    filesWithRestrictedData: int
    dataSources: int
    owner: str
    createdAt: datetime = datetime.now()


class TopFindings(BaseModel):
    fileName: str
    count: int


class Snippets(BaseModel):
    snippet: str
    sourcePath: str


class DataSource(BaseModel):
    name: str
    sourcePath: str
    sourceType: str
    findingsSummary: list
    findingsDetails: Optional[list]
    # snippets: Optional[List[Snippets]]


class ReportModel(BaseModel):
    name: str
    description: Optional[str]
    framework: Optional[FrameworkInfo] = Field(default_factory=FrameworkInfo)
    reportSummary: Optional[Summary]
    topFindings: Optional[List[TopFindings]]
    instanceDetails: Optional[InstanceDetails]
    dataSources: Optional[List[DataSource]]
    lastModified: datetime
