# Modul 5 – Pythonische Entwurfsmuster

> *"Was würde ich in Java tun – und wie denkt Python das?"*
> Der rote Faden der ganzen Veranstaltung gilt hier doppelt: Entwurfsmuster
> sind in Java oft eine Antwort auf das, was die Sprache **nicht** kann.
> Wenn man sie 1:1 nach Python übersetzt, übersetzt man unbeabsichtigt auch
> die Java-Einschränkungen mit. Pythonisch zu denken heißt: erst fragen,
> ob das Pattern überhaupt nötig ist.

## Lernziele

Nach Durcharbeitung dieses Moduls können Studierende

- die drei klassischen Patterns Singleton, Factory und Observer in Python
  sowohl im Java-Stil als auch idiomatisch umsetzen,
- erklären, **warum** Python für einige Patterns weniger Boilerplate braucht
  (first-class Funktionen, Klassen als Objekte, Modul-System),
- entscheiden, wann ein Pattern in Python **überflüssig** ist (z. B. Strategy
  mit Funktionen statt Klassen),
- Context Manager als Pythons Antwort auf "etwas muss zuverlässig danach
  passieren" einsetzen.

---

## 5.0 Was ist ein Entwurfsmuster?

Ein **Entwurfsmuster** (engl. *design pattern*) ist eine bewährte, sprach­unabhängige
Schablone für ein wiederkehrendes Entwurfsproblem. Der Klassiker ist das Buch
*"Design Patterns: Elements of Reusable Object-Oriented Software"* (1994) der
sogenannten **Gang of Four** (Gamma, Helm, Johnson, Vlissides) mit 23 Patterns
in drei Kategorien:

| Kategorie | Frage | Beispiele |
|---|---|---|
| Erzeugungsmuster | Wie entstehen Objekte? | **Singleton, Factory**, Builder, Prototype |
| Strukturmuster | Wie passen Objekte zusammen? | Adapter, Decorator, Composite |
| Verhaltensmuster | Wie kommunizieren Objekte? | **Observer, Strategy**, Command, Iterator |

Die Patterns wurden ursprünglich für C++ und Smalltalk beschrieben und sind in
der Java-Welt extrem populär geworden – nicht zuletzt, weil Java mit seiner
strikten OOP-Sicht viele alltägliche Probleme nur mit Klassen lösen kann.

Python hat von Anfang an **mehr Werkzeuge**: Funktionen sind Objekte, Klassen
sind Objekte, Module sind Objekte. Viele Java-Patterns sind in Python deshalb
"unsichtbar" – sie verschwinden in Spracheigenschaften oder werden zu einer
einzigen Zeile.

> **Peter Norvigs These (1998):** *"16 of the 23 patterns are either invisible
> or simpler in Python."*
> Wir werden in diesem Modul anhand von fünf Patterns sehen, was er damit meint.

---

## 5.1 Singleton

### Das Problem

Manchmal soll es von einer Klasse **genau eine** Instanz geben – einen Logger,
einen Konfigurations-Container, einen Verbindungspool. Wer eine "neue" Instanz
anfordert, soll dieselbe bekommen.

### Java – der Klassiker

```java
public class Logger {
    private static Logger instance;
    private List<String> eintraege = new ArrayList<>();

    private Logger() {}                            // Konstruktor privat!

    public static Logger getInstance() {
        if (instance == null) instance = new Logger();
        return instance;
    }

    public void log(String n) { eintraege.add(n); }
}
```

Drei Java-Sprachmittel zusammen erzeugen den Singleton:

1. `private static instance` als Cache,
2. **privater Konstruktor**, damit `new Logger()` von außen verboten ist,
3. statische Zugangsmethode `getInstance()`.

### Python – Variante 1: Java-Stil mit `__new__`

Python kennt keinen privaten Konstruktor. Wir hängen uns stattdessen in
`__new__` ein – die Dunder-Methode, die das Objekt erzeugt (vor `__init__`).

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

Funktioniert, ist aber Java-Denken in Python-Syntax. Drei Stolpersteine:

- `__init__` läuft bei jedem Aufruf **erneut** – wir initialisieren deshalb
  in `__new__` und nur einmal (über die `is None`-Prüfung).
- Threadsicher ist das **nicht**. In Java auch nicht ohne Weiteres
  (Double-Checked Locking), in Python schützt der GIL nicht zuverlässig.
- Vererbung wird unangenehm: alle Unterklassen würden sich dieselbe
  `_instanz`-Variable teilen, wenn man nicht aufpasst.

### Python – Variante 2: Modul-Singleton

Pythons Importsystem cacht jedes Modul beim ersten Import. **Variablen auf
Modul-Ebene sind damit automatisch Singletons.** Es gibt sie *genau einmal*
im Prozess, egal wie oft jemand das Modul importiert.

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

Das ist die idiomatische Python-Antwort. Kein Pattern-Code, keine `__new__`-
Klimmzüge, keine `getInstance()`. **Das Sprachsystem erledigt es.**

In Java geht das so nicht: jede Klasse braucht ihr eigenes Singleton-Boilerplate.

### Python – Variante 3: Singleton-Decorator

Wer den Singleton-Charakter explizit deklarieren möchte, kann einen Decorator
schreiben – wiederverwendbar für beliebige Klassen:

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

`@singleton` ist Python-Syntax für: "Wende die Funktion `singleton` auf die
Klasse `Datenbankverbindung` an." Was zurückkommt, ist `hole_instanz` – also
**keine Klasse mehr, sondern eine Funktion**, die die Klasse zwischenspeichert.
Aus Sicht des Aufrufers bleibt `Datenbankverbindung(...)` gleich.

### Wann welche Variante?

| Variante | Empfehlung |
|---|---|
| **Modul-Singleton** | Standardfall. Praktisch immer die richtige Wahl. |
| **`@singleton`-Decorator** | Wenn die Singleton-Eigenschaft sichtbar im Klassen-Header dokumentiert werden soll. |
| **`__new__`-Variante** | Wenn man das Java-Pattern lehrt – sonst eher selten. |
| **Metaklassen-Singleton** | Existiert auch (`type` selbst überschreiben) – akademisch interessant, in der Praxis selten nötig. |

> **Kritische Stimme:** Viele Python-Erfahrene halten Singletons für ein
> *Anti-Pattern* – sie sind globaler Zustand, schwer testbar, schwer zu
> mocken. Wenn möglich: lieber Abhängigkeit explizit als Argument übergeben
> ("Dependency Injection") statt versteckt über eine globale Instanz holen.

---

## 5.2 Factory

### Das Problem

Der Aufrufer soll ein Objekt eines passenden Untertyps bekommen, ohne den
konkreten Typ zu kennen. Beispiel: "Gib mir ein Tier vom Typ 'hund'." Die
Aufrufseite weiß nichts von der Klasse `Hund` – nur von `Tier`.

### Java – Factory-Klasse mit `if/elif`

```java
interface Tier { String laut(); }
class Hund  implements Tier { public String laut() { return "Wuff"; } }
class Katze implements Tier { public String laut() { return "Miau"; } }

class TierFactory {
    public static Tier erzeuge(String art) {
        if (art.equals("hund"))  return new Hund();
        if (art.equals("katze")) return new Katze();
        throw new IllegalArgumentException(art);
    }
}
```

Drei Bestandteile: **Interface** (definiert den gemeinsamen Vertrag),
**konkrete Klassen**, **Factory-Klasse**. Die `if/elif`-Kette wächst mit jeder
neuen Tierart.

### Python – Variante 1: Java-Stil 1:1

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

Direkter Java-Stil – nichts gewonnen, aber für den Vergleich gut.

### Python – Variante 2: Dict-Dispatch (Registry)

Klassen sind in Python **first-class Objekte**: man kann sie in Listen
oder Dicts speichern und ganz normal aufrufen.

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

**Variante mit Decorator-Registrierung** (für Fortgeschrittene):

```python
TIERE = {}
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

Jede Klasse "meldet sich selbst an". Frameworks wie Django und Flask
funktionieren auf dieser Idee.

### Python – Variante 3: `@classmethod` als alternativer Konstruktor

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

Lesbarer als `PizzaFactory.erzeuge("margherita")`, näher am Domänen-Vokabular.

> **Faustregel:** Wenn die Auswahl per **String/Enum zur Laufzeit** kommt –
> Dict-Dispatch. Wenn die Auswahl **zur Programmierzeit** feststeht und nur
> bequeme Konstruktoren gewollt sind – `@classmethod`.

---

## 5.3 Observer

### Das Problem

Ein Objekt (Subject / Publisher) hält andere (Observer / Subscriber) auf dem
Laufenden, ohne sie konkret zu kennen. Beispiele: Newsletter-Versand,
Event-Bus, MVC-Updates.

### Java – Listener-Interface

```java
interface Beobachter {
    void aktualisiere(String ereignis);
}

class Newsletter {
    private List<Beobachter> beobachter = new ArrayList<>();
    public void anmelden(Beobachter b)  { beobachter.add(b); }
    public void veroeffentliche(String s) {
        for (Beobachter b : beobachter) b.aktualisiere(s);
    }
}

class KonsolenAusgabe implements Beobachter {
    public void aktualisiere(String s) { System.out.println(s); }
}
```

Java **braucht** das Interface, weil `for (Beobachter b ...)` sonst nicht
weiß, welche Methode aufzurufen ist – statische Typisierung verlangt einen
gemeinsamen Vertrag.

### Python – Liste von Callables

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

Jetzt kann **alles, was aufrufbar ist**, Beobachter sein:

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

Drei verschiedene "Beobachter" – keiner musste ein Interface implementieren.

### Observer mit Zustand: `__call__`

Falls ein Beobachter Zustand mitschleppen muss, definiert man eine ganz
normale Klasse – und macht sie mit `__call__` aufrufbar:

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

> **Wozu das Ganze?** Wer in Java *jeden* möglichen Listener als eigene
> Implementierung des Beobachter-Interfaces schreiben muss, hat schnell
> drei Klassen für eine Lambda-Zeile. Python erlaubt die volle Bandbreite:
> Funktion, Lambda, gebundene Methode, aufrufbares Objekt.

### Hinweis: Konkrete Bibliotheken

Für echtes Event-Handling in Produktivcode gibt es etablierte Bibliotheken:

- `blinker` – generisches Signal-Framework
- `pydispatch` – schlanker Signal-Mechanismus
- `pyqtSignal` / `tkinter`-Events – GUI-Frameworks bringen ihre eigene Variante

Das Pattern bleibt dasselbe; die Bibliothek nimmt die Buchhaltung ab.

---

## 5.4 Strategy

### Das Problem

Ein Algorithmus soll **zur Laufzeit** austauschbar sein. Klassiker:
verschiedene Rabatt-Berechnungen, Sortier-Kriterien, Komprimierungs-Verfahren.

### Java – Strategy-Interface

```java
interface RabattStrategie {
    double berechne(double preis);
}

class KeinRabatt implements RabattStrategie {
    public double berechne(double preis) { return preis; }
}

class ProzentRabatt implements RabattStrategie {
    private double prozent;
    public ProzentRabatt(double p) { this.prozent = p; }
    public double berechne(double preis) {
        return preis * (1 - prozent / 100);
    }
}

class Warenkorb {
    private RabattStrategie strategie;
    public Warenkorb(RabattStrategie s) { this.strategie = s; }
}
```

Für *zwei verschiedene Rabatt-Funktionen* braucht Java: ein Interface, zwei
Implementierungs-Klassen plus die Warenkorb-Anbindung.

### Python – Funktionen reichen

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

**Closure-Detail:** `prozent_rabatt(10)` gibt eine **Funktion** zurück, die
den Wert `10` in ihrem Geltungsbereich behält. Das ist Pythons Antwort auf
eine "parametrisierte Strategie-Klasse" – aber ohne Klasse, ohne Interface,
ohne `new`.

### Wo das in der Standardbibliothek begegnet

Das Strategy-Pattern ist in Python so verbreitet, dass es kaum noch als
Pattern erkannt wird – es ist einfach *Funktionen übergeben*:

```python
sorted(personen, key=lambda p: p.alter)         # Strategy = key-Funktion
list(map(str.upper, namen))                     # Strategy = Transformation
threading.Thread(target=mein_job).start()       # Strategy = was getan wird
```

Jedes `key=`-Argument, jedes `target=`-Argument, jeder `lambda` ist im Kern
ein Strategy-Pattern. Java braucht dafür `Comparator`-Interfaces oder seit
Java 8 funktionale Interfaces und Lambdas.

---

## 5.5 Context Manager

### Das Problem

Manche Operationen brauchen **garantiertes Aufräumen** – egal ob der Block
erfolgreich war oder eine Exception geflogen ist. Datei schließen, Lock
freigeben, Verbindung trennen, Transaktion zurückrollen.

### Java – `try`/`finally` und `try-with-resources`

Klassisches `try`/`finally`:

```java
BufferedReader r = null;
try {
    r = new BufferedReader(new FileReader("a.txt"));
    // ... arbeiten ...
} finally {
    if (r != null) r.close();
}
```

Seit Java 7: `try-with-resources` – aber nur für Klassen, die
`AutoCloseable` implementieren:

```java
try (BufferedReader r = new BufferedReader(new FileReader("a.txt"))) {
    // ... arbeiten ...
}
```

### Python – `with` für alles

In Python kann **jedes Objekt mit `__enter__` und `__exit__`** hinter `with`
stehen:

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

Ein **Rückgabewert `True`** würde die Exception als "behandelt" markieren und
unterdrücken. `False` (oder `None`) reicht sie weiter – das ist fast immer
das richtige Verhalten.

### Variante mit `@contextmanager`

Wer keine ganze Klasse schreiben möchte: `contextlib.contextmanager` macht
aus einer Generator-Funktion einen Context Manager:

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
wichtig – sonst schluckt der Context Manager die Exception still.

### Eingebaute Context Manager

Python ist voll davon:

```python
with open("a.txt") as f: ...                 # Datei schließen
with threading.Lock(): ...                   # Lock freigeben
with sqlite3.connect("db") as c: ...         # Transaktion / close
with tempfile.TemporaryDirectory() as d: ... # Verzeichnis aufräumen
with mock.patch("modul.funktion"): ...       # Mock im Test rückgängig
```

### Java-Vergleich auf einen Blick

| Aspekt | Java | Python |
|---|---|---|
| Schlüsselwort | `try (...) { ... }` | `with ...:` |
| Voraussetzung | Klasse implementiert `AutoCloseable` | Klasse hat `__enter__` und `__exit__` |
| Mehrere Ressourcen | `try (a; b; c)` (Java 7+) | `with a, b, c:` |
| Generator-Variante | gibt es nicht | `@contextmanager` |
| Anwendungsbereiche | praktisch nur "schließen" | Zeit, Mocks, Transaktion, Lock, Verzeichnis, ... |

> **Kernlehre:** `try-with-resources` ist ein Spezialfall. Pythons `with` ist
> ein allgemeiner Mechanismus. Wo Java für Zeitmessung oder Mocking ein
> manuelles `try/finally` braucht, bekommt Python das Pattern geschenkt.

---

## 5.6 Was wir bewusst weggelassen haben

Aus Zeit­gründen (30 Minuten) nicht in dieser Modul-Einheit:

- **Iterator** – kommt teils schon in Modul 4 vor; in Python via `__iter__` und
  Generatoren mit `yield` praktisch unsichtbar.
- **Decorator (das Pattern, nicht die `@`-Syntax)** – konzeptuell verwandt
  mit Pythons Funktions-Decorator, würde eine eigene Stunde brauchen.
- **Command, Template Method, Adapter, Composite, State** – klassische GoF-
  Patterns, in Python aber oft entweder unauffällig (Funktion statt
  Command-Klasse) oder durch Duck Typing trivial (Adapter).
- **Metaklassen-Singleton** – existiert, ist aber für die meisten
  Anwendungsfälle überdimensioniert.

Für Interessierte: Peter Norvigs *"Design Patterns in Dynamic Languages"*
und Brandon Rhodes' Sammlung *"Python Patterns"* online sind die
Standard-Referenzen.

---

## 5.7 Zusammenfassung – Tabelle

| Pattern | Java-Stil in Python | Pythonische Antwort |
|---|---|---|
| Singleton | `__new__` + Klassenvariable | Modul-Singleton, `@singleton`-Decorator |
| Factory | `if/elif`-Methode | Dict-Dispatch, `@classmethod` |
| Observer | Listener-Interface mit `abc` | Liste von Callables, `__call__` |
| Strategy | Strategy-Interface + Klassen | Funktion als Argument, Closure |
| Context Manager | (existiert in Java so nicht) | `__enter__`/`__exit__`, `@contextmanager` |

**Der eine Satz, den man mitnehmen sollte:**

> *Viele Java-Patterns sind in Python keine Patterns mehr – sondern Sprache.*

---

## 5.8 Übungsaufgaben

**Aufgabe 1 – Singleton kritisch hinterfragen.** Schreibe eine Klasse
`Konfiguration` zuerst als `__new__`-Singleton, dann als Modul-Singleton.
Diskutiere: welche Variante ist im Test einfacher zu mocken? Warum?

**Aufgabe 2 – Factory erweitern.** Erweitere die `_TIER_REGISTRY` um einen
`@registriere`-Decorator (siehe Abschnitt 5.2). Lege drei neue Tierarten an,
ohne die Factory-Funktion zu ändern.

**Aufgabe 3 – Observer mit Filter.** Erweitere `Newsletter` um eine Methode
`abonnieren_mit_filter(callback, filter_fn)`, die nur dann an `callback`
weiterleitet, wenn `filter_fn(ausgabe)` wahr ist. Tipp: das ist auch wieder
ein Strategy.

**Aufgabe 4 – Strategy im Alltag.** Sortiere eine Liste von `Person`-Objekten
(Name, Alter) einmal nach Name, einmal nach Alter, einmal nach Länge des
Namens – ohne `Person` zu ändern. Wo steckt das Strategy?

**Aufgabe 5 – Context Manager schreiben.** Implementiere eine Klasse
`WechseleVerzeichnis(pfad)`, die im `__enter__` mit `os.chdir` ins
Zielverzeichnis wechselt und im `__exit__` zurück ins vorherige. Schreibe
dieselbe Funktionalität noch einmal mit `@contextmanager`.

**Aufgabe 6 – Diskussion.** Lies einen der folgenden Patterns aus dem
GoF-Buch (Adapter, Decorator, Iterator) und beschreibe, wie er sich in
Python idiomatisch umsetzen lässt – oder warum er überflüssig wird.
