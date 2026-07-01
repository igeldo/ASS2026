"""FastAPI application entrypoint for the German Invoice OCR API.

Sets up the central logging configuration used by all services, wires up
the HTTP routes for OCR/AI invoice extraction and ZUGFeRD/Factur-X CII
generation & validation, and serves a small local HTML/JS upload UI.
"""

import logging
from typing import Any, Dict, List, Optional, Union

from fastapi import FastAPI, Form, HTTPException, Query, Request, UploadFile, File
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse, JSONResponse, Response
from pydantic import ValidationError

from models.en16931 import GermanInvoice
from controllers.ai_service import AIConnectionError, AIResponseError
from controllers.cii_generator import CIIBuilder
from controllers.cii_parser import CIIXmlParser
from controllers.facturx_service import FacturXError, FacturXPdfBuilder
from controllers.invoice_mapper import InvoiceMapper, InvoiceMappingError
from controllers.invoice_number_sequencer import InvoiceNumberSequencer
from controllers.invoice_parser import parse_invoice
from controllers.ocr_service import OCRExtractionError, OCRProcessor
from controllers.validator import EN16931Validator
from controllers.visual_invoice_renderer import UnknownTemplateError, VisualInvoiceRenderer
from controllers.xsd_validator import CIIXsdValidator
from views.upload_page import UPLOAD_PAGE_HTML

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
)
logger = logging.getLogger("invoice_api")

app = FastAPI(title="German Invoice OCR API")

ocr_processor = OCRProcessor()
cii_builder = CIIBuilder()
cii_parser = CIIXmlParser()
en16931_validator = EN16931Validator()
xsd_validator = CIIXsdValidator()
facturx_builder = FacturXPdfBuilder()
invoice_mapper = InvoiceMapper()
invoice_number_sequencer = InvoiceNumberSequencer()
visual_invoice_renderer = VisualInvoiceRenderer()


def api_response(
    data: Optional[Any] = None,
    errors: Optional[List[Any]] = None,
    meta: Optional[Dict[str, Any]] = None,
    success: bool = True,
) -> Dict[str, Any]:
    """
    Build the API's standard JSON response envelope.

    Args:
        data: Payload to return on success.
        errors: List of error entries (strings or dicts). Defaults to an
            empty list.
        meta: Additional metadata (e.g. filename, version).
        success: Whether the request succeeded.

    Returns:
        A dictionary with the keys ``success``, ``data``, ``errors`` and
        ``meta``.
    """
    return {
        "success": success,
        "data": data,
        "errors": errors or [],
        "meta": meta or {},
    }


def error_response(errors: Union[str, List[Any]], status_code: int = 400) -> JSONResponse:
    """
    Build a JSON error response using the standard envelope.

    Args:
        errors: A single error message or a list of error entries.
        status_code: HTTP status code to return.

    Returns:
        A :class:`JSONResponse` with ``success: false`` and the given errors.
    """
    if isinstance(errors, str):
        errors = [errors]

    return JSONResponse(
        status_code=status_code,
        content=api_response(data=None, errors=errors, success=False),
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Convert raised :class:`HTTPException` instances into the standard error envelope."""
    logger.warning("HTTPException on %s: %s", request.url.path, exc.detail)
    return error_response(exc.detail, exc.status_code)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Convert FastAPI/Pydantic request validation errors into the standard error envelope."""
    errors = [
        {
            "field": ".".join(str(part) for part in error["loc"]),
            "message": error["msg"],
            "type": error["type"],
        }
        for error in exc.errors()
    ]
    logger.warning("Validation error on %s: %s", request.url.path, errors)
    return error_response(errors, 422)


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Catch-all handler for unexpected exceptions; logs the full traceback."""
    logger.exception("Unhandled exception on %s", request.url.path)
    return error_response("Internal server error", 500)


@app.get("/")
def home() -> Dict[str, Any]:
    """Return a basic liveness/info payload for the API."""
    return api_response(
        data={"message": "German Invoice OCR API is running"},
        meta={"version": "v1"},
    )


@app.get("/health")
def health() -> Dict[str, Any]:
    """Return a simple health-check payload."""
    return api_response(data={"status": "ok"})


@app.get("/ui", response_class=HTMLResponse, include_in_schema=False)
def ui() -> HTMLResponse:
    """Serve the local drag-and-drop HTML/JS interface for manual testing."""
    return HTMLResponse(content=UPLOAD_PAGE_HTML)


@app.post("/api/v1/invoices/extract")
async def extract_invoice(file: UploadFile = File(...)) -> Dict[str, Any]:
    """
    Extract structured invoice data from an uploaded PDF or image file.

    The file is OCR'd (PyMuPDF for text-based PDFs, Tesseract otherwise),
    then the resulting text is sent to a local Ollama model for structured
    field extraction.

    Args:
        file: Uploaded invoice file (PDF, JPG, or PNG).

    Returns:
        The standard response envelope containing the extracted invoice
        fields and the raw OCR text.

    Raises:
        HTTPException: 400 if the file could not be OCR'd, 503 if the local
            AI service (Ollama) is unreachable, 502 if the AI service
            returned an unusable response.
    """
    contents = await file.read()

    try:
        text = ocr_processor.extract_text_from_file(contents, file.filename)
    except OCRExtractionError as exc:
        logger.warning("OCR failed for %s: %s", file.filename, exc)
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    try:
        data = parse_invoice(text)
    except AIConnectionError as exc:
        logger.error("AI service unavailable while processing %s: %s", file.filename, exc)
        raise HTTPException(status_code=503, detail=f"AI service unavailable: {exc}") from exc
    except AIResponseError as exc:
        logger.error("AI service returned an invalid response for %s: %s", file.filename, exc)
        raise HTTPException(status_code=502, detail=f"AI parsing failed: {exc}") from exc

    logger.info("Extracted invoice data from %s", file.filename)

    mapped_invoice: Optional[Dict[str, Any]] = None
    mapping_warnings: List[str] = []
    try:
        mapped_invoice = invoice_mapper.map(data).model_dump(mode="json")
    except InvoiceMappingError as exc:
        logger.info("Could not fully map extracted fields to GermanInvoice: %s", exc)
        mapping_warnings = exc.missing_fields or [str(exc)]

    return api_response(
        data={
            "invoice": data,
            "mapped_invoice": mapped_invoice,
            "mapping_warnings": mapping_warnings,
            "raw_text": text,
        },
        meta={"filename": file.filename},
    )


@app.post("/api/v1/invoices/next-number")
def issue_next_invoice_number(
    year: Optional[int] = Query(
        None, description="Calendar year to issue for. Defaults to the current year."
    ),
) -> Dict[str, Any]:
    """
    Issue the next sequential invoice number (§14 UStG / GoBD compliance).

    The number is immediately persisted server-side, so it can never be
    issued again -- consecutive, gapless numbering with no manual renaming.

    Args:
        year: Calendar year to issue for. Defaults to the current year.

    Returns:
        The standard response envelope containing the newly issued
        ``number`` (e.g. ``"RE-2026-0001"``).
    """
    number = invoice_number_sequencer.issue_next(year)
    return api_response(data={"number": number})


@app.post("/api/v1/zugferd/xml")
def generate_zugferd_cii(
    invoice: GermanInvoice,
    validate: bool = Query(
        True,
        description="Run EN16931 business validation and XSD validation before returning XML.",
    ),
) -> Response:
    """
    Generate ZUGFeRD/Factur-X CII XML from a structured invoice.

    Args:
        invoice: The structured invoice payload.
        validate: If ``True`` (default), reject invoices that fail EN16931
            business rules or ZUGFeRD XSD validation instead of returning XML.

    Returns:
        An XML response with ``X-EN16931-Valid`` and ``X-ZUGFeRD-XSD-Valid``
        headers indicating validation status.

    Raises:
        HTTPException: 422 if ``validate`` is ``True`` and either the
            EN16931 business validation or the XSD validation fails.
    """
    business_result = en16931_validator.validate(invoice)
    if validate and not business_result["valid"]:
        raise HTTPException(
            status_code=422,
            detail={
                "validation": "en16931",
                "errors": business_result["errors"],
            },
        )

    xml = cii_builder.build(invoice)

    xsd_result = xsd_validator.validate(xml)
    if validate and not xsd_result["valid"]:
        raise HTTPException(
            status_code=422,
            detail={
                "validation": "zugferd_xsd",
                "errors": xsd_result["errors"],
            },
        )

    return Response(
        content=xml,
        media_type="application/xml",
        headers={
            "X-API-Success": "true",
            "X-EN16931-Valid": str(business_result["valid"]).lower(),
            "X-ZUGFeRD-XSD-Valid": str(xsd_result["valid"]).lower(),
        },
    )


@app.post("/api/v1/zugferd/pdf")
async def generate_zugferd_pdf(
    invoice_json: str = Form(
        ..., description="The structured invoice as a JSON string (GermanInvoice schema)."
    ),
    file: Optional[UploadFile] = File(
        None, description="Visual/human-readable PDF to embed the XML into."
    ),
    template_id: Optional[int] = Form(
        None,
        description="Built-in visual template (1-3) to render with the invoice's own "
        "data instead of uploading a PDF. Ignored if 'file' is given.",
    ),
    validate: bool = Query(
        True,
        description="Run EN16931 business validation and XSD validation before embedding.",
    ),
) -> Response:
    """
    Generate a ZUGFeRD/Factur-X PDF by embedding CII XML into a visual PDF.

    The visual PDF comes from exactly one of two sources: an uploaded
    ``file``, or a built-in ``template_id`` (1-3) rendered on the fly using
    the invoice's own data (so the visual page actually shows the real
    seller/buyer/amounts, not placeholder text).

    Args:
        invoice_json: The structured invoice payload, as a JSON string
            (multipart form fields can't carry nested JSON directly).
        file: The visual/human-readable PDF (e.g. the originally uploaded
            invoice scan) that the CII XML will be embedded into.
        template_id: Built-in template number (1-3) to render dynamically
            instead of uploading a PDF. Ignored if ``file`` is given.
        validate: If ``True`` (default), reject invoices that fail EN16931
            business rules or ZUGFeRD XSD validation before embedding.

    Returns:
        The resulting Factur-X PDF as an ``application/pdf`` download.

    Raises:
        HTTPException: 422 if the invoice JSON is invalid, business/XSD
            validation fails, neither ``file`` nor ``template_id`` was
            given, ``template_id`` is unknown, or the visual PDF and XML
            could not be merged.
    """
    try:
        invoice = GermanInvoice.model_validate_json(invoice_json)
    except ValidationError as exc:
        raise HTTPException(status_code=422, detail=exc.errors()) from exc

    business_result = en16931_validator.validate(invoice)
    if validate and not business_result["valid"]:
        raise HTTPException(
            status_code=422,
            detail={"validation": "en16931", "errors": business_result["errors"]},
        )

    xml = cii_builder.build(invoice)

    xsd_result = xsd_validator.validate(xml)
    if validate and not xsd_result["valid"]:
        raise HTTPException(
            status_code=422,
            detail={"validation": "zugferd_xsd", "errors": xsd_result["errors"]},
        )

    if file is not None:
        pdf_bytes = await file.read()
    elif template_id is not None:
        try:
            pdf_bytes = visual_invoice_renderer.render(invoice, template_id)
        except UnknownTemplateError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc
    else:
        raise HTTPException(
            status_code=422, detail="Either 'file' or 'template_id' must be provided."
        )

    try:
        result_pdf = facturx_builder.build(pdf_bytes, xml)
    except FacturXError as exc:
        logger.warning("Failed to build Factur-X PDF for invoice %s: %s", invoice.invoice.number, exc)
        raise HTTPException(status_code=422, detail=f"Could not generate Factur-X PDF: {exc}") from exc

    return Response(
        content=result_pdf,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{invoice.invoice.number}.pdf"',
            "X-EN16931-Valid": str(business_result["valid"]).lower(),
            "X-ZUGFeRD-XSD-Valid": str(xsd_result["valid"]).lower(),
        },
    )


@app.post("/api/v1/en16931/validate")
def validate_en16931(invoice: GermanInvoice) -> Dict[str, Any]:
    """Run EN16931 business-rule validation against a structured invoice."""
    result = en16931_validator.validate(invoice)
    return api_response(data=result)


@app.post("/api/v1/zugferd/validate-xsd")
def validate_zugferd_xsd(invoice: GermanInvoice) -> Dict[str, Any]:
    """Generate CII XML for a structured invoice and validate it against the ZUGFeRD XSD."""
    xml = cii_builder.build(invoice)
    result = xsd_validator.validate(xml)

    return api_response(data=result)


@app.post("/api/v1/zugferd/parse")
async def convert_zugferd_xml_to_json(file: UploadFile = File(...)) -> Dict[str, Any]:
    """
    Parse a ZUGFeRD/Factur-X PDF or raw CII XML file back into structured JSON.

    Args:
        file: A ZUGFeRD/Factur-X PDF (with embedded XML) or a raw ``.xml`` file.

    Returns:
        The standard response envelope containing the parsed invoice.

    Raises:
        HTTPException: 400 if no CII XML could be extracted or parsed from the file.
    """
    contents = await file.read()

    try:
        xml = cii_parser.extract_from_file(contents, file.filename)
        invoice = cii_parser.parse(xml)
    except ValueError as exc:
        logger.warning("Failed to parse ZUGFeRD file %s: %s", file.filename, exc)
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return api_response(
        data={"invoice": invoice},
        meta={"filename": file.filename},
    )


@app.post("/extract-invoice", include_in_schema=False)
async def extract_invoice_legacy(file: UploadFile = File(...)) -> Dict[str, Any]:
    """Deprecated alias for :func:`extract_invoice`."""
    return await extract_invoice(file)


@app.post("/generate/zugferd-cii", include_in_schema=False)
def generate_zugferd_cii_legacy(invoice: GermanInvoice) -> Response:
    """Deprecated alias for :func:`generate_zugferd_cii`."""
    return generate_zugferd_cii(invoice)


@app.post("/validate/en16931", include_in_schema=False)
def validate_en16931_legacy(invoice: GermanInvoice) -> Dict[str, Any]:
    """Deprecated alias for :func:`validate_en16931`."""
    return validate_en16931(invoice)


@app.post("/validate/zugferd-xsd", include_in_schema=False)
def validate_zugferd_xsd_legacy(invoice: GermanInvoice) -> Dict[str, Any]:
    """Deprecated alias for :func:`validate_zugferd_xsd`."""
    return validate_zugferd_xsd(invoice)


@app.post("/convert/zugferd-xml-to-json", include_in_schema=False)
async def convert_zugferd_xml_to_json_legacy(file: UploadFile = File(...)) -> Dict[str, Any]:
    """Deprecated alias for :func:`convert_zugferd_xml_to_json`."""
    return await convert_zugferd_xml_to_json(file)
