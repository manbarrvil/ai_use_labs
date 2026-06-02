# nts_emo_juan

Small-signal eigenvalue analysis for the NTS 631 §5.10.2.1 two-machine benchmark,
using the **pydae-BPS / CasADi** backend.

## What this is

The NTS (Norma Técnica de Supervisión) 631 defines a two-machine test system
(§5.10.2.1) used to verify that a Power Generation Module (MGE) does not
degrade inter-area oscillation damping. The acceptance criterion (§5.10.3.1)
is that the electromechanical mode must have **damping ≥ 5 %** across the full
range of inter-area line reactances (XL = 0.01 … 0.6 pu).

`nts_emo_juan` implements this test using the pydae-BPS framework:

- The benchmark network (buses, lines, loads, 6th-order generators, ST4B/ST1
  AVRs, PSS2A, IEEEG1 governor) is defined in `cases/base/nts_base.hjson`.
- `BpsBuilder` + `CasadiBuilder` assemble a CasADi SX symbolic DAE.
  **No C compiler is required.**
- `xl_sweep` loops over XL values, updates the line 2-3 reactance via
  `change_line`, re-initialises the load flow, and linearises the DAE to
  obtain the reduced state matrix A.
- `plot_eigenvalue_sweep` renders the complex-plane trajectory with 3 % and
  5 % damping cones.

## Difference from NTS_emo

| | NTS_emo | nts_emo_juan |
|---|---|---|
| Model source | Hand-coded SymPy DAE (from PDF) | HJSON definition (pydae-BPS) |
| Solver backend | ctypes DLL (requires MSVC on Windows) | CasADi / SUNDIALS (no compiler) |
| XL parameterisation | `model.ini({'XL': xl})` | `change_line` + `model.ini` |
| Build time | ~60–120 s | ~5 s |

## Quick start

```python
from nts_emo_juan import build_model, xl_sweep, plot_eigenvalue_sweep
import numpy as np

built  = build_model()
res    = xl_sweep(np.arange(0.01, 0.61, 0.05).tolist(), built=built)
fig    = plot_eigenvalue_sweep(res)
fig.savefig('eigenvalue_sweep.png', dpi=150)
print('EM damping:', [f'{z*100:.1f}%' for z in res['em_damp']])
```

## Reference eigenvalues (from HJSON)

| XL (pu) | σ (rad/s) | ω/2π (Hz) |
|---------|----------|---------|
| 0.01 | −1.640 | 5.655 |
| 0.60 | −0.183 | 1.281 |
