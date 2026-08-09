"""
Asistente ONG v0.9 - Punto de entrada
"""

import sys
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

try:
    logger.info("🆘 Iniciando Asistente ONG v0.9...")
    
    # Imports mínimos necesarios
    from src.ui.main_window import MainWindow
    from src.case_manager import CaseManager
    from src.config_manager import ConfigManager
    
    logger.info("✅ Importes completados")
    
    # Iniciar aplicación
    app = MainWindow()
    logger.info("✅ MainWindow inicializada")
    app.run()
    
except Exception as e:
    logger.error(f"❌ Error: {e}", exc_info=True)
    print(f"\n❌ ERROR CRÍTICO: {e}\n")
    sys.exit(1)
