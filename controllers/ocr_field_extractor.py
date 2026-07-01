"""Deterministic, regex-based pre-extraction of high-confidence invoice fields.

These fields (IBAN, BIC, dates, VAT IDs) follow strict formats, so pattern
matching against the raw OCR text is more reliable than asking an LLM to
retype them (LLMs occasionally transpose digits/characters in long
alphanumeric strings). Fields that require semantic understanding (party
names, addresses, which amount is net/gross, which VAT ID belongs to whom)
are intentionally left for the AI step to fill in/verify.
"""

import logging
import re
from typing import Any, Dict, List, Optional

from controllers.datum_service import normalize_date

logger = logging.getLogger(__name__)

_IBAN_RE = re.compile(r"\b[A-Z]{2}\d{2}(?:[ ]?[A-Z0-9]{1,4}){2,7}\b")
_BIC_RE = re.compile(r"\bBIC\s*:?\s*([A-Z0-9]{8}(?:[A-Z0-9]{3})?)\b", re.IGNORECASE)
_VAT_ID_RE = re.compile(r"\b[A-Z]{2}\d{8,12}\b")
_DATE_RE = re.compile(r"\b\d{1,2}\.\d{1,2}\.\d{2,4}\b")

_DUE_DATE_LABELS = re.compile(
    r"(f(?:ä|ae|a)llig|zahlbar\s*bis|due\s*date)", re.IGNORECASE
)
_ISSUE_DATE_LABELS = re.compile(
    r"(rechnungsdatum|invoice\s*date|ausstellungsdatum|\bdatum\b)", re.IGNORECASE
)
# Recognized so its date gets consumed/skipped during sequential label<->date
# matching -- otherwise an unrecognized "Lieferdatum" between issue and due
# date labels shifts every later date assignment off by one.
_DELIVERY_DATE_LABELS = re.compile(
    r"(lieferdatum|delivery\s*date|leistungsdatum)", re.IGNORECASE
)


class OCRFieldExtractor:
    """
    Extracts IBAN, BIC, dates, and VAT ID candidates directly from raw OCR
    text via regex, without involving an LLM.

    The result is a "draft" dict meant to be handed to the AI extraction
    step, which verifies/corrects it and fills in everything that requires
    contextual understanding (see :class:`controllers.ai_service.BaseInvoiceAIProcessor`).
    """

    def extract(self, text: str) -> Dict[str, Any]:
        """
        Args:
            text: Raw OCR/plain text extracted from the invoice document.

        Returns:
            A dict with the keys ``iban``, ``bic``, ``invoice_date``,
            ``due_date``, ``vat_id_candidates`` (list), and ``currency``.
            Any field that couldn't be found is ``None`` (or an empty list
            for candidates).
        """
        invoice_date, due_date = self._find_dates(text)
        return {
            "iban": self._find_iban(text),
            "bic": self._find_bic(text),
            "invoice_date": invoice_date,
            "due_date": due_date,
            "vat_id_candidates": self._find_vat_id_candidates(text),
            "currency": self._find_currency(text),
        }

    def _find_iban(self, text: str) -> Optional[str]:
        for match in _IBAN_RE.finditer(text):
            candidate = match.group(0).replace(" ", "")
            if 15 <= len(candidate) <= 34:
                return candidate
        return None

    def _find_bic(self, text: str) -> Optional[str]:
        match = _BIC_RE.search(text)
        return match.group(1).upper() if match else None

    def _find_vat_id_candidates(self, text: str) -> List[str]:
        seen = []
        for match in _VAT_ID_RE.finditer(text):
            candidate = match.group(0)
            if candidate not in seen:
                seen.append(candidate)
        return seen

    def _find_currency(self, text: str) -> Optional[str]:
        if "€" in text or re.search(r"\bEUR\b", text, re.IGNORECASE):
            return "EUR"
        return None

    def _find_dates(self, text: str) -> "tuple[Optional[str], Optional[str]]":
        """
        Find the issue date and due date by matching labels to dates in text
        order.

        Handles both inline layouts (``Rechnungsdatum: 06.05.2026``) and
        OCR'd table layouts, where a header row (``Rechnungsdatum
        Falligkeitsdatum``) is followed by a separate value row
        (``06.05.2026 20.05.2026``) -- labels and dates are matched
        positionally in the order they appear. A "Lieferdatum" (delivery
        date) label in between is recognized (and its date skipped) so it
        doesn't shift the invoice/due date pairing off by one.
        """
        labels = sorted(
            [(m.start(), "invoice_date") for m in _ISSUE_DATE_LABELS.finditer(text)]
            + [(m.start(), "due_date") for m in _DUE_DATE_LABELS.finditer(text)]
            + [(m.start(), "delivery_date") for m in _DELIVERY_DATE_LABELS.finditer(text)]
        )
        dates = [m.group(0) for m in _DATE_RE.finditer(text)]

        result: Dict[str, Optional[str]] = {"invoice_date": None, "due_date": None, "delivery_date": None}
        for (_, field), raw_date in zip(labels, dates):
            if result[field] is None:
                result[field] = normalize_date(raw_date)

        return result["invoice_date"], result["due_date"]
