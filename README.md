# Modul 3 – Vererbung & Polymorphismus

Dieses Modul demonstriert die zwei zentralen OOP-Konzepte **Vererbung** und **Polymorphismus** anhand einer kleinen Unternehmensanwendung mit REST-API.

---

## Was das Programm macht

Das Programm modelliert die Struktur eines Unternehmens mit verschiedenen Mitarbeiterrollen.
Es gibt eine Basisklasse `Unternehmen`, von der eine `Mitarbeiter`-Klasse erbt. Davon wiederum erben drei spezialisierte Rollen: `Sales`, `Admin` und `HR`. Jede Rolle verhält sich bei gemeinsamen Aktionen unterschiedlich.

Zusätzlich läuft eine REST-API (`api.py`) auf Port 8080, über die Mitarbeiterdaten abgerufen und neue Mitarbeiter angelegt werden können. Die Daten werden im Arbeitsspeicher gehalten (In-Memory).

---

## Vererbung

Vererbung bedeutet, dass eine Kindklasse die Eigenschaften und Methoden einer Elternklasse übernimmt und bei Bedarf erweitert.

```
Unternehmen
    └── Mitarbeiter          (erbt: name, kalender)
            ├── Sales        (ergänzt: provisions_prozent, verkäufe, auftrag_erstellen)
            ├── Admin        (ergänzt: lizenz_liste, laptop_seriennummer, ticket_erstellen)
            └── HR           (ergänzt: problem_counter)
```

Jeder `Mitarbeiter` kennt automatisch den Firmennamen und den Kalender, weil er von `Unternehmen` erbt.
`Sales`, `Admin` und `HR` kennen zusätzlich Rolle, Gehalt und Einstellungsart, weil sie von `Mitarbeiter` erben.
Rollenspezifische Attribute und Methoden (z. B. `auftrag_erstellen()` bei Sales) werden in der jeweiligen Kindklasse hinzugefügt.

---

## Polymorphismus

Polymorphismus bedeutet, dass dieselbe Methode bei verschiedenen Klassen unterschiedlich ausgeführt wird.

In diesem Projekt sind die Methoden `stunden_eintragen()` und `kalender_einsehen()` in jeder Rolle überschrieben:

| Methode | Sales | Admin | HR |
|---|---|---|---|
| `stunden_eintragen()` | Mo–So, alle Uhrzeiten erlaubt | Mo–Fr, nur 7–17 Uhr | Erhöht `problem_counter`, keine Stunden |
| `kalender_einsehen()` | Zeigt den vollständigen Kalender | Zeigt nur Bürotage | Erhöht `problem_counter` |
| `urlaub_buchen()` | Standard | Standard | Erhöht `problem_counter`, gibt Hinweis auf Formular HR-42b |

Der Aufruf `mitarbeiter.stunden_eintragen("Samstag", 20)` führt bei Sales zu einer Eintragung, bei Admin zu einer Ablehnung und bei HR zu einer Zählererhöhung — obwohl der Aufruf identisch ist. Das ist Polymorphismus in der Praxis.

---

## Projektstruktur

```
ASS2026/
├── modul3_vererbung.py   # OOP-Modell mit Demo-Ausgabe (Standalone)
├── api.py                # REST-API auf Basis des OOP-Modells
└── README.md
```

---

## REST-API

Der Server startet mit:

```bash
python api.py
```

Er läuft auf `http://localhost:8080`. Die interaktive Swagger-Dokumentation ist erreichbar unter `http://localhost:8080/docs`.

### Endpunkte

| Methode | Pfad | Beschreibung |
|---|---|---|
| `GET` | `/mitarbeiter` | Alle Mitarbeiter mit Stammdaten |
| `GET` | `/mitarbeiter/rollen` | Welcher Mitarbeiter hat welche Rolle |
| `GET` | `/mitarbeiter/anzahl` | Gesamtzahl der Mitarbeiter |
| `GET` | `/mitarbeiter/stunden` | Summe und Aufschlüsselung aller geleisteten Stunden |
| `POST` | `/mitarbeiter` | Neuen Mitarbeiter anlegen |

### Beispiel POST-Request

```json
POST /mitarbeiter
{
  "vorname": "Eva",
  "rolle": "HR",
  "gehalt": 3100,
  "einstellungsart": "Vollzeit"
}
```

---

## Installation & Start

```bash
pip install fastapi uvicorn

# OOP-Demo (ohne API)
python modul3_vererbung.py

# REST-API starten
python api.py
```

---

## Verwendete Prompts

Die folgenden Prompts wurden während der Entwicklung eingesetzt. Sie zeigen, wie die Anforderungen schrittweise von der Idee bis zur fertigen Anwendung formuliert wurden.

---

**Prompt 1 – OOP-Modell (Gemini, Anforderungsformulierung):**

> Erstelle ein Python-Skript, das Vererbung und Polymorphismus demonstriert. Grundlage ist ein Unternehmen mit einem Namen und einem Kalender. Ein Mitarbeiter erbt den Unternehmensnamen und den Kalender und hat zusätzlich eine Rolle, ein Gehalt und eine Einstellungsart. Es gibt drei Rollen: Sales, Admin und HR. Sales hat ein Provisionsprozent, eine Verkaufsanzahl und eine Verkaufsliste sowie die Methode `auftrag_erstellen()`. Admin hat eine Lizenzliste, eine Laptop-Seriennummer und die Methode `ticket_erstellen()`. HR hat nur einen Problem-Counter. Die Methoden `stunden_eintragen()` und `kalender_einsehen()` sollen je nach Rolle unterschiedlich funktionieren: Sales darf Stunden von Montag bis Sonntag zu jeder Uhrzeit eintragen und den gesamten Kalender einsehen. Admin darf nur von Montag bis Freitag zwischen 7 und 17 Uhr Stunden eintragen und den Kalender ebenfalls nur für Bürotage einsehen. Bei HR erhöht jede dieser Aktionen nur den Problem-Counter. `urlaub_buchen()` funktioniert bei Sales und Admin gleich. Alles soll in einer einzigen Datei stehen und nicht mehr als 300–400 Zeilen umfassen.

---

**Prompt 2 – REST-API (Claude Code, Implementierung):**

> Baue mir basierend auf unserem bestehenden OOP-Code (Unternehmen und Mitarbeiter) eine kleine, lokale REST-API. Nutze dafür ein leichtgewichtiges Framework wie FastAPI und lass den Server lokal auf Port 8080 laufen. Die Daten können vorerst einfach im Arbeitsspeicher (In-Memory) gehalten werden, eine Datenbank brauche ich noch nicht. Bitte erstelle folgende API-Endpunkte: einen Endpunkt, der alle Mitarbeiter zurückgibt; einen Endpunkt für die Rollenübersicht; einen Endpunkt für die reine Mitarbeiteranzahl; sowie einen Endpunkt, der die Gesamtzahl aller bisher eingetragenen Arbeitsstunden berechnet und ausgibt. Falls nötig, passe `stunden_eintragen()` leicht an, damit die Stunden nicht nur als Text im Kalender landen, sondern auch als Zahl berechenbar gespeichert werden.

---

**Prompt 3 – README (Claude Code, Dokumentation):**

> Erstelle eine README-Datei für das Projekt. Gehe darauf ein, inwiefern Polymorphismus und Vererbung umgesetzt wurden und was das Programm macht. Am Ende sollen die verwendeten Werkzeuge aufgeführt werden: Claude Code für die Code-Generierung, Gemini für die Prompt-Umschreibung sowie Python, FastAPI und Uvicorn für die Entwicklung.

---

## Verwendete Werkzeuge

| Werkzeug | Zweck |
|---|---|
| **Claude Code** | Code-Generierung und Implementierung |
| **Google Gemini** | Prompt-Umschreibung und Anforderungsformulierung |
| **Python 3.12** | Programmiersprache |
| **FastAPI** | REST-API-Framework |
| **Uvicorn** | ASGI-Server zum Ausführen der FastAPI-Anwendung |
| **Pydantic** | Datenschemas und Validierung (wird von FastAPI verwendet) |
