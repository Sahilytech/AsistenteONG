"""
Data Access Object - Operaciones CRUD con SQLite
"""

import sqlite3
import logging
from typing import List, Dict, Optional, Any
from datetime import datetime

from .schema import get_connection, DB_PATH

logger = logging.getLogger(__name__)


class CaseDAO:
    """DAO para operaciones con casos."""

    @staticmethod
    def create(case_data: Dict[str, Any]) -> bool:
        """Crea un nuevo caso."""
        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO cases (case_number, input_text, summary, urgency, case_type, status, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                case_data.get("case_number"),
                case_data.get("text", ""),
                case_data.get("summary", ""),
                case_data.get("urgency", "Baja"),
                case_data.get("case_type", "general"),
                case_data.get("status", "new"),
                datetime.now().isoformat()
            ))

            conn.commit()
            conn.close()
            logger.info(f"✅ Caso creado: {case_data.get('case_number')}")
            return True
        except Exception as e:
            logger.error(f"Error creando caso: {e}")
            return False

    @staticmethod
    def get_by_number(case_number: str) -> Optional[Dict]:
        """Obtiene un caso por numero."""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM cases WHERE case_number = ?", (case_number,))
            row = cursor.fetchone()
            conn.close()

            if row:
                return {
                    "id": row[0],
                    "case_number": row[1],
                    "text": row[2],
                    "summary": row[3],
                    "urgency": row[4],
                    "case_type": row[5],
                    "status": row[6],
                    "created_at": row[8]
                }
            return None
        except Exception as e:
            logger.error(f"Error obteniendo caso: {e}")
            return None

    @staticmethod
    def list_all(limit: int = 100) -> List[Dict]:
        """Lista todos los casos."""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM cases ORDER BY created_at DESC LIMIT ?", (limit,))
            rows = cursor.fetchall()
            conn.close()

            return [{
                "id": row[0],
                "case_number": row[1],
                "text": row[2],
                "summary": row[3],
                "urgency": row[4],
                "case_type": row[5],
                "status": row[6],
                "created_at": row[8]
            } for row in rows]
        except Exception as e:
            logger.error(f"Error listando casos: {e}")
            return []

    @staticmethod
    def filter_by_urgency(urgency: str) -> List[Dict]:
        """Filtra casos por urgencia."""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM cases WHERE urgency = ? ORDER BY created_at DESC", (urgency,))
            rows = cursor.fetchall()
            conn.close()

            return [{
                "id": row[0],
                "case_number": row[1],
                "text": row[2],
                "summary": row[3],
                "urgency": row[4],
                "case_type": row[5],
                "status": row[6],
                "created_at": row[8]
            } for row in rows]
        except Exception as e:
            logger.error(f"Error filtrando casos: {e}")
            return []

    @staticmethod
    def update_status(case_number: str, status: str) -> bool:
        """Actualiza el estado de un caso."""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE cases SET status = ? WHERE case_number = ?", (status, case_number))
            conn.commit()
            conn.close()
            logger.info(f"✅ Estado actualizado: {case_number} -> {status}")
            return True
        except Exception as e:
            logger.error(f"Error actualizando estado: {e}")
            return False

    @staticmethod
    def delete(case_number: str) -> bool:
        """Elimina un caso."""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM cases WHERE case_number = ?", (case_number,))
            conn.commit()
            conn.close()
            logger.info(f"🗑️ Caso eliminado: {case_number}")
            return True
        except Exception as e:
            logger.error(f"Error eliminando caso: {e}")
            return False

    @staticmethod
    def count_by_urgency() -> Dict[str, int]:
        """Cuenta casos por nivel de urgencia."""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT urgency, COUNT(*) FROM cases GROUP BY urgency")
            rows = cursor.fetchall()
            conn.close()

            return {row[0]: row[1] for row in rows}
        except Exception as e:
            logger.error(f"Error contando casos: {e}")
            return {}

    @staticmethod
    def count_today() -> int:
        """Cuenta casos de hoy."""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            today = datetime.now().strftime("%Y-%m-%d")
            cursor.execute("SELECT COUNT(*) FROM cases WHERE date(created_at) = ?", (today,))
            count = cursor.fetchone()[0]
            conn.close()
            return count
        except Exception as e:
            logger.error(f"Error contando casos de hoy: {e}")
            return 0


class ResourceDAO:
    """DAO para operaciones con recursos."""

    @staticmethod
    def create(resource_data: Dict[str, Any]) -> bool:
        """Crea un nuevo recurso."""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO resources (name, type, phone, email, address, hours, description, region)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                resource_data.get("name"),
                resource_data.get("type"),
                resource_data.get("phone"),
                resource_data.get("email"),
                resource_data.get("address"),
                resource_data.get("hours"),
                resource_data.get("description"),
                resource_data.get("region")
            ))
            conn.commit()
            conn.close()
            logger.info(f"✅ Recurso creado: {resource_data.get('name')}")
            return True
        except Exception as e:
            logger.error(f"Error creando recurso: {e}")
            return False

    @staticmethod
    def list_all() -> List[Dict]:
        """Lista todos los recursos."""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM resources ORDER BY name")
            rows = cursor.fetchall()
            conn.close()

            return [{
                "id": row[0],
                "name": row[1],
                "type": row[2],
                "phone": row[3],
                "email": row[4],
                "address": row[5],
                "hours": row[6],
                "description": row[7],
                "region": row[8]
            } for row in rows]
        except Exception as e:
            logger.error(f"Error listando recursos: {e}")
            return []

    @staticmethod
    def filter_by_type(resource_type: str) -> List[Dict]:
        """Filtra recursos por tipo."""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM resources WHERE type = ? ORDER BY name", (resource_type,))
            rows = cursor.fetchall()
            conn.close()

            return [{
                "id": row[0],
                "name": row[1],
                "type": row[2],
                "phone": row[3],
                "email": row[4],
                "address": row[5],
                "hours": row[6],
                "description": row[7],
                "region": row[8]
            } for row in rows]
        except Exception as e:
            logger.error(f"Error filtrando recursos: {e}")
            return []


class AuditDAO:
    """DAO para auditoria."""

    @staticmethod
    def log_action(user_id: int, action: str, table_name: str, record_id: int, details: str = "") -> bool:
        """Registra una accion en el log de auditoria."""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO audit_log (user_id, action, table_name, record_id, details)
                VALUES (?, ?, ?, ?, ?)
            """, (user_id, action, table_name, record_id, details))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Error en auditoria: {e}")
            return False


if __name__ == "__main__":
    # Test
    print("Casos hoy:", CaseDAO.count_today())
    print("Por urgencia:", CaseDAO.count_by_urgency())
