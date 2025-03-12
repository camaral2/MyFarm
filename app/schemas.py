from pydantic import BaseModel
from typing import Optional
from datetime import datetime

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
