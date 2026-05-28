from collections.abc import Generator
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient
from pytest_mock import MockerFixture

from app import app, get_personen_service
from models import Person
from personen import Personen


@pytest.fixture
def mock_service(mocker: MockerFixture) -> MagicMock:
    return mocker.Mock(spec=Personen)


@pytest.fixture
def client(mock_service: MagicMock) -> Generator[TestClient, None, None]:
    app.dependency_overrides[get_personen_service] = lambda: mock_service
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_create_person_calls_service(client: TestClient, mock_service: MagicMock) -> None:
    # Arrange
    mock_service.create.return_value = Person(id=1, vorname="Hugo", name="Tester")

    # Act
    client.post("/api/person", json={"vorname": "Hugo", "name": "Tester"})

    # Assert
    mock_service.create.assert_called_once_with("Hugo", "Tester")


def test_create_person_returns_person(client: TestClient, mock_service: MagicMock) -> None:
    mock_service.create.return_value = Person(id=1, vorname="Hugo", name="Tester")
    response = client.post("/api/person", json={"vorname": "Hugo", "name": "Tester"})
    assert response.status_code == 200
    assert response.json() == {"id": 1, "vorname": "Hugo", "name": "Tester"}


def test_find_by_id_returns_person(client: TestClient, mock_service: MagicMock) -> None:
    mock_service.find_by_id.return_value = Person(id=1, vorname="Hugo", name="Tester")
    response = client.get("/api/person/1")
    assert response.status_code == 200
    assert response.json()["vorname"] == "Hugo"


def test_find_by_id_returns_404_when_not_found(client: TestClient, mock_service: MagicMock) -> None:
    mock_service.find_by_id.return_value = None
    response = client.get("/api/person/999")
    assert response.status_code == 404
