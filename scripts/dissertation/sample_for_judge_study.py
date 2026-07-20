#!/usr/bin/env python3
"""Sample records for judge-robustness mini-study.

Stratified sampling: ensures representation across attack families and defence conditions.
"""

import json
import argparse
from pathlib import Path
from collections import defaultdict
import random


def sample_for_judge_study(
    runs_jsonl_path: Path,
    sample_size: int = 50,
    stratify_by: list[str] | None = None,
    output_path: Path | None = None,
    seed: int = 42,
) -> list[dict]:
    """Sample records stratified by attack family and defence condition.

    Args:
        runs_jsonl_path: Path to raw runs.jsonl file
        sample_size: Total number of records to sample (default 50)
        stratify_by: Fields to stratify on (default: ["attack_family", "defence_condition"])
        output_path: Path to write sampled records (optional)
        seed: Random seed for reproducibility

    Returns:
        List of sampled records
    """
    if stratify_by is None:
        stratify_by = ["attack_family", "defence_condition"]

    random.seed(seed)

    # Load all attack records
    attack_records = []
    with open(runs_jsonl_path) as f:
        for line in f:
            record = json.loads(line)
            if record.get("benign_or_attack") == "attack":
                attack_records.append(record)

    # Group by stratification fields
    strata: dict[tuple, list[dict]] = defaultdict(list)
    for record in attack_records:
        key = tuple(record.get(field, "unknown") for field in stratify_by)
        strata[key].append(record)

    # Proportional allocation per stratum
    sampled = []
    for stratum_key, records in sorted(strata.items()):
        # Allocate sample_size proportionally to stratum size
        stratum_sample_size = max(1, round(len(records) / len(attack_records) * sample_size))
        stratum_sample = random.sample(records, min(stratum_sample_size, len(records)))
        sampled.extend(stratum_sample)

    # Trim to exact sample size if needed
    sampled = random.sample(sampled, min(len(sampled), sample_size))

    # Write output
    if output_path:
        with open(output_path, "w") as f:
            for record in sampled:
                f.write(json.dumps(record) + "\n")
        print(f"Sampled {len(sampled)} records to {output_path}")
        print(f"Stratification: {stratify_by}")
        print(f"Strata coverage: {len(strata)} unique combinations")

    return sampled


def main():
    parser = argparse.ArgumentParser(
        description="Sample records for judge-robustness mini-study"
    )
    parser.add_argument("--runs-jsonl", type=Path, required=True, help="Path to runs.jsonl")
    parser.add_argument("--sample-size", type=int, default=50, help="Number of records to sample")
    parser.add_argument(
        "--stratify-by",
        type=str,
        default="attack_family,defence_condition",
        help="Comma-separated fields to stratify on",
    )
    parser.add_argument("--output", type=Path, required=True, help="Output path for sample")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")

    args = parser.parse_args()

    stratify_by = args.stratify_by.split(",")
    sample_for_judge_study(
        runs_jsonl_path=args.runs_jsonl,
        sample_size=args.sample_size,
        stratify_by=stratify_by,
        output_path=args.output,
        seed=args.seed,
    )


if __name__ == "__main__":
    main()
