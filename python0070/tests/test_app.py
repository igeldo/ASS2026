import pytest
from fastapi.testclient import TestClient

from app import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def test_say_hello_returns_200(client: TestClient) -> None:
    response = client.get("/api/hello")
    assert response.status_code == 200


def test_say_hello_returns_hello_world(client: TestClient) -> None:
    response = client.get("/api/hello")
    assert response.json() == "Hello, World!"
