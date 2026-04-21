from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_tracks_list():
    res = client.get("/api/v1/tracks")
    assert res.status_code == 200
