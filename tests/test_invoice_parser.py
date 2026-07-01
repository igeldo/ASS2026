"""Tests for controllers.invoice_parser normalization logic."""

from controllers.ai_service import InvoiceAIProcessor
from controllers.invoice_parser import (
    clean_iban,
    clean_vat_id,
    fix_vat,
    normalize_country,
    normalize_line_items,
    parse_invoice,
    to_float,
)


def test_to_float_parses_valid_formats():
    assert to_float("1.350,00 €") == 1350.00
    assert to_float("1350,00") == 1350.00


def test_to_float_returns_none_for_invalid_input():
    assert to_float(None) is None
    assert to_float("not a number") is None


def test_fix_vat_recomputes_or_leaves_untouched():
    assert fix_vat({"net_total": 100.0, "gross_total": 119.0}) == {
        "net_total": 100.0,
        "gross_total": 119.0,
        "vat_amount": 19.0,
        "vat_rate": 19.0,
    }

    data = {"net_total": None, "gross_total": 119.0}
    assert fix_vat(dict(data)) == data


def test_clean_iban_and_vat_id_strip_whitespace_or_return_none():
    assert clean_iban("DE89 3704 0044 0532 0130 00") == "DE89370400440532013000"
    assert clean_iban("") is None
    assert clean_iban(None) is None
    assert clean_vat_id(" DE 123456789 ") == "DE123456789"


def test_normalize_country_maps_names_keeps_codes_and_handles_unknown():
    assert normalize_country("Deutschland") == "DE"
    assert normalize_country("germany") == "DE"
    assert normalize_country("de") == "DE"
    assert normalize_country("FR") == "FR"
    assert normalize_country("Wonderland") is None
    assert normalize_country(None) is None
    assert normalize_country("") is None


def test_normalize_line_items_parses_and_drops_invalid_entries():
    items = [
        {"name": "Consulting", "quantity": "1,00", "unit_price": "100,00", "line_total": "100,00"},
        {"name": None, "quantity": "1"},  # missing name -> dropped
        {"name": "Empty row"},  # no numeric fields at all -> dropped
    ]

    assert normalize_line_items(items) == [
        {"name": "Consulting", "quantity": 1.0, "unit_price": 100.0, "line_total": 100.0}
    ]
    assert normalize_line_items(None) == []
    assert normalize_line_items("not a list") == []


class _FakeProcessor(InvoiceAIProcessor):
    """Stubbed AI processor that returns a fixed payload instead of calling Ollama."""

    def __init__(self, payload):
        super().__init__()
        self._payload = payload

    def extract(self, text, draft=None):
        return dict(self._payload)


def test_parse_invoice_normalizes_ai_output():
    fake_processor = _FakeProcessor(
        {
            "seller_name": "Seller GmbH",
            "seller_vat_id": " DE123456789 ",
            "buyer_name": "Buyer GmbH",
            "buyer_vat_id": None,
            "invoice_number": "INV-1",
            "invoice_date": "06.05.2026",
            "due_date": "20.05.2026",
            "net_total": "100,00",
            "gross_total": "119,00",
            "vat_amount": None,
            "vat_rate": None,
            "currency": None,
            "iban": "DE89 3704 0044 0532 0130 00",
            "bic": " COBADEFFXXX ",
            "seller_country": "Deutschland",
            "buyer_country": "Deutschland",
            "line_items": [
                {"name": "Consulting", "quantity": "1", "unit_price": "100,00", "line_total": "100,00"}
            ],
        }
    )

    result = parse_invoice("irrelevant ocr text", processor=fake_processor)

    assert result["net_total"] == 100.0
    assert result["gross_total"] == 119.0
    assert result["vat_amount"] == 19.0
    assert result["vat_rate"] == 19.0
    assert result["invoice_date"] == "2026-05-06"
    assert result["due_date"] == "2026-05-20"
    assert result["iban"] == "DE89370400440532013000"
    assert result["bic"] == "COBADEFFXXX"
    assert result["seller_vat_id"] == "DE123456789"
    assert result["currency"] == "EUR"
    assert result["seller_country"] == "DE"
    assert result["buyer_country"] == "DE"
    assert result["line_items"] == [
        {"name": "Consulting", "quantity": 1.0, "unit_price": 100.0, "line_total": 100.0}
    ]


def test_parse_invoice_prefers_regex_extracted_iban_over_ai_output():
    """The AI sometimes mistypes long alphanumeric strings; the regex draft must win."""
    ocr_text = (
        "Rechnungsdatum: 06.05.2026\n"
        "IBAN: DE89 3704 0044 0532 0130 00 | BIC: COBADEFFXXX\n"
    )
    fake_processor = _FakeProcessor(
        {
            "seller_name": "Seller GmbH",
            "buyer_name": "Buyer GmbH",
            "invoice_number": "INV-1",
            "invoice_date": "06.05.2026",
            "net_total": "100,00",
            "gross_total": "119,00",
            # Simulate the AI garbling the IBAN/BIC it retyped from the text.
            "iban": "DE00 0000 0000 0000 0000 00",
            "bic": "WRONGBIC",
        }
    )

    result = parse_invoice(ocr_text, processor=fake_processor)

    assert result["iban"] == "DE89370400440532013000"
    assert result["bic"] == "COBADEFFXXX"
    assert result["invoice_date"] == "2026-05-06"
