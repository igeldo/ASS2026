# Hello World REST Service

Ein einfacher REST-Service auf Basis von FastAPI.

## Anforderungen

- `GET /api/hello` antwortet mit `Hello World!`
- `GET /api/hello?name={name}` antwortet mit `Hello {name}!`

## Voraussetzungen

- Python 3.x
- Virtuelles Environment mit den installierten Abhängigkeiten

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Starten

```bash
source venv/bin/activate
uvicorn main:app --reload
```

Der Service startet auf Port `8000`.

## Endpoints

| Methode | URL                          | Antwort          |
|---------|------------------------------|------------------|
| GET     | `/api/hello`                 | `Hello World!`   |
| GET     | `/api/hello?name={name}`     | `Hello {name}!`  |

## Beispiele

```bash
curl http://localhost:8000/api/hello
# "Hello World!"

curl "http://localhost:8000/api/hello?name=Georg"
# "Hello Georg!"
```

## API-Dokumentation

FastAPI stellt automatisch eine interaktive Swagger-Dokumentation bereit:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
