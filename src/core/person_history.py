"""Historial longitudinal y análisis comparativo por persona.

No toma decisiones profesionales: organiza antecedentes, detecta coincidencias
textuales y cambios entre casos y devuelve evidencia para revisión humana.
"""
from __future__ import annotations

import re
from collections import Counter
from datetime import datetime
from typing import Any


_STOPWORDS = {
    "para", "pero", "como", "desde", "esta", "este", "una", "uno", "con",
    "por", "que", "del", "las", "los", "una", "sus", "sobre", "fue", "hay",
    "sin", "más", "muy", "ante", "entre", "hacia", "también", "caso",
}


def _tokens(text: str) -> list[str]:
    words = re.findall(r"[a-záéíóúüñ]{4,}", (text or "").casefold())
    return [w for w in words if w not in _STOPWORDS]


def _date(value: Any) -> datetime:
    try:
        return datetime.fromisoformat(str(value))
    except (TypeError, ValueError):
        return datetime.min


def build_person_timeline(person: dict[str, Any], cases: list[dict[str, Any]]) -> dict[str, Any]:
    """Construye una línea temporal estable sin modificar datos."""
    ordered = sorted(cases, key=lambda c: _date(c.get("created_at")))
    events = []
    for index, case in enumerate(ordered, 1):
        events.append({
            "order": index,
            "case_number": case.get("case_number", ""),
            "date": case.get("created_at", ""),
            "type": case.get("case_type", ""),
            "status": case.get("status", ""),
            "urgency": case.get("urgency", ""),
            "summary": (case.get("text") or "").strip()[:280],
        })
    return {
        "person_id": person.get("person_id"),
        "person_name": person.get("name", ""),
        "case_count": len(events),
        "events": events,
    }


def compare_person_cases(cases: list[dict[str, Any]]) -> dict[str, Any]:
    """Compara casos como evidencia, no como diagnóstico ni decisión."""
    ordered = sorted(cases, key=lambda c: _date(c.get("created_at")))
    token_sets = [set(_tokens(c.get("text", ""))) for c in ordered]
    common = sorted(set.intersection(*token_sets)) if token_sets else []
    frequency = Counter(t for tokens in token_sets for t in tokens)
    recurring = sorted(t for t, n in frequency.items() if n >= 2)

    changes = []
    for previous, current in zip(ordered, ordered[1:]):
        before = set(_tokens(previous.get("text", "")))
        after = set(_tokens(current.get("text", "")))
        changes.append({
            "from_case": previous.get("case_number", ""),
            "to_case": current.get("case_number", ""),
            "new_terms": sorted(after - before)[:20],
            "terms_no_longer_present": sorted(before - after)[:20],
        })

    return {
        "cases_considered": len(ordered),
        "common_signals": common[:30],
        "recurring_signals": recurring[:30],
        "changes": changes,
        "evidence_only": True,
        "review_required": True,
        "disclaimer": "Las coincidencias y cambios son indicadores documentales; requieren revisión profesional y no constituyen una decisión.",
    }


def build_person_longitudinal_view(person: dict[str, Any], cases: list[dict[str, Any]]) -> dict[str, Any]:
    timeline = build_person_timeline(person, cases)
    comparison = compare_person_cases(cases)
    return {
        "person": person,
        "timeline": timeline,
        "comparison": comparison,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
    }
