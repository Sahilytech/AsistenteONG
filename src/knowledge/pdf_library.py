"""Importador local de PDFs para la biblioteca de conocimiento.

No envía documentos a Internet. Extrae texto de PDFs digitales y los guarda
como fuentes locales para búsquedas y contexto del análisis.
"""
from __future__ import annotations
from pathlib import Path
import re

from .memory import LocalMemory

LIBRARY_DIR = Path(__file__).resolve().parents[2] / "data" / "library"
MAX_CHARS_PER_PDF = 180_000


def _clean(text: str) -> str:
    text = re.sub(r"\s+", " ", text or "").strip()
    return text


def extract_pdf_text(path: str | Path) -> str:
    """Extrae texto de un PDF digital usando pypdf."""
    from pypdf import PdfReader
    reader = PdfReader(str(path))
    pages = []
    for page in reader.pages:
        try:
            pages.append(page.extract_text() or "")
        except Exception:
            pages.append("")
    return _clean("\n".join(pages))[:MAX_CHARS_PER_PDF]


def import_pdf(path: str | Path, memory: LocalMemory | None = None) -> dict:
    path = Path(path)
    if path.suffix.lower() != ".pdf":
        raise ValueError("El archivo seleccionado no es un PDF.")
    memory = memory or LocalMemory()
    text = extract_pdf_text(path)
    if not text:
        raise ValueError("El PDF no contiene texto extraíble. Si es un escaneo, primero aplicá OCR.")
    memory.save(
        source_url=f"file://{path.resolve()}",
        domain="archivo local",
        title=path.name,
        snippet=text[:700],
        content=text,
    )
    return {"title": path.name, "chars": len(text), "pages": ""}


def import_folder(folder: str | Path | None = None, memory: LocalMemory | None = None) -> tuple[int, list[str]]:
    folder = Path(folder or LIBRARY_DIR)
    folder.mkdir(parents=True, exist_ok=True)
    memory = memory or LocalMemory()
    imported = 0
    errors: list[str] = []
    for path in sorted(folder.glob("*.pdf")):
        try:
            import_pdf(path, memory)
            imported += 1
        except Exception as exc:
            errors.append(f"{path.name}: {exc}")
    return imported, errors
