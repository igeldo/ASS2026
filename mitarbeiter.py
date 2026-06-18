from unternehmen import Unternehmen


class Mitarbeiter(Unternehmen):
    """
    Erweiterung von Unternehmen um personenbezogene Mitarbeiterdaten.
    Definiert die Schnittstelle (stunden_eintragen, kalender_einsehen,
    urlaub_buchen), die von jeder Rolle überschrieben wird.
    """

    def __init__(self, vorname: str, firmenname: str, rolle: str,
                 gehalt: float, einstellungsart: str):
        super().__init__(firmenname)
        self.vorname = vorname
        self.rolle = rolle
        self.gehalt = gehalt
        self.einstellungsart = einstellungsart
        self.stunden_gesamt: float = 0.0

    # ------------------------------------------------------------------
    # Polymorphe Methoden – werden in Unterklassen überschrieben
    # ------------------------------------------------------------------

    def stunden_eintragen(self, tag: str, uhrzeit: int, dauer: float = 1.0):
        raise NotImplementedError(f"{self.rolle} hat keine Implementierung für stunden_eintragen.")

    def kalender_einsehen(self):
        raise NotImplementedError(f"{self.rolle} hat keine Implementierung für kalender_einsehen.")

    def urlaub_buchen(self, datum: str):
        eintrag = f"Urlaub am {datum}"
        self.kalender.append(eintrag)
        print(f"[{self.rolle}] Urlaub gebucht: {datum}")

    # ------------------------------------------------------------------
    # Hilfsmethoden
    # ------------------------------------------------------------------

    def to_dict(self) -> dict:
        return {
            "vorname": self.vorname,
            "firma": self.name,
            "rolle": self.rolle,
            "gehalt": self.gehalt,
            "einstellungsart": self.einstellungsart,
            "stunden_gesamt": self.stunden_gesamt,
        }

    def __str__(self) -> str:
        return (f"{self.rolle} | {self.vorname} | Firma: {self.name} | "
                f"Gehalt: {self.gehalt:.2f} € | Einstellung: {self.einstellungsart}")
