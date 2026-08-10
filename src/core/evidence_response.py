"""Generación de respuestas basadas en evidencia local, sin convertir evidencia en decisión."""
from __future__ import annotations
import re
from typing import Any


def _terms(text: str) -> set[str]:
    return {x.casefold() for x in re.findall(r"[\wáéíóúüñ]{4,}", text or "")}


def build_evidence_response(case_text: str, evidence: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    """Resume coincidencias documentales y devuelve trazabilidad para revisión profesional."""
    evidence = evidence or []
    query_terms = _terms(case_text)
    items = []
    for item in evidence:
        content = str(item.get("content") or item.get("snippet") or "")
        matched = sorted(query_terms & _terms(content))
        if not matched:
            continue
        items.append({
            "source": item.get("title") or item.get("source_url") or "Fuente local",
            "location": item.get("location") or item.get("page") or None,
            "matched_terms": matched,
            "excerpt": content[:500],
            "source_url": item.get("source_url") or item.get("url"),
        })
    return {
        "summary": f"Se encontraron {len(items)} fuentes locales con coincidencias relevantes.",
        "evidence": items,
        "evidence_only": True,
        "is_decision": False,
        "review_required": True,
        "disclaimer": "Las coincidencias documentales sirven como evidencia de apoyo y requieren revisión profesional.",
    }


def compare_case_with_documents(case_text: str, documents: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    """Compara texto y documentos sin inferir diagnósticos ni decisiones."""
    result = build_evidence_response(case_text, documents)
    result["comparison"] = {
        "documents_considered": len(documents or []),
        "documents_with_matches": len(result["evidence"]),
        "method": "coincidencia léxica explicable",
    }
    return result
