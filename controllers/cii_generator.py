"""Builds ZUGFeRD/Factur-X CII (Cross Industry Invoice) XML from a structured invoice."""

import logging
from xml.etree.ElementTree import Element, SubElement

from models.en16931 import GermanInvoice
from controllers.builders.common import add_text, code_or_default, pretty_xml, qname
from controllers.builders.header_builder import (
    build_document_context,
    build_exchanged_document,
    build_header_delivery,
)
from controllers.builders.line_builder import build_line_items
from controllers.builders.party_builder import build_header_agreement
from controllers.builders.payment_builder import build_payment_means, build_payment_terms
from controllers.builders.tax_builder import build_header_taxes, build_monetary_summation

logger = logging.getLogger(__name__)


class CIIBuilder:
    """
    Builds a ZUGFeRD/Factur-X compliant CII XML document from a
    :class:`GermanInvoice`.

    Delegates the construction of individual XML fragments (document
    context, header agreement, line items, taxes, payment means, ...) to
    the helper functions in :mod:`controllers.builders`, and assembles them
    into the final ``CrossIndustryInvoice`` document.
    """

    DEFAULT_CURRENCY = "EUR"

    def build(self, invoice: GermanInvoice) -> str:
        """
        Build the pretty-printed CII XML string for the given invoice.

        Args:
            invoice: The structured invoice to serialize.

        Returns:
            The CII XML document as a formatted string.
        """
        root = Element(qname("rsm", "CrossIndustryInvoice"))

        build_document_context(root)
        build_exchanged_document(root, invoice.invoice)

        transaction = SubElement(root, qname("rsm", "SupplyChainTradeTransaction"))
        build_line_items(transaction, invoice.lines)
        build_header_agreement(transaction, invoice)
        build_header_delivery(transaction, invoice.invoice)

        header_settlement = SubElement(
            transaction,
            qname("ram", "ApplicableHeaderTradeSettlement"),
        )

        currency = code_or_default(invoice.invoice.currency, self.DEFAULT_CURRENCY)

        add_text(header_settlement, "ram", "InvoiceCurrencyCode", currency)
        build_payment_means(header_settlement, invoice.payment)
        build_header_taxes(header_settlement, invoice.tax_breakdowns)
        build_payment_terms(header_settlement, invoice.payment_terms, invoice.invoice)
        build_monetary_summation(header_settlement, invoice.totals, currency)

        xml = pretty_xml(root)
        logger.info("Generated CII XML for invoice %s", invoice.invoice.number)
        return xml
