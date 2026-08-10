"""Recuperación local de evidencia documental para apoyar el análisis de casos."""
from __future__ import annotations
import re
from .memory import LocalMemory
STOPWORDS={"para","como","este","esta","estos","estas","desde","sobre","entre","donde","cuando","porque","tambien","también","con","sin","una","uno","los","las","del","por","que","sus","hay","muy","más","mas","pero","ante","hacia","ella","ellos","ellas","persona","caso","situación","situacion","necesita"}
def _terms(text):return {t for t in re.findall(r"[a-záéíóúüñ]{4,}",(text or "").casefold()) if t not in STOPWORDS}
def _snippet(content,terms):
 sentences=re.split(r"(?<=[.!?])\s+|\n+",content or "");hits=[s.strip() for s in sentences if any(t in s.casefold() for t in terms)];return " ".join(hits[:3])[:1600]
def _score(content,terms):
 low=content.casefold();present=[t for t in terms if t in low];return len(present),present
def find_evidence(case_text,limit=6):
 terms=_terms(case_text)
 if not terms:return []
 # Buscar fragmentos, no solamente documentos completos. Esto mejora mucho la precisión del contexto recuperado.
 rows=LocalMemory().search(" ".join(sorted(terms,key=len,reverse=True)[:16]),limit=80,include_content=True);out=[];seen=set()
 for row in rows:
  if not row.get("domain","").startswith("archivo local"):continue
  content=row.get("content") or row.get("snippet") or "";hits,present=_score(content,terms)
  if not hits:continue
  key=(row.get("title",""),row.get("url","").split("#chunk=")[0])
  # Si aparecen varios fragmentos del mismo documento, conservar el mejor contexto.
  item={"title":row.get("title","Documento"),"url":row.get("url",""),"relevance":hits,"matched_terms":present[:12],"snippet":_snippet(content,terms) or content[:1600]}
  old=seen.get(key) if isinstance(seen,dict) else None
  if not isinstance(seen,dict):seen={};old=None
  if old is None:seen[key]=item;out.append(item)
  elif item["relevance"]>old["relevance"]:
   out.remove(old);seen[key]=item;out.append(item)
 out.sort(key=lambda x:(x["relevance"],len(x["matched_terms"])),reverse=True)
 return out[:limit]
def build_case_context(case_text,limit=5):
 matches=find_evidence(case_text,limit);return {"documents_found":len(matches),"matches":matches,"method":"recuperación local por términos y fragmentos; los documentos son evidencia de apoyo y no constituyen una conclusión automática."}
