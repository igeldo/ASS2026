# =============================================================================
# Informatik 4 – Von Java zu OOP in Python
# Ausgewählte Softwaresysteme Programmierung IV (ASS-PR4)
# FH Dortmund | Prof. Dr. Burkhard Igel
#
# tests/test_modul8.py – Pytest-Teststuite für Modul 8
#
# Ausführen:
#   pytest tests/                    # Alle Tests
#   pytest tests/ -v                 # Verbose (wie JUnit in IntelliJ)
#   pytest tests/ -v --tb=short      # Mit kurzem Traceback bei Fehlern
#   pytest tests/ --cov=informatik4_modul8_werkzeuge  # Mit Coverage-Report
#
# ┌─────────────────────────────────────────────────────────────────────────┐
# │  Java (JUnit 5)                │  Python (pytest)                      │
# ├─────────────────────────────────────────────────────────────────────────┤
# │  @Test                         │  def test_...():  (kein Decorator!)   │
# │  @BeforeEach                   │  @pytest.fixture (oder setUp-Methode) │
# │  assertEquals(e, a)            │  assert a == e   (natives assert!)    │
# │  assertThrows(Type, lambda)    │  with pytest.raises(Type):            │
# │  @ParameterizedTest            │  @pytest.mark.parametrize(...)        │
# └─────────────────────────────────────────────────────────────────────────┘
#
# Warum pytest statt unittest?
#   1. Kein Klassen-Boilerplate nötig – reine Funktionen reichen aus.
#   2. Natives `assert` statt assertEqual/assertRaises-Methoden.
#   3. Fixtures sind flexibler als @BeforeEach/@AfterEach.
#   4. Parametrisierung mit @pytest.mark.parametrize ersetzt JUnits
#      @ParameterizedTest/@MethodSource ohne externe Klassen.
#   5. pytest entdeckt Tests automatisch (Convention: Dateien mit test_*,
#      Funktionen mit test_*). Kein Registrieren nötig.
# =============================================================================

import pytest

# sys.path-Trick: Da tests/ ein Unterordner ist, muss Python wissen, wo das
# Hauptmodul liegt. In PyCharm wird das automatisch konfiguriert. Im Terminal
# arbeitet man mit PYTHONPATH=. pytest tests/ oder nutzt pyproject.toml.
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from informatik4_modul8_werkzeuge import Bankkonto, berechne_zinseszins


# =============================================================================
# FIXTURES – Pytest-Äquivalent zu @BeforeEach in JUnit
# =============================================================================
#
# Eine Fixture ist eine Funktion, die Testvoraussetzungen bereitstellt.
# pytest erkennt sie automatisch anhand des Namens in der Testfunktion.
# Scope-Optionen: "function" (default), "class", "module", "session"

@pytest.fixture
def leeres_konto():
    """Liefert ein frisches Konto mit 0€ Guthaben."""
    return Bankkonto("Test-Inhaber", 0.0)


@pytest.fixture
def konto_mit_guthaben():
    """Liefert ein Konto mit 500€ Startguthaben."""
    return Bankkonto("Ada Lovelace", 500.0)


# =============================================================================
# TESTS – Einfache Funktionen, kein Klassen-Overhead
# =============================================================================

class TestBankkonto:
    """
    Tests für die Bankkonto-Klasse.

    Hinweis: In pytest sind Testklassen optional – sie helfen lediglich
    bei der logischen Gruppierung. Anders als in JUnit sind sie KEINE
    Pflicht. Es gibt kein 'extends TestCase'.
    """

    def test_kontostand_nach_erstellung(self, konto_mit_guthaben):
        # Idiomatisches pytest: kein self.assertEqual, nur natives assert
        assert konto_mit_guthaben.kontostand == 500.0

    def test_kontostand_ist_readonly(self, konto_mit_guthaben):
        """Das @property ohne Setter muss AttributeError bei Zuweisung werfen."""
        with pytest.raises(AttributeError):
            konto_mit_guthaben.kontostand = 9999.0

    def test_einzahlung_erhoeht_kontostand(self, konto_mit_guthaben):
        konto_mit_guthaben.einzahlen(100.0)
        assert konto_mit_guthaben.kontostand == 600.0

    def test_mehrfache_einzahlungen(self, leeres_konto):
        leeres_konto.einzahlen(100.0)
        leeres_konto.einzahlen(50.0)
        leeres_konto.einzahlen(25.0)
        assert leeres_konto.kontostand == 175.0

    def test_einzahlung_null_wirft_fehler(self, leeres_konto):
        with pytest.raises(ValueError):
            leeres_konto.einzahlen(0.0)

    def test_einzahlung_negativer_betrag_wirft_fehler(self, leeres_konto):
        with pytest.raises(ValueError):
            leeres_konto.einzahlen(-50.0)

    def test_abhebung_reduziert_kontostand(self, konto_mit_guthaben):
        konto_mit_guthaben.abheben(200.0)
        assert konto_mit_guthaben.kontostand == 300.0

    def test_abhebung_gibt_betrag_zurueck(self, konto_mit_guthaben):
        abgehoben = konto_mit_guthaben.abheben(100.0)
        assert abgehoben == 100.0

    def test_ueberziehung_wirft_fehler(self, konto_mit_guthaben):
        with pytest.raises(ValueError):
            konto_mit_guthaben.abheben(600.0)

    def test_fehlermeldung_ueberziehung_enthaelt_betrag(self, konto_mit_guthaben):
        """Prüft, dass die Fehlermeldung aussagekräftig ist – wichtig für UX."""
        with pytest.raises(ValueError, match="600"):
            konto_mit_guthaben.abheben(600.0)

    def test_str_repraesentation_enthaelt_inhaber(self, konto_mit_guthaben):
        assert "Ada Lovelace" in str(konto_mit_guthaben)

    def test_str_repraesentation_enthaelt_kontostand(self, konto_mit_guthaben):
        assert "500.00" in str(konto_mit_guthaben)


# =============================================================================
# PARAMETRISIERTE TESTS – @pytest.mark.parametrize
# =============================================================================
#
# Java-Äquivalent: @ParameterizedTest + @MethodSource / @CsvSource in JUnit 5
#
# Mit @pytest.mark.parametrize können wir eine Testfunktion mit verschiedenen
# Eingaben und erwarteten Ausgaben aufrufen – ohne Code-Duplizierung.

class TestZinsrechner:
    """Parametrisierte Tests für berechne_zinseszins()."""

    @pytest.mark.parametrize(
        "kapital, zinssatz, jahre, erwartet",
        [
            # (kapital, zinssatz, jahre, erwartet)    # Beschreibung
            (1000.0,  5.0,  10,  1628.89),            # Standardfall
            (500.0,   3.5,   5,   593.84),            # Anderer Zinssatz
            (1000.0,  0.0,  10,  1000.0),             # 0% Zinsen → kein Wachstum
            (1000.0,  5.0,   0,  1000.0),             # 0 Jahre → Startkapital
            (0.0,     5.0,  10,     0.0),             # 0€ Kapital → 0€ Endkapital
        ],
    )
    def test_berechnung(
        self,
        kapital: float,
        zinssatz: float,
        jahre: int,
        erwartet: float,
    ):
        """
        Parametrisierter Test – wird für jedes Tupel in parametrize einmal
        ausgeführt. pytest zeigt die Parameter im Testergebnis an, z. B.:
        test_berechnung[1000.0-5.0-10-1628.89]
        """
        assert berechne_zinseszins(kapital, zinssatz, jahre) == erwartet

    @pytest.mark.parametrize(
        "kapital, zinssatz, jahre",
        [
            (-100.0, 5.0, 5),    # Negatives Kapital
            (100.0,  5.0, -1),   # Negative Laufzeit
        ],
    )
    def test_ungueltige_eingaben_werfen_fehler(
        self,
        kapital: float,
        zinssatz: float,
        jahre: int,
    ):
        with pytest.raises(ValueError):
            berechne_zinseszins(kapital, zinssatz, jahre)


# =============================================================================
# INTEGRATIONS-TEST-BEISPIEL
# =============================================================================
#
# Dieser Test kombiniert Bankkonto und Zinsrechner, um ein Szenario zu testen,
# das der Realität näher kommt. In einer echten Applikation würde man
# Datenbankzugriffe etc. mit pytest-Mocks (monkeypatch / unittest.mock) ersetzen.

def test_zinseszins_wachstum_entspricht_einzahlungen():
    """
    Integrations-Test: Prüft, ob das angewachsene Kapital korrekt eingezahlt
    werden kann (kein semantischer Fehler zwischen den Modulen).
    """
    startkapital = 1000.0
    konto = Bankkonto("Integrations-Test", startkapital)

    endkapital = berechne_zinseszins(startkapital, 5.0, 10)
    gewinn = round(endkapital - startkapital, 2)

    konto.einzahlen(gewinn)

    # pytest.approx ist die idiomatische Lösung für Float-Vergleiche.
    # Java-Äquivalent: assertEquals(expected, actual, delta) in JUnit.
    assert konto.kontostand == pytest.approx(round(startkapital + gewinn, 2), abs=1e-9)
