"""
4-bus network for the NTS §5.10.2.1 benchmark (rectangular bus voltages).

Bus numbering:
  1 — Generator 1 terminal  (1500 MVA MGES, PQ bus w/ generator injection)
  2 — Load bus               (T1 connection, IZ load 1250 MW)
  3 — Load bus               (line connection, IZ load 4000 MW)
  4 — Generator 2 terminal   (5000 MVA MGES, SLACK: V=1.0∠0°)

Network elements (100 MVA system base):
  T1  : buses 1–2, xT1 = 0.01 pu
  Line: buses 2–3, XL  = symbolic parameter (0.01–0.6 pu)
  T2  : buses 3–4, xT2 = 0.003 pu

Bus voltage in rectangular form: V_k = e_k + j*f_k

Equation count = 8 (one per bus-voltage component):
  Bus 1 (generator 1): current balance (2 eqs)
    Ie_net_1 − Ie_gen1 = 0
    If_net_1 − If_gen1 = 0
  Bus 2 (load): power balance (2 eqs)
    P_net_2 − P_load2 = 0
    Q_net_2 − Q_load2 = 0
  Bus 3 (load): power balance (2 eqs)
    P_net_3 − P_load3 = 0
    Q_net_3 − Q_load3 = 0
  Bus 4 (slack): voltage specification (2 eqs)
    e_4 − V4ref = 0
    f_4 = 0
"""

import sympy as sym


def _ybus_susceptances(xT1: float, XL_sym, xT2: float):
    """
    Return Im(Y_bus) for the lossless network, using the standard convention:
      Im(Y_kk) = -sum_{j≠k}(1/x_kj)   NEGATIVE diagonal
      Im(Y_kj) = +1/x_kj               POSITIVE off-diagonal

    With this sign convention, Ie_k = sum_j(-B_kj*f_j) and If_k = sum_j(B_kj*e_j)
    give the correct physical current injection.
    """
    b12 = 1 / xT1          # branch susceptance T1 (positive)
    b23 = 1 / XL_sym       # branch susceptance line (positive, contains XL symbol)
    b34 = 1 / xT2          # branch susceptance T2 (positive)

    # 4×4 B = Im(Y_bus): negative diagonal, positive off-diagonal
    B = sym.zeros(4, 4)
    B[0, 0] = -b12
    B[1, 1] = -(b12 + b23)
    B[2, 2] = -(b23 + b34)
    B[3, 3] = -b34
    B[0, 1] = B[1, 0] = b12
    B[1, 2] = B[2, 1] = b23
    B[2, 3] = B[3, 2] = b34

    return B


def network_equations(syms: dict,
                      P_load2, Q_load2,
                      P_load3, Q_load3,
                      topology: dict | None = None) -> dict:
    """
    Return the 8 algebraic network equations for the 4-bus benchmark.

    Parameters
    ----------
    syms                : shared SymPy symbol namespace
    P_load2, Q_load2    : SymPy expressions for load at bus 2 (system pu)
    P_load3, Q_load3    : SymPy expressions for load at bus 3 (system pu)
    topology            : optional dict with 'xT1' and 'xT2' (float, pu);
                          defaults to NTS benchmark values.

    Returns
    -------
    dict with partial system keys: y_ini_list, y_run_list, g_list,
                                   params_dict, u_ini_dict, u_run_dict
    """
    if topology is None:
        topology = {'xT1': 0.01, 'xT2': 0.003}

    xT1 = float(topology['xT1'])
    xT2 = float(topology['xT2'])
    XL  = syms['XL']

    # Bus voltage components
    e = [syms[f'e_{k}'] for k in range(1, 5)]  # e[0]=e_1, ..., e[3]=e_4
    f = [syms[f'f_{k}'] for k in range(1, 5)]

    # Generator 1 current injection (bus 4 is slack — gen 2 current not in network eqs)
    Ie1 = syms['Igen_e_1']
    If1 = syms['Igen_f_1']

    # Slack bus reference voltage
    V4ref = syms['V4ref']

    B = _ybus_susceptances(xT1, XL, xT2)

    # For lossless network G=0: Ie_net_k = -sum_j B_kj * f_j
    #                           If_net_k =  sum_j B_kj * e_j
    def Ie_net(k):
        return sum(-B[k, j] * f[j] for j in range(4))

    def If_net(k):
        return sum( B[k, j] * e[j] for j in range(4))

    def P_net(k):
        return e[k] * Ie_net(k) + f[k] * If_net(k)

    def Q_net(k):
        return f[k] * Ie_net(k) - e[k] * If_net(k)

    g_list = [
        # Bus 1 — current balance: network current = generator injection
        Ie_net(0) - Ie1,
        If_net(0) - If1,
        # Bus 2 — power balance: P_net + P_load = 0 (load absorbs network injection)
        P_net(1) + P_load2,
        Q_net(1) + Q_load2,
        # Bus 3 — power balance
        P_net(2) + P_load3,
        Q_net(2) + Q_load3,
        # Bus 4 — slack bus voltage specification
        e[3] - V4ref,
        f[3],
    ]

    y_names = ['e_1', 'f_1', 'e_2', 'f_2', 'e_3', 'f_3', 'e_4', 'f_4']

    return {
        'y_ini_list': y_names,
        'y_run_list': y_names,
        'g_list':     g_list,
        'params_dict': {'XL': 0.3},
        'u_ini_dict':  {'V4ref': 1.0},
        'u_run_dict':  {'V4ref': 1.0},
    }
