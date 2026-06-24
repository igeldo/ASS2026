# Informatik 4 – Modul 5: Pythonische Entwurfsmuster

Begleitmaterial zur Lehrveranstaltung **Informatik 4**, Modul 5:
*Pythonische Entwurfsmuster*. Ziel: zeigen, welcher Python-Sprachmechanismus
jeweils ein klassisches Entwurfsmuster trägt — und wann das Pattern in
Python überflüssig wird.

> *"Schön ist besser als hässlich. Einfach ist besser als komplex.
> Lesbarkeit zählt."* — aus *The Zen of Python*

---

## Projektstruktur

| Datei | Beschreibung |
|---|---|
| `modul5_entwurfsmuster.py` | Klassen- und Funktionsdefinitionen für sechs Abschnitte + zwei Exkurse – wird von `main_modul5.py` importiert |
| `main_modul5.py` | Ausführbare Demonstrations-Anwendung – zeigt jedes Pattern in Aktion |
| `MODUL5_LEHRBUCH.md` | Lehrbuch-Dokument zum Selbststudium – ausführliche Erklärungen, Idiomatik-Diskussionen, Übungsaufgaben |
| `MODUL5_PRESENTATION.md` | Stichpunkt-Notizen zum Üben der Präsentation (~20 Min Kern + Exkurse) |

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
  Abschnitt 1: Singleton – klassisch über __new__
============================================================
logger_a = LoggerJavaStil(Einträge=2)
logger_b = LoggerJavaStil(Einträge=2)

Sind es identische Objekte?  logger_a is logger_b -> True
...
```

---

## Was wird behandelt?

### `modul5_entwurfsmuster.py` – Sechs Abschnitte + zwei Exkurse

Enthält alle Klassen und Funktionen mit Python-zentrischer Idiomatik —
gruppiert nach Pattern und Variante. Keine Ausgaben; wird von
`main_modul5.py` importiert.

| Abschnitt | Pattern | Python-Mechanismus |
|---|---|---|
| 1 | Singleton – klassisch | `__new__` + Klassenvariable als Cache |
| 2 | Singleton – Pythonisch | Modul-Singleton, `@singleton`-Decorator |
| 3 | Factory – explizit | `abc.ABC` + Factory-Klasse mit `if/elif` |
| 4 | Factory – Pythonisch | Dict-Dispatch (Registry), `@classmethod` |
| 5 | Observer | Liste von Callables, `__call__` für Beobachter mit Zustand |
| 6 | MVC | Model/View/Controller auf Observer-Basis – Brücke zum REST-Backend |
| Exkurs 1 | Strategy *(Bonus)* | Funktionen als first-class Argument, Closures |
| Exkurs 2 | Context Manager *(Bonus)* | `__enter__`/`__exit__`, `@contextmanager` |

### `main_modul5.py` – Demonstrations-Anwendung

Führt alle Klassen und Funktionen vor und zeigt ihre Ausgaben Abschnitt für
Abschnitt. Ideal zum Nachvollziehen der Konzepte – und als Live-Demo für
die Präsentation.

### `MODUL5_LEHRBUCH.md` – Selbststudium

Ausführliches Lehrbuch-Dokument: pro Pattern *"Das Problem"*, *"Pythonisch
lösen"*, mehrere Varianten, *"Wo begegnet einem das in Python?"* und
*"Wann braucht man das Pattern nicht?"*. Plus eine Zusammenfassungstabelle
und sieben Übungsaufgaben.

### `MODUL5_PRESENTATION.md` – Präsentations-Notizen

Stichpunkt-Notizen zum Üben des Vortrags: Thesensätze, Kernaussagen, zu
zeigender Code, Demo-Output-Checks, optionale Speaker-Notes und ein
Pacing-Plan auf 20 Minuten (Kern) mit Strategy/Context Manager als Exkurs.

---

## Lernziele

Nach Durcharbeitung dieses Moduls können Studierende:

- die drei klassischen Patterns Singleton, Factory und Observer pythonisch
  umsetzen — und benennen, **welcher Sprachmechanismus** sie jeweils trägt
- erklären, warum Python für einige Patterns kaum Boilerplate braucht
  (first-class Funktionen, Klassen als Objekte, Modul-System)
- **MVC** als Architektur-Muster auf Observer-Basis verstehen und die Brücke
  zum **REST-Backend** der Gruppenprojekte schlagen (Controller = Endpoint,
  View = JSON-Antwort, Model = Domänenzustand)
- entscheiden, wann ein Pattern in Python **überflüssig** ist (Strategy
  mit einer einfachen Funktion, Singleton durch ein Modul-Attribut)
- Context Manager als verallgemeinerten Mechanismus für *"etwas muss
  zuverlässig danach passieren"* einsetzen

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

> **Auf Python denken — nicht Patterns aus anderen Sprachen übersetzen.**
> Das Ziel ist nicht, ein bekanntes Pattern in Python-Syntax umzuschreiben,
> sondern den passenden Python-Mechanismus zu finden, der das Pattern oft
> klein oder unsichtbar macht.

- Jeder Pattern-Abschnitt im Lehrbuch endet mit *"Wann braucht man das
  Pattern nicht?"* — ebenso wichtig wie die Antwort darauf, *wie* man es
  umsetzt.
- Der Demo-Output zeigt nicht nur Erfolgs-, sondern auch Fehlerfälle (z. B.
  unbekannte Tierart in Abschnitt 3, ungültiger Zug `z9` in Abschnitt 6,
  ROLLBACK in Exkurs 2) – beides bewusst, damit man das Verhalten unter
  Stress sieht.

---

## Lizenz

Dieses Material ist ausschließlich für den Einsatz in der Lehre bestimmt.
Weitergabe außerhalb des Kurses nur nach Rücksprache.
