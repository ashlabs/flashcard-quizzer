"""
Unit tests for the quiz ordering strategies.

The tests define the shared strategy contract and verify sequential, random,
and adaptive ordering without allowing a strategy to mutate the caller's deck.
"""

import inspect

import pytest

from models.flashcard import Flashcard
from quiz_strategies import (
    AdaptiveStrategy,
    QuizStrategy,
    RandomStrategy,
    SequentialStrategy,
)

# A seed that shuffles the three-card ``cards`` fixture into an order
# other than the one it was built in.
REORDERING_SEED = 1


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


class TestRandomStrategy:
    """Test suite for RandomStrategy ordering behavior."""

    def test_random_strategy_is_a_quiz_strategy(self) -> None:
        """Test that the strategy implements the base class."""
        assert isinstance(RandomStrategy(), QuizStrategy)

    def test_same_seed_repeats_order(self, cards: list[Flashcard]) -> None:
        """Test that a shared seed makes the shuffle reproducible."""
        first = RandomStrategy(REORDERING_SEED).order_cards(cards)
        second = RandomStrategy(REORDERING_SEED).order_cards(cards)

        assert first == second

    def test_seeded_order_differs_from_the_original_order(
        self, cards: list[Flashcard]
    ) -> None:
        """Test that the chosen seed really does reorder the deck."""
        ordered = RandomStrategy(REORDERING_SEED).order_cards(cards)

        assert ordered != cards

    def test_order_cards_keeps_exactly_the_original_cards(
        self, cards: list[Flashcard]
    ) -> None:
        """Test that shuffling neither drops nor invents cards."""
        ordered = RandomStrategy(REORDERING_SEED).order_cards(cards)

        assert len(ordered) == len(cards)
        assert all(card in ordered for card in cards)

    def test_order_cards_returns_a_new_list_and_keeps_input(
        self, cards: list[Flashcard]
    ) -> None:
        """Test that the caller's list is neither reused nor changed."""
        original = list(cards)

        ordered = RandomStrategy(REORDERING_SEED).order_cards(cards)

        assert ordered is not cards
        assert cards == original

    def test_order_cards_returns_empty_list_for_no_cards(self) -> None:
        """Test that an empty deck produces an empty list."""
        assert RandomStrategy(REORDERING_SEED).order_cards([]) == []


class TestAdaptiveStrategy:
    """Test suite for AdaptiveStrategy ordering behavior."""

    def test_adaptive_strategy_is_a_quiz_strategy(self) -> None:
        """Test that the strategy implements the base class."""
        assert isinstance(AdaptiveStrategy([]), QuizStrategy)

    def test_missed_cards_come_first(self, cards: list[Flashcard]) -> None:
        """Test that a previously missed card moves to the front."""
        strategy = AdaptiveStrategy(["la ventana"])

        ordered = strategy.order_cards(cards)

        assert ordered == [cards[2], cards[0], cards[1]]

    def test_missed_front_matching_ignores_case_and_whitespace(
        self, cards: list[Flashcard]
    ) -> None:
        """Test that missed fronts match the way answers are checked."""
        strategy = AdaptiveStrategy(["   LA VENTANA  "])

        ordered = strategy.order_cards(cards)

        assert ordered[0] == cards[2]

    def test_relative_order_is_preserved_within_each_group(
        self, cards: list[Flashcard]
    ) -> None:
        """Test that deck order survives inside both groups."""
        strategy = AdaptiveStrategy(["la ventana", "la biblioteca"])

        ordered = strategy.order_cards(cards)

        assert ordered == [cards[0], cards[2], cards[1]]

    def test_unknown_missed_fronts_leave_the_order_unchanged(
        self, cards: list[Flashcard]
    ) -> None:
        """Test that missed fronts outside the deck are ignored."""
        strategy = AdaptiveStrategy(["el coche", "la casa"])

        ordered = strategy.order_cards(cards)

        assert ordered == cards

    def test_order_cards_returns_a_new_list_and_keeps_input(
        self, cards: list[Flashcard]
    ) -> None:
        """Test that the caller's list is neither reused nor changed."""
        original = list(cards)
        strategy = AdaptiveStrategy(["la ventana"])

        ordered = strategy.order_cards(cards)

        assert ordered is not cards
        assert cards == original

    def test_order_cards_returns_empty_list_for_no_cards(self) -> None:
        """Test that an empty deck produces an empty list."""
        assert AdaptiveStrategy(["la ventana"]).order_cards([]) == []
