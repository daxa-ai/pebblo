from typing import Optional

from pydantic import BaseModel, Field


class DocsFindings(BaseModel):
    doc_name: str
    at_risk: bool
    topics: Optional[list] = Field(default_factory=list)
    entities: Optional[list] = Field(default_factory=list)
    access_groups: Optional[list] = Field(default_factory=list)


class DocResp(BaseModel):
    docs_at_risk: int = 0
    docs_findings: list[DocsFindings] = Field(default_factory=list)


class LabelDetails(BaseModel):
    data: str
    entity_details: dict
    topic_details: dict


class RetrievalDetail(BaseModel):
    with_concern: bool
    queried_by: str
    prompt_time: str
    prompt: dict = Field(default_factory=dict)
    response: dict = Field(default_factory=dict)


class RetrievalResp(BaseModel):
    retrievals_with_concern: int = 0
    retrievals: list[RetrievalDetail] = Field(default_factory=list)
