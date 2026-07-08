from __future__ import annotations

import csv
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

from .attacks.evaluator import AttackScores
from .attacks.templates import AttackTemplate
from .config import RunConfig
from .tasks.evaluator import TaskScores
from .tasks.schema import Task


def build_run_record(
    config: RunConfig,
    task: Task,
    input_text: str,
    raw_output: str,
    task_scores: TaskScores,
    attack_template: AttackTemplate | None,
    attack_scores: AttackScores | None,
    latency_ms: float,
    token_usage: dict | None,
    benign_or_attack: str,
    experiment_id: str,
    model_version: str | None,
) -> dict:
    return {
        # ── Experiment identity ────────────────────────────────────────────
        "experiment_id": experiment_id,
        "run_id": str(uuid.uuid4()),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "environment": config.environment,
        "defence_condition": config.defence_condition,
        # ── Model provenance ──────────────────────────────────────────────
        "model_provider": config.model.provider,
        "model_name": config.model.model_name,
        "model_version": model_version,
        "temperature": config.model.temperature,
        "max_tokens": config.model.max_tokens,
        "system_prompt_version": config.system_prompt_version,
        # ── Task identity ─────────────────────────────────────────────────
        "task_id": task.task_id,
        "task_type": task.task_type,
        "objective_label": task.metadata.objective_label,
        "benign_or_attack": benign_or_attack,
        # ── Attack identity ───────────────────────────────────────────────
        "attack_family": attack_template.family if attack_template else None,
        "attack_template_id": attack_template.template_id if attack_template else None,
        "cia_impact": attack_scores.cia_impact if attack_scores else [],
        # ── Inputs / outputs ──────────────────────────────────────────────
        "input_text": input_text,
        "expected_output": task.expected_output.model_dump(),
        "raw_model_output": raw_output,
        "parsed_output": task_scores.parsed_output,
        # ── Task scoring ──────────────────────────────────────────────────
        "json_valid": task_scores.json_valid,
        "required_fields_present": task_scores.required_fields_present,
        "enum_values_valid": task_scores.enum_values_valid,
        "length_constraints_valid": task_scores.length_constraints_valid,
        "category_correct": task_scores.category_correct,
        "priority_correct": task_scores.priority_correct,
        "contains_sensitive_data_correct": task_scores.contains_sensitive_data_correct,
        "core_labels_correct": task_scores.core_labels_correct,
        "task_success": task_scores.task_success,
        # ── Attack scoring ────────────────────────────────────────────────
        "attack_success": attack_scores.attack_success if attack_scores else None,
        "contains_canary": attack_scores.contains_canary if attack_scores else None,
        # ── Diagnostics ───────────────────────────────────────────────────
        "task_failure_reason": task_scores.failure_reason,
        "attack_failure_reason": (
            attack_scores.attack_failure_reason if attack_scores else None
        ),
        "latency_ms": round(latency_ms, 2),
        "token_usage": token_usage,
    }


def write_jsonl(records: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        for record in records:
            f.write(json.dumps(record) + "\n")


def write_summary_csv(records: list[dict], path: Path) -> None:
    if not records:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "experiment_id",
        "run_id",
        "task_id",
        "objective_label",
        "benign_or_attack",
        "attack_family",
        "attack_template_id",
        "cia_impact",
        "defence_condition",
        "model_provider",
        "model_name",
        "model_version",
        "task_success",
        "attack_success",
        "json_valid",
        "core_labels_correct",
        "contains_canary",
        "task_failure_reason",
        "attack_failure_reason",
        "latency_ms",
    ]
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for record in records:
            row = dict(record)
            row["cia_impact"] = "|".join(row.get("cia_impact") or [])
            writer.writerow(row)
