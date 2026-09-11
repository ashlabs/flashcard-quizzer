"""
Flashcard model for the Flashcard Quizzer application.

A flashcard holds the text on each of its two sides and knows how to check
a learner's answer against the text on its back.
"""

from dataclasses import dataclass


@dataclass
class Flashcard:
    """A single flashcard with a prompt side and an answer side."""

    front: str
    back: str

    def is_correct(self, answer: str) -> bool:
        """Return True if the answer matches the back text.

        Surrounding whitespace is ignored and the comparison is
        case-insensitive.
        """
        return answer.strip().casefold() == self.back.strip().casefold()
