"""Tests for CIIBuilder / CIIXsdValidator / CIIXmlParser working together."""

from decimal import Decimal

import pytest

from models.en16931 import GermanInvoice
from controllers.cii_generator import CIIBuilder
from controllers.cii_parser import CIIXmlParser
from controllers.xsd_validator import CIIXsdValidator


def test_generated_xml_is_xsd_valid_and_contains_expected_values(example_invoice_dict):
    invoice = GermanInvoice(**example_invoice_dict)

    xml = CIIBuilder().build(invoice)
    result = CIIXsdValidator().validate(xml)

    assert result["valid"] is True, result["errors"]
    assert invoice.invoice.number in xml
    assert invoice.seller.name in xml
    assert invoice.buyer.name in xml
    assert invoice.payment.iban in xml


def test_roundtrip_preserves_core_fields(example_invoice_dict):
    invoice = GermanInvoice(**example_invoice_dict)

    xml = CIIBuilder().build(invoice)
    parsed = CIIXmlParser().parse(xml)

    assert parsed.invoice.number == invoice.invoice.number
    assert parsed.invoice.issue_date == invoice.invoice.issue_date
    assert parsed.seller.name == invoice.seller.name
    assert parsed.buyer.name == invoice.buyer.name
    assert parsed.payment.iban == invoice.payment.iban
    assert parsed.totals.tax_exclusive_amount == invoice.totals.tax_exclusive_amount
    assert parsed.totals.payable_amount == invoice.totals.payable_amount
    assert len(parsed.lines) == len(invoice.lines)
    assert parsed.lines[0].line_net_amount == Decimal(invoice.lines[0].line_net_amount)


def test_invalid_xml_is_rejected_by_validator_and_parser():
    result = CIIXsdValidator().validate("<not-a-cii-document/>")
    assert result["valid"] is False
    assert result["errors"]

    with pytest.raises(ValueError):
        CIIXmlParser().parse("<unclosed")
