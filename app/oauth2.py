from datetime import datetime, timedelta, timezone
from typing import Annotated

from jose import JWTError
import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from . import schemas, database, models
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from .config import setting

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login')

#https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/?h=#update-the-dependencies  

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = setting.secret_key
ALGORITHM = setting.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = setting.access_token_expire_minutes

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp":expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encode_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id = payload.get("user_id")
        if id is None:
            raise credentials_exception
        
        user = db.query(models.User).filter(models.User.id == id).first()
        
        if not user: raise credentials_exception
        if not user.isActive: raise credentials_exception

        return user
        
        #token_data = schemas.TokenData(id=str(id))
    except InvalidTokenError:
        raise credentials_exception
    
