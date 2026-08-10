"""Búsqueda local explicable para la Biblioteca.

No usa servicios externos ni envía el contenido de los documentos fuera del
entorno local. Devuelve coincidencias y fragmentos que pueden citarse en un
análisis, sin convertir similitud en una decisión.
"""
from __future__ import annotations

import re
import unicodedata
from typing import Any, Iterable


def _normalize(value: Any) -> str:
    text = unicodedata.normalize("NFKD", str(value or ""))
    text = "".join(c for c in text if not unicodedata.combining(c))
    return text.casefold()


def _terms(text: str) -> list[str]:
    stop = {
        "para", "como", "esta", "este", "esto", "tengo", "tiene", "necesito",
        "quiero", "porque", "desde", "sobre", "entre", "donde", "cuando", "con",
        "una", "unos", "unas", "por", "del", "las", "los", "que", "ante", "solo",
    }
    return list(dict.fromkeys(t for t in re.findall(r"[\wáéíóúüñ]{4,}", _normalize(text)) if t not in stop))


def _snippet(content: str, matched: list[str], radius: int = 180) -> str:
    text = str(content or "").strip()
    if not text:
        return ""
    normalized = _normalize(text)
    positions = [normalized.find(term) for term in matched if normalized.find(term) >= 0]
    start = max(0, min(positions) - radius) if positions else 0
    end = min(len(text), start + radius * 2)
    prefix = "…" if start else ""
    suffix = "…" if end < len(text) else ""
    return prefix + text[start:end].strip() + suffix


def search_library(query: str, documents: Iterable[dict[str, Any]], limit: int = 10) -> list[dict[str, Any]]:
    """Rankea documentos por coincidencia léxica explicable y devuelve citas."""
    terms = _terms(query)
    if not terms:
        return []
    results: list[dict[str, Any]] = []
    for document in documents:
        title = _normalize(document.get("title"))
        content = _normalize(document.get("content"))
        haystack = f"{title} {content}"
        matched = [term for term in terms if term in haystack]
        if not matched:
            continue
        title_hits = sum(term in title for term in matched)
        content_hits = sum(term in content for term in matched)
        score = title_hits * 3 + content_hits
        results.append({
            **document,
            "matched_terms": matched,
            "search_score": score,
            "citation": {
                "source": document.get("url", document.get("source_url", "")),
                "title": document.get("title", ""),
                "saved_at": document.get("saved_at", ""),
                "fragment": _snippet(document.get("content", ""), matched),
            },
        })
    return sorted(results, key=lambda item: (-item["search_score"], str(item.get("title", "")).casefold()))[:limit]


def compare_documents(doc_a: dict[str, Any], doc_b: dict[str, Any]) -> dict[str, Any]:
    """Compara dos documentos por términos compartidos y exclusivos."""
    left = set(_terms(f"{doc_a.get('title', '')} {doc_a.get('content', '')}"))
    right = set(_terms(f"{doc_b.get('title', '')} {doc_b.get('content', '')}"))
    common = sorted(left & right)
    return {
        "common_terms": common,
        "only_first": sorted(left - right),
        "only_second": sorted(right - left),
        "similarity_hint": round(len(left & right) / len(left | right), 3) if left | right else 0.0,
        "review_required": True,
        "decision": None,
    }


def build_case_evidence(query: str, documents: Iterable[dict[str, Any]], limit: int = 8) -> dict[str, Any]:
    matches = search_library(query, documents, limit=limit)
    return {
        "query": query,
        "matches": matches,
        "evidence_count": len(matches),
        "review_required": True,
        "decision": None,
    }
