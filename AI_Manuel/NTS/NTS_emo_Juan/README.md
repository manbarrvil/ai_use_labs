# nts_emo_juan

NTS 631 §5.10.2.1 two-machine eigenvalue benchmark — **pydae-BPS / CasADi backend**.

## Requirements

- Python ≥ 3.10
- `pydae` (includes CasADi and SUNDIALS — **no C compiler needed**)
- `numpy`, `matplotlib`, `pandas`

## Install

```powershell
pip install -e .
```

## Usage

```python
from nts_emo_juan import build_model, xl_sweep, plot_eigenvalue_sweep
import numpy as np

built = build_model()                                    # ~5 s, in-memory CasADi graph
res   = xl_sweep(np.arange(0.01, 0.61, 0.05).tolist(), built=built)
fig   = plot_eigenvalue_sweep(res)
fig.savefig('eigenvalue_sweep.png', dpi=150)
```

## Tests

```powershell
# Fast structural tests (no model build)
pytest tests/ -v -m "not slow"

# Full suite including XL sweep
pytest tests/ -v
```

## Acceptance criterion — NTS §5.10.3.1

All electromechanical modes in [0.1, 1.5] Hz must have **damping ≥ 5 %**
across the entire XL sweep (0.01 – 0.6 pu).
