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


def load_flashcards(file_path: str | Path) -> list[Flashcard]:
    """Load a deck of flashcards from a JSON file.

    The cards are returned in the order they appear in the file.

    Raises:
        FlashcardDataError: If the deck file does not exist, or if it does
            not contain valid JSON.
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
    return [Flashcard(card["front"], card["back"]) for card in cards]
