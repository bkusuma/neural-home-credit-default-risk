from __future__ import annotations

import importlib.metadata

import neural_home_credit_default_risk as m


def test_version():
    assert importlib.metadata.version("neural_home_credit_default_risk") == m.__version__
