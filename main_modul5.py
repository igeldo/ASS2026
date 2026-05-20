# =============================================================================
# Informatik 4 – Von Java zu OOP in Python
# main_modul5.py – Demonstrations-Anwendung für Modul 5: Entwurfsmuster
#
# Dieses Skript importiert alle Klassen und Funktionen aus
# modul5_entwurfsmuster.py und führt die sieben Abschnitte vor.
#
# Ausführen:
#   PyCharm:  grüner Play-Button (Shift + F10)
#   Terminal: python main_modul5.py
# =============================================================================

from modul5_entwurfsmuster import (
    # Singleton
    LoggerJavaStil,
    konfiguration,
    Datenbankverbindung,
    # Factory
    TierFactoryJavaStil,
    erzeuge_tier,
    Pizza,
    # Observer
    Newsletter,
    ZaehlenderAbonnent,
    # Strategy
    Warenkorb,
    kein_rabatt,
    prozent_rabatt,
    fixer_rabatt,
    # Context Manager
    Zeitmessung,
    transaktion,
)


def trennlinie(titel: str) -> None:
    """Gibt eine formatierte Überschrift für jeden Abschnitt aus."""
    print(f"\n{'=' * 60}")
    print(f"  {titel}")
    print(f"{'=' * 60}")


# -----------------------------------------------------------------------------
# 1. SINGLETON – JAVA-STIL
# -----------------------------------------------------------------------------
def demo_singleton_java_stil() -> None:
    trennlinie("Abschnitt 1: Singleton – Java-Stil mit __new__")

    # Zweimal "erzeugt" – aber wir bekommen DAS GLEICHE Objekt zurück.
    logger_a = LoggerJavaStil()
    logger_b = LoggerJavaStil()

    logger_a.log("Server gestartet")
    logger_b.log("Erste Anfrage")

    print(f"logger_a = {logger_a}")
    print(f"logger_b = {logger_b}")
    print(f"\nSind es identische Objekte?  logger_a is logger_b -> {logger_a is logger_b}")
    print(f"Einträge (via logger_a.eintraege): {logger_a.eintraege}")
    # Beide Variablen zeigen auf dasselbe Objekt – Java-Pattern, Python-Syntax.


# -----------------------------------------------------------------------------
# 2. SINGLETON – PYTHONISCH (MODUL + DECORATOR)
# -----------------------------------------------------------------------------
def demo_singleton_pythonisch() -> None:
    trennlinie("Abschnitt 2: Singleton – Pythonisch (Modul + Decorator)")

    # Variante A: das Modul-Attribut IST der Singleton.
    # Wer "from modul5_entwurfsmuster import konfiguration" macht, bekommt
    # immer dasselbe _Konfiguration-Objekt – Python cacht Modul-Importe.
    print(f"Modul-Singleton:  {konfiguration}")
    konfiguration.debug = True
    print(f"Nach Änderung:    {konfiguration}")

    # Variante B: zweimal @singleton-dekorierte Klasse aufrufen.
    db1 = Datenbankverbindung("postgres://prod")
    db2 = Datenbankverbindung("wird-ignoriert")     # Konstruktor läuft NICHT erneut

    print(f"\n@singleton Variante:")
    print(f"  db1 = {db1}")
    print(f"  db2 = {db2}")
    print(f"  db1 is db2 -> {db1 is db2}")          # True
    # Lehre: drei verschiedene Wege – derselbe Effekt.
    # In Java bräuchte jeder dieser Wege wieder eine eigene Singleton-Klasse.


# -----------------------------------------------------------------------------
# 3. FACTORY – JAVA-STIL
# -----------------------------------------------------------------------------
def demo_factory_java_stil() -> None:
    trennlinie("Abschnitt 3: Factory – Java-Stil mit if/elif")

    # Klassische Java-Factory, 1:1 in Python nachgebaut.
    arten = ["hund", "katze", "kuh"]
    for art in arten:
        tier = TierFactoryJavaStil.erzeuge(art)
        print(f"  Factory.erzeuge({art!r:8}) -> {tier}")

    # Fehlerfall – wie eine IllegalArgumentException in Java:
    print("\nUngültige Art:")
    try:
        TierFactoryJavaStil.erzeuge("drache")
    except ValueError as fehler:
        print(f"  ValueError: {fehler}")
    # Stolperstein: für jede neue Tierart muss die if/elif-Kette wachsen.


# -----------------------------------------------------------------------------
# 4. FACTORY – PYTHONISCH (DICT-DISPATCH + CLASSMETHOD)
# -----------------------------------------------------------------------------
def demo_factory_pythonisch() -> None:
    trennlinie("Abschnitt 4: Factory – Pythonisch (Dict-Dispatch + classmethod)")

    # Variante A: Dict-Dispatch.
    # Klassen sind Objekte – wir schlagen sie im Dict nach und rufen sie auf.
    print("Dict-Dispatch (Registry):")
    for art in ["hund", "katze", "kuh"]:
        tier = erzeuge_tier(art)
        print(f"  erzeuge_tier({art!r:8}) -> {tier}")

    # Variante B: @classmethod als alternativer Konstruktor.
    # Vorteil: die Erzeugungslogik wohnt dort, wo sie hingehört – in der Klasse.
    print("\nclassmethod-Factory:")
    print(f"  Pizza.margherita() -> {Pizza.margherita()}")
    print(f"  Pizza.salami()     -> {Pizza.salami()}")
    # Vergleich:
    #   Java:    new MargheritaPizza()  oder  PizzaFactory.erzeuge("margherita")
    #   Python:  Pizza.margherita()                  – direkter, lesbarer.


# -----------------------------------------------------------------------------
# 5. OBSERVER – JAVA-INTERFACE vs. PYTHON-CALLABLES
# -----------------------------------------------------------------------------
def demo_observer() -> None:
    trennlinie("Abschnitt 5: Observer – Callables statt Listener-Interface")

    news = Newsletter()

    # Abonnent 1: eine ganz normale Funktion.
    def auf_konsole(ausgabe: str) -> None:
        print(f"  [Konsole]   {ausgabe}")

    # Abonnent 2: ein Lambda – in Java gar nicht so leicht ohne Interface.
    nachrichten_archiv: list[str] = []
    archivieren = lambda ausgabe: nachrichten_archiv.append(ausgabe)

    # Abonnent 3: ein Objekt mit __call__ (für Beobachter MIT Zustand).
    zaehler = ZaehlenderAbonnent("Statistik")

    news.abonnieren(auf_konsole)
    news.abonnieren(archivieren)
    news.abonnieren(zaehler)

    print(f"Vor dem Versand: {news}")
    news.veroeffentlichen("Ausgabe Mai 2026")
    news.veroeffentlichen("Sonderausgabe")

    print(f"\nArchiv:  {nachrichten_archiv}")
    print(f"Zähler:  {zaehler}")
    # Drei völlig unterschiedliche "Beobachter" – keiner musste ein
    # Interface implementieren. Duck Typing trifft Observer-Pattern.


# -----------------------------------------------------------------------------
# 6. STRATEGY – FUNKTIONEN ALS FIRST-CLASS OBJEKTE
# -----------------------------------------------------------------------------
def demo_strategy() -> None:
    trennlinie("Abschnitt 6: Strategy – Funktionen statt Strategy-Klassen")

    # Drei verschiedene "Strategien" – aber nur eine ist eine echte Funktion,
    # die anderen werden von Factory-Funktionen erzeugt (Closures).
    strategien = {
        "ohne Rabatt":    kein_rabatt,
        "10% Rabatt":     prozent_rabatt(10),
        "5€ Rabatt":      fixer_rabatt(5),
    }

    for bezeichnung, strategie in strategien.items():
        korb = Warenkorb(strategie)
        korb.hinzufuegen("Buch",  19.99)
        korb.hinzufuegen("Stift",  2.50)
        korb.hinzufuegen("Heft",   3.50)
        print(f"  {bezeichnung:14} -> {korb}")

    # Strategie zur Laufzeit austauschen – einfach Attribut neu setzen.
    korb = Warenkorb()
    korb.hinzufuegen("Laptop", 999.00)
    print(f"\nVor Strategie-Wechsel:  {korb}")
    korb.strategie = prozent_rabatt(20)
    print(f"Nach Strategie-Wechsel: {korb}")
    # In Java: setRabattStrategie(new ProzentRabatt(20))  – plus eine Klasse mehr.


# -----------------------------------------------------------------------------
# 7. CONTEXT MANAGER – PYTHONS "TRY-WITH-RESOURCES" AUF STEROIDEN
# -----------------------------------------------------------------------------
def demo_context_manager() -> None:
    trennlinie("Abschnitt 7: Context Manager – with-Statement")

    # Variante A: Klasse mit __enter__/__exit__ – zur Zeitmessung.
    with Zeitmessung("Liste aufbauen") as messung:
        summe = sum(i * i for i in range(100_000))
    print(f"  Ergebnis: {summe}")
    print(f"  Gemessene Dauer: {messung.dauer_ms:.2f} ms")

    # Variante B: @contextmanager – ohne Klasse, nur eine Generator-Funktion.
    # Erfolgreicher Durchlauf:
    print("\nErfolgreiche Transaktion:")
    with transaktion("Buchung 42") as tx_name:
        print(f"   ...führe Buchung '{tx_name}' aus...")

    # Bei einem Fehler im with-Block läuft trotzdem das Aufräumen –
    # ohne dass irgendwer try/finally schreiben muss.
    print("\nTransaktion mit Fehler:")
    try:
        with transaktion("Buchung 43"):
            raise RuntimeError("Konto gesperrt")
    except RuntimeError as fehler:
        print(f"   Aufrufer fängt: {fehler}")
    # Kernidee: __exit__ läuft GARANTIERT – das ist der eigentliche Wert
    # des Patterns. Genau das, was Javas try-with-resources auch will,
    # aber Python erlaubt jeden Anwendungsfall: Locks, Zeit, Transaktionen,
    # Mocks im Test, temporäres Verzeichnis, ...


# -----------------------------------------------------------------------------
# Python-Einstiegspunkt
# -----------------------------------------------------------------------------
# Java: public static void main(String[] args) { ... }
# Python: if __name__ == "__main__": schützt Code vor Ausführung beim Import.
if __name__ == "__main__":
    demo_singleton_java_stil()
    demo_singleton_pythonisch()
    demo_factory_java_stil()
    demo_factory_pythonisch()
    demo_observer()
    demo_strategy()
    demo_context_manager()

    trennlinie("Ende der Demonstration – Modul 5: Pythonische Entwurfsmuster")
