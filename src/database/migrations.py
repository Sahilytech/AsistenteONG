"""
Sistema de migraciones para la base de datos
"""

import sqlite3
import logging
from pathlib import Path
from datetime import datetime

from .schema import get_connection, DB_PATH

logger = logging.getLogger(__name__)

MIGRATIONS_DIR = Path(__file__).parent / "migrations"


class MigrationManager:
    """Gestor de migraciones."""
    
    def __init__(self):
        self.conn = None
        self.migrations_table = "schema_migrations"
    
    def _create_migrations_table(self):
        """Crea tabla de control de migraciones."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {self.migrations_table} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                migration_name TEXT UNIQUE NOT NULL,
                executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()
    
    def get_executed_migrations(self) -> list:
        """Obtiene lista de migraciones ejecutadas."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT migration_name FROM {self.migrations_table}")
        migrations = [row[0] for row in cursor.fetchall()]
        conn.close()
        return migrations
    
    def record_migration(self, migration_name: str):
        """Registra una migración como ejecutada."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            f"INSERT INTO {self.migrations_table} (migration_name) VALUES (?)",
            (migration_name,)
        )
        conn.commit()
        conn.close()
    
    def get_pending_migrations(self) -> list:
        """Obtiene migraciones pendientes."""
        if not MIGRATIONS_DIR.exists():
            MIGRATIONS_DIR.mkdir(parents=True)
            return []
        
        executed = self.get_executed_migrations()
        migration_files = sorted(MIGRATIONS_DIR.glob("*.sql"))
        
        pending = [
            f.name for f in migration_files
            if f.name not in executed
        ]
        
        return pending
    
    def run_migrations(self) -> bool:
        """Ejecuta todas las migraciones pendientes."""
        self._create_migrations_table()
        
        pending = self.get_pending_migrations()
        
        if not pending:
            logger.info("No hay migraciones pendientes")
            return True
        
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            for migration_file in pending:
                migration_path = MIGRATIONS_DIR / migration_file
                
                with open(migration_path, "r") as f:
                    sql = f.read()
                
                logger.info(f"Ejecutando migración: {migration_file}")
                
                # Ejecutar cada statement
                for statement in sql.split(";"):
                    if statement.strip():
                        cursor.execute(statement)
                
                self.record_migration(migration_file)
            
            conn.commit()
            logger.info(f"✅ {len(pending)} migraciones ejecutadas")
            return True
            
        except Exception as e:
            conn.rollback()
            logger.error(f"❌ Error en migración: {e}")
            return False
        finally:
            conn.close()
    
    def rollback_last(self) -> bool:
        """Revierte la última migración (si existe rollback)."""
        # Implementación futura
        logger.warning("Rollback no implementado aún")
        return False


def init_migrations():
    """Inicializa el sistema de migraciones."""
    manager = MigrationManager()
    return manager.run_migrations()


if __name__ == "__main__":
    init_migrations()
