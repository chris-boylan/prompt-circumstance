# Reproducibility Bundle

This folder contains the frozen dissertation protocol and run inputs.

## Included artifacts

- `PROTOCOL.md` — locked experiment protocol and reporting policy
- `ENVIRONMENT.md` — runtime/dependency guidance
- `ETHICS.md` — ethics and governance notes
- `THREATS_TO_VALIDITY.md` — validity risk register and mitigations
- `MANIFEST.json` — machine-readable metadata snapshot
- `attack_templates.json` — frozen attack template archive
- `configs/attacks/direct_attack_templates.json` — direct-only reference mirror
- `configs/dissertation_matrix.yaml` — locked 27-cell matrix definition
- `configs/tasks/*.jsonl` — frozen task corpora
- `configs/models/*.yaml` — model backend descriptors

## Refresh metadata

```bash
python3 scripts/dissertation/build_reproducibility_bundle.py
```

## Freeze local package set

```bash
python3 -m pip freeze > reproducibility/requirements.txt
```
