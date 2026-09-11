# AI Edit Log

**Instructions:** Use this document to track all your interactions with AI assistants during the project. This log will help you reflect on your AI collaboration process and demonstrate your learning journey.

## How to Use This Log

For each AI interaction, create a new entry with the following structure:

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


### Entry Template
```
## [Date] - [Brief Description]

**Context:** What were you trying to accomplish?
**AI Tool Used:** Claude/ChatGPT/Copilot/etc.
**Prompt/Request:** What exactly did you ask the AI?
**AI Response:** Summary of what the AI generated (don't copy entire code blocks)
**Changes Made:** What modifications did you make to the AI's suggestions?
**Reasoning:** Why did you make those changes?
**Outcome:** What was the final result?
**Lessons Learned:** What did you learn from this interaction?
```

---

## Example Entry

### 2024-01-15 - Initial Task Manager Implementation

**Context:** I needed to create a basic task management system to demonstrate CRUD operations and serve as the foundation for the project.

**AI Tool Used:** Claude

**Prompt/Request:** "Help me create a Python class for managing tasks with basic CRUD operations. The class should handle task creation, retrieval, completion, and deletion. Include proper error handling and type hints."

**AI Response:** Claude generated a TaskManager class with methods for add_task, get_task, get_all_tasks, complete_task, delete_task, and to_dict. The code included type hints, proper error handling with ValueError for missing tasks, and used datetime for timestamps.

**Changes Made:** 
- Added priority field to tasks with a default value of "medium"
- Modified the task structure to include created_at timestamp
- Added validation for priority values
- Renamed some variable names for clarity

**Reasoning:** 
- Priority field will be useful for implementing sorting features later
- Timestamps help with task organization and analytics
- Input validation prevents invalid data from being stored
- Better variable names improve code readability

**Outcome:** Successfully created a robust TaskManager class that serves as the core of the application with room for future enhancements.

**Lessons Learned:** 
- AI provides good starting implementations but always needs customization
- It's important to think about future requirements when reviewing AI code
- Type hints and error handling are crucial for maintainable code

---

## Your Log Entries

### [Date] - [Brief Description]

**Context:** 

**AI Tool Used:** 

**Prompt/Request:** 

**AI Response:** 

**Changes Made:** 

**Reasoning:** 

**Outcome:** 

**Lessons Learned:** 

---

### [Date] - [Brief Description]

**Context:** 

**AI Tool Used:** 

**Prompt/Request:** 

**AI Response:** 

**Changes Made:** 

**Reasoning:** 

**Outcome:** 

**Lessons Learned:** 

---

## Tips for Effective AI Collaboration

### 1. Be Specific in Your Requests
- ❌ "Write a function"
- ✅ "Write a function that validates email addresses using regex, returns a boolean, and includes proper error handling"

### 2. Provide Context
- Include relevant code snippets
- Explain the larger goal
- Mention any constraints or requirements

### 3. Review and Understand
- Never copy AI code without understanding it
- Ask for explanations of complex logic
- Test the code before accepting it

### 4. Iterate and Refine
- Use follow-up questions to improve the code
- Ask for alternative implementations
- Request code reviews and suggestions

### 5. Document Your Process
- Keep detailed notes in this log
- Explain your decision-making process
- Track what works and what doesn't

## Common AI Collaboration Patterns

### Code Generation
- Initial implementation of classes/functions
- Boilerplate code creation
- Test case generation

### Code Review
- Ask AI to review your code for issues
- Request suggestions for improvements
- Get feedback on code structure

### Problem Solving
- Debugging help
- Algorithm suggestions
- Architecture advice

### Learning and Explanation
- Ask for explanations of complex concepts
- Request examples of design patterns
- Get guidance on best practices

## Reflection Questions

As you work through the project, consider these questions:

1. **What types of tasks did AI help with most effectively?**
2. **Where did you need to make the most modifications to AI suggestions?**
3. **What patterns did you notice in AI strengths and weaknesses?**
4. **How did your prompting technique improve over time?**
5. **What would you do differently in future AI collaborations?**

## Summary Statistics

At the end of your project, fill out these statistics:

- **Total AI interactions:** ___
- **Lines of AI-generated code used:** ___
- **Lines of AI-generated code modified:** ___
- **Most helpful AI interaction:** ___
- **Most challenging AI interaction:** ___
- **Biggest lesson learned:** ___

---

**Note:** This log is a required component of your final project report. Be thorough and honest in your documentation to demonstrate your learning process and AI collaboration skills.