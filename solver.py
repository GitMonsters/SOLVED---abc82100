#!/usr/bin/env python3
"""
abc82100 — ARC-AGI-2 Task Solver
Geometric Template Projection via Indicator-Directed Color Mapping

Algorithm:
  ① Find cyan-8 connected components (geometric templates)
  ② Decode indicator pairs (proximity → color role mapping)
  ③ Build offset templates relative to entry cell
  ④ Locate source cells matching the source color
  ⑤ Stamp template shape at each source in output color, clear originals

Author: GitMonsters / Transcendplexity
Target: ARC Prize — arcprize.org
"""

from __future__ import annotations
import json
import sys
from typing import List, Tuple, Set, Dict, Optional
from collections import deque
from pathlib import Path


# ──── Types ──────────────────────────────────────────────────────────────

Grid = List[List[int]]
Point = Tuple[int, int]

EMOJI = {
    0: "⬛", 1: "🔵", 2: "🔴", 3: "🟢", 4: "🟨",
    5: "⬜", 6: "🟪", 7: "🟧", 8: "🔷", 9: "🟤",
}


# ──── Grid Utilities ─────────────────────────────────────────────────────

def dims(g: Grid) -> Tuple[int, int]:
    return len(g), len(g[0])


def copy_grid(g: Grid) -> Grid:
    return [row[:] for row in g]


def adj8(r: int, c: int, H: int, W: int) -> List[Point]:
    """8-connected neighbors."""
    return [
        (r + dr, c + dc)
        for dr in (-1, 0, 1) for dc in (-1, 0, 1)
        if (dr or dc) and 0 <= r + dr < H and 0 <= c + dc < W
    ]


def adj4(r: int, c: int, H: int, W: int) -> List[Point]:
    """4-connected neighbors."""
    return [
        (r + dr, c + dc)
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]
        if 0 <= r + dr < H and 0 <= c + dc < W
    ]


# ──── ① Cluster Detection ───────────────────────────────────────────────

def find_clusters(grid: Grid, color: int = 8) -> List[Set[Point]]:
    """BFS flood-fill to find 8-connected components of given color."""
    H, W = dims(grid)
    seen: Set[Point] = set()
    clusters = []

    for r in range(H):
        for c in range(W):
            if grid[r][c] == color and (r, c) not in seen:
                cluster: Set[Point] = set()
                q = deque([(r, c)])
                seen.add((r, c))
                while q:
                    cr, cc = q.popleft()
                    cluster.add((cr, cc))
                    for nr, nc in adj8(cr, cc, H, W):
                        if (nr, nc) not in seen and grid[nr][nc] == color:
                            seen.add((nr, nc))
                            q.append((nr, nc))
                clusters.append(cluster)

    return clusters


# ──── ② Indicator Pair Decoding ──────────────────────────────────────────

def min_dist(p: Point, cluster: Set[Point]) -> int:
    """Manhattan distance from point to nearest cell in cluster."""
    return min(abs(p[0] - cr) + abs(p[1] - cc) for cr, cc in cluster)


def find_indicators(
    grid: Grid, clusters: List[Set[Point]]
) -> List[Dict]:
    """
    Find indicator pairs by searching ALL adjacent different-colored
    non-zero non-8 cell pairs and assigning each to its nearest cluster.
    Closer cell → output_color, farther → source_color.
    """
    H, W = dims(grid)
    all_cyan: Set[Point] = set()
    for cl in clusters:
        all_cyan.update(cl)

    # Candidate cells: non-zero, non-cyan, not in any cluster
    candidates: Dict[Point, int] = {}
    for r in range(H):
        for c in range(W):
            if grid[r][c] not in (0, 8) and (r, c) not in all_cyan:
                candidates[(r, c)] = grid[r][c]

    # Find all 4-adjacent pairs of different colors
    pairs = []
    seen_pairs: Set[tuple] = set()
    for (r, c), c1 in candidates.items():
        for nr, nc in adj4(r, c, H, W):
            if (nr, nc) in candidates:
                c2 = candidates[(nr, nc)]
                if c2 != c1:
                    pair_key = tuple(sorted([(r, c), (nr, nc)]))
                    if pair_key not in seen_pairs:
                        seen_pairs.add(pair_key)
                        pairs.append(((r, c), c1, (nr, nc), c2))

    # Sort by distance to nearest cluster (closest first)
    def pair_min_dist(pair):
        p1, _, p2, _ = pair
        return min(
            min(min_dist(p1, cl) for cl in clusters),
            min(min_dist(p2, cl) for cl in clusters),
        )
    pairs.sort(key=pair_min_dist)

    indicators = []
    used: Set[Point] = set()
    used_clusters: Set[int] = set()

    for p1, c1, p2, c2 in pairs:
        if p1 in used or p2 in used:
            continue

        # Assign to nearest available cluster
        best_ci: Optional[int] = None
        best_d = 999
        for ci, cl in enumerate(clusters):
            if ci in used_clusters:
                continue
            d = min(min_dist(p1, cl), min_dist(p2, cl))
            if d < best_d:
                best_d, best_ci = d, ci

        if best_ci is None:
            continue

        cluster = clusters[best_ci]
        d1 = min_dist(p1, cluster)
        d2 = min_dist(p2, cluster)

        if d1 <= d2:
            closer, out_color, farther, src_color = p1, c1, p2, c2
        else:
            closer, out_color, farther, src_color = p2, c2, p1, c1

        used.update([p1, p2])
        used_clusters.add(best_ci)

        indicators.append({
            "cluster_idx": best_ci,
            "output_color": out_color,
            "source_color": src_color,
            "indicator_cells": {closer, farther},
            "closer": closer,
        })

    return indicators


# ──── ③ Template Building ────────────────────────────────────────────────

def compute_reference(closer: Point, cluster: Set[Point]) -> Point:
    """Reference point = 8-neighbor of closer indicator nearest to cluster centroid."""
    cr = sum(r for r, c in cluster) / len(cluster)
    cc = sum(c for r, c in cluster) / len(cluster)
    ir, ic = closer
    candidates = [(ir + dr, ic + dc) for dr in (-1, 0, 1) for dc in (-1, 0, 1) if dr or dc]
    return min(candidates, key=lambda p: abs(p[0] - cr) + abs(p[1] - cc))


def build_template(cluster: Set[Point], reference: Point) -> List[Point]:
    """Compute template as offsets relative to reference point."""
    rr, rc = reference
    return [(r - rr, c - rc) for r, c in cluster]


# ──── ④ Source Finding ───────────────────────────────────────────────────

def find_sources(grid: Grid, color: int, exclude: Set[Point]) -> List[Point]:
    """All cells of given color not in exclude set."""
    H, W = dims(grid)
    return [
        (r, c) for r in range(H) for c in range(W)
        if grid[r][c] == color and (r, c) not in exclude
    ]


# ──── ⑤ Stamp & Compose ─────────────────────────────────────────────────

def solve(input_grid: Grid) -> Grid:
    """
    Main solver: Template Stamping via Indicator-Directed Projection.

        INPUT → clusters → indicators → templates → sources → stamp → OUTPUT
    """
    H, W = dims(input_grid)
    output = copy_grid(input_grid)

    clusters = find_clusters(input_grid, color=8)
    indicators = find_indicators(input_grid, clusters)

    # Collect all cells to clear (clusters + indicators)
    clear: Set[Point] = set()
    for cl in clusters:
        clear.update(cl)

    all_ind_cells: Set[Point] = set()
    for ind in indicators:
        all_ind_cells.update(ind["indicator_cells"])
    clear.update(all_ind_cells)

    # Exclude clusters + indicators when finding sources
    exclude = set(clear)

    # Build stamp operations: find templates, sources, and colors
    stamp_ops = []
    for ind in indicators:
        cluster = clusters[ind["cluster_idx"]]
        reference = compute_reference(ind["closer"], cluster)
        template = build_template(cluster, reference)

        sources = find_sources(input_grid, ind["source_color"], exclude)
        clear.update(sources)
        stamp_ops.append((sources, template, ind["output_color"]))

    # Step 1: Clear all originals (clusters, indicators, sources)
    for r, c in clear:
        if 0 <= r < H and 0 <= c < W:
            output[r][c] = 0

    # Step 2: Stamp templates (overwrites cleared cells where needed)
    for sources, template, out_color in stamp_ops:
        for sr, sc in sources:
            for dr, dc in template:
                nr, nc = sr + dr, sc + dc
                if 0 <= nr < H and 0 <= nc < W:
                    output[nr][nc] = out_color

    return output


# ──── Visualization ─────────────────────────────────────────────────────

def render(grid: Grid) -> str:
    return "\n".join("".join(EMOJI.get(c, "?") for c in row) for row in grid)


def diff_grids(expected: Grid, actual: Grid) -> str:
    """Show side-by-side diff with markers for mismatches."""
    H, W = dims(expected)
    lines = []
    mismatches = 0
    for r in range(H):
        exp_row = "".join(EMOJI.get(expected[r][c], "?") for c in range(W))
        act_row = "".join(EMOJI.get(actual[r][c], "?") for c in range(W))
        match = expected[r] == actual[r]
        marker = "  ✓" if match else "  ✗"
        if not match:
            mismatches += sum(1 for c in range(W) if expected[r][c] != actual[r][c])
        lines.append(f"  {exp_row}  │  {act_row}{marker}")
    return "\n".join(lines), mismatches


# ──── CLI Entry Point ───────────────────────────────────────────────────

def main():
    visual = "--visual" in sys.argv
    task_path = Path("task.json")

    if not task_path.exists():
        print("  ✗ task.json not found — run from the repo root")
        sys.exit(1)

    task = json.loads(task_path.read_text())

    print()
    print("  ╔══════════════════════════════════════════════╗")
    print("  ║     abc82100 — Geometric Template Solver      ║")
    print("  ╚══════════════════════════════════════════════╝")
    print()

    total, correct = 0, 0

    for i, ex in enumerate(task["train"]):
        pred = solve(ex["input"])
        match = pred == ex["output"]
        total += 1
        correct += int(match)
        H, W = dims(pred)
        status = "✅" if match else "❌"
        print(f"  {status} Train {i}  ({H:>2}×{W:<2})")

        if visual and not match:
            diff, n = diff_grids(ex["output"], pred)
            print(f"     Expected  │  Got  ({n} mismatched cells)")
            print(diff)
            print()

    for i, ex in enumerate(task["test"]):
        pred = solve(ex["input"])
        H, W = dims(pred)
        if "output" in ex:
            match = pred == ex["output"]
            total += 1
            correct += int(match)
            status = "✅" if match else "❌"
        else:
            status = "🔮"
        print(f"  {status} Test  {i}  ({H:>2}×{W:<2})")

        if visual:
            print()
            print("  Predicted:")
            for line in render(pred).split("\n"):
                print(f"    {line}")
            print()

    pct = 100 * correct / total if total else 0
    bar = "█" * correct + "░" * (total - correct)
    print()
    print(f"  Score: {correct}/{total} ({pct:.0f}%)  [{bar}]")
    print()


if __name__ == "__main__":
    main()
