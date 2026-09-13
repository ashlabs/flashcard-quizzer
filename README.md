# Flashcard Quizzer

Flashcard Quizzer is a Python command-line learning application that loads flashcards from JSON, quizzes the learner, provides immediate feedback, and records missed terms for future adaptive sessions.

The project demonstrates test-driven development (TDD), modular design, data validation, state persistence, and the Strategy design pattern.

## Features

* Loads flashcard decks from JSON files.
* Validates malformed files and invalid deck structures.
* Compares answers in a case-insensitive manner and ignores surrounding whitespace.
* Provides immediate feedback (`correct` or `incorrect`).
* Supports multiple quiz modes: `sequential`, `random`, and `adaptive`.
* Supports reproducible random ordering with a seed.
* Saves missed terms between sessions.
* Prioritizes previously missed terms in adaptive mode.
* Displays total questions, correct answers, accuracy, and missed terms.
* Gracefully handles errors and reports user-facing error messages without exposing stack traces.

## Requirements

* Python 3.10 or later
* pip
* git

Python 3.10 or later is required because the application uses modern type annotation syntax such as `str | Path`.

## Setup

Clone the repository and enter the project directory:

```bash
git clone https://github.com/ashlabs/flashcard-quizzer.git
cd flashcard-quizzer
```

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell, activate it with:

```powershell
.venv\Scripts\Activate.ps1
```

Install the dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Flashcard Deck Format

A deck is a JSON array containing one object per flashcard. Every object must contain string values named `front` and `back`.

Example:

```json
[
  {
    "front": "HTTP",
    "back": "Hypertext Transfer Protocol"
  },
  {
    "front": "DNS",
    "back": "Domain Name System"
  }
]
```

A sample deck is available in `examples/server_acronyms.json`.

The loader provides helpful error messages when:

* The deck file does not exist.
* The file does not contain valid JSON.
* The top-level JSON value is not a list.
* A card is not an object.
* A card is missing `front` or `back`.
* Either field is not a string.

An empty JSON list is a valid data structure, but the command-line application will report that the deck has no cards to quiz.

## Usage


```bash
python main.py DECK_PATH [--mode MODE] [--history HISTORY_PATH] [--seed SEED]
```

### Sequential Mode

Sequential mode presents cards in the order stored in the JSON file. This is the default mode.

```bash
python main.py examples/server_acronyms.json
```

The mode can also be specified explicitly.

```bash
python main.py examples/server_acronyms.json --mode sequential
```

### Random Mode

Random mode presents the cards in shuffled order.

```bash
python main.py examples/server_acronyms.json --mode random
```

Supply a seed to reproduce the shuffle.

```bash
python main.py examples/server_acronyms.json --mode random --seed 7
```

Random ordering uses pseudo-randomness because card shuffling is not a security-sensitive operation.

### Adaptive Mode

Adaptive mode reads the missed-term history and presents previously missed cards first. Cards retain their original relative order within the missed and remaining groups.

```bash
python main.py examples/server_acronyms.json --mode adaptive
```

A custom history path can be supplied.

```bash
python main.py examples/server_acronyms.json --mode adaptive --history data/my_history.json
```

The default history path is `data/history.json`. Missing folders are created automatically when history is saved.

At the end of every successful session, the history is replaced with the terms missed during that session. If a learner answers every card correctly the history list is empty.

### Command-Line Help

Display all available options with:

```bash
python main.py --help
```

## Answer Checking

Answers are compared using:

* Strip Leading and trailing whitespace
* Unicode-aware case-insensitive comparison

For example, these answers are treated as equivalent:

```text
Hypertext Transfer Protocol
hypertext tranSFer protocol
  HYPERTEXT TRANSFER PROTOCOL
```

## Example Session

```text
Term: HTTP
Your answer: Hypertext Transfer Protocol
Correct!

Term: DNS
Your answer: domain name service
Incorrect. The answer is: Domain Name System

=== Quiz Summary ===
Total Questions    | 2
Correct Answers    | 1
Accuracy           | 50.00%

Missed Terms
  DNS
```

## Architecture

The application separates its responsibilities across small modules:

```text
flashcard-quizzer/
├── data_loader.py
├── history.py
├── main.py
├── models/
│   ├── __init__.py
│   └── flashcard.py
├── quiz_engine.py
├── quiz_strategies.py
├── ui.py
├── examples/
│   └── server_acronyms.json
├── tests/
│   ├── test_data_loader.py
│   ├── test_flashcard.py
│   ├── test_history.py
│   ├── test_main.py
│   ├── test_quiz_engine.py
│   ├── test_quiz_strategies.py
│   └── test_ui.py
└── docs/
    ├── ai_edit_log.md
    ├── design_patterns.md
    ├── project_rubric.md
    └── report_template.md
```

Module responsibilities:

|Module|Responsibility|
|---|---|
|`models/flashcard.py`|Defines the flashcard domain model and answer checking.|
|`data_loader.py`|Loads and validates JSON decks.|
|`quiz_strategies.py`|Defines sequential, random, and adaptive ordering.|
|`quiz_engine.py`|Conducts a session and calculates its statistics.|
|`ui.py`|Owns terminal input and output.|
|`history.py`|Validates and persists missed terms.|
|`main.py`|Parses command-line arguments and connects the components.|

### Strategy Pattern

`QuizStrategy` defines the interface used to order cards. The concrete implementations are:

* `SequentialStrategy`
* `RandomStrategy`
* `AdaptiveStrategy`

`QuizEngine` depends on the strategy interface rather than selecting an ordering algorithm itself. This allows quiz behavior to change without changing the engine.

Input and feedback are also passed to the engine as callables, keeping terminal behavior separate from quiz logic and making the engine straightforward to test.

## Testing

Run the complete test suite:

```bash
python -m pytest -q
```

Run tests with the configured statement and branch coverage report:

```bash
python -m pytest -q --cov=. --cov-report=term-missing
```

The project currently contains 68 passing tests and achieves 99.22% total coverage. The configured minimum is 81%, which exceeds the project requirement of 80%.

Run an individual test module with verbose output:

```bash
python -m pytest tests/test_quiz_engine.py -v
```

## Code Quality

Run all quality checks from the repository root:

```bash
python -m isort --check-only .
python -m black --check .
python -m flake8 .
python -m mypy . --exclude=.venv
python -m bandit -q -r . -x ./.venv,./tests
python -m pytest -q --cov=. --cov-report=term-missing
```

Formatting and linting conventions are stored in `.isort.cfg` and `.flake8`. Coverage configuration is stored in `.coveragerc`.

## Error Handling

Expected file and data problems are converted into application-specific exceptions:

* `FlashcardDataError` for deck loading and validation failures
* `HistoryDataError` for invalid history data

The command-line entry point catches actionable data and filesystem errors, prints a concise message to standard error, and returns exit status `1`. Successful sessions return exit status `0`.

## AI-Assisted Development

The application was developed iteratively with Claude Code using a test-first workflow. AI-generated suggestions were reviewed, tested, and revised before being accepted.

Supporting documentation includes:

* `prompts.md` for the substantive prompts used during development
* `docs/ai_edit_log.md` for AI interactions, review decisions, corrections, and lessons learned
* `ai_guidance/prompting_best_practices.md` for prompting guidance
* `ai_guidance/code_review_checklist.md` for systematic review guidance
* `docs/design_patterns.md` for design-pattern notes

## Development Status

The core application, all three quiz strategies, persistent history, CLI integration, automated tests, formatting, linting, type checking, and security scanning are complete.
