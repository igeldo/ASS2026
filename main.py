"""
Zentrale Steuerungsdatei – Modul 3: Vererbung & Polymorphismus

Ablauf:
  1. OOP-Demo wird im Terminal ausgegeben (Polymorphismus live beobachten)
  2. Die erzeugten Objekte werden in die API-Datenbank übertragen
  3. Der FastAPI-Server startet auf http://localhost:8080
     -> Swagger-Docs: http://localhost:8080/docs
"""

import uvicorn

from sales import Sales
from admin import Admin
from hr    import HR
import api  # API-Modul – db und app werden hier importiert


FIRMENNAME = "Mustermann GmbH"
HOST       = "0.0.0.0"
PORT       = 8080


# ── OOP-Demo ──────────────────────────────────────────────────────────

def mitarbeiter_erstellen() -> list:
    return [
        Sales("Alice", FIRMENNAME, gehalt=3800.0, einstellungsart="Vollzeit",  provisions_prozent=7.5),
        Admin("Bob",   FIRMENNAME, gehalt=3200.0, einstellungsart="Vollzeit",  laptop_seriennummer="SN-00421"),
        HR(  "Carla",  FIRMENNAME, gehalt=3000.0, einstellungsart="Teilzeit"),
        Sales("Dave",  FIRMENNAME, gehalt=2900.0, einstellungsart="Minijob",   provisions_prozent=4.0),
    ]


def übersicht_ausgeben(belegschaft: list):
    print("\n" + "=" * 55)
    print("  Mitarbeiterübersicht – Mustermann GmbH")
    print("=" * 55)
    for m in belegschaft:
        print(m)


def demo_polymorphismus_stunden(belegschaft: list):
    print("\n--- Stunden eintragen (Polymorphismus) ---")
    alice, bob, carla, dave = belegschaft
    alice.stunden_eintragen("Samstag", 20, 6.0)   # Sales: erlaubt
    bob.stunden_eintragen("Samstag",   10, 8.0)   # Admin: abgelehnt (Wochenende)
    bob.stunden_eintragen("Montag",     6, 8.0)   # Admin: abgelehnt (zu früh)
    bob.stunden_eintragen("Montag",     9, 8.0)   # Admin: ok
    carla.stunden_eintragen("Montag",   9, 8.0)   # HR:    Problem-Counter
    dave.stunden_eintragen("Sonntag",  15, 5.0)   # Sales: erlaubt


def demo_polymorphismus_kalender(belegschaft: list):
    print("\n--- Kalender einsehen (Polymorphismus) ---")
    alice, bob, carla, _ = belegschaft
    alice.kalender_einsehen()
    bob.kalender_einsehen()
    carla.kalender_einsehen()


def demo_urlaub(belegschaft: list):
    print("\n--- Urlaub buchen ---")
    alice, bob, carla, _ = belegschaft
    alice.urlaub_buchen("2026-07-14")
    bob.urlaub_buchen("2026-07-21")
    carla.urlaub_buchen("2026-08-01")


def demo_rollenspezifisch(belegschaft: list):
    print("\n--- Rollenspezifische Aktionen ---")
    alice, bob, _, dave = belegschaft
    alice.auftrag_erstellen("Kunde AG", 15_000.0)
    dave.auftrag_erstellen("Startup GmbH", 4_200.0)
    bob.ticket_erstellen("Drucker druckt nicht")


def abschlussbericht(belegschaft: list):
    print("\n--- Abschlussbericht ---")
    for m in belegschaft:
        if hasattr(m, "problem_counter"):
            print(f"  [{m.vorname}] Problem-Counter: {m.problem_counter}")
        else:
            print(f"  [{m.vorname}] Geleistete Stunden: {m.stunden_gesamt}h")


# ── Hauptprogramm ─────────────────────────────────────────────────────

def main():
    # 1. OOP-Demo
    belegschaft = mitarbeiter_erstellen()
    übersicht_ausgeben(belegschaft)
    demo_polymorphismus_stunden(belegschaft)
    demo_polymorphismus_kalender(belegschaft)
    demo_urlaub(belegschaft)
    demo_rollenspezifisch(belegschaft)
    abschlussbericht(belegschaft)

    # 2. Daten in die API-Datenbank übertragen
    api.db.extend(belegschaft)

    # 3. Webserver starten (blockiert – läuft bis Strg+C)
    print("\n" + "=" * 55)
    print(f"  REST-API startet auf http://localhost:{PORT}")
    print(f"  Swagger-Docs:        http://localhost:{PORT}/docs")
    print("  Beenden mit Strg+C")
    print("=" * 55 + "\n")
    uvicorn.run(api.app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()
