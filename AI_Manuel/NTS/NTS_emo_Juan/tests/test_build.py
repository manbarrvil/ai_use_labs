"""
Tests that the model builds without error and produces a loadable CasADi model.
"""

import pytest
from pathlib import Path


def test_build_returns_descriptor():
    from nts_emo_juan.build_model import build_model
    built = build_model()
    assert built is not None


def test_load_model_returns_model():
    from nts_emo_juan.build_model import build_model, load_model
    from pydae.core.model import CasadiModel
    built = build_model()
    model = load_model(built)
    assert isinstance(model, CasadiModel)


def test_hjson_case_file_present():
    from nts_emo_juan.build_model import HJSON_PATH
    assert HJSON_PATH.exists(), f"HJSON not found at {HJSON_PATH}"


def test_xy0_file_present():
    from nts_emo_juan.build_model import XY_0_PATH
    assert XY_0_PATH.exists(), f"xy_0 not found at {XY_0_PATH}"


def test_load_model_no_args():
    """load_model() without arguments should build internally and return a model."""
    from nts_emo_juan.build_model import load_model
    from pydae.core.model import CasadiModel
    model = load_model()
    assert isinstance(model, CasadiModel)
