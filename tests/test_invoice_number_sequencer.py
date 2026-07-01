"""Tests for controllers.invoice_number_sequencer.InvoiceNumberSequencer."""

from controllers.invoice_number_sequencer import InvoiceNumberSequencer


def test_issue_next_starts_at_one_and_increments(tmp_path):
    sequencer = InvoiceNumberSequencer(state_path=tmp_path / "state.json")

    assert sequencer.issue_next(year=2026) == "RE-2026-0001"
    assert sequencer.issue_next(year=2026) == "RE-2026-0002"
    assert sequencer.issue_next(year=2026) == "RE-2026-0003"


def test_issue_next_separates_counters_by_year(tmp_path):
    sequencer = InvoiceNumberSequencer(state_path=tmp_path / "state.json")

    assert sequencer.issue_next(year=2026) == "RE-2026-0001"
    assert sequencer.issue_next(year=2027) == "RE-2027-0001"
    assert sequencer.issue_next(year=2026) == "RE-2026-0002"


def test_issue_next_persists_across_instances(tmp_path):
    """Numbering must survive process restarts -- never reset, never reused."""
    state_path = tmp_path / "state.json"

    first_instance = InvoiceNumberSequencer(state_path=state_path)
    assert first_instance.issue_next(year=2026) == "RE-2026-0001"

    second_instance = InvoiceNumberSequencer(state_path=state_path)
    assert second_instance.issue_next(year=2026) == "RE-2026-0002"


def test_last_issued_returns_zero_when_no_state_yet(tmp_path):
    sequencer = InvoiceNumberSequencer(state_path=tmp_path / "state.json")

    assert sequencer.last_issued(year=2026) == 0

    sequencer.issue_next(year=2026)
    assert sequencer.last_issued(year=2026) == 1


def test_custom_prefix_is_used(tmp_path):
    sequencer = InvoiceNumberSequencer(state_path=tmp_path / "state.json", prefix="INV")

    assert sequencer.issue_next(year=2026) == "INV-2026-0001"
