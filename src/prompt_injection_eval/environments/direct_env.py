"""Direct prompt injection environment — single-turn, no tools, no retrieval."""
from __future__ import annotations

from ..attacks.evaluator import AttackScores, evaluate_attack
from ..attacks.generator import apply_attack
from ..attacks.templates import AttackTemplate
from ..config import RunConfig
from ..logging_utils import build_run_record
from ..models import call_model
from ..tasks.evaluator import evaluate_task
from ..tasks.schema import Task


def run_benign(config: RunConfig, task: Task, system_prompt: str) -> dict:
    """Execute one benign trial and return a full run record.

    Flow: model call -> deterministic task scoring -> log-ready record.
    """

    response = call_model(config.model, system_prompt, task.input_text)
    task_scores = evaluate_task(task, response.raw)
    return build_run_record(
        config=config,
        task=task,
        input_text=task.input_text,
        raw_output=response.raw,
        task_scores=task_scores,
        attack_template=None,
        attack_scores=None,
        latency_ms=response.latency_ms,
        token_usage=response.token_usage,
        benign_or_attack="benign",
    )


def run_attacked(
    config: RunConfig, task: Task, template: AttackTemplate, system_prompt: str
) -> dict:
    """Execute one attacked trial and return a full run record.

    Flow: apply attack overlay -> model call -> task scoring -> attack scoring -> record.
    """

    attacked_input = apply_attack(task.input_text, template)
    response = call_model(config.model, system_prompt, attacked_input)
    task_scores = evaluate_task(task, response.raw)
    attack_scores = evaluate_attack(
        template, response.raw, task_scores.task_success, config.canary_token
    )
    return build_run_record(
        config=config,
        task=task,
        input_text=attacked_input,
        raw_output=response.raw,
        task_scores=task_scores,
        attack_template=template,
        attack_scores=attack_scores,
        latency_ms=response.latency_ms,
        token_usage=response.token_usage,
        benign_or_attack="attack",
    )

