"""Puente entre relatos, memoria documental e historial de la persona."""
from __future__ import annotations

from typing import Any, Iterable

from .explainable_analysis import analyze_case


def build_case_knowledge_context(
    case_text: str,
    memory,
    history: Iterable[dict[str, Any]] = (),
    metadata: dict[str, Any] | None = None,
    limit: int = 8,
) -> dict[str, Any]:
    """Recupera evidencia local relevante y la incorpora al análisis explicable."""
    documents = memory.search(case_text, limit=limit, include_content=True)
    analysis = analyze_case(
        case_text,
        metadata=metadata or {},
        history=history,
        evidence=documents,
    )
    return {
        "query": case_text,
        "documents_considered": len(documents),
        "documents": documents,
        "analysis": analysis,
        "review_required": True,
    }


def compare_case_with_documents(case_text: str, documents: Iterable[dict[str, Any]]) -> dict[str, Any]:
    """Compara un relato con documentos sin convertir coincidencias en decisiones."""
    result = analyze_case(case_text, evidence=documents)
    return {
        "matched_documents": result["evidence"],
        "positive_signals": result["positive_signals"],
        "negative_signals": result["negative_signals"],
        "explanation": result["explanation"],
        "review_required": True,
        "decision": None,
    }
