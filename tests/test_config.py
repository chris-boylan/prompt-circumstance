from pathlib import Path

import pytest
from pydantic import ValidationError

from prompt_injection_eval.config import RunConfig


def test_from_yaml_parses_and_applies_defaults(tmp_path: Path) -> None:
    config_file = tmp_path / "config.yaml"
    config_file.write_text(
        "\n".join(
            [
                'run_id: "t"',
                'defence_condition: "none"',
                "model:",
                '  provider: "mock"',
                '  model_name: "mock"',
                'tasks_file: "data/tasks/direct_tasks.jsonl"',
                'output_dir: "results"',
            ]
        )
    )

    cfg = RunConfig.from_yaml(config_file)

    assert cfg.environment == "direct"
    assert cfg.include_benign is True
    assert cfg.include_attacked is True
    assert cfg.canary_token == "CANARY-XK7P9Q2M"
    assert isinstance(cfg.tasks_file, Path)
    assert isinstance(cfg.output_dir, Path)


def test_from_yaml_invalid_provider_raises(tmp_path: Path) -> None:
    config_file = tmp_path / "bad_provider.yaml"
    config_file.write_text(
        "\n".join(
            [
                'run_id: "t"',
                'defence_condition: "none"',
                "model:",
                '  provider: "invalid"',
                '  model_name: "mock"',
                'tasks_file: "data/tasks/direct_tasks.jsonl"',
                'output_dir: "results"',
            ]
        )
    )

    with pytest.raises(ValidationError):
        RunConfig.from_yaml(config_file)


def test_from_yaml_invalid_defence_condition_raises(tmp_path: Path) -> None:
    config_file = tmp_path / "bad_defence.yaml"
    config_file.write_text(
        "\n".join(
            [
                'run_id: "t"',
                'defence_condition: "bad"',
                "model:",
                '  provider: "mock"',
                '  model_name: "mock"',
                'tasks_file: "data/tasks/direct_tasks.jsonl"',
                'output_dir: "results"',
            ]
        )
    )

    with pytest.raises(ValidationError):
        RunConfig.from_yaml(config_file)


def test_from_yaml_allows_indirect_environment(tmp_path: Path) -> None:
    config_file = tmp_path / "indirect.yaml"
    config_file.write_text(
        "\n".join(
            [
                'run_id: "t"',
                'defence_condition: "none"',
                "model:",
                '  provider: "mock"',
                '  model_name: "mock"',
                'environment: "indirect"',
                'tasks_file: "data/tasks/indirect_tasks.jsonl"',
                'output_dir: "results"',
            ]
        )
    )

    cfg = RunConfig.from_yaml(config_file)

    assert cfg.environment == "indirect"
