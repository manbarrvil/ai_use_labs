"""
IEEEG1 Steam Turbine Governor (IEEE Std 1110, Type 1).

With T1=T2=0 (governor valve instantaneous) and T7=0 (bypass) the model
reduces to 4 states representing the steam chest and reheater stages:

  States: Psv (CV position), Pch (HP chest), Prh (reheater), Pco (crossover)

  Mechanical torque:
    Tm = K1*Pch + (K2+K3)*Prh + (K4+K5)*Pco
       = K1*Pch + K3*Prh + K5*Pco   (since K2=K4=K6=K8=0)

Gate position limits (Pmin, Pmax) and rate limits (Uc, U0) are NOT encoded
symbolically.  At the operating point they are inactive.
"""

def ieeeg1_equations(syms: dict, suffix: str, params: dict) -> dict:
    """
    Build the symbolic equations for one IEEEG1 steam-turbine governor.

    Parameters
    ----------
    syms   : shared symbol namespace
    suffix : generator suffix
    params : dict with keys K, K1, K3, K5, K7, T1, T2, T3, T4, T5, T6, T7,
                          K2, K4, K6, K8, U0, Uc, Pmax, Pmin

    Returns
    -------
    dict with partial system keys.
    """
    s = suffix

    def S(name):
        return syms[f'{name}_{s}']

    # States
    Psv = S('Psv')   # steam-valve position (CV)
    Pch = S('Pch')   # HP chest pressure
    Prh = S('Prh')   # reheater pressure
    Pco = S('Pco')   # crossover pressure

    # Inputs from GENROU
    omega_dev = S('omega')   # rotor speed deviation

    # Output: mechanical torque fed into GENROU swing equation
    Tm = S('Tm')             # algebraic

    p   = params
    K   = p['K']    # governor gain (droop 1/K)
    K1  = p['K1']
    K3  = p['K3']
    K5  = p['K5']
    T3  = p['T3']   # steam-valve actuator time constant
    T4  = p['T4']   # HP chest time constant
    T5  = p['T5']   # reheater time constant
    T6  = p['T6']   # crossover time constant

    # Power reference setpoint (machine pu); keeps Psv=Pm_ref at omega_dev=0
    Pm_ref = syms[f'Pm_ref_{s}']

    # Gate command (T1=T2=0): droop around Pm_ref
    Pgate = Pm_ref + K * (-omega_dev)   # omega_ref deviation = 0 - omega_dev

    # Steam valve actuator
    f_Psv = (Pgate - Psv) / T3

    # HP chest
    f_Pch = (Psv - Pch) / T4

    # Reheater
    f_Prh = (Pch - Prh) / T5

    # Crossover
    f_Pco = (Prh - Pco) / T6

    # Mechanical torque (algebraic equation)
    g_Tm = Tm - (K1 * Pch + K3 * Prh + K5 * Pco)

    x_names = [f'Psv_{s}', f'Pch_{s}', f'Prh_{s}', f'Pco_{s}']
    y_names = [f'Tm_{s}']

    return {
        'x_list':     x_names,
        'y_ini_list': y_names,
        'y_run_list': y_names,
        'f_list':     [f_Psv, f_Pch, f_Prh, f_Pco],
        'g_list':     [g_Tm],
        'h_dict':     {},
        'params_dict': {},
        'u_ini_dict': {},
        'u_run_dict': {},
    }
