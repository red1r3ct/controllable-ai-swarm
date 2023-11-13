from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from typing import List, Optional

from database import get_db
import swarms.models as models
import swarms.schemas as schemas

# CRUD for Swarm
swarms_router = APIRouter()


@swarms_router.post("/swarms/", response_model=schemas.Swarm)
def create_swarm(swarm: schemas.SwarmCreateRequest, db: Session = Depends(get_db)):
    db_swarm = models.Swarm(**swarm.model_dump())
    db.add(db_swarm)
    db.commit()
    db.refresh(db_swarm)
    return db_swarm


@swarms_router.get("/swarms/", response_model=schemas.SwarmListResponse)
def read_swarms(
    cursor: Optional[int] = None, limit: int = 50, db: Session = Depends(get_db)
):
    query = db.query(models.Swarm)

    if cursor:
        query = query.filter(models.Swarm.id > cursor)
    swarms = query.order_by(models.Swarm.id).limit(limit).all()
    total_swarms = db.query(models.Swarm).count()

    return {
        "meta": schemas.ListMeta(
            total=total_swarms,
            next_cursor=swarms[-1].id if swarms else None,
        ),
        "data": swarms,
    }


@swarms_router.get("/swarms/{swarm_id}", response_model=schemas.SwarmReadResponse)
def read_swarm(swarm_id: int, db: Session = Depends(get_db)):
    swarm = (
        db.query(models.Swarm)
        .options(joinedload(models.Swarm.agents))
        .filter(models.Swarm.id == swarm_id)
        .first()
    )
    if swarm is None:
        raise HTTPException(status_code=404, detail="Swarm not found")
    return swarm


@swarms_router.put("/swarms/{swarm_id}", response_model=schemas.Swarm)
def update_swarm(
    swarm_id: int, swarm: schemas.SwarmUpdateRequest, db: Session = Depends(get_db)
):
    db_swarm = db.query(models.Swarm).filter(models.Swarm.id == swarm_id).first()
    if db_swarm is None:
        raise HTTPException(status_code=404, detail="Swarm not found")
    for key, value in swarm.model_dump().items():
        setattr(db_swarm, key, value)
    db.commit()
    db.refresh(db_swarm)
    return db_swarm


@swarms_router.delete("/swarms/{swarm_id}", response_model=schemas.Swarm)
def delete_swarm(swarm_id: int, db: Session = Depends(get_db)):
    db_swarm = db.query(models.Swarm).filter(models.Swarm.id == swarm_id).first()
    if db_swarm is None:
        raise HTTPException(status_code=404, detail="Swarm not found")
    db.delete(db_swarm)
    db.commit()
    return db_swarm


@swarms_router.post(
    "/swarms/{swarm_id}/add_agents", response_model=schemas.SwarmAddAgentResponse
)
def add_agent_to_swarm(
    swarm_id: int, req: schemas.SwarmAddAgentRequest, db: Session = Depends(get_db)
):
    db_swarm = db.query(models.Swarm).filter(models.Swarm.id == swarm_id).first()
    if db_swarm is None:
        raise HTTPException(status_code=404, detail="Swarm not found")

    swarms_with_agents = (
        db.query(models.Swarm)
        .options(joinedload(models.Swarm.agents))
        .filter(models.Swarm.id == swarm_id)
        .first()
    )

    for agent_id in req.agent_ids:
        db_agent = db.query(models.Agent).filter(models.Agent.id == agent_id).first()
        if not db_agent:
            raise HTTPException(status_code=404, detail=f"Invalid agent id {agent_id}")

        found = False
        for agent in swarms_with_agents.agents:
            if agent.id == agent_id:
                found = True
                break

        if not found:
            swarms_with_agents.agents.append(db_agent)

    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Internal error")

    return swarms_with_agents


# CRUD for Agent
agents_router = APIRouter()


@agents_router.post("/agents/", response_model=schemas.Agent)
def create_agent(agent: schemas.AgentCreateRequest, db: Session = Depends(get_db)):
    db_agent = models.Agent(**agent.model_dump())

    try:
        db.add(db_agent)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400, detail="Agent with the given name already exists."
        )

    db.refresh(db_agent)
    return db_agent


@agents_router.get("/agents/", response_model=schemas.AgentListResponse)
def read_agents(
    cursor: Optional[int] = None, limit: int = 50, db: Session = Depends(get_db)
):
    query = db.query(models.Agent)

    if cursor:
        query = query.filter(models.Agent.id > cursor)
    agents = query.order_by(models.Agent.id).limit(limit).all()
    total_agents = db.query(models.Agent).count()

    return {
        "meta": schemas.ListMeta(
            total=total_agents,
            next_cursor=agents[-1].id if agents else None,
        ),
        "data": agents,
    }


@agents_router.put("/agents/{agent_id}", response_model=schemas.Agent)
def update_agent(
    agent_id: int, agent: schemas.AgentUpdateRequest, db: Session = Depends(get_db)
):
    db_agent = db.query(models.Agent).filter(models.Agent.id == agent_id).first()
    if db_agent is None:
        raise HTTPException(status_code=404, detail="Agent not found")
    for key, value in agent.model_dump().items():
        setattr(db_agent, key, value)
    db.commit()
    db.refresh(db_agent)
    return db_agent


api_router = APIRouter()
api_router.include_router(swarms_router, prefix="/api/v1", tags=["swarms"])
api_router.include_router(agents_router, prefix="/api/v1", tags=["agents"])
