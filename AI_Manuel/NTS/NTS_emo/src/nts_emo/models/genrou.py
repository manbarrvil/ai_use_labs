"""
GENROU — 6th-order round-rotor synchronous machine (IEEE standard model).

States (per machine, suffixed): delta, omega, eqp, edp, psi1d, psi2q

Convention (generator: positive current flows OUT of terminal):
  Stator algebraic (Ra = 0):
    g_Vd : Vd - Edpp + xqpp*iq = 0
    g_Vq : Vq - Eqpp + xdpp*id = 0
  Subtransient EMFs:
    Eqpp = (xdpp-xl)/(xdp-xl)*eqp + (xdp-xdpp)/(xdp-xl)*psi1d
    Edpp = (xqpp-xl)/(xqp-xl)*edp + (xqp-xqpp)/(xqp-xl)*psi2q
  Park transform (network ↔ dq):
    Vd = -e*sin(delta) + f*cos(delta)
    Vq =  e*cos(delta) + f*sin(delta)
  Current injection to network:
    Igen_e = iq*cos(delta) - id*sin(delta)
    Igen_f = iq*sin(delta) + id*cos(delta)
  Electromagnetic torque:
    Te = (Eqpp - xdpp*id)*iq - (-Edpp + xqpp*iq)*id
  Saturation (exponential, Anderson-Fouad):
    Se = A_sat * exp(B_sat * |eqp|)
"""

import sympy as sym


def _sat_coeffs(s1: float, s2: float):
    """Return (A_sat, B_sat) for S(E) = A*exp(B*E), fitted at E=1.0 and E=1.2."""
    if s1 <= 0 or s2 <= 0:
        return 0.0, 0.0
    B = float(sym.log(sym.Rational(s2) / sym.Rational(s1)) / sym.Rational(1, 5))
    A = s1 * sym.exp(-sym.Rational(B))
    return float(A.evalf()), B


def genrou_equations(syms: dict, suffix: str, bus_id: str,
                     Sbase_mach: float, Sbase_sys: float,
                     params: dict) -> dict:
    """
    Build the symbolic equations for one GENROU machine.

    Parameters
    ----------
    syms       : shared SymPy symbol namespace (all symbols with real=True)
    suffix     : suffix appended to machine variable names (e.g. '1' or '2')
    bus_id     : network bus label for this machine (e.g. '1' for bus 1, '4' for bus 4)
    Sbase_mach : machine MVA base
    Sbase_sys  : system MVA base (100 MVA)
    params     : dict with H, D, Td0p, Td0pp, Tq0p, Tq0pp,
                          xd, xq, xdp, xqp, xdpp, xqpp, xl, s1, s2

    Returns
    -------
    dict with partial system keys
    """
    s  = suffix
    br = Sbase_mach / Sbase_sys   # base conversion factor

    H     = params['H']
    D     = params['D']
    Td0p  = params['Td0p']
    Td0pp = params['Td0pp']
    Tq0p  = params['Tq0p']
    Tq0pp = params['Tq0pp']
    xd    = params['xd']
    xq    = params['xq']
    xdp   = params['xdp']
    xqp   = params['xqp']
    xdpp  = params['xdpp']
    xqpp  = params['xqpp']
    xl    = params['xl']

    omega_0 = 2.0 * sym.pi * 50

    A_sat, B_sat = _sat_coeffs(params['s1'], params['s2'])

    def S(name):
        return syms[f'{name}_{s}']

    # States
    delta = S('delta')
    omega = S('omega')
    eqp   = S('eqp')
    edp   = S('edp')
    psi1d = S('psi1d')
    psi2q = S('psi2q')

    # Algebraic variables (machine side)
    id_   = S('id')
    iq_   = S('iq')
    Vd    = S('Vd')
    Vq    = S('Vq')
    Eqpp  = S('Eqpp')
    Edpp  = S('Edpp')
    Pe    = S('Pe')     # electrical power in system pu (used by PSS)
    Igen_e = S('Igen_e')
    Igen_f = S('Igen_f')

    # Controls (resolved by assembly: Efd from AVR, Tm from governor or constant)
    Efd = S('Efd')
    Tm  = S('Tm')

    # Network bus voltage at this machine's terminal
    e_bus = syms[f'e_{bus_id}']
    f_bus = syms[f'f_{bus_id}']

    # Saturation on E'q — cap argument to prevent overflow during Newton iterations.
    # Physically eqp > 0 in normal operation; max cap at exp(20) ~ 5e8 (well beyond rated).
    eqp_cap = sym.Piecewise((eqp, eqp > 0), (sym.Integer(0), True))
    B_cap = 20.0 / B_sat if B_sat > 0 else 10.0
    eqp_sat = sym.Piecewise((eqp_cap, eqp_cap < B_cap), (sym.Float(B_cap), True))
    Se = A_sat * sym.exp(B_sat * eqp_sat) if A_sat > 0 else sym.Integer(0)

    # Subtransient EMF coefficients
    c_qd = (xdpp - xl) / (xdp - xl)
    c_1d = (xdp  - xdpp) / (xdp - xl)
    c_dq = (xqpp - xl) / (xqp - xl)
    c_2q = (xqp  - xqpp) / (xqp - xl)

    # Electromagnetic torque (machine pu)
    psid = Eqpp - xdpp * id_
    psiq = -Edpp + xqpp * iq_
    Te   = psid * iq_ - psiq * id_

    # ------------------------------------------------------------------
    # Differential equations
    # ------------------------------------------------------------------
    f_delta = omega_0 * omega

    f_omega = (Tm - Te - D * omega) / (2.0 * H * br)

    # d-axis transient (field flux E'q)
    f_eqp = (1.0 / Td0p) * (
        Efd
        - eqp * (1.0 + Se)
        - (xd - xdpp) * id_
        + (xd - xdp) / (xdp - xl) * (Eqpp - eqp)
    )

    # q-axis transient (amortisseur E'd)
    f_edp = (1.0 / Tq0p) * (
        -edp
        + (xq - xqpp) * iq_
        - (xq - xqp) / (xqp - xl) * (Edpp - edp)
    )

    # d-axis sub-transient amortisseur
    f_psi1d = (1.0 / Td0pp) * (eqp - psi1d - (xdp - xdpp) * id_)

    # q-axis sub-transient amortisseur
    f_psi2q = (1.0 / Tq0pp) * (edp - psi2q + (xqp - xqpp) * iq_)

    # ------------------------------------------------------------------
    # Algebraic equations
    # ------------------------------------------------------------------
    g_Eqpp   = Eqpp - (c_qd * eqp + c_1d * psi1d)
    g_Edpp   = Edpp - (c_dq * edp + c_2q * psi2q)
    g_Vd     = Vd   - Edpp + xqpp * iq_     # stator d
    g_Vq     = Vq   - Eqpp + xdpp * id_     # stator q
    g_Vd_net = Vd   - (-e_bus * sym.sin(delta) + f_bus * sym.cos(delta))
    g_Vq_net = Vq   - ( e_bus * sym.cos(delta) + f_bus * sym.sin(delta))
    # Scale from machine pu to system pu (br = Sbase_mach / Sbase_sys)
    g_Ie     = Igen_e - br * (iq_ * sym.cos(delta) - id_ * sym.sin(delta))
    g_If     = Igen_f - br * (iq_ * sym.sin(delta) + id_ * sym.cos(delta))
    g_Pe     = Pe - br * Te * (1.0 + omega)  # electrical power in system pu

    x_names = [f'delta_{s}', f'omega_{s}', f'eqp_{s}', f'edp_{s}',
               f'psi1d_{s}', f'psi2q_{s}']

    y_names = [f'id_{s}', f'iq_{s}', f'Vd_{s}', f'Vq_{s}',
               f'Eqpp_{s}', f'Edpp_{s}',
               f'Igen_e_{s}', f'Igen_f_{s}',
               f'Pe_{s}']

    return {
        'x_list':     x_names,
        'y_ini_list': y_names,
        'y_run_list': y_names,
        'f_list':     [f_delta, f_omega, f_eqp, f_edp, f_psi1d, f_psi2q],
        'g_list':     [g_Eqpp, g_Edpp, g_Vd, g_Vq, g_Vd_net, g_Vq_net, g_Ie, g_If, g_Pe],
        'h_dict':     {f'Vt_{s}': sym.sqrt(e_bus**2 + f_bus**2)},
        'params_dict': {},
        'u_ini_dict':  {f'Efd_{s}': 1.0, f'Tm_{s}': 1.0},
        'u_run_dict':  {f'Efd_{s}': 1.0, f'Tm_{s}': 1.0},
    }
