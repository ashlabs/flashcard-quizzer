"""
Unit tests for the missed-term history store.

These tests are written before the implementation and define how the quizzer
remembers past mistakes between sessions. A learner with no history is the
normal starting point rather than an error, but a history file that exists
and is unreadable is reported instead of being silently discarded.
"""

import json
from pathlib import Path

import pytest

from history import (
    HistoryDataError,
    load_missed_terms,
    save_missed_terms,
)

INVALID_HISTORIES = [
    pytest.param(
        ["la ventana", "el libro"],
        r"must contain an object",
        id="top_level_is_not_an_object",
    ),
    pytest.param(
        {"terms": ["la ventana"]},
        r"missing.*missed_terms",
        id="missed_terms_field_is_absent",
    ),
    pytest.param(
        {"missed_terms": "la ventana"},
        r"missed_terms.*must be a list",
        id="missed_terms_is_not_a_list",
    ),
    pytest.param(
        {"missed_terms": ["la ventana", 7]},
        r"missed_terms.*must contain only strings",
        id="missed_terms_holds_a_non_string",
    ),
]


@pytest.fixture
def missed_terms() -> list[str]:
    """Return missed terms in the order they were recorded."""
    return ["la ventana", "el libro", "la puerta"]


def write_history(path: Path, data: object) -> None:
    """Write any JSON value to a history file."""
    path.write_text(json.dumps(data), encoding="utf-8")


class TestLoadMissedTerms:
    """Test suite for reading a history file."""

    def test_missing_history_file_loads_as_no_missed_terms(
        self, tmp_path: Path
    ) -> None:
        """Test that a learner with no history starts with a clean slate."""
        missing_path = tmp_path / "no_such_history.json"

        assert load_missed_terms(missing_path) == []

    def test_valid_history_loads_terms_in_stored_order(
        self, tmp_path: Path, missed_terms: list[str]
    ) -> None:
        """Test that stored terms come back in the order they were saved."""
        history_path = tmp_path / "history.json"
        write_history(history_path, {"missed_terms": missed_terms})

        assert load_missed_terms(history_path) == missed_terms

    def test_malformed_json_raises_helpful_error(self, tmp_path: Path) -> None:
        """Test that an unparsable history file is reported clearly."""
        history_path = tmp_path / "history.json"
        history_path.write_text("this is not json {{", encoding="utf-8")

        with pytest.raises(HistoryDataError, match="Invalid history JSON"):
            load_missed_terms(history_path)

    @pytest.mark.parametrize(
        "history, expected_message",
        INVALID_HISTORIES,
    )
    def test_invalid_history_structure_is_rejected(
        self,
        tmp_path: Path,
        history: object,
        expected_message: str,
    ) -> None:
        """Test that a structurally wrong history file is rejected."""
        history_path = tmp_path / "history.json"
        write_history(history_path, history)

        with pytest.raises(
            HistoryDataError,
            match=expected_message,
        ):
            load_missed_terms(history_path)


class TestSaveMissedTerms:
    """Test suite for writing a history file."""

    def test_saved_terms_load_back_unchanged(
        self, tmp_path: Path, missed_terms: list[str]
    ) -> None:
        """Test that a saved history round-trips through a load."""
        history_path = tmp_path / "history.json"

        save_missed_terms(history_path, missed_terms)

        assert load_missed_terms(history_path) == missed_terms

    def test_saving_creates_missing_parent_directories(
        self, tmp_path: Path, missed_terms: list[str]
    ) -> None:
        """Test that saving works before the state folder exists."""
        history_path = tmp_path / "state" / "quizzer" / "history.json"

        save_missed_terms(history_path, missed_terms)

        assert history_path.is_file()
        assert load_missed_terms(history_path) == missed_terms
