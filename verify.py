#!/usr/bin/env python3
"""
abc82100 — Verification & Deep Analysis

Runs the solver against all training + test examples and produces
a detailed report including cluster detection, indicator decoding,
color statistics, and cell-level accuracy breakdown.
"""

from __future__ import annotations
import json
import sys
from pathlib import Path
from collections import Counter
from solver import solve, find_clusters, find_indicators, dims, EMOJI, render


def analyze_task(task: dict) -> None:
    """Deep analysis of the abc82100 task structure."""

    print()
    print("  ╔══════════════════════════════════════════════╗")
    print("  ║     abc82100 — Deep Task Analysis             ║")
    print("  ╚══════════════════════════════════════════════╝")
    print()

    all_examples = [(f"Train {i}", ex) for i, ex in enumerate(task["train"])]
    all_examples += [(f"Test  {i}", ex) for i, ex in enumerate(task["test"])]

    for label, ex in all_examples:
        grid = ex["input"]
        H, W = dims(grid)

        # Color census
        color_count: Counter = Counter()
        for row in grid:
            for c in row:
                color_count[c] += 1

        # Cluster detection
        clusters = find_clusters(grid, 8)
        indicators = find_indicators(grid, clusters)

        print(f"  ┌─ {label} ({H}×{W}) ─────────────────────")
        print(f"  │  Cells: {H*W}  │  Non-zero: {sum(v for k, v in color_count.items() if k != 0)}")
        print(f"  │  Cyan clusters: {len(clusters)}")
        for i, cl in enumerate(clusters):
            print(f"  │    Cluster {i}: {len(cl)} cells → {sorted(cl)[:4]}{'...' if len(cl) > 4 else ''}")
        print(f"  │  Indicator pairs: {len(indicators)}")
        for ind in indicators:
            oc = ind['output_color']
            sc = ind['source_color']
            print(f"  │    {EMOJI[sc]} ({sc}) → {EMOJI[oc]} ({oc})  entry={ind['entry']}")
        print(f"  │  Color palette: {', '.join(f'{EMOJI[c]}×{n}' for c, n in sorted(color_count.items()) if c != 0)}")

        # Solve and compare
        if "output" in ex:
            pred = solve(grid)
            expected = ex["output"]
            cell_correct = sum(
                1 for r in range(H) for c in range(W)
                if pred[r][c] == expected[r][c]
            )
            cell_total = H * W
            print(f"  │  Accuracy: {cell_correct}/{cell_total} ({100*cell_correct/cell_total:.1f}%)")

        print(f"  └────────────────────────────────────────")
        print()


def main():
    task_path = Path("task.json")
    if not task_path.exists():
        print("  ✗ task.json not found")
        sys.exit(1)

    task = json.loads(task_path.read_text())
    analyze_task(task)


if __name__ == "__main__":
    main()
