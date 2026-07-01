"""OCR text extraction from invoice PDFs and images (Tesseract + PyMuPDF)."""

import io
import logging
import shutil
from pathlib import Path

import fitz  # pymupdf
import pytesseract
from PIL import Image, ImageFilter, ImageOps

logger = logging.getLogger(__name__)

# Common Windows install locations, used as a fallback when the "tesseract"
# command isn't on PATH (some installer builds don't offer an "Add to PATH"
# option). Only used if the command isn't already resolvable.
_WINDOWS_FALLBACK_PATHS = [
    Path(r"C:\Program Files\Tesseract-OCR\tesseract.exe"),
    Path(r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"),
]


def _resolve_tesseract_cmd() -> None:
    """Point pytesseract at a known Tesseract install if it isn't already on PATH."""
    if shutil.which(pytesseract.pytesseract.tesseract_cmd):
        return

    for candidate in _WINDOWS_FALLBACK_PATHS:
        if candidate.is_file():
            logger.info("Tesseract not found on PATH, using fallback: %s", candidate)
            pytesseract.pytesseract.tesseract_cmd = str(candidate)
            return


_resolve_tesseract_cmd()


class OCRExtractionError(Exception):
    """Raised when text could not be extracted from an uploaded document."""


class OCRProcessor:
    """
    Extracts plain text from invoice documents (PDF or image) for downstream
    AI-based field extraction.

    Text-based PDFs are read directly via PyMuPDF. Image files, and PDFs
    with no embedded text (i.e. scanned documents), are rasterized and run
    through Tesseract OCR.

    Attributes:
        lang: Tesseract language string (e.g. ``"deu+eng"``).
        psm: Tesseract page segmentation mode.
        ocr_dpi: DPI used when rasterizing PDF pages for OCR fallback.
    """

    def __init__(self, lang: str = "deu+eng", psm: int = 6, ocr_dpi: int = 200) -> None:
        """
        Initialize the OCR processor.

        Args:
            lang: Tesseract language string.
            psm: Tesseract page segmentation mode.
            ocr_dpi: DPI used when rasterizing PDF pages for OCR fallback.
        """
        self.lang = lang
        self.psm = psm
        self.ocr_dpi = ocr_dpi

    def _tesseract_config(self) -> str:
        return f"--psm {self.psm}"

    def _run_tesseract(self, image: Image.Image) -> str:
        """Run Tesseract on a preprocessed image, translating its errors to :class:`OCRExtractionError`."""
        try:
            return pytesseract.image_to_string(
                image,
                lang=self.lang,
                config=self._tesseract_config(),
            )
        except pytesseract.TesseractNotFoundError as exc:
            logger.error("Tesseract executable not found: %s", exc)
            raise OCRExtractionError(
                "Tesseract OCR is not installed or not on PATH. "
                "See README.md for installation instructions."
            ) from exc
        except pytesseract.TesseractError as exc:
            logger.error("Tesseract failed to process the image: %s", exc)
            raise OCRExtractionError(f"Tesseract OCR failed: {exc}") from exc

    def _preprocess_image(self, image: Image.Image) -> Image.Image:
        """
        Apply grayscale, autocontrast, upscaling and sharpening to improve
        OCR accuracy on scanned/photographed invoices.

        Args:
            image: The source image.

        Returns:
            The preprocessed image.
        """
        image = image.convert("RGBA")
        image = image.convert("L")
        image = ImageOps.autocontrast(image)
        image = image.resize((image.width * 2, image.height * 2))
        image = image.filter(ImageFilter.SHARPEN)
        return image

    def extract_text_from_image(self, contents: bytes) -> str:
        """
        Run Tesseract OCR on an image file.

        Args:
            contents: Raw image bytes (JPG/PNG/...).

        Returns:
            The recognized text.

        Raises:
            OCRExtractionError: If the bytes cannot be decoded as an image,
                or Tesseract is not installed/fails to process it.
        """
        try:
            image = Image.open(io.BytesIO(contents))
        except Exception as exc:
            logger.error("Could not open uploaded file as an image: %s", exc)
            raise OCRExtractionError("Uploaded file is not a valid image") from exc

        processed = self._preprocess_image(image)
        text = self._run_tesseract(processed)
        logger.debug("OCR extracted %d characters from image", len(text))
        return text

    def extract_text_from_pdf(self, contents: bytes) -> str:
        """
        Extract text from a PDF, preferring the embedded text layer and
        falling back to page-by-page OCR for scanned documents.

        Args:
            contents: Raw PDF bytes.

        Returns:
            The extracted (or OCR'd) text.

        Raises:
            OCRExtractionError: If the bytes cannot be opened as a PDF, or
                (for scanned PDFs) Tesseract is not installed/fails.
        """
        try:
            doc = fitz.open(stream=contents, filetype="pdf")
        except Exception as exc:
            logger.error("Could not open uploaded file as a PDF: %s", exc)
            raise OCRExtractionError("Uploaded file is not a valid PDF") from exc

        text = ""
        for page in doc:
            text += page.get_text() + "\n"

        if text.strip():
            logger.debug("Extracted %d characters directly from PDF text layer", len(text))
            return text

        logger.info("PDF has no embedded text layer, falling back to OCR")
        ocr_text = ""

        for page in doc:
            pix = page.get_pixmap(dpi=self.ocr_dpi)
            img = Image.open(io.BytesIO(pix.tobytes("png")))
            processed = self._preprocess_image(img)

            ocr_text += self._run_tesseract(processed) + "\n"

        return ocr_text

    def extract_text_from_file(self, contents: bytes, filename: str) -> str:
        """
        Extract text from an uploaded invoice file, dispatching by extension.

        Args:
            contents: Raw file bytes.
            filename: Original filename, used to detect PDF vs. image.

        Returns:
            The extracted text.

        Raises:
            OCRExtractionError: If the file could not be opened/decoded.
        """
        if filename.lower().endswith(".pdf"):
            return self.extract_text_from_pdf(contents)

        return self.extract_text_from_image(contents)
