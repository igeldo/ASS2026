# Modul 5 – Pythonische Entwurfsmuster

> *"Schön ist besser als hässlich. Einfach ist besser als komplex.
> Lesbarkeit zählt."* — aus *The Zen of Python* (Tim Peters)
>
> Entwurfsmuster sind eine Antwort auf die Frage, wie man wiederkehrende
> Probleme robust strukturiert. Pythons Sprachmittel — Module, first-class
> Klassen und Funktionen, Dunder-Methoden, Decorators — verändern aber, was
> "robust" überhaupt heißt. Viele Patterns werden in Python kürzer, manche
> verschwinden ganz im Sprachkern, und einige wenige (Context Manager)
> erleben in Python ihren idiomatischsten Ausdruck.

## Lernziele

Nach Durcharbeitung dieses Moduls können Studierende

- die drei klassischen Patterns Singleton, Factory und Observer pythonisch
  umsetzen — und benennen, **welcher Sprachmechanismus** sie jeweils trägt,
- erklären, warum Python für einige Patterns kaum Boilerplate braucht
  (first-class Funktionen, Klassen als Objekte, Modul-System),
- entscheiden, wann ein Pattern in Python **überflüssig** ist (Strategy mit
  einer einfachen Funktion, Singleton durch ein Modul-Attribut),
- Context Manager als verallgemeinerten Mechanismus für *"etwas muss
  zuverlässig danach passieren"* einsetzen.

---

## 5.0 Was ist ein Entwurfsmuster?

Ein **Entwurfsmuster** (engl. *design pattern*) ist eine bewährte,
sprach­unabhängige Schablone für ein wiederkehrendes Entwurfsproblem. Der
Klassiker ist das Buch *"Design Patterns: Elements of Reusable Object-
Oriented Software"* (1994) der sogenannten **Gang of Four** (Gamma, Helm,
Johnson, Vlissides) mit 23 Patterns in drei Kategorien:

| Kategorie | Frage | Beispiele |
|---|---|---|
| Erzeugungsmuster | Wie entstehen Objekte? | **Singleton, Factory**, Builder, Prototype |
| Strukturmuster | Wie passen Objekte zusammen? | Adapter, Decorator, Composite |
| Verhaltensmuster | Wie kommunizieren Objekte? | **Observer, Strategy**, Command, Iterator |

Die Patterns wurden ursprünglich vor allem für statisch typisierte,
klassen­basierte Sprachen formuliert. Pythons dynamisches Typsystem und seine
"first-class everything"-Philosophie verändern den Werkzeugkasten — viele
Patterns wirken in Python kleiner, weil die Sprache bereits zur Verfügung
stellt, was anderswo Pattern-Code erst herstellt.

> **Peter Norvigs These (1998):** *"16 of the 23 patterns are either invisible
> or simpler in dynamic languages."* — wir werden in diesem Modul anhand von
> fünf Patterns sehen, was er damit meint.

### Pythons Werkzeugkasten – das Vokabular dieses Moduls

Vier Sprachmittel tauchen in fast jedem Pattern dieses Moduls wieder auf —
wer sie kennt, hat den größten Teil der Patterns schon "im Griff":

- **Modul-System.** Jedes Modul wird beim ersten Import gecached. Variablen
  auf Modul-Ebene existieren genau einmal im Prozess.
- **First-class Funktionen und Klassen.** Beide sind Werte, die in
  Variablen, Listen, Dicts gespeichert oder als Argument übergeben werden
  können.
- **Dunder-Methoden.** `__new__`, `__call__`, `__enter__`, `__exit__` und
  andere sind dokumentierte Erweiterungspunkte des Sprach-Interpreters.
- **Decorators.** Funktionen, die andere Funktionen oder Klassen entgegen­
  nehmen und etwas Erweitertes zurückgeben.

---

## 5.1 Singleton

### Das Problem

Manchmal soll es von einer Klasse **genau eine** Instanz geben – einen
Logger, einen Konfigurations-Container, einen Verbindungspool. Wer eine
"neue" Instanz anfordert, soll dieselbe bekommen.

### Pythonisch lösen

Pythons Modul-System cacht jedes Modul beim ersten Import. Variablen auf
Modul-Ebene existieren damit **automatisch genau einmal**. Das ist der
eigentliche pythonische Singleton-Mechanismus — und er kommt ohne ein
einziges Pattern auskommendes Codestück aus.

### Variante 1: Modul-Singleton (Standardfall)

```python
# datei: konfiguration.py
class _Konfiguration:
    def __init__(self):
        self.sprache = "de"
        self.debug = False

konfiguration = _Konfiguration()       # einmal beim Import erzeugt
```

```python
# datei a.py
from konfiguration import konfiguration
konfiguration.debug = True

# datei b.py – sieht dieselbe Instanz
from konfiguration import konfiguration
print(konfiguration.debug)             # True
```

Kein Pattern-Code, keine `getInstance()`-Methode. **Das Sprachsystem
erledigt es.**

### Variante 2: `__new__` als expliziter Eingriffspunkt

Wer den Singleton-Charakter direkt in der Klasse verankern möchte, hängt
sich in `__new__` ein — die Dunder-Methode, die das Objekt erzeugt (vor
`__init__`).

```python
class LoggerJavaStil:
    _instanz: "LoggerJavaStil | None" = None

    def __new__(cls):
        if cls._instanz is None:
            cls._instanz = super().__new__(cls)
            cls._instanz.eintraege = []
        return cls._instanz

    def log(self, nachricht: str) -> None:
        self.eintraege.append(nachricht)
```

```python
a = LoggerJavaStil()
b = LoggerJavaStil()
a is b              # True – dasselbe Objekt
```

Drei Dinge sollte man wissen:

- `__init__` läuft bei jedem Aufruf **erneut**. Wir initialisieren deshalb
  in `__new__` und nur einmal (über die `is None`-Prüfung).
- Threadsicher ist das **nicht**. Der GIL schützt einzelne Bytecode-
  Operationen, aber nicht zwei aufeinanderfolgende Zugriffe. Wer
  Threadsicherheit braucht: `threading.Lock()` um die Erzeugung legen — oder
  besser gleich den Modul-Singleton nehmen, der durch das Import-System
  ohnehin nur einmal entsteht.
- Vererbung wird unangenehm: alle Unterklassen würden sich dieselbe
  `_instanz`-Variable teilen, wenn man nicht aufpasst.

### Variante 3: `@singleton`-Decorator

Decorators sind Funktionen, die eine Klasse (oder Funktion) entgegennehmen
und etwas Erweitertes zurückgeben. Hier eine wiederverwendbare Singleton-
Variante:

```python
def singleton(klasse):
    instanzen = {}
    def hole_instanz(*args, **kwargs):
        if klasse not in instanzen:
            instanzen[klasse] = klasse(*args, **kwargs)
        return instanzen[klasse]
    return hole_instanz

@singleton
class Datenbankverbindung:
    def __init__(self, dsn="lokal://default"):
        self.dsn = dsn
```

`@singleton` ist Syntax für *"wende `singleton` auf `Datenbankverbindung`
an"*. Was zurückkommt, ist `hole_instanz` — **keine Klasse mehr, sondern
eine Funktion**, die die Klasse zwischenspeichert. Aus Sicht des Aufrufers
bleibt `Datenbankverbindung(...)` unverändert.

### Wo das in Python begegnet

Pythons Standardbibliothek verwendet implizit Modul-Singletons an vielen
Stellen:

- `sys.modules` – das globale Modul-Cache-Dict ist selbst ein Singleton.
- `logging.getLogger("name")` – gibt für denselben Namen immer denselben
  Logger zurück.
- `random.random()` – arbeitet auf einer Modul-internen `Random`-Instanz.

### Wann welche Variante?

| Variante | Empfehlung |
|---|---|
| **Modul-Singleton** | Standardfall. Praktisch immer die richtige Wahl. |
| **`@singleton`-Decorator** | Wenn die Singleton-Eigenschaft sichtbar im Klassen-Header dokumentiert werden soll. |
| **`__new__`-Variante** | Akademisch interessant, in der Praxis selten nötig. |
| **Metaklassen-Singleton** | Existiert auch — `type` selbst überschreiben — wird für nahezu alle Anwendungsfälle überdimensioniert. |

### Wann braucht man das Pattern *nicht*?

Singletons sind in der Python-Community **umstritten**: sie sind globaler
Zustand, schwer testbar, schwer zu mocken. Wer den vermeintlich
"einzigen" Wert lieber explizit als Argument übergibt, bekommt:

- **Testbarkeit** — im Test einfach eine Fake-Instanz übergeben.
- **Lesbarkeit** — der Datenfluss steht im Code, nicht implizit im Import.
- **Mehrere Instanzen** — falls sich später herausstellt, dass zwei
  Konfigurationen nebeneinander gebraucht werden.

> **Faustregel:** Singletons benutzen, weil "man das so macht", ist
> ein Reflex aus statisch-typisierten Sprachen. In Python lohnt sich jedes
> Mal die Frage *"brauche ich das wirklich?"*.

---

## 5.2 Factory

### Das Problem

Der Aufrufer soll ein Objekt eines passenden Untertyps bekommen, ohne den
konkreten Typ zu kennen. Beispiel: *"Gib mir ein Tier vom Typ `'hund'`."*
Die Aufrufseite weiß nichts von der Klasse `Hund` – nur von `Tier`.

### Pythonisch lösen

Klassen sind in Python **first-class Objekte**: man kann sie in Listen oder
Dicts speichern und ganz normal aufrufen. Damit wird aus der Factory ein
Lookup statt einer Verzweigung.

### Variante 1: explizit mit `if/elif`

Der direkte Weg — eine Factory-Klasse mit Verzweigungen:

```python
from abc import ABC, abstractmethod

class Tier(ABC):
    @abstractmethod
    def laut(self) -> str: ...

class Hund(Tier):
    def laut(self): return "Wuff"

class Katze(Tier):
    def laut(self): return "Miau"

class TierFactoryJavaStil:
    @staticmethod
    def erzeuge(art: str) -> Tier:
        if art == "hund":    return Hund()
        elif art == "katze": return Katze()
        else: raise ValueError(f"Unbekannte Tierart: {art!r}")
```

Lesbar — aber jede neue Tierart erzwingt eine neue Code-Zeile in der
Factory.

### Variante 2: Dict-Dispatch (Registry)

```python
_TIER_REGISTRY: dict[str, type[Tier]] = {
    "hund":  Hund,
    "katze": Katze,
    "kuh":   Kuh,
}

def erzeuge_tier(art: str) -> Tier:
    if art not in _TIER_REGISTRY:
        raise ValueError(f"Unbekannte Tierart: {art!r}")
    return _TIER_REGISTRY[art]()       # Klasse aufrufen = Instanziieren
```

**Vorteile gegenüber `if/elif`:**

- Neue Tierart? Eine Zeile im Dict – die Factory-Funktion bleibt unverändert.
- Lookup ist O(1) statt O(n) – belanglos bei drei Einträgen, relevant bei 50.
- Plugins können sich nachträglich registrieren: `_TIER_REGISTRY["drache"] = Drache`.

**Decorator-Variante** (für Fortgeschrittene): jede Klasse "meldet sich
selbst" an.

```python
TIERE: dict[str, type[Tier]] = {}

def registriere(art):
    def deco(klasse):
        TIERE[art] = klasse
        return klasse
    return deco

@registriere("hund")
class Hund(Tier):
    def laut(self): return "Wuff"

@registriere("katze")
class Katze(Tier):
    def laut(self): return "Miau"
```

Frameworks wie Django und Flask funktionieren genau auf dieser Idee.

### Variante 3: `@classmethod` als alternativer Konstruktor

Wer nur **wenige, gut benannte** Varianten erzeugen möchte, braucht keine
Factory-Klasse: die Erzeugungslogik gehört direkt in die Klasse.

```python
class Pizza:
    def __init__(self, belaege: list[str]):
        self.belaege = belaege

    @classmethod
    def margherita(cls) -> "Pizza":
        return cls(["Tomate", "Mozzarella", "Basilikum"])

    @classmethod
    def salami(cls) -> "Pizza":
        return cls(["Tomate", "Mozzarella", "Salami"])
```

```python
p1 = Pizza.margherita()
p2 = Pizza.salami()
```

`Pizza.margherita()` liest sich wie Domänen-Vokabular — näher am
Anwendungsproblem als ein Lookup mit einer Zeichenkette.

### Wo das in Python begegnet

- `dict.fromkeys(seq)`, `dict.from_keys(seq, value)` – `@classmethod`-Factory.
- `datetime.fromisoformat(s)`, `datetime.fromtimestamp(t)` – alternative
  Konstruktoren als `@classmethod`.
- `json.loads` / `pickle.loads` – Funktionen, die je nach Inhalt verschiedene
  Klassen erzeugen.
- Plugin-Systeme über `entry_points` in `pyproject.toml` – im Kern eine
  laufzeit-erweiterte Registry.

### Wann welche Variante?

> **Faustregel:** Wenn die Auswahl per **String/Enum zur Laufzeit** kommt –
> Dict-Dispatch. Wenn die Auswahl **zur Programmierzeit** feststeht und nur
> bequeme Konstruktoren gewollt sind – `@classmethod`.

### Wann braucht man das Pattern *nicht*?

Bei nur einer Klasse oder wenn der Aufrufer den konkreten Typ ohnehin
kennt, ist eine Factory überflüssig — der direkte Konstruktor reicht.
Pythonischer Pragmatismus: nicht abstrahieren, was nicht abstrahiert
werden muss.

---

## 5.3 Observer

### Das Problem

Ein Objekt (Subject / Publisher) hält andere (Observer / Subscriber) auf
dem Laufenden, ohne sie konkret zu kennen. Beispiele: Newsletter-Versand,
Event-Bus, MVC-Updates.

### Pythonisch lösen

Alles, was man mit `(...)` aufrufen kann, ist ein **Callable**: gewöhnliche
Funktion, Lambda, gebundene Methode oder Objekt mit `__call__`. Der
Newsletter braucht damit kein gemeinsames Interface für seine Abonnenten —
nur eine Liste von Callables.

```python
from typing import Callable

class Newsletter:
    def __init__(self):
        self._abonnenten: list[Callable[[str], None]] = []

    def abonnieren(self, callback):
        self._abonnenten.append(callback)

    def veroeffentlichen(self, ausgabe):
        for callback in self._abonnenten:
            callback(ausgabe)
```

Jetzt darf **alles Aufrufbare** Beobachter sein:

```python
def auf_konsole(s):
    print(s)

archiv = []
news = Newsletter()
news.abonnieren(auf_konsole)
news.abonnieren(lambda s: archiv.append(s))     # Lambda
news.abonnieren(print)                          # eingebaute Funktion
news.veroeffentlichen("Hallo")
```

Drei verschiedene Abonnenten — verbunden allein durch die Eigenschaft,
aufrufbar zu sein.

### Observer mit Zustand: `__call__`

Falls ein Beobachter Zustand mitschleppen muss, definiert man eine ganz
normale Klasse — und macht sie mit `__call__` aufrufbar:

```python
class ZaehlenderAbonnent:
    def __init__(self, name):
        self.name = name
        self.empfangen = 0

    def __call__(self, ausgabe):
        self.empfangen += 1
```

```python
zaehler = ZaehlenderAbonnent("Statistik")
news.abonnieren(zaehler)        # zaehler ist aufrufbar wie eine Funktion
```

`__call__` ist der Dunder-Mechanismus dahinter — das Sprach-Feature, das
"Objekt sieht aus wie eine Funktion" zur Vertrags­bedingung macht.

### Wo das in Python begegnet

- `tkinter` und `PyQt` arbeiten in ihrem GUI-Kern mit Callbacks-Listen für
  Events.
- `signal.signal(SIGINT, handler)` – die Standardbibliothek nimmt direkt
  ein Callable als Handler entgegen.
- Bibliotheken wie `blinker` und `pydispatch` packen das Pattern in
  einsatzfertige Signal-Frameworks.
- `dataclasses.field(default_factory=list)` – auch hier ein Callable als
  Parameter, kein gemeinsames Interface.

### Wann braucht man das Pattern *nicht*?

Wenn nur **ein** Beobachter existiert, reicht ein einfacher Methoden-
Aufruf. Wenn Beobachter und Subject im gleichen Modul wohnen, ist eine
direkte Funktion oft klarer als eine vorbereitete Abonnement-Schicht.
Pythons Devise *"explizit ist besser als implizit"* warnt vor zu vielen
versteckten Signalwegen.

---

## 5.4 Strategy

### Das Problem

Ein Algorithmus soll **zur Laufzeit** austauschbar sein. Klassiker:
verschiedene Rabatt-Berechnungen, Sortier-Kriterien, Komprimierungs-Verfahren.

### Pythonisch lösen

Funktionen sind in Python first-class Werte. Eine "Strategie" ist deshalb
keine Klassenhierarchie, sondern schlicht eine Funktion. Eine
parametrisierbare Strategie? Eine Funktion, die eine Funktion zurückgibt —
das nennt man **Closure**, denn die zurückgegebene Funktion *schließt*
ihren Geltungsbereich um die übergebenen Werte.

```python
def kein_rabatt(preis: float) -> float:
    return preis

def prozent_rabatt(prozent: float):
    def anwenden(preis: float) -> float:
        return preis * (1 - prozent / 100)
    return anwenden

class Warenkorb:
    def __init__(self, strategie = kein_rabatt):
        self.artikel = []
        self.strategie = strategie

    def gesamtpreis(self):
        roh = sum(preis for _, preis in self.artikel)
        return self.strategie(roh)
```

```python
korb = Warenkorb(prozent_rabatt(10))            # 10 % Rabatt
korb.strategie = prozent_rabatt(20)             # zur Laufzeit wechseln
```

`prozent_rabatt(10)` gibt eine **Funktion** zurück, die den Wert `10` in
ihrem Geltungsbereich behält — das ist Pythons Antwort auf eine
parametrisierte Strategie-Klasse, kompakt in fünf Zeilen.

### Wo das in Python begegnet

Strategy ist in Python so verbreitet, dass es kaum noch als Pattern
erkannt wird — es ist einfach *Funktionen übergeben*:

```python
sorted(personen, key=lambda p: p.alter)         # key = Strategie
list(map(str.upper, namen))                     # Strategie als Transformation
threading.Thread(target=mein_job).start()       # Strategie = was getan wird
heapq.nlargest(5, daten, key=lambda x: x.preis) # ebenfalls Strategie
```

Jedes `key=`-Argument, jedes `target=`-Argument, jeder `lambda` ist im
Kern ein Strategy-Pattern.

### Wann braucht man das Pattern *nicht*?

Wenn es **nur eine** mögliche Strategie gibt, ist die Indirektion
überflüssig. Pythonisch: erst beim zweiten Strategie-Bedarf einen Parameter
einführen — vorher inline schreiben. *"You ain't gonna need it."*

---

## 5.5 Context Manager

### Das Problem

Manche Operationen brauchen **garantiertes Aufräumen** – egal ob der
Block erfolgreich war oder eine Exception geflogen ist. Datei schließen,
Lock freigeben, Verbindung trennen, Transaktion zurückrollen, Zeit messen,
Mock im Test zurücknehmen.

### Pythonisch lösen

`with`-Statement plus zwei Dunder-Methoden: jedes Objekt mit `__enter__`
und `__exit__` darf hinter `with` stehen. `__exit__` läuft **garantiert** –
auch wenn im Block eine Exception fliegt.

### Variante 1: Klasse mit `__enter__`/`__exit__`

```python
class Zeitmessung:
    def __init__(self, label):
        self.label = label
        self.dauer_ms = 0.0

    def __enter__(self):
        import time
        self._start = time.perf_counter()
        return self                                    # bindet an "as"-Variable

    def __exit__(self, exc_typ, exc_wert, exc_tb):
        import time
        self.dauer_ms = (time.perf_counter() - self._start) * 1000
        return False                                   # Exception nicht schlucken
```

```python
with Zeitmessung("Berechnung") as m:
    summe = sum(i*i for i in range(1_000_000))
print(f"Dauer: {m.dauer_ms:.2f} ms")
```

**Die drei Argumente von `__exit__`** sind:

- `exc_typ` – die Exception-Klasse (`None` bei Erfolg),
- `exc_wert` – die Exception-Instanz,
- `exc_tb` – das Traceback-Objekt.

Ein **Rückgabewert `True`** würde die Exception als "behandelt" markieren
und unterdrücken. `False` (oder `None`) reicht sie weiter — das ist fast
immer das richtige Verhalten.

### Variante 2: `@contextmanager`

Wer keine ganze Klasse schreiben möchte: `contextlib.contextmanager` macht
aus einer Generator-Funktion einen Context Manager.

```python
from contextlib import contextmanager

@contextmanager
def transaktion(name):
    print(f"[TX] '{name}' beginnt")
    try:
        yield name                          # alles vor yield: __enter__
        print(f"[TX] '{name}' COMMIT")      # alles nach yield: __exit__
    except Exception as fehler:
        print(f"[TX] '{name}' ROLLBACK wegen: {fehler}")
        raise
```

```python
with transaktion("Buchung 42") as tx:
    # ... Arbeit ...
    pass
```

`yield` trennt **Setup** von **Teardown**. Eine Exception im `with`-Block
springt direkt zum `except` der Generator-Funktion. **`raise` am Ende** ist
wichtig — sonst schluckt der Context Manager die Exception still.

### Wo das in Python begegnet

`with` ist in der Standardbibliothek allgegenwärtig:

```python
with open("a.txt") as f: ...                  # Datei schließen
with threading.Lock(): ...                    # Lock freigeben
with sqlite3.connect("db") as c: ...          # Transaktion / close
with tempfile.TemporaryDirectory() as d: ...  # Verzeichnis aufräumen
with mock.patch("modul.funktion"): ...        # Mock im Test rückgängig
with open("a.txt") as a, open("b.txt") as b:  # mehrere Ressourcen
    ...
```

Auch *async* hat eine eigene Variante (`async with`) für asynchrone
Ressourcen wie Netzwerkverbindungen oder Datenbank-Sessions.

### Wann braucht man das Pattern *nicht*?

Bei Operationen, die nur reine Berechnungen sind und keine externen
Ressourcen anfassen, ist `with` überflüssig. Wer einen Wert lediglich für
einen Block braucht, schreibt eine Funktion oder eine lokale Variable —
keinen Context Manager.

> **Kernlehre:** `with` ist Pythons allgemeiner Mechanismus für *"jetzt
> etwas tun, danach garantiert aufräumen"*. Datei-Handling ist nur das
> bekannteste Beispiel — die eigentliche Stärke liegt in der Vielfalt der
> Anwendungsfälle.

---

## 5.6 Was wir bewusst weggelassen haben

Aus Zeit­gründen (30 Minuten) nicht in dieser Modul-Einheit:

- **Iterator** – in Python via `__iter__`, `__next__` und Generatoren mit
  `yield` so tief in die Sprache eingebaut, dass das Pattern fast
  unsichtbar wird.
- **Decorator (das Pattern, nicht die `@`-Syntax)** – konzeptuell verwandt
  mit Pythons Funktions-Decorator, würde eine eigene Stunde brauchen.
- **Command, Template Method, Adapter, Composite, State** – klassische
  GoF-Patterns, in Python aber oft unauffällig (Funktion statt
  Command-Klasse) oder durch Duck Typing trivial (Adapter).
- **Metaklassen-Singleton** – existiert, ist aber für die meisten
  Anwendungsfälle überdimensioniert.

Für Interessierte: Brandon Rhodes' Sammlung *"Python Patterns"* online
und Peter Norvigs *"Design Patterns in Dynamic Languages"* sind die
Standard-Referenzen.

---

## 5.7 Zusammenfassung

| Pattern | Python-Mechanismus | Pythonische Idiomatik |
|---|---|---|
| Singleton | Modul-System, `__new__`, Decorator | Modul-Attribut, selten `@singleton` |
| Factory | Klassen als first-class Objekte | Dict-Dispatch, `@classmethod` |
| Observer | Callables (Funktion, Lambda, `__call__`) | Liste von Callbacks |
| Strategy | Funktionen als first-class Werte | Funktion als Argument, Closure |
| Context Manager | `__enter__`/`__exit__`, `@contextmanager` | `with`-Statement, vielseitig |

**Vier Sätze zum Mitnehmen:**

- *Schön ist besser als hässlich. Einfach ist besser als komplex.*
- *Pythonische Lösungen nutzen die Sprache, nicht das Pattern.*
- *Frag dich: welcher Mechanismus trägt das Pattern? — dann benutze ihn direkt.*
- *Manche Patterns sind in Python keine Patterns mehr, sondern Sprache.*

---

## 5.8 Übungsaufgaben

**Aufgabe 1 – Singleton kritisch hinterfragen.** Schreibe eine Klasse
`Konfiguration` einmal als `__new__`-Singleton, einmal als Modul-Singleton.
Diskutiere: welche Variante ist im Test einfacher zu mocken? Warum?

**Aufgabe 2 – Factory erweitern.** Erweitere die `_TIER_REGISTRY` um einen
`@registriere`-Decorator (siehe Abschnitt 5.2). Lege drei neue Tierarten
an, ohne die Factory-Funktion zu ändern.

**Aufgabe 3 – Observer mit Filter.** Erweitere `Newsletter` um eine Methode
`abonnieren_mit_filter(callback, filter_fn)`, die nur dann an `callback`
weiterleitet, wenn `filter_fn(ausgabe)` wahr ist. Hinweis: `filter_fn` ist
ebenfalls ein Callable — also ein zweites Strategy-Pattern auf derselben
Schnittstelle.

**Aufgabe 4 – Strategy im Alltag.** Sortiere eine Liste von `Person`-
Objekten (Name, Alter) einmal nach Name, einmal nach Alter, einmal nach
Länge des Namens — ohne `Person` zu ändern. An welcher Stelle steckt das
Strategy-Pattern?

**Aufgabe 5 – Context Manager schreiben.** Implementiere eine Klasse
`WechseleVerzeichnis(pfad)`, die im `__enter__` mit `os.chdir` ins
Zielverzeichnis wechselt und im `__exit__` zurück ins vorherige. Schreibe
dieselbe Funktionalität anschließend mit `@contextmanager`.

**Aufgabe 6 – Pattern-Ökonomie.** Wähle einen der Patterns aus diesem
Modul und beschreibe in drei Sätzen, **wann du ihn nicht** einsetzen
würdest. Welcher Punkt aus dem *Zen of Python* spricht dafür?
