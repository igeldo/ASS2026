# Modul 5 – Pythonische Entwurfsmuster · Pythonic Design Patterns

> *"Schön ist besser als hässlich. Einfach ist besser als komplex.
> Lesbarkeit zählt."* — aus *The Zen of Python* (Tim Peters)

---

## Über dieses Heft / About this document

**Deutsch.** Dieses Lehrbuch ist als **Selbststudium-Heft** gedacht und setzt
**keine Python-Vorerfahrung** voraus. Wer Java (oder eine andere
objektorientierte Sprache) kennt, kann alles hier verstehen. Jeder Fachbegriff
wird beim ersten Auftreten erklärt; am Ende gibt es zusätzlich ein **Glossar**.
Die Code-Beispiele werden Zeile für Zeile besprochen.

**English.** This is a **self-study booklet** that assumes **no prior Python
experience**. If you know Java (or another object-oriented language), you can
follow everything here. Every technical term is explained on first use, and
there is a **glossary** at the end. Code examples are walked through line by
line.

**Aufbau / Structure.** Das Dokument hat zwei Teile mit identischem Inhalt:
The document has two parts with identical content:

- **Teil A — Deutsch** (Abschnitte 5.0 – 5.9 + Glossar)
- **Teil B — English** (sections 5.0 – 5.9 + glossary)

Lies den Teil in deiner bevorzugten Sprache; den anderen kannst du als
Nachschlagewerk benutzen, wenn ein Begriff unklar ist. / Read the part in your
preferred language; use the other as a reference when a term is unclear.

---

## Inhaltsverzeichnis / Table of contents

**Teil A — Deutsch**
- [Wie man dieses Heft liest](#wie-man-dieses-heft-liest)
- [Python-Crashkurs für Java-Kenner](#python-crashkurs-für-java-kenner)
- [5.0 Was ist ein Entwurfsmuster?](#50-was-ist-ein-entwurfsmuster)
- [5.1 Singleton](#51-singleton)
- [5.2 Factory](#52-factory)
- [5.3 Observer](#53-observer)
- [5.4 MVC – Model, View, Controller](#54-mvc--model-view-controller)
- [5.5 Strategy (Exkurs)](#55-strategy-exkurs--bonus)
- [5.6 Context Manager (Exkurs)](#56-context-manager-exkurs--bonus)
- [5.7 Was wir bewusst weggelassen haben](#57-was-wir-bewusst-weggelassen-haben)
- [5.8 Zusammenfassung](#58-zusammenfassung)
- [5.9 Übungsaufgaben](#59-übungsaufgaben)
- [Glossar](#glossar)

**Teil B — English** beginnt nach dem Glossar / begins after the glossary.

---
---

# Teil A — Deutsch

## Wie man dieses Heft liest

Du wirst in diesem Heft immer wieder dieselben **vier Kästen** sehen. Sie
helfen dir, den Text einzuordnen:

> **🔑 Begriff:** Hier wird ein Fachwort erklärt, bevor es benutzt wird.

> **☕ Aus Java bekannt:** Eine kurze Brücke zu dem, was du aus Java schon
> kennst — als Eselsbrücke, nicht als Pflichtwissen.

> **🐍 Pythonisch gedacht:** Hier steht, wie ein erfahrener Python-Mensch das
> Problem sehen würde.

> **⚠️ Stolperstein:** Eine typische Falle oder ein häufiges Missverständnis.

Begleitend gibt es zwei lauffähige Dateien:

- `modul5_entwurfsmuster.py` — enthält **nur Definitionen** (Klassen und
  Funktionen), keine Ausgabe. Das ist die „Bibliothek".
- `main_modul5.py` — **führt** die Definitionen vor und erzeugt Ausgabe. Das
  ist die „Demo". Starte sie mit `python main_modul5.py`.

Empfehlung: Lies einen Abschnitt hier, sieh dir dann die zugehörige Demo-
Ausgabe an. Theorie und sichtbares Verhalten zusammen prägen sich am besten ein.

---

## Python-Crashkurs für Java-Kenner

Bevor wir Muster anschauen, hier das absolute Minimum an Python, das du
brauchst, um **jede** Codezeile in diesem Heft zu lesen. Wenn du Java kannst,
ist das in 15 Minuten erledigt — Python ist in den meisten Punkten *weniger*
streng, nicht mehr.

### 1. Einrückung statt geschweifter Klammern

In Java markieren `{ }` einen Block. In Python macht das die **Einrückung**
(üblicherweise 4 Leerzeichen). Es gibt keine `{ }` für Blöcke und keine
Semikolons am Zeilenende.

```python
def begruesse(name):           # Doppelpunkt eröffnet den Block
    if name:                   # eingerückt = "gehört zum if"
        print("Hallo", name)   # Funktionsaufruf
    else:
        print("Hallo Welt")
```

> **☕ Aus Java bekannt:** Dasselbe wie `void begruesse(String name) { ... }`,
> nur dass die Einrückung die Klammern ersetzt. Falsche Einrückung ist in
> Python ein **Syntaxfehler**, kein Schönheitsproblem.

### 2. Variablen und dynamische Typisierung

Variablen werden **ohne Typ** deklariert — der Typ steckt im Wert, nicht im
Namen. Eine Variable kann später sogar einen Wert anderen Typs aufnehmen.

```python
x = 42          # x ist jetzt ein int
x = "Text"      # völlig legal: x ist jetzt ein str
```

> **🔑 Begriff – dynamische Typisierung:** Der Typ wird erst **zur Laufzeit**
> geprüft, nicht vom Compiler. Es gibt keinen separaten Compiler-Schritt wie
> `javac`; Python führt den Code direkt aus.

**Optionale Typhinweise (type hints).** Man *darf* Typen hinschreiben, z. B.
`def f(preis: float) -> float:`. Diese Hinweise sind reine Dokumentation/
Werkzeug-Hilfe — Python **erzwingt** sie zur Laufzeit nicht. In diesem Heft
benutzen wir sie, weil sie das Lesen erleichtern.

### 3. Funktionen

```python
def addiere(a, b=0):           # b=0 ist ein Standardwert (default)
    return a + b               # 'return' wie in Java

addiere(2, 3)                  # -> 5
addiere(2)                     # -> 2   (b nimmt den Standardwert 0)
```

Funktionen können **überall** stehen — auf Datei-Ebene, in anderen Funktionen,
in Klassen. Sie müssen nicht in einer Klasse wohnen (anders als in Java).

### 4. Klassen, `__init__` und `self`

```python
class Hund:
    def __init__(self, name):   # Konstruktor; läuft beim Erzeugen
        self.name = name        # Instanz-Attribut setzen

    def bellen(self):           # Methode; 'self' ist immer der 1. Parameter
        return f"{self.name} sagt Wuff"

hund = Hund("Rex")              # KEIN 'new' nötig
print(hund.bellen())            # -> Rex sagt Wuff
```

Die wichtigsten Übersetzungen:

| Java | Python | Bemerkung |
|---|---|---|
| Konstruktor `Hund(...)` | `def __init__(self, ...)` | „dunder init", s. u. |
| `this` | `self` | muss **explizit** als 1. Parameter stehen |
| `new Hund("Rex")` | `Hund("Rex")` | kein `new` |
| `toString()` | `def __str__(self)` | für lesbare Ausgabe |
| Feld/Attribut | `self.name = ...` | wird im `__init__` angelegt |

> **🔑 Begriff – Instanz / Objekt:** Eine **Instanz** ist ein konkretes,
> mit der Klasse erzeugtes Objekt. `hund` oben ist eine Instanz der Klasse
> `Hund`. „Objekt" und „Instanz" meinen dasselbe.

> **🔑 Begriff – Attribut:** Ein an einem Objekt gespeicherter Wert
> (`self.name`). In Java sagt man „Feld" (field) oder „Member".

> **🔑 Begriff – Methode:** Eine Funktion, die zu einer Klasse gehört und
> `self` als ersten Parameter bekommt.

### 5. Kein `public`/`private` — nur Konventionen

Python hat **keine** Zugriffsmodifizierer. Stattdessen gilt eine Konvention:

- `name` — öffentlich, frei benutzbar.
- `_name` — „bitte nicht von außen anfassen" (ein Unterstrich = intern). Wird
  technisch **nicht** verhindert; es ist eine Bitte unter Erwachsenen.
- `__name` — zwei Unterstriche: Python „verbiegt" den Namen leicht
  (*name mangling*), um versehentliche Kollisionen in Unterklassen zu
  vermeiden. Selten nötig.

> **⚠️ Stolperstein:** `_TIER_REGISTRY` mit führendem Unterstrich heißt also
> *nicht* „privat im Java-Sinn", sondern „intern, von außen bitte nicht
> direkt benutzen".

### 6. `None`, Wahrheitswerte, Wahrheitsgehalt

- `None` ist Pythons `null` — „kein Wert".
- `True` / `False` sind die Wahrheitswerte (großgeschrieben!).
- In `if`-Abfragen gelten `None`, `0`, `""` (leerer String) und `[]` (leere
  Liste) als **falsch**; nicht-leere Werte als **wahr**. Man nennt das
  *truthiness* (Wahrheitsgehalt).

```python
if cls._instanz is None:    # 'is' prüft Objekt-Identität (gleiches Objekt?)
    ...
```

> **🔑 Begriff – `is` vs `==`:** `==` fragt „**gleicher Wert**?". `is` fragt
> „**dasselbe Objekt** im Speicher?". Für Singletons ist genau `is`
> interessant: Sind zwei Variablen *dasselbe* Objekt?

### 7. Listen, Dicts, Tupel

```python
liste = [1, 2, 3]                       # Liste (wie ArrayList)
liste.append(4)                         # anhängen
zuordnung = {"hund": 1, "katze": 2}     # dict (wie HashMap)
zuordnung["kuh"] = 3                    # Eintrag setzen
paar = ("e", 2)                         # Tupel: unveränderliche Sequenz
```

> **🔑 Begriff – dict (Dictionary):** Eine Schlüssel-Wert-Tabelle, Pythons
> `HashMap`. Zugriff über `dict[schluessel]`. Tauchen später beim
> „Dict-Dispatch" auf.

### 8. f-Strings (formatierte Strings)

Ein String mit `f` davor erlaubt `{...}`-Platzhalter mit echtem Code drin:

```python
name = "Rex"
print(f"Hallo {name}, 2+2 = {2+2}")    # -> Hallo Rex, 2+2 = 4
```

### 9. Module und `import`

> **🔑 Begriff – Modul:** Eine `.py`-Datei **ist** ein Modul. Ihr Name ist der
> Dateiname ohne `.py`. `import x` lädt das Modul `x.py`.

```python
from modul5_entwurfsmuster import konfiguration   # hole EIN Ding aus dem Modul
import modul5_entwurfsmuster as m                  # hole das GANZE Modul, nenn es m
```

Das Modul-System wird in 5.1 noch eine zentrale Rolle spielen — also merk dir
schon: *eine Datei = ein Modul, beim ersten Import wird sie ausgeführt.*

### 10. „Alles ist ein Objekt"

Das ist der Satz, der Python von Java am stärksten unterscheidet — und der
halbe Grund, warum dieses Modul existiert:

> In Python sind **auch Funktionen und Klassen selbst Objekte/Werte**. Man kann
> eine Funktion in einer Variablen speichern, in eine Liste legen, als
> Argument übergeben oder aus einer Funktion zurückgeben — genau wie eine Zahl.

```python
f = print           # f zeigt jetzt auf die Funktion print (kein Aufruf!)
f("Hallo")          # -> Hallo   (Aufruf über die Variable)
```

> **🔑 Begriff – first-class:** Wenn man mit etwas all das tun kann (speichern,
> übergeben, zurückgeben), nennt man es **first-class** („erstklassig"). In
> Python sind Funktionen und Klassen first-class. In Java sind sie das nicht
> im selben Maße — dort braucht man Interfaces, Lambdas oder Reflection, um
> Ähnliches zu erreichen.

Mit diesen zehn Punkten kannst du jede Zeile dieses Hefts lesen. Los geht's.

---

## 5.0 Was ist ein Entwurfsmuster?

Ein **Entwurfsmuster** (engl. *design pattern*) ist eine bewährte,
sprach­unabhängige **Schablone** für ein wiederkehrendes Entwurfsproblem.
„Schablone" heißt: keine fertige Klasse zum Kopieren, sondern eine *Idee*, wie
man ein bestimmtes Problem strukturiert löst.

> **🔑 Begriff – Boilerplate:** Wiederkehrender Standard-Code, den man nur
> schreibt, „weil die Sprache es so verlangt" — nicht, weil er das eigentliche
> Problem löst. Java-Getter/Setter sind ein klassisches Beispiel. Ein
> Leitmotiv dieses Moduls: Python braucht für viele Muster **weniger**
> Boilerplate.

Der Klassiker ist das Buch *"Design Patterns: Elements of Reusable Object-
Oriented Software"* (1994) der sogenannten **Gang of Four** (GoF: Gamma, Helm,
Johnson, Vlissides) mit 23 Mustern in drei Kategorien:

| Kategorie | Frage | Beispiele |
|---|---|---|
| **Erzeugungsmuster** | Wie *entstehen* Objekte? | **Singleton, Factory**, Builder, Prototype |
| **Strukturmuster** | Wie *passen* Objekte zusammen? | Adapter, Decorator, Composite |
| **Verhaltensmuster** | Wie *kommunizieren* Objekte? | **Observer, Strategy**, Command, Iterator |

Die fett gedruckten Muster behandeln wir in diesem Modul.

Diese Muster wurden ursprünglich für **statisch typisierte, klassenbasierte**
Sprachen wie C++ und Java formuliert. Pythons **dynamisches** Typsystem und
seine „alles ist ein Objekt"-Philosophie verändern den Werkzeugkasten: Viele
Muster wirken in Python kleiner, weil die Sprache bereits *fertig mitbringt*,
was anderswo erst durch Pattern-Code hergestellt werden muss.

> **Peter Norvigs These (Vortrag *"Design Patterns in Dynamic Programming"*,
> 1996):** Sinngemäß beobachtet er, dass 16 der 23 GoF-Muster in hinreichend
> dynamischen Sprachen (er nennt Lisp und Dylan) eine *qualitativ einfachere —
> oder gar keine eigene —* Implementierung haben, weil dort Typen und
> Funktionen first-class sind. Wir sehen in diesem Modul an mehreren Mustern,
> was damit gemeint ist. *(Hinweis: Das ist sinngemäß wiedergegeben; die exakte
> Formulierung variiert je nach Quelle, also nicht als wörtliches Zitat zitieren.)*

### Pythons Werkzeugkasten – das Vokabular dieses Moduls

Vier Sprachmittel tauchen in fast jedem Muster wieder auf. Wer diese vier
versteht, hat die halbe Miete. Wir erklären sie hier *kurz* und dann jeweils
*ausführlich* an der Stelle, wo sie zum ersten Mal arbeiten.

**1. Das Modul-System.** Eine `.py`-Datei ist ein Modul. Beim **ersten** Import
führt Python den Datei-Inhalt **genau einmal** aus und merkt sich das Ergebnis.
Dadurch existieren Variablen auf Modul-Ebene *genau einmal pro Programmlauf*.
→ trägt das **Singleton**-Muster (5.1).

**2. First-class Funktionen und Klassen.** Beide sind Werte: in Variablen
speicherbar, in Listen/Dicts ablegbar, als Argument übergebbar, als Rückgabe
zurückgebbar. → trägt **Factory** und **Strategy** (5.2, 5.5).

> **🔑 Begriff – Callable:** Alles, was man mit Klammern `(...)` *aufrufen*
> kann. Dazu gehören Funktionen, Lambdas (kurze anonyme Funktionen), Methoden
> **und** Objekte mit einer `__call__`-Methode. „Callable" ist Pythons
> gemeinsamer Nenner statt eines Interfaces. → trägt **Observer** (5.3).

**3. Dunder-Methoden.** 

> **🔑 Begriff – Dunder:** Kurz für „**d**ouble **under**score" (doppelter
> Unterstrich). Methoden wie `__init__`, `__new__`, `__call__`, `__str__`,
> `__enter__`, `__exit__` heißen so, weil sie von zwei Unterstrichen umrahmt
> sind. Es sind **Andock-Punkte für den Python-Interpreter**: Definierst du
> `__str__`, weiß `print()` automatisch, wie es dein Objekt darstellen soll.
> Du rufst Dunder selten direkt auf — die Sprache ruft sie für dich.

→ tragen **Singleton** (`__new__`), **Observer** (`__call__`) und **Context
Manager** (`__enter__`/`__exit__`).

**4. Decorators.**

> **🔑 Begriff – Decorator:** Eine Funktion, die eine andere Funktion **oder**
> Klasse entgegennimmt und etwas „Aufgewertetes" zurückgibt. Geschrieben wird
> das mit `@name` direkt über der Definition. Mehr dazu in 5.1 (Variante 3) —
> dort sieht man genau, was `@` im Hintergrund tut.

Mit diesem Vokabular im Hinterkopf gehen wir die Muster eines nach dem anderen
durch — immer nach demselben Schema: *Das Problem → Pythonisch lösen →
Varianten → Wo es einem in Python begegnet → Wann man es nicht braucht.*

---

## 5.1 Singleton

### Das Problem

Manchmal soll es von einer Sache **genau eine** geben — und alle, die sie
benutzen, sollen *dieselbe* benutzen. Typische Beispiele:

- ein **Logger**, der alle Log-Zeilen des Programms sammelt,
- ein **Konfigurations-Container** mit Einstellungen (Sprache, Debug-Modus …),
- ein **Verbindungspool** zur Datenbank.

Wenn jeder Programmteil sich „seinen eigenen" Logger oder „seine eigene"
Konfiguration erzeugt, hat man am Ende zehn halb gefüllte Objekte statt eines
gemeinsamen. Das **Singleton-Muster** beantwortet die Frage: *„Wie sorge ich
dafür, dass es nur eine Instanz gibt und alle dieselbe bekommen?"*

> **☕ Aus Java bekannt:** Das klassische Java-Rezept ist ein privater
> Konstruktor plus eine statische Methode `getInstance()`, die eine
> `private static`-Variable zurückgibt. Python braucht das in den meisten
> Fällen gar nicht — und das ist der spannende Teil.

### Pythonisch lösen — das Modul-System *ist* schon ein Singleton

Der Schlüssel ist nicht ein Stück Pattern-Code, sondern Pythons
**Importsystem**. Wir müssen kurz verstehen, was beim Import passiert, denn
darauf beruht die ganze Eleganz.

> **🔑 Begriff – `sys.modules`:** Ein eingebautes Wörterbuch (dict), das Python
> für jeden Programmlauf führt. Schlüssel = Modulname, Wert = das geladene
> Modul-Objekt. Es ist Pythons „Liste der schon geladenen Module".

Wenn du zum **allerersten Mal** `import einmodul` schreibst, passiert dreierlei:

1. Python **führt den gesamten Datei-Inhalt von `einmodul.py` einmal aus**.
   Dabei entstehen alle Variablen, die auf Modul-Ebene stehen (z. B. eine Zeile
   `konfiguration = _Konfiguration()` legt genau jetzt *ein* Objekt an).
2. Das fertige Modul-Objekt wird in `sys.modules` **abgelegt** (gecacht),
   ungefähr so: `sys.modules["einmodul"] = <Modul-Objekt>`.
3. **Jeder weitere** `import einmodul` — egal aus welcher Datei im Projekt —
   findet das Modul in `sys.modules` und gibt es **zurück, ohne den Datei-Inhalt
   erneut auszuführen.**

> **🔑 Begriff – cachen:** Ein einmal berechnetes Ergebnis aufheben, um es beim
> nächsten Mal sofort wiederzugeben, statt es neu zu berechnen. Python *cacht*
> Module.

Die Folge: Eine Variable auf Modul-Ebene existiert **genau einmal pro
Programmlauf** und wird von allen geteilt, die das Modul importieren. Das ist
der pythonische Singleton — die Garantie liefert das Sprachsystem, nicht wir.

### Variante 1: Der Modul-Singleton (der Standardfall)

```python
# datei: konfiguration.py
class _Konfiguration:                  # führender _ : "intern, bitte nicht direkt nutzen"
    def __init__(self):
        self.sprache = "de"
        self.debug = False

konfiguration = _Konfiguration()       # <-- läuft EINMAL beim ersten Import
```

Jetzt benutzen zwei verschiedene Dateien dasselbe Objekt:

```python
# datei a.py
from konfiguration import konfiguration
konfiguration.debug = True             # a ändert das gemeinsame Objekt

# datei b.py
from konfiguration import konfiguration
print(konfiguration.debug)             # -> True : b sieht die Änderung von a!
```

**Was hier wichtig ist:** `b.py` hat nichts „bekommen kopiert". Beide Dateien
sehen *dasselbe* Objekt, weil das Modul `konfiguration` nur einmal ausgeführt
wurde. Kein Pattern-Code, keine `getInstance()`-Methode. **Das Sprachsystem
erledigt es.**

> **🐍 Pythonisch gedacht:** Bevor du eine Singleton-Klasse baust, frag dich:
> „Reicht nicht einfach eine Variable in einem Modul?" Meistens: ja.

> **⚠️ Stolperstein — was genau ist garantiert?** Der Modul-Singleton
> garantiert *eine geteilte Instanz, die alle importieren* — **nicht**, dass
> die Klasse sich kein zweites Mal instanziieren ließe. Es gibt zwei Wege zu
> einem zweiten Objekt:
>
> 1. **Von Hand:** Wer `_Konfiguration()` direkt aufruft, bekommt sehr wohl
>    eine separate, zweite Instanz. Nichts in der Sprache verbietet das.
> 2. **Dieselbe Datei landet unter zwei Namen in `sys.modules`.** Der Schlüssel
>    ist: `sys.modules` wird nach dem **Namen** abgelegt, unter dem ein Modul
>    geladen wurde — nicht nach dem Dateipfad. Die Falle Schritt für Schritt:
>    - Startest du `konfiguration.py` **direkt** mit `python konfiguration.py`,
>      läuft die Datei unter dem Sondernamen `"__main__"`. Python legt
>      `sys.modules["__main__"]` an und führt dabei die Zeile
>      `konfiguration = _Konfiguration()` aus → **Instanz Nr. 1**.
>    - Importiert nun eine *andere* Datei dieselbe Datei mit
>      `import konfiguration`, sucht Python nach dem Namen `"konfiguration"` —
>      der steht aber noch **nicht** in `sys.modules` (dort liegt sie ja als
>      `"__main__"`). Python erkennt die Datei also **nicht** wieder, lädt sie
>      ein zweites Mal unter dem Namen `"konfiguration"` und führt die
>      Erzeugungszeile erneut aus → **Instanz Nr. 2**.
>
>    Ergebnis: dieselbe Datei sitzt zweimal in `sys.modules` (als `"__main__"`
>    und als `"konfiguration"`), mit zwei verschiedenen `_Konfiguration`-
>    Instanzen. (Faustregel: dieselbe Datei nicht *gleichzeitig* direkt starten
>    **und** anderswo importieren — die Start-Datei und die importierten Module
>    sauber trennen.)
>
> Die Garantie „nur einer" beruht also auf der **Konvention**, immer das
> Modul-Attribut zu importieren und die Klasse nie von Hand erneut zu
> instanziieren. Wer möchte, dass die *Klasse selbst* einen zweiten Aufruf
> verweigert, braucht einen echten Eingriffspunkt — genau das leisten die
> beiden nächsten Varianten. Das ist der Grund, warum es überhaupt drei
> Varianten gibt.

### Variante 2: `__new__` als expliziter Eingriffspunkt

Wer den Singleton-Charakter **in der Klasse selbst** verankern will, hängt sich
in `__new__` ein.

> **🔑 Begriff – `__new__` vs `__init__`:** Bei `Klasse()` laufen *zwei*
> Schritte. Zuerst `__new__`: es **erzeugt** das Objekt (gibt Speicher zurück).
> Danach `__init__`: es **befüllt** das schon erzeugte Objekt mit Werten.
> `__new__` ist also der frühere, seltener benutzte Haken — und genau der
> richtige Ort, um zu entscheiden: „neues Objekt — oder das alte zurückgeben?"

```python
class LoggerJavaStil:
    _instanz = None                          # Klassen-Attribut: der Cache-Platz

    def __new__(cls):                        # 'cls' ist die Klasse selbst
        if cls._instanz is None:             # gibt es noch keine Instanz?
            cls._instanz = super().__new__(cls)   # dann genau EINE erzeugen
            cls._instanz.eintraege = []      # und einmalig initialisieren
        return cls._instanz                  # sonst die vorhandene zurückgeben

    def log(self, nachricht):
        self.eintraege.append(nachricht)
```

```python
a = LoggerJavaStil()
b = LoggerJavaStil()
a is b              # -> True : dasselbe Objekt (s. 'is' im Crashkurs)
```

Zeile für Zeile:

- `_instanz = None` steht **auf Klassen-Ebene** (nicht in `__init__`). 

  > **🔑 Begriff – Klassen-Attribut vs Instanz-Attribut:** Ein
  > *Klassen-Attribut* gehört der Klasse selbst und wird von allen Instanzen
  > geteilt (vergleichbar mit `static` in Java). Ein *Instanz-Attribut*
  > (`self.eintraege`) gehört einer einzelnen Instanz. `_instanz` ist
  > absichtlich ein Klassen-Attribut — es soll *eine* gemeinsame Ablage sein.

- `cls` ist bei `__new__` die **Klasse** (nicht die Instanz — die gibt es ja
  noch nicht). `cls._instanz` ist also „die gemeinsame Ablage der Klasse".
- `super().__new__(cls)` erzeugt das eigentliche, rohe Objekt (das macht die
  Basisklasse `object`). Das tun wir nur, wenn noch keins existiert.
- `return cls._instanz` gibt **immer** dieselbe Instanz zurück.

Drei Dinge solltest du wissen:

- **`__init__` läuft bei *jedem* Aufruf erneut** — auch wenn `__new__` das alte
  Objekt zurückgibt. Hätten wir `eintraege` in `__init__` gesetzt, würde es bei
  jedem `LoggerJavaStil()` zurückgesetzt. Deshalb initialisieren wir einmalig in
  `__new__` (geschützt durch die `is None`-Prüfung).
- **Threadsicher ist das nicht.** 

  > **🔑 Begriff – GIL & Threadsicherheit:** Der *Global Interpreter Lock* sorgt
  > in CPython dafür, dass immer nur **ein** Thread Python-Bytecode ausführt.
  > Er schützt aber nur **einzelne** Operationen, nicht eine Folge wie „prüfe,
  > *ob* `_instanz` None ist, **und dann** erzeuge sie". Zwei Threads könnten
  > beide das `is None` als wahr sehen und je ein Objekt bauen. Wer
  > Threadsicherheit braucht: ein `threading.Lock()` um die Erzeugung legen —
  > oder gleich den Modul-Singleton nehmen, der durch das Importsystem ohnehin
  > nur einmal entsteht.

- **Vererbung wird unangenehm:** Alle Unterklassen würden sich dasselbe
  `_instanz` teilen (weil sie das Klassen-Attribut der Basis erben), wenn man
  nicht aufpasst — eine `Unterklasse()` könnte überraschend die Basis-Instanz
  zurückbekommen.

### Variante 3: Der `@singleton`-Decorator

Diese Variante macht die Singleton-Eigenschaft **sichtbar am Klassen-Kopf** und
ist auf *jede* Klasse wiederverwendbar.

Zuerst der Decorator selbst:

```python
def singleton(klasse):
    instanzen = {}                            # Cache: Klasse -> ihre eine Instanz
    def hole_instanz(*args, **kwargs):        # ersetzt künftig "Klasse(...)"
        if klasse not in instanzen:
            instanzen[klasse] = klasse(*args, **kwargs)   # einmal erzeugen
        return instanzen[klasse]              # sonst die gecachte zurückgeben
    return hole_instanz
```

> **🔑 Begriff – `*args, **kwargs`:** Pythons Schreibweise für „nimm beliebig
> viele Argumente entgegen". `*args` sammelt die *Positions*-Argumente,
> `**kwargs` die *Schlüsselwort*-Argumente. So funktioniert `hole_instanz` für
> jede Klasse, egal wie viele Argumente deren Konstruktor erwartet.

Angewendet:

```python
@singleton
class Datenbankverbindung:
    def __init__(self, dsn="lokal://default"):
        self.dsn = dsn
```

> **🔑 Begriff – Decorator-Syntax `@`:** Die Zeile `@singleton` über `class
> Datenbankverbindung` ist **nur Abkürzung** für:
> `Datenbankverbindung = singleton(Datenbankverbindung)`.
> Das heißt: Python nimmt deine frisch definierte Klasse, schickt sie durch die
> Funktion `singleton`, und der Name `Datenbankverbindung` zeigt danach auf
> **das Ergebnis** — hier auf die Funktion `hole_instanz`.

Aus Sicht des Aufrufers bleibt alles wie gewohnt:

```python
db1 = Datenbankverbindung("postgres://prod")
db2 = Datenbankverbindung("wird-ignoriert")   # Konstruktor läuft NICHT erneut
db1 is db2                                     # -> True
```

Beim zweiten Aufruf gibt `hole_instanz` einfach die gecachte Instanz zurück —
deshalb wird das Argument `"wird-ignoriert"` schlicht **ignoriert**.

> **⚠️ Stolperstein — der Preis dieser Variante:** Weil `Datenbankverbindung`
> jetzt eine **Funktion** ist (nämlich `hole_instanz`) und keine Klasse mehr,
> brechen Dinge, die eine Klasse erwarten:
> - `isinstance(db1, Datenbankverbindung)` wirft `TypeError` (das zweite
>   Argument ist keine Klasse mehr).
> - Vererbung `class X(Datenbankverbindung): ...` ist nicht mehr möglich.
> - Introspektion/Typhinweise sehen eine Funktion statt der Klasse.
> - Argumente ab dem **zweiten** Aufruf werden stillschweigend verschluckt.
>
> Darum bleibt der **Modul-Singleton der Standardfall**; der Decorator lohnt
> sich nur, wenn man die Singleton-Eigenschaft sichtbar dokumentieren will und
> mit diesen Einschränkungen leben kann.

### Wo das in Python begegnet

Die Standardbibliothek nutzt Modul-Singletons an vielen Stellen — du hast sie
also längst benutzt, ohne es „Singleton" zu nennen:

- `sys.modules` — das Cache-Dict aller Module ist selbst genau einmal vorhanden.
- `logging.getLogger("name")` — gibt für **denselben Namen** immer **denselben**
  Logger zurück (intern eine Registry, s. 5.2).
- `random.random()` — arbeitet auf einer modul-internen, einmalig erzeugten
  `Random`-Instanz.

### Wann welche Variante?

| Variante | Wann benutzen |
|---|---|
| **Modul-Singleton** | Standardfall. Praktisch immer die richtige Wahl. |
| **`@singleton`-Decorator** | Wenn die Singleton-Eigenschaft sichtbar am Klassen-Kopf stehen soll und die Einschränkungen oben akzeptabel sind. |
| **`__new__`-Variante** | Akademisch interessant, in der Praxis selten nötig. |
| **Metaklassen-Singleton** | Existiert auch (man überschreibt das Verhalten von `type`), ist aber für fast alle Fälle überdimensioniert. |

### Wann braucht man das Muster *nicht*?

Singletons sind in der Python-Community **umstritten**, denn ein Singleton ist
**globaler Zustand**: ein Objekt, das überall sichtbar und veränderbar ist.

> **🔑 Begriff – globaler Zustand:** Daten, die nicht über Parameter
> weitergereicht, sondern „von überall" erreichbar sind. Praktisch, aber
> schwer zu testen (im Test schwer auszutauschen) und schwer nachzuvollziehen
> (man sieht der Funktionssignatur nicht an, dass sie das globale Ding benutzt).

Die erfahrene Alternative heißt **Dependency Injection** (DI):

> **🔑 Begriff – Dependency Injection:** „Abhängigkeit hineinreichen." Statt
> dass eine Funktion sich das benötigte Objekt selbst aus einer globalen
> Variablen holt, bekommt sie es als **Parameter** übergeben. Vorteile: im Test
> kann man eine Fake-Version übergeben (Mock), der Datenfluss steht sichtbar im
> Code, und man kann bei Bedarf mehrere Instanzen nebeneinander haben.

> **Faustregel:** Ein Singleton einzusetzen, „weil man das so macht", ist ein
> Reflex aus statisch typisierten Sprachen. In Python lohnt sich jedes Mal die
> Frage: *„Brauche ich das wirklich — oder reicht ein Modul-Attribut, oder
> sollte ich das Objekt lieber explizit übergeben?"*

---

## 5.2 Factory

### Das Problem

Der Aufrufer soll ein Objekt eines passenden **Untertyps** bekommen, ohne den
konkreten Typ zu kennen. Beispiel: *„Gib mir ein Tier vom Typ `'hund'`."* Die
aufrufende Stelle weiß nichts von der Klasse `Hund` — sie kennt nur den
Oberbegriff `Tier` und einen String wie `"hund"`.

> **🔑 Begriff – Untertyp / Obertyp (Vererbung):** Wenn `Hund` von `Tier`
> *erbt*, ist `Hund` ein **Untertyp** von `Tier`. Jeder `Hund` *ist auch ein*
> `Tier`. Eine Funktion, die ein `Tier` erwartet, akzeptiert daher jeden `Hund`,
> jede `Katze` usw. Das nennt man **Polymorphie**.

> **🔑 Begriff – Factory (Fabrik):** Eine Stelle, deren Job es ist, **Objekte
> herzustellen**. Statt überall im Code `Hund()`, `Katze()`, `Kuh()` zu rufen,
> ruft man `erzeuge_tier("hund")` — die Factory entscheidet, *welche* Klasse.

### Vorbereitung: die abstrakte Basisklasse

Damit alle Tiere denselben „Vertrag" erfüllen, definieren wir eine abstrakte
Basisklasse:

```python
from abc import ABC, abstractmethod      # "abstract base class" aus der Stdlib

class Tier(ABC):                          # erbt von ABC -> ist abstrakt
    @abstractmethod
    def laut(self) -> str: ...            # KEINE Implementierung, nur der Vertrag

    def __str__(self):
        return f"{type(self).__name__}({self.laut()!r})"
```

> **🔑 Begriff – abstrakte Klasse / `@abstractmethod`:** Eine **abstrakte
> Klasse** kann man nicht direkt instanziieren — sie legt nur fest, *welche*
> Methoden ihre Untertypen haben **müssen**. `@abstractmethod` markiert eine
> solche Pflichtmethode. Versucht jemand, eine Unterklasse zu instanziieren,
> die `laut()` nicht implementiert, gibt es einen `TypeError`. Das ist Pythons
> Gegenstück zu Javas `abstract class` / `interface`.

> **🔑 Begriff – `...` (Ellipsis):** Die drei Punkte sind ein echtes Python-
> Objekt und werden hier als „leerer Platzhalter-Körper" benutzt — gleichwertig
> zu `pass`. Sie sagen: „hier kommt absichtlich nichts hin".

> **🔑 Begriff – `type(self).__name__` und `!r`:** `type(self)` liefert die
> Klasse des Objekts, `.__name__` deren Namen als String (z. B. `"Hund"`). Das
> `!r` in einem f-String bedeutet „nimm die *repr*-Darstellung" — für Strings
> heißt das *mit* Anführungszeichen, praktisch fürs Debuggen.

Die konkreten Tiere sind dann einfach:

```python
class Hund(Tier):
    def laut(self): return "Wuff"

class Katze(Tier):
    def laut(self): return "Miau"

class Kuh(Tier):
    def laut(self): return "Muh"
```

### Variante 1: explizit mit `if/elif`

Der direkte Weg — eine Factory-Klasse mit einer Verzweigung pro Art:

```python
class TierFactoryJavaStil:
    @staticmethod
    def erzeuge(art: str) -> Tier:
        if art == "hund":    return Hund()
        elif art == "katze": return Katze()
        elif art == "kuh":   return Kuh()
        else: raise ValueError(f"Unbekannte Tierart: {art!r}")
```

> **🔑 Begriff – `@staticmethod`:** Eine Methode, die **kein** `self` braucht,
> weil sie nicht auf Instanz-Daten zugreift. Man ruft sie direkt über die
> Klasse: `TierFactoryJavaStil.erzeuge("hund")`. Vergleichbar mit einer
> `static`-Methode in Java.

Das ist lesbar — aber jede neue Tierart erzwingt **eine neue Code-Zeile in der
Factory**. Bei 30 Tierarten hat man 30 Zweige. Und wer eine Art ergänzen will,
muss diese (vielleicht fremde) Factory-Funktion editieren.

### Variante 2: Dict-Dispatch (Registry) — der pythonische Weg

Erinnerung aus dem Crashkurs: **Klassen sind first-class Objekte.** Man kann
eine Klasse also in ein dict legen und später nachschlagen.

> **🔑 Begriff – Dispatch:** „Verteilen/Weiterleiten an die richtige Stelle."
> *Dict-Dispatch* heißt: Ein dict bildet einen Schlüssel (`"hund"`) direkt auf
> das passende Ziel (die Klasse `Hund`) ab — statt einer `if/elif`-Kette.

> **🔑 Begriff – Registry (Register):** Eine zentrale Tabelle, in die sich
> Dinge „eintragen". Hier: ein dict, das Namen auf Klassen abbildet.

```python
_TIER_REGISTRY = {        # Schlüssel: String -> Wert: die Klasse SELBST (nicht eine Instanz!)
    "hund":  Hund,
    "katze": Katze,
    "kuh":   Kuh,
}

def erzeuge_tier(art: str) -> Tier:
    if art not in _TIER_REGISTRY:
        raise ValueError(f"Unbekannte Tierart: {art!r}")
    return _TIER_REGISTRY[art]()       # Klasse nachschlagen UND aufrufen
```

Die entscheidende Zeile ist `_TIER_REGISTRY[art]()`. Lies sie in zwei Schritten:

1. `_TIER_REGISTRY[art]` schlägt im dict nach und liefert **die Klasse** (z. B.
   `Hund`) — noch kein Objekt!
2. Die Klammern `()` dahinter **rufen** diese Klasse auf, was eine **Instanz**
   erzeugt (`Hund()`).

> **⚠️ Stolperstein:** Im dict stehen `Hund`, `Katze` (ohne Klammern) — also die
> **Klassen selbst**, nicht `Hund()`, `Katze()`. Stünden dort Klammern, lägen
> bereits *Instanzen* im dict, und alle Aufrufer bekämen dasselbe Objekt. Wir
> wollen aber bei jedem Aufruf eine *frische* Instanz.

**Vorteile gegenüber `if/elif`:**

- **Neue Art = eine Zeile im dict.** Die Funktion `erzeuge_tier` bleibt
  unverändert.
- **Lookup ist O(1)** (dict-Zugriff ist konstant schnell) statt O(n) (die
  if/elif-Kette wird im Schnitt halb durchlaufen). Bei drei Einträgen egal, bei
  fünfzig relevant.

  > **🔑 Begriff – O(1) / O(n):** Grobe Maße für „wie wächst die Laufzeit mit der
  > Größe?". *O(1)* = gleich schnell, egal wie viele Einträge. *O(n)* = linear
  > langsamer, je mehr Einträge.

- **Erweiterbar zur Laufzeit** — das ist der eigentliche Gewinn (s. u.).

**Der Beweis für den Vorteil: Registrierung zur Laufzeit.**

```python
class Drache(Tier):
    def laut(self): return "Feuer speien"

_TIER_REGISTRY["drache"] = Drache       # genau EINE Zeile
erzeuge_tier("drache")                  # -> Drache('Feuer speien')
```

`erzeuge_tier` selbst wurde dafür **nicht angefasst**. Mit `if/elif` wäre das
unmöglich gewesen, ohne den Quelltext der Factory zu ändern. Das ist das
**Open/Closed-Prinzip** in einer Zeile:

> **🔑 Begriff – Open/Closed-Prinzip:** „Offen für Erweiterung, geschlossen für
> Änderung." Man soll neues Verhalten *hinzufügen* können, ohne bestehenden,
> getesteten Code zu *ändern*. Die Registry erfüllt das mustergültig.

**Decorator-Variante** (für Fortgeschrittene): Jede Klasse „meldet sich selbst"
an, statt dass man die Registry getrennt pflegt.

```python
TIERE = {}

def registriere(art):                   # nimmt den Namen, gibt einen Decorator zurück
    def deco(klasse):
        TIERE[art] = klasse             # Klasse eintragen
        return klasse                   # Klasse unverändert zurückgeben
    return deco

@registriere("hund")
class Hund(Tier):
    def laut(self): return "Wuff"
```

Frameworks wie **Django** und **Flask** funktionieren im Kern genau so:
`@app.route("/pfad")` trägt deine Funktion in eine Routen-Tabelle ein.

### Variante 3: `@classmethod` als alternativer Konstruktor

Wenn die Varianten schon **zur Programmierzeit feststehen** (du weißt jetzt
schon, dass es „Margherita" und „Salami" gibt) und du nur **bequeme, benannte**
Konstruktoren willst, brauchst du gar keine Factory-Klasse — die
Erzeugungslogik gehört direkt in die Klasse.

> **🔑 Begriff – `@classmethod`:** Eine Methode, die als ersten Parameter nicht
> `self` (die Instanz), sondern `cls` (die Klasse) bekommt. Damit kann sie neue
> Instanzen erzeugen (`cls(...)`). Man ruft sie über die Klasse auf:
> `Pizza.margherita()`. Java-Brücke: ein *static factory method* wie
> `Pizza.margherita()` statt `new Pizza(...)`.

```python
class Pizza:
    def __init__(self, belaege):
        self.belaege = belaege

    @classmethod
    def margherita(cls):
        return cls(["Tomate", "Mozzarella", "Basilikum"])

    @classmethod
    def salami(cls):
        return cls(["Tomate", "Mozzarella", "Salami"])
```

```python
p1 = Pizza.margherita()
p2 = Pizza.salami()
```

`Pizza.margherita()` liest sich wie **Fachsprache** („eine Margherita, bitte")
— näher am Anwendungsproblem als ein Lookup mit einer Zeichenkette.

### Wo das in Python begegnet

- `dict.fromkeys(seq)` bzw. `dict.fromkeys(seq, wert)` — ein klassisches
  `@classmethod`-Factory (ein Methodenname, optionaler zweiter Parameter).
- `datetime.fromisoformat(s)`, `datetime.fromtimestamp(t)` — alternative
  Konstruktoren als `@classmethod` (erzeugen ein `datetime` aus verschiedenen
  Eingaben).
- Plugin-Systeme über `entry_points` in `pyproject.toml` — im Kern eine zur
  Laufzeit erweiterte Registry.

> **⚠️ Abgrenzung:** `json.loads` / `pickle.loads` werden oft als Factory-
> Beispiel genannt, weil sie je nach Inhalt verschiedene Typen liefern. Das ist
> aber nur *verwandt*: Es gibt keinen gemeinsamen Obertyp, aus dessen
> Untertypen ausgewählt wird (sie liefern eingebaute Typen wie `dict`, `list`,
> `int`). Eine echte Factory wählt einen passenden Untertyp eines gemeinsamen
> Vertrags aus — wie `erzeuge_tier` einen `Tier`-Untertyp.

### Wann welche Variante?

> **Faustregel:** Kommt die Auswahl per **String/Enum zur Laufzeit** (z. B. aus
> einer Konfiguration oder Nutzereingabe) → **Dict-Dispatch**. Steht die Auswahl
> **zur Programmierzeit** fest und du willst nur bequeme Konstruktoren →
> **`@classmethod`**.

### Wann braucht man das Muster *nicht*?

Bei nur **einer** Klasse, oder wenn der Aufrufer den konkreten Typ ohnehin
kennt, ist eine Factory überflüssig — dann ruf einfach den Konstruktor direkt.
Pythonischer Pragmatismus: *nicht abstrahieren, was nicht abstrahiert werden
muss.*

---

## 5.3 Observer

### Das Problem

Ein Objekt (genannt **Subject** oder **Publisher**, „Herausgeber") hält andere
Objekte (genannt **Observer** oder **Subscriber**, „Abonnenten") auf dem
Laufenden — **ohne sie im Detail zu kennen**. Beispiele: ein Newsletter-Versand,
ein Event-Bus, oder „wenn sich das Modell ändert, sollen sich alle Anzeigen
aktualisieren" (genau das brauchen wir gleich für MVC in 5.4).

> **🔑 Begriff – Subject & Observer:** Das **Subject** ist die Quelle der
> Neuigkeiten. Die **Observer** sind die, die benachrichtigt werden wollen. Das
> Subject führt eine Liste seiner Observer und sagt allen Bescheid, wenn etwas
> passiert — kennt aber nicht ihre konkreten Klassen.

> **☕ Aus Java bekannt:** In Java definiert man dafür typischerweise ein
> `interface Listener { void onEvent(...); }`, und jeder Beobachter ist eine
> Klasse, die dieses Interface implementiert. Python kommt — wie wir gleich
> sehen — ganz ohne Interface aus.

### Pythonisch lösen — eine Liste von Callables

Erinnerung aus dem Crashkurs: Ein **Callable** ist alles, was man mit `(...)`
aufrufen kann. Genau das ist der Trick: Das Subject muss seine Observer **nicht**
über ein Interface kennen — es reicht, dass sie *aufrufbar* sind. Es hält also
einfach eine **Liste von Callables**.

```python
from typing import Callable               # nur für den Typ-Hinweis

class Newsletter:
    def __init__(self):
        self._abonnenten = []             # Liste der Callables (Observer)

    def abonnieren(self, callback):       # einen Observer hinzufügen
        self._abonnenten.append(callback)

    def abbestellen(self, callback):      # einen Observer entfernen
        self._abonnenten.remove(callback)

    def veroeffentlichen(self, ausgabe):  # alle benachrichtigen
        for callback in self._abonnenten:
            callback(ausgabe)             # einfach aufrufen — mehr braucht es nicht
```

Das Herzstück ist die Schleife in `veroeffentlichen`: Für jeden Abonnenten in
der Liste wird `callback(ausgabe)` aufgerufen. `callback` kann **irgendetwas
Aufrufbares** sein — der Newsletter interessiert sich nicht dafür, *was* genau.

> **🔑 Begriff – Duck Typing:** „Wenn es wie eine Ente läuft und quakt, behandle
> es als Ente." Heißt: Python fragt nicht „bist du vom richtigen Typ/Interface?",
> sondern probiert einfach die Operation (hier: den Aufruf). Hat das Objekt das
> nötige Verhalten, klappt es. Das ist der Grund, warum kein gemeinsames
> Interface nötig ist.

Jetzt darf **alles Aufrufbare** Beobachter sein:

```python
# 1) eine ganz normale Funktion
def auf_konsole(text):
    print(f"[Konsole] {text}")

# 2) ein Lambda (kurze, namenlose Funktion)
archiv = []
archivieren = lambda text: archiv.append(text)

news = Newsletter()
news.abonnieren(auf_konsole)              # Funktion als Observer
news.abonnieren(archivieren)              # Lambda als Observer
news.abonnieren(print)                    # sogar die eingebaute print-Funktion!
news.veroeffentlichen("Ausgabe Mai 2026")
```

> **🔑 Begriff – Lambda:** Eine **kurze, namenlose Funktion** in einer Zeile.
> `lambda text: archiv.append(text)` ist gleichwertig zu `def f(text):
> return archiv.append(text)`. Praktisch, wenn man nur einen Einzeiler braucht.
> Java-Brücke: Pythons Lambda entspricht Javas `text -> archiv.add(text)`.

> **⚠️ Stolperstein:** Beachte `news.abonnieren(print)` — hier steht `print`
> **ohne** Klammern. Wir übergeben die Funktion *selbst* (als Wert), nicht ihr
> Ergebnis. `print` ohne `()` ist das Objekt; `print()` *ruft* es auf. Dieser
> Unterschied ist der Kern von „Funktionen sind first-class".

### Observer mit Gedächtnis: `__call__`

Manchmal soll ein Beobachter sich etwas **merken** (Zustand haben) — z. B.
mitzählen, wie viele Ausgaben kamen. Dafür macht man ein ganz normales Objekt
**aufrufbar**, indem man ihm die Dunder-Methode `__call__` gibt:

```python
class ZaehlenderAbonnent:
    def __init__(self, name):
        self.name = name
        self.empfangen = 0

    def __call__(self, ausgabe):          # macht Instanzen aufrufbar wie Funktionen
        self.empfangen += 1
```

```python
zaehler = ZaehlenderAbonnent("Statistik")
zaehler("Test")        # erlaubt! ruft __call__ auf -> empfangen ist jetzt 1
news.abonnieren(zaehler)   # zaehler ist ein Callable, also ein gültiger Observer
```

> **🔑 Begriff – `__call__`:** Definiert man diese Dunder-Methode, kann man eine
> **Instanz** wie eine Funktion aufrufen: `zaehler("Test")` führt
> `zaehler.__call__("Test")` aus. So bekommt man „eine Funktion mit Gedächtnis":
> Sie verhält sich wie ein Callable, kann aber zwischen Aufrufen Zustand in
> `self` speichern.

Das Schöne: Funktion, Lambda und `__call__`-Objekt sind drei **völlig
verschiedene** Dinge — und doch funktionieren alle drei als Observer, einzig
weil sie aufrufbar sind. Das ist Observer **und** Duck Typing zusammen.

### Wo das in Python begegnet

- **GUI-Frameworks** wie `tkinter` und `PyQt` arbeiten in ihrem Kern mit
  **Callback-Listen** für Events — die echte Eins-zu-viele-Form des Observers.
- Bibliotheken wie `blinker` und `pydispatch` packen das Muster in
  einsatzfertige „Signal"-Frameworks (ein Subject, viele Subscriber).
- `signal.signal(SIGINT, handler)` — **verwandt, aber nur ein** Handler pro
  Signal: Ein zweiter Aufruf *ersetzt* den ersten. Es ist also ein Callback,
  nicht die Eins-zu-viele-Benachrichtigung des klassischen Observers — zeigt
  aber dieselbe Grundidee: ein Callable wird für ein Ereignis registriert.

### Wann braucht man das Muster *nicht*?

Wenn es nur **einen** Beobachter gibt, reicht ein direkter Methodenaufruf —
die Abonnement-Liste ist dann unnötige Zeremonie. Und wohnen Subject und
Observer im selben Modul, ist oft ein direkter Funktionsaufruf klarer als eine
versteckte Signal-Kette. Pythons Leitsatz *„explizit ist besser als implizit"*
warnt vor zu vielen unsichtbaren Benachrichtigungswegen.

---

## 5.4 MVC – Model, View, Controller

### Das Problem

Eine Anwendung vermischt schnell drei Dinge, die eigentlich getrennt gehören:

- **Zustand** — die Daten (welche Figur steht wo?),
- **Darstellung** — wie der Nutzer die Daten sieht (Brett-Grafik? JSON?),
- **Steuerung** — was bei einer Eingabe passiert (Figur ziehen, prüfen).

Packt man alles in eine Klasse, kann man die Darstellung nicht austauschen,
ohne die Logik anzufassen — und man kann nichts testen, ohne eine Oberfläche zu
starten. **MVC** (Model–View–Controller) trennt diese drei Verantwortlichkeiten:

| Rolle | Aufgabe | In dieser Demo | Im REST-Backend |
|---|---|---|---|
| **Model** | Zustand + Fachlogik | Schachbrett (Figur + Feld) | Domänenobjekte / Datenbank |
| **View** | Darstellung | ASCII-Brett, JSON | HTTP-Antwort (z. B. JSON) |
| **Controller** | Eingaben verarbeiten | `Schachsteuerung.ziehe()` | Route-Handler (`POST /zug`) |

> **Warum dieses Muster hier wichtig ist:** In den Gruppenprojekten baut ihr
> REST-Backends — und die lassen sich sauber als MVC strukturieren: der
> Controller ist der Endpoint, die View ist die JSON-Antwort, das Model ist
> euer Datenbestand. Wer die drei Rollen trennt, hat ein wartbares Backend.
> *(REST und MVC sind nicht dasselbe — REST ist ein Architektur**stil** für
> Schnittstellen, MVC eine **interne** Aufteilung der Anwendung. Sie passen nur
> gut zusammen.)*

> **🔑 Begriff – REST-Backend:** Ein Server-Programm, das über HTTP angesprochen
> wird (z. B. `POST /zug` schickt einen Zug, `GET /brett` fragt den Zustand ab)
> und meist **JSON** zurückgibt. „Backend" = der Server-Teil, im Gegensatz zum
> „Frontend" (was der Nutzer im Browser sieht).

### Zwei Spielarten von MVC — wichtig für euer Projekt

Bevor wir Code schreiben, eine Unterscheidung, die später viel Verwirrung
spart. MVC gibt es in zwei Geschmacksrichtungen, die sich **nur** in einem
Punkt unterscheiden: *Wie erfährt die View von einer Änderung des Models?*

- **Klassisches / GUI-MVC („push"):** Das Model **benachrichtigt** seine Views,
  sobald es sich ändert — über genau das **Observer-Muster aus 5.3**. Das ist
  die ursprüngliche Smalltalk-Variante und das, was unsere Demo zeigt. Sinnvoll
  bei einer dauerhaft offenen Oberfläche, die sich „live" aktualisiert.
- **Web- / REST-MVC („pull"):** Eine HTTP-Anfrage löst alles aus. Der Controller
  liest/ändert das Model und baut die Antwort (View) **selbst** zusammen —
  danach ist der Request vorbei. Es gibt **keinen Observer**, keine
  Benachrichtigung; das Model „ruft" keine Views.

> **⚠️ Stolperstein:** Sucht in eurem Flask-/FastAPI-Projekt **nicht** nach
> einem Observer — dort ist keiner. Gemeinsam ist beiden Varianten nur die
> **Trennung der drei Rollen**; das ist der übertragbare Kern. Die
> Model→View-Kopplung per Observer ist die Besonderheit der GUI-Variante.

> **🔑 Begriff – push vs pull:** *Push* = die Quelle schiebt Neuigkeiten aktiv
> raus (Model ruft Views). *Pull* = der Interessent holt sich bei Bedarf den
> aktuellen Stand ab (Client fragt per HTTP, bekommt eine Antwort).

### Pythonisch lösen (klassische Variante — mit Observer)

MVC braucht in Python **kein neues Sprachmittel**. In der klassischen Variante
ist die einzige interessante Kopplung Model → View — und die *ist* das
Observer-Muster aus 5.3: Das Model hält eine Liste von Views (Callables) und
ruft sie bei Änderung auf.

**Das MODEL** — hält den Zustand und benachrichtigt seine Views:

```python
import json
from typing import Callable

class Schachbrett:                       # MODEL
    SPALTEN = "abcdefgh"                  # Klassen-Attribut: die Spalten a-h

    def __init__(self, figur="K", feld="e1"):
        self.figur = figur
        self.feld = feld
        self._views = []                  # die Observer-Liste (s. 5.3)

    def registriere_view(self, view):
        self._views.append(view)          # eine View = ein Callable

    def _benachrichtigen(self):
        for view in self._views:
            view(self)                    # jede View aufrufen, sich selbst übergeben

    def setze_feld(self, feld):
        self.feld = feld
        self._benachrichtigen()           # Zustand ändern -> alle Views aktualisieren
```

Beachte `view(self)` in `_benachrichtigen`: Das Model ruft jede View auf und
gibt ihr **sich selbst** (`self`, das ganze Brett) mit, damit die View den
aktuellen Zustand ablesen kann. Das Model kennt seine Views **nicht im Detail**
— es weiß nur, dass sie aufrufbar sind. Damit ist jede View einfach eine
Funktion, die den Modellzustand liest:

```python
def ascii_view(brett):                   # VIEW A – fürs Auge
    spalte = Schachbrett.SPALTEN.index(brett.feld[0])   # 'e' -> 4
    reihe = int(brett.feld[1:])                          # '1' -> 1
    for r in range(8, 0, -1):            # Reihen 8 herunter bis 1
        felder = (brett.figur if (c == spalte and r == reihe) else "."
                  for c in range(8))     # pro Spalte: Figur oder Punkt
        print(f"  {r} " + " ".join(felder))
    print("    " + " ".join(Schachbrett.SPALTEN))

def json_view(brett):                    # VIEW B – wie eine REST-Antwort
    print(json.dumps({"figur": brett.figur, "feld": brett.feld}))
```

Ein paar Bausteine in `ascii_view` erklärt:

> **🔑 Begriff – `range(8, 0, -1)`:** Erzeugt die Zahlenfolge 8, 7, 6, … 1
> (Start 8, Stopp *vor* 0, Schrittweite −1). Wir zählen rückwärts, weil ein
> Schachbrett oben die Reihe 8 zeigt.

> **🔑 Begriff – Slicing `brett.feld[1:]`:** `[1:]` nimmt den String **ab**
> Index 1 bis zum Ende. Aus `"e10"` würde so `"10"`. (Für unsere Felder ist es
> nur eine Ziffer, aber so ist es robust.) `feld[0]` ist das erste Zeichen.

> **🔑 Begriff – Generator-Ausdruck `(... for c in range(8))`:** Sieht aus wie
> eine Liste, benutzt aber runde Klammern. Er erzeugt die Werte **nacheinander
> bei Bedarf**. `" ".join(...)` fügt sie mit Leerzeichen zu einem String
> zusammen. Das `x if bedingung else y` darin ist Pythons **bedingter Ausdruck**
> (wie Javas `bedingung ? x : y`).

> **🔑 Begriff – `json.dumps(...)`:** „dump to string" — wandelt ein Python-dict
> in einen **JSON-String** um. `{"figur": "K"}` wird zu `'{"figur": "K"}'`.
> Genau diese Form schickt ein REST-Backend als Antwort zurück.

**Der CONTROLLER** — nimmt Eingaben, prüft sie, ändert das Model; er **rendert
nie selbst**:

```python
class Schachsteuerung:                   # CONTROLLER
    def __init__(self, brett):
        self.brett = brett

    def ziehe(self, feld):
        # Eingabe validieren, BEVOR das Model geändert wird:
        if len(feld) < 2 or feld[0] not in Schachbrett.SPALTEN or not feld[1:].isdigit():
            raise ValueError(f"Ungültiges Feld: {feld!r}")
        if not 1 <= int(feld[1:]) <= 8:
            raise ValueError(f"Reihe außerhalb des Bretts: {feld!r}")
        self.brett.setze_feld(feld)      # Model ändern -> Views reagieren automatisch
```

> **🔑 Begriff – `str.isdigit()`:** Liefert `True`, wenn ein String nur aus
> Ziffern besteht. `"7".isdigit()` → `True`, `"x".isdigit()` → `False`. Wird
> hier benutzt, um die Reihen-Angabe zu prüfen.

> **🔑 Begriff – Verkettete Vergleiche `1 <= x <= 8`:** Python erlaubt das
> direkt (anders als Java, wo man `1 <= x && x <= 8` schreiben müsste). Liest
> sich wie Mathematik.

### Das Zusammenspiel

```python
brett = Schachbrett(figur="K", feld="e1")
brett.registriere_view(ascii_view)       # zwei Views beobachten
brett.registriere_view(json_view)        # dasselbe Model

steuerung = Schachsteuerung(brett)
steuerung.ziehe("e2")    # EIN Aufruf -> Model ändert sich -> BEIDE Views aktualisieren sich
```

Die zentrale Beobachtung: **Ein** Controller-Aufruf ändert das Model, und das
Model benachrichtigt von selbst **alle** Views. Eine dritte View — etwa eine
Web-Oberfläche oder eine Logdatei — kommt mit
`brett.registriere_view(noch_eine_view)` dazu, **ohne eine Zeile am Model oder
Controller** zu ändern. Genau diese Erweiterbarkeit (wieder das Open/Closed-
Prinzip!) ist der Gewinn von MVC.

### Wo das in Python begegnet

- **GUI-Frameworks** (`tkinter`, `PyQt`): hier passt die **klassische** Variante
  unserer Demo — das Model benachrichtigt offene Views via Observer.
- **Flask / FastAPI** (Web-MVC, *pull*): Route-Handler (Controller)
  lesen/schreiben Models und geben eine Repräsentation zurück (View, meist
  JSON). Dieselben Rollen wie in der Demo, **aber ohne Observer** — der
  Controller baut die Antwort pro Anfrage selbst.
- **Django** nennt es **MTV** (Model–Template–View), dasselbe Prinzip in der
  Web-Spielart: Models (ORM) ↔ Views (Controller-Logik) ↔ Templates
  (Darstellung).

### Wann braucht man das Muster *nicht*?

Bei einem kleinen Skript ohne Oberfläche und mit nur einer Darstellung ist die
Dreiteilung Overhead. MVC zahlt sich aus, sobald es **mehr als eine View** gibt,
die Darstellung **austauschbar** sein soll, oder das Model **ohne Oberfläche
testbar** bleiben muss — also bei praktisch jedem Backend.

> **Kernlehre:** MVC ist kein neues Python-Sprachmittel, sondern eine
> Architektur-Entscheidung — die **Trennung von Zustand, Darstellung und
> Steuerung**. In der klassischen (GUI-)Variante trägt **Observer** die
> Model→View-Kopplung, wie in dieser Demo; in der Web-/REST-Variante baut der
> Controller die Antwort pro Anfrage selbst, ganz ohne Observer. Übertragbar ist
> die Trennung der drei Rollen, nicht das konkrete Kopplungs-Werkzeug.

---

## 5.5 Strategy *(Exkurs / Bonus)*

> *Exkurs:* In der 20-Minuten-Präsentation nur, falls Zeit bleibt. Zum
> Selbststudium aber lohnend, weil Strategy in Python besonders unauffällig ist.

### Das Problem

Ein **Algorithmus** soll **zur Laufzeit austauschbar** sein. Klassiker:
verschiedene Rabatt-Berechnungen, Sortier-Kriterien, Komprimierungsverfahren.
Heute „10 % Rabatt", morgen „5 € Rabatt" — ohne den umgebenden Code zu ändern.

> **☕ Aus Java bekannt:** Man definiert ein `interface RabattStrategie { double
> anwenden(double preis); }` und für jede Variante eine eigene Klasse. Der
> Warenkorb hält eine Referenz auf die Strategie und ruft `anwenden(...)`.

### Pythonisch lösen — eine Strategie *ist* einfach eine Funktion

Funktionen sind first-class Werte (Crashkurs, Punkt 10). Eine „Strategie" ist
deshalb keine Klassenhierarchie, sondern schlicht **eine Funktion**:

```python
def kein_rabatt(preis):
    return preis

def fixer_rabatt_5(preis):
    return max(0.0, preis - 5)
```

Und eine **parametrisierbare** Strategie? Eine Funktion, die eine Funktion
**zurückgibt**:

```python
def prozent_rabatt(prozent):              # nimmt den Parameter ...
    def anwenden(preis):                  # ... und baut eine passende Funktion
        return preis * (1 - prozent / 100)
    return anwenden                       # gibt die innere Funktion zurück
```

> **🔑 Begriff – Closure (Funktionsabschluss):** Die innere Funktion `anwenden`
> „merkt" sich den Wert von `prozent` aus ihrer Umgebung — auch nachdem
> `prozent_rabatt` längst zurückgekehrt ist. Diese „Funktion + gemerkte
> Umgebung" nennt man **Closure**. `prozent_rabatt(10)` gibt also eine Funktion
> zurück, die für immer „10 %" eingebaut hat. Das ist Pythons Antwort auf eine
> parametrisierte Strategie-Klasse — in fünf Zeilen statt einer Klasse.

Der Warenkorb hält dann einfach eine Funktion:

```python
class Warenkorb:
    def __init__(self, strategie=kein_rabatt):    # Standard: kein Rabatt
        self.artikel = []
        self.strategie = strategie                # nur eine Funktion, kein Interface

    def hinzufuegen(self, name, preis):
        self.artikel.append((name, preis))

    def gesamtpreis(self):
        roh = sum(preis for _, preis in self.artikel)
        return self.strategie(roh)                # Strategie einfach aufrufen
```

> **🔑 Begriff – `for _, preis in self.artikel`:** Jeder Artikel ist ein Tupel
> `(name, preis)`. Diese Schreibweise **entpackt** das Tupel in zwei Variablen.
> Der Unterstrich `_` ist Konvention für „diesen Wert brauche ich nicht" (hier
> den Namen).

Strategie zur Laufzeit wechseln? Einfach das Attribut neu setzen — kein Setter,
kein Pattern-Code:

```python
korb = Warenkorb(prozent_rabatt(10))      # 10 % Rabatt
korb.strategie = prozent_rabatt(20)       # ab jetzt 20 % — fertig
```

### Wo das in Python begegnet

Strategy ist so verbreitet, dass es kaum noch als „Muster" auffällt — es ist
einfach *eine Funktion übergeben*:

```python
sorted(personen, key=lambda p: p.alter)   # key = Sortier-Strategie
list(map(str.upper, namen))               # Transformations-Strategie
threading.Thread(target=meine_funktion)   # target = was der Thread tun soll
```

Jedes `key=`-Argument, jedes `target=`-Argument ist im Kern ein Strategy-Muster.

### Wann braucht man das Muster *nicht*?

Wenn es nur **eine** mögliche Strategie gibt, ist die Indirektion überflüssig.
Pythonisch: erst beim *zweiten* Bedarf einen Parameter einführen — vorher den
Code direkt hinschreiben. (Das Prinzip heißt **YAGNI**: „You ain't gonna need
it" — bau nichts auf Vorrat.)

---

## 5.6 Context Manager *(Exkurs / Bonus)*

> *Exkurs:* In der Präsentation nur als Bonus. Für die Praxis aber extrem
> nützlich — `with` begegnet dir in echtem Python ständig.

### Das Problem

Manche Operationen brauchen **garantiertes Aufräumen** — egal, ob der Block
erfolgreich war oder ein Fehler auftrat. Datei schließen, Sperre (Lock)
freigeben, Verbindung trennen, Transaktion zurückrollen, Zeit messen, einen
Test-Mock zurücknehmen.

> **🔑 Begriff – Exception:** Ein Laufzeitfehler, der den normalen Ablauf
> unterbricht und „nach oben" weitergereicht wird, bis ihn jemand mit
> `try/except` auffängt. (Java: „Exception" + `try/catch`.) Das Problem: Tritt
> mitten im Block ein Fehler auf, wird der Aufräum-Code am Ende leicht
> übersprungen.

### Pythonisch lösen — das `with`-Statement

Jedes Objekt mit den Dunder-Methoden `__enter__` und `__exit__` darf hinter
`with` stehen. Der Clou: `__exit__` läuft **garantiert, sobald `__enter__`
erfolgreich war** — auch wenn im Block ein Fehler fliegt.

> **⚠️ Stolperstein — „garantiert" mit zwei Ausnahmen:** (1) Scheitert schon
> `__enter__` (Fehler *vor* dem Betreten des Blocks), wird `__exit__` **nicht**
> aufgerufen — es gibt ja nichts aufzuräumen. (2) Bei einem harten
> Prozessabbruch (`os._exit()`, `SIGKILL`, Stromausfall) läuft gar kein Python-
> Code mehr. Für normale Fehler, `return`, `break` und sogar `sys.exit()` gilt
> die Garantie aber.

### Variante 1: Klasse mit `__enter__` / `__exit__`

```python
import time

class Zeitmessung:
    def __init__(self, label):
        self.label = label
        self.dauer_ms = 0.0

    def __enter__(self):                  # läuft beim Betreten des with-Blocks
        self._start = time.perf_counter()
        return self                       # der Rückgabewert landet hinter "as"

    def __exit__(self, exc_typ, exc_wert, exc_tb):   # läuft beim Verlassen
        self.dauer_ms = (time.perf_counter() - self._start) * 1000
        return False                      # Fehler NICHT schlucken (s. u.)
```

Benutzung:

```python
with Zeitmessung("Berechnung") as m:      # __enter__ läuft, m = Rückgabewert
    summe = sum(i*i for i in range(1_000_000))
# hier ist der Block zu Ende -> __exit__ läuft automatisch
print(f"Dauer: {m.dauer_ms:.2f} ms")
```

> **🔑 Begriff – `with ... as m`:** `with` ruft `__enter__` auf; was `__enter__`
> zurückgibt, wird an `m` gebunden. Am Ende des eingerückten Blocks (oder bei
> einem Fehler darin) ruft Python automatisch `__exit__` auf.

**Die drei Argumente von `__exit__`** beschreiben einen eventuellen Fehler im
Block:

- `exc_typ` — die Fehler-Klasse (oder `None`, wenn alles gut ging),
- `exc_wert` — das Fehler-Objekt selbst,
- `exc_tb` — das „Traceback"-Objekt (die Aufrufkette zum Fehler).

> **🔑 Begriff – Rückgabewert von `__exit__`:** Gibt `__exit__` `True` zurück,
> gilt der Fehler als **behandelt** und wird **unterdrückt** (verschluckt).
> `False` (oder gar nichts) reicht ihn weiter — das ist fast immer das
> gewünschte, ehrliche Verhalten.

### Variante 2: `@contextmanager` — der Generator-Weg

Wer keine ganze Klasse schreiben will: `contextlib.contextmanager` macht aus
einer **Generator-Funktion** einen Context Manager.

> **🔑 Begriff – Generator / `yield`:** Eine Funktion mit `yield` ist ein
> **Generator**: Sie läuft bis zum `yield`, **pausiert** dort und gibt einen
> Wert heraus; später läuft sie hinter dem `yield` weiter. Bei `@contextmanager`
> nutzt man genau diese Pause: Alles **vor** `yield` ist das Setup (`__enter__`),
> alles **danach** das Aufräumen (`__exit__`).

```python
from contextlib import contextmanager

@contextmanager
def transaktion(name):
    print(f"[TX] '{name}' beginnt")
    try:
        yield name                        # <-- hier läuft der with-Block des Aufrufers
        print(f"[TX] '{name}' COMMIT")    # nur bei Erfolg
    except Exception as fehler:
        print(f"[TX] '{name}' ROLLBACK wegen: {fehler}")
        raise                             # WICHTIG: Fehler weiterreichen!
```

```python
with transaktion("Buchung 42") as tx:
    ...  # Arbeit; tx ist der per yield gelieferte Wert ("Buchung 42")
```

> **⚠️ Stolperstein – das `raise` am Ende:** Tritt im `with`-Block ein Fehler
> auf, wird dieser an der `yield`-Stelle „in den Generator hineingeworfen" und
> landet im `except`. Schreibt man dort **kein** `raise`, schluckt der Context
> Manager den Fehler **still** — der Aufrufer merkt nichts vom Problem. Mit
> `raise` reicht man ihn weiter, nachdem man aufgeräumt (ROLLBACK) hat. Das ist
> fast immer richtig.

### Wo das in Python begegnet

`with` ist in der Standardbibliothek allgegenwärtig:

```python
with open("a.txt") as f: ...                  # Datei wird garantiert geschlossen
with threading.Lock(): ...                    # Sperre wird garantiert freigegeben
with sqlite3.connect("db") as c: ...          # Transaktion / Verbindung
with tempfile.TemporaryDirectory() as d: ...  # temporäres Verzeichnis aufräumen
with mock.patch("modul.funktion"): ...        # Test-Mock danach zurücknehmen
```

Es gibt sogar eine `async`-Variante (`async with`) für asynchrone Ressourcen
wie Netzwerk- oder Datenbank-Sitzungen.

### Wann braucht man das Muster *nicht*?

Bei reinen Berechnungen ohne externe Ressourcen ist `with` überflüssig. Wer
einen Wert nur kurz braucht, nimmt eine Funktion oder eine lokale Variable —
keinen Context Manager.

> **Kernlehre:** `with` ist Pythons allgemeiner Mechanismus für *„jetzt etwas
> tun, danach garantiert aufräumen"*. Datei-Handling ist nur das bekannteste
> Beispiel — die eigentliche Stärke liegt in der Vielfalt der Anwendungsfälle.

---

## 5.7 Was wir bewusst weggelassen haben

Aus Zeitgründen (20 Minuten Kern-Präsentation) nicht in dieser Modul-Einheit:

- **Iterator** — in Python über `__iter__`, `__next__` und Generatoren mit
  `yield` so tief in die Sprache eingebaut, dass das Muster fast unsichtbar wird.
- **Decorator (das *Muster*, nicht die `@`-Syntax)** — konzeptuell verwandt mit
  Pythons Funktions-Decorator, würde aber eine eigene Stunde brauchen.
- **Command, Template Method, Adapter, Composite, State** — klassische GoF-
  Muster, in Python aber oft unauffällig (Funktion statt Command-Klasse) oder
  durch Duck Typing trivial (Adapter).
- **Metaklassen-Singleton** — existiert, ist aber für die meisten Fälle
  überdimensioniert.

Für Interessierte: Brandon Rhodes' Sammlung *"Python Patterns"* (online) und
Peter Norvigs *"Design Patterns in Dynamic Languages"* sind die
Standard-Referenzen.

---

## 5.8 Zusammenfassung

| Muster | Python-Mechanismus | Pythonische Idiomatik |
|---|---|---|
| Singleton | Modul-System, `__new__`, Decorator | Modul-Attribut, selten `@singleton` |
| Factory | Klassen als first-class Objekte | Dict-Dispatch, `@classmethod` |
| Observer | Callables (Funktion, Lambda, `__call__`) | Liste von Callbacks |
| **MVC** | **Observer + Trennung der Zuständigkeiten** | **Model benachrichtigt Views (REST: Controller/View/Model)** |
| Strategy *(Exkurs)* | Funktionen als first-class Werte | Funktion als Argument, Closure |
| Context Manager *(Exkurs)* | `__enter__`/`__exit__`, `@contextmanager` | `with`-Statement, vielseitig |

**Vier Sätze zum Mitnehmen:**

- *Schön ist besser als hässlich. Einfach ist besser als komplex.*
- *Pythonische Lösungen nutzen die Sprache, nicht das Muster.*
- *Frag dich: welcher Mechanismus trägt das Muster? — dann benutze ihn direkt.*
- *Manche Muster sind in Python keine Muster mehr, sondern Sprache.*

---

## 5.9 Übungsaufgaben

**Aufgabe 1 – Singleton kritisch hinterfragen.** Schreibe eine Klasse
`Konfiguration` einmal als `__new__`-Singleton, einmal als Modul-Singleton.
Diskutiere: Welche Variante ist im Test einfacher durch eine Fake-Version zu
ersetzen (zu „mocken")? Warum?

**Aufgabe 2 – Factory erweitern.** Erweitere die `_TIER_REGISTRY` um einen
`@registriere`-Decorator (siehe 5.2). Lege drei neue Tierarten an, ohne die
Funktion `erzeuge_tier` zu ändern.

**Aufgabe 3 – Observer mit Filter.** Erweitere `Newsletter` um eine Methode
`abonnieren_mit_filter(callback, filter_fn)`, die nur dann an `callback`
weiterleitet, wenn `filter_fn(ausgabe)` wahr ist. Hinweis: `filter_fn` ist
ebenfalls ein Callable — also ein zweites Strategy-Muster auf derselben
Schnittstelle.

**Aufgabe 4 – MVC erweitern.** Füge dem `Schachbrett`-Beispiel eine dritte View
hinzu, die nur eine einzeilige Statuszeile ausgibt (z. B. `"König steht auf
e4"`) — **ohne** Model oder Controller zu ändern. Überlege anschließend: Wie
sähe `Schachsteuerung.ziehe` als Flask/FastAPI-Route-Handler (`POST /zug`) aus,
und welche View würde die HTTP-Antwort liefern? Wo wäre in dieser Web-Variante
*kein* Observer mehr im Spiel?

**Aufgabe 5 – Strategy im Alltag *(Exkurs)*.** Sortiere eine Liste von
`Person`-Objekten (Name, Alter) einmal nach Name, einmal nach Alter, einmal nach
Länge des Namens — ohne `Person` zu ändern. An welcher Stelle steckt das
Strategy-Muster?

**Aufgabe 6 – Context Manager schreiben *(Exkurs)*.** Implementiere eine Klasse
`WechseleVerzeichnis(pfad)`, die im `__enter__` mit `os.chdir` ins
Zielverzeichnis wechselt und im `__exit__` zurück ins vorherige. Schreibe
dieselbe Funktionalität anschließend mit `@contextmanager`.

**Aufgabe 7 – Muster-Ökonomie.** Wähle eines der Muster aus diesem Modul und
beschreibe in drei Sätzen, **wann du es nicht** einsetzen würdest. Welcher Punkt
aus dem *Zen of Python* spricht dafür?

---

## Glossar

Kurz-Erklärungen aller Fachbegriffe, alphabetisch. Ausführlicher stehen sie im
Fließtext beim ersten Auftreten.

- **Abstrakte Klasse** — Klasse, die man nicht direkt instanziieren kann;
  legt nur fest, welche Methoden ihre Untertypen haben müssen (`abc.ABC` +
  `@abstractmethod`). Pythons Gegenstück zu Javas `abstract class`/`interface`.
- **Attribut** — ein an einem Objekt gespeicherter Wert (`self.name`). In Java:
  „Feld".
- **Boilerplate** — wiederkehrender Standard-Code, den die Sprache erzwingt,
  der aber das eigentliche Problem nicht löst.
- **cachen** — ein einmal berechnetes Ergebnis aufheben, um es später sofort
  wiederzugeben.
- **Callable** — alles, was man mit `(...)` aufrufen kann: Funktion, Lambda,
  Methode, Objekt mit `__call__`.
- **Closure** — eine zurückgegebene innere Funktion, die sich Werte aus ihrer
  Entstehungsumgebung „merkt".
- **Decorator** — Funktion, die eine Funktion/Klasse entgegennimmt und etwas
  Aufgewertetes zurückgibt; Schreibweise `@name` über der Definition.
- **Dependency Injection (DI)** — eine benötigte Abhängigkeit als Parameter
  hineinreichen, statt sie sich aus globalem Zustand zu holen.
- **dict (Dictionary)** — Schlüssel-Wert-Tabelle; Pythons `HashMap`.
- **Dispatch** — Weiterleiten an die passende Stelle; *Dict-Dispatch* = per dict
  statt per `if/elif`.
- **Dunder** — „double underscore"; Methoden wie `__init__`, `__call__`,
  Andock-Punkte für den Interpreter.
- **Duck Typing** — „Wenn es quakt wie eine Ente …": Verhalten zählt, nicht der
  deklarierte Typ.
- **dynamische Typisierung** — Typen werden zur Laufzeit geprüft, nicht vom
  Compiler.
- **Exception** — Laufzeitfehler, der den Ablauf unterbricht und weitergereicht
  wird (Java: Exception, `try/catch` → Python `try/except`).
- **first-class** — speicherbar, übergebbar, zurückgebbar wie ein Wert; in
  Python sind Funktionen und Klassen first-class.
- **Generator** — Funktion mit `yield`, die pausieren und Werte nacheinander
  liefern kann.
- **GIL (Global Interpreter Lock)** — sorgt dafür, dass in CPython nur ein
  Thread gleichzeitig Bytecode ausführt; schützt einzelne, nicht zusammengesetzte
  Operationen.
- **globaler Zustand** — von überall erreichbare, veränderbare Daten; bequem,
  aber schwer testbar.
- **Instanz / Objekt** — ein konkret aus einer Klasse erzeugtes Exemplar.
- **`is` vs `==`** — `is` fragt „dasselbe Objekt?", `==` fragt „gleicher Wert?".
- **Klassen- vs Instanz-Attribut** — ein Klassen-Attribut teilen sich alle
  Instanzen (≈ `static`); ein Instanz-Attribut gehört einem Objekt.
- **Lambda** — kurze, namenlose Funktion in einer Zeile.
- **Methode** — Funktion, die zu einer Klasse gehört; erster Parameter `self`.
- **Modul** — eine `.py`-Datei; beim ersten Import einmal ausgeführt und
  gecacht.
- **`__new__` vs `__init__`** — `__new__` erzeugt das Objekt, `__init__` befüllt
  es; `__new__` läuft zuerst.
- **`None`** — Pythons „kein Wert" (Javas `null`).
- **O(1) / O(n)** — Laufzeit-Maße: konstant schnell / linear mit der Größe.
- **Open/Closed-Prinzip** — offen für Erweiterung, geschlossen für Änderung.
- **Polymorphie** — ein Untertyp kann überall stehen, wo der Obertyp erwartet
  wird.
- **push vs pull** — Quelle schiebt Daten aktiv (push) / Interessent holt sie
  bei Bedarf (pull).
- **Registry** — zentrale Tabelle, in die sich Dinge eintragen.
- **REST-Backend** — Server, der über HTTP angesprochen wird und meist JSON
  zurückgibt.
- **`self`** — Pythons `this`; muss explizit als erster Methoden-Parameter
  stehen.
- **Slicing `[1:]`** — Teilstück einer Sequenz ab einem Index.
- **`sys.modules`** — eingebautes dict aller bereits geladenen Module.
- **truthiness (Wahrheitsgehalt)** — `None`, `0`, `""`, `[]` gelten als falsch;
  nicht-leere Werte als wahr.
- **`yield`** — gibt aus einem Generator einen Wert heraus und pausiert dort.

---
---

# Part B — English

> *"Beautiful is better than ugly. Simple is better than complex.
> Readability counts."* — from *The Zen of Python* (Tim Peters)

This is the complete English translation of Part A. Same structure, same depth.

## How to read this booklet

Throughout, you will see the same **four boxes**. They help you place the text:

> **🔑 Term:** A technical word, explained before it is used.

> **☕ Familiar from Java:** A short bridge to what you already know from Java —
> a memory aid, not required knowledge.

> **🐍 The Pythonic view:** How an experienced Python developer would see the
> problem.

> **⚠️ Pitfall:** A typical trap or a common misunderstanding.

There are two runnable companion files:

- `modul5_entwurfsmuster.py` — contains **only definitions** (classes and
  functions), no output. This is the "library".
- `main_modul5.py` — **runs** the definitions and produces output. This is the
  "demo". Start it with `python main_modul5.py`.

Recommendation: read a section here, then look at the matching demo output.
Theory plus visible behavior together stick best.

---

## Python crash course for people who know Java

Before we look at patterns, here is the absolute minimum of Python you need to
read **every** line of code in this booklet. If you know Java, this takes 15
minutes — in most respects Python is *less* strict, not more.

### 1. Indentation instead of curly braces

In Java, `{ }` mark a block. In Python, **indentation** does (usually 4 spaces).
There are no `{ }` for blocks and no semicolons at the end of lines.

```python
def begruesse(name):           # the colon opens the block
    if name:                   # indented = "belongs to the if"
        print("Hallo", name)   # function call
    else:
        print("Hallo Welt")
```

> **☕ Familiar from Java:** Same as `void begruesse(String name) { ... }`, just
> with indentation replacing the braces. Wrong indentation is a **syntax error**
> in Python, not a cosmetic issue.

### 2. Variables and dynamic typing

Variables are declared **without a type** — the type lives in the value, not in
the name. A variable can even hold a value of a different type later.

```python
x = 42          # x is now an int
x = "Text"      # perfectly legal: x is now a str
```

> **🔑 Term – dynamic typing:** The type is checked at **run time**, not by a
> compiler. There is no separate compile step like `javac`; Python runs the
> code directly.

**Optional type hints.** You *may* write types, e.g.
`def f(preis: float) -> float:`. These hints are pure documentation / tooling
help — Python does **not enforce** them at run time. We use them in this booklet
because they make reading easier.

### 3. Functions

```python
def addiere(a, b=0):           # b=0 is a default value
    return a + b               # 'return' as in Java

addiere(2, 3)                  # -> 5
addiere(2)                     # -> 2   (b takes the default 0)
```

Functions can live **anywhere** — at file level, inside other functions, inside
classes. They need not live in a class (unlike Java).

### 4. Classes, `__init__` and `self`

```python
class Hund:
    def __init__(self, name):   # constructor; runs on creation
        self.name = name        # set an instance attribute

    def bellen(self):           # method; 'self' is always the 1st parameter
        return f"{self.name} sagt Wuff"

hund = Hund("Rex")              # NO 'new' needed
print(hund.bellen())            # -> Rex sagt Wuff
```

The key translations:

| Java | Python | Note |
|---|---|---|
| Constructor `Hund(...)` | `def __init__(self, ...)` | "dunder init", see below |
| `this` | `self` | must be the **explicit** 1st parameter |
| `new Hund("Rex")` | `Hund("Rex")` | no `new` |
| `toString()` | `def __str__(self)` | for readable output |
| Field/attribute | `self.name = ...` | created in `__init__` |

> **🔑 Term – instance / object:** An **instance** is a concrete object created
> from a class. `hund` above is an instance of class `Hund`. "Object" and
> "instance" mean the same thing.

> **🔑 Term – attribute:** A value stored on an object (`self.name`). In Java
> you say "field" or "member".

> **🔑 Term – method:** A function that belongs to a class and receives `self`
> as its first parameter.

### 5. No `public`/`private` — only conventions

Python has **no** access modifiers. Instead there is a convention:

- `name` — public, use freely.
- `_name` — "please don't touch from outside" (one underscore = internal). It
  is **not** technically prevented; it is a request among adults.
- `__name` — two underscores: Python slightly "mangles" the name (*name
  mangling*) to avoid accidental clashes in subclasses. Rarely needed.

> **⚠️ Pitfall:** So `_TIER_REGISTRY` with a leading underscore does *not* mean
> "private in the Java sense", but "internal, please don't use directly from
> outside".

### 6. `None`, booleans, truthiness

- `None` is Python's `null` — "no value".
- `True` / `False` are the booleans (capitalized!).
- In `if` checks, `None`, `0`, `""` (empty string) and `[]` (empty list) count
  as **false**; non-empty values as **true**. This is called *truthiness*.

```python
if cls._instanz is None:    # 'is' checks object identity (same object?)
    ...
```

> **🔑 Term – `is` vs `==`:** `==` asks "**same value**?". `is` asks "**same
> object** in memory?". For singletons, `is` is exactly the interesting one: are
> two variables the *same* object?

### 7. Lists, dicts, tuples

```python
liste = [1, 2, 3]                       # list (like ArrayList)
liste.append(4)                         # append
zuordnung = {"hund": 1, "katze": 2}     # dict (like HashMap)
zuordnung["kuh"] = 3                    # set an entry
paar = ("e", 2)                         # tuple: an immutable sequence
```

> **🔑 Term – dict (dictionary):** A key-value table, Python's `HashMap`. Access
> via `dict[key]`. Shows up later in "dict dispatch".

### 8. f-strings (formatted strings)

A string prefixed with `f` allows `{...}` placeholders with real code inside:

```python
name = "Rex"
print(f"Hallo {name}, 2+2 = {2+2}")    # -> Hallo Rex, 2+2 = 4
```

### 9. Modules and `import`

> **🔑 Term – module:** A `.py` file **is** a module. Its name is the filename
> without `.py`. `import x` loads the module `x.py`.

```python
from modul5_entwurfsmuster import konfiguration   # take ONE thing from the module
import modul5_entwurfsmuster as m                  # take the WHOLE module, call it m
```

The module system will play a central role in 5.1 — so remember already: *one
file = one module, executed once on first import.*

### 10. "Everything is an object"

This is the sentence that separates Python from Java the most — and half the
reason this module exists:

> In Python, **functions and classes themselves are objects/values too**. You
> can store a function in a variable, put it in a list, pass it as an argument
> or return it from a function — just like a number.

```python
f = print           # f now points at the function print (no call!)
f("Hallo")          # -> Hallo   (call via the variable)
```

> **🔑 Term – first-class:** When you can do all of that with something (store,
> pass, return), it is called **first-class**. In Python, functions and classes
> are first-class. In Java they are not, to the same degree — there you need
> interfaces, lambdas or reflection to achieve something similar.

With these ten points you can read every line of this booklet. Let's go.

---

## 5.0 What is a design pattern?

A **design pattern** is a proven, **language-independent template** for a
recurring design problem. "Template" means: not a finished class to copy, but an
*idea* for how to solve a particular problem in a structured way.

> **🔑 Term – boilerplate:** Repetitive standard code you write only "because the
> language demands it" — not because it solves the actual problem. Java
> getters/setters are a classic example. A leitmotif of this module: Python
> needs **less** boilerplate for many patterns.

The classic reference is the book *"Design Patterns: Elements of Reusable
Object-Oriented Software"* (1994) by the so-called **Gang of Four** (GoF: Gamma,
Helm, Johnson, Vlissides) with 23 patterns in three categories:

| Category | Question | Examples |
|---|---|---|
| **Creational** | How are objects *created*? | **Singleton, Factory**, Builder, Prototype |
| **Structural** | How do objects *fit together*? | Adapter, Decorator, Composite |
| **Behavioral** | How do objects *communicate*? | **Observer, Strategy**, Command, Iterator |

The patterns in bold are the ones we cover in this module.

These patterns were originally formulated for **statically typed,
class-based** languages like C++ and Java. Python's **dynamic** type system and
its "everything is an object" philosophy change the toolbox: many patterns look
smaller in Python because the language already *ships* what elsewhere has to be
built with pattern code.

> **Peter Norvig's thesis (talk *"Design Patterns in Dynamic Programming"*,
> 1996):** Paraphrased, he observes that 16 of the 23 GoF patterns have a
> *qualitatively simpler — or no separate —* implementation in sufficiently
> dynamic languages (he names Lisp and Dylan), because types and functions are
> first-class there. We see across several patterns what this means. *(Note:
> this is a paraphrase; the exact wording varies by source, so don't quote it
> verbatim.)*

### Python's toolbox – the vocabulary of this module

Four language features recur in almost every pattern. Understand these four and
you're halfway home. We explain them *briefly* here and then *in detail* at the
point where they first do their work.

**1. The module system.** A `.py` file is a module. On the **first** import,
Python executes the file's contents **exactly once** and remembers the result.
As a result, module-level variables exist *exactly once per program run*.
→ powers the **Singleton** pattern (5.1).

**2. First-class functions and classes.** Both are values: storable in
variables, placeable in lists/dicts, passable as arguments, returnable as
results. → powers **Factory** and **Strategy** (5.2, 5.5).

> **🔑 Term – callable:** Anything you can *call* with parentheses `(...)`. That
> includes functions, lambdas (short anonymous functions), methods **and**
> objects with a `__call__` method. "Callable" is Python's common denominator
> instead of an interface. → powers **Observer** (5.3).

**3. Dunder methods.**

> **🔑 Term – dunder:** Short for "**d**ouble **under**score". Methods like
> `__init__`, `__new__`, `__call__`, `__str__`, `__enter__`, `__exit__` are
> named this way because they are framed by two underscores. They are **hook
> points for the Python interpreter**: define `__str__` and `print()` knows how
> to render your object. You rarely call dunders directly — the language calls
> them for you.

→ power **Singleton** (`__new__`), **Observer** (`__call__`) and **Context
Manager** (`__enter__`/`__exit__`).

**4. Decorators.**

> **🔑 Term – decorator:** A function that takes another function **or** class
> and returns an "upgraded" version. Written with `@name` directly above the
> definition. More in 5.1 (variant 3) — there you see exactly what `@` does
> behind the scenes.

With this vocabulary in mind, we go through the patterns one by one — always in
the same shape: *The problem → Solving it the Pythonic way → Variants → Where
you meet it in Python → When you don't need it.*

---

## 5.1 Singleton

### The problem

Sometimes there should be **exactly one** of something — and everyone who uses
it should use the *same* one. Typical examples:

- a **logger** that collects all the program's log lines,
- a **configuration container** with settings (language, debug mode …),
- a **connection pool** to the database.

If every part of the program creates "its own" logger or "its own" config, you
end up with ten half-filled objects instead of one shared one. The **Singleton
pattern** answers: *"How do I ensure there is only one instance and everyone
gets the same one?"*

> **☕ Familiar from Java:** The classic Java recipe is a private constructor
> plus a static `getInstance()` method returning a `private static` variable.
> Python needs none of that in most cases — and that's the interesting part.

### Solving it the Pythonic way — the module system *is* already a singleton

The key is not a piece of pattern code but Python's **import system**. We need
to briefly understand what happens on import, because all the elegance rests on
it.

> **🔑 Term – `sys.modules`:** A built-in dictionary (dict) that Python keeps
> for each program run. Key = module name, value = the loaded module object. It
> is Python's "list of already loaded modules".

When you write `import einmodul` for the **very first time**, three things
happen:

1. Python **executes the entire contents of `einmodul.py` once**. This creates
   all module-level variables (e.g. a line `konfiguration = _Konfiguration()`
   creates exactly *one* object right now).
2. The finished module object is **stored (cached)** in `sys.modules`, roughly
   like `sys.modules["einmodul"] = <module object>`.
3. **Every later** `import einmodul` — from any file in the project — finds the
   module in `sys.modules` and **returns it without executing the file again.**

> **🔑 Term – caching:** Keeping a once-computed result so you can hand it back
> instantly next time instead of recomputing it. Python *caches* modules.

The consequence: a module-level variable exists **exactly once per program run**
and is shared by everyone who imports the module. That is the Pythonic
singleton — the guarantee comes from the language system, not from us.

### Variant 1: The module singleton (the default case)

```python
# file: konfiguration.py
class _Konfiguration:                  # leading _ : "internal, please don't use directly"
    def __init__(self):
        self.sprache = "de"
        self.debug = False

konfiguration = _Konfiguration()       # <-- runs ONCE on first import
```

Now two different files use the same object:

```python
# file a.py
from konfiguration import konfiguration
konfiguration.debug = True             # a changes the shared object

# file b.py
from konfiguration import konfiguration
print(konfiguration.debug)             # -> True : b sees a's change!
```

**What matters here:** `b.py` did not "get a copy". Both files see the *same*
object, because the `konfiguration` module ran only once. No pattern code, no
`getInstance()` method. **The language system does it.**

> **🐍 The Pythonic view:** Before building a singleton class, ask: "Wouldn't a
> variable in a module do?" Usually: yes.

> **⚠️ Pitfall — what exactly is guaranteed?** The module singleton guarantees
> *one shared instance that everyone imports* — **not** that the class couldn't
> be instantiated a second time. There are two ways to a second object:
>
> 1. **By hand:** calling `_Konfiguration()` directly does produce a separate,
>    second instance. Nothing in the language forbids it.
> 2. **The same file ends up in `sys.modules` under two names.** The key fact:
>    `sys.modules` is keyed by the **name** a module was loaded under — not by
>    its file path. The trap, step by step:
>    - If you run `konfiguration.py` **directly** with `python konfiguration.py`,
>      the file runs under the special name `"__main__"`. Python creates
>      `sys.modules["__main__"]` and, doing so, executes the line
>      `konfiguration = _Konfiguration()` → **instance #1**.
>    - If some *other* file now imports the same file with `import konfiguration`,
>      Python looks for the name `"konfiguration"` — which is **not** in
>      `sys.modules` yet (the file is in there as `"__main__"`). So Python does
>      **not** recognize the file, loads it a second time under the name
>      `"konfiguration"`, and runs the creation line again → **instance #2**.
>
>    Result: the same file sits in `sys.modules` twice (as `"__main__"` and as
>    `"konfiguration"`), with two distinct `_Konfiguration` instances. (Rule of
>    thumb: don't both run a file directly **and** import it elsewhere at the
>    same time — keep your entry-point file separate from your imported modules.)
>
> So the "only one" guarantee rests on the **convention** of always importing
> the module attribute and never instantiating the class by hand. If you want
> the *class itself* to refuse a second call, you need a real hook point —
> exactly what the next two variants provide. That's why there are three
> variants at all.

### Variant 2: `__new__` as an explicit hook point

To anchor the singleton character **in the class itself**, you hook into
`__new__`.

> **🔑 Term – `__new__` vs `__init__`:** On `Klasse()`, *two* steps run. First
> `__new__`: it **creates** the object (returns memory). Then `__init__`: it
> **fills** the already-created object with values. So `__new__` is the earlier,
> rarely used hook — and exactly the right place to decide: "new object — or
> return the old one?"

```python
class LoggerJavaStil:
    _instanz = None                          # class attribute: the cache slot

    def __new__(cls):                        # 'cls' is the class itself
        if cls._instanz is None:             # no instance yet?
            cls._instanz = super().__new__(cls)   # then create exactly ONE
            cls._instanz.eintraege = []      # and initialize once
        return cls._instanz                  # otherwise return the existing one

    def log(self, nachricht):
        self.eintraege.append(nachricht)
```

```python
a = LoggerJavaStil()
b = LoggerJavaStil()
a is b              # -> True : the same object (see 'is' in the crash course)
```

Line by line:

- `_instanz = None` lives **at class level** (not in `__init__`).

  > **🔑 Term – class attribute vs instance attribute:** A *class attribute*
  > belongs to the class itself and is shared by all instances (comparable to
  > `static` in Java). An *instance attribute* (`self.eintraege`) belongs to a
  > single instance. `_instanz` is deliberately a class attribute — it should be
  > *one* shared slot.

- In `__new__`, `cls` is the **class** (not the instance — that doesn't exist
  yet). So `cls._instanz` is "the class's shared slot".
- `super().__new__(cls)` creates the actual raw object (done by the base class
  `object`). We do that only if none exists yet.
- `return cls._instanz` **always** returns the same instance.

Three things you should know:

- **`__init__` runs again on *every* call** — even when `__new__` returns the
  old object. Had we set `eintraege` in `__init__`, it would be reset on every
  `LoggerJavaStil()`. That's why we initialize once in `__new__` (protected by
  the `is None` check).
- **It is not thread-safe.**

  > **🔑 Term – GIL & thread safety:** The *Global Interpreter Lock* ensures that
  > in CPython only **one** thread executes Python bytecode at a time. But it
  > only protects **single** operations, not a sequence like "check *whether*
  > `_instanz` is None **and then** create it". Two threads could both see the
  > `is None` as true and each build an object. If you need thread safety: wrap
  > the creation in a `threading.Lock()` — or just use the module singleton,
  > which the import system creates only once anyway.

- **Inheritance gets awkward:** all subclasses would share the same `_instanz`
  (because they inherit the base class's class attribute) unless you're careful
  — a `Subclass()` could surprisingly hand back the base instance.

### Variant 3: The `@singleton` decorator

This variant makes the singleton property **visible at the class header** and is
reusable on *any* class.

First the decorator itself:

```python
def singleton(klasse):
    instanzen = {}                            # cache: class -> its one instance
    def hole_instanz(*args, **kwargs):        # will replace "Klasse(...)" from now on
        if klasse not in instanzen:
            instanzen[klasse] = klasse(*args, **kwargs)   # create once
        return instanzen[klasse]              # otherwise return the cached one
    return hole_instanz
```

> **🔑 Term – `*args, **kwargs`:** Python's notation for "accept any number of
> arguments". `*args` collects the *positional* arguments, `**kwargs` the
> *keyword* arguments. This lets `hole_instanz` work for any class, no matter
> how many arguments its constructor expects.

Applied:

```python
@singleton
class Datenbankverbindung:
    def __init__(self, dsn="lokal://default"):
        self.dsn = dsn
```

> **🔑 Term – decorator syntax `@`:** The line `@singleton` above `class
> Datenbankverbindung` is **just shorthand** for:
> `Datenbankverbindung = singleton(Datenbankverbindung)`.
> That is: Python takes your freshly defined class, sends it through the
> function `singleton`, and the name `Datenbankverbindung` afterwards points at
> **the result** — here, the function `hole_instanz`.

From the caller's perspective, everything stays as usual:

```python
db1 = Datenbankverbindung("postgres://prod")
db2 = Datenbankverbindung("ignored")          # constructor does NOT run again
db1 is db2                                     # -> True
```

On the second call, `hole_instanz` simply returns the cached instance — that's
why the argument `"ignored"` is plainly **ignored**.

> **⚠️ Pitfall — the price of this variant:** Because `Datenbankverbindung` is
> now a **function** (namely `hole_instanz`) and no longer a class, things that
> expect a class break:
> - `isinstance(db1, Datenbankverbindung)` raises `TypeError` (the second
>   argument is no longer a class).
> - Inheritance `class X(Datenbankverbindung): ...` is no longer possible.
> - Introspection / type hints see a function instead of the class.
> - Arguments from the **second** call onward are silently swallowed.
>
> That's why the **module singleton stays the default**; the decorator is only
> worth it when you want to document the singleton property visibly and can live
> with these limitations.

### Where you meet it in Python

The standard library uses module singletons in many places — so you've long
been using them without calling them "singleton":

- `sys.modules` — the cache dict of all modules exists exactly once itself.
- `logging.getLogger("name")` — for the **same name** always returns the
  **same** logger (internally a registry, see 5.2).
- `random.random()` — works on a module-internal `Random` instance created once.

### Which variant when?

| Variant | When to use |
|---|---|
| **Module singleton** | Default case. Almost always the right choice. |
| **`@singleton` decorator** | When the singleton property should be visible at the class header and the limitations above are acceptable. |
| **`__new__` variant** | Academically interesting, rarely needed in practice. |
| **Metaclass singleton** | Exists too (you override the behavior of `type`), but is overkill for almost all cases. |

### When you *don't* need the pattern

Singletons are **controversial** in the Python community, because a singleton is
**global state**: an object visible and mutable everywhere.

> **🔑 Term – global state:** Data not passed via parameters but reachable "from
> anywhere". Convenient, but hard to test (hard to replace in tests) and hard to
> follow (a function's signature doesn't reveal that it uses the global thing).

The experienced alternative is **Dependency Injection** (DI):

> **🔑 Term – Dependency Injection:** "Hand the dependency in." Instead of a
> function fetching the needed object from a global variable itself, it receives
> it as a **parameter**. Benefits: in tests you can pass a fake version (a
> mock), the data flow is visible in the code, and you can have multiple
> instances side by side if needed.

> **Rule of thumb:** Reaching for a singleton "because that's how it's done" is
> a reflex from statically typed languages. In Python it pays to ask each time:
> *"Do I really need this — or does a module attribute suffice, or should I pass
> the object explicitly?"*

---

## 5.2 Factory

### The problem

The caller should get an object of a fitting **subtype** without knowing the
concrete type. Example: *"Give me an animal of type `'hund'`."* The calling site
knows nothing about the class `Hund` — only the umbrella term `Tier` and a
string like `"hund"`.

> **🔑 Term – subtype / supertype (inheritance):** If `Hund` *inherits* from
> `Tier`, then `Hund` is a **subtype** of `Tier`. Every `Hund` *is also a*
> `Tier`. A function expecting a `Tier` therefore accepts any `Hund`, any
> `Katze`, etc. This is called **polymorphism**.

> **🔑 Term – factory:** A place whose job is to **produce objects**. Instead of
> writing `Hund()`, `Katze()`, `Kuh()` all over the code, you call
> `erzeuge_tier("hund")` — the factory decides *which* class.

### Preparation: the abstract base class

So that all animals fulfill the same "contract", we define an abstract base
class:

```python
from abc import ABC, abstractmethod      # "abstract base class" from the stdlib

class Tier(ABC):                          # inherits from ABC -> is abstract
    @abstractmethod
    def laut(self) -> str: ...            # NO implementation, just the contract

    def __str__(self):
        return f"{type(self).__name__}({self.laut()!r})"
```

> **🔑 Term – abstract class / `@abstractmethod`:** An **abstract class** cannot
> be instantiated directly — it only fixes *which* methods its subtypes **must**
> have. `@abstractmethod` marks such a mandatory method. If someone tries to
> instantiate a subclass that does not implement `laut()`, a `TypeError`
> results. This is Python's counterpart to Java's `abstract class` / `interface`.

> **🔑 Term – `...` (Ellipsis):** The three dots are a real Python object, used
> here as an "empty placeholder body" — equivalent to `pass`. They say: "nothing
> goes here on purpose".

> **🔑 Term – `type(self).__name__` and `!r`:** `type(self)` gives the object's
> class, `.__name__` its name as a string (e.g. `"Hund"`). The `!r` in an
> f-string means "use the *repr* form" — for strings that means *with* quotes,
> handy for debugging.

The concrete animals are then simple:

```python
class Hund(Tier):
    def laut(self): return "Wuff"

class Katze(Tier):
    def laut(self): return "Miau"

class Kuh(Tier):
    def laut(self): return "Muh"
```

### Variant 1: explicit, with `if/elif`

The direct way — a factory class with one branch per kind:

```python
class TierFactoryJavaStil:
    @staticmethod
    def erzeuge(art: str) -> Tier:
        if art == "hund":    return Hund()
        elif art == "katze": return Katze()
        elif art == "kuh":   return Kuh()
        else: raise ValueError(f"Unbekannte Tierart: {art!r}")
```

> **🔑 Term – `@staticmethod`:** A method that needs **no** `self`, because it
> doesn't access instance data. You call it directly via the class:
> `TierFactoryJavaStil.erzeuge("hund")`. Comparable to a `static` method in Java.

This is readable — but every new animal kind forces **a new line of code in the
factory**. With 30 kinds you have 30 branches. And whoever wants to add a kind
must edit this (possibly someone else's) factory function.

### Variant 2: dict dispatch (registry) — the Pythonic way

Recall from the crash course: **classes are first-class objects.** So you can
put a class in a dict and look it up later.

> **🔑 Term – dispatch:** "Route to the right place." *Dict dispatch* means: a
> dict maps a key (`"hund"`) directly to the matching target (the class `Hund`)
> — instead of an `if/elif` chain.

> **🔑 Term – registry:** A central table into which things "register". Here: a
> dict mapping names to classes.

```python
_TIER_REGISTRY = {        # key: string -> value: the class ITSELF (not an instance!)
    "hund":  Hund,
    "katze": Katze,
    "kuh":   Kuh,
}

def erzeuge_tier(art: str) -> Tier:
    if art not in _TIER_REGISTRY:
        raise ValueError(f"Unbekannte Tierart: {art!r}")
    return _TIER_REGISTRY[art]()       # look the class up AND call it
```

The decisive line is `_TIER_REGISTRY[art]()`. Read it in two steps:

1. `_TIER_REGISTRY[art]` looks up the dict and yields **the class** (e.g.
   `Hund`) — not yet an object!
2. The parentheses `()` after it **call** that class, which creates an
   **instance** (`Hund()`).

> **⚠️ Pitfall:** The dict holds `Hund`, `Katze` (without parentheses) — i.e.
> the **classes themselves**, not `Hund()`, `Katze()`. With parentheses, the
> dict would already hold *instances*, and all callers would get the same
> object. But we want a *fresh* instance on each call.

**Advantages over `if/elif`:**

- **New kind = one line in the dict.** The function `erzeuge_tier` stays
  unchanged.
- **Lookup is O(1)** (dict access is constant-time) instead of O(n) (the
  if/elif chain is traversed halfway on average). Irrelevant with three entries,
  relevant with fifty.

  > **🔑 Term – O(1) / O(n):** Rough measures for "how does run time grow with
  > size?". *O(1)* = equally fast regardless of how many entries. *O(n)* =
  > linearly slower the more entries there are.

- **Extensible at run time** — the real win (see below).

**The proof of the advantage: registration at run time.**

```python
class Drache(Tier):
    def laut(self): return "Feuer speien"

_TIER_REGISTRY["drache"] = Drache       # exactly ONE line
erzeuge_tier("drache")                  # -> Drache('Feuer speien')
```

`erzeuge_tier` itself was **not touched** for this. With `if/elif` that would
have been impossible without changing the factory's source. This is the
**Open/Closed Principle** in one line:

> **🔑 Term – Open/Closed Principle:** "Open for extension, closed for
> modification." You should be able to *add* new behavior without *changing*
> existing, tested code. The registry fulfills this exemplarily.

**Decorator variant** (for the advanced): each class "registers itself" instead
of you maintaining the registry separately.

```python
TIERE = {}

def registriere(art):                   # takes the name, returns a decorator
    def deco(klasse):
        TIERE[art] = klasse             # register the class
        return klasse                   # return the class unchanged
    return deco

@registriere("hund")
class Hund(Tier):
    def laut(self): return "Wuff"
```

Frameworks like **Django** and **Flask** work essentially this way at their
core: `@app.route("/path")` registers your function in a route table.

### Variant 3: `@classmethod` as an alternative constructor

When the variants are fixed already **at programming time** (you know right now
that there will be "Margherita" and "Salami") and you only want **convenient,
named** constructors, you need no factory class at all — the creation logic
belongs in the class itself.

> **🔑 Term – `@classmethod`:** A method whose first parameter is not `self`
> (the instance) but `cls` (the class). With it, the method can create new
> instances (`cls(...)`). You call it via the class: `Pizza.margherita()`. Java
> bridge: a *static factory method* like `Pizza.margherita()` instead of
> `new Pizza(...)`.

```python
class Pizza:
    def __init__(self, belaege):
        self.belaege = belaege

    @classmethod
    def margherita(cls):
        return cls(["Tomate", "Mozzarella", "Basilikum"])

    @classmethod
    def salami(cls):
        return cls(["Tomate", "Mozzarella", "Salami"])
```

```python
p1 = Pizza.margherita()
p2 = Pizza.salami()
```

`Pizza.margherita()` reads like **domain language** ("a Margherita, please") —
closer to the application problem than a lookup with a string.

### Where you meet it in Python

- `dict.fromkeys(seq)` or `dict.fromkeys(seq, value)` — a classic
  `@classmethod` factory (one method name, optional second parameter).
- `datetime.fromisoformat(s)`, `datetime.fromtimestamp(t)` — alternative
  constructors as `@classmethod` (create a `datetime` from different inputs).
- Plugin systems via `entry_points` in `pyproject.toml` — at heart a registry
  extended at run time.

> **⚠️ Distinction:** `json.loads` / `pickle.loads` are often cited as factory
> examples because they return different types depending on the content. But
> that is only *related*: there is no common supertype from whose subtypes a
> selection is made (they return built-in types like `dict`, `list`, `int`). A
> real factory selects a fitting subtype of a common contract — like
> `erzeuge_tier` selects a `Tier` subtype.

### Which variant when?

> **Rule of thumb:** If the choice comes in via **string/enum at run time** (e.g.
> from a configuration or user input) → **dict dispatch**. If the choice is
> fixed **at programming time** and you only want convenient constructors →
> **`@classmethod`**.

### When you *don't* need the pattern

With only **one** class, or when the caller knows the concrete type anyway, a
factory is superfluous — just call the constructor directly. Pythonic
pragmatism: *don't abstract what doesn't need abstracting.*

---

## 5.3 Observer

### The problem

One object (called **subject** or **publisher**) keeps other objects (called
**observers** or **subscribers**) up to date — **without knowing them in
detail**. Examples: a newsletter dispatch, an event bus, or "when the model
changes, all displays should update" (exactly what we need for MVC in 5.4).

> **🔑 Term – subject & observer:** The **subject** is the source of news. The
> **observers** are those who want to be notified. The subject keeps a list of
> its observers and tells them all when something happens — but does not know
> their concrete classes.

> **☕ Familiar from Java:** In Java you typically define an `interface Listener
> { void onEvent(...); }`, and each observer is a class implementing that
> interface. Python — as we'll see — needs no interface at all.

### Solving it the Pythonic way — a list of callables

Recall from the crash course: a **callable** is anything you can call with
`(...)`. That's exactly the trick: the subject does **not** need to know its
observers via an interface — it's enough that they are *callable*. So it simply
keeps a **list of callables**.

```python
from typing import Callable               # only for the type hint

class Newsletter:
    def __init__(self):
        self._abonnenten = []             # list of callables (observers)

    def abonnieren(self, callback):       # add an observer
        self._abonnenten.append(callback)

    def abbestellen(self, callback):      # remove an observer
        self._abonnenten.remove(callback)

    def veroeffentlichen(self, ausgabe):  # notify everyone
        for callback in self._abonnenten:
            callback(ausgabe)             # just call it — nothing more needed
```

The heart is the loop in `veroeffentlichen`: for each subscriber in the list,
`callback(ausgabe)` is called. `callback` can be **anything callable** — the
newsletter doesn't care *what* exactly.

> **🔑 Term – duck typing:** "If it walks like a duck and quacks like a duck,
> treat it as a duck." Meaning: Python doesn't ask "are you of the right
> type/interface?", it just tries the operation (here: the call). If the object
> has the needed behavior, it works. That's why no common interface is needed.

Now **anything callable** may be an observer:

```python
# 1) a perfectly ordinary function
def auf_konsole(text):
    print(f"[Konsole] {text}")

# 2) a lambda (short, nameless function)
archiv = []
archivieren = lambda text: archiv.append(text)

news = Newsletter()
news.abonnieren(auf_konsole)              # function as observer
news.abonnieren(archivieren)              # lambda as observer
news.abonnieren(print)                    # even the built-in print function!
news.veroeffentlichen("Ausgabe Mai 2026")
```

> **🔑 Term – lambda:** A **short, nameless function** in one line. `lambda
> text: archiv.append(text)` is equivalent to `def f(text): return
> archiv.append(text)`. Handy when you only need a one-liner. Java bridge:
> Python's lambda corresponds to Java's `text -> archiv.add(text)`.

> **⚠️ Pitfall:** Note `news.abonnieren(print)` — here `print` stands **without**
> parentheses. We pass the function *itself* (as a value), not its result.
> `print` without `()` is the object; `print()` *calls* it. This difference is
> the heart of "functions are first-class".

### Observers with memory: `__call__`

Sometimes an observer should **remember** something (have state) — e.g. count
how many issues arrived. For that, you make an ordinary object **callable** by
giving it the dunder method `__call__`:

```python
class ZaehlenderAbonnent:
    def __init__(self, name):
        self.name = name
        self.empfangen = 0

    def __call__(self, ausgabe):          # makes instances callable like functions
        self.empfangen += 1
```

```python
zaehler = ZaehlenderAbonnent("Statistik")
zaehler("Test")        # allowed! calls __call__ -> empfangen is now 1
news.abonnieren(zaehler)   # zaehler is a callable, so a valid observer
```

> **🔑 Term – `__call__`:** Define this dunder method and you can call an
> **instance** like a function: `zaehler("Test")` runs
> `zaehler.__call__("Test")`. That gives you "a function with memory": it
> behaves like a callable but can store state in `self` between calls.

The beautiful part: a function, a lambda and a `__call__` object are three
**completely different** things — yet all three work as observers, solely
because they are callable. That's Observer **and** duck typing together.

### Where you meet it in Python

- **GUI frameworks** like `tkinter` and `PyQt` work at their core with
  **callback lists** for events — the true one-to-many form of Observer.
- Libraries like `blinker` and `pydispatch` package the pattern into ready-made
  "signal" frameworks (one subject, many subscribers).
- `signal.signal(SIGINT, handler)` — **related, but only one** handler per
  signal: a second call *replaces* the first. So it's a callback, not the
  one-to-many notification of the classic Observer — but it shows the same core
  idea: a callable is registered for an event.

### When you *don't* need the pattern

If there's only **one** observer, a direct method call suffices — the
subscription list is then needless ceremony. And if subject and observer live in
the same module, a direct function call is often clearer than a hidden signal
chain. Python's maxim *"explicit is better than implicit"* warns against too
many invisible notification paths.

---

## 5.4 MVC – Model, View, Controller

### The problem

An application quickly mixes three things that really should be separate:

- **State** — the data (which piece is where?),
- **Display** — how the user sees the data (board graphic? JSON?),
- **Control** — what happens on input (move a piece, validate).

If you put everything in one class, you can't swap the display without touching
the logic — and you can't test anything without starting a UI. **MVC**
(Model–View–Controller) separates these three responsibilities:

| Role | Job | In this demo | In a REST backend |
|---|---|---|---|
| **Model** | State + domain logic | Chessboard (piece + square) | Domain objects / database |
| **View** | Display | ASCII board, JSON | HTTP response (e.g. JSON) |
| **Controller** | Process input | `Schachsteuerung.ziehe()` | Route handler (`POST /zug`) |

> **Why this pattern matters here:** In the group projects you build REST
> backends — and those structure cleanly as MVC: the controller is the
> endpoint, the view is the JSON response, the model is your data. Separate the
> three roles and you have a maintainable backend. *(REST and MVC are not the
> same — REST is an architectural **style** for interfaces, MVC an **internal**
> division of the application. They just fit together well.)*

> **🔑 Term – REST backend:** A server program addressed over HTTP (e.g. `POST
> /zug` sends a move, `GET /brett` queries the state) and usually returning
> **JSON**. "Backend" = the server part, as opposed to the "frontend" (what the
> user sees in the browser).

### Two flavors of MVC — important for your project

Before we write code, a distinction that saves a lot of confusion later. MVC
comes in two flavors that differ in **only** one point: *how does the view learn
about a change in the model?*

- **Classic / GUI MVC ("push"):** The model **notifies** its views as soon as it
  changes — via exactly the **Observer pattern from 5.3**. That's the original
  Smalltalk variant and what our demo shows. Useful for a permanently open UI
  that updates "live".
- **Web / REST MVC ("pull"):** An HTTP request triggers everything. The
  controller reads/changes the model and builds the response (view) **itself** —
  then the request is over. There is **no observer**, no notification; the model
  doesn't "call" any views.

> **⚠️ Pitfall:** Do **not** look for an observer in your Flask/FastAPI project —
> there is none. What both variants share is only the **separation of the three
> roles**; that's the transferable core. The Observer-based model→view coupling
> is the specialty of the GUI variant.

> **🔑 Term – push vs pull:** *Push* = the source actively pushes news out (model
> calls views). *Pull* = the interested party fetches the current state when
> needed (client asks via HTTP, gets a response).

### Solving it the Pythonic way (classic variant — with Observer)

MVC needs **no new language feature** in Python. In the classic variant the only
interesting coupling is model → view — and that *is* the Observer pattern from
5.3: the model keeps a list of views (callables) and calls them on change.

**The MODEL** — holds the state and notifies its views:

```python
import json
from typing import Callable

class Schachbrett:                       # MODEL
    SPALTEN = "abcdefgh"                  # class attribute: the columns a-h

    def __init__(self, figur="K", feld="e1"):
        self.figur = figur
        self.feld = feld
        self._views = []                  # the observer list (see 5.3)

    def registriere_view(self, view):
        self._views.append(view)          # a view = a callable

    def _benachrichtigen(self):
        for view in self._views:
            view(self)                    # call each view, passing itself

    def setze_feld(self, feld):
        self.feld = feld
        self._benachrichtigen()           # change state -> update all views
```

Note `view(self)` in `_benachrichtigen`: the model calls each view and passes it
**itself** (`self`, the whole board) so the view can read the current state. The
model does **not** know its views in detail — it only knows they are callable.
So each view is simply a function that reads the model state:

```python
def ascii_view(brett):                   # VIEW A – for the eye
    spalte = Schachbrett.SPALTEN.index(brett.feld[0])   # 'e' -> 4
    reihe = int(brett.feld[1:])                          # '1' -> 1
    for r in range(8, 0, -1):            # rows 8 down to 1
        felder = (brett.figur if (c == spalte and r == reihe) else "."
                  for c in range(8))     # per column: piece or dot
        print(f"  {r} " + " ".join(felder))
    print("    " + " ".join(Schachbrett.SPALTEN))

def json_view(brett):                    # VIEW B – like a REST response
    print(json.dumps({"figur": brett.figur, "feld": brett.feld}))
```

A few building blocks in `ascii_view` explained:

> **🔑 Term – `range(8, 0, -1)`:** Produces the number sequence 8, 7, 6, … 1
> (start 8, stop *before* 0, step −1). We count backwards because a chessboard
> shows row 8 at the top.

> **🔑 Term – slicing `brett.feld[1:]`:** `[1:]` takes the string **from** index
> 1 to the end. From `"e10"` this would give `"10"`. (For our squares it's just
> one digit, but this is robust.) `feld[0]` is the first character.

> **🔑 Term – generator expression `(... for c in range(8))`:** Looks like a
> list but uses round parentheses. It produces the values **one at a time on
> demand**. `" ".join(...)` joins them into a string with spaces. The `x if
> condition else y` inside is Python's **conditional expression** (like Java's
> `condition ? x : y`).

> **🔑 Term – `json.dumps(...)`:** "dump to string" — turns a Python dict into a
> **JSON string**. `{"figur": "K"}` becomes `'{"figur": "K"}'`. This is exactly
> the form a REST backend sends back as a response.

**The CONTROLLER** — takes input, validates it, changes the model; it **never
renders itself**:

```python
class Schachsteuerung:                   # CONTROLLER
    def __init__(self, brett):
        self.brett = brett

    def ziehe(self, feld):
        # validate input BEFORE changing the model:
        if len(feld) < 2 or feld[0] not in Schachbrett.SPALTEN or not feld[1:].isdigit():
            raise ValueError(f"Ungültiges Feld: {feld!r}")
        if not 1 <= int(feld[1:]) <= 8:
            raise ValueError(f"Reihe außerhalb des Bretts: {feld!r}")
        self.brett.setze_feld(feld)      # change model -> views react automatically
```

> **🔑 Term – `str.isdigit()`:** Returns `True` if a string consists only of
> digits. `"7".isdigit()` → `True`, `"x".isdigit()` → `False`. Used here to
> validate the row part.

> **🔑 Term – chained comparisons `1 <= x <= 8`:** Python allows this directly
> (unlike Java, where you'd write `1 <= x && x <= 8`). Reads like math.

### Putting it together

```python
brett = Schachbrett(figur="K", feld="e1")
brett.registriere_view(ascii_view)       # two views observe
brett.registriere_view(json_view)        # the same model

steuerung = Schachsteuerung(brett)
steuerung.ziehe("e2")    # ONE call -> model changes -> BOTH views update
```

The central observation: **one** controller call changes the model, and the
model notifies **all** views by itself. A third view — say a web UI or a log
file — joins via `brett.registriere_view(noch_eine_view)`, **without a single
line changed in the model or controller**. Exactly this extensibility (the
Open/Closed Principle again!) is the payoff of MVC.

### Where you meet it in Python

- **GUI frameworks** (`tkinter`, `PyQt`): here the **classic** variant of our
  demo fits — the model notifies open views via Observer.
- **Flask / FastAPI** (web MVC, *pull*): route handlers (controllers)
  read/write models and return a representation (view, usually JSON). The same
  roles as in the demo, **but without Observer** — the controller builds the
  response per request.
- **Django** calls it **MTV** (Model–Template–View), the same principle in the
  web flavor: Models (ORM) ↔ Views (controller logic) ↔ Templates (display).

### When you *don't* need the pattern

For a small script without a UI and with only one display, the three-way split
is overhead. MVC pays off as soon as there is **more than one view**, the
display should be **swappable**, or the model must stay **testable without a
UI** — i.e. for practically every backend.

> **Core lesson:** MVC is not a new Python language feature but an architectural
> decision — the **separation of state, display and control**. In the classic
> (GUI) variant, **Observer** carries the model→view coupling, as in this demo;
> in the web/REST variant the controller builds the response per request,
> entirely without Observer. What transfers is the separation of the three
> roles, not the concrete coupling tool.

---

## 5.5 Strategy *(Excursus / Bonus)*

> *Excursus:* In the 20-minute presentation, only if time remains. Worthwhile
> for self-study, though, because Strategy is especially inconspicuous in Python.

### The problem

An **algorithm** should be **swappable at run time**. Classics: different
discount calculations, sort criteria, compression methods. Today "10% off",
tomorrow "€5 off" — without changing the surrounding code.

> **☕ Familiar from Java:** You define an `interface DiscountStrategy { double
> apply(double price); }` and a class per variant. The cart holds a reference to
> the strategy and calls `apply(...)`.

### Solving it the Pythonic way — a strategy *is* simply a function

Functions are first-class values (crash course, point 10). So a "strategy" is
not a class hierarchy but plainly **a function**:

```python
def kein_rabatt(preis):
    return preis

def fixer_rabatt_5(preis):
    return max(0.0, preis - 5)
```

And a **parameterizable** strategy? A function that **returns** a function:

```python
def prozent_rabatt(prozent):              # takes the parameter ...
    def anwenden(preis):                  # ... and builds a matching function
        return preis * (1 - prozent / 100)
    return anwenden                       # returns the inner function
```

> **🔑 Term – closure:** The inner function `anwenden` "remembers" the value of
> `prozent` from its surrounding scope — even after `prozent_rabatt` has long
> returned. This "function + remembered environment" is called a **closure**. So
> `prozent_rabatt(10)` returns a function that has "10%" built in forever. That's
> Python's answer to a parameterized strategy class — in five lines instead of a
> class.

The cart then simply holds a function:

```python
class Warenkorb:
    def __init__(self, strategie=kein_rabatt):    # default: no discount
        self.artikel = []
        self.strategie = strategie                # just a function, no interface

    def hinzufuegen(self, name, preis):
        self.artikel.append((name, preis))

    def gesamtpreis(self):
        roh = sum(preis for _, preis in self.artikel)
        return self.strategie(roh)                # just call the strategy
```

> **🔑 Term – `for _, preis in self.artikel`:** Each item is a tuple `(name,
> preis)`. This notation **unpacks** the tuple into two variables. The
> underscore `_` is convention for "I don't need this value" (here the name).

Swap the strategy at run time? Just reassign the attribute — no setter, no
pattern code:

```python
korb = Warenkorb(prozent_rabatt(10))      # 10% off
korb.strategie = prozent_rabatt(20)       # from now on 20% — done
```

### Where you meet it in Python

Strategy is so widespread that it hardly registers as a "pattern" anymore — it's
just *passing a function*:

```python
sorted(personen, key=lambda p: p.alter)   # key = sort strategy
list(map(str.upper, namen))               # transformation strategy
threading.Thread(target=meine_funktion)   # target = what the thread should do
```

Every `key=` argument, every `target=` argument is at heart a Strategy pattern.

### When you *don't* need the pattern

If there is only **one** possible strategy, the indirection is superfluous.
Pythonic: introduce a parameter only on the *second* need — before that, write
the code directly. (The principle is called **YAGNI**: "You ain't gonna need it"
— don't build on spec.)

---

## 5.6 Context Manager *(Excursus / Bonus)*

> *Excursus:* In the presentation only as a bonus. Extremely useful in practice,
> though — you meet `with` constantly in real Python.

### The problem

Some operations need **guaranteed cleanup** — regardless of whether the block
succeeded or an error occurred. Close a file, release a lock, drop a connection,
roll back a transaction, measure time, undo a test mock.

> **🔑 Term – exception:** A run-time error that interrupts the normal flow and
> is passed "upward" until someone catches it with `try/except`. (Java:
> "exception" + `try/catch`.) The problem: if an error occurs mid-block, the
> cleanup code at the end is easily skipped.

### Solving it the Pythonic way — the `with` statement

Any object with the dunder methods `__enter__` and `__exit__` may stand after
`with`. The crux: `__exit__` runs **guaranteed, once `__enter__` has
succeeded** — even if an error flies in the block.

> **⚠️ Pitfall — "guaranteed" with two exceptions:** (1) If `__enter__` itself
> fails (error *before* entering the block), `__exit__` is **not** called —
> there's nothing to clean up. (2) On a hard process kill (`os._exit()`,
> `SIGKILL`, power loss) no Python code runs at all. For ordinary errors,
> `return`, `break` and even `sys.exit()`, the guarantee holds.

### Variant 1: a class with `__enter__` / `__exit__`

```python
import time

class Zeitmessung:
    def __init__(self, label):
        self.label = label
        self.dauer_ms = 0.0

    def __enter__(self):                  # runs when entering the with-block
        self._start = time.perf_counter()
        return self                       # the return value lands after "as"

    def __exit__(self, exc_typ, exc_wert, exc_tb):   # runs when leaving
        self.dauer_ms = (time.perf_counter() - self._start) * 1000
        return False                      # do NOT swallow errors (see below)
```

Usage:

```python
with Zeitmessung("Berechnung") as m:      # __enter__ runs, m = return value
    summe = sum(i*i for i in range(1_000_000))
# block ends here -> __exit__ runs automatically
print(f"Dauer: {m.dauer_ms:.2f} ms")
```

> **🔑 Term – `with ... as m`:** `with` calls `__enter__`; whatever `__enter__`
> returns is bound to `m`. At the end of the indented block (or on an error
> inside it), Python automatically calls `__exit__`.

**The three arguments of `__exit__`** describe a possible error in the block:

- `exc_typ` — the error class (or `None` if all went well),
- `exc_wert` — the error object itself,
- `exc_tb` — the "traceback" object (the call chain to the error).

> **🔑 Term – return value of `__exit__`:** If `__exit__` returns `True`, the
> error is considered **handled** and is **suppressed** (swallowed). `False` (or
> nothing) passes it on — which is almost always the desired, honest behavior.

### Variant 2: `@contextmanager` — the generator way

If you don't want to write a whole class: `contextlib.contextmanager` turns a
**generator function** into a context manager.

> **🔑 Term – generator / `yield`:** A function with `yield` is a **generator**:
> it runs up to the `yield`, **pauses** there and yields a value; later it
> continues after the `yield`. With `@contextmanager` you use exactly that
> pause: everything **before** `yield` is the setup (`__enter__`), everything
> **after** is the cleanup (`__exit__`).

```python
from contextlib import contextmanager

@contextmanager
def transaktion(name):
    print(f"[TX] '{name}' beginnt")
    try:
        yield name                        # <-- the caller's with-block runs here
        print(f"[TX] '{name}' COMMIT")    # only on success
    except Exception as fehler:
        print(f"[TX] '{name}' ROLLBACK wegen: {fehler}")
        raise                             # IMPORTANT: re-raise the error!
```

```python
with transaktion("Buchung 42") as tx:
    ...  # work; tx is the value handed out via yield ("Buchung 42")
```

> **⚠️ Pitfall – the `raise` at the end:** If an error occurs in the `with`
> block, it is "thrown into the generator" at the `yield` point and lands in the
> `except`. If you write **no** `raise` there, the context manager swallows the
> error **silently** — the caller never learns of the problem. With `raise` you
> pass it on after cleaning up (ROLLBACK). That's almost always correct.

### Where you meet it in Python

`with` is ubiquitous in the standard library:

```python
with open("a.txt") as f: ...                  # file is guaranteed closed
with threading.Lock(): ...                    # lock is guaranteed released
with sqlite3.connect("db") as c: ...          # transaction / connection
with tempfile.TemporaryDirectory() as d: ...  # clean up a temp directory
with mock.patch("modul.funktion"): ...        # undo a test mock afterwards
```

There is even an `async` variant (`async with`) for asynchronous resources like
network or database sessions.

### When you *don't* need the pattern

For pure computations without external resources, `with` is superfluous. If you
only need a value briefly, use a function or a local variable — not a context
manager.

> **Core lesson:** `with` is Python's general mechanism for *"do something now,
> clean up afterwards guaranteed"*. File handling is just the best-known example
> — the real strength lies in the variety of use cases.

---

## 5.7 What we deliberately left out

For reasons of time (20-minute core presentation), not in this module unit:

- **Iterator** — in Python so deeply built into the language via `__iter__`,
  `__next__` and generators with `yield` that the pattern becomes almost
  invisible.
- **Decorator (the *pattern*, not the `@` syntax)** — conceptually related to
  Python's function decorator, but would need its own session.
- **Command, Template Method, Adapter, Composite, State** — classic GoF
  patterns, but in Python often inconspicuous (a function instead of a Command
  class) or trivial via duck typing (Adapter).
- **Metaclass singleton** — exists, but is overkill for most cases.

For the interested: Brandon Rhodes' collection *"Python Patterns"* (online) and
Peter Norvig's *"Design Patterns in Dynamic Languages"* are the standard
references.

---

## 5.8 Summary

| Pattern | Python mechanism | Pythonic idiom |
|---|---|---|
| Singleton | Module system, `__new__`, decorator | Module attribute, rarely `@singleton` |
| Factory | Classes as first-class objects | Dict dispatch, `@classmethod` |
| Observer | Callables (function, lambda, `__call__`) | List of callbacks |
| **MVC** | **Observer + separation of responsibilities** | **Model notifies views (REST: Controller/View/Model)** |
| Strategy *(Excursus)* | Functions as first-class values | Function as argument, closure |
| Context Manager *(Excursus)* | `__enter__`/`__exit__`, `@contextmanager` | `with` statement, versatile |

**Four sentences to take away:**

- *Beautiful is better than ugly. Simple is better than complex.*
- *Pythonic solutions use the language, not the pattern.*
- *Ask yourself: which mechanism carries the pattern? — then use it directly.*
- *Some patterns are no longer patterns in Python, but language.*

---

## 5.9 Exercises

**Exercise 1 – Question singletons critically.** Write a class `Konfiguration`
once as a `__new__` singleton and once as a module singleton. Discuss: which
variant is easier to replace with a fake version (to "mock") in a test? Why?

**Exercise 2 – Extend the factory.** Extend `_TIER_REGISTRY` with a
`@registriere` decorator (see 5.2). Add three new animal kinds without changing
the function `erzeuge_tier`.

**Exercise 3 – Observer with a filter.** Extend `Newsletter` with a method
`abonnieren_mit_filter(callback, filter_fn)` that forwards to `callback` only
when `filter_fn(ausgabe)` is true. Hint: `filter_fn` is also a callable — i.e. a
second Strategy pattern on the same interface.

**Exercise 4 – Extend MVC.** Add a third view to the `Schachbrett` example that
prints only a one-line status (e.g. `"König steht auf e4"`) — **without**
changing the model or controller. Then consider: what would `Schachsteuerung.ziehe`
look like as a Flask/FastAPI route handler (`POST /zug`), and which view would
produce the HTTP response? Where, in this web variant, would there be *no*
observer anymore?

**Exercise 5 – Strategy in everyday code *(Excursus)*.** Sort a list of
`Person` objects (name, age) once by name, once by age, once by length of the
name — without changing `Person`. Where is the Strategy pattern hiding?

**Exercise 6 – Write a context manager *(Excursus)*.** Implement a class
`WechseleVerzeichnis(pfad)` that in `__enter__` uses `os.chdir` to change into
the target directory and in `__exit__` changes back to the previous one. Then
write the same functionality with `@contextmanager`.

**Exercise 7 – Pattern economy.** Pick one of the patterns from this module and
describe in three sentences **when you would not** use it. Which point from the
*Zen of Python* supports that?

---

## Glossary

Short explanations of all technical terms, alphabetical. Fuller versions appear
inline at first use.

- **abstract class** — a class you cannot instantiate directly; it only fixes
  which methods its subtypes must have (`abc.ABC` + `@abstractmethod`). Python's
  counterpart to Java's `abstract class`/`interface`.
- **attribute** — a value stored on an object (`self.name`). Java: "field".
- **boilerplate** — repetitive standard code the language forces on you that
  doesn't solve the actual problem.
- **cache** — keep a once-computed result to hand it back instantly later.
- **callable** — anything you can call with `(...)`: function, lambda, method,
  object with `__call__`.
- **class vs instance attribute** — a class attribute is shared by all instances
  (≈ `static`); an instance attribute belongs to one object.
- **closure** — a returned inner function that "remembers" values from its
  creation environment.
- **decorator** — a function that takes a function/class and returns an upgraded
  one; written `@name` above the definition.
- **Dependency Injection (DI)** — pass a needed dependency in as a parameter
  instead of fetching it from global state.
- **dict (dictionary)** — key-value table; Python's `HashMap`.
- **dispatch** — route to the matching target; *dict dispatch* = via a dict
  instead of `if/elif`.
- **duck typing** — "if it quacks like a duck …": behavior counts, not the
  declared type.
- **dunder** — "double underscore"; methods like `__init__`, `__call__`, hook
  points for the interpreter.
- **dynamic typing** — types are checked at run time, not by a compiler.
- **exception** — a run-time error that interrupts the flow and is passed on
  (Java: exception, `try/catch` → Python `try/except`).
- **first-class** — storable, passable, returnable like a value; in Python,
  functions and classes are first-class.
- **generator** — a function with `yield` that can pause and yield values one at
  a time.
- **GIL (Global Interpreter Lock)** — ensures only one thread runs bytecode at a
  time in CPython; protects single, not compound, operations.
- **global state** — data reachable and mutable from anywhere; convenient but
  hard to test.
- **instance / object** — a concrete specimen created from a class.
- **`is` vs `==`** — `is` asks "same object?", `==` asks "same value?".
- **lambda** — a short, nameless one-line function.
- **method** — a function belonging to a class; first parameter `self`.
- **module** — a `.py` file; executed once on first import and cached.
- **`__new__` vs `__init__`** — `__new__` creates the object, `__init__` fills
  it; `__new__` runs first.
- **`None`** — Python's "no value" (Java's `null`).
- **O(1) / O(n)** — run-time measures: constant / linear in the size.
- **Open/Closed Principle** — open for extension, closed for modification.
- **polymorphism** — a subtype can stand wherever the supertype is expected.
- **push vs pull** — source pushes data actively (push) / consumer fetches it on
  demand (pull).
- **registry** — a central table into which things register.
- **REST backend** — a server addressed over HTTP that usually returns JSON.
- **`self`** — Python's `this`; must be the explicit first method parameter.
- **slicing `[1:]`** — a sub-part of a sequence from an index onward.
- **`sys.modules`** — built-in dict of all already-loaded modules.
- **subtype / supertype** — inheritance relationship; the subtype "is a"
  supertype.
- **truthiness** — `None`, `0`, `""`, `[]` count as false; non-empty values as
  true.
- **`yield`** — yields a value from a generator and pauses there.
