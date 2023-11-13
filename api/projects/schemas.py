from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime


class Project(BaseModel):
    id: int
    name: str

    created_at: datetime
    updated_at: datetime


class ProjectCreateRequest(BaseModel):
    name: str


class ListMeta(BaseModel):
    total: int
    next_cursor: Optional[int]


class ProjectListResponse(BaseModel):
    meta: ListMeta
    data: List[Project]
