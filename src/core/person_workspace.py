"""Ficha integral de persona: datos, casos, historial y evidencia."""
from __future__ import annotations
from typing import Any


def build_person_workspace(person: dict[str, Any], cases: list[dict[str, Any]], evidence: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    """Construye una vista unificada sin convertir evidencia en decisiones."""
    ordered = sorted(cases, key=lambda c: str(c.get("date") or c.get("created_at") or ""))
    return {
        "person": dict(person),
        "cases": ordered,
        "case_count": len(ordered),
        "timeline": [
            {"case_id": c.get("id"), "date": c.get("date") or c.get("created_at"), "title": c.get("title") or c.get("summary", "")}
            for c in ordered
        ],
        "evidence": list(evidence or []),
        "evidence_only": True,
        "is_decision": False,
        "review_required": True,
    }


def summarize_workspace(workspace: dict[str, Any]) -> dict[str, Any]:
    return {
        "case_count": workspace.get("case_count", 0),
        "evidence_count": len(workspace.get("evidence", [])),
        "review_required": True,
        "has_history": bool(workspace.get("cases")),
    }
