from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal, engine
from app import models
import pytest

client = TestClient(app)

@pytest.fixture(scope="module")
def setup_database():
    models.Base.metadata.drop_all(bind=engine)
    yield
    models.Base.metadata.drop_all(bind=engine)

def test_create_short_url(setup_database):
    response = client.post("/", json={"long_url": "https://www.youtube.com/watch?v=g7O-7rF0Hqk"})
    assert response.status_code == 200
    data = response.json()
    assert "key" in data
    assert "long_url" in data
    assert "short_url" in data
    assert data["long_url"] == "https://www.youtube.com/watch?v=g7O-7rF0Hqk"

def test_redirect_url(setup_database):
    response = client.post("/", json={"long_url": "https://www.youtube.com/watch?v=g7O-7rF0Hqk"})
    key = response.json()["key"]
    response = client.get(f"/{key}")
    assert response.status_code == 302
    assert response.headers["location"] == "https://www.youtube.com/watch?v=g7O-7rF0Hqk"

def test_delete_url(setup_database):
    response = client.post("/", json={"long_url": "https://www.youtube.com/watch?v=g7O-7rF0Hqk"})
    key = response.json()["key"]
    response = client.delete(f"/{key}")
    assert response.status_code == 200
    response = client.get(f"/{key}")
    assert response.status_code == 404