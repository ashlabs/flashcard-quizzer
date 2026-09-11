# Claude Code Instructions for Flashcard Quizzer

## Project Context

Flashcard Quizzer is a Python 3.10 command-line learning application. It loads flashcards from JSON, quizzes learners using multiple ordering strategies, provides immediate feedback, summarizes results, and stores missed terms for subsequent adaptive sessions.

This is an AI-assisted development course project. Changes must demonstrate sound engineering judgment, test-driven development (TDD), modular design, and critical review of AI-generated work.

## Development Approach

Work in small, reviewable increments:

1. Inspect the relevant code and tests before suggesting changes.
2. Define behavior with tests before implementing new functionality.
3. Run focused tests while developing.
4. Run the complete test suite after the focused tests pass.
5. Run formatting, linting, typing, security, and coverage checks.
6. Explain important design decisions and tradeoffs.
7. Do not modify unrelated files.

Do not generate a large implementation when a smaller tested increment will satisfy the request.

## Project Architecture

* `models/flashcard.py` defines the Flashcard domain model and answer checking.
* `data_loader.py` loads and validates JSON flashcard decks.
* `quiz_strategies.py` contains sequential, random, and adaptive ordering strategies.
* `quiz_engine.py` runs quiz sessions and calculates session statistics.
* `ui.py` handles terminal input and output.
* `history.py` loads and saves missed-term history.
* `main.py` parses command-line arguments and connects the application components.
* `tests/` contains the pytest test suite.
* `examples/` contains sample flashcard decks.
* `docs/ai_edit_log.md` records significant AI-assisted development interactions.
* `prompts.md` records the substantive prompts used during development.

## Design Requirements

* Use the Strategy pattern for quiz ordering.
* Keep terminal input and output outside the quiz engine.
* Inject answer and feedback callables into the engine.
* Do not mutate caller-owned card sequences.
* Preserve card order unless the selected strategy intentionally changes it.
* Use `strip().casefold()` for answer and missed-term normalization.
* Use custom exceptions for deck and history data failures.
* Report actionable command-line errors without exposing tracebacks.
* Use pseudo-randomness only for non-security-sensitive card shuffling.
* Keep runtime dependencies in the Python standard library.

## Python Standards

* Support Python 3.10 or later.
* Add type annotations to functions and methods.
* Use concise, useful docstrings.
* Prefer small functions and explicit names.
* Preserve exception context with `raise ... from exc` when translating errors.
* Avoid unnecessary abstractions and dependencies.
* Keep Black and flake8 configuration consistent.

## Testing Standards

Tests should cover:

* Normal behavior
* Boundary conditions
* Invalid input
* Error translation
* Non-mutation guarantees
* Strategy-specific ordering
* User-visible CLI behavior
* Persistent history behavior

Use pytest fixtures and parameterization when they make tests clearer. Use fake or injected callables instead of real terminal interaction in unit tests.

The configured coverage threshold is 81%, exceeding the project requirement of greater than 80%.

## Quality Commands

Run the complete quality gate with:

```bash
python -m isort --check-only .
python -m black --check .
python -m flake8 .
python -m mypy . --exclude=.venv
python -m bandit -q -r . -x ./.venv,./tests
python -m pytest -q --cov=. --cov-report=term-missing
```

Run the application with:

```bash
python main.py examples/server_acronyms.json
```

Run an adaptive session with:

```bash
python main.py examples/server_acronyms.json --mode adaptive
```

Run a reproducible random session with:

```bash
python main.py examples/server_acronyms.json --mode random --seed 7
```

## AI Collaboration Expectations

* Treat AI output as a proposal requiring review.
* Explain generated code before accepting it.
* Verify recommendations against the project requirements.
* Correct unnecessary complexity, missing edge cases, and formatting problems.
* Do not claim checks passed unless they were actually run.
* Record meaningful prompts, accepted changes, rejected suggestions, manual corrections, and lessons learned.
* Never add credentials, API keys, virtual environments, caches, coverage data, or generated learner history to version control.
