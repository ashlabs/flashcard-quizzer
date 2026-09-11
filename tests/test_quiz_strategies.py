"""
Unit tests for the quiz ordering strategies.

These tests are written before the implementation as the next step of the
test-driven development cycle for the Flashcard Quizzer application. They
define the contract for the simplest strategy: SequentialStrategy hands the
quiz its cards in the order the deck already has, without disturbing the
caller's list. Randomized and adaptive strategies come later.
"""

import inspect
import pytest

from models.flashcard import Flashcard
from quiz_strategies import QuizStrategy, SequentialStrategy


@pytest.fixture
def cards() -> list[Flashcard]:
    """Return a small deck of flashcards in a known order."""
    return [
        Flashcard("la biblioteca", "the library"),
        Flashcard("el libro", "the book"),
        Flashcard("la ventana", "the window"),
    ]


@pytest.fixture
def strategy() -> SequentialStrategy:
    """Return the strategy under test."""
    return SequentialStrategy()


class TestSequentialStrategy:
    """Test suite for SequentialStrategy ordering behavior."""

    def test_sequential_strategy_is_a_quiz_strategy(
        self, strategy: SequentialStrategy
    ) -> None:
        """Test that the concrete strategy implements the base class."""
        assert isinstance(strategy, QuizStrategy)

    def test_order_cards_preserves_original_order(
        self, strategy: SequentialStrategy, cards: list[Flashcard]
    ) -> None:
        """Test that cards come back in the order they were given."""
        ordered = strategy.order_cards(cards)

        assert ordered == cards

    def test_order_cards_returns_a_new_list(
        self, strategy: SequentialStrategy, cards: list[Flashcard]
    ) -> None:
        """Test that the result is a new list, not the caller's list."""
        ordered = strategy.order_cards(cards)

        assert ordered is not cards

    def test_order_cards_does_not_mutate_the_caller_list(
        self, strategy: SequentialStrategy, cards: list[Flashcard]
    ) -> None:
        """Test that ordering leaves the caller's list untouched."""
        original = list(cards)

        strategy.order_cards(cards)

        assert cards == original

    def test_order_cards_returns_empty_list_for_no_cards(
        self, strategy: SequentialStrategy
    ) -> None:
        """Test that an empty deck produces an empty list."""
        assert strategy.order_cards([]) == []

    def test_quiz_strategy_is_abstract(self) -> None:
        """Test that the base strategy cannot be used directly."""
        assert inspect.isabstract(QuizStrategy)
