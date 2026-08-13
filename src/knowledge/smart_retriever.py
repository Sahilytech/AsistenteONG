"""Recuperación local explicable para biblioteca y casos.

No toma decisiones: solo recupera evidencia y explica el motivo de coincidencia.
"""
from __future__ import annotations
import math
import re
from collections import Counter
from .memory import LocalMemory

_STOP = {"para", "como", "esta", "este", "desde", "sobre", "entre", "una", "uno", "con", "por", "del", "las", "los", "que", "sus", "son", "hay", "fue", "han", "the", "and", "with", "from", "this", "that"}

def _terms(text: str):
    return [t.casefold() for t in re.findall(r"[\wáéíóúüñ]{3,}", text or "") if t.casefold() not in _STOP]

def _score(query: str, text: str):
    q = _terms(query); d = _terms(text)
    if not q or not d:
        return 0.0, [], []
    qc, dc = Counter(q), Counter(d)
    common = sorted(set(qc) & set(dc), key=lambda x: (-qc[x], -dc[x], x))
    exact = sum(min(qc[x], dc[x]) for x in common)
    coverage = len(common) / max(1, len(set(q)))
    phrase = 1.0 if query.casefold().strip() and query.casefold().strip() in text.casefold() else 0.0
    # Saturated lexical score: frequency helps, but cannot dominate coverage.
    freq = sum(min(qc[x], dc[x]) for x in common) / max(1, len(q))
    score = min(1.0, 0.50 * coverage + 0.30 * min(1.0, freq) + 0.20 * phrase)
    return score, common, q

def retrieve(query: str, limit: int = 8, memory: LocalMemory | None = None):
    """Return ranked local evidence with provenance and explanation."""
    if not query or not query.strip():
        return []
    memory = memory or LocalMemory()
    rows = memory.search(query, limit=max(limit * 5, 30), include_content=True)
    ranked = []
    for row in rows:
        text = f"{row.get('title','')} {row.get('snippet','')} {row.get('content','')}"
        score, common, q = _score(query, text)
        if score <= 0:
            continue
        ranked.append({
            **row,
            "score": round(score, 4),
            "matched_terms": common,
            "query_terms": q,
            "evidence": row.get("content") or row.get("snippet", ""),
            "explanation": "Coincidencia textual con términos de la consulta" + (" y frase exacta" if query.casefold().strip() in text.casefold() else "") + ".",
            "is_decision": False,
            "requires_review": True,
        })
    ranked.sort(key=lambda x: (-x["score"], x.get("title", "")))
    return ranked[:limit]

def compare_texts(left: str, right: str):
    """Compare texts only; recurring terms are evidence, never a conclusion."""
    a, b = set(_terms(left)), set(_terms(right))
    common = sorted(a & b)
    return {"common_terms": common, "common_signals": common, "similarity": round(len(a & b) / max(1, len(a | b)), 4), "is_decision": False, "requires_review": True}
