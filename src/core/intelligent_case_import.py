"""Extracción asistida de candidatos a personas y casos desde documentos.

La extracción es una PREVISUALIZACIÓN: nunca crea personas ni casos por sí sola.
"""
from __future__ import annotations
import re
from typing import Any


def _clean(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def extract_case_candidates(text: str) -> dict[str, Any]:
    """Detecta bloques que parecen pertenecer a una ficha/caso sin decidir su contenido."""
    text = _clean(text)
    if not text:
        return {"people": [], "cases": [], "signals": [], "requires_review": True}

    labels = {
        "name": r"(?:nombre|persona|beneficiari[oa])\s*[:\-]\s*([^|;]+)",
        "birth_date": r"(?:fecha\s+de\s+nacimiento|nacimiento)\s*[:\-]\s*([^|;]+)",
        "case_date": r"(?:fecha\s+del\s+caso|fecha\s+de\s+atenci[oó]n|fecha)\s*[:\-]\s*([^|;]+)",
    }
    person: dict[str, str] = {}
    for field, pattern in labels.items():
        match = re.search(pattern, text, re.I)
        if match:
            person[field] = _clean(match.group(1))

    signals = []
    for term in ("despido", "violencia", "vivienda", "salud", "documentación", "alimentos"):
        if re.search(rf"\b{re.escape(term)}\b", text, re.I):
            signals.append(term)

    case = {
        "date": person.pop("case_date", None),
        "summary": text[:1200],
        "signals": signals,
        "source": "documento_importado",
    }
    people = [person] if person.get("name") else []
    return {
        "people": people,
        "cases": [case] if people else [],
        "signals": signals,
        "requires_review": True,
        "persisted": False,
        "decision": None,
    }


def build_import_review(preview: dict[str, Any]) -> dict[str, Any]:
    """Convierte una previsualización PDF/XLSX/CSV en una bandeja revisable."""
    if preview.get("type") == "pdf":
        result = extract_case_candidates(preview.get("text", ""))
    else:
        rows = preview.get("rows", [])
        result = {"people": rows, "cases": [], "signals": [], "requires_review": True}
    return {
        "filename": preview.get("filename"),
        "source_fingerprint": preview.get("fingerprint"),
        **result,
        "accepted": [],
        "rejected": [],
        "persisted": False,
    }
