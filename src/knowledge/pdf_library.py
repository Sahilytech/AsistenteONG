"""Biblioteca PDF local: importar, procesar, indexar, consultar, abrir y eliminar."""
from __future__ import annotations
from pathlib import Path
import hashlib,re,shutil
from .memory import LocalMemory
LIBRARY_DIR=Path(__file__).resolve().parents[2]/"data"/"library";MAX_CHARS_PER_PDF=500_000

def _clean(text):
 text=re.sub(r"-\s*\n\s*", "", text or "");text=re.sub(r"\s+"," ",text);return text.strip()
def extract_pdf_text(path):
 from pypdf import PdfReader
 reader=PdfReader(str(path));pages=[];page_chars=[]
 for page in reader.pages:
  try:t=_clean(page.extract_text() or "")
  except Exception:t=""
  pages.append(t);page_chars.append(len(t))
 return _clean(" ".join(pages))[:MAX_CHARS_PER_PDF],len(reader.pages),page_chars

def _fingerprint(path):
 h=hashlib.sha256()
 with open(path,"rb") as f:
  for chunk in iter(lambda:f.read(1024*1024),b""):h.update(chunk)
 return h.hexdigest()[:16]

def import_pdf(path,memory=None,copy_to_library=True):
 path=Path(path)
 if path.suffix.lower()!=".pdf":raise ValueError("El archivo seleccionado no es un PDF.")
 LIBRARY_DIR.mkdir(parents=True,exist_ok=True);target=LIBRARY_DIR/path.name
 if copy_to_library and path.resolve()!=target.resolve():shutil.copy2(path,target)
 else:target=path
 text,pages,page_chars=extract_pdf_text(target);memory=memory or LocalMemory();source=f"file://{target.resolve()}";fingerprint=_fingerprint(target)
 if not text:
  memory.save(source,"archivo local",target.name,f"PDF sin texto extraíble · SHA {fingerprint}","");return {"title":target.name,"chars":0,"pages":pages,"status":"sin_texto","path":str(target),"fingerprint":fingerprint,"chunks":0}
 chunks=memory.save_chunks(source,"archivo local",target.name,text)
 memory.save(source,"archivo local",target.name,f"{pages} páginas · {len(text):,} caracteres · {chunks} fragmentos · SHA {fingerprint}",text)
 return {"title":target.name,"chars":len(text),"pages":pages,"status":"procesado","path":str(target),"fingerprint":fingerprint,"chunks":chunks,"page_chars":page_chars}

def list_pdfs(folder=None):
 folder=Path(folder or LIBRARY_DIR);folder.mkdir(parents=True,exist_ok=True);items=[]
 for path in sorted(folder.glob("*.pdf"),key=lambda p:p.name.lower()):
  try:
   text,pages,page_chars=extract_pdf_text(path);items.append({"title":path.name,"path":str(path),"pages":pages,"chars":len(text),"status":"procesado" if text else "sin_texto","fingerprint":_fingerprint(path),"page_chars":page_chars})
  except Exception as exc:items.append({"title":path.name,"path":str(path),"pages":0,"chars":0,"status":f"error: {exc}"})
 return items

def search_pdfs(query,limit=20):
 rows=LocalMemory().search(query,limit=limit,include_content=True);seen=set();out=[]
 for r in rows:
  if not r.get("domain","").startswith("archivo local") or r.get("title") in seen:continue
  seen.add(r["title"]);out.append(r)
 return out

def delete_pdf(path,memory=None):
 path=Path(path).resolve();memory=memory or LocalMemory();memory.delete_file(path)
 if path.exists() and path.suffix.lower()==".pdf":path.unlink()

def open_pdf(path):
 import os,subprocess,sys
 path=str(Path(path).resolve())
 if sys.platform.startswith("win"):os.startfile(path)
 elif sys.platform=="darwin":subprocess.Popen(["open",path])
 else:subprocess.Popen(["xdg-open",path])

def import_folder(folder=None,memory=None):
 folder=Path(folder or LIBRARY_DIR);folder.mkdir(parents=True,exist_ok=True);imported=0;errors=[]
 for path in sorted(folder.glob("*.pdf")):
  try:import_pdf(path,memory,copy_to_library=False);imported+=1
  except Exception as exc:errors.append(f"{path.name}: {exc}")
 return imported,errors
