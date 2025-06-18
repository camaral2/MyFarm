import pytest
from app.main import app

from app.database import get_db
from app.database import Base

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import setting

from fastapi.testclient import TestClient
from app.oauth2 import create_access_token

from app import models
from app.utils.utils import has_password

SQLALCHEMY_DATABASE_URL = setting.database_url + '_test'
engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

class User:
    email = 'cristian_amaral@hotmail.com'
    password = '12345'
    
@pytest.fixture()
def user():
    return User

@pytest.fixture()
def session():
    print("my session fixture ran")
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
    
@pytest.fixture
def test_user(session, user):
    new_has_password = has_password(user.password)
    newUser = models.User(email=user.email, password=new_has_password)
    session.add(newUser)
    session.commit()
    session.refresh(newUser)

    newUser.password = new_has_password
    return newUser    

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user.id})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client