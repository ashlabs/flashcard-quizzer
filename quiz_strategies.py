"""
Ordering strategies for a flashcard quiz.

A quiz asks its strategy for the order in which to present a deck. Keeping
that decision behind a small interface lets other orderings be added later
without changing the quiz itself.
"""

from abc import ABC, abstractmethod
from collections.abc import Sequence

from models.flashcard import Flashcard


class QuizStrategy(ABC):
    """Interface for deciding the order in which cards are quizzed."""

    @abstractmethod
    def order_cards(self, cards: Sequence[Flashcard]) -> list[Flashcard]:
        """Return the cards in the order they should be quizzed."""


class SequentialStrategy(QuizStrategy):
    """Quiz the cards in the order the deck already has."""

    def order_cards(self, cards: Sequence[Flashcard]) -> list[Flashcard]:
        """Return a new list of the cards in their original order."""
        return list(cards)
