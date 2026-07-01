"""Tests for controllers.validator.EN16931Validator."""

from models.en16931 import GermanInvoice
from controllers.validator import EN16931Validator


def test_valid_invoice_passes(example_invoice_dict):
    invoice = GermanInvoice(**example_invoice_dict)

    result = EN16931Validator().validate(invoice)

    assert result["valid"] is True
    assert result["errors"] == []


def test_invoice_with_mismatched_totals_fails(example_invoice_dict):
    example_invoice_dict["totals"]["tax_exclusive_amount"] = "999.00"
    result = EN16931Validator().validate(GermanInvoice(**example_invoice_dict))
    assert result["valid"] is False
    assert any("tax_exclusive_amount" in error for error in result["errors"])

    example_invoice_dict["totals"]["tax_exclusive_amount"] = "100.00"
    example_invoice_dict["totals"]["payable_amount"] = "1.00"
    result = EN16931Validator().validate(GermanInvoice(**example_invoice_dict))
    assert result["valid"] is False
    assert any("payable_amount" in error for error in result["errors"])
