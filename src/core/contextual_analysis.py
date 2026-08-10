"""Análisis contextual de expediente: organiza señales, historial y evidencia.

La salida es deliberadamente orientativa: no diagnostica ni decide intervenciones.
"""
from __future__ import annotations

from collections import Counter
from typing import Any, Iterable

from .explainable_analysis import analyze_case


def analyze_person_case(
    case_text: str,
    history: Iterable[dict[str, Any]] = (),
    evidence: Iterable[dict[str, Any]] = (),
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    history = list(history)
    evidence = list(evidence)
    analysis = analyze_case(case_text, metadata=metadata or {}, history=history, evidence=evidence)

    related = analysis.get("history_comparison", [])
    evidence_items = analysis.get("evidence", [])
    recurring = Counter(
        term
        for item in related
        for term in item.get("matched_terms", [])
    )

    return {
        "analysis": analysis,
        "history": {
            "cases_considered": len(history),
            "related_cases": related,
            "recurring_signals": [term for term, _ in recurring.most_common()],
        },
        "evidence": {
            "documents_considered": len(evidence),
            "relevant_documents": evidence_items,
        },
        "review_required": True,
        "decision": None,
    }


def compare_case_history(case_text: str, history: Iterable[dict[str, Any]]) -> dict[str, Any]:
    """Devuelve relaciones observables con casos previos, sin convertirlas en conclusiones."""
    history = list(history)
    result = analyze_case(case_text, history=history)
    return {
        "related_cases": result.get("history_comparison", []),
        "review_required": True,
        "decision": None,
    }
