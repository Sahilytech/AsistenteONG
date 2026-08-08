"""
Configuración central de la aplicación - Portable, rutas relativas
"""

from pathlib import Path
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Detectar si estamos en modo portable (ejecutable PyInstaller)
if getattr(sys, 'frozen', False):
    # Estamos en un ejecutable PyInstaller
    BASE_DIR = Path(sys.executable).parent
else:
    # Estamos en desarrollo
    BASE_DIR = Path(__file__).parent.parent

SRC_DIR = BASE_DIR / "src"
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"
DOCS_DIR = BASE_DIR / "docs"
ASSETS_DIR = BASE_DIR / "assets"

# Crear directorios si no existen
DATA_DIR.mkdir(exist_ok=True)
MODELS_DIR.mkdir(exist_ok=True)

# Database
DATABASE_PATH = DATA_DIR / "asistente.db"

# Modelos IA
MODEL_PATH = MODELS_DIR / "gemma-3-1b.gguf"
MODEL_URL = os.getenv("MODEL_URL", "")

# Configuración IA
AI_MODEL = "gemma-3-1b"
AI_CONTEXT_SIZE = 512  # Reducido para PCs de bajos recursos
AI_TEMPERATURE = 0.7
AI_MAX_TOKENS = 256
AI_THREADS = 2  # Limitar threads para no saturar CPU

# Configuración de seguridad
ENCRYPTION_KEY_PATH = DATA_DIR / ".key"
ENABLE_2FA = False

# Configuración de la aplicación
APP_NAME = "Asistente ONG"
APP_VERSION = "0.9.0"
APP_LANGUAGE = "es"

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = DATA_DIR / "asistente.log"

# Desarrollo
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
TESTING = os.getenv("TESTING", "False").lower() == "true"

# Modo bajo consumo (para PCs del gobierno)
LOW_RESOURCE_MODE = os.getenv("LOW_RESOURCE_MODE", "False").lower() == "true"
