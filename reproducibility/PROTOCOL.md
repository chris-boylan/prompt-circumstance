# Experimental Protocol — Final Lock

## Research questions

1. How much do defence conditions reduce attack success relative to no defence?
2. How do trust-boundary-aware and layered controls compare with hardening alone?
3. In tool-integrated settings, does high-risk approval gating intercept misuse attempts without additional robustness regressions?
4. Are findings consistent across `direct`, `indirect`, and `tool_integrated` environments and across model backends?

## Locked matrix

- 3 environments: `direct`, `indirect`, `tool_integrated`
- 3 defence conditions: `none`, `prompt_hardening`, `layered_defence`
- 3 model backends: `mock`, `ollama/llama3.1:8b`, `openai/gpt-4o-mini`
- 2 repeats per cell
- Total cells: 27

## Locked tool-integrated controls

- `tool_approval_mode: high_risk`
- `structured_output_enforcement: true`
- `max_tool_calls: 3`

## Primary outcome

- `attack_success_rate` (deterministic evaluator, audited via judge study)

## Secondary outcomes

- `benign_task_success_rate`
- `canary_leak_rate`
- `approval_required_tool_calls`
- `approval_intervened_attack_runs`

## Run policy

- Include both benign and attacked trials per repeat.
- Use canonical task files frozen in `reproducibility/configs/tasks/`.
- Do not modify attack families/templates during the full sweep.

## Judge-robustness gate

- Run Phase 2 judge study on stratified 50-record sample.
- Acceptance: Cohen’s kappa >= 0.70.
- If below threshold, revise deterministic rules before final thesis analysis.

## Reporting policy

- Report all matrix cells.
- Keep raw JSONL, summaries, stats, and manifests for each experiment folder.
- Generate thesis tables from aggregation artifacts only (no manual hand edits).

