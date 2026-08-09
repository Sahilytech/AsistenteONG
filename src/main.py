"""
Asistente ONG v0.9 - PUNTO DE ENTRADA LIMPIO
"""

import sys
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

try:
    logger.info("🆘 Iniciando Asistente ONG v0.9...")
    
    from src.ui.main_window import MainWindow
    logger.info("✅ UI importada correctamente")
    
    app = MainWindow()
    logger.info("✅ Aplicación lista")
    app.run()
    
except ImportError as e:
    logger.error(f"❌ Error de importación: {e}")
    print(f"\n❌ ERROR: {e}\n")
    sys.exit(1)
except Exception as e:
    logger.error(f"❌ Error: {e}", exc_info=True)
    print(f"\n❌ ERROR CRÍTICO: {e}\n")
    sys.exit(1)
