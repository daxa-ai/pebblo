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
