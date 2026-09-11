"""
Loading of flashcard decks from JSON files.

A deck file holds a JSON array of objects, each with a `front` and a `back`
string. This module turns such a file into Flashcard objects.
"""

import json
from pathlib import Path

from models.flashcard import Flashcard


class FlashcardDataError(Exception):
    """Raised when a flashcard deck cannot be loaded."""


def _parse_card(card: object, number: int) -> Flashcard:
    """Convert one entry of a deck file into a Flashcard.

    Args:
        card: The value found in the deck's list of cards.
        number: The one-based position of the card in the file, used to
            point at the offending card in error messages.

    Raises:
        FlashcardDataError: If the card is not an object, is missing a
            required field, or has a field that is not a string.
    """
    if not isinstance(card, dict):
        message = f"Invalid card {number}: each card must be an object"
        raise FlashcardDataError(message)
    for field in ("front", "back"):
        if field not in card:
            message = f'Invalid card {number}: missing "{field}" field'
            raise FlashcardDataError(message)
        if not isinstance(card[field], str):
            raise FlashcardDataError(
                f'Invalid card {number}: "{field}" must be a string'
            )
    return Flashcard(card["front"], card["back"])


def load_flashcards(file_path: str | Path) -> list[Flashcard]:
    """Load a deck of flashcards from a JSON file.

    The cards are returned in the order they appear in the file. A file
    holding an empty list is valid and yields an empty deck.

    Raises:
        FlashcardDataError: If the deck file does not exist, does not
            contain valid JSON, or does not hold a list of well-formed
            cards.
    """
    path = Path(file_path)
    try:
        with path.open(encoding="utf-8") as deck_file:
            cards = json.load(deck_file)
    except FileNotFoundError as exc:
        raise FlashcardDataError(f"Flashcard file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        message = f"Invalid JSON in flashcard file: {path}"
        raise FlashcardDataError(message) from exc

    if not isinstance(cards, list):
        message = f"Flashcard file must contain a list of cards: {path}"
        raise FlashcardDataError(message)

    flashcards = []

    for number, card in enumerate(cards, start=1):
        flashcards.append(_parse_card(card, number))

    return flashcards
