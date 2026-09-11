# AI-Assisted Development Project Report

**Student Name:** Ashwin Parthasarathy  
**Project Title:** Flashcard Quizzer: AI-Assisted CLI Learning Application  
**Date:** September 11, 2026

## Executive Summary

I built Flashcard Quizzer, a Python command-line application that helps learners study terms and definitions stored in JSON files. The application presents each card, accepts an answer, compares it without regard to capitalization or surrounding whitespace, displays immediate feedback, and prints a summary containing the number of questions, correct answers, percentage accuracy, and missed terms. It supports sequential, random, and adaptive quiz modes. Adaptive mode uses persistent history to prioritize terms missed in the previous session.

The project was developed incrementally with Claude Code using test-driven development. I divided the work into small components, asked Claude Code to generate tests before implementation, confirmed that new tests failed for the expected reason, and then requested the smallest production change needed to make them pass. I reviewed the generated tests and code rather than accepting them automatically. That review uncovered missing negative cases, incomplete structural boundaries, weak output assertions, formatting conflicts, and one manually introduced f-string error. The final application has 68 relevant tests, 99.22% production branch coverage, and passes Black, isort, flake8, mypy, and Bandit checks.

## Project Overview

### Problem Statement

Flashcards are simple, but a useful quiz application needs more than displaying a list. It must load user-supplied data safely, judge answers consistently, vary question order, report progress, and remember difficult terms without corrupting or silently discarding learner data. The application also needs to remain easy to test even though it interacts with the terminal.

### Solution Approach

I separated the application into modules with one primary responsibility each. `Flashcard` represents a card and owns answer comparison. `data_loader.py` parses and validates deck files. `quiz_strategies.py` decides card order. `quiz_engine.py` manages the session and statistics without performing terminal input or output. `ui.py` owns presentation, while `history.py` stores missed terms. `main.py` parses arguments and connects these components.

The central architectural choice was the Strategy pattern. `QuizStrategy` defines the ordering interface, and `SequentialStrategy`, `RandomStrategy`, and `AdaptiveStrategy` implement distinct algorithms. The engine depends only on that interface, so adding or selecting a strategy does not require changing quiz logic. Answer and feedback functions are also injected into the engine. This keeps the domain logic independent of `input()` and `print()` and makes complete sessions testable with lightweight fakes.

The implementation uses Python 3.10 and the standard library at runtime. Development tools include pytest, pytest-cov, Black, isort, flake8, mypy, and Bandit.

### Final Features

- JSON deck loading with UTF-8 support and order preservation
- Validation of top-level structure, card objects, required fields, and string values
- Custom `FlashcardDataError` and `HistoryDataError` exceptions
- Case-insensitive, whitespace-tolerant answer checking
- Sequential, seeded random, and adaptive ordering
- Immediate correct or incorrect feedback
- Session totals, two-decimal accuracy, and missed-term reporting
- Persistent JSON history with automatic parent-directory creation
- Graceful command-line errors, explicit exit codes, and no user-facing traceback
- A sample server-acronym deck and comprehensive automated tests

## AI Collaboration Experience

### AI Tools Used

I used Claude Code as the AI coding assistant. Its role was to propose tests and implementations within constraints I defined. I remained responsible for scope, review, execution, correction, and acceptance.

### Collaboration Workflow

My typical workflow followed a red-green-review cycle. I described one small behavior, named the files Claude Code could modify, and explicitly prohibited unrelated production changes. I reviewed the generated tests for missing boundaries before running them. A failure caused by a missing module or behavior confirmed the red stage. I then requested the minimum implementation, ran focused tests, and followed with the complete suite and quality tools. If a test or tool exposed a weakness, I corrected the prompt, test, code, or project configuration and documented the decision in `docs/ai_edit_log.md`.

My prompts improved over time. Later requests explicitly covered mutation guarantees, stable ordering, exception messages, empty collections, deterministic randomness, allowed files, type signatures, and verification commands. I also batched closely related work, such as random and adaptive strategies, to reduce token usage without combining unrelated responsibilities.

### Most Valuable AI Interactions

#### Example 1: Strengthening the Flashcard Contract

Claude Code initially generated three useful Flashcard tests, but all described correct answers. I recognized that an implementation returning `True` for every input could pass. I requested and retained a negative test proving that an unrelated answer returns `False`. This established early that generated tests must themselves be reviewed for false-positive implementations.

#### Example 2: Defensive JSON Validation

Claude Code generated parameterized cases for malformed deck structures and proposed a `_parse_card` helper. I noticed that it had not tested a list containing a non-object value, even though it tested the top-level type and card fields. I added that boundary. The final loader translates raw parsing and structure failures into helpful application-specific errors that identify the relevant card or field.

#### Example 3: Strategy and Engine Design

Claude Code helped implement the shared strategy abstraction and the quiz engine. I added a test proving that `QuizStrategy` is actually abstract rather than merely a parent class. For the engine, generated test doubles recorded question and feedback events, proving that feedback occurs before the next question. The resulting dependency-injection design supports different orderings while keeping interactive behavior outside the engine.

#### Example 4: UI Failure Caught by Tests

After Claude Code generated the UI, I strengthened assertions to associate values with labels and manually added visible table separators. During that edit, I omitted an f-string prefix, causing the literal expression `{stats.accuracy:.2f}` to appear. The UI test failed immediately. I fixed the prefix and reran the complete suite. This demonstrated that tests protect manual changes as well as AI-generated code.

### Challenges with AI Collaboration

Claude Code generally produced clear primary-path implementations, but generated tests sometimes omitted one negative or boundary case. I therefore looked for invalid types, missing keys, empty collections, mutation, weak assertions, and failure-message quality during every review. Another challenge was tool disagreement: Black originally accepted lines that flake8 rejected. Rather than repeatedly hand-formatting individual lines, I added project configuration so Black, isort, and flake8 consistently use compatible rules.

Token limits also encouraged more deliberate collaboration. I stopped using AI for trivial terminal commands and combined only strongly related requirements. This made prompts more efficient while preserving small reviewable commits.

## Software Engineering Practices

### Code Quality Measures

All public behavior is type annotated and documented with concise docstrings. Custom exceptions separate expected data problems from programming errors, and translated exceptions retain their original context. Collection inputs use abstractions such as `Sequence` and `Collection`, while strategies return new lists to prevent unexpected mutation.

The final quality gate passes `isort --check-only`, `black --check`, flake8, mypy, Bandit, and pytest with branch coverage. The repository contains 514 physical lines across production Python files and 32 class or function definitions. Coverage configuration excludes tests and requires at least 81%, slightly above the rubric threshold. The measured production branch coverage is 99.22%; the only uncovered line is the executable script guard in `main.py`.

Git commits were organized around meaningful milestones: the model, loader, validation, strategies, engine, UI, history, CLI integration, starter cleanup, quality configuration, and documentation. Generated history, virtual environments, caches, and coverage artifacts are ignored.

## Conclusion

The project met its functional and engineering goals while providing a practical lesson in AI-assisted development. Claude Code accelerated scaffolding and repetitive implementation, but the strongest improvements came from human review: identifying missing negative cases, strengthening assertions, resolving tool conflicts, and verifying complete user workflows. The most important lesson is that AI can generate code quickly, but responsibility for the behavioral contract and evidence of correctness remains with the developer.

## Appendix A: AI Collaboration Evidence

`docs/ai_edit_log.md` contains nine detailed feature interactions, including the prompt context, AI response, modifications, personal decisions, outcomes, and lessons learned. `prompts.md` records 12 substantive prompts used during development.

## Appendix B: Code Statistics

- Production Python files: 8, including the model package initializer
- Production physical lines: 514
- Class and function definitions: 32
- Relevant automated tests: 68
- Production branch coverage: 99.22%
- Required coverage threshold: 81%
- Formatting, import sorting, linting, typing, and security checks: Passed

## Appendix C: Additional Resources

- `README.md` for setup, usage, architecture, and quality commands
- `ai_guidance/prompting_best_practices.md` for prompt construction guidance
- `ai_guidance/code_review_checklist.md` for systematic review
- `docs/design_patterns.md` for design-pattern reference
- Python, pytest, pytest-cov, Black, isort, flake8, mypy, and Bandit documentation