# Prompt and Circumstance — Slice 1

Dissertation prototype for evaluating direct prompt injection attacks and defences under reproducible, deterministic conditions.

Tagline: a prompt-injection robustness harness with deterministic scoring and auditable run logs.

---

## What this is

A researcher-controlled evaluation harness for early dissertation slices:

- **Environment**: direct and indirect prompt injection (single-turn, no tools, no retrieval)
- **Task**: structured support-ticket classification → fixed JSON output
- **Attack families**: instruction override · canary exfiltration · structured output disruption · indirect trust-boundary bypass
- **Defence conditions**: no defence (baseline) · prompt hardening · boundary spotlighting
- **Scoring**: fully deterministic — no LLM judge
- **Models**: mock (pipeline testing) · `llama3.1:8b` via Ollama (local) · `gpt-4.1` via OpenAI API

---

## Quick start

### 1. Install

```bash
cd /Users/chboylan/Code/thesis
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

### 2. Smoke test with mock provider (no API needed)

```bash
pac-run --config configs/direct/mock/baseline.yaml
pac-run --config configs/direct/mock/hardened.yaml
pac-run --config configs/indirect/mock/baseline.yaml
pac-run --config configs/indirect/mock/hardened.yaml
pac-run --config configs/indirect/mock/boundary_spotlighting.yaml
```

Results land in `results/experiments/<experiment_id>/` with:
- `raw/runs.jsonl`
- `summaries/runs.csv`
- `summaries/stats.json`
- `manifest.json`

Use `n_repeats` in config YAML to run the same experiment multiple times under one experiment folder.
The runner writes `stats.json` automatically after each experiment; use `pac-aggregate --results-dir results` to refresh all experiment stats and write the global matrix at `results/aggregation/matrix.json`.

### 3. Run with local Llama 3.1 (no cost, no API key)

```bash
brew install ollama
ollama pull llama3.1:8b
ollama serve &   # keep running in background

pac-run --config configs/direct/ollama/baseline.yaml
pac-run --config configs/direct/ollama/hardened.yaml
pac-run --config configs/indirect/ollama/baseline.yaml
pac-run --config configs/indirect/ollama/hardened.yaml
pac-run --config configs/indirect/ollama/boundary_spotlighting.yaml
```

If you see `model 'llama3.1:8b' not found`, confirm which tags are installed and
either pull the expected tag or update `model_name` in your config:

```bash
ollama list
ollama pull llama3.1:8b
```

### 4. Run with GPT-4.1 (after ethics confirmation)

```bash
export OPENAI_API_KEY=sk-...
pac-run --config configs/direct/openai/baseline.yaml
pac-run --config configs/direct/openai/hardened.yaml
pac-run --config configs/indirect/openai/baseline.yaml
pac-run --config configs/indirect/openai/hardened.yaml
pac-run --config configs/indirect/openai/boundary_spotlighting.yaml
```

---

## Config reference

Each run is controlled by one YAML config file passed to `pac-run --config ...`.

### Top-level fields

| Field | Type | Required | Meaning |
|---|---|---|---|
| `run_id` | string | yes | Logical run label used in `experiment_id` and output folder naming. |
| `defence_condition` | enum | yes | Defence mode: `none`, `prompt_hardening`, or `boundary_spotlighting`. |
| `environment` | enum | no | Environment route: `direct` or `indirect` (default: `direct`). |
| `tasks_file` | path | yes | Task dataset file path (`.jsonl`). |
| `output_dir` | path | yes | Base output directory (runner writes under `results/experiments/<experiment_id>/...`). |
| `include_benign` | bool | no | Include benign (non-attacked) trials (default: `true`). |
| `include_attacked` | bool | no | Include attacked trials (default: `true`). |
| `n_repeats` | int | no | Number of repeats for the same config (default: `1`, min: `1`). |
| `canary_token` | string | no | Synthetic secret token used for leakage detection. |
| `system_prompt_version` | string | no | Free-form prompt version label for provenance. |

### `model` block fields

| Field | Type | Required | Meaning |
|---|---|---|---|
| `provider` | enum | yes | `mock`, `ollama`, or `openai`. |
| `model_name` | string | yes | Model identifier for chosen provider. |
| `temperature` | float | no | Sampling temperature (default: `0.0`). |
| `max_tokens` | int | no | Max completion tokens (default: `512`). |
| `base_url` | string | no | Provider endpoint override (commonly used for Ollama). |

### Example config

```yaml
run_id: "indirect-ollama-hardened"
defence_condition: "prompt_hardening"
environment: "indirect"
model:
  provider: "ollama"
  model_name: "llama3.1:8b"
  temperature: 0.0
  max_tokens: 512
  base_url: "http://localhost:11434/v1"
tasks_file: "data/tasks/indirect_tasks.jsonl"
output_dir: "results"
include_benign: true
include_attacked: true
n_repeats: 3
canary_token: "CANARY-C00326765-SETU"
system_prompt_version: "v2-indirect-hardened"
```

---

## Project layout

```
src/prompt_injection_eval/
  config.py             # RunConfig + ModelConfig (Pydantic)
  models.py             # provider adapter: openai / ollama / mock
  runner.py             # CLI entrypoint (pie-run)
  logging_utils.py      # build_run_record, write_jsonl, write_summary_csv
  prompts/
    system_baseline.txt # base system prompt with {{CANARY_TOKEN}} placeholder
  tasks/
    schema.py           # Task, ExpectedOutput, Constraints Pydantic models
    loader.py           # JSONL loader
    evaluator.py        # deterministic task scoring
  attacks/
    templates.py        # AttackTemplate dataclasses + ATTACK_TEMPLATES list
    generator.py        # apply_attack(input_text, template)
    evaluator.py        # deterministic attack success detection
  defences/
    baseline.py         # Condition 0: pass-through
    prompt_hardening.py # Condition 1: prepend security policy
  environments/
    direct_env.py       # run_benign / run_attacked
    indirect_env.py     # indirect untrusted-content benign / attacked runs

data/
  tasks/direct_tasks.jsonl          # 15 synthetic support tickets
  tasks/indirect_tasks.jsonl        # indirect tasks with untrusted content blocks
  attacks/direct_attack_templates.json  # attack template reference (JSON mirror)

configs/
  direct/
    mock/
      baseline.yaml
      hardened.yaml
    ollama/
      baseline.yaml
      hardened.yaml
    openai/
      baseline.yaml
      hardened.yaml
  indirect/
    mock/
      baseline.yaml
      hardened.yaml
    ollama/
      baseline.yaml
      hardened.yaml
    openai/
      baseline.yaml
      hardened.yaml

results/
  aggregation/
    matrix.json         # global cross-experiment summary
  experiments/
    <experiment_id>/
      raw/runs.jsonl      # full audit trail
      summaries/runs.csv  # analysis-ready summary
      summaries/stats.json # repeat-aware stats for this experiment
      manifest.json       # run metadata and config snapshot
```

---

## Output record fields (per run)

| Field | Description |
|---|---|
| `experiment_id` | ID for the whole run batch; shared by all records from one `pac-run` invocation. |
| `run_id` | UUID per individual trial |
| `task_id` | task identifier |
| `attack_template_id` | stable ID for the attack suffix used in that trial |
| `carrier_type` | indirect carrier label (`email`, `markdown`, `kb_snippet`, `note`) |
| `benign_or_attack` | `"benign"` or `"attack"` |
| `attack_family` | `instruction_override` / `secret_canary_exfiltration` / `structured_output_disruption` / `trust_boundary_bypass` |
| `cia_impact` | pipe-separated CIA labels |
| `defence_condition` | `none` or `prompt_hardening` |
| `task_success` | boolean — deterministic |
| `attack_success` | boolean — deterministic |
| `contains_canary` | boolean — canary token found in output |
| `json_valid` | boolean |
| `core_labels_correct` | boolean |
| `task_failure_reason` | human-readable failure code |
| `latency_ms` | wall-clock time for model call |

### Attack ID prefix map

| Prefix | Family | Meaning |
|---|---|---|
| `io_` | `instruction_override` | Attempts to override the task or system instructions |
| `ce_` | `secret_canary_exfiltration` | Attempts to leak the synthetic canary or hidden prompt content |
| `sod_` | `structured_output_disruption` | Attempts to break JSON/schema compliance |
| `tb_` | `trust_boundary_bypass` | Attempts to launder untrusted content as trusted in indirect runs |

### ID breakdown

| ID | Meaning |
|---|---|
| `experiment_id` | One experiment batch, e.g. `indirect-openai-hardened_20260713T204512` |
| `run_id` | One trial within that batch; unique UUID per record |
| `task_id` | The underlying task fixture being evaluated |
| `attack_template_id` | The exact malicious suffix template used, e.g. `io_001` or `tb_002` |

### Task ID prefix map

| Prefix | Meaning |
|---|---|
| `direct_cls_` | Direct support-ticket classification task |
| `indirect_cls_` | Indirect support-ticket classification task |

---

## Canary token

The synthetic canary `CANARY-C00326765-SETU` is embedded in `system_baseline.txt` via `{{CANARY_TOKEN}}` and injected at runtime from the config. All task records are fully synthetic — no real user data.

---

## Ethics statement

All experiments use synthetic data only. No real user data, production systems, or third-party targets are used at any point. API usage complies with OpenAI's usage policy for academic research.

---

## Next steps after Slice 1

1. `planning/30-method-specs/attack-template-spec.md`
2. `planning/30-method-specs/run-logging-schema-spec.md`
3. Add `src/prompt_injection_eval/environments/indirect_env.py` for Slice 2
