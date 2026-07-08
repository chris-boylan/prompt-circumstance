# Prompt and Circumstance — Slice 1

Dissertation prototype for evaluating direct prompt injection attacks and defences under reproducible, deterministic conditions.

Tagline: a prompt-injection robustness harness with deterministic scoring and auditable run logs.

---

## What this is

A researcher-controlled evaluation harness for early dissertation slices:

- **Environment**: direct and indirect prompt injection (single-turn, no tools, no retrieval)
- **Task**: structured support-ticket classification → fixed JSON output
- **Attack families**: instruction override · canary exfiltration · structured output disruption
- **Defence conditions**: no defence (baseline) · prompt hardening
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
pac-run --config configs/direct-mock-baseline.yaml
pac-run --config configs/direct-mock-hardened.yaml
pac-run --config configs/indirect-mock-baseline.yaml
pac-run --config configs/indirect-mock-hardened.yaml
```

Results land in `results/raw/` (JSONL) and `results/summaries/` (CSV).

### 3. Run with local Llama 3.1 (no cost, no API key)

```bash
brew install ollama
ollama pull llama3.1:8b
ollama serve &   # keep running in background

pac-run --config configs/direct-ollama-baseline.yaml
pac-run --config configs/direct-ollama-hardened.yaml
pac-run --config configs/indirect-ollama-baseline.yaml
pac-run --config configs/indirect-ollama-hardened.yaml
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
pac-run --config configs/direct-openai-baseline.yaml
pac-run --config configs/direct-openai-hardened.yaml
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
  direct-mock-baseline.yaml
  direct-mock-hardened.yaml
  direct-ollama-baseline.yaml
  direct-ollama-hardened.yaml
  direct-openai-baseline.yaml
  direct-openai-hardened.yaml
  indirect-ollama-baseline.yaml
  indirect-ollama-hardened.yaml
  indirect-mock-baseline.yaml
  indirect-mock-hardened.yaml

results/
  raw/        # one JSONL file per run (full audit trail)
  summaries/  # one CSV file per run (analysis-ready)
```

---

## Output record fields (per run)

| Field | Description |
|---|---|
| `run_id` | UUID per individual trial |
| `task_id` | task identifier |
| `benign_or_attack` | `"benign"` or `"attack"` |
| `attack_family` | `instruction_override` / `secret_canary_exfiltration` / `structured_output_disruption` |
| `attack_template_id` | e.g. `io_001`, `ce_002` |
| `cia_impact` | pipe-separated CIA labels |
| `defence_condition` | `none` or `prompt_hardening` |
| `task_success` | boolean — deterministic |
| `attack_success` | boolean — deterministic |
| `contains_canary` | boolean — canary token found in output |
| `json_valid` | boolean |
| `core_labels_correct` | boolean |
| `task_failure_reason` | human-readable failure code |
| `latency_ms` | wall-clock time for model call |

---

## Canary token

The synthetic canary `CANARY-XK7P9Q2M` is embedded in `system_baseline.txt` via `{{CANARY_TOKEN}}` and injected at runtime from the config. All task records are fully synthetic — no real user data.

---

## Ethics statement

All experiments use synthetic data only. No real user data, production systems, or third-party targets are used at any point. API usage complies with OpenAI's usage policy for academic research.

---

## Next steps after Slice 1

1. `planning/30-method-specs/attack-template-spec.md`
2. `planning/30-method-specs/run-logging-schema-spec.md`
3. Add `src/prompt_injection_eval/environments/indirect_env.py` for Slice 2
