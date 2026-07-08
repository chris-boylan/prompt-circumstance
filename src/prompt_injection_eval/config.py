from __future__ import annotations

"""Typed configuration models for experiment runs.

YAML files are parsed into these Pydantic models to provide strict, explicit
runtime settings for reproducible experiments.
"""

from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel


class ModelConfig(BaseModel):
    """Provider-specific model invocation settings."""

    provider: Literal["openai", "ollama", "mock"]
    model_name: str
    temperature: float = 0.0
    max_tokens: int = 512
    base_url: str | None = None  # override for ollama: http://localhost:11434/v1


class RunConfig(BaseModel):
    """Top-level run configuration loaded from a YAML file."""

    run_id: str
    defence_condition: Literal["none", "prompt_hardening"]
    model: ModelConfig
    environment: Literal["direct", "indirect"] = "direct"
    tasks_file: Path
    output_dir: Path
    include_benign: bool = True
    include_attacked: bool = True
    canary_token: str = "CANARY-XK7P9Q2M"
    system_prompt_version: str = "v1"

    @classmethod
    def from_yaml(cls, path: Path) -> "RunConfig":
        """Load and validate a YAML config file into a typed RunConfig."""

        with open(path) as f:
            data = yaml.safe_load(f)
        return cls(**data)
