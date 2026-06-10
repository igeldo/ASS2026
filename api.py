"""
Modul 3 – REST-API auf Basis des OOP-Modells (Vererbung & Polymorphismus)
Startet lokal auf http://localhost:8080
Docs:  http://localhost:8080/docs
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Literal
import uvicorn

app = FastAPI(title="Mustermann GmbH API", version="1.0")

FIRMA = "Mustermann GmbH"


# ──────────────────────────────────────────────
#  OOP-Modell  (angepasst: stunden_gesamt-Zähler)
# ──────────────────────────────────────────────

class Unternehmen:
    def __init__(self, name: str):
        self.name = name
        self.kalender: list[str] = []


class Mitarbeiter(Unternehmen):
    def __init__(self, vorname: str, firmenname: str, rolle: str,
                 gehalt: float, einstellungsart: str):
        super().__init__(firmenname)
        self.vorname = vorname
        self.rolle = rolle
        self.gehalt = gehalt
        self.einstellungsart = einstellungsart
        self.stunden_gesamt: float = 0.0   # ← neu: numerisch für die API

    def stunden_eintragen(self, tag: str, uhrzeit: int, dauer: float = 1.0):
        self.stunden_gesamt += dauer
        eintrag = f"Stunden: {tag} {uhrzeit}:00 Uhr ({dauer}h)"
        self.kalender.append(eintrag)
        print(f"[{self.rolle}] Stunden eingetragen: {tag} {uhrzeit}:00 Uhr, {dauer}h")

    def kalender_einsehen(self):
        print(f"[{self.rolle}] Kalender: {self.kalender or '(leer)'}")

    def urlaub_buchen(self, datum: str):
        self.kalender.append(f"Urlaub am {datum}")
        print(f"[{self.rolle}] Urlaub gebucht: {datum}")

    def to_dict(self) -> dict:
        return {
            "vorname": self.vorname,
            "firma": self.name,
            "rolle": self.rolle,
            "gehalt": self.gehalt,
            "einstellungsart": self.einstellungsart,
            "stunden_gesamt": self.stunden_gesamt,
        }


class Sales(Mitarbeiter):
    WOCHENTAGE = ["Montag", "Dienstag", "Mittwoch", "Donnerstag",
                  "Freitag", "Samstag", "Sonntag"]

    def __init__(self, vorname: str, firmenname: str, gehalt: float,
                 einstellungsart: str, provisions_prozent: float = 5.0):
        super().__init__(vorname, firmenname, "Sales", gehalt, einstellungsart)
        self.provisions_prozent = provisions_prozent
        self.verkäufe: list[str] = []

    def stunden_eintragen(self, tag: str, uhrzeit: int, dauer: float = 1.0):
        if tag not in self.WOCHENTAGE:
            print(f"[Sales] Ungültiger Tag: {tag}")
            return
        self.stunden_gesamt += dauer
        self.kalender.append(f"Stunden: {tag} {uhrzeit}:00 Uhr ({dauer}h)")
        print(f"[Sales] Stunden eingetragen: {tag} {uhrzeit}:00 Uhr ({dauer}h, auch Wochenende)")

    def to_dict(self) -> dict:
        d = super().to_dict()
        d["provisions_prozent"] = self.provisions_prozent
        d["anzahl_verkäufe"] = len(self.verkäufe)
        return d


class Admin(Mitarbeiter):
    BÜROTAGE  = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag"]
    BÜRO_START = 7
    BÜRO_ENDE  = 17

    def __init__(self, vorname: str, firmenname: str, gehalt: float,
                 einstellungsart: str, laptop_seriennummer: str = ""):
        super().__init__(vorname, firmenname, "Admin", gehalt, einstellungsart)
        self.lizenz_liste: list[str] = []
        self.laptop_seriennummer = laptop_seriennummer

    def stunden_eintragen(self, tag: str, uhrzeit: int, dauer: float = 1.0):
        if tag not in self.BÜROTAGE:
            print(f"[Admin] Abgelehnt: '{tag}' ist kein Bürotag.")
            return
        if not (self.BÜRO_START <= uhrzeit < self.BÜRO_ENDE):
            print(f"[Admin] Abgelehnt: {uhrzeit}:00 Uhr außerhalb Bürozeiten (7–17).")
            return
        self.stunden_gesamt += dauer
        self.kalender.append(f"Stunden: {tag} {uhrzeit}:00 Uhr ({dauer}h)")
        print(f"[Admin] Stunden eingetragen: {tag} {uhrzeit}:00 Uhr ({dauer}h)")

    def to_dict(self) -> dict:
        d = super().to_dict()
        d["laptop_seriennummer"] = self.laptop_seriennummer
        return d


class HR(Mitarbeiter):
    def __init__(self, vorname: str, firmenname: str, gehalt: float, einstellungsart: str):
        super().__init__(vorname, firmenname, "HR", gehalt, einstellungsart)
        self.problem_counter: int = 0

    def stunden_eintragen(self, tag: str, uhrzeit: int, dauer: float = 1.0):
        self.problem_counter += 1
        print(f"[HR] Stunden eintragen? Problem Nr. {self.problem_counter}.")

    def to_dict(self) -> dict:
        d = super().to_dict()
        d["problem_counter"] = self.problem_counter
        return d


# ──────────────────────────────────────────────
#  In-Memory-Datenspeicher
# ──────────────────────────────────────────────

db: list[Mitarbeiter] = [
    Sales ("Alice",  FIRMA, gehalt=3800.0, einstellungsart="Vollzeit",  provisions_prozent=7.5),
    Admin ("Bob",    FIRMA, gehalt=3200.0, einstellungsart="Vollzeit",  laptop_seriennummer="SN-00421"),
    HR    ("Carla",  FIRMA, gehalt=3000.0, einstellungsart="Teilzeit"),
    Sales ("Dave",   FIRMA, gehalt=2900.0, einstellungsart="Minijob",   provisions_prozent=4.0),
]

# Etwas Demomaterial: Stunden vorab eintragen
db[0].stunden_eintragen("Samstag",  10, 6.0)
db[0].stunden_eintragen("Montag",    9, 8.0)
db[1].stunden_eintragen("Montag",    8, 8.0)
db[1].stunden_eintragen("Dienstag",  9, 7.5)
db[2].stunden_eintragen("Montag",    9, 8.0)   # HR: Problem-Counter
db[3].stunden_eintragen("Freitag",  14, 5.0)


# ──────────────────────────────────────────────
#  Pydantic-Schemas für POST /mitarbeiter
# ──────────────────────────────────────────────

class MitarbeiterCreate(BaseModel):
    vorname: str
    rolle: Literal["Sales", "Admin", "HR"]
    gehalt: float
    einstellungsart: str
    provisions_prozent: float = 5.0
    laptop_seriennummer: str = ""


# ──────────────────────────────────────────────
#  API-Endpunkte
# ──────────────────────────────────────────────

@app.get("/mitarbeiter", summary="Alle Mitarbeiter anzeigen")
def alle_mitarbeiter():
    """Gibt eine Liste aller Mitarbeiter mit ihren Stammdaten zurück."""
    return {"mitarbeiter": [m.to_dict() for m in db]}


@app.get("/mitarbeiter/rollen", summary="Rollenübersicht")
def rollen_übersicht():
    """Zeigt, welcher Mitarbeiter welche Rolle belegt."""
    return {
        "rollen": [
            {"vorname": m.vorname, "rolle": m.rolle} for m in db
        ]
    }


@app.get("/mitarbeiter/anzahl", summary="Mitarbeiteranzahl")
def mitarbeiter_anzahl():
    """Gibt die Gesamtzahl der angelegten Mitarbeiter zurück."""
    return {"anzahl": len(db)}


@app.get("/mitarbeiter/stunden", summary="Geleistete Stunden gesamt")
def geleistete_stunden():
    """Summiert alle bisher eingetragenen Arbeitsstunden über alle Mitarbeiter."""
    gesamt = sum(m.stunden_gesamt for m in db)
    detail = [{"vorname": m.vorname, "rolle": m.rolle, "stunden": m.stunden_gesamt}
              for m in db]
    return {"gesamt_stunden": gesamt, "detail": detail}


@app.post("/mitarbeiter", summary="Neuen Mitarbeiter anlegen", status_code=201)
def mitarbeiter_anlegen(data: MitarbeiterCreate):
    """Legt einen neuen Mitarbeiter an und speichert ihn im Arbeitsspeicher."""
    match data.rolle:
        case "Sales":
            neu = Sales(data.vorname, FIRMA, data.gehalt, data.einstellungsart,
                        data.provisions_prozent)
        case "Admin":
            neu = Admin(data.vorname, FIRMA, data.gehalt, data.einstellungsart,
                        data.laptop_seriennummer)
        case "HR":
            neu = HR(data.vorname, FIRMA, data.gehalt, data.einstellungsart)
        case _:
            raise HTTPException(status_code=400, detail="Unbekannte Rolle")
    db.append(neu)
    return {"message": f"Mitarbeiter '{neu.vorname}' ({neu.rolle}) angelegt.", "data": neu.to_dict()}


# ──────────────────────────────────────────────
#  Server starten
# ──────────────────────────────────────────────

if __name__ == "__main__":
    print(f"API läuft auf http://localhost:8080")
    print(f"Swagger-Docs: http://localhost:8080/docs")
    uvicorn.run("api:app", host="0.0.0.0", port=8080, reload=True)
