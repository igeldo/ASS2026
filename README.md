# German Invoice OCR API

API for German invoice extraction, EN16931 validation, and ZUGFeRD/Factur-X CII XML generation/parsing.

## Features

- Extract invoice data from images/PDFs with OCR + AI.
- Generate ZUGFeRD/Factur-X CII XML from structured invoice JSON.
- Validate invoice totals against basic EN16931 business rules.
- Validate generated CII XML against the local UNECE D22B XSD schema set.
- Parse CII XML or ZUGFeRD/Factur-X PDFs with embedded XML back to JSON.

## Setup

```bash
pip install -r requirements.txt
```

Install Tesseract OCR if you want to use `/api/v1/invoices/extract`.

Windows builds are available here:

```text
https://github.com/UB-Mannheim/tesseract/wiki
```

Run the API:

```bash
uvicorn main:app --reload
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

Health check:

```bash
curl http://127.0.0.1:8000/health
```

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

## Notes

- When parsing XML to JSON, missing `InvoiceCurrencyCode` and `CountryID` are returned as `null`.
- When generating XML from JSON, missing or placeholder `currency` falls back to `EUR`.
- When generating XML from JSON, missing or placeholder `country_id` falls back to `DE`.
- Legacy routes still exist but are hidden from Swagger.
