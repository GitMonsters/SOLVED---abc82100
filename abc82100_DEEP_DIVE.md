<div align="center">


Uploading bigBang.mp4…



https://github.com/user-attachments/assets/125ac24f-3841-489a-a00c-f82bf38daa59


<br>

```
 ╔═══════════════════════════════════════════════════════════════╗
 ║                                                               ║
 ║     █████╗ ██████╗  ██████╗ █████╗ ██████╗  ██╗ ██████╗  ██████╗  ║
 ║    ██╔══██╗██╔══██╗██╔════╝██╔══██╗╚════██╗███║██╔═████╗██╔═████╗ ║
 ║    ███████║██████╔╝██║     ╚█████╔╝ █████╔╝╚██║██║██╔██║██║██╔██║ ║
 ║    ██╔══██║██╔══██╗██║     ██╔══██╗██╔═══╝  ██║████╔╝██║████╔╝██║ ║
 ║    ██║  ██║██████╔╝╚██████╗╚█████╔╝███████╗ ██║╚██████╔╝╚██████╔╝ ║
 ║    ╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚════╝ ╚══════╝ ╚═╝ ╚═════╝  ╚═════╝ ║
 ║                                                               ║
 ║           S O L V E D   ·   A R C - A G I - 2                ║
 ╚═══════════════════════════════════════════════════════════════╝
```

<br>

**Geometric Template Projection via Indicator-Directed Color Mapping**

*A complete analysis and solution for one of the hardest tasks in the ARC-AGI-2 evaluation benchmark*

<br>

[![ARC Prize](https://img.shields.io/badge/ARC_Prize-$1M_Challenge-gold?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZmlsbD0iI2ZmZiIgZD0iTTEyIDJMMiAyMmgyMEwxMiAyeiIvPjwvc3ZnPg==)](https://arcprize.org)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Task](https://img.shields.io/badge/Task_ID-abc82100-7FDBFF?style=for-the-badge)]()
[![Grid](https://img.shields.io/badge/Grid-20×20-FF851B?style=for-the-badge)]()
[![License](https://img.shields.io/badge/License-MIT-2ECC40?style=for-the-badge)](LICENSE)

<br>

---

</div>

<br>

## 🧬 The Task

> **abc82100** is an ARC-AGI-2 evaluation task requiring the solver to decode a visual programming language embedded in colored grids — where **cyan shapes are templates**, **colored pairs are mapping rules**, and **isolated cells are projection targets**.

<br>

### Training Example 0 — `5×5`

<table>
<tr>
<td align="center"><b>INPUT</b></td>
<td align="center" width="60">→</td>
<td align="center"><b>OUTPUT</b></td>
</tr>
<tr>
<td>

```
🔵🔴🔷🔷🔷
⬛⬛⬛⬛🔵
⬛⬛⬛🔵⬛
⬛⬛⬛🔵⬛
⬛⬛⬛⬛🔵
```

</td>
<td align="center"><h2>➜</h2></td>
<td>

```
⬛⬛⬛⬛⬛
⬛⬛⬛⬛🔴
⬛⬛⬛🔴🔴
⬛⬛⬛🔴🔴
⬛⬛⬛⬛🔴
```

</td>
</tr>
</table>

<details>
<summary><b>📐 Training Example 3 — 8×8 (Color Swap)</b></summary>

<br>

<table>
<tr>
<td align="center"><b>INPUT</b></td>
<td align="center" width="60">→</td>
<td align="center"><b>OUTPUT</b></td>
</tr>
<tr>
<td>

```
🔵🔵🔵🔵🔵🔴⬛⬛
⬛⬛⬛⬛⬛🔴⬛⬛
⬛⬛⬛⬛⬛🔴⬛⬛
⬛🔴🔵🔷⬛🔴⬛⬛
⬛⬛⬛⬛⬛🔴⬛⬛
⬛⬛🔷⬛⬛🔴⬛⬛
⬛⬛🔴⬛⬛🔴⬛⬛
⬛⬛🔵⬛⬛🔴⬛⬛
```

</td>
<td align="center"><h2>➜</h2></td>
<td>

```
🔴🔴🔴🔴🔴🔵⬛⬛
⬛⬛⬛⬛⬛🔵⬛⬛
⬛⬛⬛⬛⬛🔵⬛⬛
⬛⬛⬛⬛⬛🔵⬛⬛
⬛⬛⬛⬛⬛🔵⬛⬛
⬛⬛⬛⬛⬛🔵⬛⬛
⬛⬛⬛⬛⬛🔵⬛⬛
⬛⬛⬛⬛⬛🔵⬛⬛
```

</td>
</tr>
</table>

</details>

<details>
<summary><b>🎯 Test Challenge — 20×20 (Full Complexity)</b></summary>

<br>

<table>
<tr><td align="center"><b>INPUT — 20×20</b></td></tr>
<tr><td>

```
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛🟪⬛⬛
🔴⬛⬛🔷⬛⬛⬛🟪⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛🟪
⬛🟨🔵🔷⬛⬛⬛⬛⬛⬛🔵⬛⬛⬛⬛⬛⬛⬛⬛⬛
⬛⬛⬛🔷⬛⬛⬛⬛⬛⬛⬛⬛⬛⬜⬛⬛⬛⬛⬛⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
⬛⬛⬛⬛🔷⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛🟨⬛⬛
⬛🔴🟨🔷⬛🔷⬛⬛⬛⬛⬛🔴⬛⬛⬛⬛⬛⬛⬛⬛
⬛⬛⬛⬛🔷⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
⬛⬛⬛⬛⬛⬛🔴⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬜⬛
⬛⬛⬛⬛🔷⬛⬛⬛⬛⬛⬛⬛⬛🟨⬛⬛⬛⬛⬛⬛
⬛⬜🟧🔷🔷⬛⬛⬛⬛⬜⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
⬛⬛⬛⬛🔷⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛🔴⬛⬛⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
⬛🔴⬛⬛⬛🔴⬛⬛⬛⬛⬛⬛⬛🔴⬛⬛⬛⬛⬛🟪
⬛⬛⬛⬛⬛⬛⬛⬛⬛🟨⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
⬛⬛⬜⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛🟨⬛⬛🟪⬛⬛⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
⬜⬛⬛⬛⬛⬛⬛⬛⬛🟪⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
```

</td></tr>
</table>

<table>
<tr><td align="center"><b>EXPECTED OUTPUT — 20×20</b></td></tr>
<tr><td>

```
⬛🟨⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛🟪⬛⬛
🟨⬛🟨⬛⬛⬛⬛🟪⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛🟪
⬛🟨⬛⬛⬛⬛⬛⬛⬛⬛🔵⬛⬛⬛🟧⬛⬛⬛⬛⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛🟧🟧⬛⬛⬛⬛⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛🟧⬛⬛🔵⬛⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛🟨⬛⬛⬛⬛🔵⬛⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛🟨⬛🟨⬛⬛⬛🔵⬛⬛
⬛⬛⬛⬛⬛⬛⬛🟨⬛⬛⬛⬛🟨⬛⬛⬛⬛⬛⬛🟧
⬛⬛⬛⬛⬛⬛🟨⬛🟨⬛⬛⬛⬛🔵⬛⬛⬛⬛🟧🟧
⬛⬛⬛⬛⬛⬛⬛🟨⬛⬛🟧⬛⬛🔵⬛⬛⬛⬛⬛🟧
⬛⬛⬛⬛⬛⬛⬛⬛⬛🟧🟧⬛⬛🔵⬛⬛⬛⬛⬛⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛🟧⬛⬛⬛⬛⬛⬛🟨⬛⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛🟨⬛🟨⬛
⬛⬛🟨⬛⬛⬛🟨⬛⬛⬛⬛⬛⬛⬛🟨⬛⬛🟨⬛⬛
⬛🟨⬛🟨⬛🟨⬛🟨⬛🔵⬛⬛⬛🟨⬛🟨⬛⬛⬛🟪
⬛⬛🟨🟧⬛⬛🟨⬛⬛🔵⬛⬛⬛⬛🟨⬛⬛⬛⬛⬛
⬛⬛🟧🟧⬛⬛⬛⬛⬛🔵⬛⬛⬛🔵⬛⬛⬛⬛⬛⬛
⬛⬛⬛🟧⬛⬛⬛⬛⬛⬛⬛⬛⬛🔵⬛⬛🟪⬛⬛⬛
⬛🟧⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛🔵⬛⬛⬛⬛⬛⬛
🟧🟧⬛⬛⬛⬛⬛⬛⬛🟪⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
```

</td></tr>
</table>

</details>

<br>

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    abc82100 Solver Pipeline                      │
│                                                                 │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐    │
│  │  DETECT   │──▶│  DECODE   │──▶│  BUILD   │──▶│  STAMP   │    │
│  │ Clusters  │   │ Indicators│   │ Templates │   │ Patterns │    │
│  └──────────┘   └──────────┘   └──────────┘   └──────────┘    │
│       │              │              │              │             │
│   8-connected    color pairs    offset maps    projection       │
│   flood fill     proximity      relative to    at each          │
│   on cyan(8)     ordering       entry cell     source cell      │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                    FINAL COMPOSE                          │   │
│  │  Clear cyan · Clear indicators · Clear sources · Overlay  │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

<br>

### The Visual Language

The task encodes a **geometric programming language** in colored grids:

| Symbol | Role | Description |
|:------:|:----:|:------------|
| 🔷 | **Template** | Cyan (8) cells form connected shapes — the geometric stencil |
| 🔴🟨 | **Indicator Pair** | Two adjacent cells of different colors near a template define the color mapping |
| 🔵 | **Source Cell** | Isolated cells matching the source color — projection targets |
| ⬛ | **Canvas** | Background — cleared and restamped in the output |

<br>

### Algorithm — 5 Steps

```python
def solve(grid):
    # ① DETECT — Find all cyan-8 connected components (8-connectivity)
    templates = find_cyan_clusters(grid)
    
    # ② DECODE — For each template, find the indicator pair
    #    The cell CLOSER to cyan → output color
    #    The cell FARTHER from cyan → source color  
    rules = decode_indicator_pairs(grid, templates)
    
    # ③ BUILD — Compute template shape as offsets from entry cell
    #    Entry = the cyan cell nearest to the indicator
    shapes = build_offset_templates(templates, rules)
    
    # ④ FIND — Locate all source-colored cells (excluding indicators)
    sources = find_source_cells(grid, rules)
    
    # ⑤ STAMP — Project template at each source position in output color
    output = stamp_and_clear(grid, shapes, sources, rules)
    
    return output
```

<br>

---

## 🔬 Deep Analysis

### Template Morphology

The task uses three distinct template geometries across training examples:

| Example | Grid | Template Shape | Template Cells | Complexity |
|:-------:|:----:|:--------------|:--------------:|:----------:|
| Train 0 | 5×5 | Horizontal line | 3 | ●○○○○ |
| Train 1 | 15×15 | Diamond / V-shape | 3 per cluster (×4) | ●●●○○ |
| Train 2 | 20×20 | Diamond / V-shape | 7 per cluster (×2) | ●●●●○ |
| Train 3 | 8×8 | Single point | 1 per cluster (×2) | ●○○○○ |
| **Test** | **20×20** | **Mixed: line + diamond** | **3–5 per cluster** | **●●●●●** |

### Scaling Properties

```
Grid Size vs. Number of Rules:
  
  5×5  ·  1 rule   │ █
  8×8  ·  2 rules  │ ██
 15×15 ·  4 rules  │ ████
 20×20 ·  5 rules  │ █████     ← Each rule operates independently
 20×20 ·  6 rules  │ ██████    ← Test challenge
```

### Color Distribution Analysis

<table>
<tr>
<td>

**Input Palette**
| Color | Symbol | Count | Role |
|:-----:|:------:|:-----:|:----:|
| 0 | ⬛ | ~90% | Background |
| 8 | 🔷 | ~3% | Template |
| 1-7 | 🔵🔴🟨… | ~7% | Data |

</td>
<td>

**Output Palette**
| Color | Symbol | Count | Role |
|:-----:|:------:|:-----:|:----:|
| 0 | ⬛ | ~85% | Background |
| 8 | — | 0% | Removed |
| 1-7 | 🔵🔴🟨… | ~15% | Projected |

</td>
</tr>
</table>

<br>

---

## 🚀 Quick Start

```bash
# Clone
git clone https://github.com/GitMonsters/SOLVED---abc82100.git
cd SOLVED---abc82100

# Run analysis
python3 solver.py

# Run with visualization
python3 solver.py --visual

# Verify against all examples
python3 verify.py
```

<br>

---

## 📁 Repository Structure

```
SOLVED---abc82100/
├── README.md              ← You are here
├── solver.py              ← Core solver — template stamping algorithm
├── verify.py              ← Automated verification against ground truth
├── task.json              ← Official ARC-AGI-2 task data (train + test)
├── analysis.py            ← Deep analysis: cluster detection, color stats
└── LICENSE                ← MIT License
```

<br>

---

## 🧠 Key Insights

<table>
<tr>
<td width="50%">

### 💡 What Makes This Hard

- **Multi-rule**: Up to 6 independent transformation rules per grid
- **Variable geometry**: Templates range from single points to 7-cell diamonds
- **Proximity semantics**: Color roles determined by spatial distance to cyan
- **Scale invariance**: Same logic applies from 5×5 to 20×20
- **Interference**: Multiple stamped patterns can overlap

</td>
<td>

### 🏆 What Makes This Solvable

- **Consistent encoding**: Cyan always = template, always removed in output
- **Local rules**: Each template + indicator defines a self-contained operation
- **Composable**: Rules apply independently — no inter-rule dependencies
- **Deterministic**: No ambiguity once the visual language is decoded

</td>
</tr>
</table>

<br>

---

## 🔗 References

| Resource | Link |
|:---------|:-----|
| ARC Prize | [arcprize.org](https://arcprize.org) |
| ARC-AGI-2 Paper | [arxiv.org/abs/2412.04604](https://arxiv.org/abs/2412.04604) |
| Chollet (2019) | *On the Measure of Intelligence* |
| Our Main Solver | [GitMonsters/octotetrahedral-agi](https://github.com/GitMonsters/octotetrahedral-agi) |

<br>



Uploading TRANSCENDPLEXITY.mp4…



<div align="center">

<br>

```
 ████████╗██████╗  █████╗ ███╗   ██╗███████╗ ██████╗███████╗███╗   ██╗██████╗ 
 ╚══██╔══╝██╔══██╗██╔══██╗████╗  ██║██╔════╝██╔════╝██╔════╝████╗  ██║██╔══██╗
    ██║   ██████╔╝███████║██╔██╗ ██║███████╗██║     █████╗  ██╔██╗ ██║██║  ██║
    ██║   ██╔══██╗██╔══██║██║╚██╗██║╚════██║██║     ██╔══╝  ██║╚██╗██║██║  ██║
    ██║   ██║  ██║██║  ██║██║ ╚████║███████║╚██████╗███████╗██║ ╚████║██████╔╝
    ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝ ╚═════╝╚══════╝╚═╝  ╚═══╝╚═════╝ 
                 P L E X I T Y   ·   A G I   E N G I N E
```

**Built with [Transcendplexity](https://github.com/GitMonsters/octotetrahedral-agi)** — OctoTetrahedral AGI Engine

*Targeting the ARC Prize · $1M for 85% accuracy · arcprize.org*

<br>

[![GitHub Stars](https://img.shields.io/github/stars/GitMonsters/SOLVED---abc82100?style=social)](https://github.com/GitMonsters/SOLVED---abc82100)

</div>
