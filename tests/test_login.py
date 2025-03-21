from app.config import setting
import pytest
from jose import jwt

def test_login(client, test_user, user):
    login_data = {
        "username": user.email,
        "password": user.password
    }
    
    login_response = client.post("/login", data=login_data)
    assert login_response.status_code == 200, "Login failed"
    
    token = login_response.json().get("access_token") 
    assert token is not None, "Token not found in login response"

    token_type = login_response.json().get("token_type") 
    assert token_type is not None, "Token Type not found in login response"
    assert token_type == "bearer", "Token Type is empty"

    payload = jwt.decode(token, setting.secret_key, algorithms=[setting.algorithm])
    
    id = payload.get("user_id")
    assert id == test_user.id
    
@pytest.mark.parametrize("email, password, status_code", [
    ('dontexists@gmail.com', 'password123', 403),
    ('john@gmail.com', 'wrongpassword', 403),
    ('wrongemail@gmail.com', 'wrongpassword', 403),
    (None, 'password123', 422),
    ('john@gmail.com', None, 422)
])
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post(
        "/login", data={"username": email, "password": password})

    assert res.status_code == status_code
    
    
