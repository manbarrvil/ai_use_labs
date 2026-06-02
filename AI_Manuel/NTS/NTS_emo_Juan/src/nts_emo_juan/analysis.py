"""
XL sweep: change line 2-3 reactance, re-initialise, linearise, collect eigenvalues.
"""

import logging
import numpy as np
import pandas as pd

from pydae.bps.lines import change_line

from .build_model import build_model, load_model, XY_0_PATH

_XY_0 = str(XY_0_PATH)


def xl_sweep(xl_values: list, built=None, hjson_path=None) -> dict:
    """
    Sweep line 2-3 reactance XL and collect eigenvalue data at each operating point.

    For each XL the function:
      1. Calls ``change_line`` to update the 2-3 branch reactance in-place.
      2. Calls ``model.ini`` — Newton-Raphson load-flow initialisation.
      3. Calls ``model.A_eval`` — reduced state matrix A = Fx - Fy·Gy⁻¹·Gx.
      4. Extracts eigenvalues with ``numpy.linalg.eigvals``.
      5. Identifies the electromechanical mode (least-damped in 0.1–1.5 Hz).

    Parameters
    ----------
    xl_values  : list of XL values (pu, system base) to sweep
    built      : compiled model descriptor from :func:`build_model`.
                 If None the model is built from the default HJSON.
    hjson_path : optional path to the HJSON case file (only used when
                 *built* is None)

    Returns
    -------
    dict with keys:

    ``xl_values``
        list of floats (the input)
    ``eigenvalues``
        list of ``np.ndarray`` — complex eigenvalues per XL
    ``damp_df``
        list of ``pd.DataFrame`` — freq/damping table per XL
    ``em_modes``
        list of complex — electromechanical eigenvalue per XL
    ``em_freq_hz``
        list of float — EM mode frequency (Hz)
    ``em_damp``
        list of float — EM mode damping ratio
    """
    if built is None:
        built = build_model(hjson_path)
    model = load_model(built)

    results: dict = {
        'xl_values': list(xl_values),
        'eigenvalues': [],
        'damp_df': [],
        'em_modes': [],
        'em_freq_hz': [],
        'em_damp': [],
    }

    for xl in xl_values:
        logging.info('[xl_sweep] XL = %.3f pu', xl)
        change_line(model, {'bus_j': '2', 'bus_k': '3',
                            'X_pu': float(xl), 'R_pu': 0.0,
                            'Bs_pu': 0.0, 'S_mva': 100})
        try:
            model.ini({}, _XY_0)
            model.A_eval()
            eigs = np.linalg.eigvals(model.A)
            df = _damp_dataframe(eigs)
            em_val, em_f, em_z = _find_em_mode(eigs)
        except Exception as exc:
            logging.warning('[xl_sweep] Failed for XL=%.3f: %s', xl, exc)
            n = getattr(model, 'n_x', 1)
            eigs = np.full(n, np.nan + 0j)
            df = pd.DataFrame()
            em_val, em_f, em_z = complex(np.nan, np.nan), np.nan, np.nan

        results['eigenvalues'].append(eigs)
        results['damp_df'].append(df)
        results['em_modes'].append(em_val)
        results['em_freq_hz'].append(em_f)
        results['em_damp'].append(em_z)

    return results


def _damp_dataframe(eigs: np.ndarray) -> pd.DataFrame:
    rows = []
    for lam in eigs:
        omega = abs(lam.imag)
        if omega < 1e-6:
            continue
        sigma = lam.real
        f_hz = omega / (2.0 * np.pi)
        zeta = -sigma / np.sqrt(sigma**2 + omega**2)
        rows.append({'sigma': sigma, 'omega_rad_s': omega,
                     'freq_hz': f_hz, 'damping': zeta})
    if not rows:
        return pd.DataFrame(columns=['sigma', 'omega_rad_s', 'freq_hz', 'damping'])
    return pd.DataFrame(rows).sort_values('damping').reset_index(drop=True)


def _find_em_mode(eigenvalues: np.ndarray,
                  f_min: float = 0.1, f_max: float = 1.5):
    """Return (eigenvalue, freq_hz, damping) for the least-damped EM mode."""
    best_val  = complex(np.nan, np.nan)
    best_f    = np.nan
    best_zeta = np.nan
    best_damp = 1.0   # track least-damped (smallest positive damping)

    for lam in eigenvalues:
        sigma = lam.real
        omega = abs(lam.imag)
        if omega < 1e-6:
            continue
        f_hz = omega / (2.0 * np.pi)
        if not (f_min <= f_hz <= f_max):
            continue
        zeta = -sigma / np.sqrt(sigma**2 + omega**2)
        if zeta < best_damp:
            best_damp = zeta
            best_val  = lam
            best_f    = f_hz
            best_zeta = zeta

    return best_val, best_f, best_zeta
