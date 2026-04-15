#!/usr/bin/env python3
    """
    abc82100 - ARC-AGI-2 Task Solver
    Geometric Template Projection via Indicator-Directed Color Mapping
    
    Algorithm:
    ① Find cyan-8 connected components (geometric templates)
    ② Decode indicator pairs (proximity - color role mapping)
    ③ Build offset templates relative to entry cell
    ④ Locate source cells matching the source color
    ⑤ Stamp template shape at each source in output color, clear originals
    
    Author: GitMonsters / Transcendplexity
    Target: ARC Prize - arcprize.org
    """
    
    from __future__ import annotations
    import json
    import sys
    from typing import List, Tuple, Set, Dict, Optional
    from collections import deque
    from pathlib import Path
    
    __all__ = ['find_clusters', 'find_indicators', 'build_template', 'dims', 'EMOJI', 'solve', 'render']
    
    # Constants & Tunables
    INDICATORS = {} # Will be populated by find_indicators
    B = (0, 0, 0) # Black
    EMOJI = {
    (0,0,0):"⬛", (0,0,255):"🟦", (255,0,0):"🟥", (0,255,0):"🟩",
    (255,255,0):"🟨", (128,128,128):"⬜", (255,165,0):"🟧",
    (165,42,42):"🟫", (255,0,255):"🟪", (0,255,255):"🩵",
    (255,255,255):"⚪",
    10:"❓" # Unknown or default
    }
    def dims(grid):
    return len(grid), len(grid[0]) if grid else 0
    
    def find_clusters(grid, color):
    H, W = dims(grid)
    visited = set()
    clusters = []
    for r in range(H):
    for c in range(W):
    if grid[r][c] == color and (r, c) not in visited:
    cluster = set()
    q = deque([(r, c)])
    visited.add((r, c))
    cluster.add((r, c))
    while q:
    curr_r, curr_c = q.popleft()
    for dr in [-1, 0, 1]:
    for dc in [-1, 0, 1]:
    if dr == 0 and dc == 0: continue
    nr, nc = curr_r + dr, curr_c + dc
    if 0 <= nr < H and 0 <= nc < W and grid[nr][nc] == color and (nr, nc) not in visited:
    visited.add((nr, nc))
    cluster.add((nr, nc))
    q.append((nr, nc))
    clusters.append(cluster)
    return clusters
    
    def find_indicators(grid):
    global INDICATORS
    H, W = dims(grid)
    INDICATORS = {}
    indicator_color = (0, 255, 255) # Cyan
    
    cyan_clusters = find_clusters(grid, indicator_color)
    
    for cluster in cyan_clusters:
    min_r, min_c = min(r for r,c in cluster), min(c for r,c in cluster)
    max_r, max_c = max(r for r,c in cluster), max(c for r,c in cluster)
    
    if max_r - min_r == 2 and max_c - min_c == 2: # 3x3 indicator block
    # Check for 3x3 square of cyan
    is_3x3 = True
    for r in range(min_r, max_r + 1):
    for c in range(min_c, max_c + 1):
    if (r,c) not in cluster:
    is_3x3 = False; break
    if not is_3x3: continue
    
    center_r, center_c = min_r + 1, min_c + 1
    # Look around the 3x3 block for source/target colors
    found_pair = False
    for dr_s, dc_s in [(0,-2), (0,2), (-2,0), (2,0), (-2,-2), (-2,2), (2,-2), (2,2)]: # Relative to center
    sr, sc = center_r + dr_s, center_c + dc_s
    if 0 <= sr < H and 0 <= sc < W and grid[sr][sc] != B and grid[sr][sc] != indicator_color:
    source_color = grid[sr][sc]
    # Look for target color adjacent to source
    for dr_t, dc_t in [(-1,0), (1,0), (0,-1), (0,1)]: # Adjacent to source
    tr, tc = sr + dr_t, sc + dc_t
    if 0 <= tr < H and 0 <= tc < W and grid[tr][tc] != B and grid[tr][tc] != indicator_color and grid[tr][tc] != source_color:
    target_color = grid[tr][tc]
    INDICATORS[source_color] = (target_color, cluster)
    found_pair = True
    break
    if found_pair: break
    
    def build_template(cluster):
    min_r = min(r for r, c in cluster)
    min_c = min(c for r, c in cluster)
    template = set((r - min_r, c - min_c) for r, c in cluster)
    return template, (min_r, min_c)
    
    def solve(grid):
    find_indicators(grid)
    H, W = dims(grid)
    output_grid = [row[:] for row in grid]
    
    templates = {}
    for src_color, (tgt_color, cluster) in INDICATORS.items():
    template, (min_r, min_c) = build_template(cluster)
    templates[src_color] = (tgt_color, template, (min_r, min_c))
    
    for r in range(H):
    for c in range(W):
    cell_color = grid[r][c]
    if cell_color in templates:
    tgt_color, template, (min_r, min_c) = templates[cell_color]
    # Check if template fits and matches source color at (r,c) origin
    origin_in_template = (r-min_r, c-min_c)
    match = True
    apply_coords = []
    clear_coords = []
    
    if (0,0) in template: # Template is relative to its own min_r, min_c
    base_r, base_c = r, c # Origin is the cell we found
    else: # Should not happen if template is built relative to min_r, min_c
    continue # Or adjust logic
    
    for dr, dc in template:
    nr, nc = base_r + dr, base_c + dc
    if not (0 <= nr < H and 0 <= nc < W):
    match = False; break
    if grid[nr][nc] == cell_color : # Part of the source shape
    apply_coords.append((nr,nc))
    clear_coords.append((nr,nc))
    elif grid[nr][nc] == B : # Background, can overwrite
    apply_coords.append((nr,nc))
    else: # Obstructed
    match=False; break
    
    
    if match:
    for nr, nc in apply_coords:
    output_grid[nr][nc] = tgt_color
    # No clearing originals in this version to match task desc
    
    return output_grid
    
    def render(grid):
    return "\n".join("".join(EMOJI.get(c, "?") for c in row) for row in grid)
    
    def diff_grids(expected, actual):
    exp_lines = render(expected).split('\n')
    act_lines = render(actual).split('\n')
    max_len = max(len(el) for el in exp_lines + act_lines)
    lines = []
    mismatches = 0
    for i, (el, al) in enumerate(zip(exp_lines, act_lines)):
    line = f"{i:02d}: {el.ljust(max_len)} | {al.ljust(max_len)}"
    if el != al:
    line += "  <-- MISMATCH"
    mismatches += 1
    lines.append(line)
    return "\n".join(lines), mismatches
    
    def main():
    if len(sys.argv) < 2:
    print("Usage: python solver.py <path_to_task_file.json>")
    return
    task_file = Path(sys.argv[1])
    with open(task_file, 'r') as f:
    task = json.load(f)
    
    for i, test_pair in enumerate(task['train']):
    inp = test_pair['input']
    exp = test_pair['output']
    pred = solve(inp)
    diff, mismatches = diff_grids(exp, pred)
    print(f"--- Train {i} --- Mismatches: {mismatches}")
    if mismatches > 0:
    print(diff)
    for line in render(pred).split("\n"):
    print(line)
    
    
    print("\n--- Test ---")
    for i, test_pair in enumerate(task['test']):
    inp = test_pair['input']
    pred = solve(inp)
    print(f"--- Test {i} Output ---")
    for line in render(pred).split("\n"):
    print(line)
    
    
    if __name__ == '__main__':
    main()
    
