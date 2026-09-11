"""
Unit tests for the Flashcard model.

These tests are written before the implementation as the first step of a
test-driven development cycle for the Flashcard Quizzer application. They
define the minimal contract for a flashcard: it remembers the text on each
side, and it forgives differences in capitalization and surrounding whitespace
when checking an answer.
"""

from models.flashcard import Flashcard


class TestFlashcard:
    """Test suite for Flashcard functionality."""

    def test_flashcard_stores_front_and_back_text(self) -> None:
        """Test that a flashcard exposes the text it was created with."""
        card = Flashcard("la biblioteca", "the library")
        assert card.front == "la biblioteca"
        assert card.back == "the library"

    def test_is_correct_accepts_case_insensitive_answer(self) -> None:
        """Test that an answer differing only in case is accepted."""
        card = Flashcard("la biblioteca", "the library")
        assert card.is_correct("The Library")

    def test_is_correct_ignores_surrounding_whitespace(self) -> None:
        """Test that leading/trailing whitespace in an answer is ignored."""
        card = Flashcard("la biblioteca", "the library")
        assert card.is_correct("   the library   ")

    def test_is_correct_rejects_incorrect_answer(self) -> None:
        """Test that an answer unrelated to the back text is rejected."""
        card = Flashcard("la biblioteca", "the library")
        assert not card.is_correct("the bookstore")
