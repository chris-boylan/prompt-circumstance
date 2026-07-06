from __future__ import annotations

import json
import time
from dataclasses import dataclass

from .config import ModelConfig


@dataclass
class ModelResponse:
    raw: str
    latency_ms: float
    token_usage: dict | None


def call_model(config: ModelConfig, system_prompt: str, user_prompt: str) -> ModelResponse:
    if config.provider == "mock":
        return _mock_response()
    if config.provider in ("openai", "ollama"):
        return _openai_compatible_call(config, system_prompt, user_prompt)
    raise ValueError(f"Unknown provider: {config.provider}")


def _openai_compatible_call(
    config: ModelConfig, system_prompt: str, user_prompt: str
) -> ModelResponse:
    from openai import OpenAI  # deferred so mock mode has no hard dependency

    kwargs: dict = {}
    if config.provider == "ollama":
        kwargs["api_key"] = "ollama"
        kwargs["base_url"] = config.base_url or "http://localhost:11434/v1"
    elif config.base_url:
        kwargs["base_url"] = config.base_url

    client = OpenAI(**kwargs)
    t0 = time.perf_counter()
    response = client.chat.completions.create(
        model=config.model_name,
        temperature=config.temperature,
        max_tokens=config.max_tokens,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    latency_ms = (time.perf_counter() - t0) * 1000
    raw = response.choices[0].message.content or ""
    usage = None
    if response.usage:
        usage = {
            "prompt_tokens": response.usage.prompt_tokens,
            "completion_tokens": response.usage.completion_tokens,
            "total_tokens": response.usage.total_tokens,
        }
    return ModelResponse(raw=raw, latency_ms=latency_ms, token_usage=usage)


def _mock_response() -> ModelResponse:
    """Returns valid schema-compliant JSON for pipeline testing (not accuracy testing)."""
    mock = {
        "category": "billing",
        "priority": "medium",
        "contains_sensitive_data": False,
        "recommended_action": "Review the account and process the customer request accordingly.",
    }
    return ModelResponse(raw=json.dumps(mock), latency_ms=0.0, token_usage=None)

