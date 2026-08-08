"""
Esquema de base de datos SQLite - Inicialización robusta
"""

import sqlite3
from pathlib import Path
import logging
import sys

logger = logging.getLogger(__name__)

# Ruta de la base de datos (portable)
if getattr(sys, 'frozen', False):
    BASE_DIR = Path(sys.executable).parent
else:
    BASE_DIR = Path(__file__).parent.parent.parent

DB_PATH = BASE_DIR / "data" / "asistente.db"


SCHEMA = """
-- Tabla de usuarios
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT DEFAULT 'operator',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de casos
CREATE TABLE IF NOT EXISTS cases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    case_number TEXT UNIQUE NOT NULL,
    input_text TEXT NOT NULL,
    summary TEXT,
    urgency TEXT,
    case_type TEXT,
    status TEXT DEFAULT 'new',
    created_by INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES users(id)
);

-- Tabla de análisis de casos
CREATE TABLE IF NOT EXISTS case_analysis (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    case_id INTEGER NOT NULL,
    emotions TEXT,
    risk_factors TEXT,
    identified_people TEXT,
    ai_score REAL,
    analysis_data TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (case_id) REFERENCES cases(id)
);

-- Tabla de recursos
CREATE TABLE IF NOT EXISTS resources (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    type TEXT,
    phone TEXT,
    email TEXT,
    address TEXT,
    hours TEXT,
    description TEXT,
    region TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de auditoría
CREATE TABLE IF NOT EXISTS audit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    action TEXT NOT NULL,
    table_name TEXT,
    record_id INTEGER,
    details TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Índices
CREATE INDEX IF NOT EXISTS idx_case_status ON cases(status);
CREATE INDEX IF NOT EXISTS idx_case_urgency ON cases(urgency);
CREATE INDEX IF NOT EXISTS idx_case_type ON cases(case_type);
CREATE INDEX IF NOT EXISTS idx_audit_user ON audit_log(user_id);
CREATE INDEX IF NOT EXISTS idx_audit_timestamp ON audit_log(timestamp);
"""


def init_database():
    """Inicializa la base de datos con el esquema."""
    try:
        DB_PATH.parent.mkdir(parents=True, exist_ok=True)

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Ejecutar schema
        for statement in SCHEMA.split(';'):
            if statement.strip():
                cursor.execute(statement)

        conn.commit()
        conn.close()

        logger.info(f"✅ Base de datos inicializada en {DB_PATH}")

    except Exception as e:
        logger.error(f"❌ Error inicializando base de datos: {e}")
        raise


def get_connection():
    """Obtiene una conexión a la base de datos."""
    return sqlite3.connect(DB_PATH)


if __name__ == "__main__":
    init_database()
