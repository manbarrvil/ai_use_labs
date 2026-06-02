"""
XL sweep: initialise the model at each reactance value, linearise, collect eigenvalues.
"""

import logging
import numpy as np
import pandas as pd


def xl_sweep(xl_values: list,
             model_dir: str = './build',
             xy_0_hint: dict | None = None) -> dict:
    """
    Sweep the line reactance XL and collect eigenvalue data at each operating point.

    For each XL the function:
      1. Calls model.ini({'XL': xl})  — Newton-Raphson initialisation
      2. Calls pydae.ssa.eig(model)   — eigenvalue decomposition of A = Fx - Fy·Gy⁻¹·Gx
      3. Calls pydae.ssa.damp_report  — extracts frequency and damping for each mode
      4. Identifies the electromechanical mode (0.1–1.5 Hz)

    Warm-starting: each XL uses the converged solution of the previous XL as initial
    guess, which greatly helps convergence for large XL values.

    Parameters
    ----------
    xl_values  : list of XL values (pu, system base) to sweep
    model_dir  : directory with compiled pydae library
    xy_0_hint  : optional dict of initial variable guesses for the first point

    Returns
    -------
    dict with keys:
        'xl_values'    — list of floats (the input)
        'eigenvalues'  — list of np.ndarray, complex eigenvalues per XL
        'damp_df'      — list of pd.DataFrame (damp_report output per XL)
        'em_modes'     — list of complex (electromechanical eigenvalue per XL)
        'em_freq_hz'   — list of float (EM mode frequency in Hz per XL)
        'em_damp'      — list of float (EM mode damping ratio per XL)
    """
    from nts_emo.build_model import load_model
    import pydae.ssa as ssa

    model = load_model(model_dir)

    results = {
        'xl_values': list(xl_values),
        'eigenvalues': [],
        'damp_df': [],
        'em_modes': [],
        'em_freq_hz': [],
        'em_damp': [],
    }

    # Build initial guess array (flat start at 1.0 if no hint given)
    if xy_0_hint is not None:
        xy_0 = xy_0_hint
    else:
        xy_0 = 1.0

    for xl in xl_values:
        logging.info(f'[xl_sweep] XL = {xl:.3f} pu')

        ok = model.ini({'XL': float(xl)}, xy_0=xy_0)
        if not ok:
            logging.warning(f'[xl_sweep] Initialisation did NOT converge for XL={xl:.3f}')
            # Fill with NaN and continue
            N = model.N_x
            results['eigenvalues'].append(np.full(N, np.nan + 0j))
            results['damp_df'].append(pd.DataFrame())
            results['em_modes'].append(complex(np.nan, np.nan))
            results['em_freq_hz'].append(np.nan)
            results['em_damp'].append(np.nan)
            continue

        # Eigenvalue decomposition
        eig_vals, V, W = ssa.eig(model)
        df = ssa.damp_report(model)

        # Identify electromechanical mode (slowest oscillatory mode in 0.1–1.5 Hz)
        em_val, em_f, em_z = _find_em_mode(eig_vals)

        results['eigenvalues'].append(eig_vals.copy())
        results['damp_df'].append(df)
        results['em_modes'].append(em_val)
        results['em_freq_hz'].append(em_f)
        results['em_damp'].append(em_z)

        # Warm-start next XL from current converged solution
        xy_0 = {name: model.get_value(name)
                for name in model.x_list + model.y_ini_list}

    return results


def _find_em_mode(eigenvalues: np.ndarray,
                  f_min: float = 0.1, f_max: float = 1.5):
    """
    Return (eigenvalue, freq_hz, damping) for the least-damped oscillatory
    mode whose frequency is within [f_min, f_max] Hz.
    """
    best_val  = complex(np.nan, np.nan)
    best_f    = np.nan
    best_zeta = np.nan
    best_damp = 1.0   # track least-damped (smallest positive damping)

    for lam in eigenvalues:
        sigma = lam.real
        omega = abs(lam.imag)
        if omega < 1e-6:
            continue   # skip real (non-oscillatory) modes
        f_hz = omega / (2 * np.pi)
        if not (f_min <= f_hz <= f_max):
            continue
        zeta = -sigma / np.sqrt(sigma**2 + omega**2)
        if zeta < best_damp:
            best_damp = zeta
            best_val  = lam
            best_f    = f_hz
            best_zeta = zeta

    return best_val, best_f, best_zeta
