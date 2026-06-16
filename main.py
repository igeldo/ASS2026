"""
========================================================================
Informatik 4 – Von Java zu OOP in Python
Modul 7: Typisierung & moderne Python-Praxis
------------------------------------------------------------------------
Einstiegspunkt (main.py)

Ausführen:     python main.py
Typen prüfen:  mypy main.py modul7_typisierung.py

In Java entspricht dies der Klasse mit der main()-Methode:
  public class Main {
      public static void main(String[] args) { ... }
  }

In Python ersetzt das if __name__ == "__main__"-Idiom dieses Muster.
========================================================================
"""

# -----------------------------------------------------------------------
# Imports aus dem Modul (wie Java-import com.beispiel.Modul7)
# -----------------------------------------------------------------------
from modul7_typisierung import (
    demo_71_einfache_type_hints,
    demo_72_funktionen,
    demo_73_optional,
    demo_74_union,
    demo_75_komplexe_typen,
    demo_76_callable,
    demo_77_protokolle,
    demo_78_mypy,
    demo_79_dataclasses,
    demo_710_zusammenfassung,
)


# -----------------------------------------------------------------------
# Hilfsfunktion – Abschnittsheader ausgeben
# -----------------------------------------------------------------------
def drucke_header(titel: str) -> None:
    """Gibt einen formatierten Abschnittsheader aus."""
    print()
    print("=" * 60)
    print(f"  {titel}")
    print("=" * 60)


# -----------------------------------------------------------------------
# main() – Einstiegspunkt
#
# Java:
#   public static void main(String[] args) {
#       demo71();
#       demo72();
#       ...
#   }
#
# Python: normale Funktion, aufgerufen über if __name__ == "__main__"
# -----------------------------------------------------------------------
def main() -> None:
    """Führt alle Demo-Abschnitte von Modul 7 der Reihe nach aus."""

    print()
    print("╔══════════════════════════════════════════════════════════╗")
    print("║   Informatik 4 · Von Java zu OOP in Python              ║")
    print("║   Modul 7: Typisierung & moderne Python-Praxis          ║")
    print("╚══════════════════════════════════════════════════════════╝")

    # ------------------------------------------------------------------
    # 7.1 – Einfache Type Hints
    # ------------------------------------------------------------------
    drucke_header("7.1  Einfache Type Hints – Variablen")
    print("  Java:   int alter = 25;  String name = \"Ada\";")
    print("  Python: alter: int = 25  name: str = \"Ada\"")
    print()
    demo_71_einfache_type_hints()

    # ------------------------------------------------------------------
    # 7.2 – Type Hints bei Funktionen
    # ------------------------------------------------------------------
    drucke_header("7.2  Type Hints bei Funktionen")
    print("  Java:   public static String begrüße(String name, int alter)")
    print("  Python: def begrüße(name: str, alter: int) -> str:")
    print()
    demo_72_funktionen()

    # ------------------------------------------------------------------
    # 7.3 – Optional
    # ------------------------------------------------------------------
    drucke_header("7.3  Optional – Pythons Version von null")
    print("  Java:   String s = null;  →  NullPointerException droht!")
    print("  Python: s: Optional[str] = None  →  mypy erzwingt Prüfung")
    print()
    demo_73_optional()

    # ------------------------------------------------------------------
    # 7.4 – Union
    # ------------------------------------------------------------------
    drucke_header("7.4  Union – mehrere erlaubte Typen")
    print("  Java:   kein direktes Äquivalent (nur via Generics/Interface)")
    print("  Python: Union[int, float]  oder  int | float  (ab 3.10)")
    print()
    demo_74_union()

    # ------------------------------------------------------------------
    # 7.5 – Komplexe Typen
    # ------------------------------------------------------------------
    drucke_header("7.5  Komplexe Typen – list, dict, tuple, set")
    print("  Java:   List<String>  Map<String,Integer>  int[]")
    print("  Python: list[str]     dict[str, int]       tuple[int, ...]")
    print()
    demo_75_komplexe_typen()

    # ------------------------------------------------------------------
    # 7.6 – Callable
    # ------------------------------------------------------------------
    drucke_header("7.6  Callable – Funktionen als Typen")
    print("  Java:   Function<Integer, Integer> op = x -> x * 2;")
    print("  Python: operation: Callable[[int], int]")
    print()
    demo_76_callable()

    # ------------------------------------------------------------------
    # 7.7 – Protokolle
    # ------------------------------------------------------------------
    drucke_header("7.7  Protokolle – strukturelle Typen")
    print("  Java:   interface Druckbar { }  +  class X implements Druckbar")
    print("  Python: class Druckbar(Protocol)  –  kein implements nötig!")
    print()
    demo_77_protokolle()

    # ------------------------------------------------------------------
    # 7.8 – mypy
    # ------------------------------------------------------------------
    drucke_header("7.8  mypy – statische Typprüfung")
    print("  Java:   Compiler prüft Typen (Pflicht, automatisch)")
    print("  Python: mypy prüft Typen   (optional, separater Aufruf)")
    print()
    demo_78_mypy()

    # ------------------------------------------------------------------
    # 7.9 – Dataclasses
    # ------------------------------------------------------------------
    drucke_header("7.9  Dataclasses – kompakte typisierte Klassen")
    print("  Java:   public class Punkt { ... Konstruktor, Getter, toString, equals }")
    print("  Python: @dataclass class Punkt:  →  alles automatisch")
    print()
    demo_79_dataclasses()

    # ------------------------------------------------------------------
    # 7.10 – Zusammenfassung
    # ------------------------------------------------------------------
    drucke_header("7.10 Zusammenfassung: Java ↔ Python")
    print()
    demo_710_zusammenfassung()

    # ------------------------------------------------------------------
    # Abschluss
    # ------------------------------------------------------------------
    print()
    print("=" * 60)
    print("  Modul 7 abgeschlossen.")
    print()
    print("  Nächster Schritt – Typen statisch prüfen:")
    print("    pip install mypy")
    print("    mypy main.py modul7_typisierung.py")
    print("=" * 60)
    print()


# -----------------------------------------------------------------------
# Python-Einstiegspunkt
#
# Java hat keine Entsprechung – dort ist main() per Konvention in einer
# Klasse, und der Compiler weiß, wo er starten muss.
#
# In Python signalisiert dieses Idiom:
#   "Führe main() nur aus, wenn diese Datei direkt gestartet wird –
#    nicht wenn sie von einem anderen Modul importiert wird."
# -----------------------------------------------------------------------
if __name__ == "__main__":
    # demo_78_mypy()
    # demo_77_protokolle()
    # demo_75_komplexe_typen()
    # demo_76_callable()
    # demo_79_dataclasses()
      main()
