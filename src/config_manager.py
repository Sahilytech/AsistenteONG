"""Gestor de configuración y triaje local basado en reglas explicables."""

import logging
import re
from typing import Dict, List

logger = logging.getLogger(__name__)


class ConfigManager:
    """Motor de análisis local. Las reglas priorizan contexto sobre palabras aisladas."""

    KEYWORDS = {
        "Riesgo de Vida": [
            "suicidio", "suicida", "matar", "matarme", "matarse", "muerte", "arma",
            "veneno", "sobredosis", "asfixia", "apuñalar", "disparar", "explosivo",
            "inconsciente", "no respira", "no responde", "paro cardíaco", "paro cardiaco",
        ],
        "Violencia Severa": [
            "golpeado", "fractura", "sangre", "trauma", "hospitalización", "hospitalizacion",
            "urgencia", "grave", "crítico", "critico", "coma", "lesión", "lesion", "herida",
            "apaleado", "molido", "quemadura grave", "quemaduras graves",
        ],
        "Menores": [
            "niño", "niña", "hijo", "hija", "bebé", "bebe", "infante", "menor",
            "abuso infantil", "maltrato infantil", "explotación infantil",
        ],
        "Violencia Sexual": [
            "violación", "violacion", "abuso sexual", "tocamientos", "forzado",
            "sin consentimiento", "violada", "violado", "acoso sexual",
        ],
        "Violencia Doméstica": [
            "pareja", "marido", "esposo", "novia", "novio", "ex", "golpeó", "golpeo",
            "amenaza", "controla", "aislada", "control", "dependencia", "dominio",
        ],
        "Salud Mental": [
            "depresión", "depresion", "ansiedad", "pánico", "panico", "autolesión", "autolesion",
            "adicción", "adiccion", "droga", "alcohol", "consumo", "trastorno", "psicosis",
        ],
        "Necesidad Inmediata": [
            "ahora", "urgente", "emergencia", "ayuda", "sos", "rápido", "rapido",
            "inmediato", "prisa", "ya", "ahorita",
        ],
        "Asesoría Legal": [
            "abogado", "demanda", "custodia", "divorcio", "derechos", "juicio", "proceso",
            "legal", "ley", "justicia", "tribunal",
        ],
        "Recursos": [
            "refugio", "dinero", "trabajo", "comida", "vivienda", "medicinas", "alojamiento",
            "asistencia", "auxilio", "alimento", "hospedaje",
        ],
        "Accidente / Salud Física": [
            "me quemé", "se quemó", "me queme", "se quemo", "quemé", "queme", "quemadura",
            "quemado", "quemada", "me lastimé", "se lastimó", "accidente", "caída", "caida",
            "me corté", "se cortó", "me corte", "se corto", "corte accidental",
        ],
    }

    RESPONSES = {
        "Muy Alta": """
SITUACIÓN DE POSIBLE EMERGENCIA

El análisis automático detecta indicadores que pueden requerir atención inmediata.

ACCIONES:
1. Verificar con un profesional qué ocurrió y si existe peligro actual.
2. Si hay riesgo inmediato para la vida o una persona no responde, contactar al servicio de emergencias local.
3. Registrar datos relevantes sin reemplazar la valoración profesional.

IMPORTANTE: El sistema no diagnostica ni confirma una emergencia. La decisión final corresponde al profesional responsable.
        """,
        "Alta": """
SITUACIÓN URGENTE

El caso presenta indicadores que justifican valoración profesional prioritaria.

PRÓXIMOS PASOS:
1. Confirmar la situación y su gravedad con la persona involucrada.
2. Valorar si necesita atención médica, protección u otra intervención inmediata.
3. Registrar la información relevante y derivar al recurso correspondiente.

IMPORTANTE: Este resultado es orientativo y debe ser revisado por un profesional.
        """,
        "Media": """
SITUACIÓN PARA SEGUIMIENTO

El caso presenta indicadores que justifican seguimiento o asesoramiento profesional.

PRÓXIMOS PASOS:
1. Ampliar la información disponible.
2. Identificar necesidades concretas.
3. Derivar a los recursos adecuados.

Este análisis es orientativo y no reemplaza la valoración profesional.
        """,
        "Baja": """
INFORMACIÓN Y ORIENTACIÓN

No se detectaron indicadores suficientes para clasificar el caso como urgente mediante las reglas actuales.

PRÓXIMOS PASOS:
1. Revisar el relato completo.
2. Identificar necesidades y recursos.
3. Consultar con un profesional cuando corresponda.

El resultado automático no descarta riesgos que no hayan sido expresados en el texto.
        """,
        "Accidente": """
ACCIDENTE / SITUACIÓN DE SALUD FÍSICA

El relato parece describir un accidente o una lesión física, no una situación de violencia o riesgo autoinfligido por sí sola.

PRIORIDAD:
1. Confirmar qué ocurrió, cuándo y qué síntomas presenta la persona.
2. Si la lesión parece importante, empeora, afecta una zona sensible o genera preocupación, buscar valoración médica.
3. Si existe una emergencia médica, contactar al servicio de emergencias local.
4. No asumir gravedad únicamente por una palabra clave.

IMPORTANTE: El sistema no diagnostica. La valoración de la lesión corresponde a personal sanitario.
        """,
    }

    def __init__(self):
        logger.info("ConfigManager inicializado")

    @staticmethod
    def _contains_any(text: str, phrases: List[str]) -> List[str]:
        found = []
        for phrase in phrases:
            if phrase in text:
                found.append(phrase)
        return found

    def analyze(self, text: str) -> Dict:
        """Analiza el texto considerando coincidencias y contexto básico."""
        text_lower = re.sub(r"\s+", " ", text.lower().strip())
        found_keywords = []
        scores = {}

        for category, keywords in self.KEYWORDS.items():
            found = self._contains_any(text_lower, keywords)
            if found:
                found_keywords.extend(found)
                scores[category] = len(found)

        # Un accidente físico explícito tiene una ruta propia.
        accident = "Accidente / Salud Física" in scores
        violence_signal = any(c in scores for c in ("Violencia Sexual", "Violencia Doméstica"))
        life_signal = "Riesgo de Vida" in scores
        severe_signal = "Violencia Severa" in scores

        if accident and not life_signal and not violence_signal:
            urgency = self._accident_urgency(text_lower, scores)
            response = self.RESPONSES["Accidente"]
            resources = ["atención-médica"]
        else:
            urgency = self._determine_urgency(scores)
            response = self.RESPONSES[urgency]
            resources = self._suggest_resources(scores)

        return {
            "urgency": urgency,
            "keywords": list(dict.fromkeys(found_keywords))[:10],
            "response": response,
            "suggested_resources": resources,
            "scores": scores,
            "classification": "Accidente / Salud Física" if accident and not (life_signal or violence_signal) else "Triaje social",
            "context_note": "La clasificación se basa en reglas locales y debe ser validada por un profesional.",
        }

    def _accident_urgency(self, text: str, scores: Dict) -> str:
        """No convierte una lesión accidental en violencia/riesgo de vida por una palabra aislada."""
        severe_terms = [
            "no responde", "inconsciente", "no respira", "paro cardíaco", "paro cardiaco",
            "quemadura grave", "quemaduras graves", "muy grave", "hospitalización", "hospitalizacion",
        ]
        if any(term in text for term in severe_terms):
            return "Alta"
        if "Necesidad Inmediata" in scores:
            return "Alta"
        return "Media"

    def _determine_urgency(self, scores: Dict) -> str:
        critical = ["Riesgo de Vida", "Violencia Sexual"]
        if any(cat in scores for cat in critical):
            return "Muy Alta"
        if "Violencia Doméstica" in scores or "Violencia Severa" in scores:
            return "Alta"
        if any(cat in scores for cat in ["Salud Mental", "Asesoría Legal", "Necesidad Inmediata", "Menores"]):
            return "Media"
        return "Baja"

    def _suggest_resources(self, scores: Dict) -> List[str]:
        resources = []
        if "Riesgo de Vida" in scores or "Violencia Sexual" in scores:
            resources.extend(["emergencia", "línea-crisis", "refugio"])
        if "Violencia Doméstica" in scores:
            resources.extend(["abogado", "defensoría", "refugio"])
        if "Salud Mental" in scores:
            resources.append("salud-mental")
        if "Asesoría Legal" in scores:
            resources.append("abogado")
        if "Recursos" in scores:
            resources.extend(["municipalidad", "asistencia-social"])
        if "Menores" in scores and not resources:
            resources.append("protección-de-niñez")
        return list(dict.fromkeys(resources))[:5]
