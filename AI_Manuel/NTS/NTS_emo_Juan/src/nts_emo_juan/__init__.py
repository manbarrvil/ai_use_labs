"""
nts_emo_juan — NTS 631 §5.10.2.1 eigenvalue analysis (pydae-BPS / CasADi backend).

Quick start::

    from nts_emo_juan import build_model, load_model, xl_sweep, plot_eigenvalue_sweep
    import numpy as np

    built  = build_model()                          # assemble CasADi graph (~5 s)
    res    = xl_sweep(np.arange(0.01, 0.61, 0.05).tolist(), built=built)
    fig    = plot_eigenvalue_sweep(res)
    fig.savefig('eigenvalue_sweep.png', dpi=150)
    print('EM damping:', res['em_damp'])
"""

from .build_model import build_model, load_model
from .analysis import xl_sweep
from .plots import plot_eigenvalue_sweep

__all__ = ['build_model', 'load_model', 'xl_sweep', 'plot_eigenvalue_sweep']
