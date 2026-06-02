"""
Integration tests for the XL sweep analysis.

Requires the model to be built first (pytest -m slow).
"""

import os
import numpy as np
import pytest

BUILD_DIR = os.path.join(os.path.dirname(__file__), '..', 'build_test')
SKIP_MSG = 'Model not built — run test_build_model.py::test_build_creates_json first'


def _model_available():
    return os.path.exists(os.path.join(BUILD_DIR, 'nts2gen_data.json'))


@pytest.mark.slow
def test_sweep_returns_correct_structure():
    if not _model_available():
        pytest.skip(SKIP_MSG)
    from nts_emo.analysis import xl_sweep
    results = xl_sweep([0.1, 0.3, 0.6], model_dir=BUILD_DIR)
    assert len(results['xl_values']) == 3
    assert len(results['eigenvalues']) == 3
    assert len(results['em_modes']) == 3


@pytest.mark.slow
def test_all_eigenvalues_stable():
    """All eigenvalues must have negative real parts (stable operating point)."""
    if not _model_available():
        pytest.skip(SKIP_MSG)
    from nts_emo.analysis import xl_sweep
    results = xl_sweep([0.1, 0.3, 0.6], model_dir=BUILD_DIR)
    for xl, eigs in zip(results['xl_values'], results['eigenvalues']):
        if eigs is None:
            continue
        unstable = [lam for lam in eigs if lam.real > 1e-4]
        assert not unstable, (
            f'Unstable modes at XL={xl}: {unstable}'
        )


@pytest.mark.slow
def test_em_mode_frequency_range():
    """EM mode frequencies must lie between 0.1 and 1.5 Hz."""
    if not _model_available():
        pytest.skip(SKIP_MSG)
    from nts_emo.analysis import xl_sweep
    results = xl_sweep([0.1, 0.3, 0.6], model_dir=BUILD_DIR)
    for xl, f_hz in zip(results['xl_values'], results['em_freq_hz']):
        if np.isnan(f_hz):
            continue
        assert 0.1 <= f_hz <= 1.5, (
            f'EM mode frequency {f_hz:.3f} Hz out of range [0.1, 1.5] at XL={xl}'
        )


@pytest.mark.slow
def test_em_mode_frequency_decreases_with_xl():
    """Higher XL → lower EM mode frequency (inter-area behaviour)."""
    if not _model_available():
        pytest.skip(SKIP_MSG)
    from nts_emo.analysis import xl_sweep
    results = xl_sweep([0.05, 0.3, 0.6], model_dir=BUILD_DIR)
    freqs = [f for f in results['em_freq_hz'] if not np.isnan(f)]
    if len(freqs) >= 2:
        assert freqs[-1] < freqs[0], (
            f'Frequency should decrease with XL; got {freqs}'
        )


@pytest.mark.slow
def test_em_mode_damping_above_5pct():
    """PSS2A should keep damping above 5% at all XL values (NTS acceptance criterion)."""
    if not _model_available():
        pytest.skip(SKIP_MSG)
    from nts_emo.analysis import xl_sweep
    xl_values = list(np.arange(0.05, 0.61, 0.05))
    results = xl_sweep(xl_values, model_dir=BUILD_DIR)
    for xl, zeta in zip(results['xl_values'], results['em_damp']):
        if np.isnan(zeta):
            continue
        assert zeta >= 0.05, (
            f'Damping {zeta*100:.1f}% < 5% at XL={xl:.2f} pu'
        )
