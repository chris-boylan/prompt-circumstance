from prompt_injection_eval.tools import evaluate_tool_policy


def test_high_risk_tool_requires_approval_when_enabled() -> None:
    decision = evaluate_tool_policy(
        tool="ticket_update",
        args={"ticket_id": "T-1001", "action": "close"},
        allowed_tools=["ticket_update"],
        approval_mode="high_risk",
    )
    assert decision.policy_decision == "require_approval"
    assert decision.policy_reason == "high_risk_requires_approval"


def test_high_risk_tool_allows_when_approval_mode_off() -> None:
    decision = evaluate_tool_policy(
        tool="ticket_update",
        args={"ticket_id": "T-1001", "action": "close"},
        allowed_tools=["ticket_update"],
        approval_mode="off",
    )
    assert decision.policy_decision == "allow"
    assert decision.policy_reason == "allowed"


def test_invalid_arguments_still_deny_even_with_approval_mode() -> None:
    decision = evaluate_tool_policy(
        tool="ticket_update",
        args={"ticket_id": "T-1001", "action": "wipe_account"},
        allowed_tools=["ticket_update"],
        approval_mode="high_risk",
    )
    assert decision.policy_decision == "deny"
    assert decision.policy_reason == "invalid_action"
