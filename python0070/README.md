# Python Starter

## Step 70

FastAPI Hello World

### Was ist neu?

Die Konsolenanwendung wird durch eine REST-API ersetzt. FastAPI ist das Python-Äquivalent zu Spring Boot — ein Web-Framework, das Endpunkte über Dekoratoren definiert und automatisch eine API-Dokumentation generiert.

### Vergleich Java vs. Python

| Java (Spring Boot)              | Python (FastAPI)                        |
|---------------------------------|-----------------------------------------|
| `@RestController`               | `app = FastAPI()`                       |
| `@RequestMapping("/api/hello")` | `@app.get("/api/hello")`                |
| `@GetMapping`                   | `@app.get(...)`                         |
| `SpringApplication.run(...)`    | `uvicorn.run("app:app", ...)`           |
| `MockMvc` / `WebMvcTest`        | `TestClient(app)`                       |

### Struktur

```
python0070/
├── app.py               # FastAPI-App (Endpunkte)
├── greeter.py           # Abstrakte Basisklasse
├── greeter_service.py   # Domain-Logik
├── main.py              # Einstiegspunkt (uvicorn)
└── tests/
    └── test_app.py
```

`HelloWorldApplication` aus den vorherigen Steps entfällt — die FastAPI-App übernimmt diese Rolle.

### Endpunkte

```python
@app.get("/api/hello")
def say_hello() -> str:
    return _greeter.greet("World")
```

Der Decorator `@app.get(...)` registriert die Funktion als HTTP-GET-Handler. Der Rückgabetyp `str` wird von FastAPI automatisch als JSON serialisiert.

### Automatische API-Dokumentation

FastAPI generiert aus den Typ-Annotationen automatisch eine interaktive Dokumentation:

- Swagger UI: http://localhost:8080/docs
- ReDoc: http://localhost:8080/redoc

### Tests mit TestClient

FastAPI stellt einen `TestClient` bereit, der HTTP-Requests direkt gegen die App ausführt — ohne laufenden Server:

```python
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_say_hello_returns_200(client: TestClient) -> None:
    response = client.get("/api/hello")
    assert response.status_code == 200
```

### Voraussetzungen

- Python 3.12+
- uv installiert

### Einrichten und Ausführen

```shell
uv sync
uv run python main.py
```

Im Browser oder curl:

```shell
curl http://localhost:8080/api/hello
```

Erwartete Antwort:

```
"Hello, World!"
```

### Tests ausführen

```shell
uv run pytest -v
```

Erwartete Ausgabe:

```
tests/test_app.py::test_say_hello_returns_200 PASSED
tests/test_app.py::test_say_hello_returns_hello_world PASSED

2 passed in 0.31s
```

### Typprüfung

```shell
uv run mypy .
```
