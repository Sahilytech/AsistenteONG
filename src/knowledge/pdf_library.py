"""Biblioteca PDF local: importar, procesar, indexar, consultar, abrir y eliminar."""
from __future__ import annotations
from pathlib import Path
import hashlib,os,re,shutil
from .memory import LocalMemory
LIBRARY_DIR=Path(__file__).resolve().parents[2]/"data"/"library"
MAX_CHARS_PER_PDF=500_000

def _clean(text):
 text=re.sub(r"-\s*\n\s*","",text or "");text=re.sub(r"\s+"," ",text);return text.strip()

def _ocr_pdf(path,max_pages=30):
 """OCR opcional para PDFs escaneados. Requiere PyMuPDF + pytesseract + Tesseract instalado."""
 try: import fitz,pytesseract
 except ImportError:return [],0,"ocr_no_disponible"
 try:
  doc=fitz.open(str(path));pages=[]
  for i,page in enumerate(doc):
   if i>=max_pages:break
   pix=page.get_pixmap(matrix=fitz.Matrix(1.6,1.6),alpha=False)
   from PIL import Image
   import io
   image=Image.open(io.BytesIO(pix.tobytes("png")))
   pages.append(_clean(pytesseract.image_to_string(image,lang="spa+eng")))
  return pages,len(doc),"ocr"
 except Exception:return [],0,"ocr_error"

def extract_pdf_pages(path,allow_ocr=True):
 from pypdf import PdfReader
 reader=PdfReader(str(path));pages=[]
 for number,page in enumerate(reader.pages,1):
  try:text=_clean(page.extract_text() or "")
  except Exception:text=""
  pages.append({"page":number,"text":text,"chars":len(text),"mode":"texto"})
 if any(p["text"] for p in pages): return pages,len(reader.pages),"texto"
 if allow_ocr and os.getenv("ASISTENTE_OCR","0").casefold() in {"1","true","yes","si"}:
  ocr,pcount,state=_ocr_pdf(path)
  if ocr:
   return [{"page":i+1,"text":t,"chars":len(t),"mode":state} for i,t in enumerate(ocr)],pcount or len(reader.pages),state
 return pages,len(reader.pages),"sin_texto"

def extract_pdf_text(path,allow_ocr=True):
 pages,total,mode=extract_pdf_pages(path,allow_ocr)
 text=_clean(" ".join(p["text"] for p in pages))[:MAX_CHARS_PER_PDF]
 return text,total,[p["chars"] for p in pages],mode

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
 pages,total,mode=extract_pdf_pages(target,allow_ocr=True)
 text=_clean(" ".join(p["text"] for p in pages))[:MAX_CHARS_PER_PDF]
 memory=memory or LocalMemory();source=f"file://{target.resolve()}";fingerprint=_fingerprint(target)
 if not text:
  memory.save(source,"archivo local",target.name,f"PDF sin texto extraíble · SHA {fingerprint}","")
  return {"title":target.name,"chars":0,"pages":total,"status":"sin_texto","path":str(target),"fingerprint":fingerprint,"chunks":0,"extraction":mode,"page_data":pages}
 chunks=memory.save_chunks(source,"archivo local",target.name,text)
 # Page-level evidence is kept independently so retrieval can point to the source page.
 memory.delete_pages(source)
 for p in pages:
  if p["text"]:
   memory.save_page(source,p["page"],target.name,p["text"],p["mode"])
 memory.save(source,"archivo local",target.name,f"{total} páginas · {len(text):,} caracteres · {chunks} fragmentos · extracción: {mode} · SHA {fingerprint}",text)
 return {"title":target.name,"chars":len(text),"pages":total,"status":"procesado","path":str(target),"fingerprint":fingerprint,"chunks":chunks,"page_chars":[p["chars"] for p in pages],"extraction":mode,"page_data":pages}

def list_pdfs(folder=None):
 folder=Path(folder or LIBRARY_DIR);folder.mkdir(parents=True,exist_ok=True);items=[]
 for path in sorted(folder.glob("*.pdf"),key=lambda p:p.name.lower()):
  try:
   text,pages,page_chars,mode=extract_pdf_text(path,allow_ocr=False);items.append({"title":path.name,"path":str(path),"pages":pages,"chars":len(text),"status":"procesado" if text else "sin_texto","fingerprint":_fingerprint(path),"page_chars":page_chars,"extraction":mode})
  except Exception as exc:items.append({"title":path.name,"path":str(path),"pages":0,"chars":0,"status":f"error: {exc}"})
 return items

def search_pdfs(query,limit=20):
 from .smart_retriever import retrieve
 return [r for r in retrieve(query,limit=limit) if r.get("domain","").startswith("archivo local")]

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
