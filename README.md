# dOPH — Decoupled Observer Patch Holography
**Version:** v2.2 (April 27, 2026)

## Current Project Status

We have developed a new theoretical model called **Decoupled Observer Patch Holography (dOPH)**.

The key parameter **P** is strictly fixed to the theoretical value **P ≡ √(8/3) ≈ 1.63299**.

Observer decoupling is implemented via a strict projection operator.

### Documents (Документы)

- **Русская версия** (Russian version):  
  [dOPH_Final_April2026.tex](dOPH_Final_April2026.tex)  
  [PDF (после компиляции)](dOPH_Final_April2026.pdf)

- **English Version**:  
  [dOPH_Final_April2026_EN.tex](dOPH_Final_April2026_EN.tex)  
  [PDF (after compilation)](dOPH_Final_April2026_EN.pdf)

### Achieved Results

- Synthetic tests: 20,000 galaxies → stability **98.8%** (LSB: 98.7%)
- Milky Way rotation curve (Eilers et al. 2019): reduced χ² = **1.84**
- SPARC data prepared (`data/sparc/Rotmod_LTG.zip`)
- Fitting draft: `sparc_fittings_draft_v4.py`

### Note

The full SPARC fitting (175 galaxies) has not yet been executed due to current environment limitations.  
Further work will continue when a suitable computing setup is available.

## Main Files

- `doph_model_improved.py` — core model
- `code/sparc_fittings_draft_v4.py` — SPARC fitting draft
- `dOPH_Final_April2026.tex` — Russian LaTeX document
- `dOPH_Final_April2026_EN.tex` — English LaTeX document
