"""
Gestor de configuración - Análisis inteligente de casos
"""

import logging
from typing import Dict, List

logger = logging.getLogger(__name__)


class ConfigManager:
    """Motor de análisis inteligente."""
    
    # Palabras clave por categoría
    KEYWORDS = {
        "Riesgo de Vida": [
            "suicidio", "matar", "muerte", "arma", "veneno", "sobredosis",
            "cuerda", "precipicio", "tóxico", "intoxicación", "asfixia",
            "apuñalar", "disparar", "explosivo", "ácido", "quemadura"
        ],
        "Violencia Severa": [
            "golpeado", "fractura", "sangre", "trauma", "hospitalizac",
            "urgencia", "grave", "crítico", "inconsciente", "coma",
            "lesión", "herida", "apaleado", "molido"
        ],
        "Menores": [
            "niño", "niña", "hijo", "hija", "bebé", "infante", "menor",
            "abuso infantil", "pedofilia", "maltrato niño", "explotación"
        ],
        "Violencia Sexual": [
            "violación", "abuso sexual", "tocamientos", "forzado",
            "sin consentimiento", "violada", "violado", "acoso sexual",
            "exhibicionismo", "pornografía"
        ],
        "Violencia Doméstica": [
            "pareja", "marido", "esposo", "novia", "novio", "ex",
            "golpeó", "amenaza", "controla", "aislada", "control",
            "dependencia", "dominio"
        ],
        "Salud Mental": [
            "depresión", "ansiedad", "pánico", "autolesión", "adicción",
            "droga", "alcohol", "consumo", "trastorno", "psicosis",
            "bipolar", "esquizofrenia"
        ],
        "Necesidad Inmediata": [
            "ahora", "urgente", "emergencia", "ayuda", "SOS", "rápido",
            "inmediato", "prisa", "ya", "ahorita"
        ],
        "Asesoría Legal": [
            "abogado", "demanda", "custodia", "divorcio", "derechos",
            "juicio", "proceso", "legal", "ley", "justicia", "tribunal"
        ],
        "Recursos": [
            "refugio", "dinero", "trabajo", "comida", "vivienda",
            "medicinas", "alojamiento", "asistencia", "auxilio",
            "alimento", "hospedaje"
        ],
    }
    
    # Plantillas de respuesta por urgencia
    RESPONSES = {
        "Muy Alta": """
🆘 SITUACIÓN DE EMERGENCIA - ACCIÓN INMEDIATA

Esta situación requiere intervención profesional inmediata.

ACCIONES A TOMAR AHORA:
1. Llamar 911 o emergencia local
2. Informar que hay riesgo de vida
3. Dar ubicación exacta
4. Seguir instrucciones del operador

LÍNEAS DIRECTAS 24/7:
• Crisis Nacional: 0800-666-7777
• Línea Suicida: 0800-110-1010
• Violencia: 0800-345-1999

⚠️ IMPORTANTE: Este es un análisis automático. Confirma la emergencia con un profesional.
        """,
        
        "Alta": """
🟠 SITUACIÓN URGENTE - ATENCIÓN HOY

Esta situación requiere atención profesional hoy.

RECURSOS RECOMENDADOS:
• Defensora Pública: 4321-0987
• Centro de Asistencia Legal: 0800-333-4444
• Línea de Violencia: 0800-345-1999
• Refugios de emergencia: Disponibles 24/7

PRÓXIMOS PASOS:
1. Contacta a recursos de inmediato
2. Documenta la situación
3. Busca apoyo profesional
4. Mantente en lugar seguro

⚠️ Este análisis es orientativo. Consulta con profesionales.
        """,
        
        "Media": """
🟡 SITUACIÓN IMPORTANTE - GESTIONAR PRONTO

Esta situación requiere seguimiento y recursos.

RECURSOS DISPONIBLES:
• Asesoría Legal Gratuita: 0800-333-4444
• Psicología: Centro Salud Mental
• Derechos: Centro de Derechos Humanos
• Información general disponible

RECOMENDACIONES:
1. Busca asesoría profesional
2. Documenta todo
3. Conoce tus derechos
4. Mantén contacto con recursos

💡 Este análisis es una guía. Consulta especialistas.
        """,
        
        "Baja": """
⚪ INFORMACIÓN Y ORIENTACIÓN

Esta consulta puede ser resuelta con asesoría.

RECURSOS DE INFORMACIÓN:
• Centro de Información Legal
• Líneas de orientación
• Recursos comunitarios
• Guías y materiales educativos

PASOS:
1. Busca información completa
2. Consulta con profesionales
3. Explora opciones disponibles
4. Toma decisiones informada

📌 Para más información, contacta recursos especializados.
        """
    }
    
    def __init__(self):
        """Inicializa."""
        logger.info("✅ ConfigManager inicializado")
    
    def analyze(self, text: str) -> Dict:
        """Analiza un caso completo."""
        text_lower = text.lower()
        
        # Detectar palabras clave
        found_keywords = []
        urgency_scores = {}
        
        for category, keywords in self.KEYWORDS.items():
            score = 0
            found = []
            
            for keyword in keywords:
                if keyword in text_lower:
                    score += 1
                    found.append(keyword)
            
            if score > 0:
                found_keywords.extend(found)
                urgency_scores[category] = score
        
        # Determinar urgencia
        urgency = self._determine_urgency(urgency_scores)
        
        # Generar respuesta
        response = self.RESPONSES.get(urgency, self.RESPONSES["Baja"])
        
        # Recursos sugeridos
        resources = self._suggest_resources(urgency_scores)
        
        return {
            "urgency": urgency,
            "keywords": list(set(found_keywords))[:10],  # Max 10
            "response": response,
            "suggested_resources": resources,
            "scores": urgency_scores
        }
    
    def _determine_urgency(self, scores: Dict) -> str:
        """Determina urgencia basado en palabras detectadas."""
        
        # Urgencias críticas
        critical = ["Riesgo de Vida", "Violencia Sexual", "Menores"]
        if any(cat in scores for cat in critical):
            return "Muy Alta"
        
        # Alta urgencia
        high = ["Violencia Severa", "Violencia Doméstica"]
        if any(cat in scores for cat in high):
            return "Alta"
        
        # Media urgencia
        medium = ["Salud Mental", "Asesoría Legal", "Necesidad Inmediata"]
        if any(cat in scores for cat in medium):
            return "Media"
        
        # Por defecto
        return "Baja"
    
    def _suggest_resources(self, scores: Dict) -> List[str]:
        """Sugiere recursos basado en análisis."""
        resources = []
        
        if "Riesgo de Vida" in scores or "Violencia Sexual" in scores:
            resources.extend(["emergencia", "línea-crisis", "refugio"])
        
        if "Violencia Doméstica" in scores:
            resources.extend(["abogado", "defensoría", "refugio"])
        
        if "Salud Mental" in scores:
            resources.append("psicólogo")
        
        if "Asesoría Legal" in scores:
            resources.append("abogado")
        
        if "Recursos" in scores:
            resources.extend(["municipalidad", "asistencia-social"])
        
        return list(set(resources))[:5]  # Max 5
