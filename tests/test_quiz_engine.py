"""
Unit tests for the quiz engine.

These tests are written before the implementation and define how the engine
drives a quiz: it asks the cards in the order its strategy chooses, checks
each answer as it arrives, reports feedback straight away, and summarizes
the session. Input and output belong to the caller, so the engine talks to
plain callables rather than the terminal.
"""

from collections.abc import Sequence

import pytest

from models.flashcard import Flashcard
from quiz_engine import QuizEngine, SessionStats
from quiz_strategies import QuizStrategy, SequentialStrategy


class ReverseStrategy(QuizStrategy):
    """Test double that quizzes a deck back to front."""

    def order_cards(self, cards: Sequence[Flashcard]) -> list[Flashcard]:
        """Return a new list holding the cards in reverse order."""
        return list(reversed(cards))


class RecordingSession:
    """A fake learner that answers from a script and logs the exchange."""

    def __init__(self, answers: dict[str, str]) -> None:
        """Store the answer to give for each card front."""
        self._answers = answers
        self.asked: list[Flashcard] = []
        self.feedback: list[tuple[Flashcard, bool]] = []
        self.events: list[str] = []

    def answer(self, card: Flashcard) -> str:
        """Return the scripted answer and record that it was asked."""
        self.asked.append(card)
        self.events.append("ask")
        return self._answers[card.front]

    def record_feedback(self, card: Flashcard, correct: bool) -> None:
        """Record the verdict the engine reports for a card."""
        self.feedback.append((card, correct))
        self.events.append("feedback")


@pytest.fixture
def cards() -> list[Flashcard]:
    """Return a small deck of flashcards in a known order."""
    return [
        Flashcard("la biblioteca", "the library"),
        Flashcard("el libro", "the book"),
        Flashcard("la ventana", "the window"),
        Flashcard("la puerta", "the door"),
    ]


@pytest.fixture
def session() -> RecordingSession:
    """Return a session answering every card but "la ventana" right."""
    return RecordingSession(
        {
            "la biblioteca": "THE LIBRARY",
            "el libro": "   the book   ",
            "la ventana": "the door",
            "la puerta": "the door",
        }
    )


class TestQuizEngine:
    """Test suite for QuizEngine behavior."""

    def test_engine_asks_cards_in_strategy_order(
        self, cards: list[Flashcard], session: RecordingSession
    ) -> None:
        """Test that questions follow the order the strategy returns."""
        engine = QuizEngine(SequentialStrategy())

        engine.run(cards, session.answer, session.record_feedback)

        assert session.asked == cards

    def test_engine_uses_an_injected_strategy(
        self, cards: list[Flashcard], session: RecordingSession
    ) -> None:
        """Test that another strategy changes the order of questions."""
        engine = QuizEngine(ReverseStrategy())

        engine.run(cards, session.answer, session.record_feedback)

        assert session.asked == list(reversed(cards))

    def test_feedback_reports_each_verdict_immediately(
        self, cards: list[Flashcard], session: RecordingSession
    ) -> None:
        """Test that each answer is judged before the next question."""
        engine = QuizEngine(SequentialStrategy())

        engine.run(cards, session.answer, session.record_feedback)

        assert session.events == ["ask", "feedback"] * len(cards)
        assert session.feedback == [
            (cards[0], True),
            (cards[1], True),
            (cards[2], False),
            (cards[3], True),
        ]

    def test_run_reports_totals_and_accuracy(
        self, cards: list[Flashcard], session: RecordingSession
    ) -> None:
        """Test that the summary counts questions and correct answers."""
        engine = QuizEngine(SequentialStrategy())

        stats = engine.run(cards, session.answer, session.record_feedback)

        assert isinstance(stats, SessionStats)
        assert stats.total_questions == 4
        assert stats.correct_answers == 3
        assert stats.accuracy == pytest.approx(75.0)

    def test_run_reports_the_fronts_of_missed_cards(
        self, cards: list[Flashcard], session: RecordingSession
    ) -> None:
        """Test that missed terms name the front of each wrong card."""
        engine = QuizEngine(SequentialStrategy())

        stats = engine.run(cards, session.answer, session.record_feedback)

        assert stats.missed_terms == ["la ventana"]

    def test_empty_deck_produces_zero_stats_and_no_callbacks(
        self, session: RecordingSession
    ) -> None:
        """Test that an empty deck is a valid, empty quiz session."""
        engine = QuizEngine(SequentialStrategy())

        stats = engine.run([], session.answer, session.record_feedback)

        assert stats.total_questions == 0
        assert stats.correct_answers == 0
        assert stats.accuracy == 0.0
        assert stats.missed_terms == []
        assert session.events == []

    def test_run_does_not_mutate_the_callers_deck(
        self, cards: list[Flashcard], session: RecordingSession
    ) -> None:
        """Test that running a quiz leaves the caller's deck alone."""
        original = list(cards)
        engine = QuizEngine(ReverseStrategy())

        engine.run(cards, session.answer, session.record_feedback)

        assert cards == original
