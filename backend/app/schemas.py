from typing import List, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime


class KeywordCreate(BaseModel):
    term: str
    category: str = "general"
    description: str = ""


class KeywordOut(BaseModel):
    id: int
    term: str
    category: str
    description: str
    created_at: datetime

    model_config = {"from_attributes": True}


class PostIn(BaseModel):
    id: str
    platform: str
    author_id: str | None = None
    author_handle: str | None = None
    text: str
    hashtags: List[str] = Field(default_factory=list)
    mentions: List[str] = Field(default_factory=list)
    meta: dict = Field(default_factory=dict)
    created_at: datetime | None = None


class PostOut(BaseModel):
    id: str
    platform: str
    author_id: Optional[str]
    author_handle: Optional[str]
    text: str
    language: Optional[str]
    toxicity: Optional[float]
    stance: Optional[str]
    hashtags: List[str]
    mentions: List[str]
    meta: dict
    created_at: datetime

    model_config = {"from_attributes": True}


class AlertOut(BaseModel):
    id: int
    name: str
    risk_score: float
    details: dict
    created_at: datetime

    model_config = {"from_attributes": True}


