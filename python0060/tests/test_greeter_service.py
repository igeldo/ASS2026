import pytest

from greeter_service import GreeterService


@pytest.fixture
def cut() -> GreeterService:
    return GreeterService()


def test_greet_returns_hello_georg(cut: GreeterService) -> None:
    # Arrange
    name = "Georg"

    # Act
    result = cut.greet(name)

    # Assert
    assert result == "Hello, Georg!"

def test_greet_returns_hello_hugo(cut: GreeterService) -> None:
    # Arrange
    name = "Hugo"

    # Act
    result = cut.greet(name)

    # Assert
    assert result == "Hello, Hugo!"

class TestGivenNameIsGeorg:
    def test_result_is_not_none(self, cut: GreeterService) -> None:
        assert cut.greet("Georg") is not None

    def test_result_contains_hello(self, cut: GreeterService) -> None:
        assert "Hello" in cut.greet("Georg")

    def test_result_is_hello_georg(self, cut: GreeterService) -> None:
        assert cut.greet("Georg") == "Hello, Georg!"
