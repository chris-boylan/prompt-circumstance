#!/bin/bash
# Validate dissertation matrix with mock cell (quick smoke test)

set -e

echo "=== Dissertation Matrix Validation (Mock Cell) ==="
echo ""

# Find mock cell (cell_00 should be direct + layered_defence + mock)
MOCK_CELL="configs/dissertation/cells/cell_00.yaml"

if [ ! -f "$MOCK_CELL" ]; then
    echo "Error: Mock cell config not found at $MOCK_CELL"
    exit 1
fi

echo "Running validation with: $MOCK_CELL"
echo "Expected: direct environment, layered_defence, mock model"
echo ""

# Run the cell
python3 -m prompt_injection_eval.runner --config "$MOCK_CELL"

# Check output
EXPERIMENT_DIR=$(ls -1td results/dissertation/dissertation-cell-00* 2>/dev/null | head -1)
if [ -z "$EXPERIMENT_DIR" ]; then
    echo ""
    echo "✗ Validation failed: experiment directory not found"
    exit 1
fi

echo ""
echo "✓ Validation passed"
echo "Experiment: $EXPERIMENT_DIR"
echo ""
echo "Checking outputs..."
ls -lh "$EXPERIMENT_DIR"/raw/runs.jsonl
ls -lh "$EXPERIMENT_DIR"/summaries/stats.json

echo ""
echo "✓ All required outputs present"
