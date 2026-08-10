"""Capa de análisis explicable para el expediente.

Convierte el resultado del motor local en una explicación auditable: qué señales
se encontraron, cuáles fueron descartadas por contexto/negación, qué información
falta y qué evidencia documental coincide. No toma decisiones profesionales.
"""
from typing import Any, Dict, Iterable, List, Optional
import re
from .case_profile import CaseProfile
from .reasoning import analyze_profile


def _unique(values: Iterable[Any]) -> List[Any]:
    seen = set()
    result = []
    for value in values:
        key = str(value).casefold()
        if key not in seen:
            seen.add(key)
            result.append(value)
    return result


def analyze_case(text: str, metadata: Optional[Dict[str, Any]] = None,
                 history: Optional[Iterable[Dict[str, Any]]] = None,
                 evidence: Optional[Iterable[Dict[str, Any]]] = None) -> Dict[str, Any]:
    """Analiza un relato y devuelve un resultado trazable y conservador."""
    from .case_profile import build_case_profile
    profile = build_case_profile(text, metadata or {})
    base = analyze_profile(profile)
    evidence_items = _rank_evidence(profile, evidence or [])
    history_items = _compare_history(profile, history or [])
    reasons = list(base.get("reasons", []))
    if profile.negated_signals:
        reasons.append("Se detectaron señales mencionadas en forma negada o descartada; no se usaron para elevar la urgencia.")
    if evidence_items:
        reasons.append(f"Se encontraron {len(evidence_items)} coincidencias documentales relevantes.")
    if history_items:
        reasons.append(f"Se comparó el relato con {len(history_items)} caso(s) previo(s) de la misma persona.")
    negative_signals = list(profile.negated_signals)
    positive_signals = list(profile.indicators) + list(profile.risk_indicators)
    return {
        **base,
        "profile": profile.to_dict(),
        "evidence": evidence_items,
        "history_comparison": history_items,
        "positive_signals": positive_signals,
        "negative_signals": negative_signals,
        "explanation": {
            "why": _unique(reasons),
            "positive_signals": positive_signals,
            "negative_signals": negative_signals,
            "contexts": list(profile.contexts),
            "missing_information": list(profile.missing_information),
            "limitations": [
                "La clasificación es orientativa y basada en reglas locales.",
                "La ausencia de una señal no demuestra que el hecho no exista.",
                "Toda intervención o derivación requiere revisión profesional.",
            ],
        },
        "review_required": True,
    }


def _rank_evidence(profile: CaseProfile, evidence: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Rankea evidencia usando señales estructuradas y términos relevantes del relato.

    Esto evita que la búsqueda pierda un documento solo porque el motor haya
    normalizado una expresión (por ejemplo, ``despido`` -> ``situacion laboral``).
    Las coincidencias siguen siendo evidencia, nunca una decisión.
    """
    structured = profile.indicators + profile.risk_indicators + profile.needs + profile.contexts + profile.relationships
    normalized_text = profile.text.casefold()
    stopwords = {
        "para", "como", "esta", "este", "esto", "tengo", "tiene", "necesito",
        "quiero", "porque", "desde", "sobre", "entre", "donde", "cuando", "con",
        "una", "unos", "unas", "por", "del", "las", "los", "que", "ante", "del",
    }
    text_terms = [
        term for term in re.findall(r"[\wáéíóúüñ]{4,}", normalized_text)
        if term not in stopwords
    ]
    terms = _unique(structured + text_terms)
    ranked = []
    for item in evidence:
        content = str(item.get("content", "")).casefold()
        title = str(item.get("title", "")).casefold()
        hay = f"{title} {content}"
        matched = sorted({str(term) for term in terms if str(term).casefold() in hay})
        if matched:
            ranked.append({**item, "matched_terms": matched, "evidence_score": len(matched)})
    return sorted(ranked, key=lambda x: x["evidence_score"], reverse=True)


def _compare_history(profile: CaseProfile, history: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    current = set(profile.categories + profile.indicators + profile.contexts)
    if not current:
        return []
    results = []
    for case in history:
        text = str(case.get("text", case.get("description", "")))
        hay = text.casefold()
        matched = sorted({term for term in current if str(term).casefold() in hay})
        if matched:
            results.append({
                "case_id": case.get("case_id", case.get("id")),
                "date": case.get("date", case.get("created_at", "")),
                "status": case.get("status", ""),
                "matched_terms": matched,
                "similarity_hint": min(1.0, len(matched) / max(1, len(current))),
            })
    return sorted(results, key=lambda x: x["similarity_hint"], reverse=True)


def _surface_signals(text: str) -> set[str]:
    from .case_profile import INDICATORS, normalize
    normalized = normalize(text)
    return {phrase for phrase in INDICATORS if phrase in normalized}


def compare_texts(text_a: str, text_b: str) -> Dict[str, Any]:
    """Compara dos relatos sin afirmar que sean el mismo hecho."""
    from .case_profile import build_case_profile
    a = build_case_profile(text_a)
    b = build_case_profile(text_b)
    left = set(a.indicators + a.categories + a.contexts + a.needs) | _surface_signals(text_a)
    right = set(b.indicators + b.categories + b.contexts + b.needs) | _surface_signals(text_b)
    common = sorted(left & right)
    only_a = sorted(left - right)
    only_b = sorted(right - left)
    union = left | right
    return {
        "common_signals": common,
        "only_first": only_a,
        "only_second": only_b,
        "similarity_hint": round(len(left & right) / len(union), 3) if union else 0.0,
        "review_required": True,
        "decision": None,
    }
