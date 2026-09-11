"""
Terminal presentation for the flashcard quizzer.

This module is the only place that talks to the console: it shows the term
being asked, reads the learner's answer, reports the verdict, and prints
the closing summary. Keeping that here lets the quiz engine stay free of
input and output.
"""

from models.flashcard import Flashcard
from quiz_engine import SessionStats

LABEL_WIDTH = 18


def prompt_for_answer(card: Flashcard) -> str:
    """Show a card's front text and return the answer as it was typed."""
    print()
    print(f"Term: {card.front}")
    return input("Your answer: ")


def show_feedback(card: Flashcard, correct: bool) -> None:
    """Report whether an answer was right, naming it when it was not."""
    if correct:
        print("Correct!")
    else:
        print(f"Incorrect. The answer is: {card.back}")


def show_summary(stats: SessionStats) -> None:
    """Print the closing summary of a quiz session."""
    print()
    print("=== Quiz Summary ===")
    print(f"{'Total Questions':<{LABEL_WIDTH}} | " f"{stats.total_questions}")
    print(f"{'Correct Answers':<{LABEL_WIDTH}} | " f"{stats.correct_answers}")
    print(f"{'Accuracy':<{LABEL_WIDTH}} | " f"{stats.accuracy:.2f}%")
    print()
    print("Missed Terms")
    if stats.missed_terms:
        for term in stats.missed_terms:
            print(f"  {term}")
    else:
        print("  None")
