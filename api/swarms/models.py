from typing import List
from sqlalchemy import ForeignKey, Table, Column, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from database import Base


swarm_agent_association = Table(
    "swarm_agent",
    Base.metadata,
    Column("swarm_id", ForeignKey("swarm.id")),
    Column("agent_id", ForeignKey("agent.id")),
)


class Swarm(Base):
    __tablename__ = "swarm"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    agents = relationship("Agent", secondary=swarm_agent_association)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Agent(Base):
    __tablename__ = "agent"

    id: Mapped[int] = mapped_column(primary_key=True)
    name = Column(String, unique=True)
    model: Mapped[str]
    role: Mapped[str]
    instruction: Mapped[str]

    swarms = relationship(
        "Swarm", secondary=swarm_agent_association, back_populates="agents"
    )

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
