from fastapi import FastAPI, Response, requests, status, HTTPException, Depends, APIRouter
#from routers import health, users

from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import literal

from app import oauth2
from app.oauth2 import get_current_user
from app.utils import paging_set_valid
from .. import models, schemas, oauth2
from ..database import get_db

from datetime import datetime

router = APIRouter(
    prefix="/culture",
    tags=["culture"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Culture)
def create_culture(culture: schemas.CultureCreate, db: Session = Depends(get_db)):
    
    new_culture = models.Culture(**culture.model_dump())
    
    db.add(new_culture)
    db.commit()
    db.refresh(new_culture)

    return new_culture

@router.get("/active", response_model=List[schemas.Culture])
def list_culture_active(
    db: Session = Depends(get_db), 
    get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    
    month_current = datetime.now().month
    culturesActive = db.query(models.Culture).filter(
        (models.Culture.month_start >= month_current) &
        (models.Culture.month_end <= month_current)
    ).order_by(models.Culture.month_start).all()
    
    culturesFuture = db.query(models.Culture).filter(
        (models.Culture.month_end > month_current)
    ).order_by(models.Culture.month_start).limit(3).all()
    
    
    cultures = culturesActive + culturesFuture

    return cultures

@router.get("/{id}", response_model=schemas.Culture)
def get_culture(id: int, db: Session = Depends(get_db)):
    
    culture = db.query(models.Culture).filter(models.Culture.id == id).first()
    if(culture): 
        return culture
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{id} not found')
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"success":False, "msg": f'{id} not found'}
        
@router.get("/", response_model=List[schemas.Culture])
def list_culture(
    db: Session = Depends(get_db), 
    get_current_user: schemas.User = Depends(oauth2.get_current_user),
    limit:int =10,
    page:int=1):
    
    page = paging_set_valid(page)
    
    cultures = db.query(models.Culture).offset(limit*(page)).limit(limit).all()
    return cultures


@router.delete("/{id}")
def delete_culture(id: int, db: Session = Depends(get_db)):
    
    culture = db.query(models.Culture).filter(models.Culture.id == id)
    if(culture.first()): 
        culture.delete()
        db.commit()
        
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{id} not found')
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"success":False, "msg": f'{id} not found'}

@router.put("/{id}", response_model=schemas.Culture)
def update_culture(id: int, culture_update: schemas.CultureUpdate, db: Session = Depends(get_db)):
    
    culture = db.query(models.Culture).filter(models.Culture.id == id)
    if(culture.first()): 
        culture.update(culture_update.dict())
        db.commit()
        
        return culture.first()
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{id} not found')
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"success":False, "msg": f'{id} not found'}
    
