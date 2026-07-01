"""AI-based invoice field extraction, via a local Ollama LLM or the Gemini API."""

import json
import logging
import os
import re
import time
from typing import Any, Dict, Optional

import requests

logger = logging.getLogger(__name__)


class AIServiceError(Exception):
    """Base exception for failures during AI-based invoice extraction."""


class AIConnectionError(AIServiceError):
    """Raised when the AI backend cannot be reached or times out."""


class AIResponseError(AIServiceError):
    """Raised when the AI backend returns a response that is missing, malformed, or not valid JSON."""


class BaseInvoiceAIProcessor:
    """
    Shared prompt-building logic for invoice field extraction.

    Subclasses implement :meth:`extract` against a specific LLM backend
    (Ollama, Gemini, ...) but all send the same extraction prompt and
    return the same raw field dictionary.
    """

    def _build_prompt(self, text: str, draft: Optional[Dict[str, Any]] = None) -> str:
        """
        Build the extraction prompt sent to the LLM.

        Args:
            text: Raw OCR/plain text extracted from the invoice document.
            draft: Optional pre-extracted fields from
                :class:`controllers.ocr_field_extractor.OCRFieldExtractor`
                (IBAN, BIC, dates, VAT ID candidates found via regex). When
                given, the model is asked to verify/correct these instead
                of extracting them from scratch.

        Returns:
            The fully formatted prompt string, including the target JSON
            schema and the invoice text to analyze.
        """
        draft_section = ""
        if draft:
            draft_section = f"""
A preliminary automated scan already found these values by pattern
matching. Verify each one against the text below and correct it if it
looks wrong; if a value is null, try to determine it yourself from the
text. If "vat_id_candidates" has entries, assign the correct one to
"seller_vat_id" and, if there is another, to "buyer_vat_id" based on
context (which company issued the invoice).

Pre-scanned values:
{json.dumps(draft, ensure_ascii=False)}

"""

        return f"""
You are an invoice extraction API.

Return ONLY valid JSON. Use null for anything you cannot find in the text.
Do not guess values that are not present in the text.
{draft_section}
Fields:
{{
    "invoice_number": null,
    "invoice_date": null,
    "due_date": null,
    "currency": null,

    "seller_name": null,
    "seller_vat_id": null,
    "seller_street": null,
    "seller_postcode": null,
    "seller_city": null,
    "seller_country": null,

    "buyer_name": null,
    "buyer_vat_id": null,
    "buyer_street": null,
    "buyer_postcode": null,
    "buyer_city": null,
    "buyer_country": null,

    "iban": null,
    "bic": null,
    "payment_terms": null,

    "net_total": null,
    "gross_total": null,
    "vat_amount": null,
    "vat_rate": null,

    "line_items": [
        {{
            "name": null,
            "quantity": null,
            "unit_price": null,
            "line_total": null
        }}
    ]
}}

If the invoice lists individual line items/positions, extract each one into
"line_items". If not, return an empty list for "line_items".

Text:
{text}
"""

    def extract(self, text: str, draft: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Extract raw invoice fields from OCR text. Implemented by subclasses."""
        raise NotImplementedError


class InvoiceAIProcessor(BaseInvoiceAIProcessor):
    """
    Extracts structured invoice fields from raw OCR/plain text using a local
    Ollama LLM instance.

    Attributes:
        base_url: Base URL of the Ollama server (e.g. "http://localhost:11434").
        model: Name of the Ollama model to use for extraction.
        timeout: Request timeout in seconds for the Ollama HTTP call.
    """

    DEFAULT_BASE_URL = "http://localhost:11434"
    DEFAULT_MODEL = "qwen3:8b"
    DEFAULT_TIMEOUT = 120

    def __init__(
        self,
        base_url: str = DEFAULT_BASE_URL,
        model: str = DEFAULT_MODEL,
        timeout: int = DEFAULT_TIMEOUT,
    ) -> None:
        """
        Initialize the AI processor.

        Args:
            base_url: Base URL of the Ollama server.
            model: Name of the Ollama model to use for extraction.
            timeout: Request timeout in seconds.
        """
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout = timeout

    def extract(self, text: str, draft: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Send OCR text to the local LLM and parse the structured JSON response.

        Args:
            text: Raw OCR/plain text extracted from the invoice document.
            draft: Optional pre-extracted fields to verify/complete (see
                :class:`BaseInvoiceAIProcessor._build_prompt`).

        Returns:
            A dictionary with the raw fields extracted by the model.

        Raises:
            AIConnectionError: If the Ollama endpoint could not be reached
                or the request timed out.
            AIResponseError: If Ollama returned an HTTP error, a non-JSON
                payload, or a payload that does not contain a usable
                'response' field.
        """
        prompt = self._build_prompt(text, draft)
        logger.debug("Sending extraction request to Ollama model '%s'", self.model)

        try:
            res = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "format": "json",
                    "stream": False,
                },
                timeout=self.timeout,
            )
            res.raise_for_status()
        except requests.exceptions.ConnectionError as exc:
            logger.error("Could not connect to Ollama at %s", self.base_url)
            raise AIConnectionError(
                f"Ollama service unreachable at {self.base_url}"
            ) from exc
        except requests.exceptions.Timeout as exc:
            logger.error("Ollama request timed out after %ss", self.timeout)
            raise AIConnectionError("Ollama request timed out") from exc
        except requests.exceptions.HTTPError as exc:
            logger.error("Ollama returned an HTTP error: %s", exc)
            raise AIResponseError(f"Ollama returned an error status: {exc}") from exc

        try:
            envelope = res.json()
        except json.JSONDecodeError as exc:
            logger.error("Ollama response envelope was not valid JSON")
            raise AIResponseError("Ollama returned a non-JSON response") from exc

        raw_response = envelope.get("response")
        if not raw_response:
            logger.error("Ollama response envelope missing 'response' field: %s", envelope)
            raise AIResponseError("Ollama response did not contain a 'response' field")

        data = self._parse_model_json(raw_response)
        logger.info("AI extraction succeeded (model=%s)", self.model)
        return data

    @staticmethod
    def _strip_code_fences(text: str) -> str:
        """Remove a surrounding ```json ... ``` / ``` ... ``` markdown fence, if present."""
        text = text.strip()
        text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
        text = re.sub(r"\s*```$", "", text)
        return text.strip()

    @staticmethod
    def _extract_json_object(text: str) -> str:
        """Slice out the outermost {...} object, in case the model added surrounding prose."""
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1 and end > start:
            return text[start : end + 1]
        return text

    @classmethod
    def _parse_model_json(cls, raw_response: str) -> Dict[str, Any]:
        """
        Parse the model's raw text output as a JSON object.

        LLMs occasionally wrap JSON in markdown code fences or add stray
        prose around it despite being asked for raw JSON. This tries a few
        increasingly lenient extraction strategies before giving up.
        """
        stripped = cls._strip_code_fences(raw_response)
        candidates = [raw_response, stripped, cls._extract_json_object(stripped)]

        last_error: Exception = ValueError("empty model output")
        for candidate in candidates:
            try:
                data = json.loads(candidate)
            except json.JSONDecodeError as exc:
                last_error = exc
                continue

            if isinstance(data, dict):
                return data
            last_error = ValueError("Model output JSON was not a JSON object")

        preview = raw_response[:500]
        logger.error("Model output could not be parsed as JSON: %s", raw_response)
        raise AIResponseError(
            f"Model output could not be parsed as JSON. Raw output (truncated): {preview!r}"
        ) from last_error


class GeminiAIProcessor(BaseInvoiceAIProcessor):
    """
    Extracts structured invoice fields using Google's Gemini API (free tier).

    Get a free API key at https://aistudio.google.com/apikey and set it via
    the ``GEMINI_API_KEY`` environment variable, or pass it explicitly.

    Attributes:
        api_key: Gemini API key.
        model: Gemini model name (e.g. "gemini-flash-latest").
        timeout: Request timeout in seconds.
    """

    DEFAULT_MODEL = "gemini-flash-latest"
    DEFAULT_TIMEOUT = 120
    API_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models"
    MAX_OVERLOAD_RETRIES = 2
    OVERLOAD_RETRY_DELAY_SECONDS = 3

    def __init__(
        self,
        api_key: str,
        model: str = DEFAULT_MODEL,
        timeout: int = DEFAULT_TIMEOUT,
    ) -> None:
        """
        Initialize the Gemini processor.

        Args:
            api_key: Gemini API key.
            model: Gemini model name to use for extraction.
            timeout: Request timeout in seconds.
        """
        self.api_key = api_key
        self.model = model
        self.timeout = timeout

    def extract(self, text: str, draft: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Send OCR text to the Gemini API and parse the structured JSON response.

        Args:
            text: Raw OCR/plain text extracted from the invoice document.
            draft: Optional pre-extracted fields to verify/complete (see
                :class:`BaseInvoiceAIProcessor._build_prompt`).

        Returns:
            A dictionary with the raw fields extracted by the model.

        Raises:
            AIConnectionError: If the Gemini API could not be reached or
                the request timed out.
            AIResponseError: If Gemini returned an HTTP error (e.g. invalid
                API key, rate limit), blocked the response, or returned an
                unusable/non-JSON payload.
        """
        prompt = self._build_prompt(text, draft)
        logger.debug("Sending extraction request to Gemini model '%s'", self.model)

        res = None
        for attempt in range(self.MAX_OVERLOAD_RETRIES + 1):
            try:
                res = requests.post(
                    f"{self.API_BASE_URL}/{self.model}:generateContent",
                    headers={"x-goog-api-key": self.api_key},
                    json={
                        "contents": [{"parts": [{"text": prompt}]}],
                        "generationConfig": {"response_mime_type": "application/json"},
                    },
                    timeout=self.timeout,
                )
                res.raise_for_status()
                break
            except requests.exceptions.ConnectionError as exc:
                logger.error("Could not connect to Gemini API")
                raise AIConnectionError("Gemini API unreachable") from exc
            except requests.exceptions.Timeout as exc:
                logger.error("Gemini request timed out after %ss", self.timeout)
                raise AIConnectionError("Gemini request timed out") from exc
            except requests.exceptions.HTTPError as exc:
                # The API key is sent via header (never in the URL), so it's safe
                # to include the status/body here without leaking credentials.
                status = exc.response.status_code if exc.response is not None else None
                if status == 503 and attempt < self.MAX_OVERLOAD_RETRIES:
                    logger.warning(
                        "Gemini overloaded (503), retrying in %ss (attempt %d/%d)",
                        self.OVERLOAD_RETRY_DELAY_SECONDS,
                        attempt + 1,
                        self.MAX_OVERLOAD_RETRIES,
                    )
                    time.sleep(self.OVERLOAD_RETRY_DELAY_SECONDS)
                    continue
                logger.error("Gemini returned an HTTP error: %s", exc)
                raise AIResponseError(f"Gemini returned HTTP {status}") from exc

        try:
            envelope = res.json()
        except json.JSONDecodeError as exc:
            logger.error("Gemini response envelope was not valid JSON")
            raise AIResponseError("Gemini returned a non-JSON response") from exc

        candidates = envelope.get("candidates") or []
        if not candidates:
            block_reason = envelope.get("promptFeedback", {}).get("blockReason")
            logger.error("Gemini returned no candidates (blockReason=%s): %s", block_reason, envelope)
            raise AIResponseError(f"Gemini returned no result (blockReason={block_reason})")

        parts = candidates[0].get("content", {}).get("parts") or []
        raw_response = parts[0].get("text") if parts else None
        if not raw_response:
            logger.error("Gemini candidate had no text part: %s", envelope)
            raise AIResponseError("Gemini response did not contain any text")

        data = InvoiceAIProcessor._parse_model_json(raw_response)
        logger.info("AI extraction succeeded (model=%s)", self.model)
        return data


class FallbackAIProcessor(BaseInvoiceAIProcessor):
    """
    Tries a primary AI processor first, and only falls back to a secondary
    one if the primary is unreachable or errors out.

    Used to prefer the local, free Ollama backend when it's running, while
    still working automatically (via Gemini) when it isn't.
    """

    def __init__(self, primary: BaseInvoiceAIProcessor, fallback: BaseInvoiceAIProcessor) -> None:
        """
        Args:
            primary: Processor tried first.
            fallback: Processor used if ``primary.extract()`` raises an
                :class:`AIServiceError`.
        """
        self.primary = primary
        self.fallback = fallback

    def extract(self, text: str, draft: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Extract invoice fields via the primary processor, falling back to
        the secondary one on any :class:`AIServiceError`.

        Args:
            text: Raw OCR/plain text extracted from the invoice document.
            draft: Optional pre-extracted fields to verify/complete (see
                :class:`BaseInvoiceAIProcessor._build_prompt`).

        Returns:
            A dictionary with the raw fields extracted by whichever
            processor succeeded.

        Raises:
            AIServiceError: If both the primary and fallback processor fail.
        """
        try:
            return self.primary.extract(text, draft)
        except AIServiceError as exc:
            logger.warning(
                "%s failed (%s), falling back to %s",
                type(self.primary).__name__,
                exc,
                type(self.fallback).__name__,
            )
            return self.fallback.extract(text, draft)


def get_default_ai_processor() -> BaseInvoiceAIProcessor:
    """
    Build the default AI processor based on environment configuration.

    Always prefers the local, free Ollama backend. If ``GEMINI_API_KEY`` is
    set, Gemini is wired up as an automatic fallback for when Ollama isn't
    running or fails -- no manual switching required. Without a Gemini key,
    only Ollama is used (unchanged behavior).

    Returns:
        A configured AI processor instance.
    """
    ollama = InvoiceAIProcessor()

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        logger.info("GEMINI_API_KEY not set, using local Ollama AI processor only")
        return ollama

    model = os.environ.get("GEMINI_MODEL", GeminiAIProcessor.DEFAULT_MODEL)
    gemini = GeminiAIProcessor(api_key=api_key, model=model)
    logger.info("Using Ollama with automatic Gemini fallback (model=%s)", model)
    return FallbackAIProcessor(primary=ollama, fallback=gemini)
