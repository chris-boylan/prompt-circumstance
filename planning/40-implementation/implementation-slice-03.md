# Prompt Injection Dissertation — Implementation Slice 3 (Tool-Integrated Environment)

Purpose: define the next implementation slice focused on tool-integrated agent behavior, where prompt injection can influence model-driven actions rather than only text outputs.

---

## 1. Slice objective

Build and evaluate a tool-integrated environment where the model can propose structured tool calls, and the harness enforces deterministic policy checks before execution.

Core question for this slice:

> Can prompt injection induce unsafe tool usage, and can policy/defence controls reduce that risk without breaking benign task utility?

---

## 2. Tool set for Slice 3

| Tool | Example execution in harness | Why it matters for security evaluation | Real-world system mapping |
|---|---|---|---|
| `kb_search(query)` | `{"tool":"kb_search","args":{"query":"duplicate charge refund policy"}}` | Tests retrieval steering and poisoned-context influence through untrusted content | Confluence, Notion, Zendesk Help Center, ServiceNow KB |
| `ticket_lookup(ticket_id)` | `{"tool":"ticket_lookup","args":{"ticket_id":"T-1042"}}` | Tests unauthorized read attempts and scope enforcement | Jira Service Management, Zendesk, ServiceNow, Freshdesk |
| `customer_lookup(customer_id)` | `{"tool":"customer_lookup","args":{"customer_id":"C-8821"}}` | Tests customer-data access boundaries and exfiltration attempts | Salesforce, HubSpot, Dynamics 365, Stripe Customer API |
| `draft_reply(ticket_id, content)` | `{"tool":"draft_reply","args":{"ticket_id":"T-1042","content":"Draft response text..."}}` | Tests outbound content control, leakage prevention, and policy-safe response generation | Zendesk replies/macros, Gmail API drafts, Outlook Graph drafts, Slack draft workflows |
| `ticket_update(ticket_id, action)` | `{"tool":"ticket_update","args":{"ticket_id":"T-1042","action":"close"}}` | Tests unsafe state changes, privilege abuse, and irreversible-action controls | Jira transitions, Zendesk ticket update APIs, ServiceNow incident updates |
| `escalate_ticket(ticket_id, team)` | `{"tool":"escalate_ticket","args":{"ticket_id":"T-1042","team":"fraud_review"}}` | Tests sequence bypass and policy constraints on escalation paths | Jira assignment/escalation, ServiceNow assignment groups, Zendesk groups/queues |
| `export_ticket_data(ticket_id, fields)` | `{"tool":"export_ticket_data","args":{"ticket_id":"T-1042","fields":["customer_email","notes"]}}` | Tests explicit data-exfiltration paths and field-level allow/deny policy | Salesforce report/export APIs, Zendesk exports, BigQuery/Snowflake loaders, S3/GCS sinks |

---

## 3. Representation and execution model

- Tool calls are represented as structured JSON actions emitted by the model.
- The runner validates tool name + arguments against policy before execution.
- Execution uses local adapters first (mock fixtures), then optional sandbox connectors under the same interface.
- All calls are captured in run-level `tool_call_log` for deterministic scoring.

---

## 4. Minimum build target

1. Add `tool_env.py` with policy-gated tool execution loop.
2. Define `allowed_tools` + argument constraints in task/config extensions.
3. Add deterministic `tool_call_log` schema and misuse scoring.
4. Implement the tool set above with mock adapters first.
5. Add one sandbox-backed integration path for external-validity checks.

---

## 5. Current implementation status

- `tool_integrated` environment is now implemented in `src/prompt_injection_eval/environments/tool_env.py`.
- Tool policy/runtime registry exists in `src/prompt_injection_eval/tools.py`.
- Run records now include `tool_call_log` entries with allow/deny decision and reason.
- Attack families include tool-focused cases:
  - `tool_misuse_inducement`
  - `argument_escalation`
  - `tool_data_exfiltration`
- Tool-integrated configs and fixtures are in place for mock/Ollama/OpenAI.
- Tool-call-first behavior is now enforced for tool-integrated runs.

---

## 6. Remaining Slice 3 hardening tasks

1. Add layered defence condition that combines hardening + trust-boundary handling + tool policy constraints.
2. Add `require_approval` policy branch for high-risk tools (not only allow/deny).
3. Add structured output enforcement policy in tool-integrated runs.
4. Add at least one sandbox-backed connector (non-production) behind current tool interface.
5. Extend aggregation outputs with per-family security/utility tradeoff summaries.

---

## 7. Remaining for dissertation-ready package (mirrored checklist)

1. Lock experimental protocol (final matrix, RQ mapping, hypotheses, stop/re-run rules).
2. Define run-volume/statistics plan (repeats rationale, confidence intervals, variance reporting).
3. Add judge-robustness validation layer (deterministic vs LLM-judge vs human sample).
4. Finalize threats-to-validity and ethics/governance artifacts.
5. Produce reproducibility package (pinned versions, frozen configs, manifests, archived outputs).
6. Prepare results-to-chapter outputs (final tables/figures mapped to dissertation questions).

---

## 8. Priority tiers (deadline-focused)

### Must do

1. Add layered defence condition.
2. Add approval-gate mode for high-risk tools.
3. Add structured output enforcement in tool-integrated runs.
4. Lock experiment matrix + repeat plan.
5. Produce per-family results tables (attack success + utility loss).
6. Finalize threats-to-validity, ethics, and reproducibility appendix materials.

### Should do (if time allows)

1. Add one sandbox-backed connector for external validity.
2. Run a judge-robustness mini-study (deterministic vs LLM judge vs small human sample).

### Can defer

1. Multiple sandbox integrations.
2. Additional/expanded attack families beyond current core set.
3. Non-essential dashboards/visual polish.
