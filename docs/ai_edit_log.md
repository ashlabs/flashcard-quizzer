# AI Edit Log

This log documents the substantive interactions with Claude Code during development of the Flashcard Quizzer. Each entry records the context, request, generated response, personal review, changes made, outcome, and lesson learned.

### 2026-09-10 - Flashcard Model Tests and Review

**Context:** I needed to define the basic behavior of a flashcard before implementing the production model. I used a test-driven development approach so the tests would establish the expected interface and answer-comparison behavior.

**AI Tool Used:** Claude Code

**Prompt/Request:** I asked Claude Code to create only `tests/test_flashcard.py` for a `Flashcard` model with `front` and `back` fields and case-insensitive answer checking. I specifically requested that it not create or modify production code.

**AI Response:** Claude Code created three tests covering storage of the front and back text, case-insensitive matching, and matching after removing surrounding whitespace.

**Changes Made:** During review, I identified that the generated tests only covered correct answers. I requested an additional test named `test_is_correct_rejects_incorrect_answer` to verify that an unrelated answer returns `False`. I also shortened an overly long generated test name after `flake8` reported an E501 line-length violation.

**Reasoning:** Without a negative test, an incorrect implementation that always returned `True` could pass the entire generated test suite. Adding the negative case made the behavioral contract more complete.

**Outcome:** The tests initially failed with `ModuleNotFoundError` because the production model did not exist, confirming the expected red stage of test-driven development. Claude Code then created `models/__init__.py` and `models/flashcard.py`. All four flashcard tests passed, the complete suite passed with 19 tests, and total coverage reached 90%.

**Lessons Learned:** AI-generated tests still require careful review. Positive test cases alone do not prove that incorrect input is rejected. Writing and reviewing tests before implementation helped expose this gap before production code was added.

---
### 2026-09-10 - Basic JSON Flashcard Loader

**Context:** I needed to load flashcards from a JSON file. I began with only the successful case so that file and structure validation could be introduced separately in later iterations.

**AI Tool Used:** Claude Code

**Prompt/Request:** I first asked Claude Code to create a test that loaded a valid JSON file containing flashcard objects. After confirming that the test failed because `data_loader.py` did not exist, I asked Claude Code to implement only the minimum loader needed to pass that test.

**AI Response:** Claude Code created a test using pytest's `tmp_path` fixture and generated a `load_flashcards` function. The function opens a file using UTF-8, parses it with `json.load()`, and converts each item into a `Flashcard` object while preserving its position.

**Changes Made:** I did not modify the generated implementation because it was simple, correctly scoped, and met the requirements for this iteration. I intentionally deferred validation and custom error handling.

**Reasoning:** Implementing only the successful path made the basic data flow easy to understand and test. Missing-file, malformed-JSON, and structure-validation behavior will be added through separate failing tests instead of being introduced all at once.

**Outcome:** The loader test passed, all 20 project tests passed, and total coverage reached 91%. Black, flake8, and mypy also completed successfully.

**Lessons Learned:** A narrow prompt can keep AI-generated code focused and prevent complexity early in the development cycle. TDD also makes it clear which behaviors are implemented and which remain unsupported.

---

### 2026-09-10 - JSON Structure Validation

**Context:** The loader could read valid JSON and handle missing or malformed files, but it did not validate the structure of the parsed data. Invalid data produced internal Python exceptions or created unusable flashcards.

**AI Tool Used:** Claude Code

**Prompt/Request:** I asked Claude Code to generate parameterized tests for invalid JSON structures, including an incorrect top-level type, missing fields, non-string values, and an empty deck. After reviewing the tests, I asked Claude Code to implement straightforward validation in `data_loader.py`.

**AI Response:** Claude Code generated parameterized validation tests and implemented a `_parse_card` helper. The helper verifies that each card is an object, contains the required fields, and uses string values. The loader also verifies that the top-level JSON value is a list.

**Changes Made:** During review, I noticed that the generated tests did not cover a list containing a non-object value, so I added that case. I also corrected a docstring typo. After implementation, I manually adjusted several long lines because Black's default 88-character limit conflicted with flake8's 79-character limit. I replaced a long list comprehension with a clear loop.

**Reasoning:** Validating each list item prevents raw `TypeError` and `KeyError` exceptions from reaching users. The additional test ensures every level of the JSON structure is checked. The explicit loop improves readability and satisfies the project's style requirements.

**Outcome:** All loader tests passed. Invalid structures now raise `FlashcardDataError` with helpful messages that identify the affected card or field. Black, flake8, mypy, and the full test suite passed.

**Lessons Learned:** Parameterization reduces duplicated test code, but AI-generated test cases still require review for missing structural boundaries. Automated formatting and linting tools can also disagree, so passing one tool does not guarantee compliance with another.

---

### 2026-09-10 - Sequential Quiz Strategy

**Context:** The application requires sequential, random, and adaptive quiz modes. I needed a shared interface that would allow the quiz engine to use any ordering algorithm without containing mode-specific logic.

**AI Tool Used:** Claude Code

**Prompt/Request:** I asked Claude Code to generate tests for an abstract `QuizStrategy` and a concrete `SequentialStrategy`. After reviewing the tests, I asked it to implement only the abstract interface and sequential behavior.

**AI Response:** Claude Code created tests for inheritance, order preservation, returning a new list, avoiding mutation, and handling an empty deck. It then implemented `QuizStrategy` with an abstract `order_cards` method and implemented `SequentialStrategy` using `list(cards)`.

**Changes Made:** During test review, I noticed that checking `isinstance(strategy, QuizStrategy)` proved inheritance but did not prove that `QuizStrategy` was abstract. I manually added a test using `inspect.isabstract()`.

**Reasoning:** The abstractness test verifies an important part of the design pattern rather than only its class hierarchy. Returning a new list also prevents a strategy from unexpectedly changing the caller's deck.

**Outcome:** All six strategy tests passed. The complete project suite passed with 35 tests and 94% coverage. Black, flake8, and mypy also passed.

**Lessons Learned:** Inheritance alone does not establish an abstract contract. Tests for design patterns should verify the design behavior that matters, not merely class names or relationships.

---

### 2026-09-10 - Random and Adaptive Quiz Strategies

**Context:** After establishing the Strategy Pattern with sequential ordering, I needed to implement random ordering and adaptive ordering that prioritizes previously missed cards.

**AI Tool Used:** Claude Code

**Prompt/Request:** I asked Claude Code to generate tests for both strategies in one request. The random tests covered reproducible seeded shuffling, card preservation, input immutability, and empty decks. The adaptive tests covered missed-card priority, normalized matching, stable group order, unknown terms, input immutability, and empty decks. I then requested both implementations in one focused prompt.

**AI Response:** Claude Code implemented `RandomStrategy` using a dedicated `random.Random` instance and implemented `AdaptiveStrategy` using normalized missed-front values. It separated missed and remaining cards into two lists to preserve their relative order.

**Changes Made:** During review, I updated an outdated module docstring and separated standard-library and third-party imports. I also shortened two generated test names after flake8 found line-length violations. The production implementation was accepted without logical changes.

**Reasoning:** A dedicated random-number generator makes seeded tests deterministic without modifying global random state. Normalizing missed terms with `strip()` and `casefold()` makes adaptive matching consistent with answer checking. Stable grouping makes the adaptive order predictable.

**Outcome:** All 19 strategy tests passed. The complete project suite passed with 48 tests and 95% coverage. Black, flake8, and mypy passed after the test-name corrections.

**Lessons Learned:** Closely related functionality can be generated and reviewed in one interaction without losing test-driven development discipline. Dependency isolation and deterministic behavior make randomized code easier to test reliably.

---

### 2026-09-10 - Quiz Engine and Session Statistics

**Context:** I needed to connect flashcards and ordering strategies into a quiz workflow while keeping terminal input and output separate from the application logic.

**AI Tool Used:** Claude Code

**Prompt/Request:** I asked Claude Code to create tests for a `QuizEngine` that accepts an ordering strategy, an answer provider, and a feedback provider. The tests also defined a `SessionStats` result containing totals, accuracy, and missed terms. After reviewing the tests, I requested the minimal production implementation.

**AI Response:** Claude Code generated a `RecordingSession` test double and a reverse-order strategy for testing dependency injection. It implemented `SessionStats` as a dataclass and implemented `QuizEngine.run()` to order cards, request answers, provide immediate feedback, and collect results.

**Changes Made:** I accepted the generated tests and implementation without logical changes because they were focused, testable, and consistent with the planned architecture.

**Reasoning:** Injecting input and feedback callables keeps the engine independent of `input()` and `print()`. This separation allows the same engine to support a terminal interface now and another interface later. A `default_factory` for missed terms avoids shared mutable state between sessions.

**Outcome:** All seven quiz-engine tests passed. The complete project suite passed with 55 tests and 96% coverage. Black, flake8, and mypy also passed.

**Lessons Learned:** Separating orchestration from input and output makes interactive code straightforward to test. Small dependency-injection boundaries can improve flexibility without requiring a framework or complex mocking.

---

### 2026-09-10 - Terminal UI and Summary Display

**Context:** The quiz engine needed terminal-specific functions for collecting answers, displaying immediate feedback, and presenting session statistics without adding input and output logic to the engine.

**AI Tool Used:** Claude Code

**Prompt/Request:** I asked Claude Code to generate tests for answer prompting, correct and incorrect feedback, summary metrics, missed terms, and perfect sessions. I then asked it to implement `prompt_for_answer`, `show_feedback`, and `show_summary` in a separate `ui.py` module.

**AI Response:** Claude Code generated tests using pytest's `monkeypatch` and `capsys` features. It implemented terminal input and output functions and formatted the session statistics using aligned labels.

**Changes Made:** During review, I strengthened the summary test to verify the `Total Questions` and `Accuracy` labels rather than checking only numeric text. I also added visible column separators so the metrics were clearly presented as a two-column table. During that manual refinement, I accidentally omitted an f-string prefix from the accuracy value.

**Reasoning:** Label assertions prove that values are associated with the correct metrics. Column separators make the required summary table clearer. The failed test exposed the missing f-string prefix because the expression was printed literally instead of being evaluated.

**Outcome:** I corrected the f-string, and all 9 UI tests passed. The complete suite passed with 64 tests and 96% coverage. Black, flake8, and mypy also passed.

**Lessons Learned:** Tests protect manual refinements as well as AI-generated code. A small formatting change can introduce a real defect, and output-focused tests can detect it before integration.

---

### 2026-09-10 - Persistent Missed-Term History

**Context:** Adaptive mode needed a way to remember terms missed in the previous quiz session. A first-time user also needed to start normally without an existing history file.

**AI Tool Used:** Claude Code

**Prompt/Request:** I asked Claude Code to generate tests for loading, validating, saving, and creating directories for a JSON history file. I then asked it to implement `HistoryDataError`, `load_missed_terms`, and `save_missed_terms`.

**AI Response:** Claude Code generated parameterized tests for invalid history structures and implemented a JSON-backed history module. Missing files return an empty list, while malformed or structurally invalid files raise application-specific errors.

**Changes Made:** During review, I strengthened the parameterized tests to verify helpful error-message content instead of checking only the exception type. I also refactored a long validation expression and error message so both Black and flake8 accepted the code.

**Reasoning:** Checking message content prevents an empty or generic exception from passing the tests. Returning an empty list for a missing file supports first-time users, while rejecting malformed existing data avoids silently losing history.

**Outcome:** All 9 history tests passed. The complete project suite passed with 73 tests and 97% coverage. Black, flake8, and mypy passed.

**Lessons Learned:** Persistence code needs separate treatment for absent data and corrupted data. A missing file can represent a valid initial state, while an existing invalid file should be reported clearly.

---

### 2026-09-11 - Complete CLI Integration

**Context:** The individual project modules were complete but had not yet been connected into a runnable command-line application. The original `main.py` still demonstrated the starter task manager.

**AI Tool Used:** Claude Code

**Prompt/Request:** I asked Claude Code to generate integration tests for strategy selection, complete quiz sessions, adaptive history, invalid decks, empty decks, and malformed history. I then asked it to replace the starter entry point with an argparse-based Flashcard Quizzer CLI.

**AI Response:** Claude Code generated tests that invoked `main()` with argument lists and scripted terminal input. It implemented command-line parsing, strategy construction, quiz orchestration, history loading and saving, summary display, explicit exit codes, and graceful error reporting.

**Changes Made:** During review, I strengthened the shared error assertion to require an `Error:` prefix. I also added an assertion proving that a previously missed term is removed from history after it is answered correctly in adaptive mode. The generated production implementation was accepted without logical changes.

**Reasoning:** Verifying only a nonempty error message would allow unclear output to pass. Checking that mastered terms leave history proves that adaptive mode reflects the latest learning state rather than permanently prioritizing every past mistake.

**Outcome:** All 10 CLI tests passed. Manual tests confirmed sequential ordering, seeded random ordering, adaptive prioritization across sessions, case-insensitive answers, summary output, history updates, and missing-file handling without a traceback. The complete automated suite passed with 83 tests.

**Lessons Learned:** Integration tests expose whether independently correct components work together. Directly passing argument lists and scripted input made the complete CLI testable without starting subprocesses.

---

## Reflection

### What types of tasks did AI help with most effectively?

Claude Code was most effective when given a narrow behavioral contract and a limited set of files. It quickly generated test scaffolding, simple production implementations, type annotations, docstrings, fixtures, parameterized cases, and test doubles. It was particularly useful for repetitive but structured work such as validating JSON fields and testing multiple implementations of the same strategy interface.

### Where did AI suggestions require modification?

The most frequent changes involved strengthening tests and aligning generated code with project quality requirements. I added negative answer checking, a non-object card case, verification that the strategy base class is abstract, stronger output-label assertions, specific error-message checks, and proof that mastered terms are removed from adaptive history. I also corrected long lines, outdated documentation, import ordering, and a manually introduced f-string error.

### What patterns appeared in the AI's strengths and weaknesses?

The AI performed well when requirements were explicit, bounded, and supported by existing tests. It produced clear modular designs and generally respected requests not to modify unrelated files. Its main weakness was incomplete boundary coverage: generated tests often captured the primary successful behavior but omitted one important negative case or structural boundary. Generated formatting could also satisfy Black while conflicting with flake8 until the tools were configured consistently.

### How did the prompting approach improve?

The early prompts described only the immediate feature. Later prompts became more precise about allowed files, test-first ordering, mutation guarantees, edge cases, error messages, type signatures, and verification commands. Related behavior was batched when it shared one abstraction, while unrelated work remained separate. This reduced unnecessary output and made each response easier to review.

### What would I do differently in a future project?

I would configure Black, isort, flake8, mypy, Bandit, and coverage before implementing the first feature. I would also define a reusable checklist for negative cases, collection boundaries, mutation, and error messages. Finally, I would record quantitative AI contribution metrics during each commit rather than trying to reconstruct line counts at the end.

## Summary Statistics

- **Documented feature interactions:** 9
- **Prompt records:** 12 substantive prompts in `prompts.md`
- **Final relevant test count:** 68
- **Final production branch coverage:** 99.22%
- **Required coverage threshold:** 81%
- **AI-generated lines retained or modified:** Not tracked reliably at line level; all retained code was reviewed, tested, and committed incrementally
- **Most helpful interaction:** Designing the quiz engine around an injected strategy and input/output callables
- **Most challenging interaction:** Expanding validation and output tests to cover omitted boundary cases while satisfying multiple code-quality tools
- **Biggest lesson learned:** AI accelerates implementation, but test quality, boundary analysis, and final engineering judgment remain the developer's responsibility