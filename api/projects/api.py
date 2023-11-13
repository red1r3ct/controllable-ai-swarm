from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from typing import Optional
from database import get_db
import projects.models as models
import projects.schemas as schemas

router = APIRouter()


@router.post("/projects/", response_model=schemas.Project)
def create_project(
    project: schemas.ProjectCreateRequest, db: Session = Depends(get_db)
):
    db_project = models.Project(**project.model_dump())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


@router.get("/projects/{project_id}", response_model=schemas.Project)
def read_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.delete("/project/{project_id}", response_model=schemas.Project)
def delete_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(project)
    db.commit()
    return project


@router.get("/projects/", response_model=schemas.ProjectListResponse)
def list_projects(
    cursor: Optional[int] = None, limit: int = 10, db: Session = Depends(get_db)
):
    query = db.query(models.Project)
    if cursor:
        query = query.filter(models.Project.id > cursor)
    projects = query.order_by(models.Project.id).limit(limit).all()
    total_projects = db.query(models.Project).count()

    return {
        "meta": schemas.ListMeta(
            total=total_projects,
            next_cursor=projects[-1].id if projects else None,
        ),
        "data": projects,
    }


api_router = APIRouter()
api_router.include_router(router, prefix="/api/v1", tags=["projects"])
