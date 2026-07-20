# Current Development State (Handoff Reference)

Purpose: persistent checkpoint so work can be resumed cleanly if chat/session context is lost.

---

## Last confirmed status

- Direct, indirect, and tool-integrated environments are implemented.
- Config structure now includes `configs/tool_integrated/{provider}/{baseline,hardened,layered_defence}.yaml` alongside direct/indirect provider configs.
- Tool-integrated runtime now enforces a tool-call-first contract and logs policy outcomes in `tool_call_log`.
- Current local test result: `31 passed`.
- Latest runs include tool-integrated baseline/hardened comparisons across mock and Ollama.

---

## What was completed in this phase

1. Run logging extended with stable experiment metadata:
   - `experiment_id`
   - `model_version`
2. Runner now generates a run-level `experiment_id` and propagates it through benign and attacked flows.
3. Model adapter returns provider-reported model version when available.
4. Task loader now supports robust parsing paths:
   - JSONL (primary)
   - JSON array fallback
   - concatenated JSON object fallback
5. Smoke test updated to assert run-level `experiment_id` consistency and `model_version` presence.
6. Method specs added:
   - `planning/30-method-specs/attack-template-spec.md`
   - `planning/30-method-specs/run-logging-schema-spec.md`
7. Indirect environment implementation added:
   - `src/prompt_injection_eval/environments/indirect_env.py`
   - runner dispatch by `config.environment`
   - indirect task fixtures and configs
8. Config naming and layout normalized:
   - old flat names replaced with environment-first directory structure.
9. Repeat-aware aggregation added:
   - per-experiment `summaries/stats.json`
   - global `results/aggregation/matrix.json`
   - `pac-aggregate` refresh command
10. Indirect carrier metadata added:
   - `carrier_type` on indirect tasks
   - run records and CSV exports now include carrier labels
11. Stronger indirect defence added:
   - `boundary_spotlighting` prefix
   - indirect configs for mock / Ollama / OpenAI
12. Boundary spotlighting now also adds an explicit trust-boundary note to indirect user input.
13. Indirect trust-boundary bypass attacks added to the template set for testing the spotlighting defence.
14. Matrix validation tests added:
    - defence prefix checks
    - environment-specific attack routing
    - direct vs indirect input handling
15. Tool-integrated environment implementation added:
    - `src/prompt_injection_eval/environments/tool_env.py`
    - policy-gated tool execution loop with `max_tool_calls`
    - enforced tool-call-first contract in tool-integrated runs
16. Tool policy/runtime components added:
    - `src/prompt_injection_eval/tools.py`
    - local tool registry + argument validation + allow/deny decisions
17. Tool-specific attack families added:
    - `tool_misuse_inducement`
    - `argument_escalation`
    - `tool_data_exfiltration`
18. Tool-integrated fixtures/configs added:
    - `data/tasks/tool_integrated_tasks.jsonl`
    - `configs/tool_integrated/{mock,ollama,openai}/{baseline,hardened,layered_defence}.yaml`
19. Logging schema extended with `tool_call_log` in run records.
20. Test suite expanded for Slice 3 path coverage:
    - config validation
    - attack evaluator logic
    - tool-integrated smoke and routing behavior

---

## Current branch snapshot guidance

- Before continuing implementation, review:
  - `src/prompt_injection_eval/runner.py`
  - `src/prompt_injection_eval/logging_utils.py`
  - `src/prompt_injection_eval/environments/tool_env.py`
  - `src/prompt_injection_eval/tools.py`
  - `tests/test_runner_smoke_mock.py`
- Then decide whether to:
  - implement `require_approval` tool policy mode first, or
  - implement structured output enforcement first.

---

## Recommended next build target

Proceed with the dissertation harness finish checklist:

### Remaining to finish technical harness

1. Add layered defence condition (hardening + spotlighting + tool policy) as explicit config option.
2. Add approval-gate mode for high-risk tools (`require_approval`) and log decision path.
3. Add structured output enforcement policy for tool-integrated runs (strict schema fail/repair strategy).
4. Add at least one sandbox-backed connector (non-production) behind current tool interface.
5. Add per-family utility/security reporting in aggregation outputs (not only overall rates).

### Remaining for dissertation-ready package

1. Lock experimental protocol (final matrix, RQ mapping, hypotheses, stop/re-run rules).
2. Define run-volume/statistics plan (repeats rationale, confidence intervals, variance reporting).
3. Add judge-robustness validation layer (deterministic vs LLM-judge vs human sample).
4. Finalize threats-to-validity and ethics/governance artifacts.
5. Produce reproducibility package (pinned versions, frozen configs, manifests, archived outputs).
6. Prepare results-to-chapter outputs (final tables/figures mapped to dissertation questions).

### Priority tiers (deadline-focused)

**Must do**
1. Layered defence condition.
2. Approval-gate mode for high-risk tools.
3. Structured output enforcement.
4. Final experiment matrix + repeat plan lock.
5. Per-family results tables (attack success + utility loss).
6. Threats-to-validity, ethics, and reproducibility appendix.

**Should do (if time allows)**
1. One sandbox-backed connector for external validity.
2. Judge-robustness mini-study (deterministic vs LLM judge vs small human sample).

**Can defer**
1. Multiple sandbox connectors.
2. Extra attack-family expansion beyond current core.
3. Non-essential dashboard/visual extras.

---

## Resume checklist

- [x] Add repeat-run support and manifest output.
- [x] Add aggregation command/script for matrix summaries.
- [x] Add `carrier_type` field for indirect tasks and logs.
- [x] Implement one stronger indirect defence beyond prompt hardening.
- [x] Add matrix validation tests (direct/indirect x provider x defence).
- [x] Update method specs after schema/logging extensions.
- [x] Implement Slice 3 tool-integrated environment with policy-gated execution.
- [x] Add tool-integrated task/config fixtures and smoke coverage.
- [x] Enforce tool-call-first behavior in tool-integrated runs.
- [ ] Add layered defence condition for tool-integrated and indirect paths.
- [ ] Add approval-gate mode for high-risk tool actions.
- [ ] Add structured output enforcement policy for tool-integrated runs.
- [ ] Add sandbox-backed tool connector for external-validity checks.
- [ ] Add per-family utility/security reporting in aggregation outputs.
- [ ] Lock experimental protocol and statistics plan for dissertation runs.
- [ ] Add judge-robustness validation layer (deterministic vs LLM judge vs human sample).
- [ ] Finalize validity/ethics/reproducibility package and results-to-chapter outputs.
