# =============================================================================
# Informatik 4 – Von Java zu OOP in Python
# Klassenbibliothek – Modul 5: Pythonische Entwurfsmuster
#
# Diese Datei enthält ausschließlich Klassen- und Funktionsdefinitionen –
# keine Ausgaben. Sie wird von main_modul5.py importiert.
#
# Kommentare erklären jeweils den Vergleich zu Java.
# Roter Faden: "Was würde ich in Java tun – und wie denkt Python das?"
# =============================================================================

from __future__ import annotations
from abc import ABC, abstractmethod
from contextlib import contextmanager
from typing import Callable


# -----------------------------------------------------------------------------
# 1. SINGLETON – JAVA-STIL IN PYTHON
# -----------------------------------------------------------------------------
# Java:
#   public class Logger {
#       private static Logger instance;
#       private Logger() {}
#       public static Logger getInstance() {
#           if (instance == null) instance = new Logger();
#           return instance;
#       }
#   }
#
# Python kann das nachbauen – über die Dunder-Methode __new__, die VOR __init__
# läuft und das Objekt selbst erzeugt. Wir cachen die Instanz als Klassenattribut.

class LoggerJavaStil:
    _instanz: "LoggerJavaStil | None" = None      # Klassenattribut (wie static)

    def __new__(cls):
        # __new__ ist Pythons Pendant zu Javas "new" – aber überschreibbar.
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
# Variante A: Das Modul selbst IST ein Singleton.
# Importiere ich "konfiguration" zweimal, bekomme ich dasselbe Objekt zurück.
# Java braucht dafür eine ganze Klasse – in Python reichen Modul-Variablen.
#
# (In der Praxis wären das einfach Variablen auf Modul-Ebene. Hier verpacken
#  wir sie zur Demo in einem kleinen Namespace.)

class _Konfiguration:
    """Wird einmalig instanziiert und als 'konfiguration' exportiert."""
    def __init__(self) -> None:
        self.sprache = "de"
        self.debug = False

    def __str__(self) -> str:
        return f"Konfiguration(sprache='{self.sprache}', debug={self.debug})"


konfiguration = _Konfiguration()      # <-- DAS ist der Singleton: das Modul-Attribut


# Variante B: Singleton-Decorator – wiederverwendbar für beliebige Klassen.
# Java kennt nichts Vergleichbares; man müsste jede Klasse einzeln umbauen.

def singleton(klasse):
    """Decorator – macht aus jeder Klasse einen Singleton."""
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
# 3. FACTORY – JAVA-STIL IN PYTHON
# -----------------------------------------------------------------------------
# Java:
#   interface Tier { String laut(); }
#   class Hund implements Tier { public String laut() { return "Wuff"; } }
#   class TierFactory {
#       public static Tier erzeuge(String art) {
#           if (art.equals("hund")) return new Hund();
#           else if (art.equals("katze")) return new Katze();
#           else throw new IllegalArgumentException(art);
#       }
#   }
#
# Direkte Übersetzung nach Python – mit abc.ABC statt interface.

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
# Variante A: Dict-Dispatch / Registry.
# Klassen sind in Python first-class Objekte – wir legen sie einfach in ein Dict
# und schlagen nach. Kein if/elif, kein switch, kein neuer Code beim Hinzufügen.

_TIER_REGISTRY: dict[str, type[Tier]] = {
    "hund":  Hund,
    "katze": Katze,
    "kuh":   Kuh,
}

def erzeuge_tier(art: str) -> Tier:
    if art not in _TIER_REGISTRY:
        raise ValueError(f"Unbekannte Tierart: {art!r}")
    return _TIER_REGISTRY[art]()           # Klasse aus dem Dict aufrufen


# Variante B: Alternativer Konstruktor als @classmethod.
# Statt einer separaten Factory-Klasse landet die Erzeugungslogik DIREKT in der
# Klasse, die sie betrifft – analog zum Kreis.aus_durchmesser() aus Modul 1.

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
# 5. OBSERVER – JAVA-INTERFACE vs. PYTHON-CALLABLES
# -----------------------------------------------------------------------------
# Java:
#   interface Beobachter { void aktualisiere(String ereignis); }
#   class Newsletter {
#       private List<Beobachter> beobachter = new ArrayList<>();
#       public void anmelden(Beobachter b) { beobachter.add(b); }
#       public void veroeffentliche(String s) {
#           for (Beobachter b : beobachter) b.aktualisiere(s);
#       }
#   }
#
# Java BRAUCHT das Interface, sonst weiß der Newsletter nicht, welche Methode
# er auf den Beobachtern aufrufen soll. Python braucht das nicht: jede Funktion
# ist ein Objekt, das man aufrufen kann (Callable).

class Newsletter:
    def __init__(self) -> None:
        # Liste von Callables – statt einer Liste von "Beobachter"-Objekten.
        self._abonnenten: list[Callable[[str], None]] = []

    def abonnieren(self, callback: Callable[[str], None]) -> None:
        self._abonnenten.append(callback)

    def abbestellen(self, callback: Callable[[str], None]) -> None:
        self._abonnenten.remove(callback)

    def veroeffentlichen(self, ausgabe: str) -> None:
        for callback in self._abonnenten:
            callback(ausgabe)              # einfach aufrufen – kein Interface nötig

    def __str__(self) -> str:
        return f"Newsletter(Abonnenten={len(self._abonnenten)})"


# Wenn ein Beobachter doch Zustand braucht: ganz normale Klasse mit __call__.
# __call__ macht ein Objekt aufrufbar – wie ein Lambda mit Gedächtnis.

class ZaehlenderAbonnent:
    def __init__(self, name: str) -> None:
        self.name = name
        self.empfangen = 0

    def __call__(self, ausgabe: str) -> None:
        self.empfangen += 1

    def __str__(self) -> str:
        return f"ZaehlenderAbonnent({self.name}, empfangen={self.empfangen})"


# -----------------------------------------------------------------------------
# 6. STRATEGY – FUNKTIONEN ALS FIRST-CLASS OBJEKTE
# -----------------------------------------------------------------------------
# Java:
#   interface RabattStrategie { double berechne(double preis); }
#   class ProzentRabatt implements RabattStrategie { ... }
#   class FixerRabatt   implements RabattStrategie { ... }
#   class Warenkorb {
#       private RabattStrategie strategie;
#       public Warenkorb(RabattStrategie s) { this.strategie = s; }
#   }
#
# In Python ist eine Funktion bereits ein Objekt – wir übergeben sie direkt.
# Kein Interface, keine Strategy-Klasse, keine zwei Implementierungs-Klassen.

def kein_rabatt(preis: float) -> float:
    return preis

def prozent_rabatt(prozent: float) -> Callable[[float], float]:
    """Closure: gibt eine Funktion zurück, die den Prozentsatz 'mitschleppt'."""
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
        self.strategie = strategie         # nur eine Funktion – kein Interface

    def hinzufuegen(self, name: str, preis: float) -> None:
        self.artikel.append((name, preis))

    def gesamtpreis(self) -> float:
        roh = sum(preis for _, preis in self.artikel)
        return self.strategie(roh)         # Strategy einfach aufrufen

    def __str__(self) -> str:
        return f"Warenkorb({len(self.artikel)} Artikel, Summe={self.gesamtpreis():.2f}€)"


# -----------------------------------------------------------------------------
# 7. CONTEXT MANAGER – PYTHONS "TRY-WITH-RESOURCES" AUF STEROIDEN
# -----------------------------------------------------------------------------
# Java (seit Java 7):
#   try (BufferedReader r = new BufferedReader(new FileReader("a.txt"))) {
#       ...
#   }
#   funktioniert nur für Klassen, die AutoCloseable implementieren.
#
# Python: jedes Objekt mit __enter__ und __exit__ kann hinter "with" stehen.
# __exit__ läuft IMMER – auch wenn im Block eine Exception fliegt. Damit
# eignet sich der Context Manager für alles, was ein "danach unbedingt"
# braucht: Dateien schließen, Locks freigeben, Zeitmessung, Transaktionen.

class Zeitmessung:
    """Misst die Dauer eines with-Blocks. In Java käme dafür ein try/finally."""

    def __init__(self, label: str) -> None:
        self.label = label
        self.dauer_ms: float = 0.0

    def __enter__(self) -> "Zeitmessung":
        import time
        self._start = time.perf_counter()
        return self                         # wird an 'as'-Variable gebunden

    def __exit__(self, exc_typ, exc_wert, exc_tb) -> bool:
        import time
        self.dauer_ms = (time.perf_counter() - self._start) * 1000
        # return False -> Exceptions werden weitergereicht (Standardverhalten).
        return False


# Variante B: @contextmanager – aus einer Generator-Funktion einen
# Context Manager machen. Spart die Klasse komplett ein.

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
