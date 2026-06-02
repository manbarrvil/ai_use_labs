"""
NTS_emo — Small-signal eigenvalue analysis for NTS 631 §5.10.2.1.
"""

from nts_emo.assembly    import assemble_system
from nts_emo.build_model import build_nts_model, load_model
from nts_emo.analysis    import xl_sweep
from nts_emo.plots       import plot_eigenvalue_sweep

__version__ = '0.1.0'
__all__ = [
    'assemble_system',
    'build_nts_model',
    'load_model',
    'xl_sweep',
    'plot_eigenvalue_sweep',
]
