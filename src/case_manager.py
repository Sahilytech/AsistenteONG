"""Gestor de casos - almacenamiento local SQLite."""
import sqlite3,json,logging,uuid
from dataclasses import dataclass,field,asdict
from typing import List,Optional,Dict
from datetime import datetime
from pathlib import Path
logger=logging.getLogger(__name__)
DB_PATH=Path(__file__).parent.parent/"data"/"asistente.db"; DB_PATH.parent.mkdir(parents=True,exist_ok=True)
@dataclass
class Case:
    case_id:str; case_number:str; created_at:str; text:str; urgency:str
    keywords:List[str]=field(default_factory=list); notes:str=""; status:str="nuevo"; assigned_to:str=""; resources_used:List[str]=field(default_factory=list); follow_up_date:Optional[str]=None
    person_name:str=""; contact:str=""; case_type:str=""; location:str=""
    social_report:Dict=field(default_factory=dict); combined_analysis:Dict=field(default_factory=dict)
    def to_dict(self): return asdict(self)
class CaseManager:
    def __init__(self,db_path:str=None): self.db_path=db_path or str(DB_PATH); self._init_db(); logger.info("CaseManager inicializado en %s",self.db_path)
    def _init_db(self):
        conn=sqlite3.connect(self.db_path); cur=conn.cursor(); cur.execute("""CREATE TABLE IF NOT EXISTS cases(case_id TEXT PRIMARY KEY,case_number TEXT UNIQUE,created_at TEXT,text TEXT,urgency TEXT,keywords TEXT,notes TEXT,status TEXT,assigned_to TEXT,resources_used TEXT,follow_up_date TEXT)""")
        existing={r[1] for r in cur.execute("PRAGMA table_info(cases)").fetchall()}
        for name in ("person_name","contact","case_type","location","social_report","combined_analysis"):
            if name not in existing: cur.execute(f"ALTER TABLE cases ADD COLUMN {name} TEXT DEFAULT ''")
        conn.commit(); conn.close()
    def generate_case_number(self):
        prefix=datetime.now().strftime("%Y%m"); conn=sqlite3.connect(self.db_path); cur=conn.cursor(); cur.execute("SELECT COUNT(*) FROM cases WHERE case_number LIKE ?",(f"CASE-{prefix}-%",)); count=cur.fetchone()[0]+1; conn.close(); return f"CASE-{prefix}-{count:05d}"
    def create_case(self,text:str,urgency:str,keywords:List[str],metadata:Optional[Dict]=None,analysis:Optional[Dict]=None)->Case:
        metadata=metadata or {}; case=Case(str(uuid.uuid4())[:8],self.generate_case_number(),datetime.now().isoformat(),text,urgency,keywords,person_name=metadata.get("person_name","").strip(),contact=metadata.get("contact","").strip(),case_type=metadata.get("case_type","").strip(),location=metadata.get("location","").strip(),combined_analysis=analysis or {})
        self.save_case(case); logger.info("Caso creado: %s",case.case_number); return case
    def save_case(self,case:Case):
        conn=sqlite3.connect(self.db_path); cur=conn.cursor(); cur.execute("""INSERT OR REPLACE INTO cases VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",(case.case_id,case.case_number,case.created_at,case.text,case.urgency,json.dumps(case.keywords,ensure_ascii=False),case.notes,case.status,case.assigned_to,json.dumps(case.resources_used,ensure_ascii=False),case.follow_up_date,case.person_name,case.contact,case.case_type,case.location,json.dumps(case.social_report,ensure_ascii=False),json.dumps(case.combined_analysis,ensure_ascii=False))); conn.commit(); conn.close()
    def attach_social_report(self,case_number:str,report:Dict,analysis:Optional[Dict]=None):
        case=self.get_case(case_number)
        if not case: raise ValueError(f"No existe el caso {case_number}")
        case.social_report=report or {}; case.combined_analysis=analysis or case.combined_analysis; 
        if analysis:
            case.urgency=analysis.get("urgency",case.urgency); case.keywords=analysis.get("keywords",case.keywords); case.resources_used=analysis.get("suggested_resources",case.resources_used)
        self.save_case(case); return case
    def get_case(self,case_number:str):
        conn=sqlite3.connect(self.db_path); cur=conn.cursor(); cur.execute("SELECT * FROM cases WHERE case_number=?",(case_number,)); row=cur.fetchone(); conn.close(); return self._row_to_case(row) if row else None
    def get_all_cases(self):
        conn=sqlite3.connect(self.db_path); cur=conn.cursor(); cur.execute("SELECT * FROM cases ORDER BY created_at DESC"); rows=cur.fetchall(); conn.close(); return [self._row_to_case(r) for r in rows]
    def get_statistics(self):
        cases=self.get_all_cases(); return {"total":len(cases),"por_urgencia":self._counts(cases,"urgency"),"por_status":self._counts(cases,"status")}
    @staticmethod
    def _counts(cases,attr):
        result={}
        for c in cases:
            value=getattr(c,attr); result[value]=result.get(value,0)+1
        return result
    @staticmethod
    def _json(value,default):
        try:return json.loads(value or "") if value else default
        except (TypeError,json.JSONDecodeError):return default
    @staticmethod
    def _row_to_case(row):
        return Case(case_id=row[0],case_number=row[1],created_at=row[2],text=row[3],urgency=row[4],keywords=CaseManager._json(row[5],[]),notes=row[6],status=row[7],assigned_to=row[8],resources_used=CaseManager._json(row[9],[]),follow_up_date=row[10],person_name=row[11] or "",contact=row[12] or "",case_type=row[13] or "",location=row[14] or "",social_report=CaseManager._json(row[15],{} ) if len(row)>15 else {},combined_analysis=CaseManager._json(row[16],{}) if len(row)>16 else {})
