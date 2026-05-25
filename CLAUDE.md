# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo does

Two independent workstreams under `AI_Manuel/`:

1. **GAMS/OPF data pipeline** — generates synthetic time-series datasets for a 14-bus distribution network (365 days × ~289 five-minute intervals), runs GAMS optimization models, and aggregates results into CSV files for ML training.

2. **NTS compliance tools** (`AI_Manuel/NTS/`) — scripts for processing the Spanish Grid Code supervision standard (NTS 631), including PDF→Markdown conversion and power system small-signal analysis.

## Running scripts

All scripts are standalone. Run from the repo root:

```powershell
python AI_Manuel/NTS/pdf_to_markdown.py <archivo.pdf>        # PDF → Markdown + figures
python AI_Manuel/creacarpetas_v1.py                          # Create folder structure
python AI_Manuel/datosrandom_v1.py                           # Generate synthetic data
python AI_Manuel/llamagams_v1.py                             # Run GAMS batch
python AI_Manuel/datos_entrada_v1.py                         # Build input CSV
python AI_Manuel/datos_salida_v1.py                          # Build output CSV
```

Python is installed from Microsoft Store (`python` or `python -m pip`).

## GAMS pipeline architecture

**Data flow (must run in order):**

```
creacarpetas_v1.py
  → data_set/day_N/minutoNNNN/   (364 days × ~289 time steps)

datosrandom_v1.py
  → reads day_1/ templates (LOAD_H_DATA.txt, LOAD_I_DATA.txt, GEN_DATA.txt)
  → writes perturbed versions into day_2 … day_365

llamagams_v1.py
  → runs conv_data.gms (saves .g00 restart files)
  → runs MinPerd_Base_perdidas.gms (writes RESULT_B2B_minNNNN.put)

datos_entrada_v1.py  →  inDATA/prueba.txt   (28 columns: P/Q per bus, net load - gen)
datos_salida_v1.py   →  outDATA/outset.txt  (28 columns: V per bus + line flows + losses)
```

**Network:** 14-bus, Sb = 10 MVA. Time steps: minutes 3, 8, 13, … 1443 (step 5).

**Key data files per time step:**
- `LOAD_H_DATA.txt` — residential P/Q at buses 1,3,4,5,6,8,10,11,12,14
- `LOAD_I_DATA.txt` — industrial P/Q at buses 1,3,7,9,10,12,13,14
- `GEN_DATA.txt` — 15 generators (buses 3–11), columns: Name, Bus, P, Pmax, Pmin
- `RESULT_B2B_minNNNN.put` — GAMS output: bus voltages (lines 10–23, 30–42) + losses (line 0)

## NTS tools

### pdf_to_markdown.py

Converts a PDF to Markdown using `pymupdf4llm`. Figures are extracted as PNGs into `<pdf_stem>_fig/` alongside the `.md` file. Always uses absolute paths internally to avoid GAMS-style working-directory issues.

```python
pdf_to_markdown(pdf_path, output_path=None)
```

### small_signal_2gen.py (in progress)

Small-signal eigenvalue analysis for the two-machine test system defined in NTS §5.10.2.1 (without MPE). Sweeps line reactance XL from 0.01 to 0.6 pu and plots electromechanical modes on the complex plane with 3% and 5% damping lines.

## Dependencies

```
numpy, scipy, matplotlib   # small signal analysis
pymupdf4llm                # PDF conversion
pandas                     # data pipeline
```

Install: `pip install <package>` or `python -m pip install <package>` if `pip` is not on PATH.
