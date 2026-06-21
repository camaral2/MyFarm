from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import setting

SQLALCHEMY_DATABASE_URL = setting.database_url

if not SQLALCHEMY_DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL nao configurada. Defina DATABASE_URL nas variaveis de ambiente da Vercel."
    )

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    
    try:
        yield db
    finally:
        db.close()
