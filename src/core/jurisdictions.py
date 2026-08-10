"""Jurisdicciones argentinas normalizadas para casos, recursos y fuentes."""
from __future__ import annotations
import unicodedata

# Las 23 provincias + Ciudad Autónoma de Buenos Aires = 24 jurisdicciones.
PROVINCES = (
    "Buenos Aires", "Catamarca", "Chaco", "Chubut", "Córdoba", "Corrientes",
    "Entre Ríos", "Formosa", "Jujuy", "La Pampa", "La Rioja", "Mendoza",
    "Misiones", "Neuquén", "Río Negro", "Salta", "San Juan", "San Luis",
    "Santa Cruz", "Santa Fe", "Santiago del Estero", "Tierra del Fuego",
    "Tucumán", "Ciudad Autónoma de Buenos Aires",
)

_ALIASES = {
    "caba": "Ciudad Autónoma de Buenos Aires",
    "capital federal": "Ciudad Autónoma de Buenos Aires",
    "ciudad autonoma de buenos aires": "Ciudad Autónoma de Buenos Aires",
    "ciudad de buenos aires": "Ciudad Autónoma de Buenos Aires",
}

def _key(value: str) -> str:
    text = unicodedata.normalize("NFKD", str(value or "").strip().casefold())
    return "".join(c for c in text if not unicodedata.combining(c))

_INDEX = {_key(name): name for name in PROVINCES}
_INDEX.update({_key(alias): value for alias, value in _ALIASES.items()})

def normalize_jurisdiction(province: str = "", municipality: str = "") -> dict:
    province_name = _INDEX.get(_key(province), str(province or "").strip())
    result = {"country": "Argentina", "province": province_name, "municipality": str(municipality or "").strip()}
    return result

def is_argentine_province(value: str) -> bool:
    return _key(value) in _INDEX
