# Threats to Validity

## Internal validity

- **Task design bias:** Synthetic support-ticket tasks may favor some defenses.
  - Mitigation: stratified families, multi-environment matrix, full-cell reporting.
- **Evaluator coupling:** Deterministic scoring can encode assumptions.
  - Mitigation: judge-robustness mini-study and discrepancy analysis tooling.

## External validity

- **Domain transfer risk:** Results may not generalize beyond support-like tasks.
  - Mitigation: explicitly scope claims and retain extension path for new domains.
- **Model/version drift:** Hosted and local model behavior may change over time.
  - Mitigation: pin matrix model names, archive run manifests and timestamps.

## Construct validity

- **Metric proxy limitations:** `task_success` and `attack_success` are proxies for utility/robustness.
  - Mitigation: report secondary metrics (`canary_leak_rate`, tool policy interventions).
- **Tool realism gap:** Default tool handlers are mock adapters.
  - Mitigation: document as limitation; Slice 5 sandbox bridge remains optional extension.

## Statistical validity

- **Finite repeats:** Two repeats can leave residual variance.
  - Mitigation: report per-repeat summaries and dispersion in stats artifacts.
- **Multiple comparisons:** 27 matrix cells and several families increase false-positive risk.
  - Mitigation: interpret effect sizes with full matrix context, not isolated single-cell wins.

