"""Normalizes loosely-formatted German date strings to ISO 8601."""

import logging
from datetime import datetime
from typing import List, Optional

logger = logging.getLogger(__name__)


class DateNormalizer:
    """Converts German-formatted date strings (e.g. ``"06.05.2026"``) to ISO 8601."""

    FORMATS: List[str] = [
        "%d.%m.%Y",
        "%d.%m.%y",
    ]

    def normalize(self, date_str: Optional[str]) -> Optional[str]:
        """
        Parse a date string using the supported German formats.

        Args:
            date_str: Raw date string as returned by the AI model, e.g.
                ``"06.05.2026"`` or ``"06.05.26"``.

        Returns:
            The date formatted as ``YYYY-MM-DD``, or ``None`` if ``date_str``
            is empty or does not match any supported format.
        """
        if not date_str:
            return None

        for fmt in self.FORMATS:
            try:
                dt = datetime.strptime(date_str, fmt)
                return dt.strftime("%Y-%m-%d")
            except ValueError:
                continue

        logger.warning("Could not normalize date string: %r", date_str)
        return None


_default_normalizer = DateNormalizer()


def normalize_date(date_str: Optional[str]) -> Optional[str]:
    """
    Normalize a German-formatted date string to ISO 8601.

    Thin module-level wrapper around :class:`DateNormalizer` kept for
    backward compatibility with existing callers.
    """
    return _default_normalizer.normalize(date_str)
