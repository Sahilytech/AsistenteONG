"""
Configuración central de la aplicación
"""

from pathlib import Path
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Rutas
BASE_DIR = Path(__file__).parent.parent
SRC_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"
DOCS_DIR = BASE_DIR / "docs"

# Crear directorios si no existen
DATA_DIR.mkdir(exist_ok=True)
MODELS_DIR.mkdir(exist_ok=True)

# Database
DATABASE_PATH = DATA_DIR / "asistente.db"

# Modelos IA
MODEL_PATH = MODELS_DIR / "gemma-3-1b.gguf"
MODEL_URL = os.getenv("MODEL_URL", "https://huggingface.co/...")

# Configuración IA
AI_MODEL = "gemma-3-1b"
AI_CONTEXT_SIZE = 1024
AI_TEMPERATURE = 0.7

# Configuración de seguridad
ENCRYPTION_KEY_PATH = DATA_DIR / ".key"
ENABLE_2FA = False

# Configuración de la aplicación
APP_NAME = "Asistente ONG"
APP_VERSION = "0.1.0"
APP_LANGUAGE = "es"

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = DATA_DIR / "asistente.log"

# Desarrollo
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
TESTING = os.getenv("TESTING", "False").lower() == "true"
