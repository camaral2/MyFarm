from fastapi import FastAPI, Response, requests, status, HTTPException, Depends, APIRouter
#from routers import health, users

from typing import List

from sqlalchemy.orm import Session

from app import oauth2

from ..utils import utils
from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/user",
    tags=["user"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db),
    get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    
    try:
        user.password = utils.has_password(user.password)
        
        new_user = models.User(**user.dict())
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    
        return new_user
    except requests.exceptions.HTTPException as err:
        raise HTTPException(detail=err)  
    
@router.get("/{id}", response_model=schemas.User)
def get_user(id: int, db: Session = Depends(get_db),
    get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    
    user = db.query(models.User).filter(models.User.id == id).first()
    if(user): 
        return user
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{id} not found')
        