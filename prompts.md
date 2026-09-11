# AI Prompts

This document records the substantive prompts used with Claude Code while developing the Flashcard Quizzer. Small terminal corrections and follow-up formatting requests are omitted here but are discussed in `docs/ai_edit_log.md`.

The prompts were intentionally scoped to small development increments. Tests were generally requested before production code so that each component’s expected behavior was explicit before implementation.

## 1. Flashcard Model Tests

**Date:** 2026-09-10

```text
Review the project requirements and starter structure.

Create tests/test_flashcard.py for the first test-driven development step.
Define the minimal contract for a Flashcard:

- It stores front and back text.
- is_correct accepts answers with different capitalization.
- is_correct ignores surrounding whitespace.

Do not modify production code.
Do not modify any other file.
Keep the tests compatible with Python 3.10 and pytest.
```

## 2. Flashcard Model Implementation

**Date:** 2026-09-10

```text
Review tests/test_flashcard.py and implement only the production code
required to make those tests pass.

Create a models package and models/flashcard.py.
Use a dataclass for Flashcard.
Use a Unicode-aware case-insensitive comparison.
Add type hints and concise docstrings.

Do not modify the tests or unrelated starter files.
```

## 3. Flashcard Test Review

**Date:** 2026-09-10

```text
Review tests/test_flashcard.py. Add one test named
test_is_correct_rejects_incorrect_answer that verifies an unrelated wrong
answer returns False.

Do not modify production code. Do not modify any other file.
```

## 4. Basic JSON Deck Loader

**Date:** 2026-09-10

```text
Use test-driven development for the next small feature.

First create tests/test_data_loader.py with one test proving that a valid
JSON array of objects with front and back fields loads as Flashcard objects
in file order.

Then create data_loader.py with the smallest implementation needed to pass
that test.

Accept either str or pathlib.Path as the file path. Add type hints and
docstrings. Do not add validation cases that are not tested yet, and do not
modify unrelated files.
```

## 5. Missing and Malformed Deck Files

**Date:** 2026-09-10

```text
Extend the data loader using test-driven development.

Add a custom FlashcardDataError and tests for:

- A missing deck file producing a helpful error.
- A file containing malformed JSON producing a helpful error.

The public loader must translate those expected failures into
FlashcardDataError and preserve the original exception with exception
chaining.

Do not change unrelated modules.
```

## 6. JSON Deck Structure Validation

**Date:** 2026-09-10

```text
Extend tests/test_data_loader.py and data_loader.py as one focused TDD
increment.

Add parameterized tests that reject:

- A top-level JSON value that is not a list.
- A card entry that is not an object.
- A card missing front.
- A card missing back.
- A front value that is not a string.
- A back value that is not a string.

Also test that an empty list loads as an empty deck.

Every invalid structure must raise FlashcardDataError with a useful message.
Include the one-based card number in errors concerning an individual card.
Keep valid cards in their original file order. Do not modify unrelated files.
```

## 7. Sequential Quiz Strategy

**Date:** 2026-09-10

```text
Introduce the Strategy design pattern for card ordering using a test-first
increment.

Create tests/test_quiz_strategies.py for an abstract QuizStrategy and a
SequentialStrategy. Verify that:

- SequentialStrategy implements QuizStrategy.
- Cards remain in their original order.
- The returned value is a new list.
- The caller's sequence is not mutated.
- An empty input returns an empty list.
- QuizStrategy is abstract and cannot be used directly.

Then create quiz_strategies.py with only the implementation required by
these tests. Use Sequence[Flashcard] for inputs and list[Flashcard] for
outputs. Do not modify unrelated files.
```

## 8. Random and Adaptive Strategies

**Date:** 2026-09-10

```text
Extend the quiz strategy tests and implementation in one focused increment.

Add RandomStrategy with tests proving that:

- It implements QuizStrategy.
- A supplied seed makes ordering reproducible.
- A known seed changes the order of the test deck.
- No cards are added or removed.
- A new list is returned without mutating the input.
- An empty input returns an empty list.

Add AdaptiveStrategy with tests proving that:

- It implements QuizStrategy.
- Previously missed card fronts are presented first.
- Matching missed fronts ignores case and surrounding whitespace.
- Original relative order is preserved within the missed and remaining
  groups.
- Unknown missed fronts do not affect the deck.
- A new list is returned without mutating the input.
- An empty input returns an empty list.

Use a dedicated random.Random instance so seeded strategies are reproducible
without changing global random state. Do not modify unrelated files.
```

## 9. Quiz Engine and Session Statistics

**Date:** 2026-09-10

```text
Build the quiz engine as a test-driven increment.

First create tests/test_quiz_engine.py. Use fake callables rather than real
terminal input and output. Test that the engine:

- Asks cards in the order supplied by its injected QuizStrategy.
- Works with a different test strategy.
- Checks every answer with Flashcard.is_correct.
- Reports feedback immediately after each answer.
- Returns total questions, correct answers, percentage accuracy, and missed
  card fronts.
- Returns zero-valued statistics for an empty deck.
- Does not mutate the caller's deck.

Then create quiz_engine.py with SessionStats and QuizEngine. Keep all console
input and output outside this module. Add complete type hints and concise
docstrings. Do not modify unrelated files.
```

## 10. Terminal User Interface

**Date:** 2026-09-10

```text
Add the terminal interface as a test-first increment.

Create tests/test_ui.py using monkeypatch and capsys. Test that:

- prompt_for_answer displays the card front.
- It calls input with "Your answer: ".
- It returns the exact text entered.
- Correct feedback contains "Correct!".
- Incorrect feedback contains "Incorrect." and the expected answer.
- The summary includes a heading, total questions, correct answers, accuracy
  formatted to two decimal places, and every missed term.
- A perfect session reports that no terms were missed.

Then create ui.py with prompt_for_answer, show_feedback, and show_summary.
Keep this module limited to presentation and terminal interaction. Do not
modify unrelated files.
```

## 11. Persistent Missed-Term History

**Date:** 2026-09-10

```text
Add persistent missed-term history using test-driven development.

Create tests/test_history.py for load_missed_terms and save_missed_terms.
Test that:

- A missing history file loads as an empty list.
- Valid terms load in stored order.
- Malformed JSON raises HistoryDataError.
- The top-level value must be an object.
- The missed_terms field is required.
- missed_terms must be a list containing only strings.
- Saved terms load back unchanged.
- Saving creates missing parent directories.

Then create history.py with a custom HistoryDataError. Store JSON in the form
{"missed_terms": [...]}. Preserve useful error context and add complete type
hints and docstrings. Do not modify unrelated files.
```

## 12. Complete Command-Line Integration

**Date:** 2026-09-11

```text
Complete the Flashcard Quizzer command-line entry point using test-driven
development.

First create tests/test_main.py covering:

- Strategy creation for sequential, random, and adaptive modes.
- Rejection of unsupported mode names.
- A successful sequential session that prints feedback and a summary and
  saves missed terms.
- An adaptive session that asks a previously missed term first.
- Helpful handling of a missing deck.
- Helpful handling of malformed deck JSON.
- Helpful handling of an empty deck.
- Helpful handling of malformed history in adaptive mode.
- Non-zero status for expected failures without a traceback.

Then replace the starter main.py with an argparse-based entry point.
Support:

- A positional deck path.
- --mode with sequential, random, and adaptive choices.
- --history with a default of data/history.json.
- --seed for reproducible random mode.

Wire together the loader, history store, strategies, quiz engine, and
terminal UI. Save the current session's missed terms after a successful run.
Catch actionable data and filesystem errors, print a concise message to
stderr, and return exit status 1. Return 0 after a successful session.

Use Python 3.10-compatible type hints and do not modify unrelated files.
```

## Review and Validation Approach

After each implementation increment, the generated changes were reviewed before being committed. The review included some or all of the following commands:

```bash
python -m pytest
python -m pytest --cov=. --cov-report=term-missing
python -m black --check .
python -m isort --check-only .
python -m flake8 .
python -m mypy . --exclude=.venv
python -m bandit -q -r . -x ./.venv,./tests
```

Suggestions were not accepted solely because tests passed. The implementation was also checked for understandable error messages, separation of concerns, stable ordering, type safety, formatting, security-tool findings, and consistency with the project rubric.

Detailed outcomes, manual corrections, and lessons learned are recorded in `docs/ai_edit_log.md`.
