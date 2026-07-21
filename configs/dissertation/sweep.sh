#!/bin/bash
# Dissertation matrix sweep — execute all 27 cells with logging

set -e

REGISTRY="configs/dissertation/cells/registry.json"
LOG_DIR="results/dissertation/sweep_logs"
mkdir -p "$LOG_DIR"

if [ ! -f "$REGISTRY" ]; then
    echo "Error: registry not found at $REGISTRY"
    exit 1
fi

total_cells=$(jq '.total_cells' "$REGISTRY")
echo "=== Dissertation Matrix Sweep ==="
echo "Total cells: $total_cells"
echo "Repeats per cell: 2"
echo "Log directory: $LOG_DIR"
echo ""

# Track progress
passed=0
failed=0
skipped=0

# Execute each cell
progress=0
for cell_id in $(jq -r '.cells[] | .cell_id' "$REGISTRY"); do
    ((progress++))
    cell_config=$(jq -r ".cells[] | select(.cell_id == $cell_id) | .config_path" "$REGISTRY")
    environment=$(jq -r ".cells[] | select(.cell_id == $cell_id) | .environment" "$REGISTRY")
    defence=$(jq -r ".cells[] | select(.cell_id == $cell_id) | .defence" "$REGISTRY")
    model=$(jq -r ".cells[] | select(.cell_id == $cell_id) | .model" "$REGISTRY")

    printf -v run_id "cell_%02d" "$cell_id"
    log_file="$LOG_DIR/${run_id}.log"

    echo -n "[${progress}/${total_cells}] $environment / $defence / $model ... "

    if python3 -m prompt_injection_eval.runner --config "$cell_config" > "$log_file" 2>&1; then
        echo "✓"
        ((passed++))
    else
        echo "✗"
        echo "  Log: $log_file"
        ((failed++))
    fi
done

echo ""
echo "=== Summary ==="
echo "Passed: $passed / $total_cells"
echo "Failed: $failed / $total_cells"
echo "Logs: $LOG_DIR"

if [ $failed -eq 0 ]; then
    echo ""
    echo "✓ All cells completed. Running aggregation..."
    python3 -m prompt_injection_eval.aggregation --results-dir results/dissertation
    exit 0
else
    echo ""
    echo "✗ Some cells failed. Check logs in $LOG_DIR"
    exit 1
fi
