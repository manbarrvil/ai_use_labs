"""
Full PI-VSG + CC-ICL nonlinear DAE model (grid-forming VSC)
Source: Matas-Díaz et al., "A Systematic Small-signal …", JMPSCE 2025
        §II.A (LCL filter), §II.B (OCL), §II.C.2 (CC-ICL), eqs. (1)-(20)

System:  dx/dt = f(x, y, u)      — 13 differential states
          0    = g(x, y, u)      —  8 algebraic variables

Architecture:
  [p*, q*] ─► PI-VSG OCL ─► [omega_vsg, E]
                                    │
                              CC-ICL (PI-CC) ◄── [i_s, v_s]
                                    │
                               [v_td, v_tq]
                                    │
                            LCL Filter + Grid Thevenin
                                    │
                                [v_g, i_s]

State variables x (13)
----------------------
  LCL Filter:
    i_td, i_tq  : VSC-side inductor currents, dq  (eq. 1)
    v_md, v_mq  : Capacitor voltage, dq            (eq. 2a)
    i_sd, i_sq  : Grid-side currents, dq           (eqs. 2b + 4)
  PI-VSG OCL:
    psi         : Phase angle difference ψ = θ_g − θ_vsg  (eq. 11a)
    xi_p        : Integral of active power error          (eq. 11b)
    xi_q        : Integral of reactive power error        (eq. 9b)
  CC-ICL:
    i_sd_star, i_sq_star : LPF filtered current references  (eq. 18)
    xi_id, xi_iq         : Current error integrals           (eq. 19b)

Algebraic variables y (8)
--------------------------
  v_td, v_tq   : VSC terminal voltage (CC-ICL output, eq. 19a)
  omega_vsg    : VSG angular speed    (PI-VSG, algebraic from dψ/dt)
  E            : Virtual EMF          (RPCL, eq. 9a)
  v_sd, v_sq   : PCC voltage          (from grid Thevenin + filter)
  p, q         : Active/reactive power at POI

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
i_sd_star, i_sq_star = sp.symbols('i_sd_star i_sq_star', real=True)
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

# Parameters (SymPy symbols, substituted numerically via params dict)
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
kpi_cc  = sp.Symbol('kpi_cc',  real=True, positive=True)
kii_cc  = sp.Symbol('kii_cc',  real=True, positive=True)
G_v     = sp.Symbol('G_v',     real=True)
B_v     = sp.Symbol('B_v',     real=True)
tau_lpf = sp.Symbol('tau_lpf', real=True, positive=True)

# ---------------------------------------------------------------------------
# 2. Named lists
# ---------------------------------------------------------------------------
x_list  = [i_td, i_tq, v_md, v_mq, i_sd, i_sq,
           psi, xi_p, xi_q,
           i_sd_star, i_sq_star, xi_id, xi_iq]

y_list  = [v_td, v_tq, omega_vsg, E, v_sd, v_sq, p, q]

x_names = ['i_td', 'i_tq', 'v_md', 'v_mq', 'i_sd', 'i_sq',
           'psi', 'xi_p', 'xi_q',
           'i_sd_star', 'i_sq_star', 'xi_id', 'xi_iq']

y_names = ['v_td', 'v_tq', 'omega_vsg', 'E', 'v_sd', 'v_sq', 'p', 'q']

# ---------------------------------------------------------------------------
# 3. Default parameters (Table I, paper)
# ---------------------------------------------------------------------------
params = {
    L_t:     1.25e-3,     # [H]       VSC-side inductor
    R_t:     0.04,        # [Ω]       VSC-side resistance
    C_f:     4e-6,        # [F]       Filter capacitor
    R_d:     10.0,        # [Ω]       Parallel damping
    L_s:     1.25e-3,     # [H]       Grid-side inductor
    R_s:     0.04,        # [Ω]       Grid-side resistance
    L_g:     2e-3,        # [H]       Grid Thevenin inductor
    R_g:     2.0,         # [Ω]       Grid Thevenin resistance
    k_pp:    0.0012,      # [rad/s/W] PI-VSG proportional gain
    k_ip:    0.0016,      # [rad/s²/W]PI-VSG integral gain
    k_pq:    0.0016,      # [V/W]     RPCL proportional gain
    k_iq:    0.0163,      # [V/W/s]   RPCL integral gain
    E_0:     230.0,       # [V]       Rated virtual EMF
    omega_0: 100*np.pi,   # [rad/s]   Rated speed (50 Hz)
    kpi_cc:  1.25,        # [V/A]     CC-ICL proportional gain
    kii_cc:  40.0,        # [V/A]     CC-ICL integral gain
    G_v:     0.0,         # [S]       Virtual conductance
    B_v:     1.25,        # [S]       Virtual susceptance
    tau_lpf: 1.6e-3,      # [s]       LPF time constant
}

# ---------------------------------------------------------------------------
# 4. Intermediate constants (functions of parameters)
# ---------------------------------------------------------------------------
L_sg   = L_s + L_g              # Combined grid-side inductance
R_sg   = R_s + R_g              # Combined grid-side resistance
L_f    = L_t + L_s              # Total filter inductance (for CC-ICL cross-coupling)
alpha  = L_g / L_sg             # Voltage divider for PCC (Thevenin split)
R_mix  = (R_g*L_s - R_s*L_g) / L_sg  # Residual resistance in PCC equation

# ---------------------------------------------------------------------------
# 5. Differential equations  f: dx/dt = f(x, y, u)
# ---------------------------------------------------------------------------

# --- LCL Filter ---
# VSC-side inductor (eq. 1, dq frame)
f1  = (v_td - R_t*i_td + omega_vsg*L_t*i_tq - v_md) / L_t
f2  = (v_tq - R_t*i_tq - omega_vsg*L_t*i_td - v_mq) / L_t

# Capacitor with parallel damping R_d (eq. 2a, dq frame)
f3  = (i_td - i_sd - v_md/R_d + omega_vsg*C_f*v_mq) / C_f
f4  = (i_tq - i_sq - v_mq/R_d - omega_vsg*C_f*v_md) / C_f

# Grid-side inductor + grid Thevenin (eqs. 2b + 4 combined)
f5  = (v_md - v_gd - R_sg*i_sd + omega_vsg*L_sg*i_sq) / L_sg
f6  = (v_mq - v_gq - R_sg*i_sq - omega_vsg*L_sg*i_sd) / L_sg

# --- PI-VSG Outer Control Loop ---
# APCL — PI controller, phase angle (eq. 11)
# dψ/dt = ω_0 − ω_vsg  →  substituting g3 definition of ω_vsg
f7  = -k_pp*(p_star - p) - k_ip*xi_p    # d(ψ)/dt
f8  = p_star - p                          # d(ξ_p)/dt

# RPCL — reactive power PI integrator (eq. 9b)
f9  = q_star - q                          # d(ξ_q)/dt

# --- CC-ICL ---
# Virtual admittance output (eq. 17, e = [0, E]^T)
i_s_log_d = -G_v*v_sd - B_v*(E - v_sq)
i_s_log_q = -B_v*v_sd + G_v*(E - v_sq)

# LPF filtered current references (eq. 18)
f10 = (i_s_log_d - i_sd_star) / tau_lpf  # d(i_sd*)/dt
f11 = (i_s_log_q - i_sq_star) / tau_lpf  # d(i_sq*)/dt

# PI current error integrals (eq. 19b)
f12 = i_sd_star - i_sd                    # d(ξ_id)/dt
f13 = i_sq_star - i_sq                    # d(ξ_iq)/dt

f_list = [f1, f2, f3, f4, f5, f6, f7, f8, f9, f10, f11, f12, f13]

# ---------------------------------------------------------------------------
# 6. Algebraic equations  g: 0 = g(x, y, u)
# ---------------------------------------------------------------------------

# CC-ICL terminal voltage output (eq. 19a, L_f = L_t + L_s)
g1 = v_td - (kpi_cc*(i_sd_star - i_sd)
             + kii_cc*xi_id
             + omega_vsg*L_f*i_sq          # cross-coupling +ω·Lf·i_sq
             + v_sd)                        # feed-forward

g2 = v_tq - (kpi_cc*(i_sq_star - i_sq)
             + kii_cc*xi_iq
             - omega_vsg*L_f*i_sd          # cross-coupling −ω·Lf·i_sd
             + v_sq)                        # feed-forward

# PI-VSG angular speed (from dψ/dt = ω_0 − ω_vsg, eq. 11a)
g3 = omega_vsg - omega_0 - k_pp*(p_star - p) - k_ip*xi_p

# RPCL virtual EMF (eq. 9a)
g4 = E - E_0 - k_pq*(q_star - q) - k_iq*xi_q

# PCC voltage (eqs. 2b + 4 combined; α = L_g/(L_s+L_g), R_mix = (R_g·L_s − R_s·L_g)/(L_s+L_g))
g5 = v_sd - ((1 - alpha)*v_gd + alpha*v_md + R_mix*i_sd)
g6 = v_sq - ((1 - alpha)*v_gq + alpha*v_mq + R_mix*i_sq)

# Active and reactive power at POI (grid-side, CC-ICL convention)
g7 = p - (v_sd*i_sd + v_sq*i_sq)
g8 = q - (v_sq*i_sd - v_sd*i_sq)

g_list = [g1, g2, g3, g4, g5, g6, g7, g8]

# ---------------------------------------------------------------------------
# 7. Verification helpers
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
# 8. PDF generation — 2 pages
# ---------------------------------------------------------------------------
def generate_pdf(filename: str = 'pi_vsg_cc_model.pdf') -> None:
    """Render the full PI-VSG + CC-ICL DAE model to a 2-page A4 PDF."""
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages

    def _t(s):
        return f'${s}$'

    # -----------------------------------------------------------------------
    # Helpers
    # -----------------------------------------------------------------------
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

    L = 0.07   # left margin

    # -----------------------------------------------------------------------
    # PAGE 1 — Title + Tables
    # -----------------------------------------------------------------------
    fig1, ax1 = make_page()

    y = 0.965
    put(ax1, 0.5, y,
        'Full PI-VSG + CC-ICL  —  Nonlinear DAE Model',
        ha='center', fontsize=13, fontweight='bold')
    y -= 0.030
    put(ax1, 0.5, y,
        'Matas-Díaz et al., JMPSCE 2025, §II.A–II.C.2, eqs. (1)–(20)',
        ha='center', fontsize=8.5, color='#555555', style='italic')
    y -= 0.018
    hline(ax1, y, color='#222222', lw=1.2)
    y -= 0.022

    # System architecture (text)
    put(ax1, L, y, 'System architecture', fontsize=10.5, fontweight='bold')
    y -= 0.024
    arch = [
        r'$\mathbf{dx/dt = f(x,y,u)}$  (13 differential states)     '
        r'$\mathbf{0 = g(x,y,u)}$  (8 algebraic variables)',
        u'LCL filter + Grid Thevenin  ─►  PI-VSG OCL (APCL + RPCL)  ─►  CC-ICL (PI current controller)',
    ]
    for line in arch:
        put(ax1, L + 0.02, y, line, fontsize=9.5, color='#222222')
        y -= 0.022
    y -= 0.006
    hline(ax1, y)
    y -= 0.022

    # State variables table
    put(ax1, L, y, '1.  State variables  x  (13)', fontsize=10.5, fontweight='bold')
    y -= 0.024
    states_tbl = [
        # (symbol,     code name,      subsystem,  equation ref)
        (r'$i_{td},\;i_{tq}$',   'i_td, i_tq',   'VSC-side inductor currents, dq',  'eq. 1'),
        (r'$v_{md},\;v_{mq}$',   'v_md, v_mq',   'Capacitor voltage, dq',           'eq. 2a'),
        (r'$i_{sd},\;i_{sq}$',   'i_sd, i_sq',   'Grid-side currents, dq',          'eqs. 2b+4'),
        (r'$\psi$',              'psi',           'Phase angle difference',          'eq. 11a'),
        (r'$\xi_p$',             'xi_p',          'Integral of active power error',  'eq. 11b'),
        (r'$\xi_q$',             'xi_q',          'Integral of reactive power error','eq. 9b'),
        (r'$i_{sd}^{\,*},\;i_{sq}^{\,*}$','i_sd_star, i_sq_star','LPF current references, dq','eq. 18'),
        (r'$\xi_{id},\;\xi_{iq}$','xi_id, xi_iq', 'Current error integrals, dq',   'eq. 19b'),
    ]
    for sym, code, desc, ref in states_tbl:
        put(ax1, L + 0.02, y, sym,   fontsize=10.5)
        put(ax1, L + 0.22, y, desc,  fontsize=9.5)
        put(ax1, L + 0.72, y, ref,   fontsize=8.5, color='#666666')
        y -= 0.022
    y -= 0.008

    # Algebraic variables
    put(ax1, L, y, '2.  Algebraic variables  y  (8)', fontsize=10.5, fontweight='bold')
    y -= 0.024
    alg_tbl = [
        (r'$v_{td},\;v_{tq}$',  'VSC terminal voltage (CC-ICL output)',    'eq. 19a'),
        (r'$\omega_{vsg}$',     'VSG angular speed (PI-VSG)',              'eq. 11a'),
        (r'$E$',                'Virtual EMF amplitude (RPCL)',            'eq. 9a'),
        (r'$v_{sd},\;v_{sq}$',  'PCC voltage (grid Thevenin + filter)',    'eqs. 2b+4'),
        (r'$p,\;q$',            'Active/reactive power at POI',            'POI'),
    ]
    for sym, desc, ref in alg_tbl:
        put(ax1, L + 0.02, y, sym,  fontsize=10.5)
        put(ax1, L + 0.22, y, desc, fontsize=9.5)
        put(ax1, L + 0.72, y, ref,  fontsize=8.5, color='#666666')
        y -= 0.022
    y -= 0.008

    # Inputs
    put(ax1, L, y, '3.  External inputs  u', fontsize=10.5, fontweight='bold')
    y -= 0.024
    inp_tbl = [
        (r'$p^*,\;q^*$',       'Active/reactive power references'),
        (r'$v_{gd},\;v_{gq}$', 'Grid Thevenin voltage, dq (Thevenin source)'),
    ]
    for sym, desc in inp_tbl:
        put(ax1, L + 0.02, y, sym,  fontsize=10.5)
        put(ax1, L + 0.22, y, desc, fontsize=9.5)
        y -= 0.022
    y -= 0.010
    hline(ax1, y)
    y -= 0.022

    # Parameters table (two-column)
    put(ax1, L, y, '4.  Parameters  (default values, Table I)', fontsize=10.5, fontweight='bold')
    y -= 0.025
    par_rows = [
        # (LaTeX symbol,       value string,    unit,    description)
        (r'$L_t$',   '1.25 mH',  'H',     'VSC-side inductor'),
        (r'$R_t$',   '0.04',     'Ω',     'VSC-side resistance'),
        (r'$C_f$',   '4 μF',     'F',     'Filter capacitor'),
        (r'$R_d$',   '10.0',     'Ω',     'Parallel damping'),
        (r'$L_s$',   '1.25 mH',  'H',     'Grid-side inductor'),
        (r'$R_s$',   '0.04',     'Ω',     'Grid-side resistance'),
        (r'$L_g$',   '2.0 mH',   'H',     'Grid Thevenin inductor'),
        (r'$R_g$',   '2.0',      'Ω',     'Grid Thevenin resistance'),
        (r'$k_{pp}$','0.0012',   'rad/s/W','PI-VSG proportional gain'),
        (r'$k_{ip}$','0.0016',   'rad/s²/W','PI-VSG integral gain'),
        (r'$k_{pq}$','0.0016',   'V/W',   'RPCL proportional gain'),
        (r'$k_{iq}$','0.0163',   'V/W/s', 'RPCL integral gain'),
        (r'$E_0$',   '230.0',    'V',     'Rated virtual EMF'),
        (r'$\omega_0$','100π',   'rad/s', 'Rated angular speed (50 Hz)'),
        (r'$k_{pi}^{cc}$','1.25','V/A',  'CC-ICL proportional gain'),
        (r'$k_{ii}^{cc}$','40.0','V/A',  'CC-ICL integral gain'),
        (r'$G_v$',   '0.0',      'S',     'Virtual conductance'),
        (r'$B_v$',   '1.25',     'S',     'Virtual susceptance'),
        (r'$\tau_{lpf}$','1.6 ms','s',   'LPF time constant'),
    ]
    col2_start = 0.50  # second column x offset
    for i, (sym, val, unit, desc) in enumerate(par_rows):
        col = 0 if i % 2 == 0 else col2_start
        row_y = y - (i // 2) * 0.022
        put(ax1, L + 0.02 + col, row_y, _t(sym.strip('$')), fontsize=10.5)
        put(ax1, L + 0.10 + col, row_y, val,   fontsize=9.5, color='#1a1a8c', family='monospace')
        put(ax1, L + 0.21 + col, row_y, unit,  fontsize=9.0, color='#555555')
        put(ax1, L + 0.27 + col, row_y, desc,  fontsize=9.0)

    y -= ((len(par_rows) + 1) // 2 + 1) * 0.022
    hline(ax1, y, color='#222222', lw=1.0)
    y -= 0.018
    put(ax1, 0.5, y, 'Generated from  pi_vsg_cc_dae.py  —  page 1 of 2',
        ha='center', fontsize=7.5, color='#999999')

    # -----------------------------------------------------------------------
    # PAGE 2 — All equations
    # -----------------------------------------------------------------------
    fig2, ax2 = make_page()

    y = 0.965
    put(ax2, 0.5, y,
        'Full PI-VSG + CC-ICL  —  Differential and Algebraic Equations',
        ha='center', fontsize=12, fontweight='bold')
    y -= 0.022
    hline(ax2, y, color='#222222', lw=1.2)
    y -= 0.020

    # ---- LCL Filter ---------------------------------------------------------
    put(ax2, L, y, 'A.  LCL Filter  (eqs. 1, 2a, 2b+4)  —  6 states', fontsize=10.5, fontweight='bold')
    y -= 0.024
    put(ax2, L + 0.02, y, 'VSC-side inductor  (L_t, R_t):', fontsize=8.5, color='#555555')
    y -= 0.032
    put(ax2, L + 0.06, y,
        _t(r'\dot{i}_{td} = (v_{td} - R_t i_{td} + \omega_{vsg} L_t i_{tq} - v_{md})\,/\,L_t'),
        fontsize=11)
    y -= 0.028
    put(ax2, L + 0.06, y,
        _t(r'\dot{i}_{tq} = (v_{tq} - R_t i_{tq} - \omega_{vsg} L_t i_{td} - v_{mq})\,/\,L_t'),
        fontsize=11)
    y -= 0.030
    put(ax2, L + 0.02, y, 'Capacitor  (C_f, R_d parallel):', fontsize=8.5, color='#555555')
    y -= 0.032
    put(ax2, L + 0.06, y,
        _t(r'\dot{v}_{md} = (i_{td} - i_{sd} - v_{md}/R_d + \omega_{vsg} C_f v_{mq})\,/\,C_f'),
        fontsize=11)
    y -= 0.028
    put(ax2, L + 0.06, y,
        _t(r'\dot{v}_{mq} = (i_{tq} - i_{sq} - v_{mq}/R_d - \omega_{vsg} C_f v_{md})\,/\,C_f'),
        fontsize=11)
    y -= 0.030
    put(ax2, L + 0.02, y,
        u'Grid-side inductor + grid Thevenin combined  (L_s+L_g, R_s+R_g):',
        fontsize=8.5, color='#555555')
    y -= 0.032
    put(ax2, L + 0.06, y,
        _t(r'\dot{i}_{sd} = (v_{md} - v_{gd} - (R_s{+}R_g)\,i_{sd} + \omega_{vsg}(L_s{+}L_g)\,i_{sq})\,/\,(L_s{+}L_g)'),
        fontsize=11)
    y -= 0.028
    put(ax2, L + 0.06, y,
        _t(r'\dot{i}_{sq} = (v_{mq} - v_{gq} - (R_s{+}R_g)\,i_{sq} - \omega_{vsg}(L_s{+}L_g)\,i_{sd})\,/\,(L_s{+}L_g)'),
        fontsize=11)
    y -= 0.016
    hline(ax2, y)
    y -= 0.018

    # ---- PI-VSG OCL ---------------------------------------------------------
    put(ax2, L, y, 'B.  PI-VSG Outer Control Loop  (eqs. 9, 11)  —  3 states', fontsize=10.5, fontweight='bold')
    y -= 0.024
    put(ax2, L + 0.02, y, 'APCL — PI controller for active power (eq. 11):', fontsize=8.5, color='#555555')
    y -= 0.030
    put(ax2, L + 0.06, y,
        _t(r'\dot{\psi} = -k_{pp}(p^*-p) - k_{ip}\xi_p'),
        fontsize=12)
    y -= 0.028
    put(ax2, L + 0.06, y,
        _t(r'\dot{\xi}_p = p^* - p'),
        fontsize=12)
    y -= 0.028
    put(ax2, L + 0.02, y, 'RPCL — PI controller for reactive power (eq. 9b):', fontsize=8.5, color='#555555')
    y -= 0.030
    put(ax2, L + 0.06, y,
        _t(r'\dot{\xi}_q = q^* - q'),
        fontsize=12)
    y -= 0.016
    hline(ax2, y)
    y -= 0.018

    # ---- CC-ICL ---------------------------------------------------------------
    put(ax2, L, y, 'C.  CC-ICL — PI Current Controller  (eqs. 17–19)  —  4 states', fontsize=10.5, fontweight='bold')
    y -= 0.024
    put(ax2, L + 0.02, y,
        u'Virtual admittance  (eq. 17,  eᵀ = [0, E]ᵀ,  Yᵥ = [[Gᵥ,−Bᵥ],[Bᵥ,Gᵥ]]  →  substituted inline):',
        fontsize=8.5, color='#555555')
    y -= 0.030
    put(ax2, L + 0.06, y,
        _t(r'\dot{i}_{sd}^{\,*} = (-G_v v_{sd} - B_v(E-v_{sq}) - i_{sd}^{\,*})\,/\,\tau_{lpf}'),
        fontsize=11.5)
    y -= 0.030
    put(ax2, L + 0.06, y,
        _t(r'\dot{i}_{sq}^{\,*} = (-B_v v_{sd} + G_v(E-v_{sq}) - i_{sq}^{\,*})\,/\,\tau_{lpf}'),
        fontsize=11.5)
    y -= 0.028
    put(ax2, L + 0.02, y, 'PI integrators  (eq. 19b):', fontsize=8.5, color='#555555')
    y -= 0.030
    put(ax2, L + 0.06, y,
        _t(r'\dot{\xi}_{id} = i_{sd}^{\,*} - i_{sd}'),
        fontsize=12)
    y -= 0.028
    put(ax2, L + 0.06, y,
        _t(r'\dot{\xi}_{iq} = i_{sq}^{\,*} - i_{sq}'),
        fontsize=12)
    y -= 0.016
    hline(ax2, y)
    y -= 0.018

    # ---- Algebraic equations --------------------------------------------------
    put(ax2, L, y, 'D.  Algebraic equations  0 = g(x, y, u)  —  8 equations', fontsize=10.5, fontweight='bold')
    y -= 0.024

    put(ax2, L + 0.02, y,
        'CC-ICL terminal voltage  (eq. 19a,  ' + _t(r'L_f = L_t+L_s') + '):',
        fontsize=8.5, color='#555555')
    y -= 0.032
    put(ax2, L + 0.06, y,
        _t(r'0 = v_{td} - \left[k_{pi}^{cc}(i_{sd}^{\,*}-i_{sd})'
           r' + k_{ii}^{cc}\xi_{id} + \omega_{vsg}L_f i_{sq} + v_{sd}\right]'),
        fontsize=11)
    y -= 0.030
    put(ax2, L + 0.06, y,
        _t(r'0 = v_{tq} - \left[k_{pi}^{cc}(i_{sq}^{\,*}-i_{sq})'
           r' + k_{ii}^{cc}\xi_{iq} - \omega_{vsg}L_f i_{sd} + v_{sq}\right]'),
        fontsize=11)
    y -= 0.028

    put(ax2, L + 0.02, y,
        'PI-VSG speed and EMF  (from ' + _t(r'd\psi/dt=\omega_0-\omega_{vsg}') + ', eq. 9a):',
        fontsize=8.5, color='#555555')
    y -= 0.032
    put(ax2, L + 0.06, y,
        _t(r'0 = \omega_{vsg} - \omega_0 - k_{pp}(p^*-p) - k_{ip}\xi_p'),
        fontsize=11.5)
    y -= 0.028
    put(ax2, L + 0.06, y,
        _t(r'0 = E - E_0 - k_{pq}(q^*-q) - k_{iq}\xi_q'),
        fontsize=11.5)
    y -= 0.028

    put(ax2, L + 0.02, y,
        u'PCC voltage  (eqs. 2b+4 combined,  α = L_g/(L_s+L_g),  R_mix = (R_g·L_s−R_s·L_g)/(L_s+L_g)):',
        fontsize=8.5, color='#555555')
    y -= 0.032
    put(ax2, L + 0.06, y,
        _t(r'0 = v_{sd} - \left[(1-\alpha)v_{gd} + \alpha v_{md} + R_{mix}\,i_{sd}\right]'),
        fontsize=11.5)
    y -= 0.028
    put(ax2, L + 0.06, y,
        _t(r'0 = v_{sq} - \left[(1-\alpha)v_{gq} + \alpha v_{mq} + R_{mix}\,i_{sq}\right]'),
        fontsize=11.5)
    y -= 0.028

    put(ax2, L + 0.02, y, 'Active and reactive power at POI:', fontsize=8.5, color='#555555')
    y -= 0.032
    put(ax2, L + 0.06, y,
        _t(r'0 = p - (v_{sd}\,i_{sd} + v_{sq}\,i_{sq})'),
        fontsize=11.5)
    y -= 0.028
    put(ax2, L + 0.06, y,
        _t(r'0 = q - (v_{sq}\,i_{sd} - v_{sd}\,i_{sq})'),
        fontsize=11.5)
    y -= 0.018

    hline(ax2, y, color='#222222', lw=1.0)
    y -= 0.018
    put(ax2, 0.5, y, 'Generated from  pi_vsg_cc_dae.py  —  page 2 of 2',
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
# 9. Main — print equations and generate PDF
# ---------------------------------------------------------------------------
if __name__ == '__main__':
    check_model()

    print("\n--- Differential equations  dx/dt = f(x, y, u) ---")
    for name, eq in zip(x_names, f_list):
        print(f"  d({name})/dt = {eq}")

    print("\n--- Algebraic equations  0 = g(x, y, u) ---")
    for name, eq in zip(y_names, g_list):
        print(f"  0 = {eq}")

    generate_pdf('pi_vsg_cc_model.pdf')
