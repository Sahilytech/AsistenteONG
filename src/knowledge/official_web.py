"""Consulta de Internet limitada a dominios oficiales configurados.
La aplicación es offline-first: si no hay red, usa memoria local. Los resultados
externos se guardan en SQLite para futuras consultas sin conexión.
"""
from __future__ import annotations
import html, re, socket, urllib.parse, urllib.request
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

def _host(url: str) -> str:
    return (urllib.parse.urlparse(url).hostname or "").lower().removeprefix("www.")

def _allowed(url: str) -> bool:
    host = _host(url)
    return any(host == d or host.endswith("." + d) for d in OFFICIAL_SOURCES)

def internet_available(timeout: float = 2.5) -> bool:
    """Comprueba acceso HTTP real en lugar de asumir que DNS/1.1.1.1 funciona."""
    for host in ("www.argentina.gob.ar", "www.buenosaires.gob.ar"):
        try:
            socket.getaddrinfo(host, 443, type=socket.SOCK_STREAM)
            req = urllib.request.Request(f"https://{host}/", method="HEAD", headers={"User-Agent":"AsistenteONG/1.0"})
            with urllib.request.urlopen(req, timeout=timeout):
                return True
        except Exception:
            continue
    return False

def _clean(value: str) -> str:
    value = html.unescape(value or "")
    value = re.sub(r"<[^>]+>", " ", value)
    return re.sub(r"\s+", " ", value).strip()

def _decode_result_url(href: str) -> str:
    href = html.unescape(href)
    parsed = urllib.parse.urlparse(href)
    if (parsed.hostname or "").endswith("duckduckgo.com"):
        href = urllib.parse.parse_qs(parsed.query).get("uddg", [href])[0]
    return href

def _search_engine(query: str, domain: str, limit: int = 4):
    q = urllib.parse.quote(f"site:{domain} {query}")
    url = f"https://html.duckduckgo.com/html/?q={q}"
    req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AsistenteONG/1.0"})
    with urllib.request.urlopen(req, timeout=10) as response:
        raw = response.read(1_500_000).decode("utf-8", errors="ignore")

    # DDG puede cambiar la envoltura de los resultados; extraemos los enlaces
    # result__a independientemente de la estructura de los div contenedores.
    anchors = re.findall(r'<a[^>]+class=["\'][^"\']*result__a[^"\']*["\'][^>]+href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', raw, flags=re.I|re.S)
    if not anchors:
        anchors = re.findall(r'<a[^>]+href=["\']([^"\']+)["\'][^>]*class=["\'][^"\']*result__a[^"\']*["\'][^>]*>(.*?)</a>', raw, flags=re.I|re.S)
    snippets = re.findall(r'class=["\'][^"\']*result__snippet[^"\']*["\'][^>]*>(.*?)</(?:a|div)>', raw, flags=re.I|re.S)
    results=[]
    for i,(href,title_html) in enumerate(anchors):
        href=_decode_result_url(href)
        if not _allowed(href):
            continue
        title=_clean(title_html) or href
        snippet=_clean(snippets[i]) if i < len(snippets) else "Fuente oficial"
        results.append(WebResult(title,href,snippet,domain))
        if len(results)>=limit:
            break
    return results

def search_official(query: str, memory: LocalMemory | None = None, limit: int = 8):
    query=(query or "").strip()
    memory=memory or LocalMemory()
    local=[WebResult(x["title"],x["url"],x["snippet"],x["domain"]) for x in memory.search(query,limit=limit)] if query else []
    if not query:
        return local, False
    if not internet_available():
        return local, False

    results=[]
    for domain in OFFICIAL_SOURCES:
        try:
            results.extend(_search_engine(query,domain,limit=2))
        except Exception:
            continue
        if len(results)>=limit:
            break

    unique=[]; seen=set()
    for item in results + local:
        if not _allowed(item.url) or item.url in seen:
            continue
        seen.add(item.url); unique.append(item)
        if item not in local:
            try: memory.save(item.url,item.domain,item.title,item.snippet)
            except Exception: pass
        if len(unique)>=limit:
            break
    return unique, True
