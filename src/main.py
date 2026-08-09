"""Punto de entrada de Asistente ONG."""
import logging
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.ui.splash_screen import show_splash

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def launch_app():
    try:
        from src.ui.main_window import MainWindow
        app = MainWindow()
        # Maximizar antes de mostrar el primer frame evita el salto visual de 1500x900 a pantalla completa.
        app.root.update_idletasks()
        try:
            app.root.state("zoomed")
        except Exception:
            app.root.attributes("-zoomed", True)
        app.root.update_idletasks()
        app.run()
    except Exception as exc:
        logger.error("Error crítico: %s", exc, exc_info=True)
        print(f"\nERROR CRITICO: {exc}\n")
        sys.exit(1)


if __name__ == "__main__":
    show_splash(on_complete=launch_app)
