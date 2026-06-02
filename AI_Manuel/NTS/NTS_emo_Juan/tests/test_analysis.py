"""
Tests for the XL sweep eigenvalue analysis.

Fast tests check the output structure and helper functions.
Slow tests (marked @pytest.mark.slow) run the full sweep and verify
the NTS §5.10.3.1 acceptance criterion: damping ≥ 5 % at all XL.
"""

import pytest
import numpy as np

pytest.importorskip('pydae')

from nts_emo_juan.analysis import _find_em_mode, _damp_dataframe


# ─── Unit tests for helpers ───────────────────────────────────────────────────

def test_find_em_mode_identifies_correct_frequency():
    """_find_em_mode must return the eigenvalue whose frequency is in [0.1, 1.5] Hz."""
    omega_em = 2.0 * np.pi * 0.8   # 0.8 Hz inter-area mode
    sigma_em = -0.2
    eigs = np.array([
        complex(sigma_em, omega_em),
        complex(sigma_em, -omega_em),
        complex(-5.0, 50.0),    # control mode, ~8 Hz — outside range
        complex(-3.0, 0.0),     # real mode
    ])
    val, f, z = _find_em_mode(eigs)
    assert abs(f - 0.8) < 1e-6
    assert z > 0.0   # positive damping


def test_find_em_mode_no_em_returns_nan():
    """If no mode is in [0.1, 1.5] Hz the result must be NaN."""
    eigs = np.array([complex(-5.0, 50.0), complex(-3.0, 0.0)])
    val, f, z = _find_em_mode(eigs)
    assert np.isnan(f)
    assert np.isnan(z)


def test_damp_dataframe_skips_real_modes():
    omega_em = 2.0 * np.pi * 0.5
    eigs = np.array([complex(-0.1, omega_em), complex(-3.0, 0.0)])
    df = _damp_dataframe(eigs)
    assert len(df) == 1   # only the oscillatory mode
    assert abs(df.iloc[0]['freq_hz'] - 0.5) < 1e-6


def test_damp_dataframe_empty_for_real_only():
    eigs = np.array([complex(-1.0, 0.0), complex(-2.0, 0.0)])
    df = _damp_dataframe(eigs)
    assert len(df) == 0


# ─── Integration tests (require model build) ──────────────────────────────────

@pytest.fixture(scope='module')
def sweep_results():
    from nts_emo_juan import build_model, xl_sweep
    xl_values = [0.01, 0.1, 0.3, 0.6]
    built = build_model()
    return xl_sweep(xl_values, built=built)


@pytest.mark.slow
def test_sweep_result_keys(sweep_results):
    required = {'xl_values', 'eigenvalues', 'damp_df', 'em_modes',
                'em_freq_hz', 'em_damp'}
    assert required.issubset(sweep_results.keys())


@pytest.mark.slow
def test_sweep_list_lengths(sweep_results):
    n = len(sweep_results['xl_values'])
    for key in ('eigenvalues', 'damp_df', 'em_modes', 'em_freq_hz', 'em_damp'):
        assert len(sweep_results[key]) == n, f"Length mismatch for '{key}'"


@pytest.mark.slow
def test_all_eigenvalues_stable(sweep_results):
    """All eigenvalues must have strictly negative real parts (stable system)."""
    for i, eigs in enumerate(sweep_results['eigenvalues']):
        xl = sweep_results['xl_values'][i]
        if eigs is None:
            continue
        unstable = [lam for lam in eigs if not np.isnan(lam.real) and lam.real >= 0]
        assert not unstable, (
            f"Unstable eigenvalue(s) at XL={xl:.3f}: {unstable}"
        )


@pytest.mark.slow
def test_em_mode_frequency_in_range(sweep_results):
    """EM mode frequency must be in [0.1, 1.5] Hz at every XL."""
    for xl, f in zip(sweep_results['xl_values'], sweep_results['em_freq_hz']):
        if np.isnan(f):
            pytest.fail(f"No EM mode found at XL={xl:.3f}")
        assert 0.1 <= f <= 1.5, f"EM freq {f:.3f} Hz out of range at XL={xl:.3f}"


@pytest.mark.slow
def test_em_mode_damping_above_5_percent(sweep_results):
    """NTS §5.10.3.1: EM mode damping must be ≥ 5 % at all XL values."""
    for xl, z in zip(sweep_results['xl_values'], sweep_results['em_damp']):
        if np.isnan(z):
            pytest.fail(f"No EM mode found at XL={xl:.3f}")
        assert z >= 0.05, (
            f"EM damping {z*100:.1f}% < 5% at XL={xl:.3f}"
        )


@pytest.mark.slow
def test_em_frequency_decreases_with_xl(sweep_results):
    """Inter-area mode frequency must decrease as XL increases (weaker tie)."""
    freqs = [f for f in sweep_results['em_freq_hz'] if not np.isnan(f)]
    assert len(freqs) >= 2
    # Check monotonically decreasing (allow small numerical noise: 1 mHz)
    for a, b in zip(freqs[:-1], freqs[1:]):
        assert a >= b - 0.001, (
            f"EM freq not monotonically decreasing: {a:.4f} → {b:.4f} Hz"
        )
