# Modul 5 – Präsentation: Pythonische Entwurfsmuster

> Stichpunkt-Notizen zum Üben. **Kein Wort-für-Wort-Skript.** Pro Abschnitt:
> *Thesensatz* (was muss man sagen, wenn man nur einen Satz hat), *Kern-
> aussagen*, *zu zeigender Code*, *Demo-Output-Check*, *typische
> Zwischenfragen*.
>
> **Zeitbudget gesamt: ~30 Minuten.**
> Richtwert pro Abschnitt: 3–4 Minuten Inhalt + 30 Sekunden Atem/Wechsel.

---

## Setup & Einstieg (2 Min)

**Thesensatz:** *"Viele Java-Patterns sind in Python keine Patterns mehr –
sondern Sprache."*

**Aufzubauen:**

- Erinnerung: Gang of Four, 23 Patterns, drei Kategorien (Erzeugung,
  Struktur, Verhalten) – kurz, eine Folie reicht.
- Peter Norvigs These zitieren: *"16 of 23 patterns are invisible or
  simpler in Python."* (Quelle: Norvig 1998.)
- Was wir zeigen werden: 3 klassische Patterns (Singleton, Factory,
  Observer) plus Strategy plus Context Manager. Jedes Mal: erst Java-Stil,
  dann pythonisch.
- Roter Faden: nicht *"so übersetzt man Java"*, sondern *"was hätte man in
  Python von Anfang an anders gedacht?"*.

**Übergangssatz zum 1. Pattern:** *"Fangen wir mit dem berühmtesten Pattern
an – dem, das in Java in jedem zweiten Projekt zu finden ist."*

---

## Abschnitt 1: Singleton – Java-Stil (3 Min)

**Thesensatz:** *"In Java ist Singleton ein Pattern. In Python ist es eine
Frage – braucht man es wirklich?"*

**Kernaussagen:**

- Singleton = genau eine Instanz, global zugreifbar. Beispiele: Logger,
  Konfiguration, Verbindungspool.
- Java-Klassiker: privater Konstruktor + `static getInstance()` + Cache-
  Variable. Ohne den privaten Konstruktor klappt das Pattern nicht.
- Python kennt keinen privaten Konstruktor. Eingriffspunkt:
  Dunder-Methode **`__new__`** – läuft *vor* `__init__` und erzeugt das
  Objekt selbst.

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

**Mögliche Zwischenfrage:** *"Ist das threadsicher?"* – Antwort: Nein, in
Java auch nicht trivial (Double-Checked Locking), der Python-GIL hilft nicht
zuverlässig. In Praxis: Modul-Singleton (gleich Abschnitt 2).

**Überleitung:** *"Funktioniert – aber Python kann das eleganter."*

---

## Abschnitt 2: Singleton – Pythonisch (4 Min)

**Thesensatz:** *"Pythons Modul-System ist bereits ein Singleton-Mechanismus.
Wer Modul-Variablen verwendet, hat das Pattern ohne eine einzige Zeile
Pattern-Code."*

**Kernaussagen (Variante A – Modul-Singleton):**

- Python cacht jedes Modul beim ersten Import. Variablen auf Modul-Ebene
  existieren **genau einmal** im Prozess.
- Praxis: einfach `from konfiguration import konfiguration` – fertig.
- Das ist die **idiomatische** Antwort. Java braucht dafür immer eine
  Klasse, weil Module in Java keine eigenen Werte halten können.

**Kernaussagen (Variante B – Decorator-Singleton):**

- Wenn man die Singleton-Eigenschaft sichtbar dokumentieren möchte:
  `@singleton` als Decorator – wiederverwendbar für *jede* Klasse.
- Python-Detail erklären: `@singleton` ist syntaktischer Zucker für
  `Datenbankverbindung = singleton(Datenbankverbindung)`.
- Was zurückkommt, ist *keine Klasse mehr*, sondern eine Funktion, die die
  Klasse "verwaltet". Für den Aufrufer bleibt der Aufruf identisch.

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
- Singletons benutzen, weil "man das so macht", ist eine Java-Reflex – in
  Python lohnt sich jedes Mal die Frage *"brauche ich das wirklich?"*.

**Überleitung:** *"Vom 'gibt es genau eines' zum 'gib mir bitte eines vom
Typ X' – das ist Factory."*

---

## Abschnitt 3: Factory – Java-Stil (3 Min)

**Thesensatz:** *"Die klassische Factory mit if/elif funktioniert in Python
genauso wie in Java – und genauso unelegant."*

**Kernaussagen:**

- Problem: Aufrufer kennt nur den Obertyp, will aber eine passende
  konkrete Instanz.
- Java-Bestandteile: Interface (`Tier`), konkrete Klassen (`Hund`,
  `Katze`), Factory-Klasse mit `if/elif/throw`.
- Python-Variante: `abc.ABC` ersetzt das Interface, `@staticmethod`
  ersetzt `public static`. Sonst identisch.

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
- Bei 30 Tierarten – 30 Zweige.
- Beispiel im Demo: Fehlerfall `"drache"` löst ValueError aus – analog zu
  Javas `IllegalArgumentException`.

**Übergangssatz:** *"Python kann das offensichtlich besser – weil Klassen
in Python einfache Objekte sind."*

---

## Abschnitt 4: Factory – Pythonisch (4 Min)

**Thesensatz:** *"Wenn Klassen Objekte sind, kann ich sie in ein Dict
stecken. Dann ist die Factory ein einzeiliger Lookup."*

**Kernaussagen (Variante A – Dict-Dispatch):**

- *"Klassen sind first-class Objekte"* – als zentralen Satz aussprechen.
- Klasse in ein Dict legen, beim Erzeugen nachschlagen und aufrufen:
  `_TIER_REGISTRY[art]()`.
- Drei Vorteile gegenüber if/elif:
  1. neue Tierart = eine neue Dict-Zeile, Factory-Funktion bleibt unverändert,
  2. O(1)-Lookup statt O(n),
  3. Plugins können sich nachträglich registrieren
     (`_TIER_REGISTRY["drache"] = Drache`).

**Kernaussagen (Variante B – `@classmethod`-Factory):**

- Wenn die Varianten **schon zur Programmierzeit feststehen** und nur
  *bequemer Konstruktor* gewollt ist: lieber direkt in der Klasse.
- Beispiel `Pizza.margherita()`, `Pizza.salami()` – liest sich wie der
  Domänen-Wortschatz.
- In Java: entweder zwei Subklassen oder `PizzaFactory.erzeuge("margherita")`.
  In Python: `@classmethod` reicht.

**Zu zeigen:** `erzeuge_tier()` und `Pizza.margherita()`.

**Demo-Output:**

```
erzeuge_tier('hund') -> Hund('Wuff')
Pizza.margherita()   -> Pizza(Tomate, Mozzarella, Basilikum)
```

**Faustregel laut aussprechen:**

- *String/Enum zur Laufzeit?* → Dict-Dispatch.
- *Auswahl steht zur Programmierzeit fest?* → `@classmethod`.

**Überleitung:** *"Bisher ging es um *Erzeugung* von Objekten. Jetzt zu
Kommunikation zwischen Objekten – Observer."*

---

## Abschnitt 5: Observer (4 Min)

**Thesensatz:** *"Java braucht ein Interface, damit der Newsletter weiß,
welche Methode er aufrufen soll. Python ruft einfach das auf, was man ihm
übergibt – jede Funktion ist ein Beobachter."*

**Kernaussagen:**

- Java-Stil: `interface Beobachter { void aktualisiere(...); }`. Listener
  registrieren, `for`-Schleife ruft `b.aktualisiere(...)`.
- Python-Stil: Liste von **Callables**. Jede Funktion, jedes Lambda, jede
  Methode, jedes Objekt mit `__call__` passt rein.
- Begriff einführen: *"Callable"* – alles, was man mit `(...)` aufrufen kann.
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
- In Java: für drei verschiedene Beobachter braucht man drei Klassen.
- In Python: drei Zeilen.

**Hinweis:** für Produktivcode existieren Bibliotheken wie `blinker`,
`pydispatch`. Pattern bleibt dasselbe, Buchhaltung ist abgenommen.

**Überleitung:** *"Wenn Funktionen schon Beobachter sein können – können
sie auch Strategien sein."*

---

## Abschnitt 6: Strategy (3 Min)

**Thesensatz:** *"Strategy ist in Python so unsichtbar geworden, dass keiner
es mehr Pattern nennt – wir nennen es einfach 'Funktion übergeben'."*

**Kernaussagen:**

- Java braucht: Strategy-Interface, eine Klasse pro Strategie, Setter.
- Python braucht: eine Funktion. Die übergibt man als Argument.
- **Closure-Konzept einführen:** `prozent_rabatt(10)` gibt eine *Funktion*
  zurück, die den Wert `10` "behält". Pythons Antwort auf eine
  parametrisierte Strategie-Klasse – ohne Klasse.
- Strategie zur Laufzeit austauschen: einfach Attribut neu zuweisen.

**Zu zeigen:**

```python
korb = Warenkorb(prozent_rabatt(10))
korb.strategie = prozent_rabatt(20)          # zur Laufzeit wechseln
```

**Wo das in der Standardbibliothek begegnet (kurz erwähnen):**

```python
sorted(personen, key=lambda p: p.alter)       # Strategy = key-Funktion
threading.Thread(target=mein_job)             # Strategy = was getan wird
```

- *"Jedes `key=`-Argument ist im Kern ein Strategy."*

**Überleitung:** *"Letztes Pattern – und das einzige, für das Java erst seit
Java 7 überhaupt ein Sprachmittel hat: Context Manager."*

---

## Abschnitt 7: Context Manager (4 Min)

**Thesensatz:** *"`try-with-resources` in Java ist auf 'schließen'
beschränkt. Python verallgemeinert das Konzept – jede 'davor-danach'-Logik
kann in `with` verpackt werden."*

**Kernaussagen:**

- Problem: garantiert aufräumen, auch bei Exceptions. Datei, Lock,
  Transaktion, Zeitmessung, Mock im Test, temporäres Verzeichnis.
- Java: `try/finally` oder `try-with-resources` (nur für `AutoCloseable`).
- Python: jedes Objekt mit `__enter__` und `__exit__` passt hinter `with`.

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
- Rückgabewert `True` würde Exception unterdrücken. Standard: `False`.

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

→ `__exit__` läuft **garantiert**, der Aufrufer kann die Exception trotzdem
behandeln.

**Eingebaute Context Manager auflisten (3 Beispiele reichen):**

```python
with open("a.txt") as f: ...
with threading.Lock(): ...
with mock.patch("modul.funktion"): ...
```

**Kernunterschied zu Java betonen:**

- Java: `try-with-resources` ist *ein Spezialfall* (Closing).
- Python: `with` ist ein **allgemeiner Mechanismus**. Zeitmessung,
  Transaktion, Lock, Mock – alles dasselbe Sprachmittel.

---

## Abschluss (2 Min)

**Thesensatz (gleicher Satz wie am Anfang – Klammer schließen):**
*"Viele Java-Patterns sind in Python keine Patterns mehr – sondern Sprache."*

**Punkte für den Abschluss:**

- Tabelle zusammenfassen (siehe Lehrbuch 5.7):

  | Pattern | Java-Stil | Pythonisch |
  |---|---|---|
  | Singleton | `__new__` + Klassenvariable | Modul-Singleton, Decorator |
  | Factory | `if/elif` | Dict-Dispatch, `@classmethod` |
  | Observer | Listener-Interface | Liste von Callables |
  | Strategy | Strategy-Interface + Klassen | Funktion als Argument |
  | Context Manager | (`try-with-resources` als Sonderfall) | `with`, `@contextmanager` |

- *Pythons Werkzeuge*, die immer wieder auftauchten: first-class Funktionen,
  first-class Klassen, Modul-System, Dunder-Methoden, Decorators.
- Empfehlung: Bevor man ein Pattern aus dem Java-Repertoire greift, fragen –
  *kann Python das schon von sich aus?*
- Mögliche Nächste-Schritte-Folie:
  - Modul 6 (Fehlerbehandlung) baut direkt auf Context Manager auf.
  - Modul 7 (typing/Protokolle) liefert die typ­technische Antwort darauf,
    wenn man die Java-Garantien doch zurück möchte.

**Schlussgeste:** Frage an die Hörer: *"Welches Java-Pattern hättet ihr gerne
noch idiomatisch in Python gesehen?"* – das eröffnet die Diskussion.

---

## Pacing-Übersicht

| Abschnitt | Inhalt | Zielzeit |
|---|---|---|
| Einstieg | Pattern-Definition, Norvig-These, roter Faden | 2 Min |
| 1 | Singleton Java-Stil | 3 Min |
| 2 | Singleton Pythonisch | 4 Min |
| 3 | Factory Java-Stil | 3 Min |
| 4 | Factory Pythonisch | 4 Min |
| 5 | Observer | 4 Min |
| 6 | Strategy | 3 Min |
| 7 | Context Manager | 4 Min |
| Abschluss | Tabelle + Frage | 2 Min |
| **Gesamt** | | **29 Min** |

**Puffer-Plan, falls die Zeit knapp wird:**

- Abschnitt 1 (Singleton Java-Stil) **kürzen** – das Argument "Java in
  Python-Syntax" reicht auch in 90 Sekunden.
- Demo-Output in Abschnitt 7 weglassen, nur den Fehlerfall mündlich
  beschreiben.

**Falls Zeit übrig ist:**

- Decorator-Registrierung als Bonus zur Factory zeigen (siehe Lehrbuch 5.2).
- Eingebaute Context-Manager-Beispiele länger demonstrieren.

---

## Wahrscheinliche Fragen aus dem Publikum

| Frage | Kurze Antwort |
|---|---|
| *Sind Singletons threadsicher?* | In Java auch nicht trivial. In Python: Modul-Singleton oder `threading.Lock()` in `__new__`. |
| *Wann nehme ich Dict-Dispatch, wann `@classmethod`?* | Laufzeit-Auswahl per String → Dict. Programmierzeit-Auswahl → `@classmethod`. |
| *Was ist mit Lambdas mit mehreren Zeilen?* | Geht in Python nicht direkt – stattdessen normale Funktion definieren und übergeben. |
| *Sind `@contextmanager`-Funktionen langsamer als Klassen?* | Marginaler Overhead, in der Praxis irrelevant. Lesbarkeit gewinnt. |
| *Warum kein Builder?* | Python hat Keyword-Argumente und Default-Werte – Builder ist meistens überflüssig. |
| *Was ist mit Abstract Factory?* | Selbe Logik wie Factory, nur mit Familien von Klassen. Dict-Dispatch mit verschachtelten Dicts. |

---

## Persönliche Hinweise zum Üben

- **Vor dem Vortrag mindestens einmal `python main_modul5.py` laufen
  lassen** und die Ausgabe lesen – das prägt sich besser ein als Folien.
- *"first-class"* ist der zentrale Begriff – beim Üben absichtlich oft
  verwenden, damit er sich festsetzt.
- Java-Code immer **kurz** zeigen (eine Folie), Python-Code **ausführlich**.
  Der Vortrag handelt von Python, nicht von Java.
- Wenn eine Frage kommt, deren Antwort man nicht weiß: ehrlich sagen
  *"Das schaue ich nach"* – nicht raten. Wir haben gerade ein Pattern-Modul
  gegeben, in dem Klarheit das wichtigste Argument war.
