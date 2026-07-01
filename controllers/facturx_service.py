"""Embeds ZUGFeRD/Factur-X CII XML into a visual PDF using the `factur-x` library."""

import logging

from facturx import generate_from_binary

logger = logging.getLogger(__name__)

PDF_SIGNATURE = b"%PDF"


class FacturXError(Exception):
    """Raised when a visual PDF and CII XML could not be merged into a Factur-X PDF."""


class FacturXPdfBuilder:
    """
    Merges a human-readable "visual" PDF with machine-readable CII XML into
    a single ZUGFeRD/Factur-X compliant PDF/A-3 document.

    Delegates the actual PDF/A-3 metadata and embedding work to the
    third-party `factur-x` library, which already implements the
    ZUGFeRD/Factur-X conformance rules (XMP metadata, AFRelationship,
    XSD/schematron validation).
    """

    def build(self, pdf_bytes: bytes, xml: str) -> bytes:
        """
        Embed CII XML into a visual PDF as a Factur-X document.

        Args:
            pdf_bytes: The visual/human-readable PDF to embed the XML into.
            xml: The CII XML string to embed (e.g. from :class:`CIIBuilder`).

        Returns:
            The resulting Factur-X PDF as bytes.

        Raises:
            FacturXError: If the input is not a valid PDF, or the XML fails
                Factur-X XSD/schematron validation, or embedding otherwise
                fails.
        """
        if not pdf_bytes.lstrip().startswith(PDF_SIGNATURE):
            raise FacturXError(
                "The uploaded visual file is not a valid PDF "
                "(expected a PDF, but got something else, e.g. an image)."
            )

        try:
            result = generate_from_binary(
                pdf_bytes,
                xml.encode("utf-8"),
                check_xsd=True,
                check_schematron=True,
            )
        except Exception as exc:
            logger.error("Failed to build Factur-X PDF: %s", exc)
            raise FacturXError(str(exc)) from exc

        logger.info("Generated Factur-X PDF (%d bytes)", len(result))
        return result
