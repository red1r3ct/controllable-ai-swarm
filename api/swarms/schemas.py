from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


class Swarm(BaseModel):
    id: int
    name: str
    created_at: datetime
    updated_at: datetime


class SwarmCreateRequest(BaseModel):
    name: str


class ListMeta(BaseModel):
    total: int
    next_cursor: Optional[int]


class SwarmListResponse(BaseModel):
    meta: ListMeta
    data: List[Swarm]


class SwarmUpdateRequest(BaseModel):
    name: Optional[str]


class Agent(BaseModel):
    id: int
    model: str
    name: str
    role: str
    instruction: str

    created_at: datetime
    updated_at: datetime


class AgentCreateRequest(BaseModel):
    model: str
    name: str
    role: str
    instruction: str


class AgentListResponse(BaseModel):
    meta: ListMeta
    data: List[Agent]


class AgentUpdateRequest(BaseModel):
    model: Optional[str]
    role: Optional[str]
    instruction: Optional[str]
    name: Optional[str]


class SwarmAddAgentRequest(BaseModel):
    agent_ids: List[int]


class SwarmAddAgentResponse(Swarm):
    agents: List[Agent]


class SwarmReadResponse(Swarm):
    agents: List[Agent]
