"""
PI Current Controller (PI-CC / CC-ICL) — differential-algebraic equations
Source: Matas-Díaz et al., "A Systematic Small-signal …", JMPSCE 2025, §II.C.2, eqs. (17)-(20)

System:  dx/dt = f(x, y, u)
          0    = g(x, y, u)

State variables x (4)
---------------------
  i_sd_star  : d-axis filtered current reference [LPF output]   (eq. 18)
  i_sq_star  : q-axis filtered current reference [LPF output]   (eq. 18)
  xi_id      : integral of d-axis current error                  (eq. 19b)
  xi_iq      : integral of q-axis current error                  (eq. 19b)

Algebraic variables y (2)
--------------------------
  v_td : VSC terminal voltage, d-axis  (eq. 19a)
  v_tq : VSC terminal voltage, q-axis  (eq. 19a)

Inputs u (provided by other subsystems)
----------------------------------------
  v_sd, v_sq   : grid-side inductor voltage, dq components
  i_sd, i_sq   : measured grid-side current, dq components
  E            : virtual EMF amplitude (from OCL)
  omega_vsg    : VSG angular speed (from OCL)

Parameters (Table I of paper)
------------------------------
  kpi_cc  = 1.25   [V/A]  proportional gain of PI current controller
  kii_cc  = 40.0   [V/A·s⁻¹] integral gain of PI current controller
  Gv      = 0.0    [S]    virtual conductance
  Bv      = 1.25   [S]    virtual susceptance
  tau_lpf = 1.6e-3 [s]    LPF time constant
  Lf               [H]    total filter inductance (caller-supplied)
"""

import sympy as sp

# ---------------------------------------------------------------------------
# Symbols
# ---------------------------------------------------------------------------
# State variables
i_sd_star, i_sq_star = sp.symbols('i_sd_star i_sq_star', real=True)
xi_id, xi_iq         = sp.symbols('xi_id xi_iq',         real=True)

# Algebraic variables
v_td, v_tq = sp.symbols('v_td v_tq', real=True)

# Inputs
v_sd, v_sq       = sp.symbols('v_sd v_sq',       real=True)
i_sd, i_sq       = sp.symbols('i_sd i_sq',       real=True)
E                 = sp.Symbol ('E',               real=True, positive=True)
omega_vsg         = sp.Symbol ('omega_vsg',       real=True)

# Parameter symbols (substituted numerically via params dict)
kpi_cc  = sp.Symbol('kpi_cc',  real=True, positive=True)
kii_cc  = sp.Symbol('kii_cc',  real=True, positive=True)
Gv      = sp.Symbol('Gv',      real=True)
Bv      = sp.Symbol('Bv',      real=True)
tau_lpf = sp.Symbol('tau_lpf', real=True, positive=True)
Lf      = sp.Symbol('Lf',      real=True, positive=True)

# ---------------------------------------------------------------------------
# Named lists (order matters — must be consistent)
# ---------------------------------------------------------------------------
x_list = [i_sd_star, i_sq_star, xi_id, xi_iq]
y_list = [v_td, v_tq]

x_names = ['i_sd_star', 'i_sq_star', 'xi_id', 'xi_iq']
y_names = ['v_td', 'v_tq']

# ---------------------------------------------------------------------------
# Default parameters (Table I, paper)
# ---------------------------------------------------------------------------
params = {
    kpi_cc:  1.25,
    kii_cc:  40.0,
    Gv:      0.0,
    Bv:      1.25,
    tau_lpf: 1.6e-3,
    # Lf: caller must supply a value (system-dependent)
}

# ---------------------------------------------------------------------------
# Intermediate: virtual admittance output  (eq. 17)
# Y_v = [[Gv, -Bv], [Bv, Gv]],  e = [0, E]^T
# i_s_log = Y_v * (e - v_s)
# ---------------------------------------------------------------------------
i_s_log_d = Gv * (0    - v_sd) - Bv * (E - v_sq)   # eq. 17, d-component
i_s_log_q = Bv * (0    - v_sd) + Gv * (E - v_sq)   # eq. 17, q-component

# ---------------------------------------------------------------------------
# Differential equations  f:  dx/dt = f(x, y, u)   (eqs. 18, 19b)
# ---------------------------------------------------------------------------
f1 = (i_s_log_d - i_sd_star) / tau_lpf   # d(i_sd_star)/dt  — LPF d-axis
f2 = (i_s_log_q - i_sq_star) / tau_lpf   # d(i_sq_star)/dt  — LPF q-axis
f3 = i_sd_star - i_sd                    # d(xi_id)/dt      — PI integrator d
f4 = i_sq_star - i_sq                    # d(xi_iq)/dt      — PI integrator q

f_list = [f1, f2, f3, f4]

# ---------------------------------------------------------------------------
# Algebraic equations  g:  0 = g(x, y, u)   (eq. 19a)
# v_t = kpi*(i_s* - i_s) + kii*xi_i + omega*Lf*[iq, -id]^T + v_s
# ---------------------------------------------------------------------------
g1 = v_td - (kpi_cc * (i_sd_star - i_sd)
             + kii_cc * xi_id
             + omega_vsg * Lf * i_sq    # cross-coupling  +ω·Lf·i_sq
             + v_sd)                    # feed-forward

g2 = v_tq - (kpi_cc * (i_sq_star - i_sq)
             + kii_cc * xi_iq
             - omega_vsg * Lf * i_sd   # cross-coupling  −ω·Lf·i_sd
             + v_sq)                   # feed-forward

g_list = [g1, g2]

# ---------------------------------------------------------------------------
# Verification helpers
# ---------------------------------------------------------------------------
def _all_free_symbols():
    all_sym = set()
    for eq in f_list + g_list:
        all_sym |= eq.free_symbols
    return all_sym


def check_model():
    assert len(x_list) == len(f_list), "State / f-equation count mismatch"
    assert len(y_list) == len(g_list), "Algebraic / g-equation count mismatch"

    declared = (set(x_list) | set(y_list)
                | {v_sd, v_sq, i_sd, i_sq, E, omega_vsg, Lf}
                | set(params))
    undeclared = _all_free_symbols() - declared
    assert not undeclared, f"Undeclared symbols: {undeclared}"

    print("Model check passed:")
    print(f"  States      : {len(x_list)}  {x_names}")
    print(f"  Algebraic   : {len(y_list)}  {y_names}")
    print(f"  Parameters  : {list(params)}")


# ---------------------------------------------------------------------------
# PDF generation
# ---------------------------------------------------------------------------
def generate_pdf(filename: str = 'pi_cc_model.pdf') -> None:
    """Render the PI-CC DAE model to a one-page A4 PDF using matplotlib."""
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages

    def _tex(s: str) -> str:
        """Wrap a raw LaTeX string in $ delimiters for mathtext."""
        return f'${s}$'

    # ------------------------------------------------------------------
    # Equation strings (written for matplotlib mathtext, not full LaTeX)
    # ------------------------------------------------------------------
    # Virtual admittance (eq. 17)  — intermediate step
    va_d = _tex(r'i_{s,d}^{va} = -G_v\,v_{sd} - B_v\,(E - v_{sq})')
    va_q = _tex(r'i_{s,q}^{va} = -B_v\,v_{sd} + G_v\,(E - v_{sq})')

    # LPF (eq. 18)
    lpf_d = _tex(r'\dot{i}_{sd}^{\,*} = \frac{i_{s,d}^{va} - i_{sd}^{\,*}}{\tau_{lpf}}')
    lpf_q = _tex(r'\dot{i}_{sq}^{\,*} = \frac{i_{s,q}^{va} - i_{sq}^{\,*}}{\tau_{lpf}}')

    # PI integrators (eq. 19b)
    pi_d = _tex(r'\dot{\xi}_{id} = i_{sd}^{\,*} - i_{sd}')
    pi_q = _tex(r'\dot{\xi}_{iq} = i_{sq}^{\,*} - i_{sq}')

    # Algebraic — VSC terminal voltage (eq. 19a)
    alg_d = _tex(
        r'0 = v_{td} - \left['
        r'k_{pi}^{cc}(i_{sd}^{\,*} - i_{sd}) + k_{ii}^{cc}\,\xi_{id}'
        r' + \omega_{vsg}\,L_f\,i_{sq} + v_{sd}'
        r'\right]'
    )
    alg_q = _tex(
        r'0 = v_{tq} - \left['
        r'k_{pi}^{cc}(i_{sq}^{\,*} - i_{sq}) + k_{ii}^{cc}\,\xi_{iq}'
        r' - \omega_{vsg}\,L_f\,i_{sd} + v_{sq}'
        r'\right]'
    )

    # ------------------------------------------------------------------
    # Layout
    # ------------------------------------------------------------------
    fig = plt.figure(figsize=(8.27, 11.69))   # A4 portrait
    ax  = fig.add_axes([0.0, 0.0, 1.0, 1.0])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    def put(x, y, s, **kw):
        ax.text(x, y, s, transform=ax.transAxes, va='top', **kw)

    def hline(y, color='#888888', lw=0.7):
        ax.plot([0.06, 0.94], [y, y], color=color, linewidth=lw,
                transform=ax.transAxes, clip_on=False)

    L = 0.07   # left margin
    y = 0.965

    # ---- Title -------------------------------------------------------
    put(0.5, y, 'PI Current Controller (CC-ICL) — Differential-Algebraic Equations',
        ha='center', fontsize=13, fontweight='bold')
    y -= 0.030
    put(0.5, y,
        'Matas-Díaz et al., "A Systematic Small-signal …", JMPSCE 2025, §II.C.2, eqs. (17)–(20)',
        ha='center', fontsize=8.5, color='#555555', style='italic')
    y -= 0.018
    hline(y, color='#222222', lw=1.2)
    y -= 0.022

    # ---- Section 1: State variables ----------------------------------
    put(L, y, '1.  State variables  x  (4)', fontsize=10.5, fontweight='bold')
    y -= 0.024
    for sym, desc in [
        (_tex(r'i_{sd}^{\,*}'), 'd-axis filtered current reference  [LPF output]   (eq. 18)'),
        (_tex(r'i_{sq}^{\,*}'), 'q-axis filtered current reference  [LPF output]   (eq. 18)'),
        (_tex(r'\xi_{id}'),     'Integral of d-axis current error                   (eq. 19b)'),
        (_tex(r'\xi_{iq}'),     'Integral of q-axis current error                   (eq. 19b)'),
    ]:
        put(L + 0.03, y, sym,  fontsize=10.5)
        put(L + 0.14, y, '—',  fontsize=10,  color='#444444')
        put(L + 0.17, y, desc, fontsize=9.5, color='#222222')
        y -= 0.022

    y -= 0.008

    # ---- Section 2: Algebraic variables ------------------------------
    put(L, y, '2.  Algebraic variables  y  (2)', fontsize=10.5, fontweight='bold')
    y -= 0.024
    for sym, desc in [
        (_tex(r'v_{td}'), 'VSC terminal voltage, d-axis   (eq. 19a)'),
        (_tex(r'v_{tq}'), 'VSC terminal voltage, q-axis   (eq. 19a)'),
    ]:
        put(L + 0.03, y, sym,  fontsize=10.5)
        put(L + 0.14, y, '—',  fontsize=10,  color='#444444')
        put(L + 0.17, y, desc, fontsize=9.5, color='#222222')
        y -= 0.022

    y -= 0.008

    # ---- Section 3: Parameters ---------------------------------------
    put(L, y, '3.  Parameters  (default values, Table I)', fontsize=10.5, fontweight='bold')
    y -= 0.024
    for sym, val, desc in [
        (_tex(r'k_{pi}^{cc}'), '1.25  [V/A]',        'Proportional gain of PI current controller'),
        (_tex(r'k_{ii}^{cc}'), r'40.0  [V/(A·s)]',   'Integral gain of PI current controller'),
        (_tex(r'G_v'),         '0.0   [S]',           'Virtual conductance'),
        (_tex(r'B_v'),         '1.25  [S]',           'Virtual susceptance'),
        (_tex(r'\tau_{lpf}'),  '1.6 ms',              'LPF time constant'),
        (_tex(r'L_f'),         'caller-supplied [H]', 'Total filter inductance'),
    ]:
        put(L + 0.03, y, sym, fontsize=10.5)
        put(L + 0.16, y, val, fontsize=9.5,  color='#1a1a8c', family='monospace')
        put(L + 0.37, y, desc, fontsize=9.5, color='#222222')
        y -= 0.022

    y -= 0.010
    hline(y)
    y -= 0.022

    # ---- Section 4: Differential equations ---------------------------
    put(L, y, '4.  Differential equations   dx/dt = f(x, u)', fontsize=10.5, fontweight='bold')
    y -= 0.026

    put(L + 0.02, y,
        u'Virtual admittance output  (eq. 17,  eᵀ = [0, E]ᵀ,  '
        u'Yᵥ = [[Gᵥ, −Bᵥ], [Bᵥ, Gᵥ]]):',
        fontsize=8.5, color='#555555')
    y -= 0.032
    put(L + 0.06, y, va_d, fontsize=11.5)
    y -= 0.030
    put(L + 0.06, y, va_q, fontsize=11.5)
    y -= 0.036

    put(L + 0.02, y, 'LPF dynamics  (eq. 18):', fontsize=8.5, color='#555555')
    y -= 0.040
    put(L + 0.06, y, lpf_d, fontsize=13)
    y -= 0.048
    put(L + 0.06, y, lpf_q, fontsize=13)
    y -= 0.048

    put(L + 0.02, y, 'PI integrators  (eq. 19b):', fontsize=8.5, color='#555555')
    y -= 0.034
    put(L + 0.06, y, pi_d, fontsize=11.5)
    y -= 0.030
    put(L + 0.06, y, pi_q, fontsize=11.5)
    y -= 0.018

    hline(y)
    y -= 0.022

    # ---- Section 5: Algebraic equations ------------------------------
    put(L, y, '5.  Algebraic equations   0 = g(x, y, u)    (eq. 19a)', fontsize=10.5, fontweight='bold')
    y -= 0.036
    put(L + 0.06, y, alg_d, fontsize=11)
    y -= 0.036
    put(L + 0.06, y, alg_q, fontsize=11)
    y -= 0.030

    hline(y, color='#222222', lw=1.0)
    y -= 0.020

    # ---- Section 6: Inputs ------------------------------------------
    put(L, y, '6.  Inputs  u  (provided by other subsystems)', fontsize=10.5, fontweight='bold')
    y -= 0.024
    inputs = [
        (_tex(r'v_{sd},\;v_{sq}'),   'Grid-side inductor voltage, dq components'),
        (_tex(r'i_{sd},\;i_{sq}'),   'Measured grid-side current, dq components'),
        (_tex(r'E'),                  'Virtual EMF amplitude  (from OCL)'),
        (_tex(r'\omega_{vsg}'),       'VSG angular speed  (from OCL)'),
    ]
    for sym, desc in inputs:
        put(L + 0.03, y, sym,  fontsize=10.5)
        put(L + 0.22, y, '—',  fontsize=10,  color='#444444')
        put(L + 0.25, y, desc, fontsize=9.5, color='#222222')
        y -= 0.022

    y -= 0.010
    hline(y, color='#bbbbbb', lw=0.5)
    y -= 0.018
    put(0.5, y, 'Generated from  pi_cc_dae.py  ·  SymPy symbolic model',
        ha='center', fontsize=7.5, color='#999999')

    with PdfPages(filename) as pdf:
        pdf.savefig(fig, bbox_inches='tight', dpi=150)
    plt.close(fig)
    print(f"PDF saved: {filename}")


# ---------------------------------------------------------------------------
# Main — print equations for inspection
# ---------------------------------------------------------------------------
if __name__ == '__main__':
    check_model()

    print("\n--- Differential equations  dx/dt = f(x, y, u) ---")
    for name, eq in zip(x_names, f_list):
        print(f"  d({name})/dt = {eq}")

    print("\n--- Algebraic equations  0 = g(x, y, u) ---")
    for name, eq in zip(y_names, g_list):
        print(f"  0 = {eq}")

    print("\n--- Equations with default parameters substituted ---")
    print("Differential:")
    for name, eq in zip(x_names, f_list):
        print(f"  d({name})/dt = {eq.subs(params)}")
    print("Algebraic:")
    for name, eq in zip(y_names, g_list):
        print(f"  0 = {eq.subs(params)}")

    generate_pdf('pi_cc_model.pdf')
