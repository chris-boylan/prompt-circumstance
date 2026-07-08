from __future__ import annotations

import json
from pathlib import Path

from .schema import Task


def load_tasks(path: Path) -> list[Task]:
    """Load tasks from JSONL by default, with safe fallbacks.

    Supported formats:
    1) JSONL (one object per line) [primary]
    2) JSON array of objects
    3) Concatenated JSON objects (pretty-printed objects back-to-back)
    """

    text = path.read_text()

    # Primary path: strict JSONL.
    tasks: list[Task] = []
    jsonl_error: Exception | None = None
    for lineno, line in enumerate(text.splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        try:
            tasks.append(Task.model_validate(json.loads(line)))
        except Exception as exc:  # pragma: no cover - exercised via fallback tests
            jsonl_error = ValueError(f"Invalid task record at line {lineno}: {exc}")
            tasks = []
            break

    if tasks:
        return tasks

    # Fallback A: full-file JSON array.
    try:
        parsed = json.loads(text)
        if isinstance(parsed, list):
            return [Task.model_validate(item) for item in parsed]
    except Exception:
        pass

    # Fallback B: concatenated JSON objects (no top-level array).
    decoder = json.JSONDecoder()
    idx = 0
    concat_tasks: list[Task] = []
    while idx < len(text):
        while idx < len(text) and text[idx].isspace():
            idx += 1
        if idx >= len(text):
            break
        try:
            obj, next_idx = decoder.raw_decode(text, idx)
        except json.JSONDecodeError as exc:
            if jsonl_error is not None:
                raise jsonl_error from exc
            raise ValueError(f"Invalid task data near character {idx}: {exc}") from exc
        concat_tasks.append(Task.model_validate(obj))
        idx = next_idx

    if concat_tasks:
        return concat_tasks

    if jsonl_error is not None:
        raise jsonl_error
    raise ValueError("No valid task records found")

