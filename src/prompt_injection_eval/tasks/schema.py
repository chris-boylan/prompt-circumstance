from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

ALLOWED_CATEGORIES: list[str] = ["billing", "technical", "account"]
ALLOWED_PRIORITIES: list[str] = ["low", "medium", "high"]


class ExpectedOutput(BaseModel):
    category: str
    priority: str
    contains_sensitive_data: bool
    recommended_action: str


class Constraints(BaseModel):
    output_format: str = "json_only"
    required_fields: list[str]
    allowed_values: dict[str, list[str]]
    max_recommended_action_chars: int = 240


class TaskMetadata(BaseModel):
    difficulty: str
    domain: str
    synthetic: bool
    objective_label: str | None = None
    attack_family: str | None = None
    carrier_type: Literal["email", "markdown", "kb_snippet", "note"] | None = None
    allowed_tools: list[str] = Field(default_factory=list)
    tool_policy: str | None = None
    cia_impact: list[str] = Field(default_factory=list)


class Task(BaseModel):
    task_id: str
    task_type: str
    environment: str
    version: str
    input_text: str
    expected_output: ExpectedOutput
    constraints: Constraints
    metadata: TaskMetadata
