"""API Request Model Class"""

from typing import List, Optional, Union

from pydantic import BaseModel, Field

from pebblo.app.enums.common import ClassificationMode


class Runtime(BaseModel):
    type: str = "local"
    host: str
    path: str
    ip: Optional[str] = None
    platform: str
    os: str
    os_version: str
    language: str
    language_version: str
    runtime: str = "local"


class Framework(BaseModel):
    name: str
    version: str


class VectorDB(BaseModel):
    name: Optional[str] = None
    version: Optional[str] = None
    location: Optional[str] = None
    embedding_model: Optional[str] = None


class Model(BaseModel):
    vendor: Optional[str] = None
    name: Optional[str] = None


class ChainInfo(BaseModel):
    name: str
    model: Optional[Model] = None
    vector_dbs: Optional[List[VectorDB]] = None


class ReqDiscover(BaseModel):
    name: str
    owner: str
    description: Optional[str] = None
    load_id: Optional[str] = None
    runtime: Runtime
    framework: Framework
    chains: Optional[List[ChainInfo]] = None
    plugin_version: str
    client_version: Optional[Framework] = None


class ReqLoaderDoc(BaseModel):
    name: str
    owner: str
    docs: list[dict] = None
    plugin_version: str
    load_id: str
    loader_details: dict
    loading_end: bool
    source_owner: str
    classifier_location: str
    classifier_mode: Optional[str] = None
    anonymize_snippets: Optional[bool] = None


class Context(BaseModel):
    retrieved_from: Optional[str] = None
    doc: Optional[str] = None
    vector_db: str
    pb_checksum: Optional[str] = None


class Prompt(BaseModel):
    data: Optional[Union[list, str]] = None
    entityCount: Optional[int] = None
    entities: Optional[dict] = None
    prompt_gov_enabled: Optional[bool] = None


class ReqPrompt(BaseModel):
    name: str
    context: Optional[List[Context]] = None
    prompt: Optional[Prompt] = None
    response: Optional[Prompt] = None
    prompt_time: str
    user: str
    user_identities: Optional[List[str]] = None
    classifier_location: str


class ReqPromptGov(BaseModel):
    prompt: str


class ReqClassifier(BaseModel):
    data: str
    mode: Optional[ClassificationMode] = Field(default=ClassificationMode.ALL)
    anonymize: Optional[bool] = Field(default=False)

    class Config:
        extra = "forbid"
