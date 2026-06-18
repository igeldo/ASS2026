# Informatik 4 – Von Java zu OOP in Python
## Modul 8: Werkzeuge & Ökosystem



---

## Über dieses Modul

Modul 8 vollzieht den **Tooling-Transfer**: Sie kennen bereits die Werkzeuge des Java-Ökosystems – Maven, JUnit, Javadoc, IntelliJ. Dieses Modul zeigt, wie Python dieselben Probleme löst, oft mit weniger Konfigurationsaufwand, aber anderen Konventionen.

> **Leitfrage dieses Moduls:**  
> *"Was würde ich in Java mit meinen Build-Tools, Tests und Dokumentation tun – und wie denkt Python das?"*

---

## Projektstruktur

```
modul8/
├── informatik4_modul8_werkzeuge.py   # Hauptmodul: Klassen & Funktionen (wird importiert)
├── main.py                           # Ausführbarer Einstiegspunkt – zeigt alles in Aktion
├── requirements.txt                  # Abhängigkeiten (= Maven pom.xml)
├── README.md                         # Diese Datei
└── tests/
    └── test_modul8.py                # pytest-Teststuite (= JUnit-Testklassen)
```

| Datei | Entspricht in Java | Zweck |
|---|---|---|
| `informatik4_modul8_werkzeuge.py` | `Bankkonto.java` + Utility-Klasse | Klassen & Funktionen mit Logging + Docstrings |
| `main.py` | `Main.java` mit `main()` | Ausführbarer Demonstrationseinstieg |
| `requirements.txt` | `pom.xml` / `build.gradle` | Paketabhängigkeiten deklarieren |
| `tests/test_modul8.py` | `BankkontoTest.java` (JUnit) | Automatisierte Unit-Tests mit pytest |

---

## Voraussetzungen

- **Python 3.10 oder höher** → [python.org/downloads](https://www.python.org/downloads/)
- **PyCharm** (Community Edition reicht) → [jetbrains.com/pycharm](https://www.jetbrains.com/pycharm/)
- Keine externen Bibliotheken außer `pytest` – installiert in Schritt 3

---

## Quickstart

### Schritt 1 – Repository klonen (Git-Workflow)

```bash
git clone -b Modul8 https://github.com/igeldo/ASS2026.git
cd modul8
```

> **Java-Parallele:** Entspricht dem Auschecken eines Maven-Projekts aus Ihrem Git-Repository. Der Unterschied: Kein `mvn clean install` nötig – Python-Quellcode ist direkt lauffähig.

---

### Schritt 2 – Virtuelle Umgebung einrichten

```bash
# Virtuelle Umgebung erstellen (einmalig pro Projekt)
python -m venv .venv

# Aktivieren – Linux / macOS
source .venv/bin/activate

# Aktivieren – Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

Nach der Aktivierung sehen Sie `(.venv)` am Anfang Ihrer Terminal-Zeile.

> **Java-Parallele:** Entspricht dem lokalen Maven-Repository (`~/.m2`), jedoch **pro Projekt isoliert**. Ohne `venv` installieren Sie Pakete global ins System – das führt zu Versionskonflikten zwischen Projekten. Vergleich: Stellen Sie sich vor, Maven würde alle Abhängigkeiten aller Projekte in denselben Classpath legen.

**In PyCharm:** Unten rechts auf den Interpreter-Indikator klicken → `Add New Interpreter` → `Add Local Interpreter` → `Virtualenv Environment` wählen.

---

### Schritt 3 – Abhängigkeiten installieren

```bash
pip install -r requirements.txt
```

> **Java-Parallele:** `mvn install` oder `gradle dependencies`. Python lädt die Pakete ins `.venv`-Verzeichnis, nicht in ein globales Repository.

---

### Schritt 4 – Tests ausführen (pytest)

```bash
# Alle Tests ausführen
pytest tests/

# Mit ausführlicher Ausgabe (wie JUnit in IntelliJ)
pytest tests/ -v

# Mit Coverage-Report (HTML-Bericht in htmlcov/)
pytest tests/ -v --cov=informatik4_modul8_werkzeuge --cov-report=html
```

Erwartete Ausgabe bei Erfolg:

```
tests/test_modul8.py::TestBankkonto::test_kontostand_nach_erstellung PASSED
tests/test_modul8.py::TestBankkonto::test_einzahlung_erhoeht_kontostand PASSED
...
tests/test_modul8.py::TestZinsrechner::test_berechnung[1000.0-5.0-10-1628.89] PASSED
tests/test_modul8.py::TestZinsrechner::test_berechnung[500.0-3.5-5-592.02]   PASSED
...
========================= 18 passed in 0.05s =========================
```

> **Java-Parallele:** `mvn test` oder der grüne Play-Button auf einer JUnit-Klasse in IntelliJ.

---

### Schritt 5 – Hauptprogramm starten

```bash
python main.py
```

**Oder in PyCharm:** `main.py` öffnen → grüner Play-Button (oder `Shift+F10`).

Erwartete Ausgabe (Ausschnitt):

```
=================================================================
 DEMO 1: Logging in Aktion
=================================================================
12:34:56 | informatik4_modul8_werkzeuge     | INFO     | Konto für 'Grace Hopper' mit 500.00€ eröffnet.
12:34:56 | informatik4_modul8_werkzeuge     | DEBUG    | 250.00€ eingezahlt auf Konto von 'Grace Hopper'. Neuer Stand: 750.00€
12:34:56 | informatik4_modul8_werkzeuge     | ERROR    | Abhebung von 1000.00€ für 'Grace Hopper' abgelehnt – Kontostand 750.00€ nicht ausreichend.
```

---

## Was wird behandelt?

### 1. Virtuelle Umgebungen (`venv`)

| Java | Python |
|---|---|
| Maven: `~/.m2/repository` (global) | `python -m venv .venv` (pro Projekt) |
| `pom.xml` deklariert Abhängigkeiten | `requirements.txt` deklariert Abhängigkeiten |
| `mvn install` lädt Pakete herunter | `pip install -r requirements.txt` |
| Scope: `compile`, `test`, `runtime` | Keine Scopes (einfachere Textliste) |

**Das Problem:** Python installiert Pakete standardmäßig global. Wenn Projekt A `requests==2.28` und Projekt B `requests==2.31` braucht, entsteht ein Konflikt. Ein `venv` löst das durch vollständige Isolation pro Projekt.

---

### 2. Logging statt `print()`

Sehen Sie sich `informatik4_modul8_werkzeuge.py` an: Keine einzige `print()`-Anweisung in den Klassen. Stattdessen:

```python
# Modul-Level (einmalig pro Datei, entspricht Java Logger-Initialisierung)
logger = logging.getLogger(__name__)

# In Methoden:
logger.info("Konto für '%s' eröffnet.", self.inhaber)   # Normalbetrieb
logger.debug("Detailinfo für Entwickler.")              # Nur beim Debuggen
logger.warning("Ungültige Eingabe erhalten.")           # Warnung, kein Abbruch
logger.error("Operation fehlgeschlagen: %s", grund)    # Fehler
```

**Konfiguration erfolgt zentral in `main.py`** – nie in den Modulen selbst. Das entspricht dem Prinzip, das auch `logback.xml` in Java umsetzt: Applikationslogik ist sauber von Logging-Konfiguration getrennt.

---

### 3. Docstrings statt Javadoc

| Java (Javadoc) | Python (Google-Style Docstring) |
|---|---|
| `/** Text */` *über* der Methode | `"""Text"""` *in* der Methode (erste Zeile) |
| `@param name Beschreibung` | `Args: name (typ): Beschreibung` |
| `@return Typ Beschreibung` | `Returns: typ: Beschreibung` |
| `@throws ExceptionTyp Grund` | `Raises: ExceptionTyp: Grund` |
| `javadoc` CLI erzeugt HTML | `sphinx-build` erzeugt HTML (optional) |

```python
def berechne_zinseszins(kapital: float, zinssatz: float, jahre: int) -> float:
    """
    Berechnet das Endkapital nach einer Laufzeit mit Zinseszins-Effekt.

    Args:
        kapital (float): Das Startkapital in Euro.
        zinssatz (float): Jährlicher Zinssatz in Prozent (z. B. 5.0 = 5%).
        jahre (int): Laufzeit in Jahren.

    Returns:
        float: Das berechnete Endkapital, gerundet auf 2 Dezimalstellen.

    Raises:
        ValueError: Wenn Kapital oder Jahre negativ sind.
    """
```

**Wichtig:** Docstrings sind kein Kommentar – sie sind Teil des Python-Objekts und zur Laufzeit über `funktion.__doc__` zugreifbar. PyCharm rendert sie als Tooltip (`Ctrl+Q`). KI-IDEs wie Antigravity nutzen sie als Kontext für präzisere Code-Vorschläge.

---

### 4. Unit Tests: `unittest` vs. `pytest`

Dieses Projekt enthält **beide Ansätze**:

| Aspekt | `unittest` (in `main.py`) | `pytest` (in `tests/`) |
|---|---|---|
| **Herkunft** | Python-Standardbibliothek | Drittanbieter-Paket (Industriestandard) |
| **Java-Ähnlichkeit** | Sehr hoch (`TestCase`, `setUp`) | Niedriger, aber idiomatischer |
| **Testfunktionen** | Methoden in `TestCase`-Klasse | Einfache Funktionen (kein Klassen-Zwang) |
| **Assertions** | `self.assertEqual(a, b)` | `assert a == b` (natives Python!) |
| **Fehlertest** | `with self.assertRaises(T):` | `with pytest.raises(T):` |
| **Parametrisierung** | Manuell oder `subTest` | `@pytest.mark.parametrize` (elegant) |
| **Empfehlung** | Für Verständnis des JUnit-Transfers | Für alle neuen Projekte |

---

## Lernziele

Nach Abschluss dieses Moduls können Studierende:

- eine virtuelle Python-Umgebung (`venv`) anlegen, aktivieren und befüllen
- den Unterschied zwischen globaler und projektlokaler Paketverwaltung erläutern
- `requirements.txt` als Äquivalent zur `pom.xml` einsetzen
- professionelles Logging mit dem `logging`-Modul implementieren und konfigurieren
- Docstrings im Google-Style verfassen und deren Unterschied zu `#`-Kommentaren erklären
- Unit-Tests mit `unittest` schreiben und das Mapping zu JUnit-Konzepten herstellen
- den Industriestandard `pytest` anwenden, inkl. Fixtures und `@pytest.mark.parametrize`
- ein Python-Projekt professionell mit Git versionieren und in PyCharm entwickeln

---

## Java → Python: Das vollständige Tooling-Mapping

| Kategorie | Java-Ökosystem | Python-Ökosystem |
|---|---|---|
| **IDE** | IntelliJ IDEA | PyCharm / VS Code |
| **KI-IDE** | – | Antigravity, Claude Code |
| **Build-Tool** | Maven / Gradle | pip (+ optional: uv, poetry) |
| **Abhängigkeiten** | `pom.xml` / `build.gradle` | `requirements.txt` |
| **Isolation** | Maven Local Repository | `venv` / `.venv` |
| **Testing** | JUnit 5 | pytest (Industriestandard) |
| **Code Coverage** | JaCoCo | pytest-cov |
| **Dokumentation** | Javadoc → HTML | Docstrings + Sphinx → HTML |
| **Logging** | Log4j / Logback | `logging` (Standardbibliothek) |
| **Typprüfung** | Compiler (statisch) | mypy (optional, Modul 7) |
| **Code-Style** | Checkstyle | flake8 / ruff |
| **REST-APIs** | Spring Boot | FastAPI / Flask (Modul 9) |

---


## Das Python-Ökosystem: Drei Schichten
 
Wenn wir von "Ökosystem" sprechen, meinen wir alles, was rund um die Sprache existiert – Werkzeuge, Pakete und Konventionen. Es lässt sich in drei Schichten denken:
 
| Schicht | Was sie enthält | Beispiele |
|---|---|---|
| **1. Standardbibliothek** | Kommt mit Python mit – kein `pip install` nötig | `logging`, `unittest`, `json`, `os`, `datetime` |
| **2. Paket-Ökosystem (PyPI)** | Über 500.000 Pakete auf [pypi.org](https://pypi.org), installiert via `pip` | `pytest`, `FastAPI`, `numpy`, `requests` |
| **3. Tooling** | Werkzeuge rund um den Entwicklungsprozess | `venv`, `pip`, `mypy`, `ruff`, PyCharm |
 
**Der Kulturunterschied zu Java:** Das JDK plus Maven liefert eine sehr vollständige, integrierte Welt. Python bleibt bewusst schlank – man wählt selbst, was man hinzufügt. Das bedeutet mehr Freiheit, aber auch mehr Verantwortung: Ein verwaistes Paket ohne Pflege ist ein echtes Projektrisiko.
 

---
## Kursstruktur (Überblick)

| Modul | Thema | Status |
|---|---|---|
| Modul 1 | Grundlagen & Syntax-Unterschiede | ✅ Verfügbar |
| Modul 2 | Klassen und Objekte vertieft | ✅ Verfügbar |
| Modul 3 | Vererbung und Polymorphismus | ✅ Verfügbar |
| Modul 4 | Pythonische Konzepte ohne Java-Pendant | ✅ Verfügbar |
| Modul 5 | Entwurfsmuster in Python | ✅ Verfügbar |
| Modul 6 | Fehlerbehandlung | ✅ Verfügbar |
| Modul 7 | Typisierung & moderne Python-Praxis | ✅ Verfügbar |
| **Modul 8** | **Werkzeuge & Ökosystem** | ✅ **Dieses Modul** |
| Modul 9 | Abschlussprojekt (REST-API + KI-Integration) | 🔜 Folgt |

