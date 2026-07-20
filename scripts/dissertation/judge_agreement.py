#!/usr/bin/env python3
"""Judge agreement analysis — Cohen's kappa and discrepancy report."""

import json
import argparse
from pathlib import Path
from collections import defaultdict
from statistics import mean, stdev


def cohens_kappa(determinist_labels: dict[str, bool], llm_labels: dict[str, bool]) -> float:
    """Calculate Cohen's kappa for binary classification agreement."""
    if not determinist_labels or not llm_labels:
        return None

    # Find common records
    common_ids = set(determinist_labels.keys()) & set(llm_labels.keys())
    if not common_ids:
        return None

    # Contingency table
    n = len(common_ids)
    n_both_true = sum(
        1
        for rid in common_ids
        if determinist_labels[rid] and llm_labels[rid]
    )
    n_both_false = sum(
        1
        for rid in common_ids
        if not determinist_labels[rid] and not llm_labels[rid]
    )
    n_agree = n_both_true + n_both_false

    # Observed agreement
    p_o = n_agree / n if n > 0 else 0.0

    # Expected agreement (marginal probabilities)
    p_det_true = sum(1 for v in determinist_labels.values() if v) / len(determinist_labels)
    p_llm_true = sum(1 for v in llm_labels.values() if v) / len(llm_labels)
    p_e = p_det_true * p_llm_true + (1 - p_det_true) * (1 - p_llm_true)

    # Cohen's kappa
    kappa = (p_o - p_e) / (1 - p_e) if p_e < 1.0 else 0.0

    return round(kappa, 4)


def judge_agreement_report(
    sample_path: Path,
    llm_labels_path: Path,
    output_path: Path | None = None,
) -> dict:
    """Compare deterministic vs LLM scoring and generate agreement report."""

    # Load sample records
    sample = {}
    with open(sample_path) as f:
        for line in f:
            record = json.loads(line)
            sample[record["run_id"]] = record

    # Load LLM labels
    with open(llm_labels_path) as f:
        llm_labels_raw = json.load(f)

    # Extract deterministic labels
    determinist_labels = {rid: sample[rid].get("attack_success", None) for rid in sample}

    # Extract LLM labels (handle errors)
    llm_labels_clean = {}
    for rid, label_data in llm_labels_raw.items():
        if rid in sample:
            llm_success = label_data.get("llm_judge_success")
            if llm_success is not None:
                llm_labels_clean[rid] = llm_success

    # Find common, scored records
    common_ids = set(determinist_labels.keys()) & set(llm_labels_clean.keys())
    common_ids = {rid for rid in common_ids if determinist_labels[rid] is not None}

    if not common_ids:
        print("No common, scored records found")
        return {}

    # Agreement statistics
    matches = sum(
        1
        for rid in common_ids
        if determinist_labels[rid] == llm_labels_clean[rid]
    )
    match_rate = matches / len(common_ids)
    kappa = cohens_kappa(determinist_labels, llm_labels_clean)

    # Discrepancies
    discrepancies = [
        {
            "run_id": rid,
            "task_id": sample[rid].get("task_id"),
            "attack_family": sample[rid].get("attack_family"),
            "deterministic": determinist_labels[rid],
            "llm": llm_labels_clean[rid],
            "llm_reasoning": llm_labels_raw[rid].get("llm_judge_reasoning", ""),
        }
        for rid in common_ids
        if determinist_labels[rid] != llm_labels_clean[rid]
    ]

    # Breakdown by family
    by_family = defaultdict(lambda: {"matches": 0, "total": 0})
    for rid in common_ids:
        family = sample[rid].get("attack_family", "unknown")
        by_family[family]["total"] += 1
        if determinist_labels[rid] == llm_labels_clean[rid]:
            by_family[family]["matches"] += 1

    family_agreement = {
        family: {
            "match_rate": round(stats["matches"] / stats["total"], 4),
            "matches": stats["matches"],
            "total": stats["total"],
        }
        for family, stats in sorted(by_family.items())
    }

    report = {
        "summary": {
            "records_scored": len(common_ids),
            "matches": matches,
            "disagreements": len(discrepancies),
            "overall_match_rate": round(match_rate, 4),
            "cohens_kappa": kappa,
            "kappa_interpretation": (
                "Poor" if kappa < 0.4
                else "Fair" if kappa < 0.6
                else "Moderate" if kappa < 0.75
                else "Substantial" if kappa < 0.9
                else "Almost perfect"
            ),
        },
        "by_attack_family": family_agreement,
        "discrepancies": discrepancies[:10],  # Top 10 for report
        "discrepancy_count": len(discrepancies),
    }

    # Write output
    if output_path:
        with open(output_path, "w") as f:
            json.dump(report, f, indent=2)
        print(f"Report written to {output_path}")

    return report


def print_report(report: dict) -> None:
    """Pretty-print judge agreement report."""
    if not report:
        print("No report to print")
        return

    summary = report["summary"]
    print("\n" + "=" * 80)
    print("JUDGE AGREEMENT ANALYSIS")
    print("=" * 80)
    print()
    print(f"Records scored: {summary['records_scored']}")
    print(f"Overall match rate: {summary['overall_match_rate']:.1%}")
    print(f"Cohen's kappa: {summary['cohens_kappa']:.4f} ({summary['kappa_interpretation']})")
    print()
    print("By attack family:")
    for family, stats in sorted(report["by_attack_family"].items()):
        print(f"  {family:30s} {stats['match_rate']:.1%} ({stats['matches']}/{stats['total']})")
    print()
    if report["discrepancies"]:
        print(f"Top discrepancies (of {report['discrepancy_count']} total):")
        for d in report["discrepancies"][:5]:
            print(f"  - {d['task_id']} / {d['attack_family']}: det={d['deterministic']} vs llm={d['llm']}")
            print(f"    LLM reasoning: {d['llm_reasoning'][:100]}...")
    print()


def main():
    parser = argparse.ArgumentParser(description="Judge agreement analysis")
    parser.add_argument("--sample", type=Path, required=True, help="Path to sampled records JSONL")
    parser.add_argument("--llm-labels", type=Path, required=True, help="Path to LLM labels JSON")
    parser.add_argument("--output", type=Path, required=True, help="Output path for report")

    args = parser.parse_args()

    report = judge_agreement_report(
        sample_path=args.sample,
        llm_labels_path=args.llm_labels,
        output_path=args.output,
    )

    print_report(report)


if __name__ == "__main__":
    main()
