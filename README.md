# German Invoice OCR API

API for German invoice extraction, EN16931 validation, and ZUGFeRD/Factur-X CII XML generation/parsing.

## Features

- Extract invoice data from images/PDFs with OCR + AI. A deterministic regex
  pre-pass finds IBAN/BIC/dates/VAT IDs first (see `controllers/ocr_field_extractor.py`);
  the AI verifies/completes that draft rather than retyping everything, so
  these strict-format fields can never be garbled by the model.
- Generate ZUGFeRD/Factur-X CII XML from structured invoice JSON.
- Issue legally compliant, consecutive invoice numbers (§14 UStG/GoBD) via
  a persistent server-side sequencer (see `controllers/invoice_number_sequencer.py`).
- Embed that XML into a visual PDF to produce a complete ZUGFeRD/Factur-X PDF.
- Validate invoice totals against basic EN16931 business rules.
- Validate generated CII XML against the local UNECE D22B XSD schema set.
- Parse CII XML or ZUGFeRD/Factur-X PDFs with embedded XML back to JSON.

## Project Structure

The codebase follows a Model-View-Controller layout:

```text
models/       Model      Pydantic data schemas (GermanInvoice, ...)
views/        View       HTML/JS test UI served at /ui
controllers/  Controller Business logic + FastAPI route handlers call into
main.py                  main.py wires the FastAPI app and routes together
```

## Quickstart

This section walks through everything needed to go from a fresh checkout to
a running API with a browser-based test UI.

**1. Install Python dependencies**

```bash
pip install -r requirements.txt
```

**2. (Optional) Install Tesseract OCR**

Only needed for `POST /api/v1/invoices/extract` (uploading a scanned
PDF/image). Everything else (JSON → XML, validation, XML → JSON) works
without it.

Windows installer (64-bit):

```text
https://github.com/tesseract-ocr/tesseract/releases/download/5.5.0/tesseract-ocr-w64-setup-5.5.0.20241111.exe
```

Other platforms / older builds: https://github.com/UB-Mannheim/tesseract/wiki

During setup, make sure **German** is selected under "Language data" (the
app uses `lang="deu+eng"`, see `controllers/ocr_service.py`), and enable "Add
to PATH" if the installer offers it. After installing, open a **new**
terminal (PATH changes don't apply to already-open shells) and verify with:

```bash
tesseract --version
```

**3. (Optional) Set up the AI backend**

Also only needed for `POST /api/v1/invoices/extract`. The app always
prefers the local, free Ollama backend:

- **Local (Ollama)** — no API key, no internet required. Pull and run the
  `qwen3:8b` model so it's reachable at `http://localhost:11434` (see
  `controllers/ai_service.py` for the defaults).
- **Gemini API (free tier, optional automatic fallback)** — if Ollama isn't
  running (or fails), the app automatically falls back to Gemini, no
  manual switching needed. Get a free API key at
  https://aistudio.google.com/apikey.

  Set it as a **permanent** environment variable (recommended, so you don't
  need to re-enter it in every new terminal):

  ```powershell
  setx GEMINI_API_KEY "your-key-here"
  ```

  `setx` writes it to your Windows user profile once. Open a **new**
  terminal afterwards (existing ones won't see it, same as PATH changes),
  then start the server normally:

  ```powershell
  python run.py
  ```

  For a one-off test in the current terminal only, `$env:GEMINI_API_KEY =
  "your-key-here"` also works, but is lost when you close the window.

  **Never hardcode the API key into the source code.** This is a git
  repository — a key committed to a file stays in the git history forever,
  even after you remove it later.

  Without `GEMINI_API_KEY` set, only Ollama is used (unchanged behavior).
  Optionally set `GEMINI_MODEL` to override the default model
  (`gemini-flash-latest`). See `controllers.ai_service.get_default_ai_processor`.

**4. Start the API**

```bash
python run.py
```

`run.py` finds the project root by itself, so it works from any directory,
any computer, and can be started directly from your IDE's Run button (no
shell script, no PATH setup needed). By default it listens on
`http://127.0.0.1:8000` with auto-reload enabled.

**5. Try it in the browser**

Open the built-in drag-and-drop test UI:

```text
http://127.0.0.1:8000/ui
```

- Left panel: drop a PDF/JPG invoice to run OCR + AI extraction (needs
  step 2 and 3 above). The extracted fields are automatically mapped onto
  the `GermanInvoice` schema and copied into the right panel — any fields
  the AI couldn't determine (e.g. buyer address, individual line items)
  are flagged so you can fill them in manually.
- Right panel: review/edit the `GermanInvoice` JSON (auto-filled after
  step 1, or via the "Beispiel laden" button) and generate ZUGFeRD CII
  XML from it. Copy/download buttons for the generated XML.
- Below that: generates the complete ZUGFeRD/Factur-X PDF by embedding the
  XML into a visual PDF. Pick one of 3 built-in "XPDF Vorlage" templates —
  rendered on the fly with the invoice's own data (real seller/buyer,
  amounts, line items), each with a different logo/color scheme — upload
  your own PDF, or leave both empty to reuse the file from step 1 — then
  downloads the result.

**6. Explore the full API**

Every endpoint is also documented and callable via Swagger:

```text
http://127.0.0.1:8000/docs
```

Or check the API is alive from the command line:

```bash
curl http://127.0.0.1:8000/health
```

## Testing

```bash
python -m pytest -q
```

`python -m pytest` (instead of the plain `pytest` command) avoids the same
PATH issue as running uvicorn directly. The test suite mocks the local
Ollama call, so no running Ollama/Tesseract instance is required to run it.

## Response Format

JSON endpoints return a consistent envelope:

```json
{
  "success": true,
  "data": {},
  "errors": [],
  "meta": {}
}
```

Validation errors use the same format with `success: false`.

The XML generation endpoint returns `application/xml` directly.

## Endpoints

### Extract Invoice From File

```text
POST /api/v1/invoices/extract
```

```bash
curl -X POST http://127.0.0.1:8000/api/v1/invoices/extract \
  -F "file=@invoice.pdf"
```

Response `data` contains:

- `invoice` — the raw, normalized AI-extracted fields (flat).
- `mapped_invoice` — the same data mapped onto the `GermanInvoice` schema
  (see `controllers/invoice_mapper.py`), ready for `/api/v1/zugferd/xml` or
  `/api/v1/zugferd/pdf`. `null` if required fields (invoice number/date,
  seller/buyer name, totals) could not be determined.
- `mapping_warnings` — list of fields that prevented mapping, if any.
- `raw_text` — the raw OCR text.

### Issue the Next Sequential Invoice Number

```text
POST /api/v1/invoices/next-number?year=2026
```

Issues a consecutive, gapless invoice number (e.g. `RE-2026-0001`) as
required by §14 UStG/GoBD for invoices you issue. The counter is persisted
per year to `data/invoice_number_state.json` and only ever moves forward —
a number is never reissued or reused, even across restarts. `year` defaults
to the current year.

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/invoices/next-number"
```

### Generate ZUGFeRD CII XML

```text
POST /api/v1/zugferd/xml?validate=true
```

This is the production endpoint for JSON to XML conversion.

Flow:

```text
JSON input
-> EN16931 business validation
-> CII XML generation
-> ZUGFeRD XSD validation
-> returns XML if valid
-> returns JSON errors if invalid
```

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/zugferd/xml?validate=true" \
  -H "Content-Type: application/json" \
  --data-binary "@examples/invoice.json" \
  -o invoice.xml
```

Use `validate=false` only for debugging XML output without blocking on validation.

### Generate a Complete ZUGFeRD/Factur-X PDF

```text
POST /api/v1/zugferd/pdf?validate=true
```

Embeds the CII XML into a visual PDF using the
[`factur-x`](https://pypi.org/project/factur-x/) library, producing a single
PDF/A-3 document that is both human-readable and machine-readable (the
actual "finished" ZUGFeRD invoice). The visual PDF comes from exactly one
of two sources — provide `file`, or `template_id`, not both:

- `invoice_json` — the `GermanInvoice` JSON as a string form field.
- `file` — upload your own visual PDF (e.g. the originally scanned invoice)
  to embed the XML into.
- `template_id` — instead of uploading a file, render one of 3 built-in
  templates (`1`, `2`, or `3`, see `controllers/visual_invoice_renderer.py`)
  on the fly using the invoice's own data (real seller/buyer, amounts, line
  items, not placeholder text) — each with a distinct logo mark and accent
  color. The `/ui` step-3 panel offers these via a dropdown.

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/zugferd/pdf?validate=true" \
  -F "invoice_json=<examples/invoice.json" \
  -F "file=@visual_invoice.pdf" \
  -o invoice_zugferd.pdf
```

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/zugferd/pdf?validate=true" \
  -F "invoice_json=<examples/invoice.json" \
  -F "template_id=1" \
  -o invoice_zugferd.pdf
```

### Validate EN16931 Business Rules

```text
POST /api/v1/en16931/validate
```

```bash
curl -X POST http://127.0.0.1:8000/api/v1/en16931/validate \
  -H "Content-Type: application/json" \
  --data-binary "@examples/invoice.json"
```

### Validate Generated ZUGFeRD XML Against XSD

```text
POST /api/v1/zugferd/validate-xsd
```

```bash
curl -X POST http://127.0.0.1:8000/api/v1/zugferd/validate-xsd \
  -H "Content-Type: application/json" \
  --data-binary "@examples/invoice.json"
```

### Parse XML/PDF To JSON

```text
POST /api/v1/zugferd/parse
```

Accepts either a raw CII XML file or a ZUGFeRD/Factur-X PDF with embedded XML.

```bash
curl -X POST http://127.0.0.1:8000/api/v1/zugferd/parse \
  -F "file=@invoice.xml"
```

```bash
curl -X POST http://127.0.0.1:8000/api/v1/zugferd/parse \
  -F "file=@invoice.pdf"
```

## XSD Schemas

The XSD validator expects the complete UNECE D22B CII schema package in `schemas/`.

Required root file:

```text
schemas/CrossIndustryInvoice_100pD22B.xsd
```

The imported codelist and identifierlist XSD files must be in the same folder.

## Example Files

Ready-to-use sample files are bundled in `examples/`:

For testing the **"visual PDF" upload in step 3** (or `/api/v1/zugferd/pdf`
directly) — embedding CII XML into an existing PDF:

- `examples/invoice.json` — the example `GermanInvoice` JSON used throughout
  this README, loadable via the "Beispiel laden" button in `/ui`.
- `examples/invoice_template.pdf` — a formatted visual PDF generated from
  `examples/invoice.json`, matching it field-for-field.
- `examples/invoice_EN16931.pdf` — an official EN16931-level Factur-X test
  fixture from the [`factur-x`](https://pypi.org/project/factur-x/) Python
  library (BSD-licensed, © Alexis de Lattre / Akretion), useful as an
  independent, standards-conformant reference invoice.

For testing **step 1 (upload → OCR → AI extraction)** — a different,
self-contained sample invoice (not tied to `examples/invoice.json`):

- `examples/test_invoice.pdf` — plain (non-ZUGFeRD) PDF invoice, extracted
  directly via PyMuPDF's text layer.
- `examples/test_invoice.jpg` — the same invoice as a JPG image, exercising
  the Tesseract OCR path instead.

Three more deliberately varied, harder cases for stress-testing extraction:

- `examples/freelancer_invoice_photo.jpg` — minimalist designer invoice,
  processed to look like a real phone photo (rotated, paper grain,
  vignette) with an EPC-QR-style placeholder.
- `examples/mixed_vat_invoice.pdf` — multiple line items at two different
  VAT rates (19%/7%) plus a discount line, producing two `tax_breakdowns`
  entries.
- `examples/schweizer_handwerkerrechnung.pdf` — Swiss invoice in CHF, 8.1%
  MWST, hourly labour + materials, with a QR-bill-style payment slip
  section. Note: `controllers/invoice_parser.py` currently hardcodes the
  output currency to `"EUR"` regardless of what's on the invoice, so
  extracting this one will still report `"EUR"` even though the source
  document is in CHF -- a known limitation this file is meant to surface.

## Notes

- When parsing XML to JSON, missing `InvoiceCurrencyCode` and `CountryID` are returned as `null`.
- When generating XML from JSON, missing or placeholder `currency` falls back to `EUR`.
- When generating XML from JSON, missing or placeholder `country_id` falls back to `DE`.
- Legacy routes still exist but are hidden from Swagger.
