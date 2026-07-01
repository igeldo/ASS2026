"""Tests for controllers.invoice_mapper.InvoiceMapper."""

from decimal import Decimal

import pytest

from controllers.cii_generator import CIIBuilder
from controllers.invoice_mapper import InvoiceMapper, InvoiceMappingError
from controllers.xsd_validator import CIIXsdValidator

MINIMAL_DATA = {
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


def test_map_builds_valid_xsd_compliant_invoice_without_line_items_or_address():
    invoice = InvoiceMapper().map(MINIMAL_DATA)

    assert invoice.invoice.number == "INV-2026-001"
    assert invoice.seller.name == "Seller GmbH"
    assert invoice.seller.address is None
    assert invoice.payment.iban == "DE89370400440532013000"
    assert invoice.totals.tax_exclusive_amount == Decimal("100.0")
    assert len(invoice.lines) == 1
    assert invoice.lines[0].line_net_amount == Decimal("100.0")
    assert invoice.tax_breakdowns[0].rate == Decimal("19.0")

    result = CIIXsdValidator().validate(CIIBuilder().build(invoice))
    assert result["valid"] is True, result["errors"]


def test_map_uses_extracted_line_items_and_address_when_present():
    data = dict(MINIMAL_DATA)
    data["line_items"] = [
        {"name": "Consulting service", "quantity": 1.0, "unit_price": 100.0, "line_total": 100.0}
    ]
    data.update(
        seller_street="Seller Str. 1",
        seller_postcode="10115",
        seller_city="Berlin",
        seller_country="DE",
    )

    invoice = InvoiceMapper().map(data)

    assert len(invoice.lines) == 1
    assert invoice.lines[0].name == "Consulting service"
    assert invoice.lines[0].quantity == Decimal("1.0")
    assert invoice.seller.address is not None
    assert invoice.seller.address.city == "Berlin"


def test_map_raises_for_missing_required_fields():
    data = dict(MINIMAL_DATA)
    data["seller_name"] = None

    with pytest.raises(InvoiceMappingError) as exc_info:
        InvoiceMapper().map(data)

    assert "seller_name" in exc_info.value.missing_fields
