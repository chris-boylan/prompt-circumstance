# Dissertation Matrix — Phase 1 Implementation

## Overview

Phase 1 sets up the **27-cell experimental matrix** for the dissertation final run:
- **3 environments**: direct, indirect, tool_integrated
- **3 defence conditions**: none, prompt_hardening, layered_defence
- **3 models**: mock, ollama:llama3.1:8b, openai:gpt-4o-mini
- **2 repeats per cell**

Total: ~2,100 individual runs.

## Files

### Master definition
- `matrix.yaml` — matrix specification (environments, defences, models, tool overrides)

### Config generation
- `scripts/dissertation/generate_dissertation_configs.py` — generates 27 individual cell configs from matrix definition
- `configs/dissertation/cells/` — generated cell configs (cell_00.yaml through cell_26.yaml)
- `configs/dissertation/cells/registry.json` — index of all cells

### Execution scripts
- `configs/dissertation/sweep.sh` — master sweep script (executes all 27 cells sequentially with logging)
- `configs/dissertation/validate.sh` — quick validation with one mock cell

## Quick start

### Generate configs (one-time setup)
```bash
python3 scripts/dissertation/generate_dissertation_configs.py
```

This creates:
- 27 cell config files
- registry.json (index for sweep script)

### Validate (quick smoke test)
```bash
bash configs/dissertation/validate.sh
```

Runs cell_00 (direct + layered_defence + mock) to verify setup. Should complete in ~10 seconds.

Expected output:
- ~300 total runs (2 repeats × 15 tasks × (1 benign + 9 attacks))
- Manifest + stats.json generated
- Outputs in `results/dissertation/experiments/`

### Execute full matrix (production run)
```bash
bash configs/dissertation/sweep.sh 2>&1 | tee results/dissertation/sweep.log
```

Executes all 27 cells sequentially with per-cell logging:
- Cell progress printed to stdout
- Full logs per cell in `results/dissertation/sweep_logs/`
- Automatic aggregation on success (`results/dissertation/aggregation/matrix.json`)

**Estimated runtime:**
- Mock cells: ~10–20 sec each (quick, deterministic)
- Ollama cells: ~5–10 min each (local inference, 3–5 tasks × 13 trials)
- OpenAI cells: ~5–10 min each (API calls, includes latency)
- **Total: ~5–7 hours for full sweep** (can parallelize if needed)

## Output structure

After each cell completes:

```
results/dissertation/experiments/
├── dissertation-cell-00_20260720T210318/
│   ├── manifest.json           # config snapshot + metadata
│   ├── raw/runs.jsonl          # all trial records (600K+ for 300 runs)
│   ├── summaries/
│   │   ├── runs.csv            # per-trial summary
│   │   └── stats.json          # aggregated metrics (attack_success, etc.)
├── dissertation-cell-01_20260720T211503/
│   └── ...
...
```

After all cells, aggregation produces:
```
results/dissertation/aggregation/
└── matrix.json                 # per-cell metrics grid (environment × defence × model)
```

## Monitor progress

Watch the sweep in real-time:
```bash
tail -f results/dissertation/sweep_logs/cell_*.log
```

Check aggregation after all cells complete:
```bash
python3 -c "import json; print(json.dumps(json.load(open('results/dissertation/aggregation/matrix.json')), indent=2))" | head -100
```

## Reproducibility

All 27 cell configs are frozen and archived:
- Configs committed to git
- Registry pinned (no regeneration during sweep)
- Task files locked: `data/tasks/{direct,indirect,tool_integrated}_tasks.jsonl`

To replay a specific cell:
```bash
python3 -m prompt_injection_eval.runner --config configs/dissertation/cells/cell_XX.yaml
```

## Next steps

After sweep completes:
1. **Phase 2**: Implement judge-robustness mini-study infrastructure
2. **Phase 3**: Extend aggregation for per-family reporting
3. **Phase 4**: Build reproducibility package (frozen configs + artifacts)
4. **Phase 5**: Run full matrix and generate thesis tables
