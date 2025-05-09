
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Global state
test_user = {"username": "testuser", "password": "testpass"}
token = ""

def test_register():
    response = client.post("/auth/register", json=test_user)
    assert response.status_code in [200, 400]  # 400 if already exists

def test_login():
    global token
    response = client.post("/auth/login", json=test_user)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    token = data["access_token"]

def test_input_pemakaian():
    global token
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "obat_id": 1,
        "jumlah": 100,
        "bulan": "2024-04-01"
    }
    response = client.post("/pemakaian", json=data, headers=headers)
    assert response.status_code in [200, 422]  # 422 if obat_id not exists

def test_get_pemakaian():
    response = client.get("/pemakaian")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_forecast():
    response = client.get("/forecast")
    assert response.status_code == 200
    assert "forecast" in response.json()
