# Python Starter

## Step 80

FastAPI: Query-Parameter, Path-Variable, POST

### Was ist neu?

Der `GET /api/hello`-Endpunkt erhält einen Namen als Parameter — entweder als Query-Parameter oder als Path-Variable. Neu hinzu kommt ein `POST`-Endpunkt mit einem JSON-Request-Body.

### Vergleich Java vs. Python

| Java (Spring Boot)           | Python (FastAPI)                              |
|------------------------------|-----------------------------------------------|
| `@RequestParam("name")`      | Parameter in Funktionssignatur: `name: str`   |
| `@PathVariable("name")`      | Platzhalter im Pfad: `"/api/hello/{name}"`    |
| `@RequestBody`               | Pydantic-Modell als Parameter: `request: GreetingRequest` |
| `@PostMapping`               | `@app.post(...)`                              |

### Query-Parameter

FastAPI erkennt Parameter automatisch als Query-Parameter, wenn sie nicht im Pfad stehen:

```python
@app.get("/api/hello")
def say_hello(name: str) -> str:
    return _greeter.greet(name)
```

Aufruf: `GET /api/hello?name=Georg`

### Path-Variable

Der Parametername im Pfad `{name}` und im Funktionsparameter müssen übereinstimmen:

```python
@app.get("/api/hello/{name}")
def say_hello_with_path_variable(name: str) -> str:
    return say_hello(name)
```

Aufruf: `GET /api/hello/Georg`

### POST mit JSON-Body

Der Request-Body wird als Pydantic-Modell definiert. FastAPI deserialisiert JSON automatisch:

```python
class GreetingRequest(BaseModel):
    name: str

@app.post("/api/hello")
def create_greeting(request: GreetingRequest) -> str:
    return _greeter.greet(request.name)
```

Aufruf: `POST /api/hello` mit Body `{"name": "Georg"}`

### Struktur

```
python0080/
├── app.py               # FastAPI-Endpunkte
├── models.py            # Pydantic-Modelle
├── greeter.py
├── greeter_service.py
├── main.py
└── tests/
    └── test_app.py
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
curl "http://localhost:8080/api/hello?name=Georg"
curl http://localhost:8080/api/hello/Georg
curl -X POST http://localhost:8080/api/hello -H "Content-Type: application/json" -d '{"name": "Georg"}'
```

### Tests ausführen

```shell
uv run pytest -v
```

Erwartete Ausgabe:

```
tests/test_app.py::test_say_hello_with_query_param PASSED
tests/test_app.py::test_say_hello_with_path_variable PASSED
tests/test_app.py::test_create_greeting_with_post PASSED

3 passed in 0.93s
```

### Typprüfung

```shell
uv run mypy .
```
