"""Tests for the FastAPI HTTP endpoints in main.py."""

import io
import json

import fitz

import main
from controllers.ai_service import AIConnectionError, AIResponseError
from controllers.invoice_number_sequencer import InvoiceNumberSequencer


def _blank_pdf_bytes() -> bytes:
    doc = fitz.open()
    doc.new_page()
    return doc.tobytes()


def test_next_invoice_number_endpoint_issues_sequential_numbers(client, monkeypatch, tmp_path):
    monkeypatch.setattr(
        main, "invoice_number_sequencer", InvoiceNumberSequencer(state_path=tmp_path / "state.json")
    )

    first = client.post("/api/v1/invoices/next-number", params={"year": 2026})
    second = client.post("/api/v1/invoices/next-number", params={"year": 2026})

    assert first.status_code == 200
    assert first.json()["data"]["number"] == "RE-2026-0001"
    assert second.json()["data"]["number"] == "RE-2026-0002"


def test_health_and_root_endpoints(client):
    health = client.get("/health")
    assert health.status_code == 200
    assert health.json()["data"]["status"] == "ok"

    root = client.get("/")
    assert root.status_code == 200
    assert root.json()["success"] is True


def test_zugferd_pdf_endpoint_renders_builtin_templates_with_real_data(client, example_invoice_dict):
    for template_id in (1, 2, 3):
        response = client.post(
            "/api/v1/zugferd/pdf",
            data={"invoice_json": json.dumps(example_invoice_dict), "template_id": str(template_id)},
        )

        assert response.status_code == 200
        assert response.headers["content-type"] == "application/pdf"

        doc = fitz.open(stream=response.content, filetype="pdf")
        page_text = doc[0].get_text()
        assert example_invoice_dict["seller"]["name"] in page_text
        assert example_invoice_dict["buyer"]["name"] in page_text
        assert example_invoice_dict["invoice"]["number"] in page_text


def test_zugferd_pdf_endpoint_rejects_unknown_template_id(client, example_invoice_dict):
    response = client.post(
        "/api/v1/zugferd/pdf",
        data={"invoice_json": json.dumps(example_invoice_dict), "template_id": "99"},
    )

    assert response.status_code == 422


def test_zugferd_pdf_endpoint_requires_file_or_template_id(client, example_invoice_dict):
    response = client.post(
        "/api/v1/zugferd/pdf",
        data={"invoice_json": json.dumps(example_invoice_dict)},
    )

    assert response.status_code == 422


def test_ui_endpoint_serves_html(client):
    response = client.get("/ui")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "dropzone" in response.text


def test_en16931_validate_endpoint(client, example_invoice_dict):
    response = client.post("/api/v1/en16931/validate", json=example_invoice_dict)
    assert response.status_code == 200
    assert response.json()["data"]["valid"] is True

    example_invoice_dict["totals"]["payable_amount"] = "1.00"
    response = client.post("/api/v1/en16931/validate", json=example_invoice_dict)
    assert response.status_code == 200
    body = response.json()
    assert body["data"]["valid"] is False
    assert body["data"]["errors"]


def test_zugferd_xml_endpoint_returns_xml_for_valid_invoice(client, example_invoice_dict):
    response = client.post("/api/v1/zugferd/xml", json=example_invoice_dict)

    assert response.status_code == 200
    assert response.headers["X-EN16931-Valid"] == "true"
    assert response.headers["X-ZUGFeRD-XSD-Valid"] == "true"
    assert "CrossIndustryInvoice" in response.text


def test_zugferd_xml_endpoint_rejects_or_skips_validation(client, example_invoice_dict):
    example_invoice_dict["totals"]["payable_amount"] = "1.00"

    response = client.post("/api/v1/zugferd/xml", json=example_invoice_dict)
    assert response.status_code == 422
    assert response.json()["errors"]["validation"] == "en16931"

    response = client.post(
        "/api/v1/zugferd/xml", params={"validate": "false"}, json=example_invoice_dict
    )
    assert response.status_code == 200
    assert response.headers["X-EN16931-Valid"] == "false"


def test_zugferd_pdf_endpoint_returns_pdf_for_valid_invoice(client, example_invoice_dict):
    response = client.post(
        "/api/v1/zugferd/pdf",
        data={"invoice_json": json.dumps(example_invoice_dict)},
        files={"file": ("visual.pdf", io.BytesIO(_blank_pdf_bytes()), "application/pdf")},
    )

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert response.headers["X-EN16931-Valid"] == "true"
    assert response.headers["X-ZUGFeRD-XSD-Valid"] == "true"

    doc = fitz.open(stream=response.content, filetype="pdf")
    filenames = [doc.embfile_info(i)["filename"] for i in range(doc.embfile_count())]
    assert "factur-x.xml" in filenames


def test_zugferd_pdf_endpoint_rejects_invalid_input(client, example_invoice_dict):
    invalid_totals = dict(example_invoice_dict)
    invalid_totals["totals"] = dict(invalid_totals["totals"], payable_amount="1.00")
    response = client.post(
        "/api/v1/zugferd/pdf",
        data={"invoice_json": json.dumps(invalid_totals)},
        files={"file": ("visual.pdf", io.BytesIO(_blank_pdf_bytes()), "application/pdf")},
    )
    assert response.status_code == 422
    assert response.json()["errors"]["validation"] == "en16931"

    response = client.post(
        "/api/v1/zugferd/pdf",
        data={"invoice_json": "not json"},
        files={"file": ("visual.pdf", io.BytesIO(_blank_pdf_bytes()), "application/pdf")},
    )
    assert response.status_code == 422

    response = client.post(
        "/api/v1/zugferd/pdf",
        data={"invoice_json": json.dumps(example_invoice_dict)},
        files={"file": ("visual.pdf", io.BytesIO(b"not a pdf"), "application/pdf")},
    )
    assert response.status_code == 422


def test_zugferd_parse_roundtrip_and_rejects_invalid_xml(client, example_invoice_dict):
    xml_response = client.post(
        "/api/v1/zugferd/xml", params={"validate": "false"}, json=example_invoice_dict
    )

    parse_response = client.post(
        "/api/v1/zugferd/parse",
        files={"file": ("invoice.xml", io.BytesIO(xml_response.content), "application/xml")},
    )
    assert parse_response.status_code == 200
    body = parse_response.json()
    assert body["data"]["invoice"]["invoice"]["number"] == example_invoice_dict["invoice"]["number"]

    invalid_response = client.post(
        "/api/v1/zugferd/parse",
        files={"file": ("invoice.xml", io.BytesIO(b"<not-cii/>"), "application/xml")},
    )
    assert invalid_response.status_code == 400


def test_extract_invoice_returns_error_status_for_ai_failures(client, monkeypatch):
    monkeypatch.setattr(
        main.ocr_processor, "extract_text_from_file", lambda contents, filename: "OCR text"
    )

    def fake_connection_error(text, processor=None):
        raise AIConnectionError("Ollama unreachable")

    monkeypatch.setattr(main, "parse_invoice", fake_connection_error)
    response = client.post(
        "/api/v1/invoices/extract",
        files={"file": ("invoice.pdf", io.BytesIO(b"%PDF-1.4 fake"), "application/pdf")},
    )
    assert response.status_code == 503

    def fake_response_error(text, processor=None):
        raise AIResponseError("bad response")

    monkeypatch.setattr(main, "parse_invoice", fake_response_error)
    response = client.post(
        "/api/v1/invoices/extract",
        files={"file": ("invoice.pdf", io.BytesIO(b"%PDF-1.4 fake"), "application/pdf")},
    )
    assert response.status_code == 502


_COMPLETE_EXTRACTED_DATA = {
    "invoice_number": "INV-2026-001",
    "invoice_date": "2026-05-06",
    "due_date": "2026-05-20",
    "currency": "EUR",
    "seller_name": "Seller GmbH",
    "seller_vat_id": "DE123456789",
    "seller_street": None,
    "seller_postcode": None,
    "seller_city": None,
    "seller_country": None,
    "buyer_name": "Buyer GmbH",
    "buyer_vat_id": None,
    "buyer_street": None,
    "buyer_postcode": None,
    "buyer_city": None,
    "buyer_country": None,
    "iban": "DE89370400440532013000",
    "bic": "COBADEFFXXX",
    "payment_terms": None,
    "net_total": 100.0,
    "gross_total": 119.0,
    "vat_amount": 19.0,
    "vat_rate": 19.0,
    "line_items": [],
}


def test_extract_invoice_returns_raw_data_without_mapping_when_incomplete(client, monkeypatch):
    monkeypatch.setattr(
        main.ocr_processor, "extract_text_from_file", lambda contents, filename: "OCR text"
    )
    monkeypatch.setattr(
        main, "parse_invoice", lambda text, processor=None: {"seller_name": "Seller GmbH", "net_total": 100.0}
    )

    response = client.post(
        "/api/v1/invoices/extract",
        files={"file": ("invoice.pdf", io.BytesIO(b"%PDF-1.4 fake"), "application/pdf")},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["data"]["invoice"]["seller_name"] == "Seller GmbH"
    assert body["data"]["raw_text"] == "OCR text"
    assert body["data"]["mapped_invoice"] is None
    assert "buyer_name" in body["data"]["mapping_warnings"]


def test_extract_invoice_includes_mapped_invoice_when_complete(client, monkeypatch):
    monkeypatch.setattr(main, "parse_invoice", lambda text, processor=None: dict(_COMPLETE_EXTRACTED_DATA))
    monkeypatch.setattr(
        main.ocr_processor, "extract_text_from_file", lambda contents, filename: "OCR text"
    )

    response = client.post(
        "/api/v1/invoices/extract",
        files={"file": ("invoice.pdf", io.BytesIO(b"%PDF-1.4 fake"), "application/pdf")},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["data"]["mapping_warnings"] == []
    assert body["data"]["mapped_invoice"]["invoice"]["number"] == "INV-2026-001"
    assert body["data"]["mapped_invoice"]["seller"]["name"] == "Seller GmbH"


def test_full_pipeline_extract_then_generate_pdf(client, monkeypatch):
    """End-to-end: extraction -> automatic mapping -> Factur-X PDF, as the UI would use it."""
    monkeypatch.setattr(main, "parse_invoice", lambda text, processor=None: dict(_COMPLETE_EXTRACTED_DATA))
    monkeypatch.setattr(
        main.ocr_processor, "extract_text_from_file", lambda contents, filename: "OCR text"
    )

    extract_response = client.post(
        "/api/v1/invoices/extract",
        files={"file": ("invoice.pdf", io.BytesIO(b"%PDF-1.4 fake"), "application/pdf")},
    )
    mapped_invoice = extract_response.json()["data"]["mapped_invoice"]
    assert mapped_invoice is not None

    pdf_response = client.post(
        "/api/v1/zugferd/pdf",
        data={"invoice_json": json.dumps(mapped_invoice)},
        files={"file": ("visual.pdf", io.BytesIO(_blank_pdf_bytes()), "application/pdf")},
    )

    assert pdf_response.status_code == 200
    doc = fitz.open(stream=pdf_response.content, filetype="pdf")
    filenames = [doc.embfile_info(i)["filename"] for i in range(doc.embfile_count())]
    assert "factur-x.xml" in filenames
