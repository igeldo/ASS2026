from mitarbeiter import Mitarbeiter


class Admin(Mitarbeiter):
    """
    Systemadministrator.
    Darf Stunden nur von Montag bis Freitag zwischen 7 und 17 Uhr eintragen
    und sieht im Kalender ausschließlich Bürotage.
    Zusätzliche Fähigkeit: Support-Tickets erstellen.
    """

    BÜROTAGE   = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag"]
    BÜRO_START = 7
    BÜRO_ENDE  = 17

    def __init__(self, vorname: str, firmenname: str, gehalt: float,
                 einstellungsart: str, laptop_seriennummer: str = ""):
        super().__init__(vorname, firmenname, "Admin", gehalt, einstellungsart)
        self.lizenz_liste: list[str] = []
        self.laptop_seriennummer = laptop_seriennummer

    # ------------------------------------------------------------------
    # Polymorphe Überschreibungen
    # ------------------------------------------------------------------

    def stunden_eintragen(self, tag: str, uhrzeit: int, dauer: float = 1.0):
        """Mo–Fr, 7–17 Uhr. Außerhalb dieser Grenzen wird abgelehnt."""
        if tag not in self.BÜROTAGE:
            print(f"[Admin] Abgelehnt: '{tag}' ist kein Bürotag (nur Mo–Fr).")
            return
        if not (self.BÜRO_START <= uhrzeit < self.BÜRO_ENDE):
            print(f"[Admin] Abgelehnt: {uhrzeit}:00 Uhr liegt außerhalb der Bürozeiten (7–17).")
            return
        self.stunden_gesamt += dauer
        self.kalender.append(f"Stunden: {tag} {uhrzeit}:00 Uhr ({dauer}h)")
        print(f"[Admin] Stunden eingetragen: {tag} {uhrzeit}:00 Uhr ({dauer}h)")

    def kalender_einsehen(self):
        """Zeigt nur Einträge, die einem Bürotag zugeordnet sind."""
        gefiltert = [e for e in self.kalender if any(t in e for t in self.BÜROTAGE)]
        print(f"[Admin] Kalender (nur Bürotage): {gefiltert or '(leer)'}")

    # ------------------------------------------------------------------
    # Rollenspezifische Methoden
    # ------------------------------------------------------------------

    def ticket_erstellen(self, betreff: str):
        print(f"[Admin] Ticket erstellt: '{betreff}' | Laptop S/N: {self.laptop_seriennummer}")

    def to_dict(self) -> dict:
        d = super().to_dict()
        d["laptop_seriennummer"] = self.laptop_seriennummer
        return d
