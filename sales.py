from mitarbeiter import Mitarbeiter


class Sales(Mitarbeiter):
    """
    Vertriebsmitarbeiter.
    Darf Stunden von Montag bis Sonntag zu jeder Uhrzeit eintragen
    und hat Zugriff auf den vollständigen Kalender.
    Zusätzliche Fähigkeit: Aufträge erstellen mit Provisionsberechnung.
    """

    WOCHENTAGE = ["Montag", "Dienstag", "Mittwoch", "Donnerstag",
                  "Freitag", "Samstag", "Sonntag"]

    def __init__(self, vorname: str, firmenname: str, gehalt: float,
                 einstellungsart: str, provisions_prozent: float = 5.0):
        super().__init__(vorname, firmenname, "Sales", gehalt, einstellungsart)
        self.provisions_prozent = provisions_prozent
        self.verkäufe: list[str] = []

    # ------------------------------------------------------------------
    # Polymorphe Überschreibungen
    # ------------------------------------------------------------------

    def stunden_eintragen(self, tag: str, uhrzeit: int, dauer: float = 1.0):
        """Mo–So, alle Uhrzeiten erlaubt."""
        if tag not in self.WOCHENTAGE:
            print(f"[Sales] Ungültiger Tag: {tag}")
            return
        self.stunden_gesamt += dauer
        self.kalender.append(f"Stunden: {tag} {uhrzeit}:00 Uhr ({dauer}h)")
        print(f"[Sales] Stunden eingetragen: {tag} {uhrzeit}:00 Uhr ({dauer}h) – Wochenende erlaubt")

    def kalender_einsehen(self):
        """Zeigt den vollständigen Kalender ohne Einschränkung."""
        print(f"[Sales] Vollständiger Kalender: {self.kalender or '(leer)'}")

    # ------------------------------------------------------------------
    # Rollenspezifische Methoden
    # ------------------------------------------------------------------

    def auftrag_erstellen(self, kunde: str, betrag: float):
        provision = betrag * self.provisions_prozent / 100
        eintrag = f"{kunde} | {betrag:.2f} €"
        self.verkäufe.append(eintrag)
        print(f"[Sales] Auftrag erstellt: Kunde '{kunde}', "
              f"Betrag {betrag:.2f} €, Provision {provision:.2f} €")

    def to_dict(self) -> dict:
        d = super().to_dict()
        d["provisions_prozent"] = self.provisions_prozent
        d["anzahl_verkäufe"] = len(self.verkäufe)
        return d
