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