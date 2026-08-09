"""Punto de entrada de Asistente ONG.

Soporta tanto ``python -m src.main`` como ``python src/main.py`` en Windows.
"""
import logging
import sys
from pathlib import Path

# Cuando se ejecuta ``python src/main.py``, Python agrega ``src/`` a sys.path
# y no la raíz del proyecto. Agregamos la raíz para que los imports ``src.*``
# funcionen igual que con ``python -m src.main``.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.ui.splash_screen import show_splash

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def launch_app():
    try:
        from src.ui.main_window import MainWindow
        MainWindow().run()
    except Exception as exc:
        logger.error("Error crítico: %s", exc, exc_info=True)
        print(f"\nERROR CRITICO: {exc}\n")
        sys.exit(1)


if __name__ == "__main__":
    show_splash(on_complete=launch_app)
