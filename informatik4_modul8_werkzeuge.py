# =============================================================================
# Informatik 4 – Von Java zu OOP in Python
# Ausgewählte Softwaresysteme Programmierung IV (ASS-PR4)
# FH Dortmund | Prof. Dr. Burkhard Igel
#
# informatik4_modul8_werkzeuge.py
# Modul 8 – Werkzeuge & Ökosystem
#
# Diese Datei demonstriert professionelles Tooling in Python im direkten
# Vergleich mit dem Java-Ökosystem:
#   Java-Tool          →  Python-Äquivalent
#   ───────────────────────────────────────
#   Maven / Gradle     →  pip + venv
#   java.util.logging  →  logging (stdlib)
#   Javadoc            →  Docstrings (Google Style)
#   JUnit              →  unittest / pytest
#   IntelliJ IDEA      →  PyCharm / Antigravity
# =============================================================================

import logging

# =============================================================================
# ABSCHNITT 1: Virtuelle Umgebungen & Paketverwaltung (Konzeptionelle Theorie)
# =============================================================================
#
# Lernziel: Verstehen, wie Python Abhängigkeiten pro Projekt isoliert.
#
# ┌─────────────────────────────────────────────────────────────────────────┐
# │  Java (Maven)                  │  Python (pip + venv)                  │
# ├─────────────────────────────────────────────────────────────────────────┤
# │  pom.xml                       │  requirements.txt                     │
# │  ~/.m2/repository (global)     │  .venv/ (pro Projekt, lokal)          │
# │  mvn install                   │  pip install -r requirements.txt      │
# │  Scope: compile/test/runtime   │  (Einfache Textliste, kein Scope)     │
# └─────────────────────────────────────────────────────────────────────────┘
#
# WARUM venv? Python installiert Pakete per Default global ins System.
# Projekt A braucht requests==2.28, Projekt B braucht requests==2.31 →
# Konflikt! Die Lösung ist ein isolierter Ordner (.venv), der einen eigenen
# Python-Interpreter und eigene Pakete enthält.
#
# Quickstart im Terminal:
#   python -m venv .venv          # Virtuelle Umgebung anlegen
#   source .venv/bin/activate     # Aktivieren (Linux/macOS)
#   .venv\Scripts\activate        # Aktivieren (Windows)
#   pip install -r requirements.txt
#
# Wichtige Erkenntnis:
# Bevor Sie in PyCharm ein Projekt starten, stellen Sie sicher, dass unten
# rechts in der IDE ein "(venv)" oder der Name Ihrer Umgebung angezeigt wird.
# Ohne venv arbeiten Sie unprofessionell.


# =============================================================================
# ABSCHNITT 2: Logging statt print()
# =============================================================================
#
# Lernziel: Nachvollziehbarkeit im Code durch professionelles Logging.
#
# ┌─────────────────────────────────────────────────────────────────────────┐
# │  Java                          │  Python                               │
# ├─────────────────────────────────────────────────────────────────────────┤
# │  import java.util.logging.*    │  import logging                       │
# │  Logger.getLogger(Klass.class) │  logging.getLogger(__name__)          │
# │  logger.info("...")            │  logger.info("...")                   │
# │  log4j / logback.xml           │  basicConfig() / dictConfig()         │
# └─────────────────────────────────────────────────────────────────────────┘
#
# LOG-LEVEL (identisch in Java und Python):
#   DEBUG    → Detaillierte Entwickler-Infos (z. B. jede Operation)
#   INFO     → Normale Betriebsmeldungen (z. B. "Konto erstellt")
#   WARNING  → Unerwartetes, aber kein Fehler (z. B. ungültige Eingabe)
#   ERROR    → Fehler, der eine Operation verhindert hat
#   CRITICAL → Systemkritischer Fehler (seltener)
#
# Die Konfiguration (Level, Format, Handler) wird EINMALIG zentral in
# main.py / der Applikations-Eintrittsdatei vorgenommen – nie in der Modul-
# Datei selbst. Das ist die Python-Konvention.

# Wir initialisieren den Logger für dieses Modul. __name__ enthält zur
# Laufzeit den vollständigen Modulnamen (z. B. "informatik4_modul8_werkzeuge").
# Das entspricht Javas Logger.getLogger(Bankkonto.class.getName()).
logger = logging.getLogger(__name__)


class Bankkonto:
    """
    Repräsentiert ein einfaches Bankkonto.

    Diese Klasse demonstriert professionelles Logging auf allen Level
    (INFO, DEBUG, WARNING, ERROR) sowie den Einsatz von Properties
    anstelle von Java-style Getter/Setter-Methoden.

    Attributes:
        inhaber (str): Name des Kontoinhabers.

    Note:
        Der Kontostand ist bewusst als Property mit privatem Backing-Attribut
        implementiert (_kontostand), um unkontrollierten Direktzugriff von
        außen zu vermeiden – ohne Java-erzwungenes `private`.
    """

    def __init__(self, inhaber: str, startguthaben: float = 0.0):
        """
        Initialisiert ein neues Bankkonto.

        Args:
            inhaber (str): Der Name des Kontoinhabers.
            startguthaben (float, optional): Das Startguthaben in Euro.
                Defaults to 0.0.
        """
        self.inhaber = inhaber
        self._kontostand = startguthaben
        # INFO-Level: Normale, relevante Betriebsmeldung
        logger.info("Konto für '%s' mit %.2f€ eröffnet.", self.inhaber, startguthaben)

    # -------------------------------------------------------------------------
    # @property: Pythons Antwort auf Java-Getter/Setter
    # -------------------------------------------------------------------------
    # Java:   private double kontostand; + public double getKontostand() {...}
    # Python: @property – der Zugriff sieht aus wie ein Attribut, hat aber
    #         die Kontrolle einer Methode.
    # -------------------------------------------------------------------------
    @property
    def kontostand(self) -> float:
        """Der aktuelle Kontostand in Euro (read-only)."""
        return self._kontostand

    def einzahlen(self, betrag: float) -> None:
        """
        Zahlt einen positiven Betrag auf das Konto ein.

        Args:
            betrag (float): Der einzuzahlende Betrag in Euro (muss > 0 sein).

        Raises:
            ValueError: Wenn der Betrag nicht positiv ist.
        """
        if betrag <= 0:
            # WARNING-Level: Ungültige Eingabe – Programm läuft weiter
            logger.warning(
                "Fehlgeschlagene Einzahlung: %.2f€ ist kein positiver Betrag.", betrag
            )
            raise ValueError(f"Einzahlungsbetrag muss positiv sein, erhalten: {betrag}")

        self._kontostand += betrag
        # DEBUG-Level: Granulare Detailinfo für Entwickler
        logger.debug(
            "%.2f€ eingezahlt auf Konto von '%s'. Neuer Stand: %.2f€",
            betrag, self.inhaber, self._kontostand
        )

    def abheben(self, betrag: float) -> float:
        """
        Hebt einen Betrag vom Konto ab, sofern Deckung vorhanden ist.

        Args:
            betrag (float): Der abzuhebende Betrag in Euro.

        Returns:
            float: Der tatsächlich abgehobene Betrag.

        Raises:
            ValueError: Wenn das Guthaben für die Abhebung nicht ausreicht.
        """
        if betrag > self._kontostand:
            # ERROR-Level: Operation fehlgeschlagen, Zustand aber stabil
            logger.error(
                "Abhebung von %.2f€ für '%s' abgelehnt – Kontostand %.2f€ nicht ausreichend.",
                betrag, self.inhaber, self._kontostand
            )
            raise ValueError(
                f"Nicht genügend Guthaben. Verfügbar: {self._kontostand:.2f}€, " f"Angefordert: {betrag:.2f}€"
            )

        self._kontostand -= betrag
        logger.info(
            "%.2f€ abgehoben von Konto '%s'. Restguthaben: %.2f€",
            betrag, self.inhaber, self._kontostand
        )
        return betrag

    def __str__(self) -> str:
        """
        Lesbare String-Repräsentation des Kontos.

        Java-Äquivalent: @Override public String toString() { ... }

        Returns:
            str: Formatierte Kontoübersicht.
        """
        return f"Bankkonto(inhaber='{self.inhaber}', kontostand={self._kontostand:.2f}€)"

    def __repr__(self) -> str:
        """Technische Repräsentation für Entwickler (z. B. im Debugger)."""
        return f"Bankkonto(inhaber={self.inhaber!r}, startguthaben={self._kontostand!r})"


# =============================================================================
# ABSCHNITT 3: Dokumentation mit Docstrings
# =============================================================================
#
# Lernziel: Code für Kollegen, IDEs und KI-Assistenten lesbar machen.
#
# ┌─────────────────────────────────────────────────────────────────────────┐
# │  Java (Javadoc)                │  Python (Docstrings)                  │
# ├─────────────────────────────────────────────────────────────────────────┤
# │  /** ... */  über der Methode  │  """ ... """  IN der Methode          │
# │  @param name Beschreibung      │  Args: name (typ): Beschreibung       │
# │  @return Beschreibung          │  Returns: typ: Beschreibung           │
# │  @throws ExceptionTyp          │  Raises: ExceptionTyp: Beschreibung   │
# │  javadoc CLI → HTML            │  sphinx-build → HTML (optional)       │
# └─────────────────────────────────────────────────────────────────────────┘
#
# Drei Docstring-Stile existieren (Google, NumPy, reStructuredText).
# Dieser Kurs verwendet den GOOGLE-STYLE, da er am besten lesbar ist und
# von PyCharm sowie KI-IDEs wie Antigravity optimal interpretiert wird.
#
# Wichtig: Docstrings sind keine Kommentare (#). Sie sind ein offizieller
# Bestandteil des Python-Objekts und zur Laufzeit über __doc__ abrufbar.

def berechne_zinseszins(kapital: float, zinssatz: float, jahre: int) -> float:
    """
    Berechnet das Endkapital nach einer Laufzeit mit Zinseszins-Effekt.

    Formel: Endkapital = Kapital × (1 + Zinssatz/100) ^ Jahre

    Diese Funktion zeigt den Google-Docstring-Style. KI-Assistenten wie
    Antigravity nutzen Docstrings als Kontext für präzise Code-Vorschläge.
    PyCharm rendert sie als Tooltip (Cursor auf Funktionsaufruf → Ctrl+Q).

    Args:
        kapital (float): Das Startkapital in Euro (muss >= 0 sein).
        zinssatz (float): Der jährliche Zinssatz in Prozent (z. B. 5.0 = 5%).
        jahre (int): Die Laufzeit in Jahren (muss >= 0 sein).

    Returns:
        float: Das berechnete Endkapital, gerundet auf 2 Dezimalstellen.

    Raises:
        ValueError: Wenn `kapital` negativ oder `jahre` negativ ist.

    Example:
        >>> berechne_zinseszins(1000.0, 5.0, 10)
        1628.89
        >>> berechne_zinseszins(500.0, 3.5, 5)
        593.84
    """
    if kapital < 0:
        raise ValueError(f"Kapital darf nicht negativ sein, erhalten: {kapital}")
    if jahre < 0:
        logger.error("Negative Laufzeit übergeben: %d Jahre.", jahre)
        raise ValueError(f"Laufzeit darf nicht negativ sein, erhalten: {jahre}")

    faktor = 1 + (zinssatz / 100)
    endkapital = kapital * (faktor ** jahre)
    logger.debug(
        "Zinseszins berechnet: %.2f€ × (1 + %.2f%%)^%d = %.2f€",
        kapital, zinssatz, jahre, round(endkapital, 2)
    )
    return round(endkapital, 2)


# Rückwärtskompatibles Alias (die ursprüngliche Version hatte einen Tippfehler)
# Dies zeigt außerdem, wie man in Python API-Rückwärtskompatibilität herstellt,
# ohne den alten Code zu brechen.
berechne_zinseszinz = berechne_zinseszins
