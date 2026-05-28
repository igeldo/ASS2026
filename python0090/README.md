# Python Starter

## Step 90

FastAPI: Dependency Injection

### Was ist neu?

FastAPI hat ein eingebautes Dependency-Injection-System. Abhängigkeiten werden nicht direkt instanziiert, sondern über `Depends()` als Parameter übergeben — das Python-Äquivalent zu Springs Constructor Injection.

### Vergleich Java vs. Python

| Java (Spring)                        | Python (FastAPI)                                  |
|--------------------------------------|---------------------------------------------------|
| `@Service` + Constructor Injection   | Funktion mit `Depends()`                          |
| `@Autowired`                         | `Annotated[ServiceType, Depends(get_service)]`    |
| `@Mock` + `@InjectMocks` (Mockito)   | `app.dependency_overrides[get_service] = lambda: fake` |

### Dependency-Funktion

Eine normale Python-Funktion liefert die Abhängigkeit:

```python
def get_personen_service() -> Personen:
    return _service
```

### Depends im Endpunkt

`Annotated` + `Depends` verbinden den Parameter mit der Dependency-Funktion:

```python
PersonenDep = Annotated[Personen, Depends(get_personen_service)]

@app.post("/api/person")
def create_person(request: PersonRequest, service: PersonenDep) -> Person:
    return service.create(request.vorname, request.name)
```

FastAPI erkennt `Depends` und ruft `get_personen_service()` automatisch auf.

### Dependency Override in Tests

In Tests wird die echte Implementierung durch eine Fake-Implementierung ersetzt:

```python
@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    app.dependency_overrides[get_personen_service] = lambda: FakePersonenService()
    yield TestClient(app)
    app.dependency_overrides.clear()
```

`dependency_overrides` ist das FastAPI-Äquivalent zu Mockitos `@InjectMocks` — kein Framework-Magie, sondern explizites Ersetzen.

### Struktur

```
python0090/
├── app.py               # Endpunkte mit Depends
├── models.py            # PersonRequest, Person (Pydantic)
├── personen.py          # Abstrakte Basisklasse
├── personen_service.py  # In-Memory-Implementierung
├── main.py
└── tests/
    └── test_app.py      # FakePersonenService + dependency_overrides
```

### Voraussetzungen

- Python 3.12+
- uv installiert

### Einrichten und Ausführen

```shell
uv sync
uv run python main.py
```

```shell
curl -X POST http://localhost:8080/api/person \
  -H "Content-Type: application/json" \
  -d '{"vorname": "Hugo", "name": "Tester"}'

curl http://localhost:8080/api/person/1
```

### Tests ausführen

```shell
uv run pytest -v
```

Erwartete Ausgabe:

```
tests/test_app.py::test_create_person_returns_person PASSED
tests/test_app.py::test_find_by_id_returns_person PASSED
tests/test_app.py::test_find_by_id_returns_404_when_not_found PASSED

3 passed in 0.95s
```

### Typprüfung

```shell
uv run mypy .
```
