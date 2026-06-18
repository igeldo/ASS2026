# Modul 5 – Präsentation: Pythonische Entwurfsmuster

> Stichpunkt-Notizen zum Üben. **Kein Wort-für-Wort-Skript.** Pro Abschnitt:
> *Thesensatz* (was sagt man, wenn man nur einen Satz hat), *Kernaussagen*
> (Python-zentrisch), *Zu zeigen* (Code-Auszug), *Demo-Output*,
> *Verbaler Bezug* (optionale Speaker-Notes, u. a. für die Frage *"Und in
> Java?"*).
>
> **Zeitbudget gesamt: ~30 Minuten.**
> Richtwert pro Abschnitt: 3–4 Minuten Inhalt + 30 Sekunden Atem/Wechsel.

---

## Setup & Einstieg (2 Min)

**Thesensatz:** *"Pythons Sprachmittel — Module, first-class Klassen und
Funktionen, Dunder-Methoden, Decorators — sind das eigentliche Pattern-
Vokabular. Wir schauen heute, wie sich das in der Praxis zeigt."*

**Aufzubauen:**

- Erinnerung: Gang of Four, 23 Patterns, drei Kategorien (Erzeugung,
  Struktur, Verhalten). Kurz, eine Folie reicht.
- Peter Norvigs These zitieren: *"16 of 23 patterns are invisible or
  simpler in dynamic languages."* (Norvig 1998.)
- Was wir zeigen werden: 3 klassische Patterns (Singleton, Factory,
  Observer) plus Strategy plus Context Manager. Jedes Mal *welcher Python-
  Mechanismus trägt das Pattern* und *wann braucht man es nicht*.
- Zen of Python kurz erwähnen: *"Schön ist besser als hässlich. Einfach
  ist besser als komplex. Lesbarkeit zählt."* Diese drei Sätze rahmen den
  ganzen Vortrag.

**Übergangssatz zum 1. Pattern:** *"Fangen wir mit dem berühmtesten Pattern
an — und zeigen direkt, wo Pythons Mechanismen es klein machen."*

---

## Abschnitt 1: Singleton – klassisch über `__new__` (3 Min)

**Thesensatz:** *"Singleton ist eine Frage — und Python hat mit `__new__`
eine direkte Antwort, und mit dem Modul-System eine noch elegantere."*

**Kernaussagen:**

- Singleton = genau eine Instanz, global zugreifbar. Beispiele: Logger,
  Konfiguration, Verbindungspool.
- Pythons Eingriffspunkt: die Dunder-Methode **`__new__`** — läuft *vor*
  `__init__` und erzeugt das Objekt selbst.
- Eine Klassen-Cache-Variable plus eine Eingriffspunkt-Methode reichen aus.

**Zu zeigen (`modul5_entwurfsmuster.py`, Abschnitt 1):**

```python
class LoggerJavaStil:
    _instanz = None
    def __new__(cls):
        if cls._instanz is None:
            cls._instanz = super().__new__(cls)
            cls._instanz.eintraege = []
        return cls._instanz
```

**Demo-Output (zeigen, nicht vorlesen):**

```
logger_a is logger_b -> True
```

**Wichtige Nebenbemerkung:**
`__init__` läuft jedes Mal – wir initialisieren deshalb in `__new__` einmal,
sonst überschreibt jeder Aufruf die Einträge.

**Mögliche Zwischenfrage:** *"Ist das threadsicher?"* — Antwort: nicht ohne
weiteres. Der GIL schützt einzelne Bytecode-Operationen, aber nicht die
"check-then-act"-Sequenz. Lösung: `threading.Lock()`, oder gleich Modul-
Singleton.

**Verbaler Bezug (Speaker-Note, optional):** Falls Vergleich gefragt wird —
*"Klassisch-statische Sprachen lösen das mit privatem Konstruktor plus
`getInstance()`. Python braucht den privaten Konstruktor gar nicht — der
Eingriffspunkt ist `__new__`."*

**Überleitung:** *"Funktioniert — aber Pythons Modul-System bringt es noch
einfacher."*

---

## Abschnitt 2: Singleton – Pythonisch (4 Min)

**Thesensatz:** *"Pythons Modul-System ist bereits ein Singleton-
Mechanismus. Wer Modul-Variablen verwendet, hat das Pattern ohne eine
einzige Zeile Pattern-Code."*

**Kernaussagen (Variante A – Modul-Singleton):**

- Python cacht jedes Modul beim ersten Import. Variablen auf Modul-Ebene
  existieren **genau einmal** im Prozess.
- Praxis: einfach `from konfiguration import konfiguration` — fertig.
- Das ist die **idiomatische** Antwort. Keine Klasse, keine Methode, kein
  Pattern-Code im engeren Sinn.

**Kernaussagen (Variante B – Decorator-Singleton):**

- Wenn man die Singleton-Eigenschaft sichtbar dokumentieren möchte:
  `@singleton` als Decorator — wiederverwendbar für *jede* Klasse.
- Python-Detail erklären: `@singleton` ist syntaktischer Zucker für
  `Datenbankverbindung = singleton(Datenbankverbindung)`.
- Was zurückkommt, ist **keine Klasse mehr**, sondern eine Funktion, die
  die Klasse "verwaltet". Für den Aufrufer bleibt der Aufruf identisch.

**Zu zeigen:** beide Varianten parallel (`konfiguration` und
`@singleton class Datenbankverbindung`).

**Demo-Output:**

```
db1 is db2 -> True
```

**Kritische Bemerkung am Ende einbauen:**

- Singletons sind in der Python-Community **umstritten**: globaler Zustand
  ist schwer testbar.
- Empfehlung der erfahrenen Python-Welt: lieber Abhängigkeit explizit
  übergeben (*Dependency Injection*).
- Singletons nicht aus Reflex einsetzen — die Frage *"brauche ich das
  wirklich?"* gehört zur pythonischen Denkweise.

**Verbaler Bezug (Speaker-Note, optional):** Falls jemand fragt, warum
Python keine eigene Sprachsyntax für Singletons braucht — *"Weil das
Modul-System es schon liefert. Das, was anderswo Pattern-Code ist, ist
in Python eine Standardeigenschaft des Importsystems."*

**Überleitung:** *"Vom 'gibt es genau eines' zum 'gib mir bitte eines vom
Typ X' — das ist Factory."*

---

## Abschnitt 3: Factory – explizit (3 Min)

**Thesensatz:** *"Eine Factory-Klasse mit `if/elif` funktioniert, wächst
aber mit jeder neuen Variante. Die spannende Frage ist: muss sie wachsen?"*

**Kernaussagen:**

- Problem: Aufrufer kennt nur den Obertyp, will aber eine passende
  konkrete Instanz.
- Bestandteile: abstrakte Basisklasse (`abc.ABC` + `@abstractmethod`),
  konkrete Klassen, Factory-Klasse mit Verzweigung.
- Lesbar, aber Wartung wird mühsam: jede neue Tierart = ein neuer Zweig.

**Zu zeigen (`modul5_entwurfsmuster.py`, Abschnitt 3):**

```python
class Tier(ABC):
    @abstractmethod
    def laut(self) -> str: ...

class TierFactoryJavaStil:
    @staticmethod
    def erzeuge(art):
        if art == "hund":    return Hund()
        elif art == "katze": return Katze()
        ...
```

**Was hier zu kritisieren ist:**

- `if/elif`-Kette wächst mit jeder neuen Tierart.
- Bei 30 Tierarten — 30 Zweige.
- Beispiel im Demo: Fehlerfall `"drache"` löst `ValueError` aus.

**Verbaler Bezug (Speaker-Note, optional):** Diese Art Factory ist der
direkte Weg, den die meisten statisch-typisierten Sprachen ebenfalls
nehmen würden. Wir zeigen sie hier vor allem als Kontrastfolie zum
nächsten Abschnitt.

**Übergangssatz:** *"Python kann das offensichtlich besser — weil Klassen
in Python einfache Objekte sind."*

---

## Abschnitt 4: Factory – Pythonisch (4 Min)

**Thesensatz:** *"Wenn Klassen Objekte sind, kann ich sie in ein Dict
stecken. Dann ist die Factory ein einzeiliger Lookup."*

**Kernaussagen (Variante A – Dict-Dispatch):**

- *"Klassen sind first-class Objekte"* — als zentralen Satz aussprechen.
- Klasse in ein Dict legen, beim Erzeugen nachschlagen und aufrufen:
  `_TIER_REGISTRY[art]()`.
- Drei Vorteile gegenüber `if/elif`:
  1. neue Tierart = eine neue Dict-Zeile, Factory-Funktion unverändert,
  2. O(1)-Lookup statt O(n),
  3. Plugins können sich nachträglich registrieren
     (`_TIER_REGISTRY["drache"] = Drache`).

**Kernaussagen (Variante B – `@classmethod`-Factory):**

- Wenn die Varianten **schon zur Programmierzeit feststehen** und nur
  *bequemer Konstruktor* gewollt ist: direkt in die Klasse.
- Beispiel `Pizza.margherita()`, `Pizza.salami()` — liest sich wie der
  Domänen-Wortschatz.

**Zu zeigen:** `erzeuge_tier()` und `Pizza.margherita()`.

**Demo-Output:**

```
erzeuge_tier('hund') -> Hund('Wuff')
Pizza.margherita()   -> Pizza(Tomate, Mozzarella, Basilikum)
```

**Faustregel laut aussprechen:**

- *String/Enum zur Laufzeit?* → Dict-Dispatch.
- *Auswahl steht zur Programmierzeit fest?* → `@classmethod`.

**Wo das in Python begegnet:** `dict.fromkeys`, `datetime.fromisoformat`,
Plugin-Systeme mit `entry_points`.

**Überleitung:** *"Bisher ging es um *Erzeugung* von Objekten. Jetzt zu
Kommunikation zwischen Objekten — Observer."*

---

## Abschnitt 5: Observer (4 Min)

**Thesensatz:** *"Alles, was aufrufbar ist, ist ein Callable. Eine Liste
von Callables ist alles, was ein Observer-Pattern in Python braucht."*

**Kernaussagen:**

- Begriff einführen: **Callable** — alles, was man mit `(...)` aufrufen
  kann. Funktion, Lambda, gebundene Methode, Objekt mit `__call__`.
- Newsletter hält eine Liste von Callables — kein gemeinsames Interface
  nötig.
- Demo zeigt drei Beobachter-Varianten:
  1. normale Funktion (`auf_konsole`),
  2. Lambda (`lambda s: archiv.append(s)`),
  3. Objekt mit `__call__` (`ZaehlenderAbonnent`).

**Zu zeigen (`main_modul5.py`, Abschnitt 5):**

```python
news.abonnieren(auf_konsole)
news.abonnieren(archivieren)         # Lambda
news.abonnieren(zaehler)             # Objekt mit __call__
news.veroeffentlichen("Ausgabe Mai 2026")
```

**Demo-Output:**

```
Newsletter(Abonnenten=3)
[Konsole]   Ausgabe Mai 2026
Archiv:  ['Ausgabe Mai 2026', 'Sonderausgabe']
Zähler:  ZaehlenderAbonnent(Statistik, empfangen=2)
```

**Was sich pädagogisch anbietet zu sagen:**

- Das ist **Observer + Duck Typing** zusammen.
- Drei völlig unterschiedliche Beobachter, verbunden allein durch die
  Eigenschaft "aufrufbar".

**Verbaler Bezug (Speaker-Note, optional):** Statisch-typisierte Sprachen
brauchen für genau diesen Fall ein Listener-Interface plus eine
Implementierungsklasse pro Beobachter. Python überspringt das.

**Wo das in Python begegnet:** `signal.signal(SIGINT, handler)`, GUI-
Bibliotheken wie `tkinter`/`PyQt`, Signal-Frameworks wie `blinker`.

**Überleitung:** *"Wenn Funktionen Beobachter sein können — können sie
auch Strategien sein."*

---

## Abschnitt 6: Strategy (3 Min)

**Thesensatz:** *"Strategy ist in Python so unsichtbar geworden, dass
keiner es mehr Pattern nennt — wir nennen es einfach 'Funktion
übergeben'."*

**Kernaussagen:**

- Eine Strategie ist eine Funktion. Eine parametrisierte Strategie ist
  eine Funktion, die eine Funktion zurückgibt — eine **Closure**.
- `prozent_rabatt(10)` gibt eine *Funktion* zurück, die den Wert `10`
  "behält". Pythons Antwort auf eine parametrisierte Strategie-Klasse —
  ohne Klasse.
- Strategie zur Laufzeit austauschen: einfach Attribut neu zuweisen.

**Zu zeigen:**

```python
korb = Warenkorb(prozent_rabatt(10))
korb.strategie = prozent_rabatt(20)          # zur Laufzeit wechseln
```

**Wo das in der Standardbibliothek begegnet (kurz erwähnen):**

```python
sorted(personen, key=lambda p: p.alter)       # Strategie als key
threading.Thread(target=mein_job)             # Strategie = was getan wird
heapq.nlargest(5, daten, key=...)             # ebenfalls Strategie
```

- *"Jedes `key=`-Argument ist im Kern ein Strategy."*

**Verbaler Bezug (Speaker-Note, optional):** Sprachen ohne first-class
Funktionen brauchen für das gleiche Pattern ein Interface plus eine
Klasse pro Strategie.

**Überleitung:** *"Letztes Pattern — und das einzige, für das Python ein
eigenes Sprachmittel mitbringt, das so allgemein ist wie in kaum einer
anderen Sprache: der Context Manager."*

---

## Abschnitt 7: Context Manager (4 Min)

**Thesensatz:** *"`with` ist Pythons allgemeiner Mechanismus für 'jetzt
etwas tun, danach garantiert aufräumen'. Datei-Handling ist nur das
bekannteste Beispiel."*

**Kernaussagen:**

- Problem: garantiert aufräumen, auch bei Exceptions. Datei, Lock,
  Transaktion, Zeitmessung, Mock im Test, temporäres Verzeichnis.
- Jedes Objekt mit `__enter__` und `__exit__` passt hinter `with`.
- `__exit__` läuft **garantiert** — das ist der eigentliche Wert.

**Zu zeigen – Variante A (Klasse):**

```python
class Zeitmessung:
    def __enter__(self): ...
    def __exit__(self, exc_typ, exc_wert, exc_tb): ...

with Zeitmessung("Berechnung") as m:
    ...
```

- `__exit__` bekommt 3 Argumente (Typ/Wert/Traceback der Exception oder
  jeweils `None`).
- Rückgabewert `True` würde die Exception unterdrücken. Standard: `False`.

**Zu zeigen – Variante B (`@contextmanager`):**

```python
from contextlib import contextmanager

@contextmanager
def transaktion(name):
    print("[TX] beginnt")
    try:
        yield name
        print("[TX] COMMIT")
    except Exception as fehler:
        print("[TX] ROLLBACK")
        raise
```

- `yield` trennt Setup (`__enter__`) von Teardown (`__exit__`).
- Bei Exception: springt in `except` der Generator-Funktion.

**Demo-Output (besonders der Fehlerfall ist eindrucksvoll):**

```
[TX] 'Buchung 43' beginnt
[TX] 'Buchung 43' ROLLBACK wegen: Konto gesperrt
Aufrufer fängt: Konto gesperrt
```

→ `__exit__` läuft **garantiert**, der Aufrufer kann die Exception
trotzdem behandeln.

**Eingebaute Context Manager auflisten (3 Beispiele reichen):**

```python
with open("a.txt") as f: ...
with threading.Lock(): ...
with mock.patch("modul.funktion"): ...
```

**Kernbotschaft:** `with` ist **allgemeines Sprachmittel** für Setup-
Teardown-Strukturen — Datei-Handling ist nur ein Spezialfall davon.

**Verbaler Bezug (Speaker-Note, optional):** Andere Sprachen haben oft
ein eingeschränktes Pendant (z. B. `try-with-resources`), das nur fürs
Schließen gemacht ist. Pythons Variante ist verallgemeinert: Zeit­messung,
Mocks, Verzeichnisse, Transaktionen — alles passt rein.

---

## Abschluss (2 Min)

**Thesensatz (Klammer schließen):** *"Pythonische Lösungen nutzen die
Sprache, nicht das Pattern. Frag dich: welcher Mechanismus trägt das
Pattern? — dann benutze ihn direkt."*

**Tabelle zusammenfassen:**

| Pattern | Python-Mechanismus | Idiomatik |
|---|---|---|
| Singleton | Modul-System, `__new__` | Modul-Attribut |
| Factory | Klassen als first-class Objekte | Dict-Dispatch, `@classmethod` |
| Observer | Callables, `__call__` | Liste von Callbacks |
| Strategy | Funktionen als first-class Werte | Funktion als Argument |
| Context Manager | `__enter__`/`__exit__`, `@contextmanager` | `with`, vielseitig |

**Wiederkehrende Werkzeuge laut aussprechen:** first-class Funktionen,
first-class Klassen, Modul-System, Dunder-Methoden, Decorators.

**Mögliche Nächste-Schritte-Folie:**

- Modul 6 (Fehlerbehandlung) baut direkt auf Context Manager auf.
- Modul 7 (typing/Protokolle) liefert die typtechnische Antwort darauf,
  wenn man strukturelle Schnittstellen explizit haben möchte.

**Schlussgeste:** Frage an die Hörer: *"An welcher Stelle in eurem
letzten Java-Projekt hättet ihr lieber einen pythonischen Mechanismus
gehabt?"* — eröffnet die Diskussion.

---

## Pacing-Übersicht

| Abschnitt | Inhalt | Zielzeit |
|---|---|---|
| Einstieg | Pattern-Definition, Norvig-These, Zen of Python | 2 Min |
| 1 | Singleton via `__new__` | 3 Min |
| 2 | Singleton Pythonisch (Modul + Decorator) | 4 Min |
| 3 | Factory explizit | 3 Min |
| 4 | Factory Pythonisch | 4 Min |
| 5 | Observer | 4 Min |
| 6 | Strategy | 3 Min |
| 7 | Context Manager | 4 Min |
| Abschluss | Tabelle + Frage | 2 Min |
| **Gesamt** | | **29 Min** |

**Puffer-Plan, falls die Zeit knapp wird:**

- Abschnitt 1 (Singleton via `__new__`) **kürzen** — das Pattern selbst
  ist schnell erklärt, die Modul-Variante in Abschnitt 2 ist die
  eigentlich pythonische Aussage.
- Demo-Output in Abschnitt 7 weglassen, nur den Fehlerfall mündlich
  beschreiben.

**Falls Zeit übrig ist:**

- Decorator-Registrierung als Bonus zur Factory zeigen (siehe Lehrbuch 5.2).
- Eingebaute Context-Manager-Beispiele länger demonstrieren
  (`tempfile.TemporaryDirectory`, `mock.patch`).

---

## Wahrscheinliche Fragen aus dem Publikum

| Frage | Kurze Antwort |
|---|---|
| *Sind Singletons threadsicher?* | Nicht ohne weiteres. Modul-Singleton ist sicher, weil das Importsystem die Initialisierung serialisiert; `__new__`-Variante braucht `threading.Lock()`. |
| *Wann nehme ich Dict-Dispatch, wann `@classmethod`?* | Laufzeit-Auswahl per String → Dict. Programmierzeit-Auswahl → `@classmethod`. |
| *Was ist mit Lambdas mit mehreren Zeilen?* | Geht in Python nicht direkt — stattdessen normale Funktion definieren und übergeben. |
| *Sind `@contextmanager`-Funktionen langsamer als Klassen?* | Marginaler Overhead, in der Praxis irrelevant. Lesbarkeit gewinnt. |
| *Warum kein Builder?* | Python hat Keyword-Argumente und Default-Werte — Builder ist meistens überflüssig. |
| *Was ist mit Abstract Factory?* | Dieselbe Logik wie Factory, nur mit Familien von Klassen. Dict-Dispatch mit verschachtelten Dicts. |
| *Und in Java?* | Knappe Antwort: die meisten dieser Patterns brauchen dort eigenes Boilerplate — Interfaces, statische Methoden, Initialisierungsklassen. Genau diesen Boilerplate spart Python ein. |

---

## Persönliche Hinweise zum Üben

- **Vor dem Vortrag mindestens einmal `python main_modul5.py` laufen
  lassen** und den Output lesen — das prägt sich besser ein als Folien.
- *"first-class"* ist der zentrale Begriff — beim Üben absichtlich oft
  verwenden, damit er sich festsetzt.
- Bei *"Wo begegnet einem das in Python?"*-Stellen: ein konkretes Beispiel
  aus der Standardbibliothek pro Pattern parat haben, dann wirkt der
  Vortrag verankert statt theoretisch.
- Wenn eine Frage kommt, deren Antwort man nicht weiß: ehrlich sagen
  *"Das schaue ich nach"* — nicht raten. Wir haben gerade ein Pattern-Modul
  gegeben, in dem Klarheit das wichtigste Argument war.
