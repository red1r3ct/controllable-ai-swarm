from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional

from database import get_db
import tasks.models as models
import tasks.schemas as schemas
from projects.models import Project


# CRUD for Tasks
tasks_router = APIRouter()


@tasks_router.post("/tasks/", response_model=schemas.Task)
def create_task(task: schemas.TaskCreateRequest, db: Session = Depends(get_db)):
    db_task = models.Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


@tasks_router.get("/tasks/{task_id}", response_model=schemas.Task)
def read_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@tasks_router.put("/tasks/{task_id}", response_model=schemas.Task)
def update_task(
    task_id: int, task: schemas.TaskUpdateRequest, db: Session = Depends(get_db)
):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    for key, value in task.model_dump().items():
        setattr(db_task, key, value)
    db.commit()
    return db_task


@tasks_router.delete("/tasks/{task_id}", response_model=schemas.Task)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return task


@tasks_router.get(
    "/projects/{project_id}/tasks/", response_model=schemas.TaskListResponse
)
def list_tasks(
    project_id: int,
    cursor: Optional[int] = None,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    query = db.query(models.Task).filter(Project.id == project_id)
    if cursor:
        query = query.filter(models.Task.id > cursor)
    tasks = query.order_by(models.Task.id).limit(limit).all()
    total_tasks = db.query(models.Task).filter(Project.id == project_id).count()

    return {
        "meta": schemas.ListMeta(
            total=total_tasks,
            next_cursor=tasks[-1].id if tasks else None,
        ),
        "data": tasks,
    }


api_router = APIRouter()
api_router.include_router(tasks_router, prefix="/api/v1", tags=["tasks"])
