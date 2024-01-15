# Copyright (c) 2024 Daxa. All rights reserved.
from pydantic import BaseModel, Field
from typing import Optional, List, Union
from datetime import datetime, timezone


class Metadata(BaseModel):
    createdAt: datetime = datetime.now(timezone.utc)
    modifiedAt: datetime = datetime.now(timezone.utc)
    cloudAccountId: Optional[str]
    customerId: Optional[str]
    tenantId: Optional[str]

    class Config:
        arbitrary_types_allowed = True


class PackageInfo(BaseModel):
    projectHomePage: Optional[str]
    documentationUrl: Optional[str]
    pypiUrl: Optional[str]
    licenceType: Optional[str]
    installedVia: Optional[str]
    location: Optional[str]


class VectorDb(BaseModel):
    name: str
    version: str
    embeddingModel: str
    location: Optional[str]
    packageInfo: Optional[PackageInfo] = Field(default_factory=PackageInfo)


class AppModel(BaseModel):
    name: str
    vendor: Optional[str]


class Chain(BaseModel):
    name: Optional[str]
    vectorDbs: Optional[List[VectorDb]] = []
    model: Optional[AppModel]


class LoaderMetadata(BaseModel):
    name: str
    sourcePath: str
    sourceType: str
    sourceFiles: Optional[list] = []
    lastModified: Optional[datetime] = datetime.now(timezone.utc)



class AiDataModel(BaseModel):
    data: Optional[Union[list, str]]
    entityCount: int
    entities: dict
    topicCount: int
    topics: dict


class AiDocs(BaseModel):
    name: str  # aiapp_name
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
    # label_feedback: Optional[List[LabelFeedback]] = []


class FrameworkInfo(BaseModel):
    name: Optional[str]
    version: Optional[str]


class InstanceDetail(BaseModel):
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


class AiApp(BaseModel):
    name: str
    pluginVersion: Optional[str]
    createdAt: datetime = datetime.now(timezone.utc)
    deployedAt: datetime = datetime.now(timezone.utc)
    instanceDetails: Optional[InstanceDetail]
    chains: Optional[List[Chain]] = []
    loaders: Optional[List[LoaderMetadata]] = []
    framework: Optional[FrameworkInfo] = Field(default_factory=FrameworkInfo)
    metadata: Metadata
    lastUsed: datetime = datetime.now(timezone.utc)
    # promptStats: PromptStats = Field(default_factory=PromptStats)
    # Policy violations and sensitive info
    policyViolations: Optional[List[dict]] = []  # list of policy id, title and other details