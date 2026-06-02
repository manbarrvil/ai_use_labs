"""
Complex-plane eigenvalue plot with damping cones (replicates NTS Fig 17/18/20).
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.patches import Polygon


def _damping_cone_lines(zeta: float, sigma_min: float = -10.0, n: int = 100):
    """
    Return (sigma, freq_hz_upper, freq_hz_lower) arrays for a damping cone.

    Damping ratio ζ = cos(θ)  ↔  tan(θ) = √(1-ζ²)/ζ
    Slope in (σ, ω/2π) space:  f_hz = -σ * √(1-ζ²) / (ζ · 2π)
    """
    slope = np.sqrt(1.0 - zeta**2) / (zeta * 2.0 * np.pi)
    sigma = np.linspace(sigma_min, 0.0, n)
    f_hz  = -sigma * slope   # always ≥ 0 since sigma ≤ 0
    return sigma, f_hz, -f_hz


def plot_eigenvalue_sweep(results: dict,
                          damping_cones: list = None,
                          freq_range: tuple = (0.1, 1.5),
                          ax=None) -> plt.Figure:
    """
    Plot all eigenvalues from an XL sweep on the complex plane.

    - x-axis: real part σ
    - y-axis: imaginary part ω/(2π) in Hz (positive only — complex conjugates shown)
    - Electromechanical modes colour-coded by XL with a colourbar
    - All other modes plotted as small grey markers
    - Damping cones drawn as dashed lines with shaded regions

    Parameters
    ----------
    results       : dict returned by :func:`nts_emo.analysis.xl_sweep`
    damping_cones : list of damping ratios for cone lines (default [0.03, 0.05])
    freq_range    : (f_min, f_max) Hz — window shown on y-axis
    ax            : optional Axes; creates a new figure if None

    Returns
    -------
    matplotlib.figure.Figure
    """
    if damping_cones is None:
        damping_cones = [0.03, 0.05]

    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 7))
    else:
        fig = ax.get_figure()

    xl_values = np.asarray(results['xl_values'])
    n_xl = len(xl_values)
    cmap = cm.viridis
    colours = cmap(np.linspace(0.2, 0.9, n_xl))

    # Determine plot limits from the electromechanical modes
    em_modes = results['em_modes']
    sigma_all = [lam.real for lam in em_modes if not np.isnan(lam.real)]
    sigma_min = min(sigma_all) * 1.5 if sigma_all else -6.0

    # ------------------------------------------------------------------
    # 1. Damping cones (shaded wedges + dashed boundary lines)
    # ------------------------------------------------------------------
    cone_colours = ['#e74c3c', '#e67e22']  # red for 3%, orange for 5%
    cone_labels  = ['3% damping', '5% damping']

    for zeta, colour, label in zip(damping_cones, cone_colours, cone_labels):
        sigma, f_upper, _ = _damping_cone_lines(zeta, sigma_min=sigma_min)
        f_max_cone = max(freq_range[1] * 1.2, max(f_upper))
        # Shade region between σ=sigma_min line and the cone
        verts = (list(zip(sigma, f_upper)) +
                 [(0.0, 0.0), (sigma_min, 0.0)])
        poly = Polygon(verts, closed=True, alpha=0.08, color=colour, zorder=0)
        ax.add_patch(poly)
        ax.plot(sigma, f_upper, '--', color=colour, lw=1.5,
                label=f'ζ = {zeta*100:.0f}%', zorder=1)

    # ------------------------------------------------------------------
    # 2. All eigenvalues (grey background markers)
    # ------------------------------------------------------------------
    for eig_arr in results['eigenvalues']:
        if eig_arr is None:
            continue
        for lam in eig_arr:
            if np.isnan(lam.real):
                continue
            f_hz = abs(lam.imag) / (2 * np.pi)
            if f_hz < 1e-3:
                continue   # skip non-oscillatory modes
            ax.plot(lam.real, f_hz, '.', color='#bdc3c7', ms=3, zorder=2)

    # ------------------------------------------------------------------
    # 3. Electromechanical mode trajectory (colour-coded by XL)
    # ------------------------------------------------------------------
    for i, (xl, lam) in enumerate(zip(xl_values, em_modes)):
        if np.isnan(lam.real):
            continue
        f_hz = abs(lam.imag) / (2 * np.pi)
        sc = ax.scatter(lam.real, f_hz, color=colours[i], s=50, zorder=4,
                        edgecolors='k', linewidths=0.5)

    # Connect EM mode trajectory with a line
    valid_xl = [(i, xl) for i, xl in enumerate(xl_values)
                if not np.isnan(em_modes[i].real)]
    if len(valid_xl) >= 2:
        xdata = [em_modes[i].real for i, _ in valid_xl]
        ydata = [abs(em_modes[i].imag) / (2 * np.pi) for i, _ in valid_xl]
        ax.plot(xdata, ydata, '-', color='#2c3e50', lw=1.0, zorder=3,
                label='EM mode (MGES only)')

    # Colourbar for XL
    sm = plt.cm.ScalarMappable(cmap=cmap,
                               norm=plt.Normalize(vmin=xl_values.min(),
                                                  vmax=xl_values.max()))
    sm.set_array([])
    cbar = fig.colorbar(sm, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label('$X_L$ (pu)', fontsize=11)

    # ------------------------------------------------------------------
    # 4. Formatting
    # ------------------------------------------------------------------
    ax.axvline(0, color='k', lw=0.8, ls=':')
    ax.set_xlim(sigma_min, 0.5)
    ax.set_ylim(-0.05, freq_range[1] * 1.1)
    ax.set_xlabel('Real  $\\sigma$  (rad/s)', fontsize=12)
    ax.set_ylabel('Imaginary  $\\omega/2\\pi$  (Hz)', fontsize=12)
    ax.set_title('Eigenvalue sweep — NTS §5.10.2.1 (MGES only, no MPE)', fontsize=11)
    ax.legend(fontsize=9, loc='upper left')
    ax.grid(True, alpha=0.3)

    fig.tight_layout()
    return fig
