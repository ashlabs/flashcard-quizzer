"""
Ordering strategies for a flashcard quiz.

A quiz asks its strategy for the order in which to present a deck. Keeping
that decision behind a small interface lets other orderings be added later
without changing the quiz itself.
"""

import random
from abc import ABC, abstractmethod
from collections.abc import Collection, Sequence

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


class RandomStrategy(QuizStrategy):
    """Quiz the cards in a shuffled order.

    A seed makes the shuffle reproducible, which keeps tests and repeated
    study sessions predictable.
    """

    def __init__(self, seed: int | None = None) -> None:
        """Keep a generator of this strategy's own, seeded if asked."""
        self._random = random.Random(seed)  # nosec B311

    def order_cards(self, cards: Sequence[Flashcard]) -> list[Flashcard]:
        """Return a new list holding the cards in a shuffled order."""
        shuffled = list(cards)
        self._random.shuffle(shuffled)
        return shuffled


def _normalize(front: str) -> str:
    """Return front text in the form used to compare missed cards."""
    return front.strip().casefold()


class AdaptiveStrategy(QuizStrategy):
    """Quiz previously missed cards ahead of the rest of the deck."""

    def __init__(self, missed_fronts: Collection[str]) -> None:
        """Store the normalized fronts of the cards missed so far."""
        self._missed = {_normalize(front) for front in missed_fronts}

    def order_cards(self, cards: Sequence[Flashcard]) -> list[Flashcard]:
        """Return a new list with missed cards first.

        Cards keep their deck order within the missed group and within
        the remaining group.
        """
        missed: list[Flashcard] = []
        remaining: list[Flashcard] = []
        for card in cards:
            if _normalize(card.front) in self._missed:
                missed.append(card)
            else:
                remaining.append(card)
        return missed + remaining
