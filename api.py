"""
REST-API – Modul 3
Importiert die OOP-Klassen aus den Modulen und stellt sie per HTTP bereit.
Startet nicht eigenständig – wird von main.py gestartet.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Literal

from sales import Sales
from admin import Admin
from hr    import HR
from mitarbeiter import Mitarbeiter

app = FastAPI(
    title="Mustermann GmbH API",
    description="REST-Schnittstelle zum OOP-Modell (Vererbung & Polymorphismus)",
    version="1.0",
)

FIRMA = "Mustermann GmbH"

# ── In-Memory-Datenbank (wird von main.py befüllt) ────────────────────
db: list[Mitarbeiter] = []


# ── Pydantic-Schema für POST ──────────────────────────────────────────

class MitarbeiterCreate(BaseModel):
    vorname: str
    rolle: Literal["Sales", "Admin", "HR"]
    gehalt: float
    einstellungsart: str
    provisions_prozent: float = 5.0
    laptop_seriennummer: str = ""


# ── Endpunkte ─────────────────────────────────────────────────────────

@app.get("/mitarbeiter", summary="Alle Mitarbeiter anzeigen")
def alle_mitarbeiter():
    """Gibt eine Liste aller Mitarbeiter mit ihren Stammdaten zurück."""
    return {"mitarbeiter": [m.to_dict() for m in db]}


@app.get("/mitarbeiter/rollen", summary="Rollenübersicht")
def rollen_übersicht():
    """Zeigt, welcher Mitarbeiter welche Rolle belegt."""
    return {"rollen": [{"vorname": m.vorname, "rolle": m.rolle} for m in db]}


@app.get("/mitarbeiter/anzahl", summary="Mitarbeiteranzahl")
def mitarbeiter_anzahl():
    """Gibt die Gesamtzahl der angelegten Mitarbeiter zurück."""
    return {"anzahl": len(db)}


@app.get("/mitarbeiter/stunden", summary="Geleistete Stunden gesamt")
def geleistete_stunden():
    """Summiert alle eingetragenen Arbeitsstunden über alle Mitarbeiter."""
    gesamt = sum(m.stunden_gesamt for m in db)
    detail = [
        {"vorname": m.vorname, "rolle": m.rolle, "stunden": m.stunden_gesamt}
        for m in db
    ]
    return {"gesamt_stunden": gesamt, "detail": detail}


@app.post("/mitarbeiter", summary="Neuen Mitarbeiter anlegen", status_code=201)
def mitarbeiter_anlegen(data: MitarbeiterCreate):
    """Legt einen neuen Mitarbeiter an und speichert ihn im Arbeitsspeicher."""
    match data.rolle:
        case "Sales":
            neu = Sales(data.vorname, FIRMA, data.gehalt,
                        data.einstellungsart, data.provisions_prozent)
        case "Admin":
            neu = Admin(data.vorname, FIRMA, data.gehalt,
                        data.einstellungsart, data.laptop_seriennummer)
        case "HR":
            neu = HR(data.vorname, FIRMA, data.gehalt, data.einstellungsart)
        case _:
            raise HTTPException(status_code=400, detail="Unbekannte Rolle")
    db.append(neu)
    return {"message": f"'{neu.vorname}' ({neu.rolle}) angelegt.", "data": neu.to_dict()}
