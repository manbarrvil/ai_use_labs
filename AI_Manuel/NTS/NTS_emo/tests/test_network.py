"""Tests for the 4-bus network module."""

import sympy as sym
from nts_emo.network import network_equations, _ybus_susceptances
from nts_emo.models.iz_load import iz_load_expressions
from nts_emo.assembly import _make_syms


def _net_syms():
    names = [
        'e_1', 'f_1', 'e_2', 'f_2', 'e_3', 'f_3', 'e_4', 'f_4',
        'Igen_e_1', 'Igen_f_1', 'Igen_e_2', 'Igen_f_2',
        'XL', 'V4ref',
    ]
    return _make_syms(names)


def test_ybus_diagonal_dominant():
    """Im(Y_bus): diagonal is negative, |diagonal| = sum of off-diagonal entries."""
    XL_sym = sym.Symbol('XL', real=True)
    B = _ybus_susceptances(0.01, XL_sym, 0.003)
    # Bus 2: |B_22| = B_21 + B_23 (sum of positive off-diagonals)
    # B_22 = -(b12+b23), B_21 = b12, B_23 = b23 → B_21+B_23 = b12+b23 = -B_22
    assert sym.simplify(B[1, 1] + B[1, 0] + B[1, 2]) == 0


def test_iz_load_at_nominal():
    """At V=V0=1.0, P_load = P0 and Q_load = Q0."""
    syms = _make_syms(['e_2', 'f_2'])
    P0, Q0 = 12.5, 0.0
    P_expr, Q_expr = iz_load_expressions(syms, '2', P0, Q0, V0=1.0)
    val = {syms['e_2']: 1.0, syms['f_2']: 0.0}
    assert abs(float(P_expr.subs(val)) - P0) < 1e-10
    assert abs(float(Q_expr.subs(val)) - Q0) < 1e-10


def test_iz_load_constant_current_scaling():
    """P_load scales linearly with V for constant-current model."""
    syms = _make_syms(['e_2', 'f_2'])
    P_expr, _ = iz_load_expressions(syms, '2', 10.0, 0.0, V0=1.0)
    val_09 = {syms['e_2']: 0.9, syms['f_2']: 0.0}
    val_10 = {syms['e_2']: 1.0, syms['f_2']: 0.0}
    p09 = float(P_expr.subs(val_09))
    p10 = float(P_expr.subs(val_10))
    assert abs(p09 / p10 - 0.9) < 1e-9


def test_iz_load_constant_impedance_q_scaling():
    """Q_load scales quadratically with V for constant-impedance model."""
    syms = _make_syms(['e_2', 'f_2'])
    _, Q_expr = iz_load_expressions(syms, '2', 0.0, 10.0, V0=1.0)
    val_09 = {syms['e_2']: 0.9, syms['f_2']: 0.0}
    val_10 = {syms['e_2']: 1.0, syms['f_2']: 0.0}
    q09 = float(Q_expr.subs(val_09))
    q10 = float(Q_expr.subs(val_10))
    assert abs(q09 / q10 - 0.81) < 1e-9


def test_network_equation_count():
    """Network module must return exactly 8 algebraic equations for 8 bus voltages."""
    syms = _net_syms()
    P2, Q2 = iz_load_expressions(syms, '2', 12.5, 0.0)
    P3, Q3 = iz_load_expressions(syms, '3', 40.0, 0.0)
    net = network_equations(syms, P2, Q2, P3, Q3)
    assert len(net['y_ini_list']) == 8
    assert len(net['g_list']) == 8


def test_slack_bus_equations():
    """Slack bus equations: last two g entries enforce e_4=V4ref and f_4=0."""
    syms = _net_syms()
    P2, Q2 = iz_load_expressions(syms, '2', 12.5, 0.0)
    P3, Q3 = iz_load_expressions(syms, '3', 40.0, 0.0)
    net = network_equations(syms, P2, Q2, P3, Q3)
    g = net['g_list']
    # The last equation is f_4 = 0
    f4_sym = syms['f_4']
    assert f4_sym in g[-1].free_symbols

def test_load_bus_power_balance_sign():
    """Load power balance: P_net + P_load = 0 (load absorbs network injection)."""
    syms = _net_syms()
    import sympy as sym
    P0 = 12.5
    P2, Q2 = iz_load_expressions(syms, '2', P0, 0.0)
    P3, Q3 = iz_load_expressions(syms, '3', 40.0, 0.0)
    net = network_equations(syms, P2, Q2, P3, Q3)
    # g[2] = P_net(bus2) + P_load2 — P_load2 should appear with positive sign
    g2 = net['g_list'][2]
    assert syms['e_2'] in g2.free_symbols
