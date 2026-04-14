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
    
    __all__ = ['find_clusters', 'find_indicators', 'build_template', 'dims', 'EMOJI', 'solve', 'render']
    
    # ──── Constants & Types ──────────────────────────────────────────────────
    
    INDICATORS = 5
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
    
    B = 0
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
        For each cluster, find the adjacent indicator pair.
        Closer cell → output_color, farther → source_color.
        """
        H, W = dims(grid)
        all_cyan = set()
        for cl in clusters:
            all_cyan.update(cl)
    
        # Find non-zero, non-8 cells adjacent to any cluster cell
        indicators = []
        used: Set[Point] = set()
    
        for ci, cluster in enumerate(clusters):
            # Cells in the 8-neighborhood of the cluster
            border: Set[Point] = set()
            for cr, cc in cluster:
                for nr, nc in adj8(cr, cc, H, W):
                    if (nr, nc) not in cluster and grid[nr][nc] not in (0, 8):
                        border.add((nr, nc))
    
            # Find pairs: two different-colored cells where one is in border
            best_pair = None
            best_dist = 999
    
            for p1 in border:
                if p1 in used:
                    continue
                c1 = grid[p1[0]][p1[1]]
                # Look for partner adjacent to p1 with different color
                for p2 in adj4(p1[0], p1[1], H, W):
                    if p2 in used or p2 in all_cyan:
                        continue
                    c2 = grid[p2[0]][p2[1]]
                    if c2 == 0 or c2 == 8 or c2 == c1:
                        continue
    
                    d1 = min_dist(p1, cluster)
                    d2 = min_dist(p2, cluster)
                    total = d1 + d2
    
                    if total < best_dist:
                        best_dist = total
                        if d1 <= d2:
                            best_pair = (p1, c1, p2, c2)  # p1 closer
                        else:
                            best_pair = (p2, c2, p1, c1)  # p2 closer
    
            if best_pair:
                closer, out_color, farther, src_color = best_pair
                used.add(closer)
                used.add(farther)
    
                # Entry = cyan cell nearest to the closer indicator
                entry = min(cluster, key=lambda p: abs(p[0] - closer[0]) + abs(p[1] - closer[1]))
    
                indicators.append({
                    "cluster_idx": ci,
                    "output_color": out_color,
                    "source_color": src_color,
                    "entry": entry,
                    "indicator_cells": {closer, farther},
                })
    
        return indicators
    
    
    # ──── ③ Template Building ────────────────────────────────────────────────
    
    def build_template(cluster: Set[Point], entry: Point) -> List[Point]:
        """Compute template as offsets relative to entry cell."""
        er, ec = entry
        return [(r - er, c - ec) for r, c in cluster]
    
    
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
    
        # Collect all cells to clear
        clear: Set[Point] = set()
        for cl in clusters:
            clear.update(cl)
    
        for ind in indicators:
            cluster = clusters[ind["cluster_idx"]]
            template = build_template(cluster, ind["entry"])
            clear.update(ind["indicator_cells"])
    
            sources = find_sources(input_grid, ind["source_color"], ind["indicator_cells"])
            clear.update(sources)
    
            # Stamp template at each source position
            for sr, sc in sources:
                for dr, dc in template:
                    nr, nc = sr + dr, sc + dc
                    if 0 <= nr < H and 0 <= nc < W:
                        output[nr][nc] = ind["output_color"]
    
        # Clear template, indicator, and source cells
        for r, c in clear:
            if 0 <= r < H and 0 <= c < W:
                output[r][c] = 0
    
        return output
    
    
    # ──── Visualization ─────────────────────────────────────────────────────
    
    def render(grid: Grid) -> str:
        return "
".join("".join(EMOJI.get(c, "?") for c in row) for row in grid)
    
    
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
        return "
".join(lines), mismatches
    
    
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
                for line in render(pred).split("
"):
                    print(f"    {line}")
                print()
    
        pct = 100 * correct / total if total else 0
        bar = "█" * correct + "░" * (total - correct)
        print()
        print(f"  Score: {correct}/{total} ({pct:.0f}%)  [{bar}]")
        print()
    
    
    if __name__ == "__main__":
        main()
    
