# NTS_emo Documentation

## Overview

`nts_emo` implements the small-signal eigenvalue analysis for the two-machine benchmark system defined in NTS 631 §5.10.2.1 (REE Spanish Grid Code, November 2020). The study sweeps line reactance XL from 0.01 to 0.6 pu and plots electromechanical mode trajectories on the complex plane.

## Package structure

```
src/nts_emo/
  models/        Component equation libraries (GENROU, ST4B, ST1, PSS2A, IEEEG1, IZ load)
  network.py     4-bus admittance matrix and power-balance algebraic equations
  assembly.py    Merges components into a single pydae system_dict
  build_model.py Compiles the symbolic DAE to a C/CFFI library via pydae
  analysis.py    XL sweep loop (init → linearise → collect eigenvalues)
  plots.py       Complex-plane plot with 3%/5% damping cones
```

## Quick start

```python
from nts_emo import build_nts_model, xl_sweep, plot_eigenvalue_sweep
import numpy as np

build_nts_model()                              # compile once (~1-2 min)
xl_values = np.arange(0.01, 0.61, 0.05).tolist()
results = xl_sweep(xl_values)                  # sweep
fig = plot_eigenvalue_sweep(results)           # plot
fig.savefig("eigenvalue_sweep.png", dpi=150)
```

## System parameters

See `src/nts_emo/assembly.py` for all parameter values (GEN1_PARAMS, GEN2_PARAMS, ST4B_PARAMS, PSS2A_PARAMS, ST1_PARAMS, IEEEG1_PARAMS).

## Acceptance criterion (NTS §5.10.3.1)

All electromechanical modes in 0.1–1.5 Hz must have damping ≥ 5%.  
The sweep plot visualises compliance: all modes must lie to the left of the 5% damping cone.

## References

- REE, *Norma Técnica de Supervisión NTS 631 v2*, November 2020
- IEEE Std 421.5-2016, *Excitation System Models for Power System Stability Studies*
- Kundur, P., *Power System Stability and Control*, McGraw-Hill, 1994
