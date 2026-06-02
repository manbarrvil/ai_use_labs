"""Tests for the system assembly (no compilation required)."""

import pytest
from nts_emo.assembly import assemble_system, get_system_info


@pytest.fixture(scope='module')
def sys_dict():
    return assemble_system()


def test_no_duplicate_states(sys_dict):
    x = sys_dict['x_list']
    assert len(x) == len(set(x)), f'Duplicate states: {[s for s in x if x.count(s)>1]}'


def test_no_duplicate_algebraic(sys_dict):
    y = sys_dict['y_ini_list']
    assert len(y) == len(set(y)), f'Duplicate algebraic: {[s for s in y if y.count(s)>1]}'


def test_state_equation_count_matches(sys_dict):
    assert len(sys_dict['x_list']) == len(sys_dict['f_list']), (
        f"States: {len(sys_dict['x_list'])}, ODEs: {len(sys_dict['f_list'])}"
    )


def test_algebraic_equation_count_matches(sys_dict):
    assert len(sys_dict['y_ini_list']) == len(sys_dict['g_list']), (
        f"Algebraic vars: {len(sys_dict['y_ini_list'])}, "
        f"Algebraic eqs: {len(sys_dict['g_list'])}"
    )


def test_expected_state_count(sys_dict):
    # Gen1: 6 + ST4B: 2 + PSS2A: 6 + Gen2: 6 + ST1: 2 + IEEEG1: 4 = 26
    N = len(sys_dict['x_list'])
    assert N == 26, f'Expected 26 states, got {N}: {sys_dict["x_list"]}'


def test_xl_in_params(sys_dict):
    assert 'XL' in sys_dict['params_dict'], "XL must be in params_dict"


def test_efd_not_in_inputs(sys_dict):
    """Efd_1 and Efd_2 must NOT appear in u_ini_dict (provided by AVRs)."""
    assert 'Efd_1' not in sys_dict['u_ini_dict']
    assert 'Efd_2' not in sys_dict['u_ini_dict']


def test_tm2_not_in_inputs(sys_dict):
    """Tm_2 must NOT appear in u_ini_dict (provided by IEEEG1)."""
    assert 'Tm_2' not in sys_dict['u_ini_dict']


def test_tm1_in_inputs(sys_dict):
    """Tm_1 must remain as input (no governor for gen 1)."""
    assert 'Tm_1' in sys_dict['u_ini_dict']


def test_system_name(sys_dict):
    assert sys_dict['name'] == 'nts2gen'


def test_all_f_symbols_declared(sys_dict):
    """All free symbols in f_list must be declared (x, y, u, or params)."""
    import sympy as sym
    declared = set(sys_dict['x_list'] +
                   sys_dict['y_ini_list'] +
                   list(sys_dict['u_ini_dict'].keys()) +
                   list(sys_dict['params_dict'].keys()))
    undeclared = set()
    for expr in sys_dict['f_list']:
        if hasattr(expr, 'free_symbols'):
            for s in expr.free_symbols:
                if s.name not in declared:
                    undeclared.add(s.name)
    assert not undeclared, f'Undeclared symbols in f_list: {sorted(undeclared)}'


def test_all_g_symbols_declared(sys_dict):
    """All free symbols in g_list must be declared."""
    import sympy as sym
    declared = set(sys_dict['x_list'] +
                   sys_dict['y_ini_list'] +
                   list(sys_dict['u_ini_dict'].keys()) +
                   list(sys_dict['params_dict'].keys()))
    undeclared = set()
    for expr in sys_dict['g_list']:
        if hasattr(expr, 'free_symbols'):
            for s in expr.free_symbols:
                if s.name not in declared:
                    undeclared.add(s.name)
    assert not undeclared, f'Undeclared symbols in g_list: {sorted(undeclared)}'
