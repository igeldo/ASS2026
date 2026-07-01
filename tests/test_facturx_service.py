"""Tests for controllers.facturx_service.FacturXPdfBuilder."""

import fitz
import pytest

from models.en16931 import GermanInvoice
from controllers.cii_generator import CIIBuilder
from controllers.facturx_service import FacturXError, FacturXPdfBuilder


def _blank_pdf() -> bytes:
    doc = fitz.open()
    doc.new_page()
    return doc.tobytes()


def test_build_embeds_xml_into_pdf(example_invoice_dict):
    invoice = GermanInvoice(**example_invoice_dict)
    xml = CIIBuilder().build(invoice)

    result = FacturXPdfBuilder().build(_blank_pdf(), xml)

    doc = fitz.open(stream=result, filetype="pdf")
    filenames = [doc.embfile_info(i)["filename"] for i in range(doc.embfile_count())]
    assert "factur-x.xml" in filenames


def test_build_raises_clear_error_for_non_pdf_input():
    with pytest.raises(FacturXError, match="not a valid PDF"):
        FacturXPdfBuilder().build(b"not a pdf", "<not-xml/>")

    with pytest.raises(FacturXError, match="not a valid PDF"):
        FacturXPdfBuilder().build(b"\xff\xd8\xff\xe0", "<not-xml/>")  # JPEG signature
