"""Análisis contextual longitudinal, conservador y trazable."""
from __future__ import annotations
from collections import Counter
from typing import Any, Iterable
from .explainable_analysis import analyze_case


def _history_candidates(history: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    """Normaliza formatos habituales de historial antes de compararlo."""
    result=[]
    for item in history:
        if not isinstance(item, dict):
            continue
        text=str(item.get("text") or item.get("description") or item.get("summary") or item.get("relato") or "").strip()
        if not text and isinstance(item.get("case"), dict):
            nested=item["case"]
            text=str(nested.get("text") or nested.get("description") or nested.get("summary") or "").strip()
            item={**nested, **item}
        if text:
            result.append({**item,"text":text})
    return result


def analyze_person_case(case_text: str, history: Iterable[dict[str, Any]] = (), evidence: Iterable[dict[str, Any]] = (), metadata: dict[str, Any] | None = None) -> dict[str, Any]:
    history=_history_candidates(history)
    evidence=list(evidence)
    analysis=analyze_case(case_text, metadata=metadata or {}, history=history, evidence=evidence)
    related=analysis.get("history_comparison",[])
    evidence_items=analysis.get("evidence",[])
    recurring=Counter(term for item in related for term in item.get("matched_terms",[]))
    return {"analysis":analysis,"history":{"cases_considered":len(history),"related_cases":related,"recurring_signals":[term for term,_ in recurring.most_common()]},"evidence":{"documents_considered":len(evidence),"relevant_documents":evidence_items},"review_required":True,"decision":None}


def compare_case_history(case_text: str, history: Iterable[dict[str, Any]]) -> dict[str, Any]:
    """Compara contra casos previos sin convertir similitud en una decisión."""
    normalized=_history_candidates(history)
    result=analyze_case(case_text, history=normalized)
    return {"related_cases":result.get("history_comparison",[]),"cases_considered":len(normalized),"review_required":True,"decision":None}
