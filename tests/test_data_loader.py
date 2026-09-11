"""
Unit tests for the flashcard data loader.

These tests are written before the implementation as the next step of the
test-driven development cycle for the Flashcard Quizzer application. They
define the contract for loading a deck: given a JSON file of card objects,
the loader returns the equivalent Flashcard objects in file order.
"""

import json
from pathlib import Path

from data_loader import load_flashcards
from models.flashcard import Flashcard


class TestLoadFlashcards:
    """Test suite for load_flashcards functionality."""

    def test_load_flashcards_returns_cards_from_valid_json(
        self, tmp_path: Path
    ) -> None:
        """Test that a valid JSON deck is loaded as Flashcard objects."""
        cards = [
            {"front": "la biblioteca", "back": "the library"},
            {"front": "el libro", "back": "the book"},
        ]
        deck_path = tmp_path / "deck.json"
        deck_path.write_text(json.dumps(cards), encoding="utf-8")

        loaded = load_flashcards(deck_path)

        assert len(loaded) == 2
        assert all(isinstance(card, Flashcard) for card in loaded)
        assert loaded[0].front == "la biblioteca"
        assert loaded[0].back == "the library"
        assert loaded[1].front == "el libro"
        assert loaded[1].back == "the book"
