"""XSD schema validation for generated ZUGFeRD/Factur-X CII XML."""

import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

from lxml import etree

logger = logging.getLogger(__name__)

SCHEMA_DIR = Path(__file__).resolve().parents[1] / "schemas"
XSD_PATH = SCHEMA_DIR / "CrossIndustryInvoice_100pD22B.xsd"
XSD_NAMESPACE = "{http://www.w3.org/2001/XMLSchema}"


class CIIXsdValidator:
    """
    Validates CII XML strings against the ZUGFeRD/Factur-X CII XSD schema
    set bundled under ``schemas/``.

    Attributes:
        xsd_path: Path to the root CII XSD file.
    """

    def __init__(self, xsd_path: Path = XSD_PATH) -> None:
        """
        Initialize the validator.

        Args:
            xsd_path: Path to the root CII XSD schema file. Its ``xsd:import``
                references are resolved relative to this file's directory.
        """
        self.xsd_path = xsd_path

    def _missing_imports(self, xsd_path: Path, seen: Optional[Set[Path]] = None) -> List[str]:
        """Recursively find any ``xsd:import`` schemaLocation files that are missing on disk."""
        seen = seen or set()
        xsd_path = xsd_path.resolve()

        if xsd_path in seen:
            return []

        seen.add(xsd_path)

        if not xsd_path.exists():
            return [str(xsd_path)]

        xsd_doc = etree.parse(str(xsd_path))
        missing = []

        for import_node in xsd_doc.findall(f"{XSD_NAMESPACE}import"):
            schema_location = import_node.get("schemaLocation")
            if not schema_location:
                continue

            import_path = xsd_path.parent / schema_location
            if import_path.exists():
                missing.extend(self._missing_imports(import_path, seen))
            else:
                missing.append(schema_location)

        return missing

    @staticmethod
    def _format_error_log(error_log: Any) -> List[str]:
        """Format an lxml schema error log into human-readable strings."""
        return [
            f"line {error.line}, column {error.column}: {error.message}"
            for error in error_log
        ]

    def validate(self, xml_string: str) -> Dict[str, Any]:
        """
        Validate a CII XML string against the bundled XSD schema.

        Args:
            xml_string: The CII XML document to validate.

        Returns:
            A dictionary with ``valid`` (bool) and ``errors`` (list of
            human-readable error strings). Never raises for malformed
            input -- validation failures are reported in the result instead.
        """
        try:
            xml_doc = etree.fromstring(xml_string.encode("utf-8"))
        except etree.XMLSyntaxError as exc:
            logger.warning("XSD validation received invalid XML: %s", exc)
            return {"valid": False, "errors": [f"Invalid XML: {exc}"]}

        missing_imports = self._missing_imports(self.xsd_path)
        if missing_imports:
            logger.error("CII XSD schema set is incomplete: %s", missing_imports)
            return {
                "valid": False,
                "errors": [
                    "CII XSD schema set is incomplete. Add the imported XSD files "
                    f"next to {self.xsd_path.name}: {', '.join(missing_imports)}"
                ],
            }

        try:
            # Parse from the path string so lxml keeps the schema directory as the
            # base URL for resolving relative xsd:import schemaLocation values.
            xsd_doc = etree.parse(str(self.xsd_path))
            schema = etree.XMLSchema(xsd_doc)
        except (OSError, etree.XMLSchemaParseError, etree.XMLSyntaxError) as exc:
            logger.error("Could not load CII XSD schema: %s", exc)
            return {"valid": False, "errors": [f"Could not load CII XSD schema: {exc}"]}

        valid = schema.validate(xml_doc)
        if not valid:
            logger.info("CII XML failed XSD validation: %s", schema.error_log)

        return {
            "valid": valid,
            "errors": self._format_error_log(schema.error_log),
        }
