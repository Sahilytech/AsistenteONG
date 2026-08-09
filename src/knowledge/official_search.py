"""Consulta opcional de fuentes oficiales cuando hay conectividad.

La búsqueda puede usar un buscador público solo como índice; los resultados se
aceptan únicamente si el enlace final pertenece a un dominio oficial permitido.
Los casos nunca se incluyen en la consulta.
"""
from __future__ import annotations
import html
import re
import socket
from urllib.parse import quote_plus, urlparse
from urllib.request import Request, urlopen

DEFAULT_DOMAINS = ("argentina.gob.ar", "boletinoficial.gob.ar", "mpf.gob.ar", "jus.gob.ar")


def has_internet(timeout=1.5):
    try:
        socket.create_connection(("1.1.1.1", 443), timeout=timeout).close()
        return True
    except OSError:
        return False


def _official(url, domains):
    try:
        host = (urlparse(url).hostname or "").lower().rstrip(".")
        return any(host == d or host.endswith("." + d) for d in domains)
    except Exception:
        return False


def search_official(query, domains=DEFAULT_DOMAINS, limit=8, timeout=8):
    """Devuelve enlaces y fragmentos de páginas oficiales; no envía el relato del caso."""
    query = (query or "").strip()
    if not query or not has_internet():
        return []
    site = " OR ".join(f"site:{d}" for d in domains)
    url = "https://html.duckduckgo.com/html/?q=" + quote_plus(f"({site}) {query}")
    req = Request(url, headers={"User-Agent": "AsistenteONG/1.0 (fuentes oficiales)"})
    try:
        with urlopen(req, timeout=timeout) as response:
            page = response.read().decode("utf-8", "ignore")
    except Exception:
        return []
    results = []
    blocks = re.findall(r'<a[^>]+class="result__a"[^>]+href="([^"]+)"[^>]*>(.*?)</a>', page, re.I | re.S)
    for raw_url, raw_title in blocks:
        clean = html.unescape(re.sub(r"<.*?>", "", raw_title)).strip()
        if "uddg=" in raw_url:
            from urllib.parse import parse_qs
            raw_url = parse_qs(urlparse(raw_url).query).get("uddg", [raw_url])[0]
        if not _official(raw_url, domains):
            continue
        results.append({"url": raw_url, "title": clean or raw_url, "domain": urlparse(raw_url).hostname or ""})
        if len(results) >= limit:
            break
    return results
