"""
IZ Load model: constant-current P, constant-impedance Q.

At bus voltage V = sqrt(e^2 + f^2) and reference voltage V0:
  P_load = P0 * (V/V0)        constant-current (linear in V)
  Q_load = Q0 * (V/V0)^2      constant-impedance (quadratic in V)

Returns symbolic SymPy expressions for P and Q injection (as load → negative
generation).  No dynamic states — these expressions are plugged directly into
the network power-balance algebraic equations in network.py.
"""

import sympy as sym


def iz_load_expressions(syms: dict, bus: str,
                        P0: float, Q0: float, V0: float = 1.0):
    """
    Return (P_load_expr, Q_load_expr) for a given bus.

    Parameters
    ----------
    syms : shared symbol namespace
    bus  : bus label (e.g. '2' or '3') — used to look up e_{bus}, f_{bus}
    P0   : rated active load (pu, system base)
    Q0   : rated reactive load (pu, system base)
    V0   : reference voltage magnitude (pu), default 1.0

    Returns
    -------
    (P_load, Q_load) — SymPy expressions
    """
    e = syms[f'e_{bus}']
    f = syms[f'f_{bus}']
    V2 = e**2 + f**2   # V^2 — avoids sqrt in the expressions (cleaner Jacobian)

    # P_load = P0 * (V/V0) = P0/V0 * sqrt(V2) — but to keep polynomial:
    # At operating point V=V0=1: P_load = P0, Q_load = Q0  ✓
    # We use sqrt for generality; pydae handles this symbolically.
    V_mag = sym.sqrt(V2)
    P_load = P0 * (V_mag / V0)
    Q_load = Q0 * (V2 / V0**2)    # Q ∝ V^2 — polynomial, no sqrt needed

    return P_load, Q_load
