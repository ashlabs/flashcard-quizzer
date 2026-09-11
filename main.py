"""
Command line entry point for the Flashcard Quizzer.

This module wires the parts of the quizzer together: it reads the options
a learner typed, loads their deck and the terms they missed before, runs a
session, and records what is still to be learned. Failures that a learner
can act on are reported as a message rather than a traceback.
"""

import argparse
import sys
from collections.abc import Collection, Sequence
from pathlib import Path

from data_loader import FlashcardDataError, load_flashcards
from history import HistoryDataError, load_missed_terms, save_missed_terms
from quiz_engine import QuizEngine
from quiz_strategies import (
    AdaptiveStrategy,
    QuizStrategy,
    RandomStrategy,
    SequentialStrategy,
)
from ui import prompt_for_answer, show_feedback, show_summary

SEQUENTIAL_MODE = "sequential"
RANDOM_MODE = "random"
ADAPTIVE_MODE = "adaptive"
MODES = (SEQUENTIAL_MODE, RANDOM_MODE, ADAPTIVE_MODE)

DEFAULT_HISTORY_PATH = Path("data/history.json")


def create_strategy(
    mode: str,
    missed_terms: Collection[str],
    seed: int | None = None,
) -> QuizStrategy:
    """Return the ordering strategy that a mode name asks for.

    Args:
        mode: One of "sequential", "random", or "adaptive".
        missed_terms: Terms missed in earlier sessions, used by the
            adaptive ordering to ask the hardest cards first.
        seed: Seed for the random ordering, which makes it repeatable.

    Raises:
        ValueError: If the mode is not one this quizzer supports.
    """
    if mode == SEQUENTIAL_MODE:
        return SequentialStrategy()
    if mode == RANDOM_MODE:
        return RandomStrategy(seed)
    if mode == ADAPTIVE_MODE:
        return AdaptiveStrategy(missed_terms)
    supported = ", ".join(MODES)
    error_message = f"Unsupported quiz mode {mode!r}: choose one of {supported}"
    raise ValueError(error_message)


def build_parser() -> argparse.ArgumentParser:
    """Return the parser for the quizzer's command line options."""
    parser = argparse.ArgumentParser(
        description="Quiz yourself on a deck of flashcards.",
    )
    parser.add_argument(
        "deck_path",
        metavar="DECK_PATH",
        type=Path,
        help="path of the JSON deck file to be quizzed on",
    )
    parser.add_argument(
        "--mode",
        choices=MODES,
        default=SEQUENTIAL_MODE,
        help=f"order the cards are asked in (default: {SEQUENTIAL_MODE})",
    )
    parser.add_argument(
        "--history",
        dest="history_path",
        metavar="HISTORY_PATH",
        type=Path,
        default=DEFAULT_HISTORY_PATH,
        help=(
            "path of the missed term history file " f"(default: {DEFAULT_HISTORY_PATH})"
        ),
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="seed for the random mode, making its order repeatable",
    )
    return parser


def run_quiz(args: argparse.Namespace) -> None:
    """Run one quiz session as the parsed arguments describe it.

    Past mistakes are read only for the adaptive mode, so a history
    file that cannot be parsed does not stop an unrelated session. The
    session's own misses then replace the stored history, which drops
    the terms that were answered correctly this time.

    Raises:
        FlashcardDataError: If the deck cannot be loaded or is empty.
        HistoryDataError: If adaptive mode cannot read the history.
        OSError: If the history file cannot be written.
    """
    cards = load_flashcards(args.deck_path)
    if not cards:
        raise FlashcardDataError(f"Flashcard file is empty: {args.deck_path}")

    missed_terms: list[str] = []
    if args.mode == ADAPTIVE_MODE:
        missed_terms = load_missed_terms(args.history_path)

    strategy = create_strategy(args.mode, missed_terms, args.seed)
    stats = QuizEngine(strategy).run(
        cards,
        prompt_for_answer,
        show_feedback,
    )
    show_summary(stats)
    save_missed_terms(args.history_path, stats.missed_terms)


def main(argv: Sequence[str] | None = None) -> int:
    """Run the quizzer and return the status to exit with.

    Args:
        argv: The command line arguments, defaulting to the real ones.

    Returns:
        0 once a session has finished, or 1 when a deck or history
        file could not be used.
    """
    args = build_parser().parse_args(argv)
    try:
        run_quiz(args)
    except (FlashcardDataError, HistoryDataError, OSError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
