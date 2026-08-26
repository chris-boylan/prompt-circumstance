# Reproducibility Environment

## Runtime

- Python: `3.14.6`
- Project package: `prompt-and-circumstance==0.1.0`

## Core dependencies

- click>=8.1
- pydantic>=2.0.0
- pyyaml>=6.0
- rich>=13.0
- openai>=1.30.0

## Optional dependencies

- ollama runtime (for local `ollama/llama3.1:8b` matrix cells)
- anthropic/openai SDK credentials for judge study scripts
- pytest>=8.0 (test extras)

## Models used in the locked matrix

- `mock/mock`
- `ollama/llama3.1:8b`
- `openai/gpt-4o-mini`

## Freeze command

Generate a full environment lockfile with:

```bash
python3 -m pip freeze > reproducibility/requirements.txt
```

