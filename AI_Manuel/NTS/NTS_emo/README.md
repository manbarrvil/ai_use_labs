# NTS_emo

Small-signal eigenvalue analysis for the two-machine benchmark system defined in NTS 631 §5.10.2.1 (REE Spanish Grid Code). Implements the eigenvalue sweep (XL from 0.01 to 0.6 pu) for two synchronous generators only (no MPE), using [pydae](https://github.com/pydae/pydae).

## System

4-bus network, 100 MVA base:

- **Bus 1**: Generator 1 — 1500 MVA round-rotor, IEEE ST4B exciter + PSS2A stabiliser
- **Bus 2**: Load 1250 MW (IZ model) + transformer T1 (xT1=0.01 pu)
- **Bus 3**: Load 4000 MW (IZ model) + line (XL variable, 0.01–0.6 pu)
- **Bus 4**: Generator 2 — 5000 MVA round-rotor, IEEE ST1 exciter + IEEEG1 governor

## Quick start

```bash
pip install -e ".[dev]"
```

```python
from nts_emo import build_nts_model, xl_sweep, plot_eigenvalue_sweep
import numpy as np

# Build (compiles C library — runs once, ~1-2 min)
build_nts_model()

# Sweep XL from 0.01 to 0.6 pu
xl_values = np.arange(0.01, 0.61, 0.05).tolist()
results = xl_sweep(xl_values)

# Plot complex-plane trajectory with 3% and 5% damping cones
fig = plot_eigenvalue_sweep(results)
fig.savefig("nts_eigenvalue_sweep.png", dpi=150)
```

## References

- REE, *Norma Técnica de Supervisión de la Conformidad para MGE* (NTS 631, v2), November 2020, §5.10.2.1
- IEEE Std 421.5-2016, *Excitation System Models for Power System Stability Studies*
