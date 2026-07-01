"""Tests for controllers.datum_service.DateNormalizer."""

from controllers.datum_service import normalize_date


def test_normalize_date_parses_supported_formats():
    assert normalize_date("06.05.2026") == "2026-05-06"
    assert normalize_date("06.05.26") == "2026-05-06"


def test_normalize_date_returns_none_for_invalid_input():
    assert normalize_date(None) is None
    assert normalize_date("") is None
    assert normalize_date("2026-05-06") is None
