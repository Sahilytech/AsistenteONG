"""Punto de entrada de Asistente ONG."""
import logging
import sys
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
