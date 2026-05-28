from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app import app
from database import get_session
from orm_models import Base

test_engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestSessionLocal = sessionmaker(bind=test_engine)


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    Base.metadata.create_all(test_engine)

    def override_get_session() -> Generator[Session, None, None]:
        with TestSessionLocal() as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session
    yield TestClient(app)
    app.dependency_overrides.clear()
    Base.metadata.drop_all(test_engine)


def test_create_person_returns_person(client: TestClient) -> None:
    response = client.post("/api/person", json={"vorname": "Hugo", "name": "Tester"})
    assert response.status_code == 200
    assert response.json()["vorname"] == "Hugo"
    assert response.json()["name"] == "Tester"
    assert response.json()["id"] == 1


def test_find_by_id_returns_person(client: TestClient) -> None:
    client.post("/api/person", json={"vorname": "Hugo", "name": "Tester"})
    response = client.get("/api/person/1")
    assert response.status_code == 200
    assert response.json()["vorname"] == "Hugo"


def test_find_by_id_returns_404_when_not_found(client: TestClient) -> None:
    response = client.get("/api/person/999")
    assert response.status_code == 404
