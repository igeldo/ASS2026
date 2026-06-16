# Modul 7 – Typisierung & moderne Python-Praxis

**Informatik 4 · Von Java zu OOP in Python**

> Roter Faden: *„Was würde ich in Java tun – und wie denkt Python das?"*

Diese Datei begleitet `modul7_typisierung.py` und erklärt alle behandelten Konzepte
im Überblick. Alle Codebeispiele in der `.py`-Datei sind direkt ausführbar.

---

## Voraussetzungen

| Was | Version |
|-----|---------|
| Python | ≥ 3.9 |
| mypy (optional) | ≥ 1.0 |

```bash
# mypy installieren (einmalig)
pip install mypy
```

---

## Ausführen

```bash
# Alle Beispiele ausführen
python modul7_typisierung.py

# Typen statisch prüfen (wie ein Java-Compiler)
mypy modul7_typisierung.py
```

---

## Inhalt der Datei

### 7.1 · Einfache Type Hints – Variablen

In Java ist der Typ einer Variable Pflicht. In Python ist er optional – aber empfohlen.

```python
# Java:   int alter = 25;
# Python:
alter: int   = 25
name:  str   = "Ada"
pi:    float = 3.14
aktiv: bool  = True
```

> Python ignoriert Type Hints zur **Laufzeit** vollständig.
> Nur `mypy` wertet sie aus – ähnlich wie ein Java-Compiler.

---

### 7.2 · Type Hints bei Funktionen

```python
# Java:   public static String begrüße(String name, int alter) { ... }
def begrüße(name: str, alter: int) -> str:
    return f"Hallo {name}, du bist {alter} Jahre alt."

# -> nach der Parameterliste = Rückgabetyp
# -> None als Rückgabetyp entspricht void in Java
def drucke_linie(text: str) -> None:
    print(f">> {text}")
```

**Mehrere Rückgabewerte** – in Java nicht direkt möglich, in Python über Tupel:

```python
# Java-Umweg: eigene Klasse oder Array
# Python direkt:
def min_max(zahlen: list[int]) -> tuple[int, int]:
    return min(zahlen), max(zahlen)

kleinster, größter = min_max([3, 1, 4, 1, 5])
```

---

### 7.3 · Optional – Pythons Version von `null`

```python
from typing import Optional

# Java:   String name = null;  → NullPointerException droht!
# Python:
name: Optional[str] = None   # = str oder None

def finde_nutzer(nutzer_id: int) -> Optional[str]:
    datenbank = {1: "Ada", 2: "Alan"}
    return datenbank.get(nutzer_id)   # None wenn nicht vorhanden

# mypy erzwingt eine None-Prüfung vor der Verwendung:
nutzer = finde_nutzer(99)
if nutzer is not None:
    print(nutzer.upper())
```

---

### 7.4 · Union – mehrere erlaubte Typen

Java kennt das nicht direkt (nur über Interfaces/Generics).

```python
from typing import Union

def verdopple(wert: Union[int, float]) -> Union[int, float]:
    return wert * 2

# Python 3.10+ – modernere Schreibweise:
# def verdopple(wert: int | float) -> int | float:
```

---

### 7.5 · Komplexe Typen – list, dict, tuple, set

| Java | Python (ab 3.9) |
|------|-----------------|
| `List<String>` | `list[str]` |
| `Map<String, Integer>` | `dict[str, int]` |
| `Set<String>` | `set[str]` |
| `int[]` | `tuple[int, ...]` |

```python
namen:       list[str]        = ["Ada", "Alan", "Grace"]
punkte:      dict[str, int]   = {"Ada": 95, "Alan": 88}
sprachen:    set[str]         = {"Python", "Java", "C++"}
person_info: tuple[int, str]  = (25, "Ada")

# Python bis 3.8 – mit typing-Import:
# from typing import List, Dict, Set, Tuple
# namen: List[str] = [...]
```

---

### 7.6 · Callable – Funktionen als Typen

```python
from collections.abc import Callable

# Java (ab Java 8):  Function<Integer, Integer> op = x -> x * 2;
# Python:
def wende_an(zahlen: list[int], operation: Callable[[int], int]) -> list[int]:
    return [operation(z) for z in zahlen]

wende_an([1, 2, 3], lambda x: x * 2)   # [2, 4, 6]
```

`Callable[[int], int]` bedeutet: Funktion, die ein `int` nimmt und ein `int` zurückgibt.

---

### 7.7 · Protokolle – strukturelle Typen statt Java-Interfaces

Das ist der größte konzeptuelle Unterschied bei der Typisierung.

| | Java | Python |
|---|---|---|
| Typ-System | **nominal** – explizites `implements` | **strukturell** – Methoden entscheiden |
| Deklaration | `interface Druckbar { }` | `class Druckbar(Protocol):` |
| Nutzung | `class X implements Druckbar` | `class X:` – kein `implements` nötig |

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Druckbar(Protocol):
    def drucken(self) -> str: ...

class Dokument:                   # kein "implements Druckbar"!
    def drucken(self) -> str:
        return "[Dokument]"

class Rechnung:                   # auch diese Klasse kennt Druckbar nicht
    def drucken(self) -> str:
        return "[Rechnung]"

def ausgabe(obj: Druckbar) -> None:
    print(obj.drucken())

ausgabe(Dokument())   # ✓ mypy akzeptiert das
ausgabe(Rechnung())   # ✓ auch das – wegen struktureller Typisierung

# @runtime_checkable erlaubt isinstance-Check:
isinstance(Dokument(), Druckbar)   # True
isinstance(Rechnung(), Druckbar)   # True
```

> **Duck Typing mit Typsicherheit**: „Wenn es quakt wie eine Ente, ist es eine Ente."

---

### 7.8 · mypy – statische Typprüfung

```
Java                          Python + mypy
─────────────────────────     ─────────────────────────
Compiler prüft Typen          mypy prüft Typen
Pflicht beim Kompilieren      Optional, separates Tool
Fehler → kein Start           Fehler → mypy-Ausgabe
```

```bash
mypy modul7_typisierung.py

# Beispiel-Ausgabe bei Typfehler:
# modul7_typisierung.py:5: error: Argument 1 to "addiere"
# has incompatible type "str"; expected "int"
```

Typfehler, die mypy erkennt (in der Datei auskommentiert dokumentiert):

```python
def addiere(a: int, b: int) -> int:
    return a + b

# ⚠ mypy: Incompatible types in assignment
ergebnis: str = addiere(3, 5)

# ⚠ mypy: Argument 1 has incompatible type "str"; expected "int"
addiere("drei", "fünf")
```

---

### 7.9 · Dataclasses – kompakte typisierte Klassen

`@dataclass` generiert `__init__`, `__repr__` und `__eq__` automatisch –
das entspricht einem Java-Record oder einer Klasse mit viel Boilerplate.

```python
# Java (viel Boilerplate):
# public class Punkt {
#     private final double x;
#     private final double y;
#     public Punkt(double x, double y) { this.x = x; this.y = y; }
#     public String toString() { ... }
#     public boolean equals(Object o) { ... }
# }

# Python mit @dataclass:
from dataclasses import dataclass

@dataclass
class Punkt:
    x: float
    y: float

    def abstand_zum_ursprung(self) -> float:
        return (self.x ** 2 + self.y ** 2) ** 0.5

p1 = Punkt(3.0, 4.0)
p2 = Punkt(3.0, 4.0)

print(p1)           # Punkt(x=3.0, y=4.0)  ← __repr__ automatisch
print(p1 == p2)     # True                  ← __eq__ automatisch
print(p1.abstand_zum_ursprung())  # 5.0
```

Felder mit Standardwert kommen **nach** Feldern ohne:

```python
@dataclass
class Student:
    name:      str
    matrikel:  int
    punkte:    float         = 0.0
    spitzname: Optional[str] = None
```

---

### 7.10 · Zusammenfassung Java ↔ Python

| Java | Python |
|------|--------|
| `int x = 5;` | `x: int = 5` |
| `String s = null;` | `s: Optional[str] = None` |
| `List<String> l = ...;` | `l: list[str] = [...]` |
| `Map<String, Integer> m = ...;` | `m: dict[str, int] = {...}` |
| `String f(int x) { }` | `def f(x: int) -> str:` |
| `interface Druckbar { }` | `class Druckbar(Protocol):` |
| `class X implements Y { }` | `class X:  # kein implements!` |
| Compiler prüft Typen (Pflicht) | mypy prüft Typen (optional) |
| Fehler beim Kompilieren | Fehler beim mypy-Aufruf |

---

## Fazit

Python-Typen sind **optional**, aber in größeren Projekten sehr empfehlenswert.
Mit Type Hints und `mypy` bekommt man Java-ähnliche Typsicherheit –
ohne den Zwang der Sprache. Der Code bleibt dabei lesbar und pythonisch.

---

## Verwendete Module

| Modul | Woher | Zweck |
|-------|-------|-------|
| `typing` | Standardbibliothek | `Optional`, `Union`, `Protocol` |
| `collections.abc` | Standardbibliothek | `Callable` |
| `dataclasses` | Standardbibliothek | `@dataclass` |
| `mypy` | `pip install mypy` | Statische Typprüfung |

Alle Module außer `mypy` sind Teil der Python-Standardbibliothek – **kein zusätzlicher Install nötig**.
