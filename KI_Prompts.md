# KI_Prompts.md

Nachschlagewerk fuer alle Prompts, die im Rahmen dieses Projekts eingesetzt werden:
Laufzeit-Prompts (an das lokale Ollama-Modell) sowie ein laufendes Protokoll
der Entwicklungs-Prompts, die wir gegenueber dem KI-Coding-Assistenten
verwendet haben.

---

## 1. Laufzeit-Prompts (Ollama/Gemini / Rechnungsextraktion)

### 1.1 Rechnungsfeld-Extraktion aus OCR-Text

- **Zweck:** Wandelt den per Tesseract/PyMuPDF extrahierten Freitext einer Rechnung
  in ein festes JSON-Schema um (Lieferant, Betraege, Datum, IBAN, ...).
- **Ort im Code:** [`controllers/ai_service.py`](controllers/ai_service.py) &mdash;
  `BaseInvoiceAIProcessor._build_prompt()` (gemeinsam fuer beide Backends).
- **Backends:** `InvoiceAIProcessor` (lokales Ollama, Modell `qwen3:8b`,
  `format: "json"`) oder `GeminiAIProcessor` (Gemini-API, Modell
  `gemini-flash-latest`, `response_mime_type: "application/json"`). Ueber
  `get_default_ai_processor()` wird immer zuerst Ollama versucht; nur wenn
  `GEMINI_API_KEY` gesetzt ist UND Ollama nicht erreichbar ist/fehlschlaegt,
  greift automatisch `FallbackAIProcessor` auf Gemini zurueck.
- **Prompt-Vorlage (identisch fuer beide Backends):**

  ```
  You are an invoice extraction API.

  Return ONLY valid JSON. Use null for anything you cannot find in the text.
  Do not guess values that are not present in the text.

  Fields:
  {
      "invoice_number": null,
      "invoice_date": null,
      "due_date": null,
      "currency": null,

      "seller_name": null,
      "seller_vat_id": null,
      "seller_street": null,
      "seller_postcode": null,
      "seller_city": null,
      "seller_country": null,

      "buyer_name": null,
      "buyer_vat_id": null,
      "buyer_street": null,
      "buyer_postcode": null,
      "buyer_city": null,
      "buyer_country": null,

      "iban": null,
      "bic": null,
      "payment_terms": null,

      "net_total": null,
      "gross_total": null,
      "vat_amount": null,
      "vat_rate": null,

      "line_items": [
          {"name": null, "quantity": null, "unit_price": null, "line_total": null}
      ]
  }

  Text:
  {text}
  ```

- **Anmerkung:** Nachbearbeitung (Zahlenformat, VAT, Datum, Trimming) passiert
  bewusst nicht im Prompt, sondern deterministisch in
  [`controllers/invoice_parser.py`](controllers/invoice_parser.py). Das erweiterte
  Schema (Adressen, BIC, Zahlungsbedingungen, Positionen) existiert, damit
  [`controllers/invoice_mapper.py`](controllers/invoice_mapper.py) daraus
  automatisch ein vollstaendiges `GermanInvoice` bauen kann, siehe Prompt #27
  und #28 weiter unten.

---

## 2. Entwicklungs-Gespraechsverlauf (Prompt/Ergebnis-Log)

Kurzprotokoll jedes Prompts an den KI-Coding-Assistenten (Claude Code) in
diesem Projekt, chronologisch, jeweils mit dem Ergebnis. Wird bei jedem
neuen Prompt fortgeschrieben.

**Prompt #1:** Rolle als Softwarearchitekt; `main.py` und den KI-Extraktor
nach OOP, Logging, gezielter Fehlerbehandlung, HTML-Test-UI, PyTest und
`KI_Prompts.md` refaktorieren &mdash; Start mit `main.py` + AI-Service.
**Ergebnis #1:** `controllers/ai_service.py` &rarr; `InvoiceAIProcessor` (mit
`AIConnectionError`/`AIResponseError`), `invoice_parser.py` angepasst,
`main.py` mit zentralem `logging` + spezifischem Exception-Handling + neuer
`GET /ui`-Route (`views/upload_page.py`), `KI_Prompts.md` angelegt.

**Prompt #2:** Rueckfrage, ob schon etwas testbar ist, plus Bitte, die
Unterhaltung laufend in einer `.md` zu dokumentieren; Zustimmung, mit den
restlichen Services und Tests fortzufahren.
**Ergebnis #2:** `cii_generator.py`, `ocr_service.py`, `validator.py`,
`xsd_validator.py`, `cii_parser.py`, `datum_service.py` in Klassen
(`CIIBuilder`, `OCRProcessor`, `EN16931Validator`, `CIIXsdValidator`,
`CIIXmlParser`, `DateNormalizer`) refaktoriert; `main.py` nutzt diese
Instanzen direkt. PyTest-Suite unter `tests/` (40 Tests) erstellt.
`KI_Prompts.md` und `README.md` aktualisiert.

**Prompt #3:** Fehlermeldung `uvicorn` in PowerShell nicht gefunden.
**Ergebnis #3:** Ursache erklaert (Scripts-Ordner nicht im PATH); Fix ueber
`python -m uvicorn main:app --reload`.

**Prompt #4:** Bitte, diesen PATH-Hinweis in die README aufzunehmen.
**Ergebnis #4:** README um Troubleshooting-Absatz ergaenzt.

**Prompt #5:** Neuer Fehler `Could not import module main`.
**Ergebnis #5:** Ursache war falsches Arbeitsverzeichnis; Hinweis, zuerst
ins Projektverzeichnis zu wechseln.

**Prompt #6:** Frage, ob der Befehl unabhaengig vom Arbeitsverzeichnis
zuverlaessig auf das Projekt zeigen kann.
**Ergebnis #6:** `--app-dir`-Flag von uvicorn vorgeschlagen; Angebot eines
Start-Skripts.

**Prompt #7:** Zustimmung, aber mit der Anforderung, dass es auf jedem
Computer/Pfad funktioniert (nicht nur auf diesem Rechner).
**Ergebnis #7:** `run.ps1` erstellt (loest eigenen Pfad ueber `$PSScriptRoot`
auf); erfolgreich aus einem fremden Arbeitsverzeichnis getestet.

**Prompt #8:** Bitte, README entsprechend zu aktualisieren, Unnoetiges
weglassen; Ziel: "einfach auf Run druecken".
**Ergebnis #8:** README-Setup auf `.\run.ps1` (Windows) /
`python -m uvicorn ...` (macOS/Linux) reduziert.

**Prompt #9:** Screenshot der PyCharm-Markdown-Vorschau &mdash; `run.ps1`
laesst sich dort nicht komfortabel per Klick starten; Frage nach einer
reinen Python-Loesung.
**Ergebnis #9:** `run.py` erstellt (`uvicorn.run(..., app_dir=...)`, loest
Projektpfad ueber `Path(__file__)` auf); getestet, README auf
`python run.py` umgestellt, `run.ps1` geloescht.

**Prompt #10:** Erfolgreiche JSON-Antwort von `/` als Bestaetigung
eingefuegt.
**Ergebnis #10:** Naechste Testschritte vorgeschlagen (`/ui`, `/docs`,
`/health`).

**Prompt #11:** Bitte, `/ui` auch in die README aufzunehmen und die
Dokumentation als gefuehrte Einleitung/Durchfuehrung zu gestalten.
**Ergebnis #11:** README-Abschnitt zu einem nummerierten "Quickstart"
umgebaut (Install &rarr; Tesseract/Ollama optional &rarr; `python run.py`
&rarr; `/ui` erklaert &rarr; `/docs`).

**Prompt #12:** `pytest`-PATH-Fehler; Bitte, `requirements-dev.txt`
abzuschaffen (alles in eine Datei), generell Dateien/Code zu minimieren,
und kuenftig jeden Prompt als "Prompt #N / Ergebnis #N" zusammenzufassen.
**Ergebnis #12:** `pytest`/`httpx` in `requirements.txt` zusammengefuehrt,
`requirements-dev.txt` geloescht, README auf eine Install-Zeile +
`python -m pytest -q` reduziert; dieses Prompt/Ergebnis-Log eingefuehrt
(ersetzt die vorherigen, ausfuehrlicheren Abschnitte 2.1-2.3).

**Prompt #13:** `python run.py` laeuft, aber es fehlt eine Uebersicht der
anderen Adressen (`/ui`, `/docs`, `/health`) beim Start.
**Ergebnis #13:** `run.py` gibt vor dem Serverstart die drei URLs aus
(`flush=True`, da sonst im gepufferten stdout haengen bleibt).

**Prompt #14:** "Internal server error" beim PNG-Upload ueber `/ui` &mdash;
Ursachensuche.
**Ergebnis #14:** Ursache: Tesseract nicht installiert &rarr; unbehandelte
`TesseractNotFoundError` &rarr; genereller 500er. `ocr_service.py` faengt
Tesseract-Fehler jetzt gezielt ab (400 mit klarer Meldung statt 500).
Danach folgte eine reine Installations-Begleitung (Komponentenauswahl,
Zielpfad, Startmenue) ohne Code-Aenderung.

**Prompt #15:** Direkten Tesseract-Windows-Installer-Link in die README
aufnehmen.
**Ergebnis #15:** README enthaelt jetzt den direkten Installer-Link, Hinweis
auf German-Language-Data, "Add to PATH" und `tesseract --version` zur
Verifikation.

**Prompt #16:** Fehler "Tesseract OCR is not installed or not on PATH"
besteht nach der Installation weiterhin.
**Ergebnis #16:** Ursache: Installer hat PATH nicht gesetzt, obwohl
`tesseract.exe` korrekt installiert ist. `ocr_service.py` erkennt jetzt
automatisch Standard-Windows-Installationspfade als Fallback.

**Prompt #17:** Fehler "AI service unavailable" (Ollama laeuft nicht);
Frage, ob stattdessen die kostenlose Gemini-API genutzt werden kann.
**Ergebnis #17:** `ai_service.py` um `GeminiAIProcessor` erweitert
(gemeinsame Basisklasse `BaseInvoiceAIProcessor` mit `InvoiceAIProcessor`
fuer den Prompt-Aufbau). `get_default_ai_processor()` waehlt automatisch
Gemini, falls `GEMINI_API_KEY` gesetzt ist, sonst Ollama &mdash; keine
Codeaenderung fuer den Wechsel noetig, nur die Env-Variable setzen. README
und Tests entsprechend ergaenzt (45/45 gruen).

**Prompt #18:** Nachfrage zum gesetzten `GEMINI_API_KEY` in PowerShell,
danach die Bitte, das so zu ergaenzen, dass bei fehlendem Ollama automatisch
der API-Key genutzt wird (statt es manuell umschalten zu muessen).
**Ergebnis #18:** Neue Klasse `FallbackAIProcessor` in `ai_service.py`:
versucht zuerst Ollama, faengt `AIServiceError` ab und wechselt automatisch
zu Gemini, falls `GEMINI_API_KEY` gesetzt ist. `get_default_ai_processor()`
liefert jetzt diesen Fallback-Wrapper statt einer festen Vorab-Entscheidung.
Ohne Key unveraendertes Verhalten (nur Ollama). README und Tests
aktualisiert (48/48 gruen).

**Prompt #19:** Bitte, einen (laut Nutzer nicht funktionsfaehigen) Test-API-Key
direkt in den Code einzutragen; der echte Key folge spaeter.
**Ergebnis #19:** Abgelehnt &mdash; Secrets gehoeren nicht in Code in einem
Git-Repo (bleiben sonst dauerhaft in der Historie). Stattdessen `setx
GEMINI_API_KEY "..."` als dauerhafte, sichere Alternative vorgeschlagen
(keine Code-Aenderung).

**Prompt #20:** Bitte, den `setx`-Ansatz als empfohlenen Weg (Alternative zu
Ollama) in die README aufzunehmen.
**Ergebnis #20:** README-Abschnitt "AI backend" um `setx`-Anleitung
(dauerhaft), Hinweis auf `$env:` fuer einmalige Tests, und expliziten
Warnhinweis "kein Hardcoding von API-Keys" ergaenzt.

**Prompt #21:** "python run.py" liess sich per Linksklick (PyCharm) nicht
mehr starten; spaeter Fehler "AI parsing failed" nach PC-Neustart.
**Ergebnis #21:** Ursache Nr. 1: ein haengengebliebener alter Testprozess
blockierte Port 8000 (beendet). Ursache Nr. 2: `python -m uvicorn ...`
wurde erneut aus dem falschen Verzeichnis gestartet (Home-Ordner statt
Projekt) &mdash; `run.py` mit vollem Pfad als Loesung bestaetigt. Fuer
"AI parsing failed" wurde die Fehlerantwort in `main.py` um die konkrete
Ursache (`str(exc)`) ergaenzt, statt nur eines generischen Textes.

**Prompt #22:** Bitte, den Code aufzuraeumen (alles Ungenutzte/Unnoetige
entfernen) und die Anzahl aufgeraeumter Zeilen zu nennen.
**Ergebnis #22:** Tote, ungenutzte Backward-Compat-Wrapperfunktionen
(`generate_cii_xml`, `validate_invoice`, `validate_cii_xml`,
`extract_cii_xml_from_file`, `extract_cii_xml_from_pdf`, `parse_cii_xml`,
`extract_text_from_file`) aus `cii_generator.py`, `validator.py`,
`xsd_validator.py`, `cii_parser.py`, `ocr_service.py` entfernt (durch
Grep bestaetigt: nirgendwo mehr referenziert) &mdash; 95 Zeilen. Zusaetzlich
im Git getrackte `.pyc`-Dateien entfernt und `.gitignore` angelegt
(`__pycache__/`, `*.pyc`, `.venv/`, `.idea/`). 48/48 Tests weiterhin gruen.

**Prompt #23:** Fehler "Gemini returned an error status: 404 ... ?key=<echter
Key sichtbar>" &mdash; der Key stand im Klartext in der Fehlermeldung.
**Ergebnis #23:** Sicherheitsluecke gefixt: `GeminiAIProcessor` sendet den
API-Key jetzt per Header (`x-goog-api-key`) statt als URL-Query-Parameter
(`ai_service.py`), damit er nie wieder in Fehlermeldungen/Logs/URLs auftaucht.
2 Tests dafuer ergaenzt (Header statt URL, kein Key-Leak bei HTTPError).
Vermutung zur 404-Ursache (ungueltiges Key-Format) war falsch, siehe #25.

**Prompt #24:** Screenshot des AI-Studio-Key-Dialogs &mdash; Key beginnt mit
`AQ.Ab8...`, Nutzer bestaetigt, dass das ein echter, aktueller Gemini-Key ist.
**Ergebnis #24:** Fehleinschaetzung eingeraeumt (Wissensstand Januar 2026,
Google hat offenbar zwischenzeitlich ein neues Key-Format eingefuehrt, das
nicht mehr zwingend mit `AIzaSy...` beginnt). Nutzer gebeten, die von AI
Studio generierte cURL-Kurzanleitung zu teilen, um Header/Endpoint zu
verifizieren statt weiter zu raten.

**Prompt #25:** cURL-Beispiel aus AI Studio geteilt.
**Ergebnis #25:** Zeigt: Header (`x-goog-api-key`) war schon korrekt, aber
Google nutzt dort als Modellname `gemini-flash-latest`, nicht
`gemini-2.0-flash` (vermutlich veraltet/nicht mehr verfuegbar). Default-Modell
in `GeminiAIProcessor.DEFAULT_MODEL` sowie README/KI_Prompts.md aktualisiert.
50/50 Tests gruen.

**Prompt #26:** Wunsch nach Kopier- und Download-Buttons fuer das erzeugte
XML in der `/ui`-Oberflaeche.
**Ergebnis #26:** Zwei Buttons in `views/upload_page.py` ergaenzt: "XML kopieren"
(Zwischenablage via `navigator.clipboard`) und "XML herunterladen" (Blob-
Download als `.xml`-Datei), beide erst aktiv nach erfolgreicher XML-Erzeugung.

**Prompt #27:** Frage nach einer fertigen Schablone, um aus der XML ein
"xPDF" (= ZUGFeRD/Factur-X-PDF) zu machen &mdash; das soll am Ende das fertige
Endergebnis sein.
**Ergebnis #27:** Bibliothek `factur-x` (PyPI) gefunden und getestet &mdash; das
ist die etablierte Referenzimplementierung fuers Einbetten von CII-XML in
ein PDF/A-3-Dokument (XMP-Metadaten, AFRelationship, XSD/Schematron-Pruefung
inklusive). Dabei einen echten Bug in unserem eigenen Generator gefunden und
behoben: die "Guideline"-URN in `controllers/builders/header_builder.py` war
nicht standardkonform (`urn:factur-x.eu:1p0:en16931:comfort` &rarr; korrekt:
`urn:cen.eu:en16931:2017`). Neuer Service `controllers/facturx_service.py`
(`FacturXPdfBuilder`), neuer Endpoint `POST /api/v1/zugferd/pdf` (Multipart:
`invoice_json` + visuelle PDF-Datei &rarr; fertiges ZUGFeRD-PDF), neues
UI-Panel 3 in `views/upload_page.py` zum Hochladen der Vorlage und automatischen
Download des Ergebnisses. `factur-x` zu `requirements.txt` hinzugefuegt.
6 neue Tests, 56/56 gruen.

**Prompt #28:** Screenshot der `/ui`-Oberflaeche; Frage "machen wir eine
json 2mal?" &mdash; Beobachtung, dass Panel 1 und Panel 2 zwei verschiedene
JSON-Formen brauchen.
**Ergebnis #28:** Erklaert, dass das flache Extraktionsschema (Panel 1) und
das verschachtelte `GermanInvoice`-Schema (Panel 2) bewusst unterschiedlich
sind, da die KI bisher keine Kaeufer-Adresse/Positionen/BIC extrahiert.
Loesungsoptionen zur Diskussion gestellt (Auto-Uebernahme vs. KI-Prompt
erweitern) &mdash; vom Nutzer nicht per Auswahl beantwortet, sondern im
naechsten Prompt direkt przisiert.

**Prompt #29:** Wunsch, dass die KI komplett selbststaendig extrahiert,
daraus automatisch XML macht und am Ende eine ZUGFeRD-PDF speicherbar ist
(durchgehende Kette ohne manuelles Doppel-Eintragen).
**Ergebnis #29:** Beide Loesungsoptionen aus #28 kombiniert:
- Extraktions-Prompt in `ai_service.py` erweitert (Kaeufer-/Verkaeufer-
  Adresse, BIC, Zahlungsbedingungen, Faelligkeitsdatum, Positionsliste
  `line_items`), Felder `vendor_name`/`vendor_vat_id` zu `seller_name`/
  `seller_vat_id` umbenannt (konsistent zu `buyer_*`).
- `controllers/invoice_parser.py` normalisiert die neuen Felder
  (`normalize_line_items()`, `clean_bic`, `due_date`).
- Neuer Service `controllers/invoice_mapper.py` (`InvoiceMapper`): baut aus den
  normalisierten Feldern ein vollstaendiges `GermanInvoice` &mdash; synthetisiert
  bei Bedarf eine einzelne Rechnungsposition/Steueraufschluesselung aus den
  Summen, wenn die KI keine Einzelpositionen liefert, damit das Ergebnis
  immer XML-faehig ist. Wirft `InvoiceMappingError` mit `missing_fields`,
  wenn Pflichtfelder (Rechnungsnummer/-datum, Verkaeufer-/Kaeufername,
  Summen) fehlen.
- `POST /api/v1/invoices/extract` liefert jetzt zusaetzlich `mapped_invoice`
  (fertiges `GermanInvoice`-JSON) und `mapping_warnings` (fehlende Felder).
- `/ui`: nach erfolgreicher Extraktion wird Panel 2 automatisch mit
  `mapped_invoice` befuellt; die in Schritt 1 hochgeladene Datei wird in
  Schritt 3 automatisch als visuelle PDF-Vorlage wiederverwendet (kein
  zweiter Upload noetig).
- Neuer End-to-End-Test bestaetigt die komplette Kette (Upload &rarr;
  Extraktion &rarr; automatisches Mapping &rarr; ZUGFeRD-PDF) in einem Zug.
  66/66 Tests gruen.

**Prompt #30 (Nachtrag):** "GermanInvoice JSON" in `/ui` zeigt beim
Seitenaufruf schon Beispielinhalt, obwohl noch keine Extraktion stattfand
&mdash; verwirrend; danach explizit der Wunsch, dass die KI komplett
selbststaendig extrahiert -> XML -> ZUGFeRD-PDF liefert.
**Ergebnis #30:** Panel 2 startet jetzt leer (Platzhaltertext), separater
"Beispiel laden"-Button statt automatischer Vorbefuellung. Ausserdem 422-Fehler
"CountryID ... 'Deutschland' is not an element of the set" gemeldet und
behoben: `normalize_country()` in `invoice_parser.py` mappt gaengige
Laendernamen (Deutschland, Oesterreich, Schweiz, ...) auf ISO-3166-Codes;
unbekannte Werte werden `None` und fallen auf den bestehenden "DE"-Default
zurueck. 69/69 Tests gruen.

**Prompt #31:** Fehler "Model output could not be parsed as JSON" bei der
KI-Extraktion.
**Ergebnis #31:** JSON-Parsing in `ai_service.py` robuster gemacht: entfernt
automatisch Markdown-Codezaeune (```json ... ```) und Fliesstext um das
JSON-Objekt herum, bevor es aufgibt; Fehlermeldung zeigt jetzt einen
Ausschnitt der rohen Modellantwort zur Diagnose. 71/71 Tests gruen.

**Prompt #32:** Fehler "Could not generate Factur-X PDF: Stream has ended
unexpectedly"; Bitte, 2 offizielle Beispiel-Vorlagen (PDFs) zur Auswahl
bereitzustellen.
**Ergebnis #32:** Ursache: eine nicht-PDF-Datei (z.B. ein wiederverwendetes
JPG aus Schritt 1) wurde als visuelle PDF an `pypdf` (intern von `factur-x`
genutzt) durchgereicht, was einen kryptischen internen Fehler ausloeste.
`FacturXPdfBuilder.build()` prueft jetzt vorab die `%PDF`-Signatur und wirft
eine klare `FacturXError`; `/ui` reicht in Schritt 3 nur noch echte PDFs aus
Schritt 1 automatisch weiter. Zwei Beispiel-PDFs in `examples/` ergaenzt:
`invoice_EN16931.pdf` (offizielles Testfixture aus dem `factur-x`-Python-Paket,
BSD-lizenziert) und `invoice_template.pdf` (selbst generiert, passend zu
`examples/invoice.json`). 72/72 Tests gruen.

**Prompt #33:** Frage, ob 72 Tests noetig sind bzw. reduzierbar; ausserdem
Bitte, die Projektstruktur nochmal zu pruefen und sichtbar in 3 Ordner
(Model/View/Controller) aufzuteilen.
**Ergebnis #33:** Testsuite konsolidiert: sehr kleinteilige, fast identische
Einzeltests zu je einer Funktion mit mehreren Asserts zusammengefasst (kein
Verlust an Abdeckung, insbesondere die zuvor gefundenen Regressionen wie
Key-Leak-Schutz, Laendernormalisierung, PDF-Signaturpruefung blieben
erhalten) &mdash; 72 auf 43 Tests reduziert (rund 40%). Projektstruktur auf 3
Ordner umgestellt: `services/` &rarr; `controllers/`, `ui/` &rarr; `views/`,
`models/` unveraendert (war schon der Model-Layer). Alle Imports in
`main.py`, `controllers/*.py` und `tests/*.py` sowie Pfad-Referenzen in
README/KI_Prompts.md angepasst. README um einen "Project Structure"-Abschnitt
ergaenzt. 43/43 Tests gruen.

**Prompt #34:** Fehler "AI service unavailable: Gemini request timed out";
Frage, ob ein vorgeschaltetes OCR-Programm es schneller machen wuerde.
**Ergebnis #34:** Klargestellt, dass OCR bereits vor der KI laeuft (Reihenfolge
war schon korrekt) &mdash; der langsame Teil ist der Gemini-Aufruf selbst.
Gemini-Timeout in `ai_service.py` von 60s auf 120s erhoeht (konsistent mit
Ollama), da das erweiterte Extraktionsschema mehr Antwortzeit braucht.
Danach neuer Fehler "Gemini returned HTTP 503" (Google-seitig ueberlastet,
haeufig bei kostenlosen Modellen) &mdash; automatischer Retry mit kurzem Backoff
(bis zu 2 Versuche, 3s Wartezeit) fuer 503-Antworten ergaenzt. 2 neue Tests
(Retry gelingt, Retry gibt nach mehrfachem Ueberlast-Fehler auf). 45/45 Tests
gruen.

**Prompt #35:** Vorschlag, dass OCR die Vorarbeit macht und die KI nur noch
prueft/ergaenzt, um Qualitaet und Geschwindigkeit zu verbessern.
**Ergebnis #35:** Neuer Service `controllers/ocr_field_extractor.py`
(`OCRFieldExtractor`): findet IBAN, BIC, Rechnungs-/Faelligkeitsdatum und
USt-ID-Kandidaten per Regex direkt im OCR-Text (inkl. Tabellen-Layouts, wo
Label und Wert in getrennten Zeilen stehen, und dem "ae"-Digraph fuer "ä").
`BaseInvoiceAIProcessor._build_prompt()` bekommt diesen Entwurf jetzt als
Parameter und bittet die KI, ihn zu verifizieren/korrigieren statt alles neu
zu erraten. Zusaetzliche Absicherung in `invoice_parser.py`: nach der
KI-Antwort werden IBAN/BIC/Datum hart mit den Regex-Werten ueberschrieben,
falls gefunden &mdash; die KI kann diese Felder also nicht mehr verfaelschen,
selbst wenn sie es versucht. Qualitaet damit strukturell abgesichert;
Geschwindigkeitsgewinn ist moeglich (weniger, was die KI "raten" muss), aber
nicht garantiert, da Netzwerklatenz/Modellgeschwindigkeit weiterhin dominieren.
9 neue Tests (Regex-Extraktion inkl. Tabellen-/Inline-Layout, Entwurf landet
im Prompt, KI-Antwort wird bei Abweichung ueberschrieben). 51/51 Tests gruen.

**Prompt #36:** Bitte, eine visuelle PDF-Vorlage fuer eine Rechnung zu
erstellen.
**Ergebnis #36:** `examples/invoice_template.pdf` von einem reinen Text-Dump
zu einer richtig formatierten Rechnung umgebaut (PyMuPDF-Zeichenprimitive):
Kopfbereich, Empfaenger-Block, Metadaten-Box, Positionstabelle mit
Kopfzeile, Summenblock, Footer mit IBAN/BIC. Layout-Bug beim ersten Versuch
(ueberlappender Text bei rechtsbuendigen Spalten) durch feste, ausreichend
beabstandete Anker-x-Positionen behoben. Passt zu `examples/invoice.json`;
per Screenshot-Rendering gepueft und gegen `FacturXPdfBuilder` erfolgreich
getestet. 51/51 Tests weiterhin gruen (kein Code betroffen, nur Asset).

**Prompt #37:** Bitte, 2 weitere Test-Vorlagen als JPG und PDF (kein xPDF)
bereitzustellen, zum Testen im Programm, in `examples/`.
**Ergebnis #37:** Zweite, eigenstaendige Beispielrechnung erzeugt (andere
Firma/Betraege/IBAN als `examples/invoice.json`, damit echte Testvielfalt
besteht): `examples/test_invoice.pdf` (normales PDF, textbasiert) und
`examples/test_invoice.jpg` (dieselbe Rechnung als Bild). Beide gegen die
echte `OCRProcessor`-Pipeline getestet (PyMuPDF-Textlayer bzw.
Tesseract-OCR) &mdash; Umlaute (ß, ü) korrekt erkannt in beiden. Fuer Schritt 1
(Upload -> OCR -> KI-Extraktion) gedacht, im Unterschied zu
`invoice_template.pdf`/`invoice_EN16931.pdf` (Schritt 3, ZUGFeRD-Einbettung).
51/51 Tests weiterhin gruen (kein Code betroffen, nur Assets).

**Prompt #38:** Anforderung: fortlaufende Dateibenennung, die nicht
umbenannt werden darf. Nach Rueckfrage praezisiert: gemeint ist die
Rechnungsnummer selbst, gemaess §14 UStG/GoBD (luekenlos, nie wiederverwendet,
nachtraeglich unveraenderlich).
**Ergebnis #38:** Neuer Service `controllers/invoice_number_sequencer.py`
(`InvoiceNumberSequencer`): vergibt fortlaufende Nummern (`RE-2026-0001`,
...) und persistiert den letzten Stand pro Jahr in `data/invoice_number_state.json`
(threading.Lock fuer atomare Vergabe, ueberlebt Neustarts, kann nie
zurueckgesetzt/wiederverwendet werden). Neuer Endpoint
`POST /api/v1/invoices/next-number`. Neuer Button "Naechste Rechnungsnummer
holen" in `/ui` Panel 2, traegt die vergebene Nummer automatisch in
`invoice.number` ein. `data/` zu `.gitignore` hinzugefuegt (lokaler
Laufzeitzustand, kein Code). Per Live-Browser-Test (zwei Klicks) bestaetigt:
liefert RE-2026-0001, dann RE-2026-0002. 6 neue Tests, 57/57 gruen.
Hinweis zur Grenze der Durchsetzung: die serverseitige Vergabe/Persistenz
ist hart erzwungen; ein Nutzer koennte die Nummer im freien JSON-Textfeld
theoretisch von Hand ueberschreiben, bevor er XML/PDF erzeugt &mdash; eine
harte serverseitige Sperre dafuer wuerde legitime Anwendungsfaelle
(bereits nummerierte, empfangene Rechnungen reformatieren/einbetten)
brechen und wurde bewusst nicht eingebaut.

**Prompt #39:** Wunsch nach 3 unterschiedlichen visuellen PDF-Vorlagen mit
Logo, auswaehlbar per Dropdown/Liste ("XPDF Vorlage #X"), Upload-Button soll
zusaetzlich bestehen bleiben.
**Ergebnis #39:** Drei visuell unterschiedliche PDF-Vorlagen erzeugt
(`examples/xpdf_vorlage_{1,2,3}.pdf`): unterschiedliches Logo (Kreis/Quadrat/
Dreieck), Akzentfarbe (Blau/Gruen/Orange) und Platzhaltertext (die visuelle
Seite zeigt bewusst generische Platzhalter statt echter Rechnungsdaten, da
das eingebettete PDF sich nicht automatisch an die XML-Daten anpasst).
Neuer Endpoint `GET /api/v1/templates/{1,2,3}` liefert die jeweilige PDF.
`/ui` Schritt 3 hat jetzt ein `<select>`-Dropdown zur Auswahl einer Vorlage,
zusaetzlich zum bestehenden Datei-Upload-Feld (Prioritaet: Dropdown-Auswahl
&gt; manueller Upload &gt; Wiederverwendung aus Schritt 1). Per Live-Browser-Test
bestaetigt: Dropdown-Auswahl "1" -&gt; `GET /api/v1/templates/1` wird geholt
und fuer die PDF-Erzeugung verwendet (im Netzwerk-Log sichtbar). Alle 3
Vorlagen gegen `FacturXPdfBuilder` erfolgreich getestet. 2 neue Tests,
59/59 gruen.

**Nachtrag:** Waehrend dieser Arbeit sind mehrere zuvor erstellte
`examples/`-Dateien (`invoice.json`, `invoice_template.pdf`,
`test_invoice.pdf/jpg`) unerwartet verschwunden (Ursache unklar, keine
eigene Aktion sollte das ausgeloest haben) und aus den gespeicherten
Erzeugungs-Skripten wiederhergestellt worden. Nutzer auf das Risiko
hingewiesen (Dateien waren nie committed) und Commit empfohlen.

**Prompt #40:** Wunsch nach 2 komplett unterschiedlichen JPGs und 2 PDFs,
bewusst kreativer/grenzwertiger gestaltet, zum Testen im Programm.
**Ergebnis #40:** Vier bewusst vielfaeltige, schwierigere Testfaelle erzeugt:
- `examples/freelancer_invoice_photo.jpg` &mdash; minimalistische Designer-
  Rechnung, per PIL nachbearbeitet (Rotation, Papierkoernung, Vignette,
  EPC-QR-Platzhalter), um wie ein echtes Handyfoto zu wirken.
- `examples/kassenbon_photo.jpg` &mdash; schmaler Kassenbon im Monospace-Stil,
  bewusst ohne foermlichen Verkaeufer-/Kaeufer-Adressblock (harter Testfall
  fuer den Mapper); Rotation/Rauschen erzeugt realistische OCR-Fehler bei
  einzelnen Zahlen.
- `examples/mixed_vat_invoice.pdf` &mdash; Positionen mit zwei Steuersaetzen
  (19%/7%) plus Rabattzeile, ergibt zwei `tax_breakdowns`-Eintraege.
- `examples/schweizer_handwerkerrechnung.pdf` &mdash; Schweizer Rechnung in CHF,
  8.1% MWST, mit QR-Zahlteil-Optik; deckt dabei eine bestehende Einschraenkung
  auf: `invoice_parser.py` setzt die Waehrung aktuell hart auf `"EUR"`,
  unabhaengig vom tatsaechlichen Rechnungsinhalt (in README dokumentiert,
  bewusst nicht behoben, da nicht angefragt).
Alle 4 gegen die echte `OCRProcessor`-Pipeline getestet und Ergebnisse
inspiziert. 59/59 Tests weiterhin gruen (reine Asset-Ergaenzung).

**Prompt #41:** Mapping-Warnung "fehlende Felder: invoice_date" bei der
Freelancer-Rechnung; Frage, was `invoice_date` bedeutet und ob die
englischen Feldnamen korrekt sind.
**Ergebnis #41:** Erklaert, dass `invoice_date` = "Rechnungsdatum" ist
(interne Feldnamen bewusst englisch, kein Uebersetzungsfehler). Ursache
gefunden: die Freelancer-Rechnung nutzt nur "Datum:" statt "Rechnungsdatum",
was die bisherige Regex in `controllers/ocr_field_extractor.py` nicht
erkannte. Fix: `\bdatum\b` als zusaetzliches Label ergaenzt. Dabei einen
zweiten, tieferliegenden Fehler beim Testen gefunden: ein unerkanntes
"Lieferdatum" zwischen Rechnungs- und Faelligkeitsdatum verschob bisher die
sequentielle Datums-Label-Zuordnung, sodass `due_date` faelschlich das
Lieferdatum bekam (in `examples/test_invoice.pdf` bisher unbemerkt, weil dort
Rechnungs- und Lieferdatum zufaellig identisch waren). Fix: `Lieferdatum`
wird jetzt als eigenes Label erkannt und sein Datum uebersprungen, ohne die
Zuordnung zu verschieben. 4 neue Tests, 61/61 gruen.

**Prompt #42:** Screenshots der Kassenbon- und Freelancer-Testbilder; Bitte
zu pruefen, ob alles (besonders das Datum) drauf ist, und Frage, ob eine
Rechnung zwingend einen Namen (Kaeufer) tragen muss &mdash; falls ja, den
Kassenbon entfernen.
**Ergebnis #42:** Beide Bilder visuell bestaetigt (Datum auf der Freelancer-
Rechnung war immer korrekt, der fruehere Fehler lag nur in der Erkennung,
nicht im Bild). Rechtliche Einordnung: volle Rechnung braucht Kaeufername
(§14 UStG), Kleinbetragsrechnung bis 250€ brutto (§33 UStDV) ausdruecklich
nicht &mdash; der Kassenbon (19,46€) waere damit eigentlich rechtlich korrekt.
Nutzer hat sich trotzdem fuer Entfernen entschieden: `examples/kassenbon_photo.jpg`
geloescht, README-Eintrag entfernt (keine Tests betroffen).

**Prompt #43:** "XPDF wird nicht richtig die XML-Datei verwendet für die 3
Templates."
**Ergebnis #43:** Ursache gefunden (kein technischer Fehler, aber ein echtes
Problem): die eingebettete XML war byte-genau korrekt, aber die 3 XPDF-
Vorlagen zeigten nur statischen Platzhaltertext ("[Kaeufername]", "[siehe
XML]") statt der echten Rechnungsdaten &mdash; fuer einen Menschen sah das PDF
kaputt aus, obwohl die maschinenlesbare XML stimmte. Neu gebaut:
`controllers/visual_invoice_renderer.py` (`VisualInvoiceRenderer`) rendert
die visuelle Seite jetzt dynamisch aus dem echten `GermanInvoice` (Verkaeufer,
Kaeufer, Positionen, Betraege) im jeweiligen Vorlagen-Design (Logo/Akzentfarbe).
`POST /api/v1/zugferd/pdf` bekommt ein neues optionales Feld `template_id`
(1-3) statt eines zweiten Requests an einen separaten Vorlagen-Endpoint;
der alte `GET /api/v1/templates/{id}` sowie die statischen
`examples/xpdf_vorlage_*.pdf`-Dateien wurden entfernt (ueberfluessig).
`/ui` schickt `template_id` jetzt direkt mit dem Haupt-Request statt vorher
die Vorlage separat zu laden (ein Request statt zwei). 6 neue/angepasste
Tests, 65/65 gruen; per Rendering + Live-Browser-Test bestaetigt (kein
Platzhaltertext mehr, echte Daten sichtbar).

---

## Pflegehinweise

- Neue Laufzeit-Prompts (z. B. weitere Ollama-Modelle, andere Extraktionsfelder)
  unter Abschnitt 1 ergaenzen, inklusive Modellname und Datei-Referenz.
- Jeden neuen Prompt an den Assistenten unter Abschnitt 2 als
  `Prompt #N` / `Ergebnis #N` anhaengen &mdash; kurz halten, keine
  Wiederholung von Details, die schon im Code/Diff stehen.
