from fastapi import FastAPI, HTTPException, Query, Request, UploadFile, File
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, Response
from services.ocr_service import extract_text_from_file
from services.invoice_parser import parse_invoice

from models.en16931 import GermanInvoice
from services.cii_generator import generate_cii_xml
from services.cii_parser import extract_cii_xml_from_file, parse_cii_xml
from services.validator import validate_invoice
from services.xsd_validator import validate_cii_xml

app = FastAPI(title="German Invoice OCR API")


def api_response(data=None, errors=None, meta=None, success: bool = True):
    return {
        "success": success,
        "data": data,
        "errors": errors or [],
        "meta": meta or {},
    }


def error_response(errors, status_code: int = 400):
    if isinstance(errors, str):
        errors = [errors]

    return JSONResponse(
        status_code=status_code,
        content=api_response(data=None, errors=errors, success=False),
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return error_response(exc.detail, exc.status_code)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = [
        {
            "field": ".".join(str(part) for part in error["loc"]),
            "message": error["msg"],
            "type": error["type"],
        }
        for error in exc.errors()
    ]
    return error_response(errors, 422)


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    return error_response("Internal server error", 500)


@app.get("/")
def home():
    return api_response(
        data={"message": "German Invoice OCR API is running"},
        meta={"version": "v1"},
    )


@app.get("/health")
def health():
    return api_response(data={"status": "ok"})


@app.post("/api/v1/invoices/extract")
async def extract_invoice(file: UploadFile = File(...)):
    contents = await file.read()
    text = extract_text_from_file(contents, file.filename)

    try:
        data = parse_invoice(text)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=422, detail="AI parsing failed") from e

    return api_response(
        data={
            "invoice": data,
            "raw_text": text,
        },
        meta={"filename": file.filename},
    )


@app.post("/api/v1/zugferd/xml")
def generate_zugferd_cii(
    invoice: GermanInvoice,
    validate: bool = Query(
        True,
        description="Run EN16931 business validation and XSD validation before returning XML.",
    ),
):
    business_result = validate_invoice(invoice)
    if validate and not business_result["valid"]:
        raise HTTPException(
            status_code=422,
            detail={
                "validation": "en16931",
                "errors": business_result["errors"],
            },
        )

    xml = generate_cii_xml(invoice)

    xsd_result = validate_cii_xml(xml)
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


@app.post("/api/v1/en16931/validate")
def validate_en16931(invoice: GermanInvoice):
    result = validate_invoice(invoice)
    return api_response(data=result)


@app.post("/api/v1/zugferd/validate-xsd")
def validate_zugferd_xsd(invoice: GermanInvoice):
    xml = generate_cii_xml(invoice)
    result = validate_cii_xml(xml)

    return api_response(data=result)


@app.post("/api/v1/zugferd/parse")
async def convert_zugferd_xml_to_json(file: UploadFile = File(...)):
    contents = await file.read()

    try:
        xml = extract_cii_xml_from_file(contents, file.filename)
        invoice = parse_cii_xml(xml)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return api_response(
        data={"invoice": invoice},
        meta={"filename": file.filename},
    )


@app.post("/extract-invoice", include_in_schema=False)
async def extract_invoice_legacy(file: UploadFile = File(...)):
    return await extract_invoice(file)


@app.post("/generate/zugferd-cii", include_in_schema=False)
def generate_zugferd_cii_legacy(invoice: GermanInvoice):
    return generate_zugferd_cii(invoice)


@app.post("/validate/en16931", include_in_schema=False)
def validate_en16931_legacy(invoice: GermanInvoice):
    return validate_en16931(invoice)


@app.post("/validate/zugferd-xsd", include_in_schema=False)
def validate_zugferd_xsd_legacy(invoice: GermanInvoice):
    return validate_zugferd_xsd(invoice)


@app.post("/convert/zugferd-xml-to-json", include_in_schema=False)
async def convert_zugferd_xml_to_json_legacy(file: UploadFile = File(...)):
    return await convert_zugferd_xml_to_json(file)
