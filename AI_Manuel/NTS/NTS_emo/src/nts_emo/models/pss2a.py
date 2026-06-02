"""
IEEE PSS2A Power System Stabiliser (IEEE 421.5-2016 §8.2).

Two input signals:
  u1 = rotor speed deviation  (omega_dev)
  u2 = generator electrical power  (Pe)

Signal chain:
  u1 → washout Tw1 → washout Tw2 → w1
  u2 → Ks2 gain → washout Tw3 → ramp-tracking T7/Ks3 → w2
       (T6 transducer = 0, T8/T9 band-pass = 0 here since T8=0)
  w1 + w2 → lead-lag (T1,T2) → lead-lag (T3,T4) → Ks1 gain → clamp → Vs

States (6): sw1a, sw1b, sw2, st7, sll1, sll2

With T6=0, T8=0 the transducer and band-pass blocks are bypassed.
Limiter [VsTmin, VsTmax] is not encoded symbolically (not smooth → bad Jacobian).
"""

import sympy as sym


def pss2a_equations(syms: dict, suffix: str, params: dict) -> dict:
    """
    Build the symbolic equations for one IEEE PSS2A stabiliser.

    Parameters
    ----------
    syms   : shared symbol namespace
    suffix : generator suffix
    params : dict with keys Tw1, Tw2, T6, Tw3, Tw4, T7, Ks2, Ks3,
                          T8, T9, m, n, Ks1, T1, T2, T3, T4,
                          VsTmax, VsTmin

    Returns
    -------
    dict with partial system keys.
    """
    s = suffix

    def S(name):
        return syms[f'{name}_{s}']

    # States
    sw1a = S('sw1a')  # first washout state for input 1
    sw1b = S('sw1b')  # second washout state for input 1
    sw2  = S('sw2')   # washout state for input 2
    st7  = S('st7')   # ramp-tracking state (T7)
    sll1 = S('sll1')  # first lead-lag integrator state
    sll2 = S('sll2')  # second lead-lag integrator state

    # Algebraic output
    Vs = S('Vs')       # PSS output voltage signal

    # Inputs from GENROU
    omega_dev = S('omega')   # rotor speed deviation (same symbol as GENROU state)
    Pe        = S('Pe')      # electrical power output

    p    = params
    Tw1  = p['Tw1']
    Tw2  = p['Tw2']
    Tw3  = p['Tw3']
    T7   = p['T7']
    Ks2  = p['Ks2']
    Ks3  = p['Ks3']
    Ks1  = p['Ks1']
    T1   = p['T1']
    T2   = p['T2']
    T3   = p['T3']
    T4   = p['T4']

    # ------------------------------------------------------------------
    # Signal path for input 1: washout × 2
    # Washout H(s) = Tw·s/(1+Tw·s): state x, output y = u - x  (NOT u - x/Tw)
    # d(x)/dt = (u - x) / Tw  →  at DC: x→u, y→0  ✓
    # ------------------------------------------------------------------
    f_sw1a = (omega_dev - sw1a) / Tw1
    y_w1a  = omega_dev - sw1a        # correct washout output

    f_sw1b = (y_w1a - sw1b) / Tw2
    y_w1b  = y_w1a - sw1b

    # ------------------------------------------------------------------
    # Signal path for input 2: Ks2 gain + single washout
    # ------------------------------------------------------------------
    u2 = Ks2 * Pe
    f_sw2 = (u2 - sw2) / Tw3
    y_w2  = u2 - sw2

    # ------------------------------------------------------------------
    # Ramp-tracking filter: Ks3·T7·s/(1+T7·s)
    # ------------------------------------------------------------------
    f_st7 = (y_w2 - st7) / T7
    y_t7  = Ks3 * (y_w2 - st7)

    # Combined signal
    y_in = y_w1b + y_t7

    # ------------------------------------------------------------------
    # Lead-lag 1: (1 + T1·s)/(1 + T2·s)
    # d(sll1)/dt = (y_in - sll1) / T2
    # output = (T1/T2) * y_in + (1 - T1/T2) * sll1
    # ------------------------------------------------------------------
    f_sll1 = (y_in - sll1) / T2
    y_ll1  = (T1 / T2) * y_in + (1.0 - T1 / T2) * sll1

    # ------------------------------------------------------------------
    # Lead-lag 2: (1 + T3·s)/(1 + T4·s)
    # ------------------------------------------------------------------
    f_sll2 = (y_ll1 - sll2) / T4
    y_ll2  = (T3 / T4) * y_ll1 + (1.0 - T3 / T4) * sll2

    # ------------------------------------------------------------------
    # Final gain Ks1 and algebraic output Vs
    # (Limiter omitted for small-signal analysis)
    # ------------------------------------------------------------------
    g_Vs = Vs - Ks1 * y_ll2

    x_names = [f'sw1a_{s}', f'sw1b_{s}', f'sw2_{s}',
               f'st7_{s}',  f'sll1_{s}', f'sll2_{s}']
    y_names = [f'Vs_{s}']

    return {
        'x_list':     x_names,
        'y_ini_list': y_names,
        'y_run_list': y_names,
        'f_list':     [f_sw1a, f_sw1b, f_sw2, f_st7, f_sll1, f_sll2],
        'g_list':     [g_Vs],
        'h_dict':     {},
        'params_dict': {},
        'u_ini_dict': {},
        'u_run_dict': {},
    }
