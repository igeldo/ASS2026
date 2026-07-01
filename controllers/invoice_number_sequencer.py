"""Persistent, sequential invoice numbering (§14 UStG / GoBD compliance).

German law requires outgoing invoices to carry a consecutive, gapless
number that is never reused or altered after issuance. This module is the
single source of truth for assigning that number: once issued, a number
is immediately persisted to disk and the counter can only move forward,
so numbering survives process restarts and can never repeat or go
backwards.
"""

import json
import logging
import threading
from datetime import date
from pathlib import Path
from typing import Dict, Optional

logger = logging.getLogger(__name__)

DEFAULT_STATE_PATH = Path(__file__).resolve().parents[1] / "data" / "invoice_number_state.json"


class InvoiceNumberSequencer:
    """
    Issues sequential invoice numbers (e.g. ``"RE-2026-0001"``) and
    persists the last-issued number per year to a JSON state file.

    Attributes:
        state_path: Path to the JSON file storing the last issued number
            per year, e.g. ``{"2026": 3}``.
        prefix: Prefix used when formatting issued numbers.
    """

    def __init__(self, state_path: Path = DEFAULT_STATE_PATH, prefix: str = "RE") -> None:
        """
        Args:
            state_path: Where to persist the per-year counters.
            prefix: Prefix used when formatting issued numbers.
        """
        self.state_path = state_path
        self.prefix = prefix
        self._lock = threading.Lock()
        self.state_path.parent.mkdir(parents=True, exist_ok=True)

    def _load_state(self) -> Dict[str, int]:
        if not self.state_path.exists():
            return {}

        try:
            return json.loads(self.state_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as exc:
            logger.error("Could not read invoice number state file %s: %s", self.state_path, exc)
            raise

    def _save_state(self, state: Dict[str, int]) -> None:
        self.state_path.write_text(json.dumps(state, indent=2), encoding="utf-8")

    def issue_next(self, year: Optional[int] = None) -> str:
        """
        Atomically issue the next sequential invoice number for a year.

        Args:
            year: Calendar year to number for. Defaults to the current year.

        Returns:
            The newly issued invoice number, e.g. ``"RE-2026-0001"``. It is
            persisted before being returned, so it can never be issued
            again, even across process restarts.
        """
        year = year or date.today().year

        with self._lock:
            state = self._load_state()
            next_sequence = state.get(str(year), 0) + 1
            state[str(year)] = next_sequence
            self._save_state(state)

        formatted = f"{self.prefix}-{year}-{next_sequence:04d}"
        logger.info("Issued invoice number %s", formatted)
        return formatted

    def last_issued(self, year: Optional[int] = None) -> int:
        """Return the last issued sequence number for ``year`` (0 if none issued yet)."""
        year = year or date.today().year
        with self._lock:
            return self._load_state().get(str(year), 0)
