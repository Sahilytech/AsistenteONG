"""
Gestor de casos - Auto-generación de IDs, almacenamiento, filtros
Sincronizado con DAO para persistencia real
"""

from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional
from datetime import datetime
import sqlite3
import logging
import uuid
import json

from .database.schema import get_connection, DB_PATH

logger = logging.getLogger(__name__)


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
        """Convierte a diccionario."""
        return asdict(self)

    def to_json(self) -> str:
        """Convierte a JSON."""
        return json.dumps(self.to_dict())


class CaseManager:
    """Gestor de casos con persistencia SQLite."""

    def __init__(self, db_path: str = None):
        """Inicializa gestor de casos."""
        self.db_path = db_path or str(DB_PATH)
        self.counter = 0
        self._init_db()
        logger.info("✅ CaseManager inicializado")

    def _init_db(self):
        """Inicializa base de datos SQLite."""
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
        logger.info("✅ Tabla de casos creada/verificada")

    def generate_case_number(self) -> str:
        """Genera número de caso automático: CASE-202608-00001."""
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
        """Crea un nuevo caso y lo guarda en DB."""
        case_id = str(uuid.uuid4())[:8]
        case_number = self.generate_case_number()
        created_at = datetime.now().isoformat()

        case = Case(
            case_id=case_id,
            case_number=case_number,
            created_at=created_at,
            text=text,
            urgency=urgency,
            keywords=keywords,
            notes="",
            status="nuevo",
            assigned_to="",
            resources_used=[],
            follow_up_date=None
        )

        # Guardar en SQLite
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO cases (case_id, case_number, created_at, text, urgency, keywords, notes, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            case.case_id, case.case_number, case.created_at, case.text,
            case.urgency, json.dumps(case.keywords), case.notes, case.status
        ))
        conn.commit()
        conn.close()

        logger.info(f"✅ Caso guardado: {case_number}")
        return case

    def get_case(self, case_number: str) -> Optional[Case]:
        """Obtiene un caso por número."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cases WHERE case_number = ?", (case_number,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return Case(
                case_id=row[0],
                case_number=row[1],
                created_at=row[2],
                text=row[3],
                urgency=row[4],
                keywords=json.loads(row[5]) if row[5] else [],
                notes=row[6] or "",
                status=row[7] or "nuevo",
                assigned_to=row[8] or "",
                resources_used=json.loads(row[9]) if row[9] else [],
                follow_up_date=row[10]
            )
        return None

    def list_cases(self, limit: int = 100) -> List[Case]:
        """Lista todos los casos."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cases ORDER BY created_at DESC LIMIT ?", (limit,))
        rows = cursor.fetchall()
        conn.close()

        cases = []
        for row in rows:
            cases.append(Case(
                case_id=row[0],
                case_number=row[1],
                created_at=row[2],
                text=row[3],
                urgency=row[4],
                keywords=json.loads(row[5]) if row[5] else [],
                notes=row[6] or "",
                status=row[7] or "nuevo",
                assigned_to=row[8] or "",
                resources_used=json.loads(row[9]) if row[9] else [],
                follow_up_date=row[10]
            ))
        return cases

    def filter_cases(self, urgency: str = None, status: str = None) -> List[Case]:
        """Filtra casos por urgencia y/o estado."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        query = "SELECT * FROM cases WHERE 1=1"
        params = []

        if urgency:
            query += " AND urgency = ?"
            params.append(urgency)
        if status:
            query += " AND status = ?"
            params.append(status)

        query += " ORDER BY created_at DESC"

        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()

        cases = []
        for row in rows:
            cases.append(Case(
                case_id=row[0],
                case_number=row[1],
                created_at=row[2],
                text=row[3],
                urgency=row[4],
                keywords=json.loads(row[5]) if row[5] else [],
                notes=row[6] or "",
                status=row[7] or "nuevo",
                assigned_to=row[8] or "",
                resources_used=json.loads(row[9]) if row[9] else [],
                follow_up_date=row[10]
            ))
        return cases


if __name__ == "__main__":
    manager = CaseManager()
    case = manager.create_case(
        text="Test de caso de prueba",
        urgency="Alta",
        keywords=["violencia", "menores"]
    )
    print(f"Caso creado: {case.case_number}")
