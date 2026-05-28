# Python Starter

## Step 70

FastAPI Hello World

### Was ist neu?

Die Konsolenanwendung wird durch eine REST-API ersetzt. FastAPI ist das Python-Äquivalent zu Spring Boot — ein Web-Framework, das Endpunkte über Dekoratoren definiert und automatisch eine API-Dokumentation generiert.

### Vergleich Java vs. Python

| Java (Spring Boot)              | Python (FastAPI)                          |
|---------------------------------|-------------------------------------------|
| `@RestController`               | Klasse mit `APIRouter`                    |
| `@RequestMapping("/api/hello")` | `router.add_api_route("/api/hello", ...)` |
| `@GetMapping`                   | `methods=["GET"]`                         |
| `SpringApplication.run(...)`    | `uvicorn.run("app:app", ...)`             |
| `MockMvc` / `WebMvcTest`        | `TestClient(app)`                         |

### Struktur

```
python0070/
├── app.py                  # Kompositions-Root (FastAPI + Router)
├── hello_world_router.py   # HTTP-Endpunkte (analog zu @RestController)
├── greeter.py              # Abstrakte Basisklasse
├── greeter_service.py      # Domain-Logik
├── main.py                 # Einstiegspunkt (uvicorn)
└── tests/
    └── test_app.py
```

`HelloWorldApplication` aus den vorherigen Steps entfällt — die FastAPI-App übernimmt diese Rolle.

### Router-Klasse

Endpunkte werden in einer eigenen Klasse gebündelt, analog zu Javas `@RestController`:

```python
class HelloWorldRouter:
    def __init__(self, greeter: Greeter) -> None:
        self._greeter = greeter
        self.router = APIRouter()
        self.router.add_api_route("/api/hello", self.say_hello, methods=["GET"])

    def say_hello(self) -> str:
        return self._greeter.greet("World")
```

`app.py` bleibt als dünne Kompositions-Root:

```python
app = FastAPI()
app.include_router(HelloWorldRouter(GreeterService()).router)
```

Der Rückgabetyp `str` wird von FastAPI automatisch als JSON serialisiert.

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
