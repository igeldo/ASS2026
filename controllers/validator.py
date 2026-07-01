"""EN16931 business-rule validation for structured invoices."""

import logging
from typing import Any, Dict, List

from models.en16931 import GermanInvoice

logger = logging.getLogger(__name__)


class EN16931Validator:
    """
    Validates a :class:`GermanInvoice` against a core subset of EN16931
    business rules (totals consistency, tax breakdown consistency).

    This is a lightweight arithmetic cross-check, not a full implementation
    of the EN16931 rule set (e.g. BR-CO-* rules). It is intended to catch
    obvious inconsistencies before CII XML generation and XSD validation.
    """

    def validate(self, invoice: GermanInvoice) -> Dict[str, Any]:
        """
        Run business-rule validation against the given invoice.

        Args:
            invoice: The structured invoice to validate.

        Returns:
            A dictionary with ``valid`` (bool) and ``errors`` (list of
            human-readable rule violation messages).
        """
        errors: List[str] = []

        line_sum = sum(line.line_net_amount for line in invoice.lines)
        if line_sum != invoice.totals.tax_exclusive_amount:
            errors.append("Sum of line_net_amount must equal tax_exclusive_amount")

        tax_sum = sum(tax.calculated_amount for tax in invoice.tax_breakdowns)
        if tax_sum != invoice.totals.tax_amount:
            errors.append("Sum of tax_breakdowns.calculated_amount must equal tax_amount")

        calculated_gross = invoice.totals.tax_exclusive_amount + invoice.totals.tax_amount
        if calculated_gross != invoice.totals.tax_inclusive_amount:
            errors.append("tax_exclusive_amount + tax_amount must equal tax_inclusive_amount")

        if invoice.totals.payable_amount != invoice.totals.tax_inclusive_amount:
            errors.append(
                "payable_amount must equal tax_inclusive_amount for invoices without prepaid amount"
            )

        if errors:
            logger.info("EN16931 validation failed for invoice %s: %s", invoice.invoice.number, errors)
        else:
            logger.debug("EN16931 validation passed for invoice %s", invoice.invoice.number)

        return {
            "valid": len(errors) == 0,
            "errors": errors,
        }
