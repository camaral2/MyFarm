from fastapi import FastAPI, Response, requests, status, HTTPException, Depends, APIRouter
from typing import List
from sqlalchemy.orm import Session

from app import oauth2
from app.utils import paging_set_valid
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/event_culture",
    tags=["event_culture"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Event_Culture)
def create_event_culture(
    event_culture: schemas.Event_CultureCreate, 
    db: Session = Depends(get_db),
    get_current_user: schemas.User = Depends(oauth2.get_current_user)
    ):
    
    new_event_culture = models.Event_Culture(user_id= get_current_user.id, **event_culture.model_dump())
    
    db.add(new_event_culture)
    db.commit()
    db.refresh(new_event_culture)

    return new_event_culture

@router.get("/", response_model=List[schemas.Event_Culture])
def list_event_culture(
    db: Session = Depends(get_db), 
    get_current_user: schemas.User = Depends(oauth2.get_current_user),
    limit:int =10,
    page:int=1):
    
    page = paging_set_valid(page)
    
    event_cultures = db.query(models.Event_Culture).offset(limit*(page)).limit(limit).all()
    return event_cultures
