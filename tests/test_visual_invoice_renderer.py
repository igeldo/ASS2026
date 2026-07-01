"""Tests for controllers.visual_invoice_renderer.VisualInvoiceRenderer."""

import fitz
import pytest

from models.en16931 import GermanInvoice
from controllers.visual_invoice_renderer import UnknownTemplateError, VisualInvoiceRenderer


def test_render_shows_real_invoice_data_for_each_template(example_invoice_dict):
    invoice = GermanInvoice(**example_invoice_dict)

    for template_id in (1, 2, 3):
        pdf_bytes = VisualInvoiceRenderer().render(invoice, template_id)

        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        page_text = doc[0].get_text()

        assert invoice.seller.name in page_text
        assert invoice.buyer.name in page_text
        assert invoice.invoice.number in page_text
        assert invoice.lines[0].name in page_text
        assert "[siehe XML]" not in page_text
        assert "[Kaeufername]" not in page_text


def test_render_raises_for_unknown_template_id(example_invoice_dict):
    invoice = GermanInvoice(**example_invoice_dict)

    with pytest.raises(UnknownTemplateError):
        VisualInvoiceRenderer().render(invoice, 99)


def test_render_handles_missing_optional_fields(example_invoice_dict):
    example_invoice_dict["buyer"]["address"] = None
    example_invoice_dict["payment"] = None
    example_invoice_dict["payment_terms"] = None
    invoice = GermanInvoice(**example_invoice_dict)

    pdf_bytes = VisualInvoiceRenderer().render(invoice, 1)

    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    assert invoice.buyer.name in doc[0].get_text()
