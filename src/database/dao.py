"""
Data Access Objects (DAOs)
Interfaz de acceso a la base de datos
"""

import sqlite3
from datetime import datetime
from typing import List, Optional, Dict, Any
import logging
import json

from .schema import get_connection

logger = logging.getLogger(__name__)


class BaseDAO:
    """Clase base para todos los DAOs."""
    
    def __init__(self):
        self.conn = None
    
    def get_connection(self):
        """Obtiene una conexión a la base de datos."""
        return get_connection()
    
    def execute(self, query: str, params: tuple = ()) -> sqlite3.Cursor:
        """Ejecuta una query."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        return cursor
    
    def fetch_one(self, query: str, params: tuple = ()) -> Optional[Dict]:
        """Obtiene un registro."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.row_factory = sqlite3.Row
        cursor.execute(query, params)
        result = cursor.fetchone()
        conn.close()
        return dict(result) if result else None
    
    def fetch_all(self, query: str, params: tuple = ()) -> List[Dict]:
        """Obtiene todos los registros."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.row_factory = sqlite3.Row
        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()
        return [dict(row) for row in results]


class UserDAO(BaseDAO):
    """DAO para usuarios."""
    
    def create(self, username: str, password_hash: str, role: str = "operator") -> int:
        """Crea un nuevo usuario."""
        cursor = self.execute(
            "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
            (username, password_hash, role)
        )
        return cursor.lastrowid
    
    def get_by_username(self, username: str) -> Optional[Dict]:
        """Obtiene usuario por username."""
        return self.fetch_one(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        )
    
    def get_by_id(self, user_id: int) -> Optional[Dict]:
        """Obtiene usuario por ID."""
        return self.fetch_one(
            "SELECT * FROM users WHERE id = ?",
            (user_id,)
        )
    
    def list_all(self) -> List[Dict]:
        """Lista todos los usuarios."""
        return self.fetch_all("SELECT * FROM users")


class CaseDAO(BaseDAO):
    """DAO para casos."""
    
    def create(self, case_number: str, input_text: str, created_by: int) -> int:
        """Crea un nuevo caso."""
        cursor = self.execute(
            """INSERT INTO cases (case_number, input_text, created_by, status)
               VALUES (?, ?, ?, 'new')""",
            (case_number, input_text, created_by)
        )
        return cursor.lastrowid
    
    def get_by_id(self, case_id: int) -> Optional[Dict]:
        """Obtiene caso por ID."""
        return self.fetch_one(
            "SELECT * FROM cases WHERE id = ?",
            (case_id,)
        )
    
    def update(self, case_id: int, **kwargs) -> bool:
        """Actualiza un caso."""
        allowed_fields = ["summary", "urgency", "case_type", "status"]
        fields = [(k, v) for k, v in kwargs.items() if k in allowed_fields]
        
        if not fields:
            return False
        
        set_clause = ", ".join([f"{k} = ?" for k, _ in fields])
        values = [v for _, v in fields]
        values.append(case_id)
        
        cursor = self.execute(
            f"""UPDATE cases SET {set_clause}, updated_at = CURRENT_TIMESTAMP
               WHERE id = ?""",
            tuple(values)
        )
        return cursor.rowcount > 0
    
    def list_by_status(self, status: str) -> List[Dict]:
        """Lista casos por estado."""
        return self.fetch_all(
            "SELECT * FROM cases WHERE status = ? ORDER BY created_at DESC",
            (status,)
        )
    
    def list_by_urgency(self, urgency: str) -> List[Dict]:
        """Lista casos por urgencia."""
        return self.fetch_all(
            "SELECT * FROM cases WHERE urgency = ? ORDER BY created_at DESC",
            (urgency,)
        )
    
    def list_all(self, limit: int = 100, offset: int = 0) -> List[Dict]:
        """Lista todos los casos con paginación."""
        return self.fetch_all(
            "SELECT * FROM cases ORDER BY created_at DESC LIMIT ? OFFSET ?",
            (limit, offset)
        )


class CaseAnalysisDAO(BaseDAO):
    """DAO para análisis de casos."""
    
    def create(self, case_id: int, emotions: str, risk_factors: str,
               identified_people: str, ai_score: float, analysis_data: str) -> int:
        """Crea análisis de un caso."""
        cursor = self.execute(
            """INSERT INTO case_analysis 
               (case_id, emotions, risk_factors, identified_people, ai_score, analysis_data)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (case_id, emotions, risk_factors, identified_people, ai_score, analysis_data)
        )
        return cursor.lastrowid
    
    def get_by_case_id(self, case_id: int) -> Optional[Dict]:
        """Obtiene análisis de un caso."""
        return self.fetch_one(
            "SELECT * FROM case_analysis WHERE case_id = ? ORDER BY created_at DESC",
            (case_id,)
        )
    
    def get_analysis_data(self, case_id: int) -> Optional[Dict]:
        """Obtiene datos de análisis como JSON."""
        analysis = self.get_by_case_id(case_id)
        if analysis and analysis["analysis_data"]:
            return json.loads(analysis["analysis_data"])
        return None


class ResourceDAO(BaseDAO):
    """DAO para recursos."""
    
    def create(self, name: str, resource_type: str, phone: str = None,
               email: str = None, address: str = None, hours: str = None,
               description: str = None, region: str = None) -> int:
        """Crea un nuevo recurso."""
        cursor = self.execute(
            """INSERT INTO resources 
               (name, type, phone, email, address, hours, description, region)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (name, resource_type, phone, email, address, hours, description, region)
        )
        return cursor.lastrowid
    
    def get_by_id(self, resource_id: int) -> Optional[Dict]:
        """Obtiene recurso por ID."""
        return self.fetch_one(
            "SELECT * FROM resources WHERE id = ?",
            (resource_id,)
        )
    
    def list_by_type(self, resource_type: str) -> List[Dict]:
        """Lista recursos por tipo."""
        return self.fetch_all(
            "SELECT * FROM resources WHERE type = ?",
            (resource_type,)
        )
    
    def list_by_region(self, region: str) -> List[Dict]:
        """Lista recursos por región."""
        return self.fetch_all(
            "SELECT * FROM resources WHERE region = ?",
            (region,)
        )
    
    def search(self, query: str) -> List[Dict]:
        """Busca recursos por nombre o descripción."""
        search_pattern = f"%{query}%"
        return self.fetch_all(
            """SELECT * FROM resources 
               WHERE name LIKE ? OR description LIKE ?
               LIMIT 10""",
            (search_pattern, search_pattern)
        )
    
    def list_all(self) -> List[Dict]:
        """Lista todos los recursos."""
        return self.fetch_all("SELECT * FROM resources ORDER BY name")


class AuditLogDAO(BaseDAO):
    """DAO para auditoría."""
    
    def log(self, user_id: int, action: str, table_name: str = None,
            record_id: int = None, details: str = None) -> int:
        """Registra una acción en auditoría."""
        cursor = self.execute(
            """INSERT INTO audit_log (user_id, action, table_name, record_id, details)
               VALUES (?, ?, ?, ?, ?)""",
            (user_id, action, table_name, record_id, details)
        )
        return cursor.lastrowid
    
    def get_by_user(self, user_id: int, limit: int = 50) -> List[Dict]:
        """Obtiene auditoría de un usuario."""
        return self.fetch_all(
            """SELECT * FROM audit_log WHERE user_id = ?
               ORDER BY timestamp DESC LIMIT ?""",
            (user_id, limit)
        )
    
    def get_by_record(self, table_name: str, record_id: int) -> List[Dict]:
        """Obtiene auditoría de un registro específico."""
        return self.fetch_all(
            """SELECT * FROM audit_log 
               WHERE table_name = ? AND record_id = ?
               ORDER BY timestamp DESC""",
            (table_name, record_id)
        )
    
    def get_all(self, limit: int = 100, offset: int = 0) -> List[Dict]:
        """Lista toda la auditoría con paginación."""
        return self.fetch_all(
            """SELECT * FROM audit_log 
               ORDER BY timestamp DESC LIMIT ? OFFSET ?""",
            (limit, offset)
        )
