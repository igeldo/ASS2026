"""
========================================================================
Informatik 4 – Von Java zu OOP in Python
Modul 7: Typisierung & moderne Python-Praxis
========================================================================

Roter Faden: "Was würde ich in Java tun – und wie denkt Python das?"

Dieses Modul exportiert eine Demo-Funktion pro Abschnitt (7.1–7.10).
main.py importiert und ruft diese der Reihe nach auf.

Typen prüfen:  mypy modul7_typisierung.py
========================================================================
"""

# -----------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------
from typing import Optional, Union
from collections.abc import Callable
from typing import Protocol, runtime_checkable
from dataclasses import dataclass


# ========================================================================
# 7.1  EINFACHE TYPE HINTS – Variablen
# ========================================================================
#
# Java (statische Typisierung – Pflicht):
#   int    alter  = 25;
#   String name   = "Ada";
#   double gehalt = 3500.50;
#
# Python MIT Type Hints (optional, aber empfohlen):
#   alter  : int   = 25
#   name   : str   = "Ada"
#   gehalt : float = 3500.50
#
# Wichtig: Python ignoriert Hints zur Laufzeit komplett.
#          Nur mypy (oder andere Tools) werten sie aus.

def demo_71_einfache_type_hints() -> None:
    """7.1 – Einfache Type Hints bei Variablen."""

    alter:  int   = 25
    name:   str   = "Ada"
    gehalt: float = 3500.50
    aktiv:  bool  = True

    print(f"  Name:   {name!r:<12} | Typ: {type(name).__name__}")
    print(f"  Alter:  {alter!r:<12} | Typ: {type(alter).__name__}")
    print(f"  Gehalt: {gehalt!r:<12} | Typ: {type(gehalt).__name__}")
    print(f"  Aktiv:  {aktiv!r:<12} | Typ: {type(aktiv).__name__}")

    # Python erlaubt dies zur Laufzeit – mypy würde warnen:
    alter = "fünfundzwanzig"  # ⚠ mypy: Incompatible types
    print(f"\n  Nach Neuzuweisung: alter = {alter!r} | Typ: {type(alter).__name__}")
    print("  → Python erlaubt es, mypy würde warnen.")


# ========================================================================
# 7.2  TYPE HINTS BEI FUNKTIONEN
# ========================================================================
#
# Java:
#   public static String begrüße(String name, int alter) {
#       return "Hallo " + name + ", du bist " + alter + " Jahre alt.";
#   }
#   public static void druckeLinie(String text) {
#       System.out.println(">> " + text);
#   }
#
# Python: -> nach der Parameterliste = Rückgabetyp
#          None als Rückgabetyp      = void in Java

def begrüße(name: str, alter: int) -> str:
    """Gibt einen Begrüßungsstring zurück."""
    return f"Hallo {name}, du bist {alter} Jahre alt."


def drucke_linie(text: str) -> None:
    """Gibt Text aus. Kein Rückgabewert (= void in Java)."""
    print(f"  >> {text}")


# Mehrere Rückgabewerte als Tupel – in Java nicht direkt möglich:
#   Java-Umweg: eigene Klasse oder int[]
#   public static int[] minMax(int[] zahlen) { ... }
#
# Python direkt:
#   def min_max(zahlen: list[int]) -> tuple[int, int]:

def min_max(zahlen: list[int]) -> tuple[int, int]:
    """Gibt (Minimum, Maximum) zurück – Tupel statt eigener Klasse."""
    return min(zahlen), max(zahlen)


def demo_72_funktionen() -> None:
    """7.2 – Type Hints bei Funktionen und Rückgabetypen."""

    print(f"  {begrüße('Ada', 30)}")
    drucke_linie(begrüße("Alan", 41))

    kleinster, größter = min_max([3, 1, 4, 1, 5, 9, 2, 6])
    print(f"\n  min_max([3,1,4,1,5,9,2,6])")
    print(f"    → kleinster={kleinster}, größter={größter}")
    print("  (Tupel-Rückgabe: in Java nicht direkt möglich)")


# ========================================================================
# 7.3  OPTIONAL – Pythons Version von null / nullable
# ========================================================================
#
# Java (ab Java 8):
#   String spitzname = null;
#   public static String findeNutzer(int id) {
#       if (id == 1) return "Ada";
#       return null;   // NullPointerException droht!
#   }
#
# Python mit Optional[str]:
#   Optional[str] = str oder None
#   mypy erzwingt eine None-Prüfung vor der Verwendung.

def finde_nutzer(nutzer_id: int) -> Optional[str]:
    """Gibt den Nutzernamen zurück oder None, wenn nicht gefunden."""
    datenbank: dict[int, str] = {1: "Ada", 2: "Alan", 3: "Grace"}
    return datenbank.get(nutzer_id)


def demo_73_optional() -> None:
    """7.3 – Optional als Pythons null-Äquivalent."""

    spitzname: Optional[str] = None
    print(f"  spitzname = {spitzname!r}  (Optional[str] = str oder None)")

    print()
    for test_id in [1, 2, 99]:
        nutzer = finde_nutzer(test_id)
        # mypy erwartet hier eine None-Prüfung:
        if nutzer is not None:
            print(f"  ID {test_id}: gefunden → {nutzer.upper()}")
        else:
            print(f"  ID {test_id}: nicht gefunden (None)")


# ========================================================================
# 7.4  UNION – mehrere erlaubte Typen
# ========================================================================
#
# Java kennt das nicht direkt (nur über Interfaces/Generics).
# Python bis 3.9:  Union[int, float]
# Python ab 3.10:  int | float

def verdopple(wert: Union[int, float]) -> Union[int, float]:
    """Verdoppelt eine Zahl – akzeptiert int oder float."""
    return wert * 2


def demo_74_union() -> None:
    """7.4 – Union für mehrere erlaubte Typen."""

    print(f"  verdopple(5)      = {verdopple(5)!r}    (int)")
    print(f"  verdopple(3.14)   = {verdopple(3.14)!r}  (float)")
    print()
    print("  Python 3.10+: int | float  statt  Union[int, float]")
    print("  Java kennt kein direktes Äquivalent (nur via Generics).")


# ========================================================================
# 7.5  KOMPLEXE TYPEN – list, dict, tuple, set
# ========================================================================
#
# Java:
#   List<String>         namen  = new ArrayList<>();
#   Map<String, Integer> punkte = new HashMap<>();
#   int[]                zahlen = {1, 2, 3};
#
# Python ab 3.9 (Kleinbuchstaben, kein Import nötig):
#   namen:  list[str]       = ["Ada", "Alan"]
#   punkte: dict[str, int]  = {"Ada": 95}
#
# Python bis 3.8 (mit typing-Import):
#   from typing import List, Dict
#   namen: List[str] = [...]

def durchschnitt(zahlen: list[float]) -> float:
    """Berechnet den Durchschnitt einer Liste."""
    return sum(zahlen) / len(zahlen)


def demo_75_komplexe_typen() -> None:
    """7.5 – Komplexe Typen: list, dict, set, tuple."""

    namen:       list[str]            = ["Ada", "Alan", "Grace"]
    punkte:      dict[str, int]       = {"Ada": 95, "Alan": 88, "Grace": 92}
    sprachen:    set[str]             = {"Python", "Java", "C++"}
    person_info: tuple[int, str, bool] = (25, "Ada", True)

    print(f"  list[str]              → {namen}")
    print(f"  dict[str, int]         → {punkte}")
    print(f"  set[str]               → {sprachen}")
    print(f"  tuple[int, str, bool]  → {person_info}")
    print(f"\n  durchschnitt([1..5])   = {durchschnitt([1, 2, 3, 4, 5])}")


# ========================================================================
# 7.6  CALLABLE – Funktionen als Typen
# ========================================================================
#
# Java (ab Java 8 mit Functional Interfaces):
#   Function<Integer, Integer> verdoppler = x -> x * 2;
#
# Python:
#   Callable[[int], int] = Funktion, die int nimmt und int zurückgibt

def quadrat(x: int) -> int:
    """x²"""
    return x * x


def verdopple_int(x: int) -> int:
    """x * 2"""
    return x * 2


def wende_an(zahlen: list[int], operation: Callable[[int], int]) -> list[int]:
    """Wendet eine Funktion auf jedes Element an (wie map in Java Streams)."""
    return [operation(z) for z in zahlen]


def demo_76_callable() -> None:
    """7.6 – Callable: Funktionen als Typ-Argument."""

    zahlen: list[int] = [1, 2, 3, 4, 5]
    print(f"  Original:           {zahlen}")
    print(f"  wende_an(quadrat):  {wende_an(zahlen, quadrat)}")
    print(f"  wende_an(verdopp.): {wende_an(zahlen, verdopple_int)}")
    # Lambda wie Java-Lambda:
    print(f"  Lambda x+10:        {wende_an(zahlen, lambda x: x + 10)}")
    print()
    print("  Callable[[int], int] = Java Function<Integer, Integer>")


# ========================================================================
# 7.7  PROTOKOLLE – strukturelle Typen statt Java-Interfaces
# ========================================================================
#
# Java (nominale Typisierung – explizites "implements" nötig):
#   interface Druckbar { String drucken(); }
#   class Dokument implements Druckbar { ... }
#
# Python Protokoll (strukturelle Typisierung):
#   Eine Klasse erfüllt ein Protokoll automatisch,
#   wenn sie die richtigen Methoden besitzt – kein "implements"!
#
# Duck Typing mit Typsicherheit:
#   "Wenn es quakt wie eine Ente, ist es eine Ente."

@runtime_checkable
class Druckbar(Protocol):
    """Protokoll: Jedes Objekt mit drucken() erfüllt es – ohne implements."""
    def drucken(self) -> str:
        ...


class Dokument:
    """Kein 'implements Druckbar' – erfüllt das Protokoll trotzdem."""
    def __init__(self, titel: str) -> None:
        self.titel = titel

    def drucken(self) -> str:
        return f"[Dokument] {self.titel}"


class Rechnung:
    """Auch diese Klasse kennt Druckbar nicht – hat aber die Methode."""
    def __init__(self, nummer: int, betrag: float) -> None:
        self.nummer = nummer
        self.betrag = betrag

    def drucken(self) -> str:
        return f"[Rechnung #{self.nummer}] {self.betrag:.2f} €"


class Foto:
    """Hat KEINE drucken()-Methode – erfüllt das Protokoll NICHT."""
    def __init__(self, datei: str) -> None:
        self.datei = datei


def ausgabe(obj: Druckbar) -> None:
    """Nimmt alles, das Druckbar ist – egal welche Klasse."""
    print(f"    → {obj.drucken()}")


def demo_77_protokolle() -> None:
    """7.7 – Protokolle als strukturelle Typen statt Java-Interfaces."""

    objekte: list[Druckbar] = [
        Dokument("Abschlussarbeit"),
        Rechnung(42, 199.99),
        Dokument("Vorlesungsfolien"),
    ]
    print("  Druckbare Objekte (kein 'implements' nötig!):")
    for obj in objekte:
        ausgabe(obj)

    # @runtime_checkable erlaubt isinstance-Check:
    print()
    print(f"  isinstance(Dokument, Druckbar) → {isinstance(Dokument('x'), Druckbar)}")
    print(f"  isinstance(Rechnung, Druckbar) → {isinstance(Rechnung(1, 0.0), Druckbar)}")
    print(f"  isinstance(Foto,     Druckbar) → {isinstance(Foto('bild.jpg'), Druckbar)}")
    print()
    print("  Java: class X implements Y  →  Python: class X:  # kein implements!")


# ========================================================================
# 7.8  MYPY – statische Typprüfung
# ========================================================================
#
# Java: Compiler prüft Typen beim Kompilieren – automatisch, Pflicht.
#   int x = "hallo";  // Compiler-Fehler
#
# Python: mypy prüft Typen als separates Tool – optional.
#   mypy modul7_typisierung.py

def addiere(a: int, b: int) -> int:
    """Addiert zwei Ganzzahlen."""
    return a + b


def demo_78_mypy() -> None:
    """7.8 – mypy als statischer Typ-Prüfer (Pendant zum Java-Compiler)."""

    ergebnis: int = addiere(3, 5)
    print(f"  addiere(3, 5) = {ergebnis}  ← korrekt")
    print()
    print("  Typfehler, die mypy erkennen würde (hier auskommentiert):")
    print("    ergebnis: str = addiere(3, 5)")
    print("    ⚠ Incompatible types in assignment (str vs int)")
    print()
    print("    addiere('drei', 'fünf')")
    print("    ⚠ Argument 1 has incompatible type 'str'; expected 'int'")
    print()
    print("  mypy-Workflow:")
    print("    pip install mypy")
    print("    mypy modul7_typisierung.py")
    print()
    print("  Java Compiler   ←→   Python mypy")
    print("  Pflicht              Optional")
    print("  beim Kompilieren     als separater Aufruf")


# ========================================================================
# 7.9  DATACLASSES – Typen + weniger Boilerplate
# ========================================================================
#
# Java (viel Boilerplate für eine einfache Datenklasse):
#   public class Punkt {
#       private final double x;
#       private final double y;
#       public Punkt(double x, double y) { this.x = x; this.y = y; }
#       public double getX() { return x; }
#       public double getY() { return y; }
#       public String toString() { return "Punkt(" + x + ", " + y + ")"; }
#       public boolean equals(Object o) { ... }
#   }
#
# Python mit @dataclass:
#   __init__, __repr__ und __eq__ werden automatisch generiert.
#   Entspricht ungefähr einem Java-Record (ab Java 16).

@dataclass
class Punkt:
    """2D-Punkt. @dataclass generiert __init__, __repr__, __eq__ automatisch."""
    x: float
    y: float

    def abstand_zum_ursprung(self) -> float:
        """Berechnet den Abstand zum Ursprung (Pythagoras)."""
        return (self.x ** 2 + self.y ** 2) ** 0.5


@dataclass
class Student:
    """Student – Felder mit Standardwert kommen nach Pflichtfeldern."""
    name:      str
    matrikel:  int
    punkte:    float         = 0.0
    spitzname: Optional[str] = None

    def bestanden(self) -> bool:
        return self.punkte >= 50.0


def demo_79_dataclasses() -> None:
    """7.9 – @dataclass: kompakte typisierte Klassen ohne Boilerplate."""

    p1 = Punkt(3.0, 4.0)
    p2 = Punkt(3.0, 4.0)
    p3 = Punkt(1.0, 1.0)

    print(f"  p1 = {p1}")
    print(f"  p1 == p2 → {p1 == p2}   (automatisches __eq__)")
    print(f"  p1 == p3 → {p1 == p3}  (automatisches __eq__)")
    print(f"  Abstand p1 zum Ursprung: {p1.abstand_zum_ursprung()}")

    s1 = Student("Ada Lovelace", 12345, 87.5, "Ada")
    s2 = Student("Alan Turing",  67890, 42.0)

    print()
    print(f"  {s1}")
    print(f"    bestanden: {s1.bestanden()}")
    print(f"  {s2}")
    print(f"    bestanden: {s2.bestanden()}")
    print()
    print("  @dataclass ≈ Java-Record (ab Java 16)")
    print("  __init__ / __repr__ / __eq__ → automatisch generiert")


# ========================================================================
# 7.10  ZUSAMMENFASSUNG – Java ↔ Python Typisierung
# ========================================================================

def demo_710_zusammenfassung() -> None:
    """7.10 – Zusammenfassende Gegenüberstellung Java ↔ Python."""

    zeilen: list[tuple[str, str]] = [
        ("Java",                         "Python"),
        ("-" * 33,                        "-" * 33),
        ("int x = 5;",                   "x: int = 5"),
        ("String s = null;",             "s: Optional[str] = None"),
        ("List<String> l = ...;",        "l: list[str] = [...]"),
        ("Map<String,Integer> m = ...;", "m: dict[str, int] = {...}"),
        ("String f(int x) { }",          "def f(x: int) -> str:"),
        ("interface Druckbar { }",       "class Druckbar(Protocol):"),
        ("class X implements Y { }",     "class X:  # kein implements!"),
        ("Compiler prüft Typen",         "mypy prüft Typen (optional)"),
        ("Fehler beim Kompilieren",      "Fehler beim mypy-Aufruf"),
    ]

    for java, python in zeilen:
        print(f"  {java:<33} │  {python}")

    print()
    print("  Fazit:")
    print("  Python-Typen sind optional, aber in größeren Projekten")
    print("  sehr empfehlenswert. Type Hints + mypy geben Java-ähnliche")
    print("  Typsicherheit – ohne den Zwang der Sprache.")
