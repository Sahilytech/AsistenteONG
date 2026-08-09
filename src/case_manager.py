"""Gestor de casos - cada persona puede tener múltiples casos sin duplicar su registro."""
import sqlite3,json,logging,uuid
from dataclasses import dataclass,field,asdict
from typing import List,Optional,Dict
from datetime import datetime
from pathlib import Path
from src.core.case_profile import build_case_profile
from src.core.reasoning import analyze_profile
logger=logging.getLogger(__name__);DB_PATH=Path(__file__).parent.parent/"data"/"asistente.db";DB_PATH.parent.mkdir(parents=True,exist_ok=True)
@dataclass
class Case:
 case_id:str;case_number:str;created_at:str;text:str;urgency:str;keywords:List[str]=field(default_factory=list);notes:str="";status:str="nuevo";assigned_to:str="";resources_used:List[str]=field(default_factory=list);follow_up_date:Optional[str]=None;person_name:str="";contact:str="";case_type:str="";location:str="";social_report:Dict=field(default_factory=dict);combined_analysis:Dict=field(default_factory=dict);timeline:List[Dict]=field(default_factory=list);referrals:List[Dict]=field(default_factory=list);person_id:str=""
 def to_dict(self):return asdict(self)
class CaseManager:
 def __init__(self,db_path=None):self.db_path=db_path or str(DB_PATH);self._init_db();logger.info("CaseManager inicializado en %s",self.db_path)
 def _init_db(self):
  with sqlite3.connect(self.db_path) as conn:
   conn.execute("CREATE TABLE IF NOT EXISTS cases(case_id TEXT PRIMARY KEY,case_number TEXT UNIQUE,created_at TEXT,text TEXT,urgency TEXT,keywords TEXT,notes TEXT,status TEXT,assigned_to TEXT,resources_used TEXT,follow_up_date TEXT,person_name TEXT,contact TEXT,case_type TEXT,location TEXT,social_report TEXT,combined_analysis TEXT,timeline TEXT,referrals TEXT)")
   existing={r[1] for r in conn.execute("PRAGMA table_info(cases)")};adds={"person_name":"TEXT DEFAULT ''","contact":"TEXT DEFAULT ''","case_type":"TEXT DEFAULT ''","location":"TEXT DEFAULT ''","social_report":"TEXT DEFAULT '{}'","combined_analysis":"TEXT DEFAULT '{}'","timeline":"TEXT DEFAULT '[]'","referrals":"TEXT DEFAULT '[]'","person_id":"TEXT DEFAULT ''"}
   for n,d in adds.items():
    if n not in existing:conn.execute(f"ALTER TABLE cases ADD COLUMN {n} {d}")
 def generate_case_number(self):
  prefix=datetime.now().strftime("%Y%m")
  with sqlite3.connect(self.db_path) as conn:count=conn.execute("SELECT COUNT(*) FROM cases WHERE case_number LIKE ?",(f"CASE-{prefix}-%",)).fetchone()[0]+1
  return f"CASE-{prefix}-{count:05d}"
 def create_case(self,text,urgency="no determinada",keywords=None,metadata=None,analysis=None)->Case:
  metadata=metadata or {};profile=build_case_profile(text,metadata);brain=analysis or analyze_profile(profile);detected=keywords or sorted(set(profile.indicators+profile.relationships+profile.contexts));person_id=metadata.get("person_id","")
  case=Case(str(uuid.uuid4())[:8],self.generate_case_number(),datetime.now().isoformat(),text,brain.get("urgency",urgency),detected,person_name=metadata.get("person_name","").strip(),contact=metadata.get("contact","").strip(),case_type=metadata.get("case_type","").strip(),location=metadata.get("location","").strip(),combined_analysis={**brain,"profile":profile.to_dict()},person_id=person_id)
  case.timeline.append({"event_type":"caso","title":"Caso creado","description":"Registro inicial del caso","created_at":datetime.now().isoformat(timespec="seconds"),"actor":"","status":"registrado"});self.save_case(case);return case
 def save_case(self,case):
  with sqlite3.connect(self.db_path) as conn:conn.execute("INSERT OR REPLACE INTO cases VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(case.case_id,case.case_number,case.created_at,case.text,case.urgency,json.dumps(case.keywords,ensure_ascii=False),case.notes,case.status,case.assigned_to,json.dumps(case.resources_used,ensure_ascii=False),case.follow_up_date,case.person_name,case.contact,case.case_type,case.location,json.dumps(case.social_report,ensure_ascii=False),json.dumps(case.combined_analysis,ensure_ascii=False),json.dumps(case.timeline,ensure_ascii=False),json.dumps(case.referrals,ensure_ascii=False),case.person_id))
 def attach_social_report(self,case_number,report,analysis=None):
  case=self.get_case(case_number)
  if not case:raise ValueError(f"No existe el caso {case_number}")
  case.social_report=report or {}
  if analysis:case.combined_analysis=analysis;case.urgency=analysis.get("urgency",case.urgency);case.keywords=analysis.get("keywords",case.keywords);case.resources_used=analysis.get("suggested_resources",case.resources_used)
  case.timeline.append({"event_type":"informe","title":"Informe social actualizado","description":"El informe fue asociado al análisis integral","created_at":datetime.now().isoformat(timespec="seconds"),"actor":"","status":"registrado"});self.save_case(case);return case
 def add_timeline_event(self,case_number,event_type,title,description="",actor=""):
  case=self.get_case(case_number)
  if not case:raise ValueError(f"No existe el caso {case_number}")
  case.timeline.append({"event_type":event_type,"title":title,"description":description,"created_at":datetime.now().isoformat(timespec="seconds"),"actor":actor,"status":"registrado"});self.save_case(case);return case
 def add_referral(self,case_number,referral):
  case=self.get_case(case_number)
  if not case:raise ValueError(f"No existe el caso {case_number}")
  item=dict(referral);item.setdefault("status","pendiente");item.setdefault("created_at",datetime.now().isoformat(timespec="seconds"));case.referrals.append(item);self.save_case(case);return case
 def get_case(self,case_number):
  with sqlite3.connect(self.db_path) as conn:row=conn.execute("SELECT * FROM cases WHERE case_number=?",(case_number,)).fetchone()
  return self._row_to_case(row) if row else None
 def get_all_cases(self):
  with sqlite3.connect(self.db_path) as conn:rows=conn.execute("SELECT * FROM cases ORDER BY created_at DESC").fetchall()
  return [self._row_to_case(r) for r in rows]
 def get_statistics(self):
  cases=self.get_all_cases();return {"total":len(cases),"por_urgencia":self._counts(cases,"urgency"),"por_status":self._counts(cases,"status")}
 @staticmethod
 def _counts(cases,attr):
  result={}
  for c in cases:result[getattr(c,attr)]=result.get(getattr(c,attr),0)+1
  return result
 @staticmethod
 def _json(value,default):
  try:return json.loads(value or "") if value else default
  except (TypeError,json.JSONDecodeError):return default
 @classmethod
 def _row_to_case(cls,row):
  return Case(case_id=row[0],case_number=row[1],created_at=row[2],text=row[3],urgency=row[4],keywords=cls._json(row[5],[]),notes=row[6],status=row[7],assigned_to=row[8],resources_used=cls._json(row[9],[]),follow_up_date=row[10],person_name=row[11] or "",contact=row[12] or "",case_type=row[13] or "",location=row[14] or "",social_report=cls._json(row[15],{}),combined_analysis=cls._json(row[16],{}),timeline=cls._json(row[17],[]),referrals=cls._json(row[18],[]),person_id=row[19] or "")
