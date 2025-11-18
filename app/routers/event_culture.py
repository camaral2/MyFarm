from fastapi import FastAPI, Response, requests, status, HTTPException, Depends, APIRouter
from typing import List
from sqlalchemy.orm import Session

from app import oauth2
from app.utils.utils import paging_set_valid
from .. import models, schemas, oauth2
from ..database import get_db
from ..utils.decorators import db_safe

router = APIRouter(
    prefix="/event_culture",
    tags=["event_culture"]
)

@db_safe
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

@router.get("/{idculture}", response_model=List[schemas.Event_Culture])
def list_event_culture(
    idculture: int,
    db: Session = Depends(get_db), 
    get_current_user: schemas.User = Depends(oauth2.get_current_user),
    limit:int =10,
    page:int=1):
    
    page = paging_set_valid(page)
    
    event_cultures = db.query(models.Event_Culture).filter(models.Event_Culture.culture_id==idculture).order_by(models.Event_Culture.date.desc()).offset(limit*(page)).limit(limit).all()
    return event_cultures

@router.get("/item/{id}", response_model=schemas.Event_Culture)
def item_event_culture(
    id: int,
    db: Session = Depends(get_db), 
    get_current_user: schemas.User = Depends(oauth2.get_current_user)):

    event_culture = db.query(models.Event_Culture).filter(models.Event_Culture.id == id).first()
    if(event_culture): 
        return event_culture
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{id} not found')


@db_safe
@router.delete("/{id}")
def delete_event_culture(id: int, db: Session = Depends(get_db),
    get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    
    event_culture = db.query(models.Event_Culture).filter(models.Event_Culture.id == id)
    if(event_culture.first()): 
        event_culture.delete()
        db.commit()
        
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{id} not found')


@router.put("/{id}", response_model=schemas.Event_Culture)
def update_event_culture(
    id: int, 
    event_culture_update: schemas.Event_CultureUpdate, 
    db: Session = Depends(get_db),
    get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    
    event_culture = db.query(models.Event_Culture).filter(models.Event_Culture.id == id)
    if(event_culture.first()): 
        event_culture.update(event_culture_update.model_dump())
        db.commit()
        
        return event_culture.first()
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{id} not found')
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"success":False, "msg": f'{id} not found'}