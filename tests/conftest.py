"""Shared pytest fixtures for the German Invoice OCR API test suite."""

import copy
import json
from pathlib import Path
from typing import Any, Dict

import pytest
from fastapi.testclient import TestClient

from main import app

EXAMPLE_INVOICE_PATH = Path(__file__).resolve().parents[1] / "examples" / "invoice.json"


@pytest.fixture
def client() -> TestClient:
    """FastAPI test client for the application under test."""
    return TestClient(app)


@pytest.fixture
def example_invoice_dict() -> Dict[str, Any]:
    """A fresh copy of the bundled example ``GermanInvoice`` JSON payload."""
    with open(EXAMPLE_INVOICE_PATH, encoding="utf-8") as f:
        return copy.deepcopy(json.load(f))
