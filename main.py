# =============================================================================
# Informatik 4 – Von Java zu OOP in Python
# Ausgewählte Softwaresysteme Programmierung IV (ASS-PR4)
# FH Dortmund | Prof. Dr. Burkhard Igel
#
# main.py – Demonstrations-Einstiegspunkt für Modul 8
#
# HINWEIS: Diese Datei ist der Einstiegspunkt der Anwendung.
# In Python entspricht das dem `public static void main(String[] args)` in
# Java – aber ohne Klasse, ohne Typ-Annotation der Signatur.
#
# Ausführen:
#   python main.py
# =============================================================================

import logging
import unittest

# Importiere die Lehrmodule
from informatik4_modul8_werkzeuge import Bankkonto, berechne_zinseszins


# =============================================================================
# ABSCHNITT 1: Unit Tests mit unittest
# =============================================================================
#
# Lernziel: Testgetriebene Entwicklung (TDD) in Python.
#
# ┌─────────────────────────────────────────────────────────────────────────┐
# │  Java (JUnit 5)                │  Python (unittest)                    │
# ├─────────────────────────────────────────────────────────────────────────┤
# │  @Test                         │  def test_...(self):                  │
# │  @BeforeEach                   │  def setUp(self):                     │
# │  @AfterEach                    │  def tearDown(self):                  │
# │  assertEquals(expected, actual)│  self.assertEqual(expected, actual)   │
# │  assertThrows(Type, lambda)    │  with self.assertRaises(Type):        │
# └─────────────────────────────────────────────────────────────────────────┘
#
# Industriestandard: pytest (→ tests/test_modul8.py)
# Hier zeigen wir das eingebaute unittest, das konzeptuell JUnit entspricht.

class TestBankkonto(unittest.TestCase):
    """Testklasse für die Bankkonto-Implementierung."""

    def setUp(self):
        """
        Wird VOR jedem einzelnen Test ausgeführt.
        Java-Äquivalent: @BeforeEach
        """
        self.konto = Bankkonto("Ada Lovelace", 100.0)

    # -------------------------------------------------------------------------
    # Testmethoden müssen mit test_ beginnen – das ist Convention-over-Config.
    # Java: @Test Annotation. Python: Namenskonvention (kein Framework-Zwang).
    # -------------------------------------------------------------------------

    def test_einzahlung_erhoeht_kontostand(self):
        self.konto.einzahlen(50.0)
        self.assertEqual(150.0, self.konto.kontostand)

    def test_einzahlung_negativer_betrag_wirft_fehler(self):
        with self.assertRaises(ValueError):
            self.konto.einzahlen(-10.0)

    def test_abhebung_reduziert_kontostand(self):
        self.konto.abheben(40.0)
        self.assertEqual(60.0, self.konto.kontostand)

    def test_abhebung_bei_ueberziehung_wirft_fehler(self):
        # Java: assertThrows(ValueError.class, () -> konto.abheben(200));
        # Python: Context Manager `with` – lesbarer und idiomatischer
        with self.assertRaises(ValueError):
            self.konto.abheben(200.0)

    def test_str_repraesentation(self):
        # __str__ entspricht Java toString()
        self.assertIn("Ada Lovelace", str(self.konto))
        self.assertIn("100.00€", str(self.konto))


class TestZinsrechner(unittest.TestCase):
    """Testklasse für die Zinseszins-Berechnung."""

    def test_standard_berechnung(self):
        ergebnis = berechne_zinseszins(1000.0, 5.0, 10)
        self.assertEqual(1628.89, ergebnis)

    def test_nulljahre_gibt_startkapital_zurueck(self):
        ergebnis = berechne_zinseszins(500.0, 3.5, 0)
        self.assertEqual(500.0, ergebnis)

    def test_negatives_kapital_wirft_fehler(self):
        with self.assertRaises(ValueError):
            berechne_zinseszins(-100.0, 5.0, 5)

    def test_negative_laufzeit_wirft_fehler(self):
        with self.assertRaises(ValueError):
            berechne_zinseszins(1000.0, 5.0, -1)


# =============================================================================
# ABSCHNITT 2: Logging-Konfiguration
# =============================================================================

def konfiguriere_logging() -> None:
    """
    Konfiguriert das globale Logging-Format für die gesamte Applikation.

    In Python wird Logging EINMALIG zentral konfiguriert – typischerweise
    in main.py oder der Applikations-Eintrittsdatei.

    Java-Äquivalent: logback.xml oder log4j2.xml Konfigurationsdatei.
    """
    logging.basicConfig(
        level=logging.DEBUG,
        # Ähnlich wie in Java: Zeitstempel, Klassenname, Level, Nachricht
        format="%(asctime)s | %(name)-35s | %(levelname)-8s | %(message)s",
        datefmt="%H:%M:%S",
    )


# =============================================================================
# Python-Einstiegspunkt: if __name__ == "__main__"
# =============================================================================
#
# Java hat public static void main(String[] args) als erzwungenen Einstieg.
# Python-Module können sowohl importiert als auch direkt ausgeführt werden.
# Dieser Guard stellt sicher, dass der folgende Code nur beim direkten
# Ausführen (`python main.py`), NICHT beim Importieren läuft.
#
# Beim Import gilt:   __name__ == "main"    → FALSCH → Block wird übersprungen
# Beim Direktaufruf:  __name__ == "__main__" → WAHR  → Block wird ausgeführt

if __name__ == "__main__":

    # 1. Logging konfigurieren (einmalig, zentral, bevor irgendetwas anderes läuft)
    konfiguriere_logging()

    # -------------------------------------------------------------------------
    print("\n" + "=" * 65)
    print(" DEMO 1: Logging in Aktion")
    print("=" * 65)
    # -------------------------------------------------------------------------
    konto_grace = Bankkonto("Grace Hopper", 500.0) #1
    konto_grace.einzahlen(250.0)  #2

    try:
        konto_grace.abheben(1000.0)   # → löst ValueError aus
    except ValueError as e:
        logging.getLogger(__name__).error("Exception abgefangen in main: %s", e)

    # -------------------------------------------------------------------------
    print("\n" + "=" * 65)
    print(" DEMO 2: Docstrings zur Laufzeit auslesen")
    print("=" * 65)
    # -------------------------------------------------------------------------
    # Docstrings sind kein toter Kommentar – sie sind Teil des Objekts und
    # zur Laufzeit über das __doc__-Attribut zugreifbar.
    # IDEs wie PyCharm zeigen sie als Tooltip (Cursor auf Funktionsname → Ctrl+links klick).
    print(f"\nDokumentaion von berechne_zinseszins():\n{berechne_zinseszins.__doc__}")

    # -------------------------------------------------------------------------
    print("\n" + "=" * 65)
    print(" DEMO 3: Zinseszins-Berechnung")
    print("=" * 65)
    # -------------------------------------------------------------------------
    ergebnis = berechne_zinseszins(1000.0, 5.0, 10)
    print(f"\n1000€ × 5% p.a. über 10 Jahre = {ergebnis}€")

    # -------------------------------------------------------------------------
    print("\n" + "=" * 65)
    print(" DEMO 4: Unit Tests ausführen (unittest)")
    print("=" * 65)
    # -------------------------------------------------------------------------
    # Hinweis: Im industriellen Umfeld nutzt man pytest (→ tests/test_modul8.py).
    # argv=['first-arg-is-ignored'] verhindert Konflikte mit sys.argv,
    # exit=False verhindert, dass das Programm nach den Tests beendet wird.
    unittest.main(argv=["first-arg-is-ignored"], exit=False, verbosity=2)
