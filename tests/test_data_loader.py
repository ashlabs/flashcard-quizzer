"""
Unit tests for the flashcard data loader.

These tests are written before the implementation as the next step of the
test-driven development cycle for the Flashcard Quizzer application. They
define the contract for loading a deck: given a JSON file of card objects,
the loader returns the equivalent Flashcard objects in file order.
"""

import json
from pathlib import Path

import pytest

from data_loader import FlashcardDataError, load_flashcards
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

    def test_load_flashcards_raises_helpful_error_when_file_is_missing(
        self, tmp_path: Path
    ) -> None:
        """Test that a missing file raises a helpfulcodes data error."""
        missing_path = tmp_path / "no_such_deck.json"

        expected_message = "Flashcard file not found"
        with pytest.raises(FlashcardDataError, match=expected_message):
            load_flashcards(missing_path)

    def test_load_flashcards_raises_helpful_error_for_malformed_json(
        self, tmp_path: Path
    ) -> None:
        """Test that a file that is not valid JSON raises a helpful error."""
        malformed_path = tmp_path / "malformed.json"
        malformed_path.write_text("this is not json {{", encoding="utf-8")

        with pytest.raises(FlashcardDataError, match="Invalid JSON"):
            load_flashcards(malformed_path)
