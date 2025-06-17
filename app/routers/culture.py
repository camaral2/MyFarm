from fastapi import FastAPI, Response, requests, status, HTTPException, Depends, APIRouter
#from routers import health, users

from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from psycopg2.errors import UniqueViolation  # PostgreSQL-specific error

from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import literal

from app import oauth2
from app.oauth2 import get_current_user
from app.utils.utils import paging_set_valid
from .. import models, schemas, oauth2
from ..database import get_db

from datetime import datetime

router = APIRouter(
    prefix="/culture",
    tags=["culture"]
)

def events_for_culture(culture, db):
    # Find the earliest '0-Start' event for this culture
    start_event = db.query(models.Event_Culture).filter(
        models.Event_Culture.culture_id == culture.id,
        models.Event_Culture.mode == 0
    ).order_by(models.Event_Culture.date.asc()).first()

    status = 0

    if start_event:
        # Check if there's a '2-End' event after the start event
        end_event_exists = db.query(models.Event_Culture).filter(
            models.Event_Culture.culture_id == culture.id,
            models.Event_Culture.mode == 2,
            models.Event_Culture.date > start_event.date
        ).first() is not None
        
        status = 2 if end_event_exists else 1
        
    # Convert culture to dict and add status
    culture_dict = {c.name: getattr(culture, c.name) for c in culture.__table__.columns}
    culture_dict['status'] = status

    return culture_dict

def events_for_cultures(cultures, db):
    result = []
    
    for culture in cultures:
        culture_dict = events_for_culture(culture = culture, db = db)
        result.append(culture_dict)  
        
    return result  

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Culture)
def create_culture(
    culture: schemas.CultureCreate, 
    db: Session = Depends(get_db),
    get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    
    try:
        new_culture = models.Culture(**culture.model_dump())
        
        db.add(new_culture)
        db.commit()
        db.refresh(new_culture)

        return new_culture
    
    except IntegrityError as e:
        db.rollback()
        
        
        if isinstance(e.orig, UniqueViolation):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,  # 409 Conflict is standard for duplicates
                detail={
                    "error": "Duplicate entry",
                    "message": "This record already exists"
                }
            )
            
        # Handle other IntegrityError cases (foreign key, etc.)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "Database integrity error",
                "message": str(e.orig) if e.orig else str(e),
                "type": "integrity_error"
            }
        )
        
    except SQLAlchemyError as e:
        db.rollback()
        
        print('Error_1:' + str(e))
        # Handle other SQLAlchemy errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "Database operation failed",
                "message": str(e),
                "type": "database_error"
            }
        )
        
    except Exception as e:
        db.rollback()
        print('Error_2:' + str(e))
        
        # Handle any other unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "Internal server error",
                "message": str(e),
                "type": "unexpected_error"
            }
        )

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
    
    return events_for_cultures(cultures=cultures, db=db)


@router.get("/{id}", response_model=schemas.Culture)
def get_culture(id: int, db: Session = Depends(get_db),
    get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    
    culture = db.query(models.Culture).filter(models.Culture.id == id).first()
    if(culture): 
        return events_for_culture(culture = culture, db=db)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{id} not found')
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"success":False, "msg": f'{id} not found'}


#    get_current_user: schemas.User = Depends(oauth2.get_current_user),
        
@router.get("/", response_model=List[schemas.Culture])
def list_culture(
    db: Session = Depends(get_db), 
    limit:int =200,
    page:int=1,
    get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    
    page = paging_set_valid(page)
    
    cultures = db.query(models.Culture).order_by(models.Culture.name).offset(limit*(page)).limit(limit).all()
    
    return events_for_cultures(cultures=cultures, db=db)


@router.delete("/{id}")
def delete_culture(id: int, db: Session = Depends(get_db),
    get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    
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
def update_culture(
    id: int, 
    culture_update: schemas.CultureUpdate, 
    db: Session = Depends(get_db),
    get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    
    culture = db.query(models.Culture).filter(models.Culture.id == id)
    if(culture.first()): 
        culture.update(culture_update.model_dump())
        db.commit()
        
        return culture.first()
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{id} not found')
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"success":False, "msg": f'{id} not found'}
