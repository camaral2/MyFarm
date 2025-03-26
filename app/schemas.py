from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime, date

class CultureBase(BaseModel):
    name: str
    month_start: Optional[int] = 0
    month_end: Optional[int] = 0
    isActive: Optional[bool] = True

class CultureCreate(CultureBase):
    pass

class CultureUpdate(CultureBase):
    pass

class Culture(CultureBase):
    id: int    
    created_at: datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str  
    isActive: Optional[bool] = True

class User(BaseModel):
    id: int    
    email: EmailStr
    created_at: datetime
    isActive: bool
    
# class UserLogin(BaseModel):
#     email: EmailStr
#     password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user: User
    
class TokenData(BaseModel):
    id: Optional[str] = None
    
class Event_CultureBase(BaseModel):
    event: str
    mode: Optional[int] = 2
    detail: Optional[str] = ""
    pass

class Event_CultureCreate(Event_CultureBase):
    culture_id: int    
    date: Optional[datetime] = None
    
class Event_Culture(Event_CultureBase):
    id: int
    date: date
    created_at: datetime
    user: User
    culture: Culture