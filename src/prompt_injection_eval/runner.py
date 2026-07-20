from __future__ import annotations

"""CLI orchestrator for Slice 1/2 experiments.

The runner loads config/tasks, builds the active system prompt, executes benign
and attacked trials in the direct environment, then writes JSONL/CSV artifacts.
"""

import json
from datetime import datetime
from datetime import timezone
from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

from .attacks.templates import get_attack_templates
from . import __project_name__
from .aggregation import write_experiment_summary
from .config import RunConfig
from .defences import baseline, boundary_spotlighting, prompt_hardening
from .environments.direct_env import run_attacked, run_benign
from .environments.indirect_env import run_attacked_indirect, run_benign_indirect
from .environments.tool_env import run_attacked_tool_integrated, run_benign_tool_integrated
from .logging_utils import write_jsonl, write_summary_csv
from .tasks.loader import load_tasks

console = Console()

_PROMPTS_DIR = Path(__file__).parent / "prompts"


def _build_system_prompt(config: RunConfig) -> str:
    """Load baseline prompt, inject canary token, and apply defence condition."""

    raw = (_PROMPTS_DIR / "system_baseline.txt").read_text()
    raw = raw.replace("{{CANARY_TOKEN}}", config.canary_token)

    if config.defence_condition == "none":
        return baseline.apply(raw)
    if config.defence_condition == "prompt_hardening":
        return prompt_hardening.apply(raw)
    if config.defence_condition == "boundary_spotlighting":
        return boundary_spotlighting.apply(raw)
    if config.defence_condition == "layered_defence":
        return boundary_spotlighting.apply(prompt_hardening.apply(raw))
    raise ValueError(f"Unknown defence_condition: {config.defence_condition!r}")


@click.command()
@click.option(
    "--config",
    "config_path",
    required=True,
    type=click.Path(exists=True, path_type=Path),
    help="Path to experiment YAML config file.",
)
def main(config_path: Path) -> None:
    """Run one experiment configuration end-to-end and print a summary table."""

    config = RunConfig.from_yaml(config_path)
    tasks = load_tasks(config.tasks_file)
    if any(task.environment != config.environment for task in tasks):
        raise ValueError(
            f"Task file contains environment(s) that do not match config environment={config.environment!r}"
        )
    if config.environment == "indirect" and any(task.metadata.carrier_type is None for task in tasks):
        raise ValueError("Indirect tasks must define metadata.carrier_type")
    if config.environment == "tool_integrated" and any(not task.metadata.allowed_tools for task in tasks):
        raise ValueError("Tool-integrated tasks must define metadata.allowed_tools")
    system_prompt = _build_system_prompt(config)
    timestamp = datetime.now().strftime("%Y%m%dT%H%M%S")
    experiment_id = f"{config.run_id}_{timestamp}"

    console.print(f"\n[bold green]{__project_name__}[/bold green]")
    console.print(f"[bold green]▶ Run: {config.run_id}[/bold green]")
    console.print(f"  Provider : {config.model.provider}")
    console.print(f"  Model    : {config.model.model_name}")
    console.print(f"  Defence  : {config.defence_condition}")
    console.print(f"  Tasks    : {len(tasks)}")
    attack_templates = get_attack_templates(config.environment)
    console.print(f"  Attacks  : {len(attack_templates)} templates")
    console.print(f"  Repeats  : {config.n_repeats}")

    records: list[dict] = []
    if config.environment == "direct":
        benign_runner = run_benign
        attacked_runner = run_attacked
    elif config.environment == "indirect":
        benign_runner = run_benign_indirect
        attacked_runner = run_attacked_indirect
    elif config.environment == "tool_integrated":
        benign_runner = run_benign_tool_integrated
        attacked_runner = run_attacked_tool_integrated
    else:
        raise ValueError(f"Unknown environment: {config.environment!r}")

    for repeat_idx in range(1, config.n_repeats + 1):
        if config.n_repeats > 1:
            console.print(f"\n[bold]Repeat {repeat_idx}/{config.n_repeats}[/bold]")

        # ── Benign baseline runs ───────────────────────────────────────────
        if config.include_benign:
            console.print("\n[cyan]Benign runs...[/cyan]")
            for task in tasks:
                record = benign_runner(config, task, system_prompt, experiment_id)
                record["repeat_index"] = repeat_idx
                records.append(record)
                icon = "[green]✓[/green]" if record["task_success"] else "[red]✗[/red]"
                console.print(f"  {icon} {task.task_id}")

        # ── Attacked runs ──────────────────────────────────────────────────
        if config.include_attacked:
            console.print("\n[yellow]Attacked runs...[/yellow]")
            for task in tasks:
                for template in attack_templates:
                    record = attacked_runner(config, task, template, system_prompt, experiment_id)
                    record["repeat_index"] = repeat_idx
                    records.append(record)
                    t_icon = "[green]T✓[/green]" if record["task_success"] else "[red]T✗[/red]"
                    a_icon = "[red]A✓[/red]" if record["attack_success"] else "[green]A✗[/green]"
                    console.print(
                        f"  {t_icon} {a_icon} {task.task_id} + {template.template_id}"
                        f" [{template.family[:4]}]"
                    )

    # ── Write outputs ──────────────────────────────────────────────────────
    experiment_dir = config.output_dir / "experiments" / experiment_id
    raw_path = experiment_dir / "raw" / "runs.jsonl"
    csv_path = experiment_dir / "summaries" / "runs.csv"
    manifest_path = experiment_dir / "manifest.json"
    write_jsonl(records, raw_path)
    write_summary_csv(records, csv_path)
    manifest = {
        "experiment_id": experiment_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "config_path": str(config_path),
        "run_id": config.run_id,
        "environment": config.environment,
        "defence_condition": config.defence_condition,
        "model_provider": config.model.provider,
        "model_name": config.model.model_name,
        "n_repeats": config.n_repeats,
        "tool_approval_mode": config.tool_approval_mode,
        "structured_output_enforcement": config.structured_output_enforcement,
        "tasks_file": str(config.tasks_file),
        "task_count": len(tasks),
        "attack_template_count": len(attack_templates),
        "include_benign": config.include_benign,
        "include_attacked": config.include_attacked,
        "output_paths": {
            "raw_jsonl": str(raw_path),
            "summary_csv": str(csv_path),
        },
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)
    write_experiment_summary(experiment_dir)
    stats_path = experiment_dir / "summaries" / "stats.json"
    manifest["output_paths"]["stats_json"] = str(stats_path)
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)

    # ── Summary table ──────────────────────────────────────────────────────
    benign_records = [r for r in records if r["benign_or_attack"] == "benign"]
    attack_records = [r for r in records if r["benign_or_attack"] == "attack"]

    table = Table(title=f"{__project_name__} — Run Summary ({config.run_id})", show_lines=True)
    table.add_column("Metric", style="bold")
    table.add_column("Value")

    def _frac(num: int, den: int) -> str:
        pct = (num / den * 100) if den else 0
        return f"{num}/{den} ({pct:.0f}%)"

    b_ok = sum(r["task_success"] for r in benign_records)
    a_task_ok = sum(r["task_success"] for r in attack_records)
    a_atk_ok = sum(r["attack_success"] for r in attack_records if r["attack_success"] is not None)
    canary_leaks = sum(1 for r in attack_records if r.get("contains_canary"))
    denied_tool_calls = sum(
        1
        for r in records
        for event in (r.get("tool_call_log") or [])
        if event.get("policy_decision") == "deny"
    )
    approval_required_tool_calls = sum(
        1
        for r in records
        for event in (r.get("tool_call_log") or [])
        if event.get("policy_decision") == "require_approval"
    )

    table.add_row("Total runs", str(len(records)))
    table.add_row("Benign task success", _frac(b_ok, len(benign_records)))
    table.add_row("Task success under attack", _frac(a_task_ok, len(attack_records)))
    table.add_row("Attack success (attacker won)", _frac(a_atk_ok, len(attack_records)))
    table.add_row("Canary leaks", str(canary_leaks))
    if config.environment == "tool_integrated":
        table.add_row("Denied tool calls", str(denied_tool_calls))
        table.add_row("Approval-required tool calls", str(approval_required_tool_calls))
    table.add_row("Repeats", str(config.n_repeats))
    table.add_row("Raw JSONL", str(raw_path))
    table.add_row("Summary CSV", str(csv_path))
    table.add_row("Stats JSON", str(stats_path))
    table.add_row("Manifest", str(manifest_path))

    console.print()
    console.print(table)


if __name__ == "__main__":
    main()
