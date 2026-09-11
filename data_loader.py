"""
Loading of flashcard decks from JSON files.

A deck file holds a JSON array of objects, each with a `front` and a `back`
string. This module turns such a file into Flashcard objects.
"""

import json
from pathlib import Path

from models.flashcard import Flashcard


def load_flashcards(file_path: str | Path) -> list[Flashcard]:
    """Load a deck of flashcards from a JSON file.

    The cards are returned in the order they appear in the file.
    """
    path = Path(file_path)
    with path.open(encoding="utf-8") as deck_file:
        cards = json.load(deck_file)
    return [Flashcard(card["front"], card["back"]) for card in cards]
