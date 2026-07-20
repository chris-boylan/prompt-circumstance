#!/usr/bin/env python3
"""Generate dissertation matrix configs from master definition."""

import json
from pathlib import Path
from itertools import product
import yaml


def generate_cell_config(
    cell_id: int,
    env_id: str,
    env_tasks_file: str,
    defence_id: str,
    model_provider: str,
    model_name: str,
    tool_overrides: dict | None = None,
) -> dict:
    """Generate a single cell config."""
    config = {
        "run_id": f"dissertation-cell-{cell_id:02d}",
        "environment": env_id,
        "defence_condition": defence_id,
        "model": {
            "provider": model_provider,
            "model_name": model_name,
        },
        "tasks_file": Path(env_tasks_file),
        "output_dir": Path("results/dissertation"),
        "include_benign": True,
        "include_attacked": True,
        "n_repeats": 2,
        "canary_token": "CANARY-C00326765-SETU",
    }

    # Tool-integrated specific
    if env_id == "tool_integrated" and tool_overrides:
        config.update(tool_overrides)

    return config


def main():
    # Load matrix definition
    matrix_path = Path("configs/dissertation/matrix.yaml")
    with open(matrix_path) as f:
        matrix_def = yaml.safe_load(f)

    matrix = matrix_def["matrix"]
    envs = {e["id"]: e["tasks_file"] for e in matrix["environments"]}
    defences = [d["id"] for d in matrix["defence_conditions"]]
    models = [(m["provider"], m["model_name"]) for m in matrix["models"]]
    tool_overrides = matrix.get("tool_integrated_overrides", {})

    # Generate all 27 cells
    output_dir = Path("configs/dissertation/cells")
    output_dir.mkdir(parents=True, exist_ok=True)

    cells = []
    cell_id = 0

    for env_id, defence_id, (provider, model_name) in product(
        sorted(envs.keys()), sorted(defences), sorted(models)
    ):
        config = generate_cell_config(
            cell_id=cell_id,
            env_id=env_id,
            env_tasks_file=envs[env_id],
            defence_id=defence_id,
            model_provider=provider,
            model_name=model_name,
            tool_overrides=tool_overrides if env_id == "tool_integrated" else None,
        )

        # Write cell config
        cell_config_path = output_dir / f"cell_{cell_id:02d}.yaml"
        with open(cell_config_path, "w") as f:
            # Convert Path objects to strings for YAML serialization
            config_serializable = json.loads(json.dumps(config, default=str))
            yaml.dump(config_serializable, f, default_flow_style=False, sort_keys=False)

        cells.append(
            {
                "cell_id": cell_id,
                "config_path": str(cell_config_path),
                "environment": env_id,
                "defence": defence_id,
                "model": f"{provider}/{model_name}",
            }
        )

        cell_id += 1

    # Write cell registry
    registry_path = output_dir / "registry.json"
    with open(registry_path, "w") as f:
        json.dump(
            {
                "total_cells": len(cells),
                "cells": cells,
            },
            f,
            indent=2,
        )

    print(f"Generated {len(cells)} cell configs in {output_dir}")
    print(f"Registry: {registry_path}")


if __name__ == "__main__":
    main()
