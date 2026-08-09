"""Recuperación local de evidencia documental para apoyar el análisis de casos.
No modifica el modelo ni presenta coincidencias como hechos: devuelve fragmentos para revisión humana.
"""
from __future__ import annotations
import re
from .memory import LocalMemory
STOPWORDS={"para","como","este","esta","estos","estas","desde","sobre","entre","donde","cuando","porque","tambien","también","con","sin","una","uno","los","las","del","por","que","sus","hay","muy","más","mas","pero","ante","hacia","ella","ellos","ellas","persona","caso"}
def _terms(text):return {t for t in re.findall(r"[a-záéíóúüñ]{4,}",(text or "").casefold()) if t not in STOPWORDS}
def find_evidence(case_text,limit=6):
 memory=LocalMemory();terms=_terms(case_text)
 if not terms:return []
 rows=memory.search(" ".join(list(terms)[:12]),limit=30);out=[]
 for row in rows:
  if row.get("domain")!="archivo local":continue
  content=row.get("content") or row.get("snippet") or "";low=content.casefold();hits=sum(1 for t in terms if t in low)
  if hits:out.append({"title":row.get("title","Documento"),"url":row.get("url",""),"relevance":hits,"snippet":content[:1200]})
 return sorted(out,key=lambda x:x["relevance"],reverse=True)[:limit]

def build_case_context(case_text,limit=5):
 matches=find_evidence(case_text,limit);return {"documents_found":len(matches),"matches":matches,"method":"coincidencia de términos + fragmentos locales; requiere revisión humana"}
