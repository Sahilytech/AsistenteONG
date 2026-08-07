"""
Gestor de configuración - Palabras clave, plantillas, urgencia
"""

from dataclasses import dataclass, field
from typing import Dict, List, Set
import json
import logging

logger = logging.getLogger(__name__)


@dataclass
class UrgencyConfig:
    """Configuración de detectores de urgencia."""
    
    # Palabras clave de RIESGO DE VIDA (Muy Alta)
    risk_of_death: Set[str] = field(default_factory=lambda: {
        "suicidio", "matar", "muerte", "arma", "cuchillo", "revolver", "pistola",
        "veneno", "sobredosis", "ahorcarse", "tirarse", "acantilado",
        "me voy a matar", "no quiero vivir", "quiero morir",
        "amenaza de muerte", "intento de suicidio", "riesgo inmediato"
    })
    
    # Palabras clave VIOLENCIA SEVERA (Muy Alta)
    severe_violence: Set[str] = field(default_factory=lambda: {
        "violencia", "golpes", "golpeada", "golpeado", "fractura", "sangre",
        "herida", "lesión", "traumático", "ataque", "agresión",
        "puñetazos", "patadas", "paliza", "pegadas", "pegaron",
        "hospital", "emergencia", "urgencias"
    })
    
    # Palabras clave MENORES (Muy Alta)
    minors_involved: Set[str] = field(default_factory=lambda: {
        "niño", "niña", "hijo", "hija", "bebé", "menor", "infancia",
        "abuso infantil", "explotación", "tocamientos", "abuso sexual",
        "pederastia", "violación de menores", "pornografía infantil"
    })
    
    # Palabras clave VIOLENCIA SEXUAL (Muy Alta)
    sexual_violence: Set[str] = field(default_factory=lambda: {
        "violación", "violada", "violada", "abuso sexual", "tocamientos",
        "coerción sexual", "acoso sexual", "sexo forzado", "violencia sexual",
        "pasó algo sexual", "me obligó", "me forzó"
    })
    
    # Palabras clave VIOLENCIA DOMÉSTICA (Alta)
    domestic_violence: Set[str] = field(default_factory=lambda: {
        "pareja", "marido", "esposo", "novio", "novia", "ex",
        "golpeó", "pegó", "empujó", "amenazó", "controla",
        "aislamiento", "control coercitivo", "abuso emocional",
        "amenaza", "celos", "me prohibe"
    })
    
    # Palabras clave PROBLEMAS DE SALUD MENTAL (Alta)
    mental_health: Set[str] = field(default_factory=lambda: {
        "depresión", "ansiedad", "pánico", "autolesión", "se corta",
        "trastorno", "adicción", "droga", "alcohol", "cocaína",
        "no puedo más", "crisis de nervios", "ataque de pánico"
    })
    
    # Palabras clave NECESIDAD INMEDIATA (Alta)
    immediate_need: Set[str] = field(default_factory=lambda: {
        "ahora", "ya", "urgente", "rápido", "inmediato", "emergencia",
        "no sé qué hacer", "ayuda", "por favor", "necesito", "desesperada"
    })
    
    # Palabras clave ASESORÍA LEGAL (Media)
    legal_advice: Set[str] = field(default_factory=lambda: {
        "abogado", "demanda", "proceso", "legal", "derecho",
        "denuncia", "sentencia", "juicio", "tribunal",
        "custodia", "pensión", "divorcio", "herencia"
    })
    
    # Palabras clave RECURSOS (Media)
    resources: Set[str] = field(default_factory=lambda: {
        "refugio", "hospedaje", "dinero", "trabajo", "empleo",
        "comida", "vivienda", "medicinas", "psicólogo"
    })

    def detect_urgency(self, text: str) -> tuple[str, List[str]]:
        """
        Detecta nivel de urgencia y keywords encontradas.
        Retorna: (nivel, [keywords_encontradas])
        """
        text_lower = text.lower()
        found_keywords = []
        
        # Buscar en cada categoría (orden de importancia)
        if self._check_keywords(text_lower, self.risk_of_death):
            found_keywords.extend(["RIESGO DE VIDA"])
            return "Muy Alta", found_keywords
        
        if self._check_keywords(text_lower, self.severe_violence):
            found_keywords.extend(["VIOLENCIA SEVERA"])
            if self._check_keywords(text_lower, self.immediate_need):
                return "Muy Alta", found_keywords
            return "Alta", found_keywords
        
        if self._check_keywords(text_lower, self.minors_involved):
            found_keywords.extend(["MENORES INVOLUCRADOS"])
            return "Muy Alta", found_keywords
        
        if self._check_keywords(text_lower, self.sexual_violence):
            found_keywords.extend(["VIOLENCIA SEXUAL"])
            return "Muy Alta", found_keywords
        
        if self._check_keywords(text_lower, self.domestic_violence):
            found_keywords.extend(["VIOLENCIA DOMÉSTICA"])
            return "Alta", found_keywords
        
        if self._check_keywords(text_lower, self.mental_health):
            found_keywords.extend(["SALUD MENTAL"])
            return "Alta", found_keywords
        
        if self._check_keywords(text_lower, self.immediate_need):
            found_keywords.extend(["NECESIDAD INMEDIATA"])
            return "Alta", found_keywords
        
        if self._check_keywords(text_lower, self.legal_advice):
            found_keywords.extend(["ASESORÍA LEGAL"])
            return "Media", found_keywords
        
        if self._check_keywords(text_lower, self.resources):
            found_keywords.extend(["RECURSOS"])
            return "Media", found_keywords
        
        return "Baja", []
    
    @staticmethod
    def _check_keywords(text: str, keywords: Set[str]) -> bool:
        """Verifica si alguna palabra clave está en el texto."""
        for keyword in keywords:
            if keyword in text:
                return True
        return False


@dataclass
class ResponseTemplate:
    """Plantilla de respuesta automática."""
    
    urgency_level: str
    category: str
    template: str
    resources_suggested: List[str] = field(default_factory=list)
    follow_up: str = ""


class TemplateManager:
    """Gestor de plantillas de respuesta."""
    
    def __init__(self):
        self.templates: Dict[str, List[ResponseTemplate]] = {}
        self._init_templates()
    
    def _init_templates(self):
        """Inicializa plantillas por defecto."""
        
        # RIESGO DE VIDA
        self.templates["Muy Alta"] = [
            ResponseTemplate(
                urgency_level="Muy Alta",
                category="suicidio",
                template="""🆘 LÍNEA DE CRISIS DISPONIBLE 24/7

Tu vida es valiosa. Hay personas dispuestas a ayudarte AHORA.

📞 LLAMA INMEDIATAMENTE:
• Línea de Crisis Nacional: 0800-666-7777
• Teleasistencia Emocional: 0800-888-9999
• Hospital de Emergencia más cercano: 911

Tu privacidad está protegida. Nada de lo que digas será compartido sin tu consentimiento.

⏰ Próximos pasos:
1. Llamá ahora a cualquiera de estos números
2. Si no podés hablar, escribí tu ubicación
3. Estamos aquí para ayudarte""",
                resources_suggested=["linea_crisis", "hospital", "psicólogo"]
            ),
            ResponseTemplate(
                urgency_level="Muy Alta",
                category="violencia_severa",
                template="""🚨 ACCIÓN INMEDIATA REQUERIDA

Tu seguridad es lo primero. Esta situación requiere intervención urgente.

📞 LLAMA AHORA:
• Policía (si está en peligro inmediato): 911
• Ambulancia (si hay lesiones): 911
• Línea de Violencia de Género 24/7: 0800-222-8444

🏥 Si tienes lesiones:
- Dirígete al hospital más cercano
- Pide atención de emergencia
- Solicita documentar tus lesiones (protocolo de atención)

📋 Información importante para guardar:
- Guarda esta conversación como prueba
- Toma fotos de lesiones o daños
- Recuerda fechas y horarios de agresiones

⏰ Contactaremos con un abogado de emergencia""",
                resources_suggested=["hospital", "abogado", "refugio"]
            ),
        ]
        
        # VIOLENCIA DOMÉSTICA
        self.templates["Alta"] = [
            ResponseTemplate(
                urgency_level="Alta",
                category="violencia_doméstica",
                template="""⚠️ PLAN DE SEGURIDAD INMEDIATO

Reconocemos que estás en una situación difícil. Aquí hay pasos que puedes tomar:

🛡️ PLAN DE SEGURIDAD:
1. Identifica lugares seguros (casa de amigos/familia)
2. Prepara un bolso de emergencia con documentos
3. Establece una palabra clave con alguien de confianza
4. Guarda números de emergencia ocultos

📞 RECURSOS DISPONIBLES:
• Casa de Tránsito (Refugio 24/7): 0800-555-1234
• Asesoría Legal Gratuita: 0800-333-4444
• Psicólogo especializado: 4111-5555

🏠 Opciones de alojamiento:
Podemos ayudarte a acceder a un refugio seguro y gratuito si es necesario.

⏰ Próximo paso: Conectarte con un profesional especializado""",
                resources_suggested=["refugio", "abogado", "psicólogo"],
                follow_up="¿Necesitas asistencia inmediata para alojamiento seguro?"
            ),
        ]
        
        # ASESORÍA LEGAL
        self.templates["Media"] = [
            ResponseTemplate(
                urgency_level="Media",
                category="legal",
                template="""⚖️ ASESORÍA LEGAL DISPONIBLE

Entendemos que necesitas orientación legal. Podemos conectarte con profesionales.

📋 SERVICIOS LEGALES GRATUITOS:
• Defensoría Pública: 4321-0987
• Asesoría Legal Comunitaria: 0800-333-4444
• Centro de Derechos Humanos: 5678-1234

📄 DOCUMENTACIÓN IMPORTANTE:
- Guarda todos los registros de comunicaciones
- Documenta cualquier incidente con fechas
- Recopila pruebas relevantes

🕐 Disponibilidad:
Lun-Vie: 9:00 - 17:00 hs

Conectaremos tu caso con un abogado dentro de 24 horas.""",
                resources_suggested=["abogado", "defensoría"]
            ),
        ]
        
        logger.info("✅ Plantillas de respuesta inicializadas")
    
    def get_template(self, urgency: str, category: str) -> ResponseTemplate:
        """Obtiene plantilla según urgencia y categoría."""
        templates = self.templates.get(urgency, self.templates.get("Media"))
        if templates:
            return templates[0]  # Retorna la primera plantilla
        return None


class ConfigManager:
    """Gestor central de configuración."""
    
    def __init__(self):
        self.urgency_config = UrgencyConfig()
        self.templates = TemplateManager()
        logger.info("✅ ConfigManager inicializado")
    
    def analyze(self, text: str) -> dict:
        """Analiza texto y retorna configuración completa."""
        urgency, keywords = self.urgency_config.detect_urgency(text)
        template = self.templates.get_template(urgency, "general")
        
        return {
            "urgency": urgency,
            "keywords": keywords,
            "template": template.template if template else "",
            "resources": template.resources_suggested if template else [],
            "follow_up": template.follow_up if template else ""
        }
