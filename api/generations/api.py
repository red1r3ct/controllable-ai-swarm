from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from database import get_db
import swarms.models as models
import swarms.schemas as schemas

router = APIRouter()


api_router = APIRouter()
api_router.include_router(router, prefix="/api/v1", tags=["generations"])
