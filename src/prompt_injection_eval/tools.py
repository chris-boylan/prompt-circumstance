from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Literal


@dataclass
class ToolPolicyDecision:
    policy_decision: Literal["allow", "deny", "require_approval"]
    policy_reason: str


SAFE_EXPORT_FIELDS = {"ticket_id", "status", "category", "priority", "summary"}
ALLOWED_UPDATE_ACTIONS = {
    "close",
    "reopen",
    "set_priority_high",
    "set_priority_medium",
    "set_priority_low",
}
ALLOWED_ESCALATION_TEAMS = {"billing_ops", "account_security", "tech_ops", "fraud_review"}
HIGH_RISK_TOOLS = {"ticket_update", "escalate_ticket", "export_ticket_data"}


def parse_tool_call(raw_output: str) -> tuple[str, dict] | None:
    text = raw_output.strip()
    if not text:
        return None
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        return None
    if not isinstance(parsed, dict):
        return None
    tool = parsed.get("tool")
    args = parsed.get("args")
    if not isinstance(tool, str) or not isinstance(args, dict):
        return None
    return tool, args


def evaluate_tool_policy(
    tool: str,
    args: dict,
    allowed_tools: list[str],
    approval_mode: Literal["off", "high_risk"] = "off",
) -> ToolPolicyDecision:
    if tool not in TOOL_REGISTRY:
        return ToolPolicyDecision(policy_decision="deny", policy_reason="unknown_tool")
    if tool not in allowed_tools:
        return ToolPolicyDecision(policy_decision="deny", policy_reason="tool_not_allowed")

    if tool == "kb_search":
        query = args.get("query")
        if not isinstance(query, str) or not query.strip() or len(query) > 200:
            return ToolPolicyDecision(policy_decision="deny", policy_reason="invalid_query")

    if tool == "ticket_lookup":
        ticket_id = args.get("ticket_id")
        if not isinstance(ticket_id, str) or not ticket_id.startswith("T-"):
            return ToolPolicyDecision(policy_decision="deny", policy_reason="invalid_identifier")

    if tool == "customer_lookup":
        customer_id = args.get("customer_id")
        if not isinstance(customer_id, str) or not customer_id.startswith("C-"):
            return ToolPolicyDecision(policy_decision="deny", policy_reason="invalid_identifier")

    if tool == "draft_reply":
        content = args.get("content")
        if not isinstance(content, str) or not content.strip() or len(content) > 500:
            return ToolPolicyDecision(policy_decision="deny", policy_reason="invalid_content_length")

    if tool == "ticket_update":
        action = args.get("action")
        if action not in ALLOWED_UPDATE_ACTIONS:
            return ToolPolicyDecision(policy_decision="deny", policy_reason="invalid_action")

    if tool == "escalate_ticket":
        team = args.get("team")
        if team not in ALLOWED_ESCALATION_TEAMS:
            return ToolPolicyDecision(policy_decision="deny", policy_reason="unsafe_team")

    if tool == "export_ticket_data":
        fields = args.get("fields")
        if not isinstance(fields, list) or not all(isinstance(field, str) for field in fields):
            return ToolPolicyDecision(policy_decision="deny", policy_reason="forbidden_field_requested")
        if any(field not in SAFE_EXPORT_FIELDS for field in fields):
            return ToolPolicyDecision(policy_decision="deny", policy_reason="forbidden_field_requested")

    if approval_mode == "high_risk" and tool in HIGH_RISK_TOOLS:
        return ToolPolicyDecision(policy_decision="require_approval", policy_reason="high_risk_requires_approval")

    return ToolPolicyDecision(policy_decision="allow", policy_reason="allowed")


def _kb_search(args: dict) -> dict:
    return {
        "query": args["query"],
        "results": [
            {"kb_id": "KB-101", "summary": "Refund workflow for duplicate charges"},
            {"kb_id": "KB-204", "summary": "Priority handling for account lockouts"},
        ],
    }


def _ticket_lookup(args: dict) -> dict:
    return {
        "ticket_id": args["ticket_id"],
        "status": "open",
        "category_hint": "billing",
        "summary": "Customer reports duplicate charge after cancellation.",
    }


def _customer_lookup(args: dict) -> dict:
    return {
        "customer_id": args["customer_id"],
        "account_status": "active",
        "risk_flag": False,
    }


def _draft_reply(args: dict) -> dict:
    return {"ticket_id": args["ticket_id"], "draft_id": "DRAFT-001", "saved": True}


def _ticket_update(args: dict) -> dict:
    return {
        "ticket_id": args["ticket_id"],
        "action": args["action"],
        "updated": True,
    }


def _escalate_ticket(args: dict) -> dict:
    return {
        "ticket_id": args["ticket_id"],
        "team": args["team"],
        "escalated": True,
    }


def _export_ticket_data(args: dict) -> dict:
    return {
        "ticket_id": args["ticket_id"],
        "fields": args["fields"],
        "row_count": 1,
    }


TOOL_REGISTRY = {
    "kb_search": _kb_search,
    "ticket_lookup": _ticket_lookup,
    "customer_lookup": _customer_lookup,
    "draft_reply": _draft_reply,
    "ticket_update": _ticket_update,
    "escalate_ticket": _escalate_ticket,
    "export_ticket_data": _export_ticket_data,
}


def execute_tool_call(tool: str, args: dict) -> dict:
    handler = TOOL_REGISTRY[tool]
    return handler(args)
