"""Consulta de Internet limitada a dominios oficiales configurados.

La aplicación sigue siendo offline-first: si no hay red, devuelve memoria local.
Los resultados externos se guardan en la memoria local para futuras consultas.
"""
from __future__ import annotations
import html
import re
import socket
import urllib.parse
import urllib.request
from dataclasses import dataclass
from .memory import LocalMemory

OFFICIAL_SOURCES = {
    "argentina.gob.ar": "Argentina.gob.ar",
    "buenosaires.gob.ar": "Buenos Aires Ciudad",
    "msal.gob.ar": "Ministerio de Salud",
    "jus.gob.ar": "Ministerio de Justicia",
    "minseg.gob.ar": "Ministerio de Seguridad",
}

@dataclass
class WebResult:
    title: str
    url: str
    snippet: str
    domain: str

def _host(url):
    return (urllib.parse.urlparse(url).hostname or "").lower().removeprefix("www.")

def _allowed(url):
    host = _host(url)
    return any(host == d or host.endswith("." + d) for d in OFFICIAL_SOURCES)

def internet_available(timeout=1.0):
    try:
        socket.create_connection(("1.1.1.1", 53), timeout=timeout).close(); return True
    except OSError: return False

def _clean(value):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", html.unescape(value or ""))).strip()

def _search_engine(query, domain, limit=4):
    q = urllib.parse.quote(f"site:{domain} {query}")
    url = f"https://html.duckduckgo.com/html/?q={q}"
    req = urllib.request.Request(url, headers={"User-Agent":"AsistenteONG/1.0"})
    with urllib.request.urlopen(req, timeout=7) as response:
        raw = response.read(1_000_000).decode("utf-8", errors="ignore")
    blocks = re.findall(r'<div[^>]+class=["\'][^"\']*result[^"\']*["\'][^>]*>(.*?)(?=<div[^>]+class=["\'][^"\']*result|</body>)', raw, flags=re.S|re.I)
    results=[]
    for block in blocks:
        link=re.search(r'class=["\'][^"\']*result__a[^"\']*["\'][^>]*href=["\']([^"\']+)', block, re.I) or re.search(r'href=["\']([^"\']+)["\'][^>]*class=["\'][^"\']*result__a', block, re.I)
        if not link: continue
        href=html.unescape(link.group(1)); parsed=urllib.parse.urlparse(href)
        if (parsed.hostname or "").endswith("duckduckgo.com"): href=urllib.parse.parse_qs(parsed.query).get("uddg", [""])[0]
        if not _allowed(href): continue
        title_m=re.search(r'class=["\'][^"\']*result__a[^"\']*["\'][^>]*>(.*?)</a>', block, re.I|re.S)
        snippet_m=re.search(r'class=["\'][^"\']*result__snippet[^"\']*["\'][^>]*>(.*?)</(?:a|div)>', block, re.I|re.S)
        results.append(WebResult(_clean(title_m.group(1)) if title_m else href,href,_clean(snippet_m.group(1)) if snippet_m else "Fuente oficial",domain))
        if len(results)>=limit: break
    return results

def search_official(query: str, memory: LocalMemory | None = None, limit=8):
    memory = memory or LocalMemory(); local = memory.search(query, limit=limit)
    if not internet_available(): return [WebResult(x["title"],x["url"],x["snippet"],x["domain"]) for x in local], False
    results=[]
    for domain in OFFICIAL_SOURCES:
        try: results.extend(_search_engine(query,domain,limit=2))
        except Exception: continue
        if len(results)>=limit: break
    unique=[]; seen=set()
    for item in results:
        if item.url in seen: continue
        seen.add(item.url); unique.append(item)
        try: memory.save(item.url,item.domain,item.title,item.snippet)
        except Exception: pass
        if len(unique)>=limit: break
    for item in [WebResult(x["title"],x["url"],x["snippet"],x["domain"]) for x in local]:
        if item.url not in seen and len(unique)<limit: unique.append(item)
    return unique, True
