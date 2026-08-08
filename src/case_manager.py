"""
Gestor de casos - Auto-generación de IDs, almacenamiento, filtros
"""

from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional
from datetime import datetime
import sqlite3
import logging
import uuid
import json

logger = logging.getLogger(__name__)


@dataclass
class Case:
    """Modelo de caso."""
    
    case_id: str  # Auto-generado
    case_number: str  # Formato: CASE-YYYYMM-XXXXX
    created_at: str
    text: str
    urgency: str
    keywords: List[str] = field(default_factory=list)
    notes: str = ""
    status: str = "nuevo"  # nuevo, en_progreso, resuelto
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
    """Gestor de casos con persistencia."""
    
    def __init__(self, db_path: str = "cases.db"):
        """Inicializa gestor de casos."""
        self.db_path = db_path
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
        
        # Obtener contador de casos este mes
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
        """Crea un nuevo caso."""
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
        """Guarda caso en base de datos."""
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
    
    def get_case(self, case_id: str) -> Optional[Case]:
        """Obtiene caso por ID."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM cases WHERE case_id = ?", (case_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return self._row_to_case(row)
        return None
    
    def get_all_cases(self) -> List[Case]:
        """Obtiene todos los casos."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM cases ORDER BY created_at DESC")
        rows = cursor.fetchall()
        conn.close()
        
        return [self._row_to_case(row) for row in rows]
    
    def filter_cases(self, **filters) -> List[Case]:
        """Filtra casos por criterios."""
        cases = self.get_all_cases()
        
        # Filtrar por urgencia
        if "urgency" in filters and filters["urgency"]:
            cases = [c for c in cases if c.urgency == filters["urgency"]]
        
        # Filtrar por status
        if "status" in filters and filters["status"]:
            cases = [c for c in cases if c.status == filters["status"]]
        
        # Filtrar por mes
        if "month" in filters and filters["month"]:
            cases = [c for c in cases if c.case_number.split("-")[1] == filters["month"]]
        
        # Ordenar
        order_by = filters.get("order_by", "created_at")
        reverse = filters.get("reverse", True)
        
        if order_by == "urgency":
            urgency_order = {"Muy Alta": 0, "Alta": 1, "Media": 2, "Baja": 3}
            cases.sort(key=lambda c: urgency_order.get(c.urgency, 4), reverse=reverse)
        elif order_by == "created_at":
            cases.sort(key=lambda c: c.created_at, reverse=reverse)
        elif order_by == "case_number":
            cases.sort(key=lambda c: c.case_number, reverse=reverse)
        
        return cases
    
    def update_case_status(self, case_id: str, status: str):
        """Actualiza estado de caso."""
        case = self.get_case(case_id)
        if case:
            case.status = status
            self.save_case(case)
            logger.info(f"✅ Caso {case.case_number} actualizado a: {status}")
    
    def update_case_notes(self, case_id: str, notes: str):
        """Actualiza notas de caso."""
        case = self.get_case(case_id)
        if case:
            case.notes = notes
            self.save_case(case)
    
    def export_cases_json(self, filename: str = "casos_exportados.json"):
        """Exporta casos a JSON."""
        cases = self.get_all_cases()
        with open(filename, "w", encoding="utf-8") as f:
            json.dump([c.to_dict() for c in cases], f, ensure_ascii=False, indent=2)
        logger.info(f"✅ Casos exportados a {filename}")
    
    def export_cases_csv(self, filename: str = "casos_exportados.csv"):
        """Exporta casos a CSV."""
        import csv
        cases = self.get_all_cases()
        
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=[
                "case_number", "created_at", "urgency", "status", "keywords"
            ])
            writer.writeheader()
            for case in cases:
                writer.writerow({
                    "case_number": case.case_number,
                    "created_at": case.created_at,
                    "urgency": case.urgency,
                    "status": case.status,
                    "keywords": ", ".join(case.keywords)
                })
        logger.info(f"✅ Casos exportados a {filename}")
    
    def get_statistics(self) -> dict:
        """Obtiene estadísticas de casos."""
        cases = self.get_all_cases()
        
        stats = {
            "total": len(cases),
            "por_urgencia": {},
            "por_status": {},
            "hoy": 0,
            "esta_semana": 0
        }
        
        for case in cases:
            # Por urgencia
            stats["por_urgencia"][case.urgency] = stats["por_urgencia"].get(case.urgency, 0) + 1
            
            # Por status
            stats["por_status"][case.status] = stats["por_status"].get(case.status, 0) + 1
        
        return stats
    
    @staticmethod
    def _row_to_case(row) -> Case:
        """Convierte fila de BD a Case."""
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
