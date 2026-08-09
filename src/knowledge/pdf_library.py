"""Biblioteca PDF local: importar, procesar, consultar, abrir y eliminar."""
from __future__ import annotations
from pathlib import Path
import re
import shutil
from .memory import LocalMemory

LIBRARY_DIR = Path(__file__).resolve().parents[2] / "data" / "library"
MAX_CHARS_PER_PDF = 180_000

def _clean(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()

def extract_pdf_text(path: str | Path) -> tuple[str, int]:
    from pypdf import PdfReader
    reader = PdfReader(str(path))
    pages = []
    for page in reader.pages:
        try: pages.append(page.extract_text() or "")
        except Exception: pages.append("")
    return _clean("\n".join(pages))[:MAX_CHARS_PER_PDF], len(reader.pages)

def import_pdf(path: str | Path, memory: LocalMemory | None = None, copy_to_library: bool = True) -> dict:
    path = Path(path)
    if path.suffix.lower() != ".pdf": raise ValueError("El archivo seleccionado no es un PDF.")
    LIBRARY_DIR.mkdir(parents=True, exist_ok=True)
    target = LIBRARY_DIR / path.name
    if copy_to_library and path.resolve() != target.resolve():
        shutil.copy2(path, target)
    else: target = path
    text, pages = extract_pdf_text(target)
    memory = memory or LocalMemory()
    source = f"file://{target.resolve()}"
    if not text:
        memory.save(source, "archivo local", target.name, "PDF sin texto extraíble", "")
        return {"title": target.name, "chars": 0, "pages": pages, "status": "sin_texto", "path": str(target)}
    memory.save(source, "archivo local", target.name, text[:700], text)
    return {"title": target.name, "chars": len(text), "pages": pages, "status": "procesado", "path": str(target)}

def list_pdfs(folder: str | Path | None = None) -> list[dict]:
    folder = Path(folder or LIBRARY_DIR); folder.mkdir(parents=True, exist_ok=True)
    memory = LocalMemory(); items=[]
    for path in sorted(folder.glob("*.pdf"), key=lambda p:p.name.lower()):
        try:
            text,pages=extract_pdf_text(path)
            items.append({"title":path.name,"path":str(path),"pages":pages,"chars":len(text),"status":"procesado" if text else "sin_texto"})
        except Exception as exc:
            items.append({"title":path.name,"path":str(path),"pages":0,"chars":0,"status":f"error: {exc}"})
    return items

def search_pdfs(query: str, limit: int = 20) -> list[dict]:
    query=query.strip()
    if not query:return []
    memory=LocalMemory(); rows=memory.search(query,limit=limit)
    return [r for r in rows if r.get("domain")=="archivo local"]

def delete_pdf(path: str | Path, memory: LocalMemory | None = None) -> None:
    path=Path(path).resolve(); memory=memory or LocalMemory()
    memory.delete_file(path)
    if path.exists() and path.suffix.lower()==".pdf": path.unlink()

def open_pdf(path: str | Path) -> None:
    import os, subprocess, sys
    path=str(Path(path).resolve())
    if sys.platform.startswith("win"): os.startfile(path)
    elif sys.platform == "darwin": subprocess.Popen(["open",path])
    else: subprocess.Popen(["xdg-open",path])

def import_folder(folder: str | Path | None = None, memory: LocalMemory | None = None) -> tuple[int,list[str]]:
    folder=Path(folder or LIBRARY_DIR); folder.mkdir(parents=True,exist_ok=True); imported=0; errors=[]
    for path in sorted(folder.glob("*.pdf")):
        try: import_pdf(path,memory,copy_to_library=False); imported+=1
        except Exception as exc: errors.append(f"{path.name}: {exc}")
    return imported,errors
