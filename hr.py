from mitarbeiter import Mitarbeiter


class HR(Mitarbeiter):
    """
    Human-Resources-Mitarbeiter.
    Jede Interaktion mit dem Arbeitszeitmodell erhöht den internen
    Problem-Counter – ein satirischer Kommentar zur HR-Realität.
    """

    def __init__(self, vorname: str, firmenname: str,
                 gehalt: float, einstellungsart: str):
        super().__init__(vorname, firmenname, "HR", gehalt, einstellungsart)
        self.problem_counter: int = 0

    # ------------------------------------------------------------------
    # Polymorphe Überschreibungen
    # ------------------------------------------------------------------

    def stunden_eintragen(self, tag: str, uhrzeit: int, dauer: float = 1.0):
        self.problem_counter += 1
        print(f"[HR] Stunden eintragen? Das ist schon Problem Nr. {self.problem_counter}.")

    def kalender_einsehen(self):
        self.problem_counter += 1
        print(f"[HR] Kalender einsehen? Das ist schon Problem Nr. {self.problem_counter}.")

    def urlaub_buchen(self, datum: str):
        self.problem_counter += 1
        print(f"[HR] Urlaub buchen für '{datum}'? "
              f"Das ist schon Problem Nr. {self.problem_counter}. "
              f"Bitte Formular HR-42b ausfüllen.")

    def to_dict(self) -> dict:
        d = super().to_dict()
        d["problem_counter"] = self.problem_counter
        return d
