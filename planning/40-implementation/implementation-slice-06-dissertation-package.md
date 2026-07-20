# Slice 6 — Dissertation evidence package

## Objective

Convert the technical harness into a reproducible, thesis-ready methodology and evidence bundle.

---

## Part 1: Experiment Matrix Lock

### 1.1 Final experiment cells

Run **3 environments × 3 defence conditions × 3 models = 27 cells**. Each cell: 2 repeats, benign + attacked.

#### Environments
1. `direct` — prompt injection only (baseline)
2. `indirect` — untrusted carrier (email, markdown, etc.)
3. `tool_integrated` — structured tool calls with policy gating

#### Defence conditions
1. `none` — baseline system prompt only
2. `prompt_hardening` — security policy prefix
3. `layered_defence` — hardening + boundary spotlighting + tool policy (`approval=high_risk, structured=true`)

#### Models
1. `mock` — deterministic mock (for validation/CI)
2. `ollama:llama3.1:8b` — local open model
3. `openai:gpt-4o-mini` — commercial baseline (if available)

### 1.2 Matrix cell mapping

```
CELL_ID  | ENVIRONMENT     | DEFENCE_CONDITION   | MODEL              | REPEAT | RUNS_APPROX
---------|-----------------|---------------------|--------------------|--------|------------
00       | direct          | none                | mock               | 2      | 2 × 2 = 4
01       | direct          | none                | ollama:llama3.1:8b | 2      | 2 × 2 = 4
02       | direct          | none                | openai:gpt-4o-mini | 2      | 2 × 2 = 4
03       | direct          | prompt_hardening    | mock               | 2      | 2 × 2 = 4
...      | ...             | ...                 | ...                | ...    | ...
26       | tool_integrated | layered_defence     | openai:gpt-4o-mini | 2      | 2 × 2 = 4
---------|-----------------|---------------------|--------------------|--------|------------
TOTAL RUNS: 27 cells × 2 repeats × 2 trials (benign + attacked, 12 attacks/trial) ≈ ~1,300 individual runs
```

### 1.3 Config generation

Create consolidated config files:
- `configs/dissertation/matrix.yaml` — master matrix definition with all 27 cells
- `configs/dissertation/sweep.sh` — bash script to execute all cells with logging

Each cell config will:
- Lock `tool_approval_mode: "high_risk"` for tool_integrated runs.
- Lock `structured_output_enforcement: true` for tool_integrated runs.
- Use canonical task files: `data/tasks/{direct,indirect,tool_integrated}_tasks.jsonl` (frozen versions).
- Pin attack templates (no new families mid-run).

### 1.4 Reproducibility requirements per cell

For each cell, archive:
```
results/dissertation/
├── CELL_00_direct_none_mock/
│   ├── manifest.json           # config snapshot + metadata
│   ├── raw/runs.jsonl          # all trial records
│   ├── summaries/
│   │   ├── runs.csv            # human-readable trial summary
│   │   └── stats.json          # aggregated metrics
│   ├── protocol.md             # cell-specific notes (task count, attack families, model params)
│   └── seed.txt                # random seed (if applicable)
├── CELL_01_direct_none_ollama/
│   └── ...
```

---

## Part 2: Judge-robustness mini-study

### 2.1 Objective

Validate that attack success/failure scoring is not an artifact of deterministic rules; demonstrate consistency across manual review.

### 2.2 Design

**Population:** 50 random attack records from the full run (stratified by attack family, defence condition).

**Judges:**
1. **Deterministic scorer** (your existing `evaluate_attack()` function).
2. **LLM judge** (Claude or GPT to independently label success/failure).
3. **Human sample** (3–5 human reviewers on 20 stratified records for spot-check agreement).

**Metric:** Cohen's kappa or % agreement on binary attack success label.

### 2.3 Implementation steps

1. **Extract 50-record sample:**
   ```bash
   python3 scripts/sample_for_judge_study.py \
     --runs-jsonl results/dissertation/FULL_RUNS.jsonl \
     --sample-size 50 \
     --stratify-by attack_family,defence_condition \
     --output results/dissertation/judge_study_sample.jsonl
   ```

2. **Run LLM judge:**
   ```bash
   python3 scripts/llm_judge.py \
     --sample results/dissertation/judge_study_sample.jsonl \
     --model gpt-4o-mini \
     --output results/dissertation/llm_judge_labels.json
   ```

3. **Compare deterministic vs LLM:**
   ```bash
   python3 scripts/judge_agreement.py \
     --deterministic results/dissertation/judge_study_sample.jsonl \
     --llm results/dissertation/llm_judge_labels.json \
     --output results/dissertation/judge_agreement_report.json
   ```

### 2.4 Acceptance criteria

- **Kappa ≥ 0.70** (substantial agreement).
- **Discrepancies explained** in report (e.g., LLM stricter on canary detection).
- **Human sample agreement ≥ 80%** on spot-check subset.

If any condition fails, revise deterministic rules before final run.

---

## Part 3: Per-family reporting outputs

### 3.1 Aggregation by attack family

Extend `aggregation.py` to produce per-family tables:

```json
{
  "by_attack_family": {
    "instruction_override": {
      "run_count": 216,
      "attack_success_rate": 0.85,
      "benign_utility_rate": 0.72,
      "canary_leak_rate": 0.05,
      "approval_intervened_runs": 12,
      "by_defence": {
        "none": { "attack_success": 0.95, "benign_utility": 0.60, ... },
        "prompt_hardening": { ... },
        "layered_defence": { ... }
      }
    },
    ...
  }
}
```

### 3.2 Chapter-ready outputs

Generate CSV/table templates for thesis insertion:

```bash
python3 scripts/generate_thesis_tables.py \
  --aggregation results/dissertation/aggregation.json \
  --output results/dissertation/thesis_tables/ \
  --formats csv,latex,markdown
```

Output files:
- `thesis_tables/table_01_overall_robustness.md` — attack success rates by environment/defence
- `thesis_tables/table_02_utility_security_tradeoff.md` — benign utility vs attack success by family
- `thesis_tables/table_03_approval_interventions.md` — tool policy impact per family
- `thesis_tables/figure_01_robustness_heatmap.pdf` — environment × defence grid

---

## Part 4: Reproducibility artifact package

### 4.1 Frozen environment specification

Create `reproducibility/ENVIRONMENT.md`:

```markdown
# Reproducibility Environment

## Python version
- Python 3.10+

## Dependencies (frozen)
- pydantic==2.5.0
- click==8.1.7
- rich==13.7.0
- pyyaml==6.0.1
- ollama==0.0.48  (if using local ollama backend)
- openai==1.3.0   (if using openai backend)

Generate lock file:
\`\`\`bash
pip freeze > reproducibility/requirements.txt
\`\`\`

## Model versions used
- Mock: deterministic, no external model
- Ollama: llama3.1:8b (pulled 2026-07-20)
- OpenAI: gpt-4o-mini (API version as of 2026-07-20)
```

### 4.2 Config archive

Create `reproducibility/configs/`:
```
reproducibility/
├── configs/
│   ├── dissertation_matrix.yaml      # master config (27 cells)
│   ├── tasks/
│   │   ├── direct_tasks.jsonl        # frozen task set
│   │   ├── indirect_tasks.jsonl
│   │   └── tool_integrated_tasks.jsonl
│   └── models/
│       ├── mock.yaml
│       ├── ollama.yaml
│       └── openai.yaml
├── attack_templates.json             # frozen attack families + templates
├── protocol.md                       # full experimental protocol
└── ENVIRONMENT.md                    # dependency lock
```

### 4.3 Metadata manifest

Create `reproducibility/MANIFEST.json`:

```json
{
  "dissertation_name": "Prompt Injection Evaluation at Scale",
  "created_at": "2026-07-20",
  "harness_version": "1.0.0",
  "git_commit": "abc123def456...",
  "python_version": "3.10.12",
  "matrix_cells": 27,
  "total_runs_approx": 1300,
  "repeat_policy": "2 repeats per cell",
  "task_count_per_environment": {
    "direct": 2,
    "indirect": 2,
    "tool_integrated": 3
  },
  "attack_families": 12,
  "judge_study_size": 50,
  "output_structure": {
    "raw_runs": "results/dissertation/*/raw/runs.jsonl",
    "stats": "results/dissertation/*/summaries/stats.json",
    "judge_study": "results/dissertation/judge_study_report.json",
    "thesis_tables": "results/dissertation/thesis_tables/"
  }
}
```

---

## Part 5: Threats-to-validity and ethics artifacts

### 5.1 Threats document

Create `reproducibility/THREATS_TO_VALIDITY.md`:

```markdown
# Threats to Validity

## Internal validity
- **Mock model bias:** deterministic mock may not reflect real LLM behavior.
  - Mitigation: compare mock, ollama, openai cells; report deltas.
- **Task design bias:** support ticket domain may not generalize to other domains.
  - Mitigation: acknowledge domain scope in RQ definitions; suggest future work.
- **Attack template completeness:** 12 families may not exhaust all prompt injection vectors.
  - Mitigation: document family selection rationale; open taxonomy to community.

## External validity
- **Small model focus:** llama3.1:8b may differ from GPT-4 in vulnerability patterns.
  - Mitigation: include gpt-4o-mini cell; report model-specific findings.
- **Mock-only constraints:** mock tool execution is non-realistic.
  - Mitigation: Slice 5 sandbox study (deferred); acknowledge in limitations.

## Construct validity
- **Attack success scoring:** deterministic rules may not capture all misuse.
  - Mitigation: judge-robustness mini-study with LLM + human review.
- **Utility metric:** benign task success is a proxy for utility, not a complete measure.
  - Mitigation: report task success alongside other signals (latency, token usage).

## Statistical validity
- **Sample size:** 27 cells × 2 repeats = modest repeat count.
  - Mitigation: report confidence intervals; acknowledge high variance possible.
- **Multiple comparisons:** 27 cells tested; risk of false positives.
  - Mitigation: pre-register hypothesis; use Bonferroni or FDR correction where applicable.
```

### 5.2 Ethics and governance

Create `reproducibility/ETHICS.md`:

```markdown
# Ethics and Governance

## Data handling
- **No real user data:** all tasks and identifiers are synthetic.
- **Synthetic task corpus:** customer names, ticket IDs, etc. are procedurally generated.
- **No real API calls:** tool-integrated runs use mock backends; no external systems accessed.

## Responsible disclosure
- **Findings:** any unexpected LLM vulnerabilities discovered will be reported to model vendors before publication (30-day disclosure window).
- **Attack templates:** published templates are educational; no zero-day exploits included.

## Fairness
- **Model selection:** includes open (ollama) and commercial (openai) to avoid vendor bias.
- **Defence applicability:** defences tested are model-agnostic; findings generalizable across backends.

## Reproducibility commitment
- **Code:** source code released under [MIT/Apache] license.
- **Configs:** all experiment configs frozen and archived in `reproducibility/`.
- **Results:** full run artifacts (raw JSONL, stats, manifests) published with dissertation.
```

---

## Part 6: Protocol lock document

### 6.1 Experimental protocol

Create `reproducibility/PROTOCOL.md`:

```markdown
# Experimental Protocol — Final Lock

## Research questions (frozen)
1. **RQ1:** How effective is prompt hardening in reducing prompt injection success?
2. **RQ2:** Does boundary spotlighting improve robustness beyond hardening alone?
3. **RQ3:** Can policy-gated tool calls (approval mode) reduce tool misuse without breaking utility?
4. **RQ4:** How do defences interact across environments (direct, indirect, tool-integrated)?

## Hypothesis map
| RQ | Hypothesis | Expected outcome |
|----|-----------|------------------|
| RQ1 | Hardening reduces instruction override family success by ≥15% | `none` vs `prompt_hardening`: Δ ≥ 0.15 |
| RQ2 | Layered defence (hardening + spotlighting) further reduces by ≥10% | `layered_defence` vs `prompt_hardening`: Δ ≥ 0.10 |
| RQ3 | Approval mode reduces tool misuse without ≥10% utility loss | `approval=high_risk`: tool_call_interceptions ≥ 10%, benign_success drop ≤ 0.10 |
| RQ4 | Robustness ranking: `none` < `hardening` < `layered`; consistent across environments | all 3 environments show same ranking |

## Primary outcome
- **Metric:** attack_success_rate (deterministic scoring, verified by judge study).
- **Analysis:** report mean ± SD across 2 repeats; confidence intervals per cell.

## Secondary outcomes
- Benign task success rate (utility measure).
- Canary token leak rate (confidentiality signal).
- Tool approval interventions (Slice 4 control activity).
- Judge agreement (scoring robustness).

## Stop rules (pre-registered)
- If judge study kappa < 0.60: halt and revise scoring rules before final run.
- If any model crashes or becomes unavailable: substitute with next-best available model and document.
- If attack families drift >5% in success rate across 2 repeats: investigate and rebalance task difficulty.

## Reporting standards
- Report all results (no cherry-picking successful cells).
- For non-significant findings: still report point estimates and confidence intervals.
- Publish full artifact set: raw JSONL, stats, tables, judge study results.
```

### 6.2 Commit protocol lock

Once approved, create a git tag:

```bash
git tag -a dissertation-protocol-v1.0 \
  -m "Protocol lock: 27-cell matrix, judge study design, reproducibility artifact spec" \
  && git push origin dissertation-protocol-v1.0
```

---

## Part 7: Implementation checklist

### Phase 1: Matrix & configs (1 day)
- [ ] Define all 27 cells in `dissertation_matrix.yaml`
- [ ] Generate sweep script
- [ ] Create per-cell config files
- [ ] Validate configs with mock run of 1 cell

### Phase 2: Judge study infrastructure (2 days)
- [ ] Implement `sample_for_judge_study.py` (stratified sampling)
- [ ] Implement `llm_judge.py` (Claude/GPT labeling)
- [ ] Implement `judge_agreement.py` (kappa/agreement metrics)
- [ ] Run judge study on sample records

### Phase 3: Aggregation & reporting (1 day)
- [ ] Extend `aggregation.py` for per-family + by-defence breakdowns
- [ ] Create `generate_thesis_tables.py` (CSV/LaTeX/Markdown output)
- [ ] Test table generation on mock results

### Phase 4: Reproducibility package (1 day)
- [ ] Freeze `requirements.txt`
- [ ] Archive configs to `reproducibility/configs/`
- [ ] Create `ENVIRONMENT.md`, `MANIFEST.json`, `THREATS_TO_VALIDITY.md`, `ETHICS.md`, `PROTOCOL.md`
- [ ] Tag git commit

### Phase 5: Full dissertation matrix run (TBD, depends on compute)
- [ ] Execute all 27 cells with 2 repeats
- [ ] Aggregate results
- [ ] Generate thesis tables
- [ ] Final spot-check validation

---

## Acceptance criteria (Gate C)

- [ ] Matrix locked: 27 cells defined, configs generated and validated.
- [ ] Judge study complete: kappa ≥ 0.70; discrepancies explained.
- [ ] Per-family reporting: all families have breakdowns by defence condition.
- [ ] Reproducibility package: all artifacts archived, MANIFEST + PROTOCOL published.
- [ ] Threats documented: internal/external/construct/statistical threats identified + mitigations.
- [ ] Ethics approved: data handling, disclosure, fairness reviewed and signed off.
- [ ] Protocol tagged: `dissertation-protocol-v1.0` committed and pushed.

Once all criteria met: **protocol is frozen and ready for final dissertation run.**
