"""Tests de ejemplo"""

import pytest


def test_app_imports():
    """Test que la aplicación se puede importar."""
    try:
        import src
        assert src.__version__ == "0.1.0"
    except ImportError:
        pytest.fail("No se puede importar src")


def test_config_loads():
    """Test que la configuración se carga correctamente."""
    from src.config import APP_NAME, APP_VERSION
    assert APP_NAME == "Asistente ONG"
    assert APP_VERSION == "0.1.0"
