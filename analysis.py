#!/usr/bin/env python3
"""
abc82100 — Structural Analysis

Extracts and visualizes the geometric structure of the task:
cluster shapes, indicator topology, template morphology.
"""

from __future__ import annotations
import json
from pathlib import Path
from solver import find_clusters, find_indicators, build_template, dims, EMOJI


def analyze(task_path: str = "task.json"):
    task = json.loads(Path(task_path).read_text())

    print()
    print("  ╔══════════════════════════════════════════════╗")
    print("  ║     abc82100 — Structural Analysis            ║")
    print("  ╚══════════════════════════════════════════════╝")
    print()

    for idx, example in enumerate(task["train"] + task["test"]):
        grid = example["input"]
        H, W = dims(grid)
        is_test = idx >= len(task["train"])
        label = f"Test  {idx - len(task['train'])}" if is_test else f"Train {idx}"

        clusters = find_clusters(grid, 8)
        indicators = find_indicators(grid, clusters)

        print(f"  ── {label} ({H}×{W}) ──")
        print()

        for i, cl in enumerate(clusters):
            # Find bounding box
            rows = [r for r, c in cl]
            cols = [c for r, c in cl]
            min_r, max_r = min(rows), max(rows)
            min_c, max_c = min(cols), max(cols)
            shape_h = max_r - min_r + 1
            shape_w = max_c - min_c + 1

            # Render shape as mini-grid
            print(f"  Cluster {i}: {len(cl)} cells ({shape_h}×{shape_w})")
            for r in range(min_r, max_r + 1):
                row = ""
                for c in range(min_c, max_c + 1):
                    if (r, c) in cl:
                        row += "🔷"
                    else:
                        row += "  "
                print(f"    {row}")

            # Show indicator for this cluster
            matching = [ind for ind in indicators if ind["cluster_idx"] == i]
            for ind in matching:
                src = ind["source_color"]
                out = ind["output_color"]
                print(f"    Rule: {EMOJI[src]}({src}) → {EMOJI[out]}({out})")
                print(f"    Entry: {ind['entry']}")
                tpl = build_template(cl, ind["entry"])
                print(f"    Template offsets: {sorted(tpl)}")

            print()

    print("  ════════════════════════════════════════════════")
    print()


if __name__ == "__main__":
    analyze()
