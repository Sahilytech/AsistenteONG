#!/usr/bin/env python3
"""
Asistente de Triaje y Canalización para Líneas de Ayuda
Punto de entrada - Sarah Lee Olivera, 2025
"""

import sys
import logging
from pathlib import Path

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Función principal."""
    logger.info("🆘 Iniciando Asistente ONG...")
    
    try:
        # Import RELATIVO (con punto)
        from .ui.main_window import MainWindow
        
        logger.info("✅ Cargando interfaz gráfica...")
        app = MainWindow()
        app.run()
        
    except ImportError as e:
        logger.error(f"❌ Error de importación: {e}")
        print(f"❌ Error de importación: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Error: {e}", exc_info=True)
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
