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
from html.parser import HTMLParser
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

class _TextParser(HTMLParser):
    def __init__(self):
        super().__init__(); self.parts=[]; self.skip=0
    def handle_starttag(self, tag, attrs):
        if tag in {"script","style","noscript","svg"}: self.skip += 1
    def handle_endtag(self, tag):
        if tag in {"script","style","noscript","svg"} and self.skip: self.skip -= 1
    def handle_data(self, data):
        if not self.skip: self.parts.append(data)
    def text(self):
        return re.sub(r"\s+", " ", " ".join(self.parts)).strip()

def _host(url):
    return (urllib.parse.urlparse(url).hostname or "").lower().removeprefix("www.")

def _allowed(url):
    host = _host(url)
    return any(host == d or host.endswith("." + d) for d in OFFICIAL_SOURCES)

def internet_available(timeout=1.2):
    try:
        socket.create_connection(("1.1.1.1", 53), timeout=timeout).close(); return True
    except OSError: return False

def _search_engine(query, domain, limit=4):
    q = urllib.parse.quote(f"site:{domain} {query}")
    url = f"https://html.duckduckgo.com/html/?q={q}"
    req = urllib.request.Request(url, headers={"User-Agent":"AsistenteONG/1.0 (offline-first research)"})
    with urllib.request.urlopen(req, timeout=7) as response:
        raw = response.read(800_000).decode("utf-8", errors="ignore")
    results=[]
    for block in re.findall(r'<div class="result[^>]*>(.*?)</div>\s*</div>', raw, flags=re.S):
        hrefs = re.findall(r'href="([^"]+)"', block)
        if not hrefs: continue
        href=html.unescape(hrefs[0])
        parsed=urllib.parse.urlparse(href)
        if parsed.netloc.endswith("duckduckgo.com"): 
            params=urllib.parse.parse_qs(parsed.query); href=params.get("uddg", [""])[0]
        if not _allowed(href): continue
        title_m=re.search(r'class="result__a"[^>]*>(.*?)</a>', block, re.S)
        snippet_m=re.search(r'class="result__snippet"[^>]*>(.*?)</a?>', block, re.S)
        title=re.sub("<.*?>","",html.unescape(title_m.group(1))).strip() if title_m else href
        snippet=re.sub("<.*?>","",html.unescape(snippet_m.group(1))).strip() if snippet_m else "Fuente oficial"
        results.append(WebResult(title,href,snippet,domain))
        if len(results)>=limit: break
    return results

def search_official(query: str, memory: LocalMemory | None = None, limit=8):
    memory = memory or LocalMemory()
    local = memory.search(query, limit=limit)
    if not internet_available():
        return [WebResult(x["title"],x["url"],x["snippet"],x["domain"]) for x in local], False
    results=[]
    for domain in OFFICIAL_SOURCES:
        try: results.extend(_search_engine(query,domain,limit=2))
        except Exception: continue
        if len(results)>=limit: break
    seen=set()
    unique=[]
    for item in results:
        if item.url in seen: continue
        seen.add(item.url); unique.append(item)
        try: memory.save(item.url,item.domain,item.title,item.snippet)
        except Exception: pass
        if len(unique)>=limit: break
    # La memoria local aparece primero cuando ya contiene información útil.
    local_urls={x.url for x in unique}
    for item in [WebResult(x["title"],x["url"],x["snippet"],x["domain"]) for x in local]:
        if item.url not in local_urls and len(unique)<limit: unique.append(item)
    return unique, True
