# Python Starter

## Step 100

Mocking in Tests mit pytest-mock

### Was ist neu?

Statt einer Fake-Implementierung aus dem vorherigen Step wird jetzt ein Mock-Objekt verwendet. `pytest-mock` ist das Python-Äquivalent zu Mockito.

### Vergleich Java vs. Python

| Java (Mockito)                              | Python (pytest-mock)                              |
|---------------------------------------------|---------------------------------------------------|
| `@Mock Personen personen`                   | `mocker.Mock(spec=Personen)`                      |
| `given(personen.create(...)).willReturn(x)` | `mock_service.create.return_value = x`            |
| `verify(personen).create("Hugo", "Tester")` | `mock_service.create.assert_called_once_with(...)` |
| `@InjectMocks PersonController cut`         | `app.dependency_overrides[get_personen_service] = lambda: mock_service` |

### Mock erstellen

`mocker` ist ein pytest-Fixture von `pytest-mock`. `spec=Personen` stellt sicher, dass der Mock nur Methoden hat, die in `Personen` definiert sind:

```python
@pytest.fixture
def mock_service(mocker: MockerFixture) -> MagicMock:
    return mocker.Mock(spec=Personen)
```

### Return-Wert festlegen

```python
mock_service.create.return_value = Person(id=1, vorname="Hugo", name="Tester")
```

### Aufruf verifizieren

```python
mock_service.create.assert_called_once_with("Hugo", "Tester")
```

### Mock in FastAPI injizieren

Der Mock wird über `dependency_overrides` in die App eingehängt:

```python
@pytest.fixture
def client(mock_service: MagicMock) -> Generator[TestClient, None, None]:
    app.dependency_overrides[get_personen_service] = lambda: mock_service
    yield TestClient(app)
    app.dependency_overrides.clear()
```

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
uv run pytest -v
```

Erwartete Ausgabe:

```
tests/test_app.py::test_create_person_calls_service PASSED
tests/test_app.py::test_create_person_returns_person PASSED
tests/test_app.py::test_find_by_id_returns_person PASSED
tests/test_app.py::test_find_by_id_returns_404_when_not_found PASSED

4 passed in 0.96s
```

### Typprüfung

```shell
uv run mypy .
```
