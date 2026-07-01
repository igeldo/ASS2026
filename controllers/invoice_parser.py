"""Normalizes raw AI-extracted invoice fields into clean, typed values."""

import logging
from typing import Any, Dict, List, Optional

from controllers.ai_service import BaseInvoiceAIProcessor, get_default_ai_processor
from controllers.datum_service import normalize_date
from controllers.ocr_field_extractor import OCRFieldExtractor

logger = logging.getLogger(__name__)

_default_processor = get_default_ai_processor()
_field_extractor = OCRFieldExtractor()

# Common country names (as they appear on invoices) mapped to their
# ISO 3166-1 alpha-2 code, required by the CII XSD schema's CountryID field.
_COUNTRY_NAME_TO_ISO = {
    "deutschland": "DE",
    "germany": "DE",
    "österreich": "AT",
    "oesterreich": "AT",
    "austria": "AT",
    "schweiz": "CH",
    "switzerland": "CH",
    "frankreich": "FR",
    "france": "FR",
    "italien": "IT",
    "italy": "IT",
    "spanien": "ES",
    "spain": "ES",
    "niederlande": "NL",
    "netherlands": "NL",
    "belgien": "BE",
    "belgium": "BE",
    "polen": "PL",
    "poland": "PL",
}


def normalize_country(value: Optional[str]) -> Optional[str]:
    """
    Normalize a country name/code to an ISO 3166-1 alpha-2 code.

    Args:
        value: Raw country value from the AI model, e.g. "Deutschland",
            "Germany", or already an ISO code like "DE".

    Returns:
        The two-letter ISO code, or ``None`` if ``value`` is empty or not
        a recognized country name/code (callers should fall back to a
        sensible default rather than pass an unrecognized value into XML).
    """
    if not value:
        return None

    value = value.strip()
    if len(value) == 2 and value.isalpha():
        return value.upper()

    iso_code = _COUNTRY_NAME_TO_ISO.get(value.lower())
    if iso_code is None:
        logger.warning("Could not map country name to ISO code: %r", value)
    return iso_code


def to_float(value: Any) -> Optional[float]:
    """
    Convert a German-formatted currency string (e.g. "1.350,00 €") to a float.

    Args:
        value: Raw value as returned by the AI model. May be ``None``,
            a number, or a string containing currency symbols/German
            thousands separators.

    Returns:
        The parsed float, or ``None`` if ``value`` is ``None`` or cannot
        be parsed.
    """
    if value is None:
        return None

    value = str(value)
    value = value.replace("€", "").replace("EUR", "").replace(" ", "").strip()

    # German number format: 1.350,00 or 1350,00
    if "," in value:
        value = value.replace(".", "").replace(",", ".")

    try:
        return float(value)
    except ValueError:
        logger.warning("Could not parse numeric value: %r", value)
        return None


def fix_vat(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Recompute VAT amount and rate from net/gross totals when both are present.

    Args:
        data: Invoice field dictionary, expected to contain ``net_total``
            and ``gross_total`` as floats (or ``None``).

    Returns:
        The same dictionary with ``vat_amount`` and ``vat_rate`` updated
        in place when a valid net/gross pair is available.
    """
    net = data.get("net_total")
    gross = data.get("gross_total")

    if net is None or gross is None or net <= 0:
        return data

    vat_amount = round(gross - net, 2)
    vat_rate = round((vat_amount / net) * 100, 2)

    data["vat_amount"] = vat_amount
    data["vat_rate"] = vat_rate

    return data


def clean_iban(value: Optional[str]) -> Optional[str]:
    """Strip whitespace from an IBAN string, or return ``None`` if empty."""
    if not value:
        return None

    return str(value).replace(" ", "").strip()


def clean_vat_id(value: Optional[str]) -> Optional[str]:
    """Strip whitespace from a VAT ID string, or return ``None`` if empty."""
    if not value:
        return None

    return str(value).replace(" ", "").strip()


# BIC/SWIFT codes and VAT IDs are formatted the same way (strip whitespace).
clean_bic = clean_vat_id


def normalize_line_items(items: Any) -> List[Dict[str, Any]]:
    """
    Normalize a raw ``line_items`` array from the AI model.

    Args:
        items: Raw value of the ``line_items`` field. Expected to be a list
            of dicts with ``name``, ``quantity``, ``unit_price``, and
            ``line_total``, but tolerates ``None``/malformed input.

    Returns:
        A list of normalized line item dicts (numeric fields as floats).
        Items missing a ``name`` or all numeric fields are dropped.
    """
    if not isinstance(items, list):
        return []

    normalized = []
    for item in items:
        if not isinstance(item, dict) or not item.get("name"):
            continue

        quantity = to_float(item.get("quantity"))
        unit_price = to_float(item.get("unit_price"))
        line_total = to_float(item.get("line_total"))

        if quantity is None and unit_price is None and line_total is None:
            continue

        normalized.append(
            {
                "name": str(item["name"]).strip(),
                "quantity": quantity,
                "unit_price": unit_price,
                "line_total": line_total,
            }
        )

    return normalized


def parse_invoice(
    text: str,
    processor: Optional[BaseInvoiceAIProcessor] = None,
) -> Dict[str, Any]:
    """
    Extract and normalize invoice fields from raw OCR text.

    Deterministic, regex-based pre-extraction (IBAN, BIC, dates, VAT ID
    candidates -- see :class:`controllers.ocr_field_extractor.OCRFieldExtractor`)
    runs first, since these strict-format fields are more reliably read via
    pattern matching than by an LLM. The AI extraction step then verifies
    and completes this draft (party names, addresses, amounts, line items).
    After the AI responds, the pre-extracted IBAN/BIC/dates are restored
    verbatim whenever the regex scan found them, so the AI can never
    introduce a typo/transposition in these fields.

    Args:
        text: Raw OCR/plain text extracted from the invoice document.
        processor: Optional AI processor instance to use (Ollama- or
            Gemini-backed). Defaults to a module-level shared instance.

    Returns:
        A dictionary of normalized invoice fields.

    Raises:
        AIConnectionError: If the Ollama endpoint could not be reached.
        AIResponseError: If Ollama returned an invalid/unparsable payload.
    """
    ai_processor = processor or _default_processor
    draft = _field_extractor.extract(text)
    ai_data = ai_processor.extract(text, draft=draft)

    ai_data["net_total"] = to_float(ai_data.get("net_total"))
    ai_data["gross_total"] = to_float(ai_data.get("gross_total"))
    ai_data["vat_amount"] = to_float(ai_data.get("vat_amount"))

    ai_data = fix_vat(ai_data)

    ai_data["invoice_date"] = normalize_date(ai_data.get("invoice_date"))
    ai_data["due_date"] = normalize_date(ai_data.get("due_date"))

    ai_data["iban"] = clean_iban(ai_data.get("iban"))
    ai_data["bic"] = clean_bic(ai_data.get("bic"))
    ai_data["seller_vat_id"] = clean_vat_id(ai_data.get("seller_vat_id"))
    ai_data["buyer_vat_id"] = clean_vat_id(ai_data.get("buyer_vat_id"))

    ai_data["seller_country"] = normalize_country(ai_data.get("seller_country"))
    ai_data["buyer_country"] = normalize_country(ai_data.get("buyer_country"))

    ai_data["line_items"] = normalize_line_items(ai_data.get("line_items"))

    ai_data["currency"] = "EUR"

    # Regex-extracted values are guaranteed to match the source text
    # verbatim, so they take precedence over whatever the AI returned.
    for field in ("iban", "bic", "invoice_date", "due_date"):
        if draft.get(field):
            ai_data[field] = draft[field]

    logger.info("Parsed and normalized invoice fields")
    return ai_data
