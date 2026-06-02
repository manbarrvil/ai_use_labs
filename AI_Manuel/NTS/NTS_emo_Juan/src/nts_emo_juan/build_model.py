"""
Build and load the NTS base-case CasADi model from nts_base.hjson.

No C compiler required — the model is assembled as a CasADi SX symbolic
graph and integrated by SUNDIALS/IDAS entirely in-process.
"""

from pathlib import Path

from pydae.bps import BpsBuilder
from pydae.core.builder import CasadiBuilder
from pydae.core.model import CasadiModel

CASES_DIR = Path(__file__).parents[2] / 'cases' / 'base'
HJSON_PATH = CASES_DIR / 'nts_base.hjson'
XY_0_PATH  = CASES_DIR / 'nts_base_xy_0.json'


def build_model(hjson_path=None):
    """
    Assemble and compile the CasADi DAE for the NTS base case.

    Returns the built model descriptor consumed by :func:`load_model`.
    """
    if hjson_path is None:
        hjson_path = HJSON_PATH
    grid = BpsBuilder(str(hjson_path), use_casadi=True)
    grid.construct('nts_base')
    return CasadiBuilder(grid.sys_dict).build()


def load_model(built=None):
    """
    Create a :class:`CasadiModel` runtime instance.

    Parameters
    ----------
    built : object returned by :func:`build_model`.
            If None, :func:`build_model` is called with default paths.
    """
    if built is None:
        built = build_model()
    return CasadiModel(built)
