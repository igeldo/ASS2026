# =============================================================================
# Informatik 4
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
    Tier,
    erzeuge_tier,
    _TIER_REGISTRY,
    Pizza,
    # Observer
    Newsletter,
    ZaehlenderAbonnent,
    # MVC
    Schachbrett,
    Schachsteuerung,
    ascii_view,
    json_view,
    # Strategy (Exkurs)
    Warenkorb,
    kein_rabatt,
    prozent_rabatt,
    fixer_rabatt,
    # Context Manager (Exkurs)
    Zeitmessung,
    transaktion,
)


def trennlinie(titel: str) -> None:
    """Gibt eine formatierte Überschrift für jeden Abschnitt aus."""
    print(f"\n{'=' * 60}")
    print(f"  {titel}")
    print(f"{'=' * 60}")


# -----------------------------------------------------------------------------
# 1. SINGLETON – __new__ ALS EINGRIFFSPUNKT
# -----------------------------------------------------------------------------
def demo_singleton_klassisch() -> None:
    trennlinie("Abschnitt 1: Singleton – klassisch über __new__")

    # Zweimal "erzeugt" – aber wir bekommen DASSELBE Objekt zurück.
    # __new__ entscheidet, ob ein neues Objekt entsteht oder das gecachte
    # zurückkommt.
    logger_a = LoggerJavaStil()
    logger_b = LoggerJavaStil()

    logger_a.log("Server gestartet")
    logger_b.log("Erste Anfrage")

    print(f"logger_a = {logger_a}")
    print(f"logger_b = {logger_b}")
    print(f"\nSind es identische Objekte?  logger_a is logger_b -> {logger_a is logger_b}")
    print(f"Einträge (via logger_a.eintraege): {logger_a.eintraege}")
    # Beide Variablen zeigen auf dasselbe Objekt – ein Klassenattribut als
    # Cache, eine Eingriffspunkt-Methode, fertig.


# -----------------------------------------------------------------------------
# 2. SINGLETON – PYTHONISCH (MODUL + DECORATOR)
# -----------------------------------------------------------------------------
def demo_singleton_pythonisch() -> None:
    trennlinie("Abschnitt 2: Singleton – Modul-Singleton + @singleton")

    # Variante A: das Modul-Attribut IST der Singleton.
    # Der Beweis ist nicht "es existiert", sondern "es existiert nur EINMAL".
    # Dazu simulieren wir zwei voneinander unabhängige Stellen im Programm:
    import sys
    import modul5_entwurfsmuster as modul          # Stelle A: ganzes Modul
    konfig_stelle_a = modul.konfiguration
    konfig_stelle_b = konfiguration                # Stelle B: Top-Level-Import (Kopf der Datei)

    # Beide Zugriffswege liefern DASSELBE Objekt – nicht nur ein gleiches.
    print(f"Stelle A sieht: {konfig_stelle_a}")
    print(f"Stelle B sieht: {konfig_stelle_b}")
    print(f"Dasselbe Objekt?  A is B -> {konfig_stelle_a is konfig_stelle_b}")

    # Folge: eine Änderung an Stelle A ist sofort an Stelle B sichtbar –
    # es gibt schlicht nur EIN Objekt im ganzen Prozess.
    print("\nStelle A setzt debug = True ...")
    konfig_stelle_a.debug = True
    print(f"... Stelle B sieht jetzt: {konfig_stelle_b}")

    # Warum nur einmal? Beim ersten Import führt Python den Modul-Code GENAU
    # EINMAL aus (dabei läuft 'konfiguration = _Konfiguration()') und legt das
    # Modulobjekt in sys.modules ab. Jeder weitere Import findet es dort und
    # führt den Code NICHT erneut aus – die Instanz entsteht nie ein zweites Mal.
    print(f"\nModul in sys.modules gecacht? -> {'modul5_entwurfsmuster' in sys.modules}")

    # Variante B: zweimal @singleton-dekorierte Klasse aufrufen.
    # Der Decorator hält die einzige Instanz in einem Dict fest und gibt sie
    # bei jedem weiteren Aufruf zurück – der Konstruktor läuft NICHT erneut.
    db1 = Datenbankverbindung("postgres://prod")
    db2 = Datenbankverbindung("wird-ignoriert")     # Konstruktor läuft NICHT erneut

    print(f"\n@singleton Variante:")
    print(f"  db1 = {db1}")
    print(f"  db2 = {db2}")
    print(f"  db1 is db2 -> {db1 is db2}")          # True
    # Drei pythonische Wege, derselbe Effekt – das Modul-System reicht für
    # die meisten Fälle aus.


# -----------------------------------------------------------------------------
# 3. FACTORY – EXPLIZIT MIT if/elif
# -----------------------------------------------------------------------------
def demo_factory_explizit() -> None:
    trennlinie("Abschnitt 3: Factory – explizit mit if/elif")

    # Die explizite Variante: eine Factory-Klasse mit einer Verzweigung pro Art.
    # Lesbar, aber jede neue Tierart erzwingt eine neue Code-Zeile.
    arten = ["hund", "katze", "kuh"]
    for art in arten:
        tier = TierFactoryJavaStil.erzeuge(art)
        print(f"  Factory.erzeuge({art!r:8}) -> {tier}")

    # Fehlerfall: unbekannter Schlüssel löst ValueError aus.
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
    trennlinie("Abschnitt 4: Factory – Dict-Dispatch + classmethod")

    # Variante A: Dict-Dispatch.
    # Klassen sind first-class Objekte – wir schlagen sie im Dict nach und
    # rufen sie auf. Neue Tierart? Eine Dict-Zeile, kein Code an der Factory.
    print("Dict-Dispatch (Registry):")
    for art in ["hund", "katze", "kuh"]:
        tier = erzeuge_tier(art)
        print(f"  erzeuge_tier({art!r:8}) -> {tier}")

    # Der eigentliche Gewinn gegenüber if/elif zeigt sich erst HIER: eine neue
    # Art kommt zur LAUFZEIT dazu – mit einer einzigen Registry-Zeile, ohne dass
    # erzeuge_tier angefasst wird. (In Abschnitt 3 wäre dafür ein neuer
    # if/elif-Zweig im Quelltext nötig gewesen.)
    print("\nNeue Art zur Laufzeit registrieren:")

    class Drache(Tier):
        def laut(self) -> str:
            return "Feuer speien"

    _TIER_REGISTRY["drache"] = Drache               # genau eine Zeile genügt
    print(f"  erzeuge_tier('drache') -> {erzeuge_tier('drache')}")
    print("  -> erzeuge_tier() selbst blieb dabei unverändert.")

    # Variante B: @classmethod als alternativer Konstruktor.
    # Die Erzeugungslogik wohnt direkt in der Klasse; Aufruf liest sich wie
    # Domänen-Vokabular.
    print("\nclassmethod-Factory:")
    print(f"  Pizza.margherita() -> {Pizza.margherita()}")
    print(f"  Pizza.salami()     -> {Pizza.salami()}")
    # Faustregel:
    #   Laufzeit-Auswahl per String/Enum   -> Dict-Dispatch
    #   Auswahl steht zur Programmierzeit  -> @classmethod


# -----------------------------------------------------------------------------
# 5. OBSERVER – CALLABLES STATT LISTENER-INTERFACE
# -----------------------------------------------------------------------------
def demo_observer() -> None:
    trennlinie("Abschnitt 5: Observer – Liste von Callables")

    news = Newsletter()

    # Abonnent 1: eine ganz normale Funktion.
    def auf_konsole(ausgabe: str) -> None:
        print(f"  [Konsole]   {ausgabe}")

    # Abonnent 2: ein Lambda – Funktionen sind first-class, also direkt einsetzbar.
    nachrichten_archiv: list[str] = []
    archivieren = lambda ausgabe: nachrichten_archiv.append(ausgabe)

    # Abonnent 3: ein Objekt mit __call__ – für Beobachter MIT Zustand.
    zaehler = ZaehlenderAbonnent("Statistik")

    news.abonnieren(auf_konsole)
    news.abonnieren(archivieren)
    news.abonnieren(zaehler)

    print(f"Vor dem Versand: {news}")
    news.veroeffentlichen("Ausgabe Mai 2026")
    news.veroeffentlichen("Sonderausgabe")

    print(f"\nArchiv:  {nachrichten_archiv}")
    print(f"Zähler:  {zaehler}")
    # Drei völlig unterschiedliche Abonnenten – verbunden allein durch die
    # Eigenschaft, aufrufbar zu sein. Genau dieser Mechanismus trägt gleich MVC.


# -----------------------------------------------------------------------------
# 6. MVC – MODEL / VIEW / CONTROLLER (BAUT AUF OBSERVER AUF)
# -----------------------------------------------------------------------------
def demo_mvc() -> None:
    trennlinie("Abschnitt 6: MVC – Model, View, Controller")

    # MODEL: hält den Zustand (eine Figur auf einem Feld). Die View-Liste im
    # Model IST der Observer-Mechanismus aus Abschnitt 5.
    brett = Schachbrett(figur="K", feld="e1")

    # Zwei VIEWS abonnieren DASSELBE Model: eine fürs Auge (ASCII), eine als
    # JSON – so sähe die Antwort eines REST-Backends aus.
    brett.registriere_view(ascii_view)
    brett.registriere_view(json_view)

    # CONTROLLER: vermittelt zwischen Eingabe und Model. Im Projekt ein
    # Route-Handler (POST /zug); hier ein simpler Methodenaufruf.
    steuerung = Schachsteuerung(brett)

    print("Startaufstellung (König auf e1):")
    ascii_view(brett)            # erste Darstellung anstoßen
    json_view(brett)

    # Ein einziger Controller-Aufruf – beide Views aktualisieren sich von selbst,
    # weil das Model sie als Observer benachrichtigt.
    print("\nController: ziehe nach e2  ->  beide Views reagieren:")
    steuerung.ziehe("e2")

    print("\nController: ziehe nach e4:")
    steuerung.ziehe("e4")

    # Fehlerfall: der Controller validiert die Eingabe, bevor er das Model ändert.
    print("\nUngültiges Kommando:")
    try:
        steuerung.ziehe("z9")
    except ValueError as fehler:
        print(f"  ValueError: {fehler}")
    # Kernaussage: Model, View und Controller sind entkoppelt. Eine zweite View
    # (z. B. eine Web-Oberfläche) kommt ohne eine Zeile Model-Änderung dazu.


# -----------------------------------------------------------------------------
# EXKURS 1 (BONUS): STRATEGY – FUNKTIONEN ALS FIRST-CLASS OBJEKTE
# -----------------------------------------------------------------------------
def demo_strategy() -> None:
    trennlinie("Exkurs 1 (Bonus): Strategy – Funktionen als Argument")

    # Drei Strategien als Funktionen. prozent_rabatt(10) ist ein Aufruf, der
    # eine FUNKTION zurückgibt – eine Closure, die den Wert 10 mitschleppt.
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
    # Kein Setter, kein Pattern-Code: die Strategie IST nur ein Funktionswert.
    korb = Warenkorb()
    korb.hinzufuegen("Laptop", 999.00)
    print(f"\nVor Strategie-Wechsel:  {korb}")
    korb.strategie = prozent_rabatt(20)
    print(f"Nach Strategie-Wechsel: {korb}")
    # In der Praxis begegnet man dem Pattern überall: sorted(key=...),
    # threading.Thread(target=...), map(funktion, ...) – jedes Mal Strategy.


# -----------------------------------------------------------------------------
# EXKURS 2 (BONUS): CONTEXT MANAGER – __enter__/__exit__ UND @contextmanager
# -----------------------------------------------------------------------------
def demo_context_manager() -> None:
    trennlinie("Exkurs 2 (Bonus): Context Manager – with-Statement")

    # Variante A: Klasse mit __enter__/__exit__ zur Zeitmessung.
    # __exit__ läuft garantiert (sobald __enter__ durch ist) – auch bei Exceptions.
    with Zeitmessung("Liste aufbauen") as messung:
        summe = sum(i * i for i in range(100_000))
    print(f"  Ergebnis: {summe}")
    print(f"  Gemessene Dauer: {messung.dauer_ms:.2f} ms")

    # Variante B: @contextmanager – Generator-Funktion mit einem yield.
    # Erfolgreicher Durchlauf:
    print("\nErfolgreiche Transaktion:")
    with transaktion("Buchung 42") as tx_name:
        print(f"   ...führe Buchung '{tx_name}' aus...")

    # Auch bei einer Exception im with-Block läuft das Aufräumen zuverlässig –
    # niemand muss try/finally schreiben.
    print("\nTransaktion mit Fehler:")
    try:
        with transaktion("Buchung 43"):
            raise RuntimeError("Konto gesperrt")
    except RuntimeError as fehler:
        print(f"   Aufrufer fängt: {fehler}")
    # Anwendungsbreite: open(), Locks, Verbindungen, Mocks im Test,
    # tempfile.TemporaryDirectory – alles dasselbe Sprachmittel.


# -----------------------------------------------------------------------------
# Python-Einstiegspunkt
# -----------------------------------------------------------------------------
# if __name__ == "__main__" schützt Code vor Ausführung, wenn die Datei nur
# als Modul importiert wird.
if __name__ == "__main__":
    # Kern der Präsentation (~20 Min)
    demo_singleton_klassisch()
    demo_singleton_pythonisch()
    demo_factory_explizit()
    demo_factory_pythonisch()
    demo_observer()
    demo_mvc()

    # Exkurs / Bonus – nur, falls am Ende noch Zeit ist
    demo_strategy()
    demo_context_manager()

    trennlinie("Ende der Demonstration – Modul 5: Pythonische Entwurfsmuster")
