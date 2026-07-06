from __future__ import annotations

from .templates import AttackTemplate


def apply_attack(input_text: str, template: AttackTemplate) -> str:
    """Append the attack suffix to the benign input text."""
    return input_text + template.suffix

