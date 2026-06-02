"""
Integration test: build the pydae model and check the compiled artefacts.

Marked as slow — run with:  pytest -m slow
"""

import os
import json
import pytest

BUILD_DIR = os.path.join(os.path.dirname(__file__), '..', 'build_test')


@pytest.mark.slow
def test_build_creates_json():
    from nts_emo.build_model import build_nts_model
    build_nts_model(output_dir=BUILD_DIR, force_rebuild=False)
    json_path = os.path.join(BUILD_DIR, 'nts2gen_data.json')
    assert os.path.exists(json_path), f'JSON not found at {json_path}'


@pytest.mark.slow
def test_json_has_expected_keys():
    json_path = os.path.join(BUILD_DIR, 'nts2gen_data.json')
    if not os.path.exists(json_path):
        pytest.skip('Model not built yet — run test_build_creates_json first')
    with open(json_path) as fh:
        data = json.load(fh)
    for key in ('x_list', 'y_ini_list', 'params_dict', 'u_ini_dict'):
        assert key in data, f'Missing key: {key}'


@pytest.mark.slow
def test_model_loads():
    from nts_emo.build_model import load_model
    model = load_model(BUILD_DIR)
    assert model.N_x == 26, f'Expected 26 states, got {model.N_x}'


@pytest.mark.slow
def test_initialization_converges():
    from nts_emo.build_model import load_model
    model = load_model(BUILD_DIR)
    ok = model.ini({'XL': 0.1}, xy_0=1.0)
    assert ok, 'Newton-Raphson did not converge for XL=0.1'


@pytest.mark.slow
def test_slack_bus_voltage_at_init():
    from nts_emo.build_model import load_model
    model = load_model(BUILD_DIR)
    model.ini({'XL': 0.1}, xy_0=1.0)
    e4 = model.get_value('e_4')
    f4 = model.get_value('f_4')
    assert abs(e4 - 1.0) < 1e-4, f'e_4 = {e4:.5f}, expected ~1.0'
    assert abs(f4) < 1e-4, f'f_4 = {f4:.6f}, expected 0.0'
