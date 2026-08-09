"""Construcción de un perfil integral y explicable a partir de un caso.

No diagnostica ni reemplaza al profesional. Extrae estructura para que el
motor pueda razonar sobre contexto, señales, necesidades e información faltante.
"""
from dataclasses import dataclass, field, asdict
import re
import unicodedata
from typing import Dict, List


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFKD", text or "")
    text = "".join(c for c in text if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", text.lower()).strip()


@dataclass
class CaseProfile:
    text: str
    people: List[str] = field(default_factory=list)
    relationships: List[str] = field(default_factory=list)
    contexts: List[str] = field(default_factory=list)
    indicators: List[str] = field(default_factory=list)
    risk_indicators: List[str] = field(default_factory=list)
    needs: List[str] = field(default_factory=list)
    categories: List[str] = field(default_factory=list)
    location: str = ""
    temporal_markers: List[str] = field(default_factory=list)
    negated_signals: List[str] = field(default_factory=list)
    missing_information: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict:
        return asdict(self)


# Frases deliberadamente concretas: una palabra aislada no alcanza para elevar riesgo.
RELATIONSHIPS = {
    "hijo": "hijo", "hija": "hija", "pareja": "pareja", "ex pareja": "ex pareja",
    "ex marido": "ex pareja", "ex esposa": "ex pareja", "madre": "madre",
    "padre": "padre", "hermano": "hermano", "hermana": "hermana",
}
CONTEXTS = {
    "trabajo": "laboral", "empleo": "laboral", "escuela": "educacion", "colegio": "educacion",
    "vivienda": "vivienda", "alquiler": "vivienda", "hospital": "salud", "medico": "salud",
    "juzgado": "legal", "abogado": "legal", "documentacion": "documentacion",
}
INDICATORS = {
    "despido": ("laboral", "situacion laboral"),
    "no me pagan": ("laboral", "situacion laboral"),
    "horas extras": ("laboral", "situacion laboral"),
    "quemadura": ("salud", "accidente"), "se quemo": ("salud", "accidente"),
    "fractura": ("salud", "lesion"), "accidente": ("salud", "accidente"),
    "amenaza": ("proteccion", "violencia o amenaza"),
    "maltrato": ("proteccion", "violencia"), "violencia": ("proteccion", "violencia"),
    "abuso sexual": ("proteccion", "violencia sexual"),
    "demanda": ("legal", "procedimiento legal"), "denuncia": ("legal", "procedimiento legal"),
    "desalojo": ("vivienda", "riesgo habitacional"), "sin vivienda": ("vivienda", "situacion habitacional"),
}
HIGH_RISK = {
    "no respira": "emergencia de salud", "inconsciente": "emergencia de salud",
    "sangrado abundante": "emergencia de salud", "riesgo de vida": "riesgo vital",
    "peligro inmediato": "peligro inmediato", "arma": "amenaza con arma",
}
NEEDS = {
    "ayuda": "orientacion", "asesoria": "orientacion", "asesoramiento": "orientacion",
    "refugio": "alojamiento seguro", "comida": "alimentacion", "medicacion": "salud",
}


def _contains_phrase(text: str, phrase: str) -> bool:
    # Evita el error clásico de detectar "ex" dentro de "extraño".
    return bool(re.search(r"(?<!\w)" + re.escape(phrase) + r"(?!\w)", text))


def _negated(text: str, phrase: str) -> bool:
    for m in re.finditer(r"(?<!\w)" + re.escape(phrase) + r"(?!\w)", text):
        before = text[max(0, m.start() - 30):m.start()]
        if re.search(r"\b(no|nunca|sin|niega|negó|nego)\b", before):
            return True
    return False


def build_case_profile(text: str, metadata: Dict | None = None) -> CaseProfile:
    metadata = metadata or {}
    normalized = normalize(text)
    profile = CaseProfile(text=text, location=(metadata.get("location") or "").strip())

    for phrase, relation in RELATIONSHIPS.items():
        if _contains_phrase(normalized, normalize(phrase)):
            profile.relationships.append(relation)
    for phrase, category in CONTEXTS.items():
        if _contains_phrase(normalized, normalize(phrase)):
            profile.contexts.append(category)
    for phrase, (category, indicator) in INDICATORS.items():
        phrase_n = normalize(phrase)
        if _contains_phrase(normalized, phrase_n):
            if _negated(normalized, phrase_n):
                profile.negated_signals.append(indicator)
                continue
            profile.indicators.append(indicator)
            profile.categories.append(category)
    for phrase, indicator in HIGH_RISK.items():
        phrase_n = normalize(phrase)
        if _contains_phrase(normalized, phrase_n) and not _negated(normalized, phrase_n):
            profile.risk_indicators.append(indicator)
    for phrase, need in NEEDS.items():
        if _contains_phrase(normalized, normalize(phrase)):
            profile.needs.append(need)

    profile.contexts = sorted(set(profile.contexts))
    profile.categories = sorted(set(profile.categories))
    profile.relationships = sorted(set(profile.relationships))
    profile.indicators = sorted(set(profile.indicators))
    profile.risk_indicators = sorted(set(profile.risk_indicators))
    profile.needs = sorted(set(profile.needs))
    profile.missing_information = _missing(profile)
    return profile


def _missing(profile: CaseProfile) -> List[str]:
    missing = []
    if not profile.text.strip():
        missing.append("relato")
    if not profile.location:
        missing.append("localidad o jurisdiccion")
    if not profile.indicators:
        missing.append("situacion concreta o hecho principal")
    if profile.categories and "laboral" in profile.categories:
        missing.extend(["fecha del hecho laboral", "documentacion o comunicaciones disponibles"])
    if "salud" in profile.categories:
        missing.extend(["estado actual", "atencion profesional recibida"])
    return list(dict.fromkeys(missing))
