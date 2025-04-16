from __future__ import annotations

import importlib.metadata

import neural_home_credit_default_risk as m


def test_version():
    """Test the version of the neural_home_credit_default_risk package.
    
    This function checks if the version obtained from `importlib.metadata.version` matches the expected version stored in
    module `m`.
    """
    assert importlib.metadata.version("neural_home_credit_default_risk") == m.__version__
