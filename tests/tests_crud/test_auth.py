# Charger les librairies nécessaires
import os
import sys
from uuid import uuid4

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"..", "..")))

from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)

def test_login_success():
    email = f"test_{uuid4().hex[:10]}@example.com"
    password = "superpassword"

    register_response = client.post(
        "/api/v1/auth/register",
        json={"name": "Data Queen", "email": email, "password": password, "role": "user"}
    )
    assert register_response.status_code == 200

    response = client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": password}
    )
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["data"][0]["access_token"]

def test_login_failure():
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "wrong@gmail.com", "password": "wrong"}
    )
    assert response.status_code == 401
