from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import setting

import pytest
from app.main import app

from app.database import get_db
from app.database import Base

from fastapi.testclient import TestClient

SQLALCHEMY_DATABASE_URL = setting.database_url + '_test'
engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(session):
    def override_get_db():

        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
