# Informatik 4 – Von Java zu OOP in Python

Begleitmaterial zur Lehrveranstaltung **Informatik 4**.  
Ziel: Den Umstieg von Java auf objektorientiertes Python praxisnah vermitteln – nicht durch Übersetzen, sondern durch idiomatisches Python-Denken.

---

## Projektstruktur

| Datei | Beschreibung |
|---|---|
| `informatik4_oop_java_zu_python.py` | Klassendefinitionen zu Modul 1 – werden von `main.py` importiert |
| `main.py` | Ausführbare Demonstrations-Anwendung – importiert alle Klassen und zeigt sie in Aktion |

> **Reihenfolge:** Zuerst `informatik4_oop_java_zu_python.py` lesen (Konzepte verstehen), dann `main.py` ausführen (Konzepte in Aktion sehen).

---

## Voraussetzungen

- **Python 3.8 oder höher** – [python.org/downloads](https://www.python.org/downloads/)
- **PyCharm** (Community Edition reicht) – [jetbrains.com/pycharm](https://www.jetbrains.com/pycharm/)
- Keine externen Bibliotheken nötig – nur die Python-Standardbibliothek

---

## Quickstart

### In PyCharm
1. Den gesamten Projektordner in PyCharm öffnen
2. `main.py` auswählen
3. Oben rechts auf den grünen **Play-Button** klicken (oder `Shift + F10`)
4. Die Ausgabe erscheint im unteren **Run-Fenster**

### Im Terminal (alternativ)
```bash
python main.py
```

### Erwartete Ausgabe (Ausschnitt)
```
=== Modul 1: Klassen und Objekte ===
Ich bin Anna, 22 Jahre alt.
Person(Anna, 22 Jahre)

=== Modul 2: Sichtbarkeit ===
Konto von Max, Nr: DE12345

=== Modul 3: Properties ===
...
```

---

## Was wird behandelt?

### `informatik4_oop_java_zu_python.py` – Klassendefinitionen (Modul 1)

Enthält alle Klassen mit direktem Java-Vergleich. Der Java-Code steht jeweils als Kommentar direkt über dem Python-Äquivalent. Keine Ausgaben – wird von `main.py` importiert.

| Abschnitt | Inhalt |
|---|---|
| 1 – Klassen und Objekte | `__init__`, `self`, kein `new` |
| 2 – Sichtbarkeit | `public` / `_protected` / `__private` als Konvention |
| 3 – Properties | `@property` statt Getter/Setter |
| 4 – Klassen- und statische Methoden | `@classmethod`, `@staticmethod` |
| 5 – Dunder-Methoden | `__str__`, `__add__`, `__eq__` und mehr |
| 6 – Vererbung | `super()` ohne Argumente, Methoden überschreiben |
| 7 – Duck Typing | Polymorphismus ohne gemeinsames Interface |

### `main.py` – Demonstrations-Anwendung

Führt alle Klassen aus `informatik4_oop_java_zu_python.py` vor und zeigt ihre Ausgaben Abschnitt für Abschnitt. Ideal zum Nachvollziehen der Konzepte.

---

## Lernziele

Nach Durcharbeitung der Beispieldatei können Studierende:

- Python-Klassen lesen und schreiben
- den Unterschied zwischen Pythons Konventionen und Javas Erzwingung erklären
- `@property` sinnvoll einsetzen statt Java-style Getter/Setter zu schreiben
- Dunder-Methoden für eigene Klassen definieren
- einfache Vererbungshierarchien in Python aufbauen
- den Begriff *Duck Typing* erklären und anwenden

---

## Kursstruktur (Überblick)

| Modul | Thema | Status |
|---|---|---|
| **Modul 1** | Grundlagen & Unterschiede – Syntax, Typisierung, Funktionen, OOP-Einstieg | ✅ Verfügbar |
| Modul 2 | Klassen und Objekte vertieft | 🔜 Folgt |
| Modul 3 | Vererbung und Polymorphismus | 🔜 Folgt |
| Modul 4 | Pythonische Konzepte ohne Java-Pendant | 🔜 Folgt |
| Modul 5 | Entwurfsmuster in Python | 🔜 Folgt |
| Modul 6 | Fehlerbehandlung | 🔜 Folgt |
| Modul 7 | Typisierung & moderne Python-Praxis | 🔜 Folgt |
| Modul 8 | Werkzeuge & Ökosystem | 🔜 Folgt |
| Modul 9 | Abschlussprojekt | 🔜 Folgt |

---

## Hinweise für Studierende

> **Nicht einfach übersetzen – auf Python denken.**  
> Das Ziel ist nicht, Java-Code in Python-Syntax umzuschreiben, sondern die Sprache idiomatisch zu verwenden. Ein guter Test: Würde ein erfahrener Python-Entwickler den Code so schreiben?

- Kommentare mit `# Java:` zeigen immer das Java-Äquivalent
- Abschnitte können unabhängig voneinander gelesen werden
- Fehler sind teilweise absichtlich eingebaut und auskommentiert – zum Ausprobieren einfach die Kommentarzeichen entfernen

Bei Fragen oder gefundenen Fehlern bitte im Kurs-Forum melden.

---

## Lizenz

Dieses Material ist ausschließlich für den Einsatz in der Lehre bestimmt. Weitergabe außerhalb des Kurses nur nach Rücksprache.
