from __future__ import annotations

"""Deterministic task scoring for structured extraction/classification.

Evaluation is performed in ordered gates:
1) JSON validity
2) schema presence checks
3) enum/value checks
4) length checks
5) label correctness against ground truth

Each failed gate produces a machine-readable `failure_reason`.
"""

import json
from dataclasses import dataclass

from .schema import Task


@dataclass
class TaskScores:
    """Scoring payload for one model output against one task."""

    json_valid: bool = False
    required_fields_present: bool = False
    enum_values_valid: bool = False
    length_constraints_valid: bool = False
    category_correct: bool = False
    priority_correct: bool = False
    contains_sensitive_data_correct: bool = False
    core_labels_correct: bool = False
    task_success: bool = False
    failure_reason: str = ""
    parsed_output: dict | None = None


def evaluate_task(task: Task, raw_output: str) -> TaskScores:
    """Evaluate model output against deterministic Slice 1 task rules."""

    scores = TaskScores()

    # 1. JSON validity
    try:
        parsed = json.loads(raw_output.strip())
        if not isinstance(parsed, dict):
            raise ValueError("Response is not a JSON object")
        scores.json_valid = True
        scores.parsed_output = parsed
    except (json.JSONDecodeError, ValueError):
        scores.failure_reason = "json_parse_failed"
        return scores

    # 2. Required fields
    required = task.constraints.required_fields
    missing = [f for f in required if f not in parsed]
    if missing:
        scores.failure_reason = f"missing_fields:{','.join(missing)}"
        return scores
    scores.required_fields_present = True

    # 3. Enum validity
    allowed = task.constraints.allowed_values
    enum_errors: list[str] = []
    if "category" in parsed and parsed["category"] not in allowed.get("category", []):
        enum_errors.append(f"category={parsed['category']!r}")
    if "priority" in parsed and parsed["priority"] not in allowed.get("priority", []):
        enum_errors.append(f"priority={parsed['priority']!r}")
    if enum_errors:
        scores.failure_reason = f"invalid_enums:{','.join(enum_errors)}"
        return scores
    scores.enum_values_valid = True

    # 4. Length constraints
    action = str(parsed.get("recommended_action", ""))
    max_chars = task.constraints.max_recommended_action_chars
    if not action or len(action) > max_chars:
        scores.failure_reason = f"recommended_action_length:{len(action)}"
        return scores
    scores.length_constraints_valid = True

    # 5. Label correctness vs ground truth
    expected = task.expected_output
    scores.category_correct = parsed.get("category") == expected.category
    scores.priority_correct = parsed.get("priority") == expected.priority
    scores.contains_sensitive_data_correct = (
        parsed.get("contains_sensitive_data") == expected.contains_sensitive_data
    )
    scores.core_labels_correct = (
        scores.category_correct
        and scores.priority_correct
        and scores.contains_sensitive_data_correct
    )

    if not scores.core_labels_correct:
        wrong = []
        if not scores.category_correct:
            wrong.append(f"category(got={parsed.get('category')!r},expected={expected.category!r})")
        if not scores.priority_correct:
            wrong.append(f"priority(got={parsed.get('priority')!r},expected={expected.priority!r})")
        if not scores.contains_sensitive_data_correct:
            wrong.append(
                f"sensitive(got={parsed.get('contains_sensitive_data')},expected={expected.contains_sensitive_data})"
            )
        scores.failure_reason = "core_label_mismatch:" + ";".join(wrong)

    scores.task_success = (
        scores.json_valid
        and scores.required_fields_present
        and scores.enum_values_valid
        and scores.length_constraints_valid
        and scores.core_labels_correct
    )

    return scores

