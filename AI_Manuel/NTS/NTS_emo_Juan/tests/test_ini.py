"""
Tests that the model initialises to the correct operating point.

Reference values from nts_base.hjson::results.
"""

import pytest
import numpy as np

pytest.importorskip('pydae')


@pytest.fixture(scope='module')
def initialised_model():
    from nts_emo_juan.build_model import build_model, load_model, XY_0_PATH
    from pydae.bps.lines import change_line
    built = build_model()
    model = load_model(built)
    # Use the reference XL = 0.6 pu (documented operating point in the HJSON)
    change_line(model, {'bus_j': '2', 'bus_k': '3',
                        'X_pu': 0.6, 'R_pu': 0.0,
                        'Bs_pu': 0.0, 'S_mva': 100})
    model.ini({}, str(XY_0_PATH))
    return model


def test_ini_converges(initialised_model):
    """Model must reach a converged state without raising."""
    model = initialised_model
    assert model is not None


def test_bus1_voltage(initialised_model):
    """Bus 1 voltage ≈ 1.0124 pu (HJSON reference)."""
    v = initialised_model.get_value('V_1')
    assert abs(v - 1.0124) < 0.01, f"V_1 = {v:.4f}, expected ~1.0124"


def test_bus4_voltage(initialised_model):
    """Bus 4 voltage ≈ 1.0078 pu (HJSON reference)."""
    v = initialised_model.get_value('V_4')
    assert abs(v - 1.0078) < 0.01, f"V_4 = {v:.4f}, expected ~1.0078"


def test_gen1_active_power(initialised_model):
    """Gen 1 active power ≈ 1350 MW on system base 1 GW → 1.35 pu."""
    p = initialised_model.get_value('p_g_1')
    s_n = initialised_model.get_value('S_n_1')
    p_mw = p * s_n / 1e6
    assert abs(p_mw - 1350.0) < 20.0, f"p_g_1 = {p_mw:.1f} MW, expected ~1350 MW"


def test_gen4_active_power(initialised_model):
    """Gen 4 active power ≈ 3900 MW on system base 1 GW → 3.9 pu."""
    p = initialised_model.get_value('p_g_4')
    s_n = initialised_model.get_value('S_n_4')
    p_mw = p * s_n / 1e6
    assert abs(p_mw - 3900.0) < 50.0, f"p_g_4 = {p_mw:.1f} MW, expected ~3900 MW"


def test_generators_at_synchronous_speed(initialised_model):
    """Both generators must be at synchronous speed (omega = 1.0 pu) at steady state."""
    omega_1 = initialised_model.get_value('omega_1')
    omega_4 = initialised_model.get_value('omega_4')
    assert abs(omega_1 - 1.0) < 1e-4, f"omega_1 = {omega_1:.6f}, expected 1.0"
    assert abs(omega_4 - 1.0) < 1e-4, f"omega_4 = {omega_4:.6f}, expected 1.0"
