# Python Starter

## Step 110

SQLAlchemy + PostgreSQL

### Was ist neu?

Der In-Memory-Store wird durch eine echte PostgreSQL-Datenbank ersetzt. SQLAlchemy ist das Python-Äquivalent zu JPA/Hibernate — ein ORM, das Python-Klassen auf Datenbanktabellen abbildet.

### Vergleich Java vs. Python

| Java (JPA/Spring Data)               | Python (SQLAlchemy 2.0)                    |
|--------------------------------------|--------------------------------------------|
| `@Entity`                            | `class PersonModel(Base)`                  |
| `@Id @GeneratedValue`                | `mapped_column(primary_key=True, autoincrement=True)` |
| `@Column`                            | `mapped_column(String(100))`               |
| `CrudRepository`                     | `PersonDAO` mit `Session`                  |
| `repository.save(entity)`            | `session.add(model); session.commit()`     |
| `repository.findById(id)`            | `session.get(PersonModel, id)`             |
| `@Autowired EntityManager`           | `Depends(get_session)`                     |

### ORM-Modell

```python
class PersonModel(Base):
    __tablename__ = "persons"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    vorname: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(100))
```

`Mapped[str]` ist SQLAlchemy 2.0's typsicheres Äquivalent zu `@Column`.

### Session als Dependency

Die Datenbankverbindung wird per `Depends` in den Request-Lifecycle eingebunden:

```python
def get_session() -> Generator[Session, None, None]:
    with SessionLocal() as session:
        yield session
```

FastAPI öffnet die Session vor dem Request und schließt sie danach automatisch.

### Abhängigkeitskette

```
get_session()           → Session
get_personen_service()  → PersonenService(PersonDAO(session))
```

### Struktur

```
python0110/
├── app.py               # Endpunkte
├── database.py          # Engine + Session-Dependency
├── orm_models.py        # SQLAlchemy ORM-Modell
├── models.py            # Pydantic-Modelle (Request/Response)
├── person_dao.py        # Datenbankzugriff
├── personen.py          # Abstrakte Basisklasse
├── personen_service.py  # Service-Schicht
├── main.py
├── docker-compose.yml
└── tests/
    └── test_app.py      # SQLite in-memory mit StaticPool
```

### Voraussetzungen

- Python 3.12+
- uv installiert
- Docker (für PostgreSQL)

### Datenbank starten

```shell
docker compose up -d
```

### Einrichten und Ausführen

```shell
uv sync
uv run python main.py
```

`main.py` erstellt die Tabellen automatisch beim Start (`create_all`).

```shell
curl -X POST http://localhost:8080/api/person \
  -H "Content-Type: application/json" \
  -d '{"vorname": "Hugo", "name": "Tester"}'

curl http://localhost:8080/api/person/1
```

### Tests ausführen

Tests laufen ohne Docker — SQLite in-memory ersetzt PostgreSQL:

```shell
uv run pytest -v
```

`StaticPool` stellt sicher, dass alle Verbindungen dieselbe In-Memory-Datenbank nutzen.

### Typprüfung

```shell
uv run mypy .
```
