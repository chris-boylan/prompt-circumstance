from __future__ import annotations

"""Repeat-aware aggregation utilities for experiment outputs."""

import json
from collections import defaultdict
from datetime import datetime
from datetime import timezone
from pathlib import Path
from statistics import StatisticsError
from statistics import mean
from statistics import stdev

import click
from rich.console import Console
from rich.table import Table


def _load_jsonl(path: Path) -> list[dict]:
    with open(path) as f:
        return [json.loads(line) for line in f if line.strip()]


def _rate(num: int, den: int) -> float | None:
    return round(num / den, 4) if den else None


def _series_summary(values: list[float]) -> dict[str, float | int | None]:
    if not values:
        return {"mean": None, "stdev": None, "min": None, "max": None}
    summary = {
        "mean": round(mean(values), 4),
        "min": round(min(values), 4),
        "max": round(max(values), 4),
    }
    try:
        summary["stdev"] = round(stdev(values), 4)
    except StatisticsError:
        summary["stdev"] = 0.0
    return summary


def _summarize_tool_policy(records: list[dict]) -> dict[str, int | float | None]:
    tool_events = [
        event
        for record in records
        for event in (record.get("tool_call_log") or [])
    ]
    denied = sum(1 for event in tool_events if event.get("policy_decision") == "deny")
    approval_required = sum(
        1 for event in tool_events if event.get("policy_decision") == "require_approval"
    )
    attack_records = [r for r in records if r.get("benign_or_attack") == "attack"]
    approval_attack_runs = sum(
        1
        for record in attack_records
        if any(
            event.get("policy_decision") == "require_approval"
            for event in (record.get("tool_call_log") or [])
        )
    )
    return {
        "tool_call_count": len(tool_events),
        "denied_tool_calls": denied,
        "denied_tool_call_rate": _rate(denied, len(tool_events)),
        "approval_required_tool_calls": approval_required,
        "approval_required_tool_call_rate": _rate(approval_required, len(tool_events)),
        "approval_intervened_attack_runs": approval_attack_runs,
        "approval_intervened_attack_run_rate": _rate(approval_attack_runs, len(attack_records)),
    }


def _summarize_records(records: list[dict]) -> dict:
    benign_records = [r for r in records if r["benign_or_attack"] == "benign"]
    attack_records = [r for r in records if r["benign_or_attack"] == "attack"]

    task_success_count = sum(1 for r in records if r["task_success"])
    benign_task_success_count = sum(1 for r in benign_records if r["task_success"])
    attack_task_success_count = sum(1 for r in attack_records if r["task_success"])
    attack_success_count = sum(1 for r in attack_records if r.get("attack_success"))
    canary_leak_count = sum(1 for r in attack_records if r.get("contains_canary"))

    return {
        "run_count": len(records),
        "benign_run_count": len(benign_records),
        "attack_run_count": len(attack_records),
        "task_success_count": task_success_count,
        "task_success_rate": _rate(task_success_count, len(records)),
        "benign_task_success_rate": _rate(benign_task_success_count, len(benign_records)),
        "attack_task_success_rate": _rate(attack_task_success_count, len(attack_records)),
        "attack_success_count": attack_success_count,
        "attack_success_rate": _rate(attack_success_count, len(attack_records)),
        "canary_leak_count": canary_leak_count,
        "canary_leak_rate": _rate(canary_leak_count, len(attack_records)),
    }


def summarize_experiment(experiment_dir: Path) -> dict:
    raw_path = experiment_dir / "raw" / "runs.jsonl"
    manifest_path = experiment_dir / "manifest.json"
    if not raw_path.exists():
        raise FileNotFoundError(raw_path)
    if not manifest_path.exists():
        raise FileNotFoundError(manifest_path)

    records = _load_jsonl(raw_path)
    with open(manifest_path) as f:
        manifest = json.load(f)

    repeat_groups: dict[int, list[dict]] = defaultdict(list)
    for record in records:
        repeat_groups[int(record.get("repeat_index", 1))].append(record)

    repeat_stats = []
    for repeat_index in sorted(repeat_groups):
        repeat_records = repeat_groups[repeat_index]
        repeat_stats.append(
            {
                "repeat_index": repeat_index,
                **_summarize_records(repeat_records),
            }
        )

    by_attack_family: dict[str, list[dict]] = defaultdict(list)
    attack_records = [r for r in records if r.get("benign_or_attack") == "attack"]
    for record in records:
        if record.get("benign_or_attack") == "attack":
            family = record.get("attack_family") or "unknown"
            by_attack_family[family].append(record)

    experiment_summary = {
        "experiment_id": manifest["experiment_id"],
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": {
            "experiment_dir": str(experiment_dir),
            "manifest_path": str(manifest_path),
            "raw_path": str(raw_path),
        },
        "config": {
            "run_id": manifest["run_id"],
            "environment": manifest["environment"],
            "defence_condition": manifest["defence_condition"],
            "model_provider": manifest["model_provider"],
            "model_name": manifest["model_name"],
            "n_repeats": manifest["n_repeats"],
            "tasks_file": manifest["tasks_file"],
            "include_benign": manifest["include_benign"],
            "include_attacked": manifest["include_attacked"],
        },
        "overall": _summarize_records(records),
        "tool_policy_overall": _summarize_tool_policy(records),
        "tool_policy_attack_runs": _summarize_tool_policy(attack_records),
        "repeat_stats": repeat_stats,
        "repeat_summary": {
            "task_success_rate": _series_summary(
                [repeat["task_success_rate"] for repeat in repeat_stats if repeat["task_success_rate"] is not None]
            ),
            "attack_success_rate": _series_summary(
                [repeat["attack_success_rate"] for repeat in repeat_stats if repeat["attack_success_rate"] is not None]
            ),
            "canary_leak_rate": _series_summary(
                [repeat["canary_leak_rate"] for repeat in repeat_stats if repeat["canary_leak_rate"] is not None]
            ),
        },
        "by_attack_family": {
            family: _summarize_records(family_records)
            for family, family_records in sorted(by_attack_family.items())
        },
        "approval_interventions_by_attack_family": {
            family: _summarize_tool_policy(family_records)
            for family, family_records in sorted(by_attack_family.items())
        },
    }
    return experiment_summary


def write_experiment_summary(experiment_dir: Path) -> dict:
    summary = summarize_experiment(experiment_dir)
    stats_path = experiment_dir / "summaries" / "stats.json"
    stats_path.parent.mkdir(parents=True, exist_ok=True)
    summary["output_path"] = str(stats_path)
    with open(stats_path, "w") as f:
        json.dump(summary, f, indent=2)
    return summary


def aggregate_results(results_dir: Path) -> dict:
    experiments_dir = results_dir / "experiments"
    if not experiments_dir.exists():
        return {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "results_dir": str(results_dir),
            "cells": [],
        }

    cells: dict[tuple[str, str, str, str], list[dict]] = defaultdict(list)
    experiment_ids: dict[tuple[str, str, str, str], list[str]] = defaultdict(list)

    for experiment_dir in sorted(p for p in experiments_dir.iterdir() if p.is_dir()):
        manifest_path = experiment_dir / "manifest.json"
        raw_path = experiment_dir / "raw" / "runs.jsonl"
        if not manifest_path.exists() or not raw_path.exists():
            continue
        with open(manifest_path) as f:
            manifest = json.load(f)
        records = _load_jsonl(raw_path)
        key = (
            manifest["model_provider"],
            manifest["environment"],
            manifest["defence_condition"],
            manifest["model_name"],
        )
        cells[key].extend(records)
        experiment_ids[key].append(manifest["experiment_id"])

    matrix_cells = []
    for key in sorted(cells):
        model_provider, environment, defence_condition, model_name = key
        cell_records = cells[key]
        matrix_cells.append(
            {
                "model_provider": model_provider,
                "environment": environment,
                "defence_condition": defence_condition,
                "model_name": model_name,
                "experiment_ids": sorted(experiment_ids[key]),
                "experiment_count": len(set(experiment_ids[key])),
                "summary": _summarize_records(cell_records),
            }
        )

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "results_dir": str(results_dir),
        "cell_count": len(matrix_cells),
        "cells": matrix_cells,
    }


def write_results_matrix(results_dir: Path) -> dict:
    matrix = aggregate_results(results_dir)
    output_path = results_dir / "aggregation" / "matrix.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    matrix["output_path"] = str(output_path)
    with open(output_path, "w") as f:
        json.dump(matrix, f, indent=2)
    return matrix


def refresh_results(results_dir: Path) -> tuple[list[Path], dict]:
    experiments_dir = results_dir / "experiments"
    refreshed: list[Path] = []
    if experiments_dir.exists():
        for experiment_dir in sorted(p for p in experiments_dir.iterdir() if p.is_dir()):
            write_experiment_summary(experiment_dir)
            refreshed.append(experiment_dir)
    matrix = write_results_matrix(results_dir)
    return refreshed, matrix

console = Console()


@click.command()
@click.option(
    "--results-dir",
    default=Path("results"),
    type=click.Path(file_okay=False, path_type=Path),
    show_default=True,
    help="Base results directory containing experiment folders.",
)
def main(results_dir: Path) -> None:
    refreshed, matrix = refresh_results(results_dir)

    table = Table(title="Aggregation Summary", show_lines=True)
    table.add_column("Metric", style="bold")
    table.add_column("Value")
    table.add_row("Results dir", str(results_dir))
    table.add_row("Refreshed experiments", str(len(refreshed)))
    table.add_row("Cells", str(matrix["cell_count"]))
    table.add_row("Matrix", matrix["output_path"])
    console.print(table)


if __name__ == "__main__":
    main()
