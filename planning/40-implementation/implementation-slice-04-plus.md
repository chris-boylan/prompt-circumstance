# Prompt Injection Dissertation — Implementation Slice 4+ Roadmap

Purpose: define the post-Slice-3 implementation plan needed to complete a dissertation-defensible evaluation suite.

---

## 1. Slice 4 — Policy maturity and output safety

### Objective

Harden the control layer so the harness can distinguish safe refusal, approved action, and blocked misuse in a reproducible way.

### Scope

1. Add `require_approval` decision path for high-risk tools.
2. Add structured output enforcement for tool-integrated runs.
3. Add layered-defence behavior checks across indirect + tool-integrated environments.
4. Expand run logging for approval state transitions.

### Deliverables

- tool policy engine supports `allow`, `deny`, `require_approval`
- deterministic approval audit trail in `tool_call_log`
- structured output enforcement strategy documented and implemented
- regression tests for approval + enforcement paths

### Acceptance criteria

- high-risk tool actions can be routed to `require_approval` and logged
- invalid/non-schema final outputs are deterministically handled
- existing direct/indirect/tool-integrated tests remain green

---

## 2. Slice 5 — External-validity bridge

### Objective

Demonstrate that harness findings are not purely mock-artifacts by validating with at least one real sandbox connector.

### Scope

1. Implement one non-production sandbox-backed adapter (read-only or low-risk first).
2. Run matched scenarios in mock and sandbox modes.
3. Compare policy decisions, misuse outcomes, and utility effects.

### Deliverables

- sandbox adapter behind existing tool interface
- config route for sandbox run mode
- comparison report template (mock vs sandbox deltas)

### Acceptance criteria

- same task/attack definitions execute in both mock and sandbox routes
- mismatches are measurable and explained in validity notes
- no production systems or real user data involved

---

## 3. Slice 6 — Dissertation evidence package

### Objective

Convert the technical harness into a reproducible, thesis-ready methodology and evidence bundle.

### Scope

1. Lock experiment matrix, repeat policy, and run protocol.
2. Add per-family utility/security reporting outputs.
3. Add judge-robustness mini-study (deterministic vs LLM judge vs small human sample).
4. Finalize threats-to-validity, ethics, and reproducibility artifacts.

### Deliverables

- frozen run matrix + protocol document
- per-family results tables ready for chapter insertion
- judge agreement summary (where applicable)
- reproducibility appendix assets (versions/configs/manifests)

### Acceptance criteria

- all dissertation RQs map to concrete experiment outputs
- results can be rerun from frozen configs with consistent artifacts
- chapter-ready tables/figures are generated from repository outputs

---

## 4. Execution order and gates

1. Complete Slice 4 first (safety policy maturity).
2. Proceed to Slice 5 only after Slice 4 tests are stable.
3. Execute Slice 6 once technical behavior is stable and run matrix is frozen.

Decision gates:

- **Gate A (after Slice 4):** approval/enforcement behaviors deterministic and tested.
- **Gate B (after Slice 5):** at least one sandbox comparison complete.
- **Gate C (after Slice 6):** protocol + outputs ready for dissertation write-up.

