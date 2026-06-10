"""
Modul 3 - Vererbung & Polymorphismus
Beispiel: Unternehmensstruktur mit Mitarbeiterrollen
"""


# ──────────────────────────────────────────────
#  Basisklasse
# ──────────────────────────────────────────────

class Unternehmen:
    def __init__(self, name: str):
        self.name = name
        self.kalender: list[str] = []

    def __str__(self):
        return f"Unternehmen: {self.name}"


# ──────────────────────────────────────────────
#  Mitarbeiter  (erbt von Unternehmen)
# ──────────────────────────────────────────────

class Mitarbeiter(Unternehmen):
    def __init__(self, firmenname: str, rolle: str, gehalt: float, einstellungsart: str):
        super().__init__(firmenname)
        self.rolle = rolle
        self.gehalt = gehalt
        self.einstellungsart = einstellungsart

    # --- Methoden, die in Unterklassen überschrieben werden (Polymorphismus) ---

    def stunden_eintragen(self, tag: str, uhrzeit: int):
        print(f"[{self.rolle}] Stunden eintragen: {tag} {uhrzeit}:00 Uhr -> nicht erlaubt (Basisklasse)")

    def kalender_einsehen(self):
        print(f"[{self.rolle}] Kalender: {self.kalender if self.kalender else '(leer)'}")

    def urlaub_buchen(self, datum: str):
        eintrag = f"Urlaub am {datum}"
        self.kalender.append(eintrag)
        print(f"[{self.rolle}] Urlaub gebucht: {datum}")

    def __str__(self):
        return (f"{self.rolle} | Firma: {self.name} | "
                f"Gehalt: {self.gehalt:.2f} € | Einstellung: {self.einstellungsart}")


# ──────────────────────────────────────────────
#  Sales  (erbt von Mitarbeiter)
# ──────────────────────────────────────────────

class Sales(Mitarbeiter):
    WOCHENTAGE = ["Montag", "Dienstag", "Mittwoch", "Donnerstag",
                  "Freitag", "Samstag", "Sonntag"]

    def __init__(self, firmenname: str, gehalt: float, einstellungsart: str,
                 provisions_prozent: float = 5.0):
        super().__init__(firmenname, "Sales", gehalt, einstellungsart)
        self.provisions_prozent = provisions_prozent
        self.verkäufe_anzahl: int = 0
        self.verkäufe: list[str] = []

    def stunden_eintragen(self, tag: str, uhrzeit: int):
        """Sales: Mo–So, alle Uhrzeiten erlaubt."""
        if tag not in self.WOCHENTAGE:
            print(f"[Sales] Ungültiger Tag: {tag}")
            return
        eintrag = f"Stunden: {tag} {uhrzeit}:00 Uhr"
        self.kalender.append(eintrag)
        print(f"[Sales] Stunden eingetragen: {tag} {uhrzeit}:00 Uhr (auch Wochenende erlaubt)")

    def kalender_einsehen(self):
        """Sales: Sieht den gesamten Kalender."""
        print(f"[Sales] Vollständiger Kalender: {self.kalender if self.kalender else '(leer)'}")

    def auftrag_erstellen(self, kunde: str, betrag: float):
        eintrag = f"{kunde} | {betrag:.2f} €"
        self.verkäufe.append(eintrag)
        self.verkäufe_anzahl += 1
        provision = betrag * self.provisions_prozent / 100
        print(f"[Sales] Auftrag erstellt: Kunde '{kunde}', "
              f"Betrag {betrag:.2f} €, Provision {provision:.2f} €")


# ──────────────────────────────────────────────
#  Admin  (erbt von Mitarbeiter)
# ──────────────────────────────────────────────

class Admin(Mitarbeiter):
    BÜROTAGE = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag"]
    BÜRO_START = 7
    BÜRO_ENDE = 17

    def __init__(self, firmenname: str, gehalt: float, einstellungsart: str,
                 laptop_seriennummer: str = ""):
        super().__init__(firmenname, "Admin", gehalt, einstellungsart)
        self.lizenz_liste: list[str] = []
        self.laptop_seriennummer = laptop_seriennummer

    def stunden_eintragen(self, tag: str, uhrzeit: int):
        """Admin: Mo–Fr, 7–17 Uhr."""
        if tag not in self.BÜROTAGE:
            print(f"[Admin] Stunden ablehnt: '{tag}' ist kein Bürotag (nur Mo–Fr).")
            return
        if not (self.BÜRO_START <= uhrzeit < self.BÜRO_ENDE):
            print(f"[Admin] Stunden ablehnt: {uhrzeit}:00 Uhr liegt außerhalb der Bürozeiten (7–17).")
            return
        eintrag = f"Stunden: {tag} {uhrzeit}:00 Uhr"
        self.kalender.append(eintrag)
        print(f"[Admin] Stunden eingetragen: {tag} {uhrzeit}:00 Uhr")

    def kalender_einsehen(self):
        """Admin: Sieht nur Bürotage im Kalender."""
        gefiltert = [e for e in self.kalender if any(t in e for t in self.BÜROTAGE)]
        print(f"[Admin] Kalender (nur Bürotage): {gefiltert if gefiltert else '(leer)'}")

    def ticket_erstellen(self, betreff: str):
        print(f"[Admin] Ticket erstellt: '{betreff}' | Laptop S/N: {self.laptop_seriennummer}")


# ──────────────────────────────────────────────
#  HR  (erbt von Mitarbeiter)
# ──────────────────────────────────────────────

class HR(Mitarbeiter):
    def __init__(self, firmenname: str, gehalt: float, einstellungsart: str):
        super().__init__(firmenname, "HR", gehalt, einstellungsart)
        self.problem_counter: int = 0

    def stunden_eintragen(self, tag: str, uhrzeit: int):
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


# ──────────────────────────────────────────────
#  Main – Demo
# ──────────────────────────────────────────────

def main():
    FIRMA = "Mustermann GmbH"

    print("=" * 55)
    print(f"  {FIRMA} – Mitarbeiterübersicht")
    print("=" * 55)

    alice = Sales(FIRMA, gehalt=3800.0, einstellungsart="Vollzeit", provisions_prozent=7.5)
    bob   = Admin(FIRMA, gehalt=3200.0, einstellungsart="Vollzeit",  laptop_seriennummer="SN-00421")
    carla = HR(FIRMA,    gehalt=3000.0, einstellungsart="Teilzeit")
    dave  = Sales(FIRMA, gehalt=2900.0, einstellungsart="Minijob",   provisions_prozent=4.0)

    mitarbeiter = [alice, bob, carla, dave]
    for m in mitarbeiter:
        print(m)

    # ── Polymorphismus: gleiche Methode, unterschiedliches Verhalten ──
    print("\n--- Stunden eintragen (Polymorphismus) ---")
    alice.stunden_eintragen("Samstag", 20)   # Sales: erlaubt
    bob.stunden_eintragen("Samstag", 10)     # Admin: abgelehnt (kein Bürotag)
    bob.stunden_eintragen("Montag",   6)     # Admin: abgelehnt (zu früh)
    bob.stunden_eintragen("Montag",  9)      # Admin: ok
    carla.stunden_eintragen("Montag", 9)     # HR: Problem-Counter
    dave.stunden_eintragen("Sonntag", 15)    # Sales: erlaubt

    print("\n--- Kalender einsehen (Polymorphismus) ---")
    alice.kalender_einsehen()   # alles
    bob.kalender_einsehen()     # nur Bürotage
    carla.kalender_einsehen()   # Problem-Counter

    print("\n--- Urlaub buchen ---")
    alice.urlaub_buchen("2026-07-14")
    bob.urlaub_buchen("2026-07-21")
    carla.urlaub_buchen("2026-08-01")   # HR: Problem-Counter

    print("\n--- Rollenspezifische Aktionen ---")
    alice.auftrag_erstellen("Kunde AG", 15000.0)
    dave.auftrag_erstellen("Startup GmbH", 4200.0)
    bob.ticket_erstellen("Drucker druckt nicht")

    print(f"\n[HR] Problem-Counter gesamt: {carla.problem_counter}")
    print("\nFertig.")


if __name__ == "__main__":
    main()
