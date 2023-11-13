from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from enum import Enum


class TaskStatus(str, Enum):
    todo = "todo"
    in_progress = "assigned"
    completed = "completed"
    failed = "failed"


class Task(BaseModel):
    id: int
    name: str
    status: TaskStatus
    description: str
    log: List[str]

    author: str
    assignee: Optional[str]

    project_id: int

    created_at: datetime
    updated_at: datetime


class TaskCreateRequest(BaseModel):
    name: str
    status: TaskStatus = TaskStatus.todo
    description: str
    project_id: int
    author: str
    assignee: Optional[str]
    log: List[str]


class TaskUpdateRequest(BaseModel):
    name: Optional[str]
    status: Optional[TaskStatus]
    assignee: Optional[str]
    description: Optional[str]


class ListMeta(BaseModel):
    total: int
    next_cursor: Optional[int]


class TaskListResponse(BaseModel):
    meta: ListMeta
    data: List[Task]
