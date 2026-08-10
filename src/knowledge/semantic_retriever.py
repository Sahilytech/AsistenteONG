"""Recuperador local, explicable y sin servicios externos para la Biblioteca.

No toma decisiones sobre casos: solamente ordena evidencia documental por relevancia.
"""
from __future__ import annotations
import math
import re
from collections import Counter
from dataclasses import dataclass
from typing import Iterable

_WORD = re.compile(r"[\wáéíóúüñ]{2,}", re.IGNORECASE)
_STOP = {"para", "como", "esta", "este", "con", "los", "las", "del", "una", "uno", "por", "que", "una", "sus", "sobre", "entre", "desde", "hacia"}


def _tokens(text: str) -> list[str]:
    return [w.casefold() for w in _WORD.findall(text or "") if w.casefold() not in _STOP]


def _cosine(a: Counter[str], b: Counter[str]) -> float:
    if not a or not b:
        return 0.0
    dot = sum(v * b.get(k, 0) for k, v in a.items())
    na = math.sqrt(sum(v * v for v in a.values()))
    nb = math.sqrt(sum(v * v for v in b.values()))
    return dot / (na * nb) if na and nb else 0.0


@dataclass(frozen=True)
class EvidenceHit:
    source_url: str
    title: str
    domain: str
    snippet: str
    score: float
    matched_terms: tuple[str, ...]
    reason: str

    def as_dict(self) -> dict:
        return {
            "source_url": self.source_url,
            "title": self.title,
            "domain": self.domain,
            "snippet": self.snippet,
            "score": round(self.score, 4),
            "matched_terms": list(self.matched_terms),
            "reason": self.reason,
            "evidence_only": True,
            "review_required": True,
        }


class LocalSemanticRetriever:
    """Ranking híbrido: coincidencia léxica + similitud de vocabulario.

    Está pensado para funcionar completamente offline y ser auditable. No afirma
    que dos textos tengan el mismo significado; sólo calcula relevancia documental.
    """

    def rank(self, query: str, documents: Iterable[dict], limit: int = 8) -> list[dict]:
        q_terms = _tokens(query)
        if not q_terms:
            return []
        q_counter = Counter(q_terms)
        query_lower = (query or "").casefold().strip()
        hits: list[EvidenceHit] = []
        for doc in documents:
            title = str(doc.get("title") or "")
            snippet = str(doc.get("snippet") or "")
            content = str(doc.get("content") or "")
            haystack = f"{title} {snippet} {content}".casefold()
            terms = _tokens(haystack)
            counts = Counter(terms)
            matched = tuple(sorted(set(q_terms) & set(terms)))
            if not matched:
                continue
            coverage = len(matched) / max(1, len(set(q_terms)))
            cosine = _cosine(q_counter, counts)
            title_bonus = sum(1 for term in set(q_terms) if term in title.casefold()) * 0.08
            phrase_bonus = 0.12 if query_lower and query_lower in haystack else 0.0
            score = min(1.0, coverage * 0.62 + cosine * 0.22 + title_bonus + phrase_bonus)
            reason_parts = [f"{len(matched)}/{len(set(q_terms))} términos coinciden"]
            if title_bonus:
                reason_parts.append("coincidencia en título")
            if phrase_bonus:
                reason_parts.append("frase exacta")
            hits.append(EvidenceHit(
                source_url=str(doc.get("url") or doc.get("source_url") or ""),
                title=title,
                domain=str(doc.get("domain") or ""),
                snippet=snippet or content[:500],
                score=score,
                matched_terms=matched,
                reason="; ".join(reason_parts),
            ))
        hits.sort(key=lambda h: (-h.score, h.title.casefold()))
        return [h.as_dict() for h in hits[:max(1, limit)]]

    def explain(self, query: str, documents: Iterable[dict], limit: int = 8) -> dict:
        results = self.rank(query, documents, limit)
        return {
            "query": query,
            "results": results,
            "method": "ranking local híbrido (términos + vocabulario + título + frase)",
            "offline": True,
            "is_decision": False,
            "review_required": True,
        }
