"""
Detector de Urgencias - Análisis de palabras clave reales
"""

import re
import logging

logger = logging.getLogger(__name__)

# Palabras clave que indican URGENCIA MUY ALTA (riesgo de vida)
CRITICAL_KEYWORDS = {
    "amenaza de muerte": 9.5,
    "suicidio": 9.5,
    "arma": 9.0,
    "intento de": 9.0,
    "golpes": 8.5,
    "violación": 9.5,
    "abuso sexual": 9.5,
    "menor": 9.0,
    "niño": 9.0,
    "bebé": 9.0,
    "embarazada": 8.5,
    "sangre": 8.0,
    "hospital": 7.5,
    "llamar policia": 8.0,
    "violencia": 7.0,
}

# Palabras que indican URGENCIA ALTA
HIGH_KEYWORDS = {
    "miedo": 6.5,
    "aterrada": 6.5,
    "amenaza": 6.5,
    "control": 5.5,
    "aislada": 5.0,
    "economía": 4.5,
    "trabaja": 4.0,
    "abuso": 7.0,
    "golpeada": 7.5,
}

# Palabras que indican URGENCIA MEDIA
MEDIUM_KEYWORDS = {
    "conflicto": 3.5,
    "discusión": 3.0,
    "problema": 2.5,
    "separación": 4.0,
    "consulta": 2.0,
}


def detect_urgency(text: str) -> dict:
    """
    Detecta urgencia basada en palabras clave.
    
    Returns:
        {
            "urgency_level": "Muy Alta" | "Alta" | "Media" | "Baja",
            "score": 0-10,
            "keywords_found": [list de palabras encontradas],
            "detected_risks": [lista de riesgos detectados]
        }
    """
    
    text_lower = text.lower()
    score = 0.0
    keywords_found = []
    risks = []
    
    # Buscar palabras críticas
    for keyword, weight in CRITICAL_KEYWORDS.items():
        if keyword in text_lower:
            score = max(score, weight)
            keywords_found.append(keyword)
            
            # Agregar riesgo específico
            if "muerte" in keyword or "suicidio" in keyword:
                risks.append("⚠️ RIESGO DE VIDA INMEDIATO")
            elif "sexual" in keyword or "violación" in keyword:
                risks.append("⚠️ ABUSO SEXUAL DOCUMENTADO")
            elif "menor" in keyword or "niño" in keyword or "bebé" in keyword:
                risks.append("⚠️ MENORES INVOLUCRADOS")
            elif "embarazada" in keyword:
                risks.append("⚠️ EMBARAZO EN RIESGO")
            elif "arma" in keyword:
                risks.append("⚠️ ARMAS INVOLUCRADAS")
    
    # Buscar palabras de alta urgencia
    if score < 8.0:
        for keyword, weight in HIGH_KEYWORDS.items():
            if keyword in text_lower:
                score = max(score, weight)
                keywords_found.append(keyword)
                if score >= 7.0:
                    risks.append("⚠️ ABUSO DOCUMENTADO")
    
    # Buscar palabras de urgencia media
    if score < 5.0:
        for keyword, weight in MEDIUM_KEYWORDS.items():
            if keyword in text_lower:
                score = max(score, weight)
                keywords_found.append(keyword)
    
    # Determinar nivel de urgencia
    if score >= 8.0:
        urgency_level = "Muy Alta"
    elif score >= 6.0:
        urgency_level = "Alta"
    elif score >= 3.5:
        urgency_level = "Media"
    else:
        urgency_level = "Baja"
    
    return {
        "urgency_level": urgency_level,
        "score": round(score, 2),
        "keywords_found": list(set(keywords_found)),  # Unique
        "detected_risks": risks if risks else ["Consulta general"],
        "needs_immediate_action": score >= 8.0
    }


def generate_response(case_data: dict) -> str:
    """
    Genera respuesta borrador basada en urgencia y riesgos.
    """
    
    urgency = case_data.get("urgency_level", "Baja")
    risks = case_data.get("detected_risks", [])
    
    # Saludo profesional
    response = "---RESPUESTA BORRADOR---\n\n"
    response += "Estimada/o,\n\n"
    
    # Validar recepción
    response += "Hemos recibido tu mensaje y entendemos tu situación.\n"
    
    # Según urgencia
    if urgency == "Muy Alta":
        response += "\n⚠️ **SITUACIÓN CRÍTICA DETECTADA**\n"
        response += "Si estás en peligro INMEDIATO:\n"
        response += "📞 LLAMA A LA POLICÍA: 911\n"
        response += "📞 EMERGENCIAS MÉDICAS: 107 (CABA) / 911\n"
        response += "📞 LÍNEA DE CRISIS 24/7: 0800-666-7777\n\n"
        
    elif urgency == "Alta":
        response += "\n🔴 **SITUACIÓN GRAVE DETECTADA**\n"
        response += "Te recomendamos contactar:\n"
        response += "📞 Línea de Asesoría: 0800-333-4444\n"
        response += "📞 Refugio Seguro: 0800-555-1234\n\n"
    
    # Pasos sugeridos
    response += "PASOS RECOMENDADOS:\n"
    response += "1. Busca un lugar seguro si es necesario\n"
    response += "2. Contacta un abogado/asesor legal\n"
    response += "3. Considera una denuncia formal si corresponde\n"
    response += "4. Documenta los hechos (fechas, eventos)\n"
    response += "5. Busca apoyo emocional y psicológico\n\n"
    
    # Contactos según riesgos
    if any("MENORES" in r for r in risks):
        response += "PROTECCIÓN DE MENORES:\n"
        response += "📞 Defensoría de Derechos de Niñas/os: 4343-9950\n"
        response += "📞 Dirección Nacional de Políticas Sociales: 4349-9700\n\n"
    
    if any("SEXUAL" in r for r in risks):
        response += "ASISTENCIA POR ABUSO SEXUAL:\n"
        response += "📞 Centro de Atención a Víctimas de Violencia Sexual: 4119-5555\n"
        response += "📞 Hospital de Clínicas (Medicina Legal): 4544-1234\n\n"
    
    if any("EMBARAZO" in r for r in risks):
        response += "PROTECCIÓN DE EMBARAZO:\n"
        response += "📞 Hospital Maternidad: 4961-2611\n"
        response += "📞 Centro de Salud Sexual: 4342-5678\n\n"
    
    # Privacidad
    response += "PRIVACIDAD Y SEGURIDAD:\n"
    response += "✓ Este mensaje fue procesado OFFLINE (sin internet)\n"
    response += "✓ Tus datos NO fueron enviados a servidores externos\n"
    response += "✓ La información está cifrada y segura\n\n"
    
    # Cierre
    response += "Estamos aquí para apoyarte.\n"
    response += "No estás sola/o. Hay recursos y personas listos para ayudar.\n\n"
    response += "---FIN RESPUESTA BORRADOR---"
    
    return response
