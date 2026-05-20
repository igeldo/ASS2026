# Informatik 4 – Von Java zu OOP in Python (Modul 5)

Begleitmaterial zur Lehrveranstaltung **Informatik 4**, Modul 5: *Pythonische
Entwurfsmuster*. Ziel: Java-bekannte Patterns (Singleton, Factory, Observer)
nach Python übertragen – und zeigen, wo Python idiomatische Abkürzungen
kennt, die Java so nicht hat.

> *"Was würde ich in Java tun – und wie denkt Python das?"*
> Viele Java-Patterns sind in Python keine Patterns mehr – sondern Sprache.

---

## Projektstruktur

| Datei | Beschreibung |
|---|---|
| `modul5_entwurfsmuster.py` | Klassen- und Funktionsdefinitionen für die sieben Abschnitte – wird von `main_modul5.py` importiert |
| `main_modul5.py` | Ausführbare Demonstrations-Anwendung – zeigt jedes Pattern in Aktion |
| `MODUL5_LEHRBUCH.md` | Lehrbuch-Dokument zum Selbststudium – ausführliche Erklärungen, Trade-offs, Übungsaufgaben |
| `MODUL5_PRESENTATION.md` | Stichpunkt-Notizen zum Üben der Präsentation (~30 Min) |

> **Reihenfolge:** Zuerst `modul5_entwurfsmuster.py` lesen (Konzepte
> verstehen), dann `main_modul5.py` ausführen (Konzepte in Aktion sehen).
> Für tiefere Erklärungen das Lehrbuch konsultieren.

---

## Voraussetzungen

- **Python 3.10 oder höher** – wegen `dict[str, type[Tier]]`-Syntax und
  `Tier | None`-Union-Schreibweise
- **PyCharm** (Community Edition reicht) – [jetbrains.com/pycharm](https://www.jetbrains.com/pycharm/)
- Keine externen Bibliotheken nötig – nur die Python-Standardbibliothek

---

## Quickstart

### In PyCharm
1. Den gesamten Projektordner in PyCharm öffnen
2. `main_modul5.py` auswählen
3. Oben rechts auf den grünen **Play-Button** klicken (oder `Shift + F10`)
4. Die Ausgabe erscheint im unteren **Run-Fenster**

### Im Terminal (alternativ)
```bash
python main_modul5.py
```

### Erwartete Ausgabe (Ausschnitt)
```
============================================================
  Abschnitt 1: Singleton – Java-Stil mit __new__
============================================================
logger_a = LoggerJavaStil(Einträge=2)
logger_b = LoggerJavaStil(Einträge=2)

Sind es identische Objekte?  logger_a is logger_b -> True
...
```

---

## Was wird behandelt?

### `modul5_entwurfsmuster.py` – Sieben Abschnitte

Enthält alle Klassen und Funktionen mit direktem Java-Vergleich. Der
Java-Code steht jeweils als Kommentar direkt über dem Python-Äquivalent.
Keine Ausgaben – wird von `main_modul5.py` importiert.

| Abschnitt | Pattern | Inhalt |
|---|---|---|
| 1 | Singleton – Java-Stil | `__new__` + Klassenvariable als Cache |
| 2 | Singleton – Pythonisch | Modul-Singleton, `@singleton`-Decorator |
| 3 | Factory – Java-Stil | `abc.ABC` + Factory-Klasse mit `if/elif` |
| 4 | Factory – Pythonisch | Dict-Dispatch (Registry), `@classmethod` |
| 5 | Observer | Liste von Callables statt Listener-Interface, `__call__` |
| 6 | Strategy | Funktion als Argument, Closures statt Strategy-Klassen |
| 7 | Context Manager | `__enter__`/`__exit__`, `@contextmanager` |

### `main_modul5.py` – Demonstrations-Anwendung

Führt alle Klassen und Funktionen vor und zeigt ihre Ausgaben Abschnitt für
Abschnitt. Ideal zum Nachvollziehen der Konzepte – und als Live-Demo für
die Präsentation.

### `MODUL5_LEHRBUCH.md` – Selbststudium

Ausführliches Lehrbuch-Dokument mit zusätzlichen Beispielen, Trade-off-
Diskussionen (z. B. Singleton als Anti-Pattern), Decorator-Registrierung als
Factory-Erweiterung, Java-Vergleichstabellen und sechs Übungsaufgaben.

### `MODUL5_PRESENTATION.md` – Präsentations-Notizen

Stichpunkt-Notizen zum Üben des Vortrags: Thesensätze, Kernaussagen, zu
zeigender Code, Demo-Output-Checks, typische Zwischenfragen und ein
Pacing-Plan auf 30 Minuten.

---

## Lernziele

Nach Durcharbeitung dieses Moduls können Studierende:

- die drei klassischen Patterns Singleton, Factory und Observer in Python
  sowohl im Java-Stil als auch idiomatisch umsetzen
- erklären, **warum** Python für einige Patterns weniger Boilerplate braucht
  (first-class Funktionen, Klassen als Objekte, Modul-System)
- entscheiden, wann ein Pattern in Python **überflüssig** ist (z. B.
  Strategy mit Funktionen statt Klassen)
- Context Manager als Pythons Antwort auf *"etwas muss zuverlässig danach
  passieren"* einsetzen

---

## Kursstruktur (Überblick)

| Modul | Thema | Status |
|---|---|---|
| Modul 1 | Grundlagen & Unterschiede – Syntax, Typisierung, Funktionen, OOP-Einstieg | ✅ Verfügbar (Branch `Python_OOP`) |
| Modul 2 | Klassen und Objekte vertieft | 🔜 Folgt |
| Modul 3 | Vererbung und Polymorphismus | 🔜 Folgt |
| Modul 4 | Pythonische Konzepte ohne Java-Pendant | 🔜 Folgt |
| **Modul 5** | **Pythonische Entwurfsmuster** | **✅ Verfügbar (dieser Branch)** |
| Modul 6 | Fehlerbehandlung | 🔜 Folgt |
| Modul 7 | Typisierung & moderne Python-Praxis | 🔜 Folgt |
| Modul 8 | Werkzeuge & Ökosystem | 🔜 Folgt |
| Modul 9 | Abschlussprojekt | 🔜 Folgt |

---

## Hinweise für Studierende

> **Nicht einfach übersetzen – auf Python denken.**
> Das Ziel ist nicht, Java-Patterns in Python-Syntax umzuschreiben, sondern
> die Sprache idiomatisch zu verwenden. Ein guter Test: Würde ein erfahrener
> Python-Entwickler den Code so schreiben?

- Kommentare mit `# Java:` zeigen immer das Java-Äquivalent
- Abschnitte können unabhängig voneinander gelesen werden
- Der Demo-Output zeigt nicht nur Erfolgs-, sondern auch Fehlerfälle (z. B.
  unbekannte Tierart in Abschnitt 3, ROLLBACK in Abschnitt 7) – beides
  bewusst, damit man das Verhalten unter Stress sieht.

---

## Lizenz

Dieses Material ist ausschließlich für den Einsatz in der Lehre bestimmt.
Weitergabe außerhalb des Kurses nur nach Rücksprache.
