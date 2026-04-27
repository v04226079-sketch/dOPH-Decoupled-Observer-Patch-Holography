# dOPH — Decoupled Observer Patch Holography
**Version:** v2.2 (April 27, 2026)

## Current Project Status

We have developed a new theoretical model called **Decoupled Observer Patch Holography (dOPH)**.

The key feature of the model is that the parameter **P** is strictly fixed to the theoretical value:
**P ≡ √(8/3) ≈ 1.63299**

Observer decoupling is implemented via a strict projection operator.

### Achieved Results

- **Synthetic tests**: 20,000 galaxies → stability **98.8%** (LSB galaxies: 98.7%)
- **Milky Way test** (Eilers et al. 2019): reduced χ² = **1.84**
- **SPARC data**: Rotmod_LTG.zip is placed in `data/sparc/`
- **Fitting draft**: `sparc_fittings_draft_v4.py` is ready

### Documents

- **Русская версия** (для русскоязычных читателей):  
  [`dOPH_Final_April2026.tex`](dOPH_Final_April2026.tex) → [PDF](dOPH_Final_April2026.pdf) (после компиляции)

- **English Version** (for English-speaking readers):  
  [`dOPH_Final_April2026_EN.tex`](dOPH_Final_April2026_EN.tex) → [PDF](dOPH_Final_April2026_EN.pdf) (после компиляции)

### Important Note

The full fitting on 175 real SPARC galaxies has not yet been executed due to technical limitations of the current environment.  
As soon as a suitable computing setup (computer or Google Colab) is available, a detailed analysis will be performed.

The project is in an active draft stage. All key theoretical components (P, projection operator, observer decoupling) are fixed and documented.

## Main Files

- `doph_model_improved.py` — core model implementation
- `code/doph_reproducible_test.py` — reproducible test on 20,000 galaxies
- `code/sparc_fittings_draft_v4.py` — SPARC fitting draft
- `dOPH_Final_April2026.tex` — main LaTeX document (Russian)
- `dOPH_Final_April2026_EN.tex` — English version
