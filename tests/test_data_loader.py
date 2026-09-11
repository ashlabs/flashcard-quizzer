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

INVALID_DECKS = [
    pytest.param(
        {"front": "la biblioteca", "back": "the library"},
        r"must contain a list",
        id="top_level_object_instead_of_list",
    ),
    pytest.param(
        ["not a flashcard object"],
        r"card must be an object",
        id="card_is_not_an_object",
    ),
    pytest.param(
        [{"back": "the library"}],
        r"missing.*front",
        id="card_missing_front",
    ),
    pytest.param(
        [{"front": "la biblioteca"}],
        r"missing.*back",
        id="card_missing_back",
    ),
    pytest.param(
        [{"front": 42, "back": "the library"}],
        r"front.*must be a string",
        id="front_not_a_string",
    ),
    pytest.param(
        [{"front": "la biblioteca", "back": ["the library"]}],
        r"back.*must be a string",
        id="back_not_a_string",
    ),
]


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
        """Test that a missing file raises a helpful data error."""
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

    @pytest.mark.parametrize("deck, expected_message", INVALID_DECKS)
    def test_load_flashcards_rejects_invalid_deck_structure(
        self, tmp_path: Path, deck: object, expected_message: str
    ) -> None:
        """Test that a structurally invalid deck is rejected."""
        deck_path = tmp_path / "deck.json"
        deck_path.write_text(json.dumps(deck), encoding="utf-8")

        with pytest.raises(FlashcardDataError, match=expected_message):
            load_flashcards(deck_path)

    def test_load_flashcards_returns_empty_list_for_empty_deck(
        self, tmp_path: Path
    ) -> None:
        """Test that an empty deck is valid and loads as no cards."""
        deck_path = tmp_path / "empty_deck.json"
        deck_path.write_text(json.dumps([]), encoding="utf-8")

        assert load_flashcards(deck_path) == []
