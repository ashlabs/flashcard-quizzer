"""
The engine that runs a flashcard quiz.

The engine owns the shape of a session: the order of the questions, the
grading, and the running tally. It does not own the conversation with the
learner. Answers arrive from a caller-supplied callable and feedback goes
back out through another, which keeps this module free of input and output.
"""

from collections.abc import Callable, Sequence
from dataclasses import dataclass, field

from models.flashcard import Flashcard
from quiz_strategies import QuizStrategy


@dataclass
class SessionStats:
    """The tally of a single quiz session."""

    total_questions: int = 0
    correct_answers: int = 0
    missed_terms: list[str] = field(default_factory=list)

    @property
    def accuracy(self) -> float:
        """Return the share of correct answers as a percentage.

        A session with no questions scores 0.0 rather than dividing by
        zero.
        """
        if self.total_questions == 0:
            return 0.0
        return self.correct_answers / self.total_questions * 100


class QuizEngine:
    """Runs a deck of flashcards past a learner and scores the result."""

    def __init__(self, strategy: QuizStrategy) -> None:
        """Store the strategy that decides the order of the questions."""
        self._strategy = strategy

    def run(
        self,
        cards: Sequence[Flashcard],
        answer_provider: Callable[[Flashcard], str],
        feedback_provider: Callable[[Flashcard, bool], None],
    ) -> SessionStats:
        """Quiz the deck and return the statistics for the session.

        Args:
            cards: The deck to quiz. It is left unchanged.
            answer_provider: Called once per card to obtain an answer.
            feedback_provider: Called with each card and whether the
                answer given for it was correct.
        """
        stats = SessionStats()
        for card in self._strategy.order_cards(cards):
            correct = card.is_correct(answer_provider(card))
            feedback_provider(card, correct)
            stats.total_questions += 1
            if correct:
                stats.correct_answers += 1
            else:
                stats.missed_terms.append(card.front)
        return stats
