# Test Coverage and Code Quality Report

**Project:** Flashcard Quizzer
**Verification date:** September 11, 2026
**Python version:** 3.10.14

## Test Results

The final test suite was executed with:

```bash
python -m pytest -q --cov=. --cov-report=term-missing
```

Result:

```text
68 passed
Required test coverage of 81.0% reached.
Total.22%
```

## Production Coverage

| Module                | Statements | Missed | Branches | Partial branches |   Coverage |
| --------------------- | ---------: | -----: | -------: | ---------------: | ---------: |
| `data_loader.py`      |         32 |      0 |       12 |                0 |       100% |
| `history.py`          |         35 |      0 |       10 |                0 |       100% |
| `main.py`             |         52 |      1 |       12 |                1 |        97% |
| `models/__init__.py`  |          0 |      0 |        0 |                0 |       100% |
| `models/flashcard.py` |          7 |      0 |        0 |                0 |       100% |
| `quiz_engine.py`      |         27 |      0 |        6 |                0 |       100% |
| `quiz_strategies.py`  |         30 |      0 |        4 |                0 |       100% |
| `ui.py`               |         23 |      0 |        6 |                0 |       100% |
| **Total**             |    **206** |  **1** |   **50** |            **1** | **99.22%** |

Tests and virtual-environment files are excluded from the reported source coverage. Branch coverage is enabled, and `.coveragerc` enforces a minimum of 81%, exceeding the project requirement of greater than 80%.

The only uncovered production line is the executable script guard in `main.py`. The `main()` function and its successful and failed outcomes are tested directly.

## Code Quality Verification

The following checks completed successfully:

| Tool   | Command                                                 | Result                         |
| ------ | ------------------------------------------------------- | ------------------------------ |
| isort  | `python -m isort --check-only .`                        | Passed                         |
| Black  | `python -m black --check .`                             | Passed                         |
| flake8 | `python -m flake8 .`                                    | Passed with no violations      |
| mypy   | `python -m mypy . --exclude=.venv`                      | Passed with no type errors     |
| Bandit | `python -m bandit -q -r . -x ./.venv,./tests`           | Passed with no reported issues |
| pytest | `python -m pytest -q --cov=. --cov-report=term-missing` | 68 tests passed                |

`RandomStrategy` uses `random.Random` only to shuffle study cards. The line has a narrow Bandit `B311` suppression because the operation is intentionally non-cryptographic and is not used for secrets, authentication, or security decisions.
