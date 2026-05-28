from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

from app import app, get_personen_service
from models import Person
from personen import Personen


class FakePersonenService(Personen):
    def __init__(self) -> None:
        self._store: dict[int, Person] = {}
        self._next_id: int = 1

    def create(self, vorname: str, name: str) -> Person:
        person = Person(id=self._next_id, vorname=vorname, name=name)
        self._store[self._next_id] = person
        self._next_id += 1
        return person

    def find_by_id(self, id: int) -> Person | None:
        return self._store.get(id)


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    fake = FakePersonenService()
    app.dependency_overrides[get_personen_service] = lambda: fake
    yield TestClient(app)
    app.dependency_overrides.clear()


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
