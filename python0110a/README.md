# Python Starter

## Step 110a

Direktes SQL ohne ORM

### Was ist neu?

Dieselbe Anwendung wie in Step 110 — aber ohne ORM-Mapping. Statt SQLAlchemy-Modellklassen werden SQL-Strings direkt mit `text()` ausgeführt.

### Vergleich: ORM vs. direktes SQL

| python0110 (ORM)                              | python0110a (direktes SQL)                        |
|-----------------------------------------------|---------------------------------------------------|
| `class PersonModel(Base)`                     | keine Modellklasse                                |
| `Mapped[int]`, `mapped_column(...)`           | `CREATE TABLE persons (...)`                      |
| `session.add(model); session.commit()`        | `session.execute(text("INSERT INTO ..."))`        |
| `session.get(PersonModel, id)`                | `session.execute(text("SELECT ... WHERE id = :id"))` |
| Schema-Erstellung automatisch via `create_all` | Schema-Erstellung per DDL-Statement              |

### SQL in Python

SQLAlchemy's `text()` kennzeichnet rohe SQL-Strings explizit. Parameter werden mit `:name`-Platzhaltern übergeben — das verhindert SQL Injection:

```python
session.execute(
    text("INSERT INTO persons (vorname, name) VALUES (:vorname, :name) RETURNING id"),
    {"vorname": vorname, "name": name},
)
```

Das `RETURNING id` gibt die generierte ID direkt aus dem INSERT zurück — kein separates SELECT nötig.

### Ergebnis-Zugriff

`mappings()` gibt Zeilen als Dict-ähnliche Objekte zurück, Zugriff per Spaltenname:

```python
row = result.mappings().fetchone()
Person(id=row["id"], vorname=row["vorname"], name=row["name"])
```

### Struktur

```
python0110a/
├── app.py               # identisch zu python0110
├── database.py          # identisch zu python0110
├── models.py            # identisch zu python0110
├── person_dao.py        # direktes SQL statt ORM
├── personen.py          # identisch zu python0110
├── personen_service.py  # identisch zu python0110
├── main.py              # CREATE TABLE per DDL-Statement
├── docker-compose.yml
└── tests/
    └── test_app.py      # SQLite mit manueller Tabellenerstellung
```

`orm_models.py` entfällt vollständig.

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

### Tests ausführen

```shell
uv run pytest -v
```

Tests erstellen die Tabelle per SQLite-kompatiblem DDL und löschen sie nach jedem Test wieder.

### Typprüfung

```shell
uv run mypy .
```
