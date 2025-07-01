# Charger les librairies nécessaires
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"..", "..")))

from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_login_success():
    response = client.post(
        "/auth/login",
        data={"username": "dataqueen", "password": "superpassword"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_failure():
    response = client.post(
        "/auth/login",
        data={"username": "wrong", "password": "wrong"}
    )
    assert response.status_code == 401
