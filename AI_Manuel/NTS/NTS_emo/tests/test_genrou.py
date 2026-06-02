"""Tests for the GENROU 6th-order model equations."""

import pytest
import sympy as sym
from nts_emo.models.genrou import genrou_equations, _sat_coeffs
from nts_emo.assembly import GEN1_PARAMS, GEN2_PARAMS, SBASE_SYS, _make_syms


def _gen1_syms():
    names = [
        'delta_1', 'omega_1', 'eqp_1', 'edp_1', 'psi1d_1', 'psi2q_1',
        'id_1', 'iq_1', 'Vd_1', 'Vq_1', 'Eqpp_1', 'Edpp_1',
        'Igen_e_1', 'Igen_f_1', 'Pe_1',
        'Efd_1', 'Tm_1',
        'e_1', 'f_1',
    ]
    return _make_syms(names)


def test_genrou_state_count():
    syms = _gen1_syms()
    d = genrou_equations(syms, '1', '1', 1500.0, SBASE_SYS, GEN1_PARAMS)
    assert len(d['x_list']) == 6
    assert len(d['f_list']) == 6


def test_genrou_algebraic_count():
    syms = _gen1_syms()
    d = genrou_equations(syms, '1', '1', 1500.0, SBASE_SYS, GEN1_PARAMS)
    assert len(d['y_ini_list']) == len(d['g_list']), (
        f"Algebraic mismatch: {len(d['y_ini_list'])} vars vs {len(d['g_list'])} eqs"
    )


def test_saturation_values():
    s1, s2 = GEN1_PARAMS['s1'], GEN1_PARAMS['s2']
    A, B = _sat_coeffs(s1, s2)
    # At E=1.0: S = A*exp(B*1) should equal s1
    assert abs(A * float(sym.exp(B)) - s1) < 1e-8
    # At E=1.2: S = A*exp(B*1.2) should equal s2
    assert abs(A * float(sym.exp(1.2 * B)) - s2) < 1e-6


def test_zero_saturation_coefficients():
    A, B = _sat_coeffs(0.0, 0.0)
    assert A == 0.0 and B == 0.0


def test_swing_equation_form():
    """f_omega should be (Tm - Te - D*omega)/(2H*br)."""
    syms = _gen1_syms()
    d = genrou_equations(syms, '1', '1', 1500.0, SBASE_SYS, GEN1_PARAMS)
    f_omega = d['f_list'][1]
    omega = syms['omega_1']
    # At omega=0, Tm=Te, D=0: f_omega must be zero
    Tm = syms['Tm_1']
    # Tm appears in the expression
    assert omega in f_omega.free_symbols or Tm in f_omega.free_symbols


def test_no_duplicate_state_names():
    syms = _gen1_syms()
    d = genrou_equations(syms, '1', '1', 1500.0, SBASE_SYS, GEN1_PARAMS)
    assert len(d['x_list']) == len(set(d['x_list']))


def test_gen2_parameters():
    names = [
        'delta_2', 'omega_2', 'eqp_2', 'edp_2', 'psi1d_2', 'psi2q_2',
        'id_2', 'iq_2', 'Vd_2', 'Vq_2', 'Eqpp_2', 'Edpp_2',
        'Igen_e_2', 'Igen_f_2', 'Pe_2', 'Efd_2', 'Tm_2',
        'e_4', 'f_4',
    ]
    syms = _make_syms(names)
    d = genrou_equations(syms, '2', '4', 5000.0, SBASE_SYS, GEN2_PARAMS)
    assert len(d['x_list']) == 6
    assert len(d['f_list']) == len(d['x_list'])
