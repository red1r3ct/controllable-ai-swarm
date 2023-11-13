from sqlalchemy import Column, Integer, String, DateTime, ARRAY, ForeignKey
from datetime import datetime
from enum import Enum as PyEnum

from database import Base


class Task(Base):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True)
    status = Column(String, index=True)
    name = Column(String)
    description = Column(String)
    log = Column(ARRAY(String))

    project_id = Column(Integer, ForeignKey("project.id"), index=True)

    author = Column(String)
    assignee = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
