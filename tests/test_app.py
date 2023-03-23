import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from src.database import Base
from src.dependencies import get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture()
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_create_short_url(mocker, test_db):
    mocker.patch("src.crud.generate_id", return_value="12345678")

    response = client.post("/create/", json={"original_url": "example.com"})
    assert response.status_code == 201
    assert response.json() == {"url": "https://short.ly/12345678"}

    response = client.get("/12345678", follow_redirects=False)
    print(dir(response))
    assert response.status_code == 307


def test_get_original_url_failed(test_db):
    response = client.get("/12345678")
    assert response.status_code == 404
    assert response.json() == {"detail": "URL not found"}
