"""
Full PI-VSG + VC-ICL nonlinear DAE model (grid-forming VSC)
Source: Matas-Díaz et al., "A Systematic Small-signal …", JMPSCE 2025
        §II.A (LCL filter), §II.B (OCL), §II.C.1 (VC-ICL), eqs. (1)-(16)

System:  dx/dt = f(x, y, u)      — 13 differential states
          0    = g(x, y, u)      —  8 algebraic variables

Architecture:
  [p*, q*] ─► PI-VSG OCL ─► [omega_vsg, E]
                                    │
                       VC-ICL (cascaded PI) ◄── [i_t, v_m, i_s]
                            │ (outer: voltage loop)
                            │ (inner: current loop)
                                    │
                               [v_td, v_tq]
                                    │
                            LCL Filter + Grid Thevenin
                                    │
                                [v_g, i_t, i_s]

State variables x (13)
----------------------
  LCL Filter:
    i_td, i_tq  : VSC-side inductor currents, dq   (eq. 1)
    v_md, v_mq  : Capacitor voltage, dq             (eq. 2a)
    i_sd, i_sq  : Grid-side currents, dq            (eqs. 2b + 4)
  PI-VSG OCL:
    psi         : Phase angle difference ψ = θ_g − θ_vsg  (eq. 11a)
    xi_p        : Integral of active power error           (eq. 11b)
    xi_q        : Integral of reactive power error         (eq. 9b)
  VC-ICL:
    xi_vd, xi_vq : Voltage error integrals, dq   (eq. 14, outer loop)
    xi_id, xi_iq : Current error integrals, dq   (eq. 15, inner loop)

Algebraic variables y (8)
--------------------------
  v_td, v_tq   : VSC terminal voltage (inner current-loop output, eq. 15)
  omega_vsg    : VSG angular speed    (PI-VSG, algebraic from dψ/dt)
  E            : Virtual EMF          (RPCL, eq. 9a)
  v_sd, v_sq   : PCC voltage          (from grid Thevenin + filter)
  p, q         : Active/reactive power at POI

Intermediate expressions (substituted inline — not SymPy algebraic vars)
--------------------------------------------------------------------------
  v_md_star, v_mq_star  : Voltage references from virtual impedance (eq. 13)
  i_td_star, i_tq_star  : Current references from PI voltage controller (eq. 14)

External inputs u
-----------------
  p_star, q_star : Power references
  v_gd, v_gq    : Grid Thevenin voltage (dq)

Parameters (Table I, paper)
----------------------------
  See params dict below.
"""

import numpy as np
import sympy as sp

# ---------------------------------------------------------------------------
# 1. Symbols
# ---------------------------------------------------------------------------
# State variables
i_td, i_tq           = sp.symbols('i_td i_tq',           real=True)
v_md, v_mq           = sp.symbols('v_md v_mq',           real=True)
i_sd, i_sq           = sp.symbols('i_sd i_sq',           real=True)
psi                   = sp.Symbol ('psi',                  real=True)
xi_p, xi_q           = sp.symbols('xi_p xi_q',           real=True)
xi_vd, xi_vq         = sp.symbols('xi_vd xi_vq',         real=True)
xi_id, xi_iq         = sp.symbols('xi_id xi_iq',         real=True)

# Algebraic variables
v_td, v_tq   = sp.symbols('v_td v_tq',     real=True)
omega_vsg     = sp.Symbol ('omega_vsg',     real=True)
E             = sp.Symbol ('E',             real=True, positive=True)
v_sd, v_sq   = sp.symbols('v_sd v_sq',     real=True)
p, q         = sp.symbols('p q',           real=True)

# External inputs
p_star, q_star = sp.symbols('p_star q_star', real=True)
v_gd, v_gq   = sp.symbols('v_gd v_gq',     real=True)

# Parameters
L_t     = sp.Symbol('L_t',     real=True, positive=True)
R_t     = sp.Symbol('R_t',     real=True, positive=True)
C_f     = sp.Symbol('C_f',     real=True, positive=True)
R_d     = sp.Symbol('R_d',     real=True, positive=True)
L_s     = sp.Symbol('L_s',     real=True, positive=True)
R_s     = sp.Symbol('R_s',     real=True, positive=True)
L_g     = sp.Symbol('L_g',     real=True, positive=True)
R_g     = sp.Symbol('R_g',     real=True, positive=True)
k_pp    = sp.Symbol('k_pp',    real=True, positive=True)
k_ip    = sp.Symbol('k_ip',    real=True, positive=True)
k_pq    = sp.Symbol('k_pq',    real=True, positive=True)
k_iq    = sp.Symbol('k_iq',    real=True, positive=True)
E_0     = sp.Symbol('E_0',     real=True, positive=True)
omega_0 = sp.Symbol('omega_0', real=True, positive=True)
R_v     = sp.Symbol('R_v',     real=True)           # virtual resistance
X_v     = sp.Symbol('X_v',     real=True)           # virtual reactance
kpv_vc  = sp.Symbol('kpv_vc',  real=True, positive=True)  # voltage-loop P gain
kiv_vc  = sp.Symbol('kiv_vc',  real=True, positive=True)  # voltage-loop I gain
kpi_vc  = sp.Symbol('kpi_vc',  real=True, positive=True)  # current-loop P gain
kii_vc  = sp.Symbol('kii_vc',  real=True, positive=True)  # current-loop I gain

# ---------------------------------------------------------------------------
# 2. Named lists
# ---------------------------------------------------------------------------
x_list  = [i_td, i_tq, v_md, v_mq, i_sd, i_sq,
           psi, xi_p, xi_q,
           xi_vd, xi_vq, xi_id, xi_iq]

y_list  = [v_td, v_tq, omega_vsg, E, v_sd, v_sq, p, q]

x_names = ['i_td', 'i_tq', 'v_md', 'v_mq', 'i_sd', 'i_sq',
           'psi', 'xi_p', 'xi_q',
           'xi_vd', 'xi_vq', 'xi_id', 'xi_iq']

y_names = ['v_td', 'v_tq', 'omega_vsg', 'E', 'v_sd', 'v_sq', 'p', 'q']

# ---------------------------------------------------------------------------
# 3. Default parameters (Table I, paper)
# ---------------------------------------------------------------------------
params = {
    L_t:    1.25e-3,     # [H]       VSC-side inductor
    R_t:    0.04,        # [Ω]       VSC-side resistance
    C_f:    4e-6,        # [F]       Filter capacitor
    R_d:    10.0,        # [Ω]       Parallel damping
    L_s:    1.25e-3,     # [H]       Grid-side inductor
    R_s:    0.04,        # [Ω]       Grid-side resistance
    L_g:    2e-3,        # [H]       Grid Thevenin inductor
    R_g:    2.0,         # [Ω]       Grid Thevenin resistance
    k_pp:   0.0012,      # [rad/s/W] PI-VSG proportional gain
    k_ip:   0.0016,      # [rad/s²/W]PI-VSG integral gain
    k_pq:   0.0016,      # [V/W]     RPCL proportional gain
    k_iq:   0.0163,      # [V/W/s]   RPCL integral gain
    E_0:    230.0,       # [V]       Rated virtual EMF
    omega_0: 100*np.pi,  # [rad/s]   Rated speed (50 Hz)
    R_v:    0.0,         # [Ω]       Virtual resistance (0 in paper)
    X_v:    0.08,        # [Ω]       Virtual reactance  (= ω₀·L_v)
    kpv_vc: 0.1,         # [A/V]     Voltage-loop proportional gain
    kiv_vc: 0.1,         # [A/V/s]   Voltage-loop integral gain
    kpi_vc: 0.1,         # [V/A]     Current-loop proportional gain
    kii_vc: 15.1,        # [V/A/s]   Current-loop integral gain
}

# ---------------------------------------------------------------------------
# 4. Intermediate constants
# ---------------------------------------------------------------------------
L_sg  = L_s + L_g
R_sg  = R_s + R_g
alpha = L_g / L_sg                        # voltage divider (PCC equation)
R_mix = (R_g*L_s - R_s*L_g) / L_sg       # residual resistance (PCC equation)

# ---------------------------------------------------------------------------
# 5. Intermediate expressions — VC-ICL (substituted inline)
# ---------------------------------------------------------------------------
# Virtual impedance (eq. 13): v_m* = e - Z_v·i_s, e = [0, E]^T
# Z_v = [[R_v, -X_v], [X_v, R_v]]
v_md_star = -R_v*i_sd + X_v*i_sq          # d-axis (e_d = 0)
v_mq_star =  E - X_v*i_sd - R_v*i_sq     # q-axis (e_q = E)

# PI voltage controller output (eq. 14)
# i_t* = k_pv·(dξ_v/dt) + k_iv·ξ_v + ω·C·v_m + i_s
# Cross-coupling: j·ω·C·v_m → d: −ω·C·v_mq,  q: +ω·C·v_md
i_td_star = (kpv_vc*(v_md_star - v_md)
             + kiv_vc*xi_vd
             - omega_vsg*C_f*v_mq          # dq cross-coupling cancelation
             + i_sd)                        # load current feed-forward

i_tq_star = (kpv_vc*(v_mq_star - v_mq)
             + kiv_vc*xi_vq
             + omega_vsg*C_f*v_md          # dq cross-coupling cancelation
             + i_sq)                        # load current feed-forward

# ---------------------------------------------------------------------------
# 6. Differential equations  f: dx/dt = f(x, y, u)
# ---------------------------------------------------------------------------

# --- LCL Filter ---
# VSC-side inductor (eq. 1)
f1  = (v_td - R_t*i_td + omega_vsg*L_t*i_tq - v_md) / L_t
f2  = (v_tq - R_t*i_tq - omega_vsg*L_t*i_td - v_mq) / L_t

# Capacitor with parallel damping R_d (eq. 2a)
f3  = (i_td - i_sd - v_md/R_d + omega_vsg*C_f*v_mq) / C_f
f4  = (i_tq - i_sq - v_mq/R_d - omega_vsg*C_f*v_md) / C_f

# Grid-side inductor + grid Thevenin combined (eqs. 2b + 4)
f5  = (v_md - v_gd - R_sg*i_sd + omega_vsg*L_sg*i_sq) / L_sg
f6  = (v_mq - v_gq - R_sg*i_sq - omega_vsg*L_sg*i_sd) / L_sg

# --- PI-VSG Outer Control Loop ---
# APCL (eq. 11)
f7  = -k_pp*(p_star - p) - k_ip*xi_p    # d(ψ)/dt
f8  = p_star - p                          # d(ξ_p)/dt
# RPCL (eq. 9b)
f9  = q_star - q                          # d(ξ_q)/dt

# --- VC-ICL ---
# Voltage error integrals (outer loop, eq. 14: dξ_v/dt = v_m* - v_m)
f10 = v_md_star - v_md                    # d(ξ_vd)/dt
f11 = v_mq_star - v_mq                    # d(ξ_vq)/dt

# Current error integrals (inner loop, eq. 15: dξ_i/dt = i_t* - i_t)
f12 = i_td_star - i_td                    # d(ξ_id)/dt
f13 = i_tq_star - i_tq                    # d(ξ_iq)/dt

f_list = [f1, f2, f3, f4, f5, f6, f7, f8, f9, f10, f11, f12, f13]

# ---------------------------------------------------------------------------
# 7. Algebraic equations  g: 0 = g(x, y, u)
# ---------------------------------------------------------------------------

# VC-ICL inner current-loop output (eq. 15)
# v_t = k_pi·(dξ_i/dt) + k_ii·ξ_i + ω·L_t·i_t + v_m
# Cross-coupling: j·ω·L_t·i_t → d: +ω·L_t·i_tq,  q: −ω·L_t·i_td
g1 = v_td - (kpi_vc*(i_td_star - i_td)
             + kii_vc*xi_id
             + omega_vsg*L_t*i_tq          # cross-coupling cancelation
             + v_md)                        # capacitor voltage feed-forward

g2 = v_tq - (kpi_vc*(i_tq_star - i_tq)
             + kii_vc*xi_iq
             - omega_vsg*L_t*i_td          # cross-coupling cancelation
             + v_mq)                        # capacitor voltage feed-forward

# PI-VSG angular speed (from dψ/dt = ω_0 − ω_vsg, eq. 11a)
g3 = omega_vsg - omega_0 - k_pp*(p_star - p) - k_ip*xi_p

# RPCL virtual EMF (eq. 9a)
g4 = E - E_0 - k_pq*(q_star - q) - k_iq*xi_q

# PCC voltage (eqs. 2b + 4 combined)
g5 = v_sd - ((1 - alpha)*v_gd + alpha*v_md + R_mix*i_sd)
g6 = v_sq - ((1 - alpha)*v_gq + alpha*v_mq + R_mix*i_sq)

# Active and reactive power at POI
g7 = p - (v_sd*i_sd + v_sq*i_sq)
g8 = q - (v_sq*i_sd - v_sd*i_sq)

g_list = [g1, g2, g3, g4, g5, g6, g7, g8]

# ---------------------------------------------------------------------------
# 8. Verification helpers
# ---------------------------------------------------------------------------
def _all_free_symbols():
    all_sym = set()
    for eq in f_list + g_list:
        all_sym |= eq.free_symbols
    return all_sym


def check_model():
    assert len(x_list) == len(f_list), \
        f"State/f-equation count mismatch: {len(x_list)} vs {len(f_list)}"
    assert len(y_list) == len(g_list), \
        f"Algebraic/g-equation count mismatch: {len(y_list)} vs {len(g_list)}"

    declared = (set(x_list) | set(y_list)
                | {p_star, q_star, v_gd, v_gq}
                | set(params))
    undeclared = _all_free_symbols() - declared
    assert not undeclared, f"Undeclared symbols: {undeclared}"

    print("Model check passed:")
    print(f"  States     ({len(x_list):2d}) : {x_names}")
    print(f"  Algebraic  ({len(y_list):2d}) : {y_names}")
    print(f"  Parameters ({len(params):2d}) : {[str(k) for k in params]}")


# ---------------------------------------------------------------------------
# 9. PDF generation — 2 pages
# ---------------------------------------------------------------------------
def generate_pdf(filename: str = 'pi_vsg_vc_model.pdf') -> None:
    """Render the full PI-VSG + VC-ICL DAE model to a 2-page A4 PDF."""
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages

    def _t(s):
        return f'${s}$'

    def make_page():
        fig = plt.figure(figsize=(8.27, 11.69))
        ax  = fig.add_axes([0.0, 0.0, 1.0, 1.0])
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        return fig, ax

    def put(ax, x, y, s, **kw):
        ax.text(x, y, s, transform=ax.transAxes, va='top', **kw)

    def hline(ax, y, color='#888888', lw=0.7):
        ax.plot([0.06, 0.94], [y, y], color=color, linewidth=lw,
                transform=ax.transAxes, clip_on=False)

    L = 0.07

    # -----------------------------------------------------------------------
    # PAGE 1 — Title + Tables
    # -----------------------------------------------------------------------
    fig1, ax1 = make_page()

    y = 0.965
    put(ax1, 0.5, y,
        'Full PI-VSG + VC-ICL  —  Nonlinear DAE Model',
        ha='center', fontsize=13, fontweight='bold')
    y -= 0.030
    put(ax1, 0.5, y,
        'Matas-Díaz et al., JMPSCE 2025, §II.A–II.C.1, eqs. (1)–(16)',
        ha='center', fontsize=8.5, color='#555555', style='italic')
    y -= 0.018
    hline(ax1, y, color='#222222', lw=1.2)
    y -= 0.022

    put(ax1, L, y, 'System architecture', fontsize=10.5, fontweight='bold')
    y -= 0.024
    for line in [
        r'$\mathbf{dx/dt = f(x,y,u)}$  (13 differential states)     '
        r'$\mathbf{0 = g(x,y,u)}$  (8 algebraic variables)',
        u'LCL filter + Grid Thevenin  ─►  PI-VSG OCL (APCL + RPCL)  ─►  VC-ICL  (outer: voltage loop / inner: current loop)',
    ]:
        put(ax1, L + 0.02, y, line, fontsize=9.5)
        y -= 0.022
    y -= 0.006
    hline(ax1, y)
    y -= 0.022

    # State variables
    put(ax1, L, y, '1.  State variables  x  (13)', fontsize=10.5, fontweight='bold')
    y -= 0.024
    for sym, desc, ref in [
        (r'$i_{td},\;i_{tq}$', 'VSC-side inductor currents, dq',   'eq. 1'),
        (r'$v_{md},\;v_{mq}$', 'Capacitor voltage, dq',             'eq. 2a'),
        (r'$i_{sd},\;i_{sq}$', 'Grid-side currents, dq',            'eqs. 2b+4'),
        (r'$\psi$',            'Phase angle difference',             'eq. 11a'),
        (r'$\xi_p$',           'Integral of active power error',     'eq. 11b'),
        (r'$\xi_q$',           'Integral of reactive power error',   'eq. 9b'),
        (r'$\xi_{vd},\;\xi_{vq}$', 'Voltage error integrals, dq — outer loop',  'eq. 14'),
        (r'$\xi_{id},\;\xi_{iq}$', 'Current error integrals, dq — inner loop',  'eq. 15'),
    ]:
        put(ax1, L + 0.02, y, _t(sym.strip('$')), fontsize=10.5)
        put(ax1, L + 0.24, y, desc,  fontsize=9.5)
        put(ax1, L + 0.72, y, ref,   fontsize=8.5, color='#666666')
        y -= 0.022
    y -= 0.008

    # Algebraic variables
    put(ax1, L, y, '2.  Algebraic variables  y  (8)', fontsize=10.5, fontweight='bold')
    y -= 0.024
    for sym, desc, ref in [
        (r'$v_{td},\;v_{tq}$', 'VSC terminal voltage (current-loop output)', 'eq. 15'),
        (r'$\omega_{vsg}$',    'VSG angular speed (PI-VSG)',                  'eq. 11a'),
        (r'$E$',               'Virtual EMF amplitude (RPCL)',                'eq. 9a'),
        (r'$v_{sd},\;v_{sq}$', 'PCC voltage (grid Thevenin + filter)',        'eqs. 2b+4'),
        (r'$p,\;q$',           'Active/reactive power at POI',                'POI'),
    ]:
        put(ax1, L + 0.02, y, _t(sym.strip('$')), fontsize=10.5)
        put(ax1, L + 0.24, y, desc,  fontsize=9.5)
        put(ax1, L + 0.72, y, ref,   fontsize=8.5, color='#666666')
        y -= 0.022
    y -= 0.008

    # Intermediate (substituted inline)
    put(ax1, L, y, '3.  Intermediate expressions  (substituted inline — not states)', fontsize=10.5, fontweight='bold')
    y -= 0.024
    for sym, desc, ref in [
        (r'$v_{md}^{*},\;v_{mq}^{*}$', 'Capacitor voltage references (virtual impedance)', 'eq. 13'),
        (r'$i_{td}^{*},\;i_{tq}^{*}$', 'VSC-side current references (PI voltage loop)',    'eq. 14'),
    ]:
        put(ax1, L + 0.02, y, _t(sym.strip('$')), fontsize=10.5)
        put(ax1, L + 0.24, y, desc,  fontsize=9.5)
        put(ax1, L + 0.72, y, ref,   fontsize=8.5, color='#666666')
        y -= 0.022
    y -= 0.008

    # Inputs
    put(ax1, L, y, '4.  External inputs  u', fontsize=10.5, fontweight='bold')
    y -= 0.024
    for sym, desc in [
        (r'$p^*,\;q^*$',       'Active/reactive power references'),
        (r'$v_{gd},\;v_{gq}$', 'Grid Thevenin voltage, dq'),
    ]:
        put(ax1, L + 0.02, y, _t(sym.strip('$')), fontsize=10.5)
        put(ax1, L + 0.24, y, desc,  fontsize=9.5)
        y -= 0.022
    y -= 0.010
    hline(ax1, y)
    y -= 0.022

    # Parameters (two-column)
    put(ax1, L, y, '5.  Parameters  (default values, Table I)', fontsize=10.5, fontweight='bold')
    y -= 0.025
    par_rows = [
        (r'$L_t$',    '1.25 mH',  'H',      'VSC-side inductor'),
        (r'$R_t$',    '0.04',     'Ω',      'VSC-side resistance'),
        (r'$C_f$',    '4 μF',     'F',      'Filter capacitor'),
        (r'$R_d$',    '10.0',     'Ω',      'Parallel damping'),
        (r'$L_s$',    '1.25 mH',  'H',      'Grid-side inductor'),
        (r'$R_s$',    '0.04',     'Ω',      'Grid-side resistance'),
        (r'$L_g$',    '2.0 mH',   'H',      'Grid Thevenin inductor'),
        (r'$R_g$',    '2.0',      'Ω',      'Grid Thevenin resistance'),
        (r'$k_{pp}$', '0.0012',   'rad/s/W','PI-VSG proportional gain'),
        (r'$k_{ip}$', '0.0016',   'rad/s²/W','PI-VSG integral gain'),
        (r'$k_{pq}$', '0.0016',   'V/W',    'RPCL proportional gain'),
        (r'$k_{iq}$', '0.0163',   'V/W/s',  'RPCL integral gain'),
        (r'$E_0$',    '230.0',    'V',      'Rated virtual EMF'),
        (r'$\omega_0$','100π',    'rad/s',  'Rated speed (50 Hz)'),
        (r'$R_v$',    '0.0',      'Ω',      'Virtual resistance'),
        (r'$X_v$',    '0.08',     'Ω',      'Virtual reactance'),
        (r'$k_{pv}^{vc}$','0.1', 'A/V',    'Voltage-loop P gain'),
        (r'$k_{iv}^{vc}$','0.1', 'A/V/s',  'Voltage-loop I gain'),
        (r'$k_{pi}^{vc}$','0.1', 'V/A',    'Current-loop P gain'),
        (r'$k_{ii}^{vc}$','15.1','V/A/s',  'Current-loop I gain'),
    ]
    col2 = 0.50
    for i, (sym, val, unit, desc) in enumerate(par_rows):
        col = 0 if i % 2 == 0 else col2
        row_y = y - (i // 2) * 0.021
        put(ax1, L + 0.02 + col, row_y, _t(sym.strip('$')), fontsize=10.5)
        put(ax1, L + 0.12 + col, row_y, val,   fontsize=9.5, color='#1a1a8c', family='monospace')
        put(ax1, L + 0.23 + col, row_y, unit,  fontsize=9.0, color='#555555')
        put(ax1, L + 0.29 + col, row_y, desc,  fontsize=9.0)

    y -= ((len(par_rows) + 1) // 2 + 1) * 0.021
    hline(ax1, y, color='#222222', lw=1.0)
    y -= 0.018
    put(ax1, 0.5, y, 'Generated from  pi_vsg_vc_dae.py  —  page 1 of 2',
        ha='center', fontsize=7.5, color='#999999')

    # -----------------------------------------------------------------------
    # PAGE 2 — All equations
    # -----------------------------------------------------------------------
    fig2, ax2 = make_page()

    y = 0.965
    put(ax2, 0.5, y,
        'Full PI-VSG + VC-ICL  —  Differential and Algebraic Equations',
        ha='center', fontsize=12, fontweight='bold')
    y -= 0.022
    hline(ax2, y, color='#222222', lw=1.2)
    y -= 0.020

    # ---- LCL Filter --------------------------------------------------------
    put(ax2, L, y, 'A.  LCL Filter  (eqs. 1, 2a, 2b+4)  —  6 states', fontsize=10.5, fontweight='bold')
    y -= 0.024
    put(ax2, L + 0.02, y, 'VSC-side inductor:', fontsize=8.5, color='#555555')
    y -= 0.030
    put(ax2, L + 0.06, y,
        _t(r'\dot{i}_{td} = (v_{td} - R_t i_{td} + \omega_{vsg} L_t i_{tq} - v_{md})\,/\,L_t'),
        fontsize=11)
    y -= 0.026
    put(ax2, L + 0.06, y,
        _t(r'\dot{i}_{tq} = (v_{tq} - R_t i_{tq} - \omega_{vsg} L_t i_{td} - v_{mq})\,/\,L_t'),
        fontsize=11)
    y -= 0.028
    put(ax2, L + 0.02, y, 'Capacitor (parallel R_d damping):', fontsize=8.5, color='#555555')
    y -= 0.030
    put(ax2, L + 0.06, y,
        _t(r'\dot{v}_{md} = (i_{td} - i_{sd} - v_{md}/R_d + \omega_{vsg} C_f v_{mq})\,/\,C_f'),
        fontsize=11)
    y -= 0.026
    put(ax2, L + 0.06, y,
        _t(r'\dot{v}_{mq} = (i_{tq} - i_{sq} - v_{mq}/R_d - \omega_{vsg} C_f v_{md})\,/\,C_f'),
        fontsize=11)
    y -= 0.028
    put(ax2, L + 0.02, y, 'Grid-side inductor + grid Thevenin combined:', fontsize=8.5, color='#555555')
    y -= 0.030
    put(ax2, L + 0.06, y,
        _t(r'\dot{i}_{sd} = (v_{md} - v_{gd} - (R_s{+}R_g) i_{sd} + \omega_{vsg}(L_s{+}L_g) i_{sq})\,/\,(L_s{+}L_g)'),
        fontsize=11)
    y -= 0.026
    put(ax2, L + 0.06, y,
        _t(r'\dot{i}_{sq} = (v_{mq} - v_{gq} - (R_s{+}R_g) i_{sq} - \omega_{vsg}(L_s{+}L_g) i_{sd})\,/\,(L_s{+}L_g)'),
        fontsize=11)
    y -= 0.014
    hline(ax2, y)
    y -= 0.016

    # ---- PI-VSG OCL --------------------------------------------------------
    put(ax2, L, y, 'B.  PI-VSG Outer Control Loop  (eqs. 9, 11)  —  3 states', fontsize=10.5, fontweight='bold')
    y -= 0.024
    put(ax2, L + 0.02, y, 'APCL (eq. 11):', fontsize=8.5, color='#555555')
    y -= 0.028
    put(ax2, L + 0.06, y, _t(r'\dot{\psi} = -k_{pp}(p^*-p) - k_{ip}\xi_p'), fontsize=12)
    y -= 0.026
    put(ax2, L + 0.06, y, _t(r'\dot{\xi}_p = p^* - p'), fontsize=12)
    y -= 0.024
    put(ax2, L + 0.02, y, 'RPCL (eq. 9b):', fontsize=8.5, color='#555555')
    y -= 0.028
    put(ax2, L + 0.06, y, _t(r'\dot{\xi}_q = q^* - q'), fontsize=12)
    y -= 0.014
    hline(ax2, y)
    y -= 0.016

    # ---- VC-ICL ----------------------------------------------------------------
    put(ax2, L, y, 'C.  VC-ICL — Cascaded PI Controllers  (eqs. 13–15)  —  4 states', fontsize=10.5, fontweight='bold')
    y -= 0.022
    put(ax2, L + 0.02, y,
        u'Virtual impedance (eq. 13,  eᵀ=[0,E]ᵀ,  Zᵥ=[[Rᵥ,−Xᵥ],[Xᵥ,Rᵥ]])  →  substituted inline:',
        fontsize=8.5, color='#555555')
    y -= 0.028
    put(ax2, L + 0.06, y,
        _t(r'v_{md}^{*} = -R_v i_{sd} + X_v i_{sq}'),
        fontsize=11.5)
    y -= 0.026
    put(ax2, L + 0.06, y,
        _t(r'v_{mq}^{*} = E - X_v i_{sd} - R_v i_{sq}'),
        fontsize=11.5)
    y -= 0.024
    put(ax2, L + 0.02, y,
        u'Outer voltage loop  (eq. 14):  voltage error integrals  +  current references:',
        fontsize=8.5, color='#555555')
    y -= 0.028
    put(ax2, L + 0.06, y, _t(r'\dot{\xi}_{vd} = v_{md}^{*} - v_{md}'), fontsize=12)
    y -= 0.026
    put(ax2, L + 0.06, y, _t(r'\dot{\xi}_{vq} = v_{mq}^{*} - v_{mq}'), fontsize=12)
    y -= 0.026
    put(ax2, L + 0.06, y,
        _t(r'i_{td}^{*} = k_{pv}^{vc}(v_{md}^{*}-v_{md}) + k_{iv}^{vc}\xi_{vd} - \omega_{vsg}C_f v_{mq} + i_{sd}'),
        fontsize=11)
    y -= 0.026
    put(ax2, L + 0.06, y,
        _t(r'i_{tq}^{*} = k_{pv}^{vc}(v_{mq}^{*}-v_{mq}) + k_{iv}^{vc}\xi_{vq} + \omega_{vsg}C_f v_{md} + i_{sq}'),
        fontsize=11)
    y -= 0.024
    put(ax2, L + 0.02, y,
        u'Inner current loop  (eq. 15):  current error integrals:',
        fontsize=8.5, color='#555555')
    y -= 0.028
    put(ax2, L + 0.06, y, _t(r'\dot{\xi}_{id} = i_{td}^{*} - i_{td}'), fontsize=12)
    y -= 0.026
    put(ax2, L + 0.06, y, _t(r'\dot{\xi}_{iq} = i_{tq}^{*} - i_{tq}'), fontsize=12)
    y -= 0.014
    hline(ax2, y)
    y -= 0.016

    # ---- Algebraic equations -----------------------------------------------
    put(ax2, L, y, 'D.  Algebraic equations  0 = g(x, y, u)  —  8 equations', fontsize=10.5, fontweight='bold')
    y -= 0.022

    put(ax2, L + 0.02, y,
        'Inner current-loop terminal voltage  (eq. 15):',
        fontsize=8.5, color='#555555')
    y -= 0.030
    put(ax2, L + 0.06, y,
        _t(r'0 = v_{td} - \left[k_{pi}^{vc}(i_{td}^{*}-i_{td})'
           r' + k_{ii}^{vc}\xi_{id} + \omega_{vsg}L_t i_{tq} + v_{md}\right]'),
        fontsize=11)
    y -= 0.028
    put(ax2, L + 0.06, y,
        _t(r'0 = v_{tq} - \left[k_{pi}^{vc}(i_{tq}^{*}-i_{tq})'
           r' + k_{ii}^{vc}\xi_{iq} - \omega_{vsg}L_t i_{td} + v_{mq}\right]'),
        fontsize=11)
    y -= 0.026
    put(ax2, L + 0.02, y,
        'PI-VSG speed and EMF:', fontsize=8.5, color='#555555')
    y -= 0.028
    put(ax2, L + 0.06, y,
        _t(r'0 = \omega_{vsg} - \omega_0 - k_{pp}(p^*-p) - k_{ip}\xi_p'),
        fontsize=11.5)
    y -= 0.026
    put(ax2, L + 0.06, y,
        _t(r'0 = E - E_0 - k_{pq}(q^*-q) - k_{iq}\xi_q'),
        fontsize=11.5)
    y -= 0.026
    put(ax2, L + 0.02, y,
        u'PCC voltage  (α = L_g/(L_s+L_g),  R_mix = (R_g·L_s−R_s·L_g)/(L_s+L_g)):',
        fontsize=8.5, color='#555555')
    y -= 0.028
    put(ax2, L + 0.06, y,
        _t(r'0 = v_{sd} - \left[(1-\alpha)v_{gd} + \alpha v_{md} + R_{mix}\,i_{sd}\right]'),
        fontsize=11.5)
    y -= 0.026
    put(ax2, L + 0.06, y,
        _t(r'0 = v_{sq} - \left[(1-\alpha)v_{gq} + \alpha v_{mq} + R_{mix}\,i_{sq}\right]'),
        fontsize=11.5)
    y -= 0.026
    put(ax2, L + 0.02, y, 'Active and reactive power at POI:', fontsize=8.5, color='#555555')
    y -= 0.028
    put(ax2, L + 0.06, y,
        _t(r'0 = p - (v_{sd}\,i_{sd} + v_{sq}\,i_{sq})'), fontsize=11.5)
    y -= 0.026
    put(ax2, L + 0.06, y,
        _t(r'0 = q - (v_{sq}\,i_{sd} - v_{sd}\,i_{sq})'), fontsize=11.5)
    y -= 0.016

    hline(ax2, y, color='#222222', lw=1.0)
    y -= 0.018
    put(ax2, 0.5, y, 'Generated from  pi_vsg_vc_dae.py  —  page 2 of 2',
        ha='center', fontsize=7.5, color='#999999')

    # -----------------------------------------------------------------------
    # Save
    # -----------------------------------------------------------------------
    with PdfPages(filename) as pdf:
        pdf.savefig(fig1, bbox_inches='tight', dpi=150)
        pdf.savefig(fig2, bbox_inches='tight', dpi=150)
    plt.close(fig1)
    plt.close(fig2)
    print(f"PDF saved: {filename}  (2 pages)")


# ---------------------------------------------------------------------------
# 10. Main
# ---------------------------------------------------------------------------
if __name__ == '__main__':
    check_model()

    print("\n--- Differential equations  dx/dt = f(x, y, u) ---")
    for name, eq in zip(x_names, f_list):
        print(f"  d({name})/dt = {eq}")

    print("\n--- Algebraic equations  0 = g(x, y, u) ---")
    for name, eq in zip(y_names, g_list):
        print(f"  0 = {eq}")

    generate_pdf('pi_vsg_vc_model.pdf')
