"""Tests for controllers.ai_service (Ollama and Gemini backends)."""

import json
import time

import pytest
import requests

from controllers.ai_service import (
    AIConnectionError,
    AIResponseError,
    FallbackAIProcessor,
    GeminiAIProcessor,
    InvoiceAIProcessor,
    get_default_ai_processor,
)


class _FakeResponse:
    def __init__(self, payload):
        self._payload = payload

    def raise_for_status(self):
        pass

    def json(self):
        return self._payload


def test_extract_returns_parsed_fields(monkeypatch):
    processor = InvoiceAIProcessor()
    inner = {"vendor_name": "Seller GmbH", "net_total": "100,00"}

    def fake_post(*args, **kwargs):
        return _FakeResponse({"response": json.dumps(inner)})

    monkeypatch.setattr(requests, "post", fake_post)

    result = processor.extract("some ocr text")

    assert result == inner


def test_extract_includes_draft_in_prompt_when_given(monkeypatch):
    processor = InvoiceAIProcessor()
    captured = {}

    def fake_post(url, json, timeout):
        captured["prompt"] = json["prompt"]
        return _FakeResponse({"response": "{}"})

    monkeypatch.setattr(requests, "post", fake_post)

    draft = {"iban": "DE89370400440532013000", "vat_id_candidates": ["DE123456789"]}
    processor.extract("some ocr text", draft=draft)

    assert "DE89370400440532013000" in captured["prompt"]
    assert "vat_id_candidates" in captured["prompt"]


def test_extract_raises_on_connection_or_timeout_error(monkeypatch):
    processor = InvoiceAIProcessor()

    def fake_connection_error(*args, **kwargs):
        raise requests.exceptions.ConnectionError("refused")

    monkeypatch.setattr(requests, "post", fake_connection_error)
    with pytest.raises(AIConnectionError):
        processor.extract("some ocr text")

    def fake_timeout(*args, **kwargs):
        raise requests.exceptions.Timeout("too slow")

    monkeypatch.setattr(requests, "post", fake_timeout)
    with pytest.raises(AIConnectionError):
        processor.extract("some ocr text")


def test_extract_raises_when_response_malformed(monkeypatch):
    processor = InvoiceAIProcessor()

    monkeypatch.setattr(requests, "post", lambda *a, **k: _FakeResponse({}))
    with pytest.raises(AIResponseError):
        processor.extract("some ocr text")

    monkeypatch.setattr(requests, "post", lambda *a, **k: _FakeResponse({"response": "not valid json"}))
    with pytest.raises(AIResponseError):
        processor.extract("some ocr text")


def test_extract_tolerates_wrapped_json(monkeypatch):
    processor = InvoiceAIProcessor()
    inner = {"seller_name": "Seller GmbH"}

    fenced = "```json\n" + json.dumps(inner) + "\n```"
    monkeypatch.setattr(requests, "post", lambda *a, **k: _FakeResponse({"response": fenced}))
    assert processor.extract("some ocr text") == inner

    wrapped = "Sure, here is the JSON:\n" + json.dumps(inner) + "\nLet me know if you need anything else."
    monkeypatch.setattr(requests, "post", lambda *a, **k: _FakeResponse({"response": wrapped}))
    assert processor.extract("some ocr text") == inner


def test_gemini_extract_returns_parsed_fields(monkeypatch):
    processor = GeminiAIProcessor(api_key="fake-key")
    inner = {"vendor_name": "Seller GmbH", "net_total": "100,00"}

    def fake_post(*args, **kwargs):
        return _FakeResponse(
            {"candidates": [{"content": {"parts": [{"text": json.dumps(inner)}]}}]}
        )

    monkeypatch.setattr(requests, "post", fake_post)

    result = processor.extract("some ocr text")

    assert result == inner


def test_gemini_extract_raises_on_connection_error_or_blocked_response(monkeypatch):
    processor = GeminiAIProcessor(api_key="fake-key")

    def fake_connection_error(*args, **kwargs):
        raise requests.exceptions.ConnectionError("refused")

    monkeypatch.setattr(requests, "post", fake_connection_error)
    with pytest.raises(AIConnectionError):
        processor.extract("some ocr text")

    def fake_blocked(*args, **kwargs):
        return _FakeResponse({"candidates": [], "promptFeedback": {"blockReason": "SAFETY"}})

    monkeypatch.setattr(requests, "post", fake_blocked)
    with pytest.raises(AIResponseError):
        processor.extract("some ocr text")


def test_gemini_sends_api_key_via_header_not_url(monkeypatch):
    processor = GeminiAIProcessor(api_key="super-secret-key")
    captured = {}

    def fake_post(url, **kwargs):
        captured["url"] = url
        captured["headers"] = kwargs.get("headers", {})
        return _FakeResponse({"candidates": [{"content": {"parts": [{"text": "{}"}]}}]})

    monkeypatch.setattr(requests, "post", fake_post)

    processor.extract("some ocr text")

    assert "super-secret-key" not in captured["url"]
    assert captured["headers"].get("x-goog-api-key") == "super-secret-key"


def test_gemini_http_error_does_not_leak_api_key(monkeypatch):
    processor = GeminiAIProcessor(api_key="super-secret-key")

    class _FakeErrorResponse:
        status_code = 404
        url = "https://generativelanguage.googleapis.com/v1beta/models/x:generateContent"

        def raise_for_status(self):
            error = requests.exceptions.HTTPError("404 Client Error: Not Found")
            error.response = self
            raise error

    def fake_post(*args, **kwargs):
        return _FakeErrorResponse()

    monkeypatch.setattr(requests, "post", fake_post)

    with pytest.raises(AIResponseError) as exc_info:
        processor.extract("some ocr text")

    assert "super-secret-key" not in str(exc_info.value)


def test_gemini_retries_on_overload_and_succeeds(monkeypatch):
    processor = GeminiAIProcessor(api_key="fake-key")
    monkeypatch.setattr(time, "sleep", lambda seconds: None)

    class _OverloadedResponse:
        status_code = 503

        def raise_for_status(self):
            error = requests.exceptions.HTTPError("503 Server Error: Service Unavailable")
            error.response = self
            raise error

    calls = {"count": 0}

    def fake_post(*args, **kwargs):
        calls["count"] += 1
        if calls["count"] < 2:
            return _OverloadedResponse()
        return _FakeResponse({"candidates": [{"content": {"parts": [{"text": "{}"}]}}]})

    monkeypatch.setattr(requests, "post", fake_post)

    processor.extract("some ocr text")

    assert calls["count"] == 2


def test_gemini_gives_up_after_repeated_overload(monkeypatch):
    processor = GeminiAIProcessor(api_key="fake-key")
    monkeypatch.setattr(time, "sleep", lambda seconds: None)

    class _OverloadedResponse:
        status_code = 503

        def raise_for_status(self):
            error = requests.exceptions.HTTPError("503 Server Error: Service Unavailable")
            error.response = self
            raise error

    monkeypatch.setattr(requests, "post", lambda *a, **k: _OverloadedResponse())

    with pytest.raises(AIResponseError, match="503"):
        processor.extract("some ocr text")


def test_get_default_ai_processor_selects_backend_based_on_api_key(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "fake-key")
    processor = get_default_ai_processor()
    assert isinstance(processor, FallbackAIProcessor)
    assert isinstance(processor.primary, InvoiceAIProcessor)
    assert isinstance(processor.fallback, GeminiAIProcessor)

    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    assert isinstance(get_default_ai_processor(), InvoiceAIProcessor)


class _StubProcessor:
    def __init__(self, result=None, error=None):
        self._result = result
        self._error = error
        self.called = False

    def extract(self, text, draft=None):
        self.called = True
        if self._error:
            raise self._error
        return self._result


def test_fallback_uses_primary_when_it_succeeds():
    primary = _StubProcessor(result={"vendor_name": "Primary"})
    fallback = _StubProcessor(result={"vendor_name": "Fallback"})

    result = FallbackAIProcessor(primary, fallback).extract("text")

    assert result == {"vendor_name": "Primary"}
    assert fallback.called is False


def test_fallback_switches_to_secondary_when_primary_is_unreachable():
    primary = _StubProcessor(error=AIConnectionError("Ollama down"))
    fallback = _StubProcessor(result={"vendor_name": "Fallback"})

    result = FallbackAIProcessor(primary, fallback).extract("text")

    assert result == {"vendor_name": "Fallback"}
    assert fallback.called is True


def test_fallback_propagates_error_if_both_fail():
    primary = _StubProcessor(error=AIConnectionError("Ollama down"))
    fallback = _StubProcessor(error=AIResponseError("Gemini rejected"))

    with pytest.raises(AIResponseError):
        FallbackAIProcessor(primary, fallback).extract("text")
