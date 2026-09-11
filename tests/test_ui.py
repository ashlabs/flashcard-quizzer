"""
Unit tests for the terminal user interface.

These tests are written before the implementation and pin down what the
learner actually sees and types: the term being asked, the wording of the
prompt, the verdict after each answer, and the end-of-session summary. They
check the text that matters and ignore decorative borders and spacing, so
the presentation can be restyled without breaking them.
"""

import pytest

from models.flashcard import Flashcard
from quiz_engine import SessionStats
from ui import prompt_for_answer, show_feedback, show_summary


class FakeInput:
    """Stands in for input(), recording prompts and scripting a reply."""

    def __init__(self, reply: str) -> None:
        """Store the reply that every call will return."""
        self._reply = reply
        self.prompts: list[str] = []

    def __call__(self, prompt: str = "") -> str:
        """Record the prompt that was shown and return the reply."""
        self.prompts.append(prompt)
        return self._reply


@pytest.fixture
def card() -> Flashcard:
    """Return a single flashcard to ask about."""
    return Flashcard("la biblioteca", "the library")


@pytest.fixture
def stats() -> SessionStats:
    """Return stats for a session that missed three terms."""
    return SessionStats(
        total_questions=8,
        correct_answers=5,
        missed_terms=["la ventana", "el libro", "la puerta"],
    )


@pytest.fixture
def perfect_stats() -> SessionStats:
    """Return stats for a session that missed nothing."""
    return SessionStats(
        total_questions=3,
        correct_answers=3,
        missed_terms=[],
    )


class TestPromptForAnswer:
    """Test suite for the answer prompt."""

    def test_prompt_for_answer_displays_the_card_front(
        self,
        card: Flashcard,
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """Test that the learner sees the term being asked."""
        monkeypatch.setattr("builtins.input", FakeInput("the library"))

        prompt_for_answer(card)

        assert "la biblioteca" in capsys.readouterr().out

    def test_prompt_for_answer_uses_the_expected_input_prompt(
        self, card: Flashcard, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test that input() is asked with the agreed wording."""
        fake_input = FakeInput("the library")
        monkeypatch.setattr("builtins.input", fake_input)

        prompt_for_answer(card)

        assert fake_input.prompts == ["Your answer: "]

    def test_prompt_for_answer_returns_the_text_from_input(
        self, card: Flashcard, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test that the typed text comes back exactly as entered."""
        monkeypatch.setattr("builtins.input", FakeInput("  The Library  "))

        answer = prompt_for_answer(card)

        assert answer == "  The Library  "


class TestShowFeedback:
    """Test suite for per-answer feedback."""

    def test_show_feedback_confirms_a_correct_answer(
        self, card: Flashcard, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Test that a correct answer is confirmed."""
        show_feedback(card, True)

        assert "Correct!" in capsys.readouterr().out

    def test_show_feedback_reports_the_answer_when_incorrect(
        self, card: Flashcard, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Test that a wrong answer is named and corrected."""
        show_feedback(card, False)

        output = capsys.readouterr().out
        assert "Incorrect." in output
        assert "the library" in output


class TestShowSummary:
    """Test suite for the end-of-session summary."""

    def test_show_summary_displays_a_heading(
        self, stats: SessionStats, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Test that the summary announces itself."""
        show_summary(stats)

        assert "Quiz Summary" in capsys.readouterr().out

    def test_show_summary_displays_total_and_accuracy(
        self, stats: SessionStats, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Test that totals and a two-decimal percentage are shown."""
        show_summary(stats)

        output = capsys.readouterr().out
        assert "Total Questions" in output
        assert "8" in output
        assert "Accuracy" in output
        assert "62.50%" in output

    def test_show_summary_lists_every_missed_term(
        self, stats: SessionStats, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Test that each missed term appears in the summary."""
        show_summary(stats)

        output = capsys.readouterr().out
        for term in stats.missed_terms:
            assert term in output

    def test_show_summary_reports_none_when_nothing_missed(
        self,
        perfect_stats: SessionStats,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """Test that a clean session says so instead of listing terms."""
        show_summary(perfect_stats)

        assert "None" in capsys.readouterr().out
