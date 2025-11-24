from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/cost_credit",
    tags=["Cost & Credit"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Cost_Credit_Culture)
def create_cost_credit(
    cost_credit: schemas.Cost_Credit_CultureCreate, 
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user)):

    new_cost_credit = models.Cost_Credit_Culture(**cost_credit.model_dump())
    db.add(new_cost_credit)
    db.commit()
    db.refresh(new_cost_credit)

    return new_cost_credit

@router.get("/", response_model=List[schemas.Cost_Credit_Culture])
def get_cost_credits(
    db: Session = Depends(get_db), 
    current_user: schemas.User = Depends(oauth2.get_current_user),
    limit: int = 10, 
    skip: int = 0,
    search: Optional[str] = ""):

    results = db.query(models.Cost_Credit_Culture).filter(
        models.Cost_Credit_Culture.description.contains(search)).limit(limit).offset(skip).all()
    return results

@router.get("/{id}", response_model=schemas.Cost_Credit_Culture)
def get_cost_credit(
    id: int, 
    db: Session = Depends(get_db), 
    current_user: schemas.User = Depends(oauth2.get_current_user)):

    cost_credit = db.query(models.Cost_Credit_Culture).filter(models.Cost_Credit_Culture.id == id).first()

    if not cost_credit:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Cost/Credit with id: {id} was not found")

    return cost_credit

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cost_credit(
    id: int, 
    db: Session = Depends(get_db), 
    current_user: schemas.User = Depends(oauth2.get_current_user)):

    cost_credit_query = db.query(models.Cost_Credit_Culture).filter(models.Cost_Credit_Culture.id == id)

    cost_credit = cost_credit_query.first()

    if cost_credit == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Cost/Credit with id: {id} does not exist")

    cost_credit_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Cost_Credit_Culture)
def update_cost_credit(
    id: int, 
    updated_cost_credit: schemas.Cost_Credit_CultureCreate, 
    db: Session = Depends(get_db), 
    current_user: schemas.User = Depends(oauth2.get_current_user)):

    cost_credit_query = db.query(models.Cost_Credit_Culture).filter(models.Cost_Credit_Culture.id == id)

    cost_credit = cost_credit_query.first()

    if cost_credit == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Cost/Credit with id: {id} does not exist")

    cost_credit_query.update(updated_cost_credit.model_dump(), synchronize_session=False)

    db.commit()

    return cost_credit_query.first()
