from fastapi import FastAPI, Response, requests, status, HTTPException, Depends
#from routers import health, users

from typing import List

from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

# Include routers
#app.include_router(health.router)

@app.get("/")
def root():
    return {"message": "Welcome To !"}

@app.post("/culture/", status_code=status.HTTP_201_CREATED, response_model=schemas.Culture)
def create_post(culture: schemas.CultureCreate, db: Session = Depends(get_db)):
    
    try:
        new_culture = models.Culture(**culture.dict())
        
        db.add(new_culture)
        db.commit()
        db.refresh(new_culture)
    
        return new_culture
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)  

@app.get("/culture/{id}", response_model=schemas.Culture)
def get_culture(id: int, db: Session = Depends(get_db)):
    
    culture = db.query(models.Culture).filter(models.Culture.id == id).first()
    if(culture): 
        return culture
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{id} not found')
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"success":False, "msg": f'{id} not found'}
        
@app.get("/culture/", response_model=List[schemas.Culture])
def list_culture(db: Session = Depends(get_db)):
    cultures = db.query(models.Culture).all()
    return cultures

@app.delete("/culture/{id}")
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

@app.put("/culture/{id}", response_model=schemas.Culture)
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
    