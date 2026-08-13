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
THEME_FILE = Path.home() / ".asistente_ong_theme"


def _saved_theme():
    try:
        value = THEME_FILE.read_text(encoding="utf-8").strip().lower()
        return value if value in {"light", "dark"} else "light"
    except Exception:
        return "light"


def launch_app():
    """Construye la aplicación y sincroniza su tema antes de crear la interfaz."""
    try:
        import customtkinter as ctk
        from src.ui.main_window import MainWindow
        ctk.set_appearance_mode(_saved_theme())
        app = MainWindow()
        # main_window históricamente fija el modo claro al importar; se vuelve a aplicar
        # después de construir la ventana para que el tema elegido gane prioridad.
        ctk.set_appearance_mode(_saved_theme())
        app.root.withdraw()
        app.root.update_idletasks()
        try:
            app.root.state("zoomed")
        except Exception:
            try:
                app.root.attributes("-zoomed", True)
            except Exception:
                pass
        app.root.update_idletasks()
        return app
    except Exception as exc:
        logger.error("Error crítico: %s", exc, exc_info=True)
        print(f"\nERROR CRITICO: {exc}\n")
        sys.exit(1)


if __name__ == "__main__":
    show_splash(on_complete=launch_app)
