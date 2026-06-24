# Modul 5 – Präsentation: Pythonische Entwurfsmuster

> Stichpunkt-Notizen zum Üben. **Kein Wort-für-Wort-Skript.** Pro Abschnitt:
> *Thesensatz* (was sagt man, wenn man nur einen Satz hat), *Kernaussagen*
> (Python-zentrisch), *Zu zeigen* (Code-Auszug), *Demo-Output*,
> *Verbaler Bezug* (optionale Speaker-Notes, u. a. für die Frage *"Und in
> Java?"*).
>
> **Zeitbudget gesamt: ~20 Minuten (Kern).**
> Richtwert pro Kern-Abschnitt: 2–3 Minuten. Strategy und Context Manager
> sind als **Exkurs/Bonus** angehängt – nur zeigen, falls am Ende Zeit ist.

---

## Zielzeit-Überblick (Kern = 20 Min)

| Abschnitt | Inhalt | Zielzeit |
|---|---|---|
| Einstieg | Pattern-Definition, Norvig-These, Zen of Python | 2 Min |
| 1 | Singleton (`__new__` + Modul/Decorator) | 3 Min |
| 2 | Factory (explizit → Dict-Dispatch/`@classmethod`) | 3 Min |
| 3 | Observer → **MVC** (Observer als Mechanismus, MVC-Demo) | 6 Min |
| Abschluss | Tabelle + Frage | 2 Min |
| Puffer | Übergänge, Atem, kurze Zwischenfragen | ~4 Min |
| **Kern gesamt** | | **~20 Min** |
| Exkurs 1 | Strategy (Bonus) | +2–3 Min |
| Exkurs 2 | Context Manager (Bonus) | +3 Min |

> **Plan für 20 Min:** Einstieg → Singleton → Factory → Observer/MVC →
> Abschluss. **Wenn Zeit bleibt:** Exkurs Strategy, dann Context Manager.
> Beide sind so geschnitten, dass man sie weglassen kann, ohne dass der
> rote Faden reißt.

---

## Setup & Einstieg (2 Min)

**Thesensatz:** *"Pythons Sprachmittel — Module, first-class Klassen und
Funktionen, Dunder-Methoden, Decorators — sind das eigentliche Pattern-
Vokabular. Wir schauen heute, wie sich das in der Praxis zeigt."*

**Aufzubauen:**

- Erinnerung: Gang of Four, 23 Patterns, drei Kategorien (Erzeugung,
  Struktur, Verhalten). Kurz, eine Folie reicht.
- Peter Norvigs These (Vortrag 1996, *"Design Patterns in Dynamic
  Programming"*) **sinngemäß**: 16 der 23 GoF-Patterns sind in hinreichend
  dynamischen Sprachen (Lisp/Dylan) einfacher oder ganz unsichtbar, weil
  Typen und Funktionen dort first-class sind. (Nicht als wörtliches Zitat
  bringen — die genaue Formulierung variiert je nach Quelle.)
- Was wir zeigen werden: **Singleton, Factory, Observer** — und Observer
  führt direkt zu **MVC**, dem Muster, das sich in euren Gruppenprojekten als
  REST-Backend strukturieren lässt. Strategy und Context Manager als Bonus,
  falls Zeit bleibt.
- Roter Faden in jedem Abschnitt: *welcher Python-Mechanismus trägt das
  Pattern* und *wann braucht man es nicht*.
- Zen of Python kurz erwähnen: *"Schön ist besser als hässlich. Einfach
  ist besser als komplex. Lesbarkeit zählt."*

**Übergangssatz zum 1. Pattern:** *"Fangen wir mit dem berühmtesten Pattern
an — und zeigen direkt, wo Pythons Mechanismen es klein machen."*

---

## Abschnitt 1: Singleton (3 Min)

**Thesensatz:** *"Singleton ist eine Frage — und Python hat mit `__new__`
eine direkte Antwort, und mit dem Modul-System eine noch elegantere."*

**Kernaussagen:**

- Singleton = genau eine Instanz, global zugreifbar. Beispiele: Logger,
  Konfiguration, Verbindungspool.
- **Klassischer Weg:** die Dunder-Methode `__new__` — läuft *vor* `__init__`
  und erzeugt das Objekt selbst. Eine Klassen-Cache-Variable plus die
  Eingriffspunkt-Methode reichen aus.
- **Pythonischer Weg:** Beim ersten Import führt Python den Modul-Code
  **genau einmal** aus und legt das Modul in `sys.modules` ab; jeder weitere
  Import gibt das gecachte Modul zurück, ohne den Code erneut auszuführen.
  Die Modul-Variable existiert damit **einmal pro Prozess**.
- **Wichtig beim Vorführen:** nicht nur zeigen, *dass* `konfiguration`
  existiert — sondern dass zwei Zugriffswege **dasselbe Objekt** liefern
  (`A is B -> True`) und eine Änderung an einer Stelle sofort an der anderen
  sichtbar ist. Das ist der Beweis für "existiert nur einmal".
- Ehrlich bleiben — was ist garantiert? Der Modul-Singleton garantiert *eine
  geteilte Instanz, die alle importieren*, **nicht** dass die Klasse
  uninstanziierbar wäre. Zwei Wege zu einem zweiten Objekt: **(a)**
  `_Konfiguration()` von Hand aufrufen; **(b)** dieselbe Datei landet unter
  *zwei Namen* in `sys.modules` — einmal als `__main__` (direkt mit `python
  konfiguration.py` gestartet), einmal als `konfiguration` (von woanders
  importiert). `sys.modules` wird nach dem Namen indiziert, nicht nach dem
  Pfad → Python erkennt die Datei nicht wieder, führt sie zweimal aus, zwei
  Instanzen. Wer die *Klasse* zum Verweigern zwingen will, nimmt `__new__`
  oder den Decorator — deshalb gibt es alle drei Varianten.
- Der `@singleton`-Decorator **erzwingt** die Einzigkeit (zweiter Aufruf,
  andere Args → dasselbe Objekt), hat aber einen Preis: `Datenbankverbindung`
  ist danach eine *Funktion*, keine Klasse — `isinstance(...)` und Vererbung
  brechen, Args ab dem 2. Aufruf werden still ignoriert. Darum bleibt der
  Modul-Singleton der Standardfall.

**Zu zeigen (`modul5_entwurfsmuster.py`, Abschnitt 1+2):**

```python
class LoggerJavaStil:
    _instanz = None
    def __new__(cls):
        if cls._instanz is None:
            cls._instanz = super().__new__(cls)
            cls._instanz.eintraege = []
        return cls._instanz

konfiguration = _Konfiguration()   # <-- das Modul-Attribut IST der Singleton
```

**Demo-Output (zeigen, nicht vorlesen):**

```
logger_a is logger_b -> True          # __new__-Variante: ein Objekt
Dasselbe Objekt?  A is B -> True      # Modul-Singleton: zwei Zugriffe, ein Objekt
... Stelle B sieht jetzt: debug=True  # Änderung an A -> bei B sichtbar
db1 is db2 -> True                    # @singleton erzwingt es
```

**Wichtige Nebenbemerkung:** `__init__` läuft jedes Mal – deshalb im
`__new__` einmalig initialisieren. Threadsicher ist die `__new__`-Variante
nicht ohne `threading.Lock()`; der Modul-Singleton schon.

**Kritische Bemerkung (ein Satz):** Singletons sind umstritten — globaler
Zustand ist schwer testbar. Die Python-Devise: lieber explizit übergeben
(*Dependency Injection*), nicht aus Reflex einsetzen.

**Verbaler Bezug (Speaker-Note, optional):** *"Klassisch-statische Sprachen
lösen das mit privatem Konstruktor plus `getInstance()`. Python braucht den
privaten Konstruktor gar nicht — der Eingriffspunkt ist `__new__`, und das
Modul-System macht es meist ganz überflüssig."*

**Überleitung:** *"Vom 'gibt es genau eines' zum 'gib mir bitte eines vom
Typ X' — das ist Factory."*

---

## Abschnitt 2: Factory (3 Min)

**Thesensatz:** *"Eine Factory mit `if/elif` funktioniert, wächst aber mit
jeder Variante. In Python sind Klassen Objekte — also wird die Factory ein
einzeiliger Lookup."*

**Kernaussagen:**

- Problem: Aufrufer kennt nur den Obertyp, will aber eine passende konkrete
  Instanz. Bestandteile: abstrakte Basisklasse (`abc.ABC` +
  `@abstractmethod`), konkrete Klassen.
- **Explizit:** Factory-Klasse mit `if/elif` — lesbar, aber jede neue
  Tierart erzwingt einen neuen Zweig (bei 30 Arten → 30 Zweige).
- **Pythonisch (Dict-Dispatch):** *"Klassen sind first-class Objekte"* —
  in ein Dict legen, beim Erzeugen nachschlagen und aufrufen:
  `_TIER_REGISTRY[art]()`.
- **Der Beweis für den Vorteil (live zeigen!):** in der Demo registrieren wir
  zur **Laufzeit** eine neue Art (`_TIER_REGISTRY["drache"] = Drache`) und
  `erzeuge_tier("drache")` funktioniert sofort — **ohne dass `erzeuge_tier`
  geändert wird**. Genau das ginge mit `if/elif` nicht (neuer Zweig im
  Quelltext nötig). Open/Closed-Prinzip in einer Zeile.
- **`@classmethod`-Factory:** wenn die Varianten zur Programmierzeit
  feststehen — `Pizza.margherita()` liest sich wie Domänen-Vokabular.

**Zu zeigen (`modul5_entwurfsmuster.py`, Abschnitt 3+4):**

```python
_TIER_REGISTRY = {"hund": Hund, "katze": Katze, "kuh": Kuh}

def erzeuge_tier(art):
    return _TIER_REGISTRY[art]()        # Klasse aus dem Dict aufrufen

_TIER_REGISTRY["drache"] = Drache       # <-- neue Art zur Laufzeit, Factory unverändert
```

**Demo-Output:**

```
erzeuge_tier('hund')   -> Hund('Wuff')
erzeuge_tier('drache') -> Drache('Feuer speien')   # zur Laufzeit dazugekommen
Pizza.margherita()     -> Pizza(Tomate, Mozzarella, Basilikum)
```

**Faustregel laut aussprechen:** *String/Enum zur Laufzeit?* → Dict-Dispatch.
*Auswahl steht zur Programmierzeit fest?* → `@classmethod`.

**Wo das in Python begegnet:** `dict.fromkeys`, `datetime.fromisoformat`,
Plugin-Systeme mit `entry_points`.

**Überleitung:** *"Bisher ging es um *Erzeugung* von Objekten. Jetzt zur
Kommunikation zwischen Objekten — und genau die brauchen wir gleich für MVC."*

---

## Abschnitt 3: Observer → MVC (6 Min)

> **Das ist das Kernstück.** Observer wird kurz als Mechanismus eingeführt
> (~2 Min) und dann sofort auf MVC angewendet (~4 Min). MVC ist der Grund,
> warum dieser Abschnitt wichtig ist: er kommt in den Gruppenprojekten als
> REST-Backend wieder.

### Teil A – Observer (~2 Min)

**Thesensatz:** *"Alles, was aufrufbar ist, ist ein Callable. Eine Liste
von Callables ist alles, was ein Observer-Pattern in Python braucht."*

**Kernaussagen:**

- Begriff **Callable** — alles, was man mit `(...)` aufrufen kann: Funktion,
  Lambda, gebundene Methode, Objekt mit `__call__`.
- Subject (Newsletter) hält eine Liste von Callables — kein gemeinsames
  Interface nötig. Veröffentlichen = die Callables der Reihe nach aufrufen.

**Zu zeigen (`main_modul5.py`, Abschnitt 5):**

```python
news.abonnieren(auf_konsole)
news.abonnieren(lambda s: archiv.append(s))   # Lambda
news.abonnieren(zaehler)                       # Objekt mit __call__
news.veroeffentlichen("Ausgabe Mai 2026")
```

**Kernsatz für den Übergang:** *"Diese eine Idee — ein Objekt hält eine
Liste von Beobachtern und ruft sie bei Änderung auf — ist das Rückgrat von
MVC."*

### Teil B – MVC (~4 Min)

**Thesensatz:** *"MVC trennt drei Verantwortlichkeiten — Zustand,
Darstellung, Steuerung. In der klassischen Variante trägt das eben gezeigte
Observer-Pattern die Kopplung Model → View."*

**Kernaussagen (kurz halten — MVC kennt ihr schon):**

- **Model** = Zustand + Fachlogik. **View** = Darstellung. **Controller** =
  nimmt Eingaben, ändert das Model.
- **In dieser Demo (klassisches/GUI-MVC, "push"):** Das Model hält eine Liste
  von Views (= Observer) und ruft sie bei Änderung auf. Es kennt seine Views
  **nicht im Detail** — nur, dass sie aufrufbar sind. Eine Modelländerung →
  alle Views aktualisieren sich von selbst; eine dritte View kommt ohne eine
  Zeile Model-Änderung dazu.
- **Wichtige Abgrenzung (sonst entsteht ein Trugschluss):** Ein REST-Backend
  ist **Web-MVC ("pull")** — eine HTTP-Anfrage löst alles aus, der Controller
  baut die Antwort **selbst** zusammen, **kein Observer im Spiel**. Nicht
  sagen "REST *ist* MVC" und nicht behaupten, im Flask-Projekt stecke ein
  Observer — tut es nicht. Übertragbar ist die **Trennung der drei Rollen**.
- **Brücke zu den Projekten (laut sagen!):** die Rollen bleiben dieselben —
  - **Controller** = Route-Handler (z. B. `POST /zug`),
  - **View** = die Antwort, die zurückgeht (hier JSON — wie eine HTTP-Antwort),
  - **Model** = Domänenzustand (hier ein Brett, im Projekt die Datenbank).

**Zu zeigen (`modul5_entwurfsmuster.py`/`main_modul5.py`, Abschnitt 6):**

```python
class Schachbrett:                       # MODEL
    def setze_feld(self, feld):
        self.feld = feld
        self._benachrichtigen()          # ruft alle Views auf (= Observer)

brett.registriere_view(ascii_view)       # VIEW fürs Auge
brett.registriere_view(json_view)        # VIEW als REST-Antwort

steuerung = Schachsteuerung(brett)       # CONTROLLER
steuerung.ziehe("e2")                    # ein Aufruf -> beide Views reagieren
```

**Demo-Output (live laufen lassen — das ist der Wow-Moment):**

```
Controller: ziehe nach e2  ->  beide Views reagieren:
  8 . . . . . . . .
  ...
  2 . . . . K . . .
  1 . . . . . . . .
    a b c d e f g h
  {"figur": "K", "feld": "e2"}
```

→ **Ein** Controller-Aufruf, **zwei** Views aktualisieren sich automatisch.
Der Fehlerfall `ziehe("z9")` zeigt: der Controller validiert, bevor er das
Model ändert.

**Was sich pädagogisch anbietet zu sagen:**

- In der *klassischen* Variante ist Observer das Werkzeug, das MVCs
  Model→View-Kopplung trägt — Pattern auf zwei Abstraktionsebenen.
- Die JSON-View ist bewusst gewählt: genau so sieht eine REST-Antwort aus.

**Verbaler Bezug (Speaker-Note, optional):** MVC ist sprachunabhängig — ihr
kennt es aus früheren Kursen. Neu ist hier nur, **wie billig** Python die
(klassische) Model→View-Kopplung macht: eine Liste von Callables, kein
Listener-Interface.

**Wo das in Python begegnet:**
- **GUI** (`tkinter`, `PyQt`): klassisches MVC mit Observer — wie die Demo.
- **Flask / FastAPI / Django** (Request → Controller → Response): Web-MVC,
  gleiche Rollen, **ohne** Observer.

**Überleitung zum Abschluss:** *"Drei Patterns, ein wiederkehrendes Muster:
finde den Python-Mechanismus, der das Pattern trägt — dann benutze ihn
direkt."*

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
| MVC | Observer + Trennung der Zuständigkeiten | Model benachrichtigt Views |

**Wiederkehrende Werkzeuge laut aussprechen:** first-class Funktionen,
first-class Klassen, Modul-System, Dunder-Methoden, Decorators.

**Brücke zu den Projekten:** *"MVC nehmt ihr direkt mit ins Gruppenprojekt —
Controller = Endpoint, View = JSON-Antwort, Model = euer Datenbestand."*

**Schlussgeste / Diskussionseröffnung:** *"An welcher Stelle in eurem
Backend-Entwurf wird MVC euch die meiste Arbeit sparen?"*

**Falls noch Zeit ist:** *"Ich habe noch zwei kurze Exkurse — Strategy und
Context Manager — falls ihr mögt."* → siehe unten.

---

## Exkurs 1 (Bonus): Strategy (2–3 Min)

> Nur zeigen, falls nach dem Abschluss noch Zeit ist.

**Thesensatz:** *"Strategy ist in Python so unsichtbar geworden, dass keiner
es mehr Pattern nennt — wir nennen es einfach 'Funktion übergeben'."*

**Kernaussagen:**

- Eine Strategie ist eine Funktion. Eine parametrisierte Strategie ist eine
  Funktion, die eine Funktion zurückgibt — eine **Closure**.
- `prozent_rabatt(10)` gibt eine *Funktion* zurück, die den Wert `10`
  behält. Strategie zur Laufzeit austauschen = Attribut neu zuweisen.

**Zu zeigen:**

```python
korb = Warenkorb(prozent_rabatt(10))
korb.strategie = prozent_rabatt(20)          # zur Laufzeit wechseln
```

**Wo das begegnet (ein Satz):** `sorted(key=…)`, `threading.Thread(target=…)`,
`map(funktion, …)` — *"jedes `key=`-Argument ist im Kern ein Strategy."*

---

## Exkurs 2 (Bonus): Context Manager (3 Min)

> Nur zeigen, falls noch Zeit ist. Der Fehlerfall (ROLLBACK) ist der
> eindrucksvollste Teil — falls die Zeit ganz knapp ist, nur den mündlich
> beschreiben.

**Thesensatz:** *"`with` ist Pythons allgemeiner Mechanismus für 'jetzt
etwas tun, danach garantiert aufräumen'. Datei-Handling ist nur das
bekannteste Beispiel."*

**Kernaussagen:**

- Jedes Objekt mit `__enter__` und `__exit__` passt hinter `with`.
  `__exit__` läuft **garantiert, sobald `__enter__` erfolgreich war** — auch
  bei Exceptions. (Ehrlichkeits-Fußnote, falls gefragt: scheitert schon
  `__enter__`, gibt es kein `__exit__`; ein harter Kill wie `SIGKILL`/`os._exit`
  führt ohnehin keinen Code mehr aus.)
- `@contextmanager` macht aus einer Generator-Funktion mit einem `yield`
  einen Context Manager: alles vor `yield` = Setup, alles danach = Teardown.

**Zu zeigen – beide Varianten kurz:**

```python
with Zeitmessung("Berechnung") as m:
    ...
print(f"Dauer: {m.dauer_ms:.2f} ms")

@contextmanager
def transaktion(name):
    try:
        yield name
        print("[TX] COMMIT")
    except Exception:
        print("[TX] ROLLBACK")
        raise
```

**Demo-Output (der Fehlerfall ist eindrucksvoll):**

```
[TX] 'Buchung 43' beginnt
[TX] 'Buchung 43' ROLLBACK wegen: Konto gesperrt
Aufrufer fängt: Konto gesperrt
```

→ `__exit__` läuft **garantiert**, der Aufrufer kann die Exception trotzdem
behandeln.

**Wo das begegnet:** `open()`, `threading.Lock()`, `mock.patch()`,
`tempfile.TemporaryDirectory()`.

---

## Wahrscheinliche Fragen aus dem Publikum

| Frage | Kurze Antwort |
|---|---|
| *Ist das jetzt Observer oder MVC?* | Observer ist der Mechanismus (Liste von Callables). MVC ist das größere Muster; in der *klassischen* Variante nutzt es Observer für die Model→View-Kopplung. |
| *Wie wird MVC zum REST-Backend?* | Gleiche drei Rollen: Controller = Route-Handler, View = JSON-Antwort, Model = Domänenzustand/DB. **Aber:** Web-MVC ist pull-basiert — der Controller baut die Antwort pro Request selbst, **kein Observer**. Nur die Rollentrennung überträgt sich, nicht die Benachrichtigung. |
| *Wo steckt der Observer in meinem Flask-Projekt?* | Nirgends — und das ist korrekt. Observer ist die GUI-/Live-Variante. REST ist Request→Response ohne Benachrichtigung. |
| *Sind Singletons threadsicher?* | Modul-Singleton ja (Import serialisiert); `__new__`-Variante braucht `threading.Lock()`. |
| *Wann Dict-Dispatch, wann `@classmethod`?* | Laufzeit-Auswahl per String → Dict. Programmierzeit-Auswahl → `@classmethod`. |
| *Warum kennt Python kein Listener-Interface?* | Braucht es nicht — Duck Typing: alles Aufrufbare ist ein gültiger Observer. |
| *Und in Java?* | Die meisten dieser Patterns brauchen dort Boilerplate — Interfaces, statische Methoden, Listener-Klassen. Genau den spart Python ein. |

---

## Persönliche Hinweise zum Üben

- **Vor dem Vortrag mindestens einmal `python main_modul5.py` laufen
  lassen** und den Output lesen — besonders den MVC-Abschnitt, der ist der
  Höhepunkt.
- *"first-class"* und *"Mechanismus, der das Pattern trägt"* sind die
  zentralen Begriffe — absichtlich oft verwenden.
- Beim MVC-Teil **nicht** in eine MVC-Grundsatzvorlesung abdriften — das
  kennt das Publikum. Fokus: *wie billig Python die Kopplung macht* und
  *die Brücke zum REST-Projekt*.
- 20-Minuten-Disziplin: Strategy/Context Manager sind Bonus. Lieber den
  Kern ruhig zu Ende bringen als die Exkurse hetzen.
- Bei einer Frage, deren Antwort man nicht weiß: ehrlich *"Das schaue ich
  nach"* — nicht raten.
