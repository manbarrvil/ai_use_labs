"""
IEEE ST4B Excitation System (IEEE 421.5-2016 §7.4).

With the NTS-specified simplification (KIN=0, KG=KI=0, XL_avr=0, θP=0)
the model reduces to a 2-state PI voltage regulator:
  - vm : terminal-voltage measurement filter  (TR)
  - vr : integral state of the voltage error  (KIR/s)

The field voltage output Efd is then:
  Efd = KPM * (KPR * v_error + vr) * KP * |Vt|
where v_error = Vref - vm + Vs (PSS signal).

Limits: vr is anti-windup limited to [VRMIN, VRMAX].
For small-signal analysis the limiter is inactive at the operating point,
so it is NOT included in the symbolic equations (avoids non-smooth functions
that break the Jacobian).  Limits are noted for time-domain use only.
"""

import sympy as sym


def st4b_equations(syms: dict, suffix: str, params: dict) -> dict:
    """
    Build the symbolic equations for one IEEE ST4B exciter.

    Parameters
    ----------
    syms   : shared symbol namespace
    suffix : generator suffix (same as GENROU suffix)
    params : dict with keys TR, KPR, KIR, VRMAX, VRMIN, TA, KPM, KIN,
                          VMMAX, VMMIN, KG, KI, KP, VBMAX, KC, XL_avr, thetaP

    Returns
    -------
    dict with partial system keys
    """
    s = suffix

    def S(name):
        return syms[f'{name}_{s}']

    # States
    vm  = S('vm_avr')   # filtered terminal voltage
    vr  = S('vr_avr')   # PI integrator state (voltage regulator)

    # Inputs / algebraic from other components
    Vt  = S('Vt')       # terminal voltage magnitude (from GENROU h_dict)
    Vs  = S('Vs')       # PSS output (0 if no PSS)
    Vref = S('Vref')    # voltage reference setpoint

    # Output: Efd fed into GENROU
    Efd = S('Efd')      # field voltage (algebraic)

    p = params
    TR  = p['TR']
    KPR = p['KPR']
    KIR = p['KIR']
    TA  = p['TA']
    KPM = p['KPM']
    KP  = p['KP']

    # Voltage measurement filter
    f_vm = (Vt - vm) / TR

    # Error signal
    v_err = Vref - vm + Vs

    # Outer PI regulator integrator (TA is the inner loop time constant, used here
    # for the integrator state rate; with TA very small compared to T, the
    # integrator dominates → 1/KIR is an approximation for the integration)
    f_vr = KIR * v_err

    # Inner PI: Efd = KPM * (KPR*v_err + vr) * KP * Vt
    # Simplified: Efd = KP * KPM * (KPR * v_err + vr) * Vt
    # (for θP=0, XL_avr=0, KC≈0 demagnetization neglected at op. point)
    g_Efd = Efd - KP * KPM * (KPR * v_err + vr) * Vt

    x_names = [f'vm_avr_{s}', f'vr_avr_{s}']
    y_names = [f'Efd_{s}']   # Efd is now algebraic (determined by AVR)

    return {
        'x_list':     x_names,
        'y_ini_list': y_names,
        'y_run_list': y_names,
        'f_list':     [f_vm, f_vr],
        'g_list':     [g_Efd],
        'h_dict':     {},
        'params_dict': {},
        'u_ini_dict': {f'Vref_{s}': 1.0},
        'u_run_dict': {f'Vref_{s}': 1.0},
    }
