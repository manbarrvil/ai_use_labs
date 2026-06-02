"""
IEEE ST1 Excitation System (IEEE 421.5-2016 §7.1, Type ST1A).

With TA=0 (instantaneous HV gate) and Kc=KF=0 the model reduces to:
  - vm   : terminal-voltage measurement filter  (TR)
  - vll  : lead-lag compensator state           (TB, TC)

Efd is algebraic:  Efd = KA * (v_ll + (TC/TB)·v_err)
                       = KA * [lead-lag output on (Vref - vm)]

This corresponds to the proportional-gain-plus-lead-lag structure from
IEEE 421.5 Fig. 7-1 with KF=0 (no derivative feedback).
"""

import sympy as sym


def st1_equations(syms: dict, suffix: str, params: dict) -> dict:
    """
    Build the symbolic equations for one IEEE ST1 exciter.

    Parameters
    ----------
    syms   : shared symbol namespace
    suffix : generator suffix
    params : dict with keys TR, TB, TC, KA, TA, Vimax, Vimin, VRmax, VRmin, Kc, KF, TF

    Returns
    -------
    dict with partial system keys
    """
    s = suffix

    def S(name):
        return syms[f'{name}_{s}']

    # States
    vm  = S('vm_avr')   # filtered terminal voltage
    vll = S('vll_avr')  # lead-lag integrator state

    # Inputs / algebraic
    Vt   = S('Vt')
    Vref = S('Vref')
    Efd  = S('Efd')     # field voltage (algebraic output)

    p   = params
    TR  = p['TR']
    TB  = p['TB']
    TC  = p['TC']
    KA  = p['KA']

    # Voltage measurement
    f_vm = (Vt - vm) / TR

    # Lead-lag compensator (1 + TC·s) / (1 + TB·s):
    # TB * d(vll)/dt = (Vref - vm) - vll
    # y_ll = TC/TB*(Vref - vm) + (1 - TC/TB)*vll  (or equivalently vll + TC/TB*v_err)
    v_err = Vref - vm
    f_vll = (v_err - vll) / TB

    # Efd = KA * lead-lag output  (TA=0: no integrator pole)
    y_ll = vll + (TC / TB) * v_err   # lead-lag output
    g_Efd = Efd - KA * y_ll

    x_names = [f'vm_avr_{s}', f'vll_avr_{s}']
    y_names = [f'Efd_{s}']

    return {
        'x_list':     x_names,
        'y_ini_list': y_names,
        'y_run_list': y_names,
        'f_list':     [f_vm, f_vll],
        'g_list':     [g_Efd],
        'h_dict':     {},
        'params_dict': {},
        'u_ini_dict': {f'Vref_{s}': 1.0},
        'u_run_dict': {f'Vref_{s}': 1.0},
    }
