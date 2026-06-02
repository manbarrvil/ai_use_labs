"""
Assembly of the complete NTS §5.10.2.1 two-machine system.

System components
-----------------
Generator 1 (bus 1, 1500 MVA): GENROU + ST4B AVR + PSS2A
Generator 2 (bus 4, 5000 MVA): GENROU + ST1 AVR + IEEEG1 governor
Network: 4-bus lossless (T1 + line XL + T2)
Loads: IZ at bus 2 (1250 MW) and bus 3 (4000 MW)

Coupling equations added by assembly
-------------------------------------
  Vt_1 = sqrt(e_1^2 + f_1^2)   terminal voltage for ST4B (y_ini/g equation)
  Vt_2 = sqrt(e_4^2 + f_4^2)   terminal voltage for ST1
  Vs_2 = 0                      no PSS on gen 2 (algebraic constant = 0)
  Efd_1, Tm_1 — resolved from ST4B and constant (no governor for gen 1)
  Efd_2, Tm_2 — resolved from ST1 and IEEEG1

Variables removed from u_ini/u_run when provided by a model
------------------------------------------------------------
  Efd_1 : removed from u_ini/u_run (provided by ST4B as y_ini algebraic)
  Efd_2 : removed from u_ini/u_run (provided by ST1  as y_ini algebraic)
  Tm_2  : removed from u_ini/u_run (provided by IEEEG1 as y_ini algebraic)
  Tm_1  : kept in u_ini/u_run (constant mechanical torque, no governor)
"""

import sympy as sym


# ---------------------------------------------------------------------------
# NTS §5.10.2.1 system parameters
# ---------------------------------------------------------------------------

SBASE_SYS = 100.0   # MVA

GEN1_PARAMS = dict(
    H=6.3,   D=0.0,
    Td0p=6.47,  Td0pp=0.022,  Tq0p=0.61,  Tq0pp=0.034,
    xd=2.135,   xq=2.046,
    xdp=0.34,   xqp=0.573,
    xdpp=0.269, xqpp=0.269,
    xl=0.234,   s1=0.1275,   s2=0.2706,
)

GEN2_PARAMS = dict(
    H=6.175, D=0.0,
    Td0p=8.0,   Td0pp=0.03,   Tq0p=0.4,   Tq0pp=0.05,
    xd=1.8,     xq=1.7,
    xdp=0.3,    xqp=0.55,
    xdpp=0.25,  xqpp=0.25,
    xl=0.2,     s1=0.0392,   s2=0.2227,
)

ST4B_PARAMS = dict(
    TR=0.02, KPR=3.15, KIR=3.15, VRMAX=1.0, VRMIN=-0.87,
    TA=0.02, KPM=1.0,  KIN=0.0,  VMMAX=1.0, VMMIN=-0.87,
    KG=0.0,  KI=0.0,   KP=6.5,   VBMAX=8.0, KC=-0.08,
    XL_avr=0.0, thetaP=0.0,
)

ST1_PARAMS = dict(
    TR=0.01, TB=10.0, TC=1.0, KA=200.0, TA=0.0,
    Vimax=999.0, Vimin=-999.0, VRmax=999.0, VRmin=-999.0,
    Kc=0.0, KF=0.0, TF=1.0,
)

PSS2A_PARAMS = dict(
    Tw1=2.0, Tw2=2.0, T6=0.0, Tw3=2.0, Tw4=0.0, T7=2.0,
    Ks2=0.158, Ks3=1.0, T8=0.0, T9=0.1, m=5, n=1,
    Ks1=17.069, T1=0.28, T2=0.04, T3=0.28, T4=0.12,
    VsTmax=0.1, VsTmin=-0.1,
)

IEEEG1_PARAMS = dict(
    K=20.0, K1=0.3, K3=0.3, K5=0.4, K7=0.0,
    T1=0.0, T2=0.0, T3=0.1, T4=0.3, T5=7.0, T6=0.6, T7=0.0,
    K2=0.0, K4=0.0, K6=0.0, K8=0.0,
    U0=0.5, Uc=-0.5, Pmax=1.0, Pmin=0.0,
)

# Power flow (system pu, Sbase=100 MVA)
PF = dict(
    P_gen1=1350.0 / SBASE_SYS,   # 13.5 pu
    P_gen2=3900.0 / SBASE_SYS,   # 39.0 pu
    P_load2=1250.0 / SBASE_SYS,  # 12.5 pu
    Q_load2=0.0,
    P_load3=4000.0 / SBASE_SYS,  # 40.0 pu
    Q_load3=0.0,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_syms(names: list[str]) -> dict:
    """Create a dict of SymPy real symbols from a list of name strings."""
    return {n: sym.Symbol(n, real=True) for n in names}


def _merge(base: dict, patch: dict) -> None:
    """In-place deep merge of patch into base (lists concatenated, dicts updated)."""
    for key, val in patch.items():
        if key in ('x_list', 'y_ini_list', 'y_run_list', 'f_list', 'g_list'):
            base.setdefault(key, []).extend(val)
        elif key in ('h_dict', 'params_dict', 'u_ini_dict', 'u_run_dict'):
            base.setdefault(key, {}).update(val)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def assemble_system(Sbase: float = SBASE_SYS) -> dict:
    """
    Build the complete pydae system_dict for the NTS two-machine benchmark.

    The returned dict is ready to be passed to ``Builder(system_dict).build()``.

    Parameters
    ----------
    Sbase : float
        System MVA base (default 100 MVA).

    Returns
    -------
    dict — complete pydae system_dict with name 'nts2gen'
    """
    from nts_emo.models.genrou  import genrou_equations
    from nts_emo.models.avr_st4b import st4b_equations
    from nts_emo.models.avr_st1  import st1_equations
    from nts_emo.models.pss2a    import pss2a_equations
    from nts_emo.models.ieeeg1   import ieeeg1_equations
    from nts_emo.models.iz_load  import iz_load_expressions
    from nts_emo.network         import network_equations

    # ------------------------------------------------------------------
    # 1. Build the global symbol namespace
    #    All symbols must be created with real=True and shared across
    #    all component functions so that SymPy treats them as identical.
    # ------------------------------------------------------------------
    all_names = [
        # Machine 1 states
        'delta_1', 'omega_1', 'eqp_1', 'edp_1', 'psi1d_1', 'psi2q_1',
        # Machine 1 AVR states
        'vm_avr_1', 'vr_avr_1',
        # Machine 1 PSS states
        'sw1a_1', 'sw1b_1', 'sw2_1', 'st7_1', 'sll1_1', 'sll2_1',
        # Machine 2 states
        'delta_2', 'omega_2', 'eqp_2', 'edp_2', 'psi1d_2', 'psi2q_2',
        # Machine 2 AVR states
        'vm_avr_2', 'vll_avr_2',
        # Machine 2 governor states
        'Psv_2', 'Pch_2', 'Prh_2', 'Pco_2',
        # Machine 1 algebraic
        'id_1', 'iq_1', 'Vd_1', 'Vq_1', 'Eqpp_1', 'Edpp_1',
        'Igen_e_1', 'Igen_f_1', 'Pe_1',
        'Efd_1', 'Vt_1', 'Vs_1',
        # Machine 2 algebraic
        'id_2', 'iq_2', 'Vd_2', 'Vq_2', 'Eqpp_2', 'Edpp_2',
        'Igen_e_2', 'Igen_f_2', 'Pe_2',
        'Efd_2', 'Tm_2', 'Vt_2', 'Vs_2',
        # Network bus voltages
        'e_1', 'f_1', 'e_2', 'f_2', 'e_3', 'f_3', 'e_4', 'f_4',
        # Parameters / inputs
        'XL', 'V4ref', 'Vref_1', 'Vref_2', 'Tm_1', 'Pm_ref_2',
    ]
    syms = _make_syms(all_names)

    # ------------------------------------------------------------------
    # 2. Get partial dicts from each component
    # ------------------------------------------------------------------
    gen1  = genrou_equations(syms, '1', '1', 1500.0, Sbase, GEN1_PARAMS)
    st4b1 = st4b_equations(syms, '1', ST4B_PARAMS)
    pss1  = pss2a_equations(syms, '1', PSS2A_PARAMS)
    gen2  = genrou_equations(syms, '2', '4', 5000.0, Sbase, GEN2_PARAMS)
    st1_2 = st1_equations(syms, '2', ST1_PARAMS)
    gov2  = ieeeg1_equations(syms, '2', IEEEG1_PARAMS)

    P_load2, Q_load2 = iz_load_expressions(syms, '2', PF['P_load2'], PF['Q_load2'])
    P_load3, Q_load3 = iz_load_expressions(syms, '3', PF['P_load3'], PF['Q_load3'])
    net = network_equations(syms, P_load2, Q_load2, P_load3, Q_load3)

    # ------------------------------------------------------------------
    # 3. Start with an empty skeleton
    # ------------------------------------------------------------------
    sys = {
        'name':        'nts2gen',
        'x_list':      [],
        'y_ini_list':  [],
        'y_run_list':  [],
        'f_list':      [],
        'g_list':      [],
        'h_dict':      {},
        'params_dict': {'alpha_solver': 0.5, 'XL': 0.3},
        'u_ini_dict':  {},
        'u_run_dict':  {},
    }

    # Merge all components
    for part in [gen1, st4b1, pss1, gen2, st1_2, gov2, net]:
        _merge(sys, part)

    # ------------------------------------------------------------------
    # 4. Add coupling algebraic equations
    #    These link GENROU outputs to AVR/PSS inputs and vice versa.
    # ------------------------------------------------------------------
    e1 = syms['e_1'];  f1 = syms['f_1']
    e4 = syms['e_4'];  f4 = syms['f_4']
    Vt1 = syms['Vt_1'];  Vt2 = syms['Vt_2']
    Vs2 = syms['Vs_2']

    # Terminal voltage magnitude equations (sqrt — needed by AVRs)
    g_Vt1 = Vt1 - sym.sqrt(e1**2 + f1**2)
    g_Vt2 = Vt2 - sym.sqrt(e4**2 + f4**2)

    # Gen 2 has no PSS → Vs_2 = 0
    g_Vs2 = Vs2

    coupling_y = ['Vt_1', 'Vt_2', 'Vs_2']
    coupling_g = [g_Vt1, g_Vt2, g_Vs2]

    sys['y_ini_list'].extend(coupling_y)
    sys['y_run_list'].extend(coupling_y)
    sys['g_list'].extend(coupling_g)

    # ------------------------------------------------------------------
    # 5. Resolve control connections:
    #    Efd_1 and Efd_2 come from AVRs (algebraic).
    #    Tm_2 comes from IEEEG1 (algebraic).
    #    Tm_1 is a user input (constant mechanical torque — no governor).
    #    Remove them from u_ini/u_run; they are already in y_ini via AVR/governor.
    # ------------------------------------------------------------------
    for key in ('Efd_1', 'Efd_2', 'Tm_2'):
        sys['u_ini_dict'].pop(key, None)
        sys['u_run_dict'].pop(key, None)

    # Tm_1 stays as input (constant) — initial value set during ini()
    # Vref_1, Vref_2 are voltage reference setpoints (inputs)
    # V4ref is the slack-bus reference voltage (input, =1.0)

    # ------------------------------------------------------------------
    # 6. Move Vt_k from h_dict to y_ini (they were in GENROU h_dict as outputs).
    #    pydae can have both — h_dict is fine for observation; coupling uses y_ini.
    #    Keep them in h_dict too so they appear in z_list for post-processing.
    # ------------------------------------------------------------------

    # ------------------------------------------------------------------
    # 7. Default parameter and input values
    # ------------------------------------------------------------------
    # Operating-point inputs (set during ini() — approximated here as flat start)
    pu_tm1    = PF['P_gen1'] * Sbase / 1500.0   # machine-pu mech. torque gen 1
    pu_pm2    = PF['P_gen2'] * Sbase / 5000.0   # machine-pu power ref for gov gen 2
    sys['u_ini_dict'].update({
        'Tm_1':    pu_tm1,
        'Pm_ref_2': pu_pm2,
        'Vref_1': 1.0,
        'Vref_2': 1.0,
        'V4ref':  1.0,
    })
    sys['u_run_dict'].update({
        'Tm_1':    pu_tm1,
        'Pm_ref_2': pu_pm2,
        'Vref_1': 1.0,
        'Vref_2': 1.0,
        'V4ref':  1.0,
    })

    return sys


def get_system_info(sys: dict) -> dict:
    """Return a summary of variable counts for debugging."""
    return {
        'N_x': len(sys['x_list']),
        'N_y_ini': len(sys['y_ini_list']),
        'N_y_run': len(sys['y_run_list']),
        'N_f': len(sys['f_list']),
        'N_g': len(sys['g_list']),
        'N_params': len(sys['params_dict']),
        'N_u_ini': len(sys['u_ini_dict']),
        'N_u_run': len(sys['u_run_dict']),
    }
