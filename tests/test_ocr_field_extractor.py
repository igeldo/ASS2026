"""Tests for controllers.ocr_field_extractor.OCRFieldExtractor."""

from controllers.ocr_field_extractor import OCRFieldExtractor

TABLE_LAYOUT_TEXT = """RECHNUNG Seller GmbH
Rechnungsempfanger: Absender:
Buyer GmbH Seller GmbH
Rechnungsnummer Rechnungsdatum Falligkeitsdatum
INV-2026-001 06.05.2026 20.05.2026
Summe Netto: 100,00 EUR
IBAN: DE89 3704 0044 0532 0130 00 | BIC: COBADEFFXXX
USt-IdNr.: DE123456789
"""

INLINE_LAYOUT_TEXT = "Rechnungsdatum: 01.02.2026\nFaelligkeitsdatum: 15.02.2026\n"


def test_extract_finds_iban_bic_vat_id_and_currency():
    result = OCRFieldExtractor().extract(TABLE_LAYOUT_TEXT)

    assert result["iban"] == "DE89370400440532013000"
    assert result["bic"] == "COBADEFFXXX"
    assert result["vat_id_candidates"] == ["DE123456789"]
    assert result["currency"] == "EUR"


def test_extract_finds_dates_in_table_layout():
    result = OCRFieldExtractor().extract(TABLE_LAYOUT_TEXT)

    assert result["invoice_date"] == "2026-05-06"
    assert result["due_date"] == "2026-05-20"


def test_extract_finds_dates_with_ae_digraph_and_inline_layout():
    result = OCRFieldExtractor().extract(INLINE_LAYOUT_TEXT)

    assert result["invoice_date"] == "2026-02-01"
    assert result["due_date"] == "2026-02-15"


def test_extract_returns_none_and_empty_list_when_nothing_found():
    result = OCRFieldExtractor().extract("just some unrelated text with no fields")

    assert result["iban"] is None
    assert result["bic"] is None
    assert result["invoice_date"] is None
    assert result["due_date"] is None
    assert result["vat_id_candidates"] == []
    assert result["currency"] is None


def test_extract_recognizes_plain_datum_label_as_issue_date():
    text = "Freie Grafikdesignerin Datum: 03.02.2026\nFaellig bis: 17.02.2026\n"

    result = OCRFieldExtractor().extract(text)

    assert result["invoice_date"] == "2026-02-03"
    assert result["due_date"] == "2026-02-17"


def test_extract_skips_delivery_date_between_issue_and_due_date():
    """A Lieferdatum between issue/due date labels must not shift due_date's match."""
    text = "Rechnungsdatum Lieferdatum Faelligkeitsdatum\n01.01.2026 02.01.2026 15.01.2026\n"

    result = OCRFieldExtractor().extract(text)

    assert result["invoice_date"] == "2026-01-01"
    assert result["due_date"] == "2026-01-15"
