"""
Unit tests for the command line entry point.

These tests are written before the implementation and define how the
quizzer behaves when it is run as a program: how a mode name becomes an
ordering strategy, what a whole session prints and remembers, and how a
bad deck or history file is reported. Failures reach the learner as a
message on stderr and a non-zero exit code, never as a traceback.
"""

import json
from collections.abc import Sequence
from pathlib import Path

import pytest

from history import load_missed_terms
from main import create_strategy, main
from models.flashcard import Flashcard
from quiz_strategies import (
    AdaptiveStrategy,
    RandomStrategy,
    SequentialStrategy,
)

DECK = [("el gato", "the cat"), ("el perro", "the dog")]


class ScriptedAnswers:
    """Stands in for input(), replying with scripted answers in turn."""

    def __init__(self, answers: Sequence[str]) -> None:
        """Store the answers to give, in the order they will be given."""
        self._answers = list(answers)
        self.asked = 0

    def __call__(self, prompt: str = "") -> str:
        """Return the next scripted answer for the prompt shown."""
        if self.asked >= len(self._answers):
            raise AssertionError("The quiz asked more questions than scripted")
        answer = self._answers[self.asked]
        self.asked += 1
        return answer


def write_deck(path: Path, cards: Sequence[tuple[str, str]]) -> Path:
    """Write a deck file holding the given front and back pairs."""
    document = [{"front": front, "back": back} for front, back in cards]
    path.write_text(json.dumps(document), encoding="utf-8")
    return path


def write_history(path: Path, missed_terms: Sequence[str]) -> Path:
    """Write a history file holding the given missed terms."""
    document = {"missed_terms": list(missed_terms)}
    path.write_text(json.dumps(document), encoding="utf-8")
    return path


def script_answers(
    monkeypatch: pytest.MonkeyPatch, answers: Sequence[str]
) -> ScriptedAnswers:
    """Answer every question of a session from a fixed script."""
    scripted = ScriptedAnswers(answers)
    monkeypatch.setattr("builtins.input", scripted)
    return scripted


def assert_reports_error(out: str, err: str) -> None:
    """Assert the run explained itself without showing a traceback."""
    assert err.strip() != ""
    assert "Error:" in err
    assert "Traceback" not in err
    assert "Traceback" not in out


@pytest.fixture
def cards() -> list[Flashcard]:
    """Return the deck in the order it is stored on disk."""
    return [Flashcard(front, back) for front, back in DECK]


@pytest.fixture
def deck_path(tmp_path: Path) -> Path:
    """Return the path of a written two-card deck."""
    return write_deck(tmp_path / "deck.json", DECK)


@pytest.fixture
def history_path(tmp_path: Path) -> Path:
    """Return the path a session should keep its history at."""
    return tmp_path / "history.json"


class TestCreateStrategy:
    """Test suite for turning a mode name into an ordering strategy."""

    def test_sequential_mode_builds_a_sequential_strategy(self) -> None:
        """Test that "sequential" asks the deck in its stored order."""
        strategy = create_strategy("sequential", [])

        assert isinstance(strategy, SequentialStrategy)

    def test_random_mode_builds_a_random_strategy(self) -> None:
        """Test that "random" shuffles, reproducibly when seeded."""
        strategy = create_strategy("random", [], seed=7)

        assert isinstance(strategy, RandomStrategy)

    def test_adaptive_mode_orders_by_the_supplied_missed_terms(
        self, cards: list[Flashcard]
    ) -> None:
        """Test that "adaptive" asks the terms it was told were missed."""
        strategy = create_strategy("adaptive", ["el perro"])

        assert isinstance(strategy, AdaptiveStrategy)
        ordered = strategy.order_cards(cards)
        assert [card.front for card in ordered] == ["el perro", "el gato"]

    def test_unsupported_mode_is_rejected(self) -> None:
        """Test that an unknown mode is refused rather than guessed at."""
        with pytest.raises(ValueError):
            create_strategy("backwards", [])


class TestSuccessfulRun:
    """Test suite for a quiz that runs from start to finish."""

    def test_sequential_run_reports_and_records_the_session(
        self,
        deck_path: Path,
        history_path: Path,
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """Test that a full session grades, summarizes, and remembers."""
        script_answers(monkeypatch, ["the cat", "the bird"])

        exit_code = main([str(deck_path), "--history", str(history_path)])

        assert exit_code == 0
        output = capsys.readouterr().out
        assert "Correct!" in output
        assert "Incorrect" in output
        assert "Quiz Summary" in output
        assert load_missed_terms(history_path) == ["el perro"]

    def test_adaptive_run_asks_a_previously_missed_term_first(
        self,
        deck_path: Path,
        history_path: Path,
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """Test that stored history moves a missed term to the front."""
        write_history(history_path, ["el perro"])
        script_answers(monkeypatch, ["the dog", "the cat"])

        exit_code = main(
            [
                str(deck_path),
                "--mode",
                "adaptive",
                "--history",
                str(history_path),
            ]
        )

        assert exit_code == 0
        output = capsys.readouterr().out
        assert output.index("el perro") < output.index("el gato")
        assert load_missed_terms(history_path) == []


class TestFailedRun:
    """Test suite for runs that cannot start or finish."""

    def test_missing_deck_is_reported(
        self,
        tmp_path: Path,
        history_path: Path,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """Test that a deck that is not there is named, not crashed on."""
        missing_path = tmp_path / "no_such_deck.json"

        exit_code = main([str(missing_path), "--history", str(history_path)])

        assert exit_code == 1
        captured = capsys.readouterr()
        assert_reports_error(captured.out, captured.err)
        assert missing_path.name in captured.err

    def test_malformed_deck_is_reported(
        self,
        tmp_path: Path,
        history_path: Path,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """Test that an unparsable deck file ends the run cleanly."""
        deck_path = tmp_path / "deck.json"
        deck_path.write_text("this is not json {{", encoding="utf-8")

        exit_code = main([str(deck_path), "--history", str(history_path)])

        assert exit_code == 1
        captured = capsys.readouterr()
        assert_reports_error(captured.out, captured.err)

    def test_empty_deck_is_reported(
        self,
        tmp_path: Path,
        history_path: Path,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """Test that a deck with no cards says so instead of quizzing."""
        deck_path = write_deck(tmp_path / "deck.json", [])

        exit_code = main([str(deck_path), "--history", str(history_path)])

        assert exit_code == 1
        captured = capsys.readouterr()
        assert_reports_error(captured.out, captured.err)
        assert "empty" in captured.err.casefold()

    def test_malformed_history_is_reported_in_adaptive_mode(
        self,
        deck_path: Path,
        history_path: Path,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """Test that unreadable history stops the run, losing nothing."""
        history_path.write_text("this is not json {{", encoding="utf-8")

        exit_code = main(
            [
                str(deck_path),
                "--mode",
                "adaptive",
                "--history",
                str(history_path),
            ]
        )

        assert exit_code == 1
        captured = capsys.readouterr()
        assert_reports_error(captured.out, captured.err)
