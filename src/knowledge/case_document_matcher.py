"""Recuperación local de evidencia documental para apoyar el análisis de casos."""
from __future__ import annotations
import re
from .memory import LocalMemory
STOPWORDS={"para","como","este","esta","estos","estas","desde","sobre","entre","donde","cuando","porque","tambien","también","con","sin","una","uno","los","las","del","por","que","sus","hay","muy","más","mas","pero","ante","hacia","ella","ellos","ellas","persona","caso"}
def _terms(text):return {t for t in re.findall(r"[a-záéíóúüñ]{4,}",(text or "").casefold()) if t not in STOPWORDS}
def _snippet(content,terms):
 sentences=re.split(r"(?<=[.!?])\s+|\n+",content or "");hits=[s.strip() for s in sentences if any(t in s.casefold() for t in terms)];return " ".join(hits[:3])[:1400]
def find_evidence(case_text,limit=6):
 terms=_terms(case_text)
 if not terms:return []
 rows=LocalMemory().search(" ".join(list(terms)[:12]),limit=50,include_content=True);out=[]
 for row in rows:
  if row.get("domain")!="archivo local":continue
  content=row.get("content") or row.get("snippet") or "";low=content.casefold();hits=sum(1 for t in terms if t in low)
  if hits:out.append({"title":row.get("title","Documento"),"url":row.get("url",""),"relevance":hits,"snippet":_snippet(content,terms) or content[:1400]})
 return sorted(out,key=lambda x:x["relevance"],reverse=True)[:limit]
def build_case_context(case_text,limit=5):
 matches=find_evidence(case_text,limit);return {"documents_found":len(matches),"matches":matches,"method":"coincidencia de términos y fragmentos locales; no es una conclusión automática"}
