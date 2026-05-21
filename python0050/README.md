# Python Starter

## Step 50

Service-Klassen

### Was ist neu?

Die Anwendung wird in separate Klassen aufgeteilt — analog zur Struktur in Java-Projekten.

| Java                          | Python                        |
|-------------------------------|-------------------------------|
| `interface Greeter`           | `class Greeter(ABC)`          |
| `implements Greeter`          | `class GreeterService(Greeter)` |
| `@Override`                   | entfällt (Python prüft das automatisch) |
| `new GreeterService()`        | `GreeterService()`            |

### Struktur

```
python0050/
├── greeter.py                  # Abstrakte Basisklasse (wie Java-Interface)
├── greeter_service.py          # Konkrete Implementierung
├── hello_world_application.py  # Anwendungsklasse
└── main.py                     # Einstiegspunkt
```

### Abstrakte Basisklasse

Python kennt kein `interface`-Schlüsselwort. Stattdessen wird `ABC` (Abstract Base Class) aus der Standardbibliothek verwendet:

```python
from abc import ABC, abstractmethod

class Greeter(ABC):
    @abstractmethod
    def greet(self, name: str) -> str: ...
```

`@abstractmethod` entspricht einer abstrakten Methode in Java — eine Klasse, die `Greeter` erbt, **muss** `greet` implementieren, sonst schlägt die Instanziierung fehl.

### Dependency Injection

`HelloWorldApplication` erhält den `Greeter` von außen übergeben, statt ihn selbst zu erzeugen:

```python
def __init__(self, greeter: Greeter) -> None:
    self._greeter = greeter
```

Der Typ `Greeter` (abstrakt) statt `GreeterService` (konkret) macht die Klasse austauschbar — z.B. für Tests mit einem Mock. Das Muster wird in Step 90 (Dependency Injection) vertieft.

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
2026-05-21 10:00:00,000 INFO     HelloWorldApplication - Hello, World!
```

### Typprüfung

```shell
uv run mypy .
```
