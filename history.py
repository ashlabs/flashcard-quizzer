"""
Storage of the terms a learner has missed in past sessions.

The history file is a small JSON object shaped as
``{"missed_terms": [...]}``. A learner who has never been quizzed simply
has no file yet, which is a clean slate rather than an error; a file that
exists but cannot be read is reported instead of being discarded.
"""

import json
from collections.abc import Collection
from pathlib import Path
from typing import Any

MISSED_TERMS_KEY = "missed_terms"


class HistoryDataError(Exception):
    """Raised when a history file cannot be read."""


def _parse_missed_terms(data: Any, path: Path) -> list[str]:
    """Pull the missed terms out of a parsed history document.

    Raises:
        HistoryDataError: If the document is not an object, lacks the
            missed terms field, or holds anything but a list of strings.
    """
    if not isinstance(data, dict):
        raise HistoryDataError(f"History file must contain an object: {path}")
    if MISSED_TERMS_KEY not in data:
        message = f'History file is missing "{MISSED_TERMS_KEY}": {path}'
        raise HistoryDataError(message)

    terms = data[MISSED_TERMS_KEY]
    if not isinstance(terms, list):
        message = f'History "{MISSED_TERMS_KEY}" must be a list: {path}'
        raise HistoryDataError(message)
    terms_are_strings = all(isinstance(term, str) for term in terms)
    if not terms_are_strings:
        message = f'History "{MISSED_TERMS_KEY}" must contain only ' f"strings: {path}"
        raise HistoryDataError(message)
    return list(terms)


def load_missed_terms(file_path: str | Path) -> list[str]:
    """Return the terms missed in earlier sessions, oldest first.

    A history file that does not exist yet yields an empty list.

    Raises:
        HistoryDataError: If an existing file is not valid JSON or does
            not hold a list of missed terms.
    """
    path = Path(file_path)
    if not path.exists():
        return []

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise HistoryDataError(f"Invalid history JSON: {path}") from exc

    return _parse_missed_terms(data, path)


def save_missed_terms(
    file_path: str | Path,
    missed_terms: Collection[str],
) -> None:
    """Write the missed terms to a history file, creating its folder.

    The terms are stored in the order the collection yields them.
    """
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    document = {MISSED_TERMS_KEY: list(missed_terms)}
    path.write_text(
        json.dumps(document, indent=2),
        encoding="utf-8",
    )
