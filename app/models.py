from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Date
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base
from sqlalchemy.orm import relationship

class Culture(Base):
    __tablename__ = 'culture'
    
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False, unique=True)
    month_start = Column(Integer, nullable=False, server_default='0')
    month_end = Column(Integer, nullable=False, server_default='0')
    isActive = Column(Boolean, nullable=False, server_default='TRUE')
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    
class User(Base):
    __tablename__ = 'user'
    
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    isActive = Column(Boolean, nullable=False, server_default='TRUE')
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    phone = Column(String)
    
class Event_Culture(Base):
    __tablename__ = 'event_culture'
    
    id = Column(Integer, primary_key=True, nullable=False)
    culture_id = Column(Integer, ForeignKey("culture.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    date = Column(Date, nullable=False, server_default=text('now()'))
    event = Column(String, nullable=False)
    mode = Column(Integer, nullable=False, server_default=text('2'))
    detail = Column(String)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    user = relationship("User")
    culture = relationship("Culture")
    