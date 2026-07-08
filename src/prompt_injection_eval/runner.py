from __future__ import annotations

"""CLI orchestrator for Slice 1/2 experiments.

The runner loads config/tasks, builds the active system prompt, executes benign
and attacked trials in the direct environment, then writes JSONL/CSV artifacts.
"""

from datetime import datetime
from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

from .attacks.templates import ATTACK_TEMPLATES
from . import __project_name__
from .config import RunConfig
from .defences import baseline, prompt_hardening
from .environments.direct_env import run_attacked, run_benign
from .environments.indirect_env import run_attacked_indirect, run_benign_indirect
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
    system_prompt = _build_system_prompt(config)
    timestamp = datetime.now().strftime("%Y%m%dT%H%M%S")
    experiment_id = f"{config.run_id}_{timestamp}"

    console.print(f"\n[bold green]{__project_name__}[/bold green]")
    console.print(f"[bold green]▶ Run: {config.run_id}[/bold green]")
    console.print(f"  Provider : {config.model.provider}")
    console.print(f"  Model    : {config.model.model_name}")
    console.print(f"  Defence  : {config.defence_condition}")
    console.print(f"  Tasks    : {len(tasks)}")
    console.print(f"  Attacks  : {len(ATTACK_TEMPLATES)} templates")

    records: list[dict] = []
    benign_runner = run_benign if config.environment == "direct" else run_benign_indirect
    attacked_runner = run_attacked if config.environment == "direct" else run_attacked_indirect

    # ── Benign baseline runs ───────────────────────────────────────────────
    if config.include_benign:
        console.print("\n[cyan]Benign runs...[/cyan]")
        for task in tasks:
            record = benign_runner(config, task, system_prompt, experiment_id)
            records.append(record)
            icon = "[green]✓[/green]" if record["task_success"] else "[red]✗[/red]"
            console.print(f"  {icon} {task.task_id}")

    # ── Attacked runs ──────────────────────────────────────────────────────
    if config.include_attacked:
        console.print("\n[yellow]Attacked runs...[/yellow]")
        for task in tasks:
            for template in ATTACK_TEMPLATES:
                record = attacked_runner(config, task, template, system_prompt, experiment_id)
                records.append(record)
                t_icon = "[green]T✓[/green]" if record["task_success"] else "[red]T✗[/red]"
                a_icon = "[red]A✓[/red]" if record["attack_success"] else "[green]A✗[/green]"
                console.print(
                    f"  {t_icon} {a_icon} {task.task_id} + {template.template_id}"
                    f" [{template.family[:4]}]"
                )

    # ── Write outputs ──────────────────────────────────────────────────────
    slug = experiment_id
    raw_path = config.output_dir / "raw" / f"{slug}.jsonl"
    csv_path = config.output_dir / "summaries" / f"{slug}.csv"
    write_jsonl(records, raw_path)
    write_summary_csv(records, csv_path)

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

    table.add_row("Total runs", str(len(records)))
    table.add_row("Benign task success", _frac(b_ok, len(benign_records)))
    table.add_row("Task success under attack", _frac(a_task_ok, len(attack_records)))
    table.add_row("Attack success (attacker won)", _frac(a_atk_ok, len(attack_records)))
    table.add_row("Canary leaks", str(canary_leaks))
    table.add_row("Raw JSONL", str(raw_path))
    table.add_row("Summary CSV", str(csv_path))

    console.print()
    console.print(table)


if __name__ == "__main__":
    main()
