"""
Gestor de casos - Almacenamiento local SQLite
"""

import sqlite3
import json
import logging
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional
from datetime import datetime
import uuid
from pathlib import Path

logger = logging.getLogger(__name__)

# Path a base de datos
DB_PATH = Path(__file__).parent.parent / "data" / "asistente.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)


@dataclass
class Case:
    """Modelo de caso."""
    
    case_id: str
    case_number: str
    created_at: str
    text: str
    urgency: str
    keywords: List[str] = field(default_factory=list)
    notes: str = ""
    status: str = "nuevo"
    assigned_to: str = ""
    resources_used: List[str] = field(default_factory=list)
    follow_up_date: Optional[str] = None
    
    def to_dict(self) -> dict:
        return asdict(self)


class CaseManager:
    """Gestor de casos."""
    
    def __init__(self, db_path: str = None):
        self.db_path = db_path or str(DB_PATH)
        self._init_db()
        logger.info(f"✅ CaseManager inicializado en {self.db_path}")
    
    def _init_db(self):
        """Inicializa BD."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cases (
                case_id TEXT PRIMARY KEY,
                case_number TEXT UNIQUE,
                created_at TEXT,
                text TEXT,
                urgency TEXT,
                keywords TEXT,
                notes TEXT,
                status TEXT,
                assigned_to TEXT,
                resources_used TEXT,
                follow_up_date TEXT
            )
        """)
        
        conn.commit()
        conn.close()
    
    def generate_case_number(self) -> str:
        """Genera número automático."""
        now = datetime.now()
        year_month = now.strftime("%Y%m")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM cases WHERE case_number LIKE ?",
            (f"CASE-{year_month}-%",)
        )
        count = cursor.fetchone()[0] + 1
        conn.close()
        
        return f"CASE-{year_month}-{count:05d}"
    
    def create_case(self, text: str, urgency: str, keywords: List[str]) -> Case:
        """Crea caso."""
        case_id = str(uuid.uuid4())[:8]
        case_number = self.generate_case_number()
        created_at = datetime.now().isoformat()
        
        case = Case(
            case_id=case_id,
            case_number=case_number,
            created_at=created_at,
            text=text,
            urgency=urgency,
            keywords=keywords
        )
        
        self.save_case(case)
        logger.info(f"✅ Caso creado: {case_number}")
        return case
    
    def save_case(self, case: Case):
        """Guarda caso."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO cases VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            case.case_id,
            case.case_number,
            case.created_at,
            case.text,
            case.urgency,
            json.dumps(case.keywords),
            case.notes,
            case.status,
            case.assigned_to,
            json.dumps(case.resources_used),
            case.follow_up_date
        ))
        
        conn.commit()
        conn.close()
    
    def get_all_cases(self) -> List[Case]:
        """Obtiene todos los casos."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM cases ORDER BY created_at DESC")
        rows = cursor.fetchall()
        conn.close()
        
        return [self._row_to_case(row) for row in rows]
    
    def get_statistics(self) -> dict:
        """Obtiene estadísticas."""
        cases = self.get_all_cases()
        
        stats = {
            "total": len(cases),
            "por_urgencia": {},
            "por_status": {}
        }
        
        for case in cases:
            stats["por_urgencia"][case.urgency] = stats["por_urgencia"].get(case.urgency, 0) + 1
            stats["por_status"][case.status] = stats["por_status"].get(case.status, 0) + 1
        
        return stats
    
    @staticmethod
    def _row_to_case(row) -> Case:
        """Convierte fila a Case."""
        return Case(
            case_id=row[0],
            case_number=row[1],
            created_at=row[2],
            text=row[3],
            urgency=row[4],
            keywords=json.loads(row[5]),
            notes=row[6],
            status=row[7],
            assigned_to=row[8],
            resources_used=json.loads(row[9]),
            follow_up_date=row[10]
        )
