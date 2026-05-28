# Python Starter

## Step 60

Tests mit pytest

### Was ist neu?

Python verwendet `pytest` als Standard-Testframework — das Python-Äquivalent zu JUnit 5 in Java.

### Vergleich Java vs. Python

| Java (JUnit 5)                  | Python (pytest)                          |
|---------------------------------|------------------------------------------|
| `@Test`                         | Funktion oder Methode beginnt mit `test_` |
| `@BeforeEach`                   | `@pytest.fixture` — wird als Parameter übergeben |
| Klassen ohne Vererbung möglich  | Klassen beginnen mit `Test`              |
| `assertThat(x).isEqualTo(y)`   | `assert x == y`                          |
| `assertThat(x).isNotNull()`    | `assert x is not None`                  |
| `assertThat(x).contains(y)`    | `assert y in x`                          |

### Fixtures

Fixtures ersetzen `@BeforeEach` — sie erstellen Testdaten oder Objekte und werden per Parameter übergeben:

```python
@pytest.fixture
def cut() -> GreeterService:
    return GreeterService()

def test_greet_returns_hello_georg(cut: GreeterService) -> None:
    result = cut.greet("Georg")
    assert result == "Hello, Georg!"
```

pytest erkennt, dass `cut` eine Fixture ist, und ruft sie vor dem Test auf. Der Typ-Hint `cut: GreeterService` macht die Abhängigkeit für mypy sichtbar.

### Arrange / Act / Assert

Das bewährte Muster für strukturierte Tests:

```python
def test_greet_returns_hello_georg(cut: GreeterService) -> None:
    # Arrange
    name = "Georg"

    # Act
    result = cut.greet(name)

    # Assert
    assert result == "Hello, Georg!"
```

### Struktur

```
python0060/
├── greeter.py
├── greeter_service.py
├── hello_world_application.py
├── main.py
└── tests/
    └── test_greeter_service.py
```

Tests liegen im Unterverzeichnis `tests/`. pytest findet sie automatisch über die Konfiguration in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["."]
```

`pythonpath = ["."]` sorgt dafür, dass pytest die Quell-Dateien im Wurzelverzeichnis importieren kann.

### Voraussetzungen

- Python 3.12+
- uv installiert

### Einrichten und Ausführen

```shell
uv sync
uv run python main.py
```

### Tests ausführen

```shell
uv run pytest
```

Erwartete Ausgabe:

```
collected 4 items

tests/test_greeter_service.py ....                                   [100%]

4 passed in 0.01s
```

Mit Details:

```shell
uv run pytest -v
```

```
tests/test_greeter_service.py::test_greet_returns_hello_georg PASSED
tests/test_greeter_service.py::TestGivenNameIsGeorg::test_result_is_not_none PASSED
tests/test_greeter_service.py::TestGivenNameIsGeorg::test_result_contains_hello PASSED
tests/test_greeter_service.py::TestGivenNameIsGeorg::test_result_is_hello_georg PASSED
```

### Typprüfung

```shell
uv run mypy .
```
