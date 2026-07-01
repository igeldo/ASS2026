"""Maps normalized AI-extracted invoice fields onto the structured GermanInvoice schema."""

import logging
from decimal import Decimal, InvalidOperation
from typing import Any, Dict, List, Optional

from pydantic import ValidationError

from models.en16931 import (
    Address,
    GermanInvoice,
    InvoiceHeader,
    InvoiceLine,
    Party,
    Payment,
    PaymentTerms,
    TaxBreakdown,
    Totals,
)

logger = logging.getLogger(__name__)

REQUIRED_FIELDS = ["invoice_number", "invoice_date", "seller_name", "buyer_name", "net_total", "gross_total"]


class InvoiceMappingError(Exception):
    """Raised when normalized AI fields cannot be assembled into a valid GermanInvoice."""

    def __init__(self, message: str, missing_fields: Optional[List[str]] = None) -> None:
        """
        Args:
            message: Human-readable summary of what went wrong.
            missing_fields: Names of the fields that made mapping impossible,
                so a caller (e.g. the API layer) can point the user at
                exactly what to fill in.
        """
        super().__init__(message)
        self.missing_fields = missing_fields or []


class InvoiceMapper:
    """
    Builds a best-effort :class:`GermanInvoice` from the flat fields produced
    by AI-based invoice extraction (see :mod:`controllers.invoice_parser`).

    Fields the AI could not determine (e.g. buyer address, individual line
    items) are either left empty (where the schema allows it) or filled
    with a single synthesized line item / tax breakdown derived from the
    invoice totals, so the result is always a valid, XML-generatable
    invoice. The caller is expected to let the user review/complete any
    gaps before generating XML or a Factur-X PDF.
    """

    DEFAULT_UNIT_CODE = "C62"
    DEFAULT_CATEGORY_CODE = "S"

    def map(self, data: Dict[str, Any]) -> GermanInvoice:
        """
        Args:
            data: Normalized fields as produced by
                :func:`controllers.invoice_parser.parse_invoice`.

        Returns:
            A validated :class:`GermanInvoice`.

        Raises:
            InvoiceMappingError: If required fields are missing, or the
                assembled data fails :class:`GermanInvoice` validation.
        """
        missing = [field for field in REQUIRED_FIELDS if not data.get(field)]
        if missing:
            raise InvoiceMappingError(
                f"Cannot build invoice, missing required fields: {', '.join(missing)}",
                missing_fields=missing,
            )

        try:
            return GermanInvoice(
                invoice=self._build_header(data),
                seller=self._build_party(data, "seller"),
                buyer=self._build_party(data, "buyer"),
                payment=self._build_payment(data),
                payment_terms=self._build_payment_terms(data),
                totals=self._build_totals(data),
                lines=self._build_lines(data),
                tax_breakdowns=[self._build_tax_breakdown(data)],
            )
        except ValidationError as exc:
            missing = sorted({".".join(str(p) for p in err["loc"]) for err in exc.errors()})
            raise InvoiceMappingError(
                f"Assembled invoice failed validation: {missing}", missing_fields=missing
            ) from exc

    @staticmethod
    def _decimal(value: Any, default: str = "0") -> Decimal:
        """Convert a float/str value to Decimal, falling back to ``default`` if unusable."""
        if value is None:
            return Decimal(default)
        try:
            return Decimal(str(value))
        except InvalidOperation:
            return Decimal(default)

    def _build_header(self, data: Dict[str, Any]) -> InvoiceHeader:
        return InvoiceHeader(
            number=data["invoice_number"],
            issue_date=data["invoice_date"],
            due_date=data.get("due_date"),
            currency=data.get("currency"),
        )

    def _build_party(self, data: Dict[str, Any], prefix: str) -> Party:
        postcode = data.get(f"{prefix}_postcode")
        line_one = data.get(f"{prefix}_street")
        city = data.get(f"{prefix}_city")

        address = None
        if postcode and line_one and city:
            address = Address(
                postcode=postcode,
                line_one=line_one,
                city=city,
                country_id=data.get(f"{prefix}_country"),
            )

        return Party(
            name=data[f"{prefix}_name"],
            vat_id=data.get(f"{prefix}_vat_id"),
            address=address,
        )

    def _build_payment(self, data: Dict[str, Any]) -> Optional[Payment]:
        iban = data.get("iban")
        bic = data.get("bic")
        if not iban and not bic:
            return None
        return Payment(iban=iban, bic=bic)

    def _build_payment_terms(self, data: Dict[str, Any]) -> Optional[PaymentTerms]:
        description = data.get("payment_terms")
        if not description:
            return None
        return PaymentTerms(description=description)

    def _build_totals(self, data: Dict[str, Any]) -> Totals:
        net = self._decimal(data.get("net_total"))
        gross = self._decimal(data.get("gross_total"))
        vat = self._decimal(data.get("vat_amount"), default=str(gross - net))
        return Totals(
            tax_exclusive_amount=net,
            tax_inclusive_amount=gross,
            tax_amount=vat,
            payable_amount=gross,
        )

    def _build_lines(self, data: Dict[str, Any]) -> List[InvoiceLine]:
        items = data.get("line_items") or []
        vat_rate = self._decimal(data.get("vat_rate"))

        if not items:
            return [
                InvoiceLine(
                    id="1",
                    name=f"Invoice {data['invoice_number']}",
                    quantity=Decimal("1"),
                    unit_code=self.DEFAULT_UNIT_CODE,
                    net_price=self._decimal(data.get("net_total")),
                    line_net_amount=self._decimal(data.get("net_total")),
                    tax_rate=vat_rate,
                )
            ]

        lines = []
        for index, item in enumerate(items, start=1):
            quantity = self._decimal(item.get("quantity"), default="1")
            line_total = self._decimal(item.get("line_total"))
            unit_price = self._decimal(item.get("unit_price"), default=str(line_total))
            lines.append(
                InvoiceLine(
                    id=str(index),
                    name=item.get("name") or f"Position {index}",
                    quantity=quantity,
                    unit_code=self.DEFAULT_UNIT_CODE,
                    net_price=unit_price,
                    line_net_amount=line_total,
                    tax_rate=vat_rate,
                )
            )
        return lines

    def _build_tax_breakdown(self, data: Dict[str, Any]) -> TaxBreakdown:
        return TaxBreakdown(
            category_code=self.DEFAULT_CATEGORY_CODE,
            rate=self._decimal(data.get("vat_rate")),
            basis_amount=self._decimal(data.get("net_total")),
            calculated_amount=self._decimal(data.get("vat_amount")),
        )
