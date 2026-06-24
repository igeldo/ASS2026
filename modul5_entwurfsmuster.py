# =============================================================================
# Informatik 4
# Klassenbibliothek – Modul 5: Pythonische Entwurfsmuster
#
# Diese Datei enthält ausschließlich Klassen- und Funktionsdefinitionen –
# keine Ausgaben. Sie wird von main_modul5.py importiert.
#
# Roter Faden: Welcher Python-Mechanismus trägt das jeweilige Pattern?
#   - Modul-System (Singleton)
#   - Dunder-Methoden (__new__, __call__, __enter__/__exit__)
#   - Klassen und Funktionen als first-class Objekte (Factory, Strategy)
#   - Callables (Observer, Strategy)
# =============================================================================

from __future__ import annotations
import json
from abc import ABC, abstractmethod
from contextlib import contextmanager
from typing import Callable


# -----------------------------------------------------------------------------
# 1. SINGLETON – DER KLASSISCHE WEG ÜBER __new__
# -----------------------------------------------------------------------------
# Ziel: Von der Klasse soll es genau eine Instanz geben, egal wie oft jemand
# sie "erzeugt". Python bietet dafür den Einstiegspunkt __new__: diese
# Dunder-Methode erzeugt das Objekt selbst und läuft VOR __init__. Wir cachen
# die einzige Instanz als Klassenattribut.
#
# Der Klassenname trägt "JavaStil" als Etikett, weil dieser explizite Weg
# konzeptionell der ist, den man aus klassischen OO-Sprachen kennt – der
# pythonische Weg folgt im nächsten Abschnitt.

class LoggerJavaStil:
    _instanz: "LoggerJavaStil | None" = None      # Klassenattribut als Cache

    def __new__(cls):
        # __new__ ist der Eingriffspunkt: hier entscheiden wir, ob ein
        # neues Objekt entsteht – oder das bereits existierende zurückkommt.
        if cls._instanz is None:
            cls._instanz = super().__new__(cls)
            cls._instanz.eintraege = []           # einmalige Initialisierung
        return cls._instanz

    def log(self, nachricht: str) -> None:
        self.eintraege.append(nachricht)

    def __str__(self) -> str:
        return f"LoggerJavaStil(Einträge={len(self.eintraege)})"


# -----------------------------------------------------------------------------
# 2. SINGLETON – PYTHONISCH (MODUL + DECORATOR)
# -----------------------------------------------------------------------------
# Beim allerersten Import führt Python den gesamten Modul-Code GENAU EINMAL
# aus (dabei läuft auch die Zeile 'konfiguration = _Konfiguration()') und legt
# das fertige Modulobjekt in sys.modules ab – einem prozessweiten Cache-Dict.
# Jeder spätere "import modul5_entwurfsmuster", egal aus welcher Datei, findet
# das Modul dort und gibt es zurück, OHNE den Code erneut auszuführen. Die
# Instanz entsteht also genau einmal pro Prozess und wird von allen Importeuren
# geteilt – das ist der pythonische Singleton, getragen vom Importsystem statt
# von Pattern-Code.
#
# Zur Ehrlichkeit: erzwungen ist das nicht. Wer _Konfiguration() von Hand
# erneut aufruft, bekommt ein zweites Objekt. Die Garantie "nur einer" beruht
# auf der Konvention, immer das Modul-Attribut zu verwenden – während der
# @singleton-Decorator (Variante B) die Einzigkeit tatsächlich erzwingt.
#
# Variante A: das Modul-Attribut "konfiguration" IST der Singleton.

class _Konfiguration:
    """Wird einmalig instanziiert und als Modul-Attribut 'konfiguration' exportiert."""
    def __init__(self) -> None:
        self.sprache = "de"
        self.debug = False

    def __str__(self) -> str:
        return f"Konfiguration(sprache='{self.sprache}', debug={self.debug})"


konfiguration = _Konfiguration()      # <-- DAS ist der Singleton: das Modul-Attribut


# Variante B: ein wiederverwendbarer @singleton-Decorator. Decorators sind in
# Python first-class – sie nehmen eine Klasse entgegen und geben etwas zurück,
# das sich beim Aufruf wie eine Klasse verhält, aber die Instanz cacht.

def singleton(klasse):
    """Decorator – macht aus jeder dekorierten Klasse einen Singleton."""
    instanzen: dict = {}

    def hole_instanz(*args, **kwargs):
        if klasse not in instanzen:
            instanzen[klasse] = klasse(*args, **kwargs)
        return instanzen[klasse]

    return hole_instanz


@singleton
class Datenbankverbindung:
    def __init__(self, dsn: str = "lokal://default") -> None:
        self.dsn = dsn
        self.verbunden = True

    def __str__(self) -> str:
        return f"Datenbankverbindung(dsn='{self.dsn}', verbunden={self.verbunden})"


# -----------------------------------------------------------------------------
# 3. FACTORY – DER EXPLIZITE WEG MIT if/elif
# -----------------------------------------------------------------------------
# Der Aufrufer soll ein Objekt eines passenden Untertyps bekommen, ohne den
# konkreten Typ zu kennen. Hier zuerst die explizite Variante: eine
# Factory-Klasse mit einer Verzweigung pro Art. Sauber, lesbar, aber jede neue
# Tierart braucht einen neuen if-Zweig.
#
# abc.ABC + @abstractmethod legen den gemeinsamen Vertrag fest, an den sich
# alle Untertypen halten müssen.

class Tier(ABC):
    @abstractmethod
    def laut(self) -> str: ...

    def __str__(self) -> str:
        return f"{type(self).__name__}({self.laut()!r})"


class Hund(Tier):
    def laut(self) -> str: return "Wuff"


class Katze(Tier):
    def laut(self) -> str: return "Miau"


class Kuh(Tier):
    def laut(self) -> str: return "Muh"


class TierFactoryJavaStil:
    @staticmethod
    def erzeuge(art: str) -> Tier:
        if art == "hund":    return Hund()
        elif art == "katze": return Katze()
        elif art == "kuh":   return Kuh()
        else: raise ValueError(f"Unbekannte Tierart: {art!r}")


# -----------------------------------------------------------------------------
# 4. FACTORY – PYTHONISCH (DICT-DISPATCH + CLASSMETHOD)
# -----------------------------------------------------------------------------
# Klassen sind in Python first-class Objekte: sie lassen sich in Listen und
# Dicts speichern, als Argument übergeben, aus Funktionen zurückgeben.
# Damit wird aus der Factory ein Lookup – kein if/elif mehr nötig.
#
# Variante A: Dict-Dispatch / Registry.

_TIER_REGISTRY: dict[str, type[Tier]] = {
    "hund":  Hund,
    "katze": Katze,
    "kuh":   Kuh,
}

def erzeuge_tier(art: str) -> Tier:
    if art not in _TIER_REGISTRY:
        raise ValueError(f"Unbekannte Tierart: {art!r}")
    return _TIER_REGISTRY[art]()           # Klasse aus dem Dict aufrufen


# Variante B: @classmethod als alternativer Konstruktor. Wenn die Varianten
# schon zur Programmierzeit feststehen, lebt die Erzeugungslogik dort, wo sie
# hingehört – in der Klasse selbst, mit aussagekräftigen Namen.

class Pizza:
    def __init__(self, belaege: list[str]) -> None:
        self.belaege = belaege

    @classmethod
    def margherita(cls) -> "Pizza":
        return cls(["Tomate", "Mozzarella", "Basilikum"])

    @classmethod
    def salami(cls) -> "Pizza":
        return cls(["Tomate", "Mozzarella", "Salami"])

    def __str__(self) -> str:
        return f"Pizza({', '.join(self.belaege)})"


# -----------------------------------------------------------------------------
# 5. OBSERVER – CALLABLES STATT LISTENER-INTERFACE
# -----------------------------------------------------------------------------
# Ein Subject (Newsletter) hält Subscriber auf dem Laufenden, ohne ihren
# konkreten Typ zu kennen. In Python ist alles, was man mit (...) aufrufen
# kann, ein Callable: gewöhnliche Funktion, Lambda, gebundene Methode oder
# Objekt mit __call__. Wir brauchen also kein gemeinsames Interface, sondern
# nur eine Liste von Callables.

class Newsletter:
    def __init__(self) -> None:
        self._abonnenten: list[Callable[[str], None]] = []

    def abonnieren(self, callback: Callable[[str], None]) -> None:
        self._abonnenten.append(callback)

    def abbestellen(self, callback: Callable[[str], None]) -> None:
        self._abonnenten.remove(callback)

    def veroeffentlichen(self, ausgabe: str) -> None:
        for callback in self._abonnenten:
            callback(ausgabe)              # einfach aufrufen – mehr braucht es nicht

    def __str__(self) -> str:
        return f"Newsletter(Abonnenten={len(self._abonnenten)})"


# Wenn ein Abonnent Zustand mitschleppen muss: eine normale Klasse mit
# __call__ machen ein Objekt aufrufbar wie eine Funktion – mit Gedächtnis.

class ZaehlenderAbonnent:
    def __init__(self, name: str) -> None:
        self.name = name
        self.empfangen = 0

    def __call__(self, ausgabe: str) -> None:
        self.empfangen += 1

    def __str__(self) -> str:
        return f"ZaehlenderAbonnent({self.name}, empfangen={self.empfangen})"


# -----------------------------------------------------------------------------
# 6. MVC – MODEL / VIEW / CONTROLLER (BAUT AUF OBSERVER AUF)
# -----------------------------------------------------------------------------
# MVC trennt drei Verantwortlichkeiten: das MODEL hält den Zustand und die
# Fachlogik, die VIEW stellt ihn dar, der CONTROLLER nimmt Eingaben entgegen
# und ändert das Model.
#
# Achtung, zwei Spielarten:
#   - Klassisches/GUI-MVC ("push"): das Model BENACHRICHTIGT seine Views bei
#     Änderung – genau das Observer-Pattern aus Abschnitt 5. Das zeigt diese
#     Demo: das Model hält eine Liste von Callables (die Views) und ruft sie
#     auf. Es kennt seine Views nicht im Detail – nur, dass sie aufrufbar sind.
#   - Web-/REST-MVC ("pull"): eine HTTP-Anfrage löst alles aus, der Controller
#     baut die Antwort selbst zusammen – KEIN Observer, keine Benachrichtigung.
#
# Warum hier? In den Gruppenprojekten lässt sich das REST-Backend als MVC
# strukturieren (gleiche drei Rollen, aber ohne Observer):
#   Controller = Route-Handler (z. B. POST /zug),
#   View       = das, was zurückgeht (hier JSON – wie eine HTTP-Antwort),
#   Model      = Domänenzustand (hier ein Brett, im Projekt die Datenbank).
# Übertragbar ist die Trennung der Rollen, nicht die konkrete Model->View-Kopplung.

class Schachbrett:
    """MODEL: hält Figur + Position und benachrichtigt seine Views bei Änderung.

    Die View-Liste IST der Observer-Mechanismus aus Abschnitt 5 – eine Liste
    von Callables, die das Model nur aufruft, ohne ihren Typ zu kennen.
    """

    SPALTEN = "abcdefgh"

    def __init__(self, figur: str = "K", feld: str = "e1") -> None:
        self.figur = figur
        self.feld = feld
        self._views: list[Callable[["Schachbrett"], None]] = []

    def registriere_view(self, view: Callable[["Schachbrett"], None]) -> None:
        self._views.append(view)

    def _benachrichtigen(self) -> None:
        for view in self._views:
            view(self)                       # Observer: einfach aufrufen

    def setze_feld(self, feld: str) -> None:
        self.feld = feld
        self._benachrichtigen()              # Model -> alle Views automatisch


def feld_zu_koordinaten(feld: str) -> tuple[int, int]:
    """'e2' -> (4, 2): Spaltenindex 0–7 und Reihe 1–8."""
    return Schachbrett.SPALTEN.index(feld[0]), int(feld[1:])


def ascii_view(brett: Schachbrett) -> None:
    """VIEW A: rendert den Modellzustand als ASCII-Brett (fürs Auge)."""
    spalte, reihe = feld_zu_koordinaten(brett.feld)
    for r in range(8, 0, -1):
        felder = (brett.figur if (c == spalte and r == reihe) else "."
                  for c in range(8))
        print(f"  {r} " + " ".join(felder))
    print("    " + " ".join(Schachbrett.SPALTEN))


def json_view(brett: Schachbrett) -> None:
    """VIEW B: rendert DENSELBEN Zustand als JSON – wie eine REST-Antwort."""
    print("  " + json.dumps({"figur": brett.figur, "feld": brett.feld}))


class Schachsteuerung:
    """CONTROLLER: nimmt Kommandos entgegen, validiert sie, ändert das Model.

    Im REST-Backend wäre 'ziehe' der Route-Handler hinter z. B. POST /zug.
    """

    def __init__(self, brett: Schachbrett) -> None:
        self.brett = brett

    def ziehe(self, feld: str) -> None:
        if len(feld) < 2 or feld[0] not in Schachbrett.SPALTEN or not feld[1:].isdigit():
            raise ValueError(f"Ungültiges Feld: {feld!r}")
        if not 1 <= int(feld[1:]) <= 8:
            raise ValueError(f"Reihe außerhalb des Bretts: {feld!r}")
        self.brett.setze_feld(feld)          # Model ändern -> Views aktualisieren sich


# -----------------------------------------------------------------------------
# EXKURS 1 (BONUS): STRATEGY – FUNKTIONEN ALS FIRST-CLASS OBJEKTE
# -----------------------------------------------------------------------------
# Funktionen sind in Python ganz normale Werte – man übergibt sie wie
# Strings oder Zahlen. Eine "Strategie" ist deshalb keine Klassenhierarchie,
# sondern schlicht eine Funktion. Mit Closures kann man sie parametrisieren:
# eine Funktion gibt eine Funktion zurück, die den Parameter im Scope behält.

def kein_rabatt(preis: float) -> float:
    return preis

def prozent_rabatt(prozent: float) -> Callable[[float], float]:
    """Closure: gibt eine Funktion zurück, die den Prozentsatz mitschleppt."""
    def anwenden(preis: float) -> float:
        return preis * (1 - prozent / 100)
    return anwenden

def fixer_rabatt(betrag: float) -> Callable[[float], float]:
    def anwenden(preis: float) -> float:
        return max(0.0, preis - betrag)
    return anwenden


class Warenkorb:
    def __init__(self, strategie: Callable[[float], float] = kein_rabatt) -> None:
        self.artikel: list[tuple[str, float]] = []
        self.strategie = strategie         # nur eine Funktion, kein Interface

    def hinzufuegen(self, name: str, preis: float) -> None:
        self.artikel.append((name, preis))

    def gesamtpreis(self) -> float:
        roh = sum(preis for _, preis in self.artikel)
        return self.strategie(roh)         # Strategy einfach aufrufen

    def __str__(self) -> str:
        return f"Warenkorb({len(self.artikel)} Artikel, Summe={self.gesamtpreis():.2f}€)"


# -----------------------------------------------------------------------------
# EXKURS 2 (BONUS): CONTEXT MANAGER – ZUVERLÄSSIGES AUFRÄUMEN MIT with
# -----------------------------------------------------------------------------
# Manche Operationen brauchen garantiertes Aufräumen – egal ob der Block
# erfolgreich war oder eine Exception fliegt. Dateien schließen, Locks
# freigeben, Zeit messen, Transaktionen abschließen, Mocks zurücknehmen.
#
# Pythons Antwort: jedes Objekt mit __enter__ und __exit__ darf hinter "with"
# stehen. __exit__ läuft GARANTIERT, sobald __enter__ erfolgreich war – auch
# bei Exceptions im Block. (Nur zwei Ausnahmen: scheitert schon __enter__,
# gibt es kein __exit__; und ein harter Kill wie os._exit/SIGKILL führt
# keinen Python-Code mehr aus.) Das ist der eigentliche Wert.

class Zeitmessung:
    """Misst die Dauer eines with-Blocks – mit nur zwei Dunder-Methoden."""

    def __init__(self, label: str) -> None:
        self.label = label
        self.dauer_ms: float = 0.0

    def __enter__(self) -> "Zeitmessung":
        import time
        self._start = time.perf_counter()
        return self                         # wird an die 'as'-Variable gebunden

    def __exit__(self, exc_typ, exc_wert, exc_tb) -> bool:
        import time
        self.dauer_ms = (time.perf_counter() - self._start) * 1000
        # return False -> Exceptions werden weitergereicht (Standardverhalten).
        return False


# Variante B: @contextmanager – aus einer Generator-Funktion einen Context
# Manager machen. yield trennt "Setup" von "Teardown" und spart die Klasse.

@contextmanager
def transaktion(name: str):
    """yield trennt 'Setup' (__enter__) von 'Teardown' (__exit__)."""
    print(f"   [TX] '{name}' beginnt")
    try:
        yield name                          # alles vor yield = __enter__
        print(f"   [TX] '{name}' COMMIT")   # alles nach yield = __exit__
    except Exception as fehler:
        print(f"   [TX] '{name}' ROLLBACK wegen: {fehler}")
        raise                               # weiterreichen, damit Aufrufer es sieht
