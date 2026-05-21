# Python Starter

## Step 40

Type Hints

### Was ist neu?

Python ist dynamisch typisiert — Typen müssen nicht angegeben werden.
Type Hints sind optionale Annotationen, die Typen explizit dokumentieren und von IDEs und Tools ausgewertet werden.

Für Java-Entwickler: Type Hints sind das Python-Äquivalent zu Typdeklarationen in Java, werden aber **nicht zur Laufzeit erzwungen**.

### Syntax

#### Parameter und Rückgabewert

```python
def greeting(self) -> str:       # Rückgabetyp: str
    ...

def __init__(self, name: str) -> None:   # Parameter: str, kein Rückgabewert
    ...
```

#### Instanz-Attribute

```python
def __init__(self, name: str) -> None:
    self._name: str = name       # Attribut-Typ explizit angegeben
```

#### Optionale Werte

```python
# Python 3.10+
def find(self, name: str) -> str | None:
    ...

# alternativ (alle Python-Versionen)
from typing import Optional
def find(self, name: str) -> Optional[str]:
    ...
```

#### Kollektionen

```python
names: list[str] = ["Alice", "Bob"]
scores: dict[str, int] = {"Alice": 42}
```

### Vergleich Java vs. Python

| Java                        | Python                        |
|-----------------------------|-------------------------------|
| `String greet(String name)` | `def greet(self, name: str) -> str:` |
| `void run()`                | `def run(self) -> None:`      |
| `Optional<String>`          | `str \| None`                 |
| Zur Laufzeit erzwungen      | Nur zur Entwicklungszeit      |

### Werkzeuge

Type Hints werden von diesen Tools ausgewertet:

| Tool   | Zweck                                      |
|--------|--------------------------------------------|
| PyCharm | Typfehler direkt im Editor anzeigen       |
| mypy   | Statische Typprüfung auf der Kommandozeile |
| FastAPI | Generiert API-Dokumentation aus Typen     |

### Voraussetzungen

- Python 3.12+
- uv installiert

### Einrichten und Ausführen

```shell
uv sync
uv run python main.py
```

Erwartete Ausgabe:

```
2026-05-21 10:00:00,000 INFO     HelloWorld - Hello, World!
2026-05-21 10:00:00,001 INFO     HelloWorld - Hello, Python!
```
