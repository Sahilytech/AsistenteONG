"""Memoria local SQLite para fuentes, documentos, páginas y fragmentos recuperables."""
from __future__ import annotations
import re, sqlite3
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
DB_PATH=Path(__file__).resolve().parents[2]/"data"/"asistente.db"
class LocalMemory:
 def __init__(self,db_path=None):self.db_path=str(db_path or DB_PATH);Path(self.db_path).parent.mkdir(parents=True,exist_ok=True);self._init()
 @contextmanager
 def _connect(self):
  db=sqlite3.connect(self.db_path)
  try:yield db;db.commit()
  finally:db.close()
 def _init(self):
  with self._connect() as db:
   db.execute("CREATE TABLE IF NOT EXISTS knowledge_memory(id INTEGER PRIMARY KEY AUTOINCREMENT,source_url TEXT UNIQUE,domain TEXT,title TEXT,snippet TEXT,content TEXT,saved_at TEXT)")
   db.execute("CREATE INDEX IF NOT EXISTS idx_knowledge_domain ON knowledge_memory(domain)")
   db.execute("CREATE TABLE IF NOT EXISTS knowledge_pages(id INTEGER PRIMARY KEY AUTOINCREMENT,source_url TEXT,page_number INTEGER,title TEXT,content TEXT,mode TEXT,saved_at TEXT,UNIQUE(source_url,page_number))")
   db.execute("CREATE INDEX IF NOT EXISTS idx_knowledge_pages_source ON knowledge_pages(source_url)")
 def save(self,source_url,domain,title,snippet,content=""):
  with self._connect() as db:db.execute("INSERT INTO knowledge_memory(source_url,domain,title,snippet,content,saved_at) VALUES(?,?,?,?,?,?) ON CONFLICT(source_url) DO UPDATE SET domain=excluded.domain,title=excluded.title,snippet=excluded.snippet,content=excluded.content,saved_at=excluded.saved_at",(source_url,domain,title,snippet,content,datetime.now().isoformat(timespec="seconds")))
 def save_chunks(self,source_url,domain,title,content,chunk_size=1800,overlap=250):
  text=re.sub(r"\s+"," ",content or "").strip()
  if not text:return 0
  self.save(source_url,domain,title,text[:1800],text);chunks=[];start=0
  while start<len(text):
   end=min(len(text),start+chunk_size);chunk=text[start:end]
   if end<len(text):
    cut=max(chunk.rfind(". "),chunk.rfind("; "),chunk.rfind(" "))
    if cut>chunk_size//2:end=start+cut+1;chunk=text[start:end]
   chunks.append(chunk);start=end-overlap if end<len(text) else len(text)
  with self._connect() as db:
   db.execute("DELETE FROM knowledge_memory WHERE domain='archivo local · fragmento' AND title=?",(title,));now=datetime.now().isoformat(timespec="seconds")
   for i,chunk in enumerate(chunks,1):
    db.execute("INSERT INTO knowledge_memory(source_url,domain,title,snippet,content,saved_at) VALUES(?,?,?,?,?,?) ON CONFLICT(source_url) DO UPDATE SET snippet=excluded.snippet,content=excluded.content,saved_at=excluded.saved_at",(f"{source_url}#chunk={i}","archivo local · fragmento",title,f"Fragmento {i} · {len(chunk)} caracteres",chunk,now))
  return len(chunks)
 def save_page(self,source_url,page_number,title,content,mode="texto"):
  with self._connect() as db:db.execute("INSERT INTO knowledge_pages(source_url,page_number,title,content,mode,saved_at) VALUES(?,?,?,?,?,?) ON CONFLICT(source_url,page_number) DO UPDATE SET title=excluded.title,content=excluded.content,mode=excluded.mode,saved_at=excluded.saved_at",(source_url,page_number,title,content,mode,datetime.now().isoformat(timespec="seconds")))
 def delete_pages(self,source_url):
  with self._connect() as db:db.execute("DELETE FROM knowledge_pages WHERE source_url=?",(source_url,))
 def page_evidence(self,source_url,query="",limit=8):
  terms=[t.casefold() for t in re.findall(r"[\wáéíóúüñ]{3,}",query or "")]
  with self._connect() as db:rows=db.execute("SELECT page_number,title,content,mode FROM knowledge_pages WHERE source_url=? ORDER BY page_number",(source_url,)).fetchall()
  out=[]
  for page,title,content,mode in rows:
   matches=[t for t in terms if t in (content or "").casefold()]
   if not terms or matches:out.append({"page":page,"title":title,"content":content,"mode":mode,"matched_terms":sorted(set(matches))})
  return out[:limit]
 def search(self,query,limit=8,include_content=False,domain=None):
  terms=[t.strip().casefold() for t in re.findall(r"[\wáéíóúüñ]{3,}",query or "")]
  if not terms:return []
  clauses=[];args=[]
  for term in terms:
   like=f"%{term}%";clauses.append("(lower(title) LIKE ? OR lower(snippet) LIKE ? OR lower(content) LIKE ?)");args.extend([like,like,like])
  sql=f"SELECT source_url,domain,title,snippet,content,saved_at FROM knowledge_memory WHERE ({' OR '.join(clauses)})"
  if domain:sql+=" AND domain=?";args.append(domain)
  sql+=" ORDER BY saved_at DESC LIMIT ?";args.append(limit)
  with self._connect() as db:rows=db.execute(sql,args).fetchall()
  keys=("url","domain","title","snippet","content","saved_at")
  return [dict(zip(keys,r if include_content else (r[0],r[1],r[2],r[3],r[5]))) for r in rows]
 def delete_file(self,path):
  raw=str(path).replace("\\","/");resolved=str(Path(path).resolve()).replace("\\","/");candidates={f"file://{raw}",f"file://{resolved}",f"file:///{raw.lstrip('/')}",f"file:///{resolved.lstrip('/')}"}
  with self._connect() as db:
   for base in candidates:
    db.execute("DELETE FROM knowledge_memory WHERE source_url=? OR source_url LIKE ?",(base,base+"#chunk=%"));db.execute("DELETE FROM knowledge_pages WHERE source_url=?",(base,))
 def get_document(self,path):
  resolved=str(Path(path).resolve()).replace("\\","/")
  with self._connect() as db:return db.execute("SELECT source_url,domain,title,snippet,content,saved_at FROM knowledge_memory WHERE source_url IN (?,?)",(f"file://{resolved}",f"file:///{resolved.lstrip('/')}" )).fetchone()
 def clear_library(self):
  with self._connect() as db:
   db.execute("DELETE FROM knowledge_memory WHERE domain LIKE 'archivo local%'");db.execute("DELETE FROM knowledge_pages WHERE source_url LIKE 'file://%'")
 def count(self):
  with self._connect() as db:return db.execute("SELECT COUNT(*) FROM knowledge_memory WHERE domain='archivo local'").fetchone()[0]
