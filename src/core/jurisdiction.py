"""Normalización de jurisdicción argentina para recursos y derivaciones."""
from dataclasses import dataclass, asdict
from typing import Dict

PROVINCES = {
    "caba": "Ciudad Autónoma de Buenos Aires", "capital federal": "Ciudad Autónoma de Buenos Aires",
    "buenos aires": "Buenos Aires", "cordoba": "Córdoba", "santa fe": "Santa Fe",
    "mendoza": "Mendoza", "tucuman": "Tucumán", "entre rios": "Entre Ríos",
    "salta": "Salta", "misiones": "Misiones", "chaco": "Chaco", "corrientes": "Corrientes",
    "formosa": "Formosa", "jujuy": "Jujuy", "la pampa": "La Pampa", "la rioja": "La Rioja",
    "neuquen": "Neuquén", "rio negro": "Río Negro", "san juan": "San Juan",
    "san luis": "San Luis", "santa cruz": "Santa Cruz", "santiago del estero": "Santiago del Estero",
    "tierra del fuego": "Tierra del Fuego", "catamarca": "Catamarca",
}

@dataclass
class Jurisdiction:
    province: str = ""
    municipality: str = ""
    locality: str = ""
    level: str = "no determinada"

    def to_dict(self) -> Dict:
        return asdict(self)


def resolve_jurisdiction(location: str) -> Jurisdiction:
    raw = (location or "").strip()
    low = raw.lower()
    for key, province in PROVINCES.items():
        if key in low:
            return Jurisdiction(province=province, locality=raw, level="provincial")
    return Jurisdiction(locality=raw)
