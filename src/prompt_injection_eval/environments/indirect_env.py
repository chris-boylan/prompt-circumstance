"""Indirect prompt injection environment — single-turn with untrusted content."""
from __future__ import annotations

from ..attacks.evaluator import evaluate_attack
from ..attacks.templates import AttackTemplate
from ..config import RunConfig
from ..defences.boundary_spotlighting import is_spotlighting_active, spotlight_input
from ..logging_utils import build_run_record
from ..models import call_model
from ..tasks.evaluator import evaluate_task
from ..tasks.schema import Task

UNTRUSTED_START = "[UNTRUSTED_CONTENT_START]"
UNTRUSTED_END = "[UNTRUSTED_CONTENT_END]"


def _inject_attack_in_untrusted_block(input_text: str, template: AttackTemplate) -> str:
    """Inject attack text inside the marked untrusted content block when possible."""
    start_idx = input_text.find(UNTRUSTED_START)
    end_idx = input_text.find(UNTRUSTED_END)
    if start_idx != -1 and end_idx != -1 and start_idx < end_idx:
        return f"{input_text[:end_idx]}\n{template.suffix}\n{input_text[end_idx:]}"
    return f"{input_text}\n\n[UNTRUSTED_INJECTION]\n{template.suffix}"


def run_benign_indirect(
    config: RunConfig, task: Task, system_prompt: str, experiment_id: str
) -> dict:
    """Execute one benign indirect trial and return a full run record."""
    input_text = (
        spotlight_input(task.input_text)
        if is_spotlighting_active(config.defence_condition)
        else task.input_text
    )
    response = call_model(config.model, system_prompt, input_text)
    task_scores = evaluate_task(task, response.raw)
    return build_run_record(
        config=config,
        task=task,
        input_text=input_text,
        raw_output=response.raw,
        task_scores=task_scores,
        attack_template=None,
        attack_scores=None,
        latency_ms=response.latency_ms,
        token_usage=response.token_usage,
        benign_or_attack="benign",
        experiment_id=experiment_id,
        model_version=response.model_version,
    )


def run_attacked_indirect(
    config: RunConfig, task: Task, template: AttackTemplate, system_prompt: str, experiment_id: str
) -> dict:
    """Execute one attacked indirect trial and return a full run record."""
    base_input = (
        spotlight_input(task.input_text)
        if is_spotlighting_active(config.defence_condition)
        else task.input_text
    )
    attacked_input = _inject_attack_in_untrusted_block(base_input, template)
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
        experiment_id=experiment_id,
        model_version=response.model_version,
    )
