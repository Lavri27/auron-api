from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_register_login():
    res = client.post("/api/v1/auth/register", json={
        "email": "test@test.com",
        "username": "test",
        "password": "123456"
    })
    assert res.status_code == 201

    res = client.post("/api/v1/auth/login", json={
        "email": "test@test.com",
        "password": "123456"
    })
    assert res.status_code == 200
    assert "access_token" in res.json()
