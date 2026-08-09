"""Motor de razonamiento local, explicable y conservador."""
from typing import Dict
from .case_profile import CaseProfile


def analyze_profile(profile: CaseProfile) -> Dict:
    risk = "no determinada"
    reasons = []
    if profile.risk_indicators:
        risk = "muy alta"
        reasons.extend(profile.risk_indicators)
    elif profile.indicators:
        risk = "media"
        reasons.extend(profile.indicators)
    elif profile.contexts:
        risk = "no determinada"
        reasons.append("solo hay contexto, sin indicador concreto suficiente")
    else:
        reasons.append("no hay señales suficientes para clasificar la situación")

    category = _category(profile)
    questions = _questions(profile)
    return {
        "urgency": risk,
        "category": category,
        "confidence": _confidence(profile),
        "indicators": profile.indicators,
        "risk_indicators": profile.risk_indicators,
        "contexts": profile.contexts,
        "relationships": profile.relationships,
        "needs": profile.needs,
        "missing_information": profile.missing_information,
        "negated_signals": profile.negated_signals,
        "reasons": reasons,
        "questions": questions,
        "professional_note": "Resultado generado por reglas locales explicables. No constituye diagnóstico ni decisión profesional.",
    }


def _category(profile: CaseProfile) -> str:
    priority = ["salud", "proteccion", "legal", "laboral", "vivienda", "educacion", "documentacion"]
    for item in priority:
        if item in profile.categories:
            labels = {"salud":"Salud / accidente", "proteccion":"Proteccion / violencia", "legal":"Orientacion legal", "laboral":"Situacion laboral", "vivienda":"Vivienda", "educacion":"Educacion", "documentacion":"Documentacion"}
            return labels[item]
    return "Consulta general"


def _confidence(profile: CaseProfile) -> str:
    if profile.risk_indicators:
        return "alta"
    if len(profile.indicators) >= 2:
        return "media-alta"
    if profile.indicators:
        return "media"
    return "baja"


def _questions(profile: CaseProfile):
    questions = []
    if not profile.text.strip():
        questions.append("¿Qué ocurrió y cuándo?")
    if not profile.location:
        questions.append("¿En qué localidad, municipio o provincia ocurre la situación?")
    if "salud" in profile.categories:
        questions += ["¿Cuál es el estado actual?", "¿Recibió atención profesional?"]
    if "laboral" in profile.categories:
        questions += ["¿Cuándo ocurrió el hecho laboral?", "¿Qué documentación o comunicaciones conserva?"]
    if "legal" in profile.categories:
        questions += ["¿Qué actuación o trámite legal existe actualmente?", "¿Qué necesita la persona en este momento?"]
    if not profile.indicators:
        questions.append("¿Cuál es el hecho concreto que motiva la consulta?")
    return list(dict.fromkeys(questions))
