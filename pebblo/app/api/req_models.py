"""API Request Model Class"""

from typing import Optional

from pydantic import BaseModel

from pebblo.app.enums.common import ClassificationMode


class ReqClassifier(BaseModel):
    data: str
    mode: Optional[ClassificationMode] = None
    anonymize: Optional[bool] = None

    class Config:
        extra = "forbid"
