from __future__ import annotations

import json
from pathlib import Path

from .schema import Task


def load_tasks(path: Path) -> list[Task]:
    tasks: list[Task] = []
    with open(path) as f:
        for lineno, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                tasks.append(Task.model_validate(json.loads(line)))
            except Exception as exc:
                raise ValueError(f"Invalid task record at line {lineno}: {exc}") from exc
    return tasks

