import pytest
from fastapi.testclient import TestClient

from app import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def test_say_hello_with_query_param(client: TestClient) -> None:
    response = client.get("/api/hello?name=Georg")
    assert response.status_code == 200
    assert response.json() == "Hello, Georg!"


def test_say_hello_with_path_variable(client: TestClient) -> None:
    response = client.get("/api/hello/Georg")
    assert response.status_code == 200
    assert response.json() == "Hello, Georg!"


def test_create_greeting_with_post(client: TestClient) -> None:
    response = client.post("/api/hello", json={"name": "Georg"})
    assert response.status_code == 200
    assert response.json() == "Hello, Georg!"
