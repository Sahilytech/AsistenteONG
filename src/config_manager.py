"""
Gestor de configuración - Palabras clave expandidas, plantillas, urgencia
+200 palabras clave en 9 categorías
"""

from dataclasses import dataclass, field
from typing import Dict, List, Set
import json
import logging

logger = logging.getLogger(__name__)


@dataclass
class UrgencyConfig:
    """Configuración de detectores de urgencia - EXPANDIDA."""
    
    # 🔴 RIESGO DE VIDA (Muy Alta) - +40 palabras clave
    risk_of_death: Set[str] = field(default_factory=lambda: {
        # Suicidio
        "suicidio", "me voy a matar", "no quiero vivir", "quiero morir",
        "intento de suicidio", "suicidarme", "suicida", "suicidas",
        "ahorcarse", "ahorcado", "cuerda", "veneno", "venenos",
        "sobredosis", "sobredosis de", "pastillas", "medicamentos",
        "tirarme", "acantilado", "puente", "arrojarse",
        "terminar con mi vida", "no soporto", "no aguanto más",
        "me quiero morir", "pensamiento suicida", "ideación suicida",
        "plan de suicidio", "intento suicida", "riesgo inmediato",
        "riesgo de vida", "peligro de muerte", "riesgo mortales",
        # Armas
        "arma", "armas", "revolver", "pistola", "cuchillo",
        "escopeta", "rifle", "ballesta", "navaja", "hacha",
        "muerte", "morir", "matar", "asesinato"
    })
    
    # 🔴 VIOLENCIA SEVERA (Muy Alta) - +50 palabras clave
    severe_violence: Set[str] = field(default_factory=lambda: {
        "violencia", "violencias", "violento", "violenta",
        "golpeada", "golpeado", "golpes", "golpean", "golpeador",
        "pegadas", "pegado", "pegar", "pegó", "pegaba",
        "empujada", "empujado", "empujó", "empujadas",
        "fractura", "fracturas", "fracturada", "fracturado",
        "sangre", "sangrado", "sangraba", "sangrante",
        "herida", "heridas", "herida grave", "herido",
        "lesión", "lesiones", "lesionada", "lesionado",
        "hueso roto", "rotura", "trauma", "traumático",
        "paliza", "palizas", "apaleada", "apaleado",
        "puñetazos", "puñetazo", "bofetadas", "bofetada",
        "patadas", "patada", "pataleada", "pateada",
        "hospital", "emergencia", "urgencias", "hospitalización",
        "ataque", "atacada", "atacado", "agresión", "agredida",
        "abuso", "abusada", "abusado", "abusador",
        "maltrato", "maltratada", "maltratado", "maltratos",
        "tortura", "torturada", "torturado", "torturas",
        "privación", "encierro", "encerrada", "encerrado",
        "cautiverio", "retenida", "retenido", "retención"
    })
    
    # 🔴 MENORES INVOLUCRADOS (Muy Alta) - +40 palabras clave
    minors_involved: Set[str] = field(default_factory=lambda: {
        "niño", "niña", "niños", "niñas", "menor", "menores",
        "hijo", "hija", "hijos", "hijas",
        "bebé", "bebés", "lactante", "lactantes",
        "infancia", "infante", "infantes",
        "adolescente", "adolescentes", "pre-adolescente",
        "criatura", "criaturas", "pequeño", "pequeña",
        "abuso infantil", "abuso de menores", "abuso sexual infantil",
        "explotación infantil", "explotación sexual infantil",
        "tocamientos", "tocamiento inapropiado", "contacto inapropiado",
        "pederastia", "pedófilo", "pedófila",
        "violación de menores", "violado", "violada",
        "pornografía infantil", "material sexual infantil",
        "grooming", "ciberacoso", "acoso infantil",
        "maltrato infantil", "maltrato de niños",
        "negligencia infantil", "abandono de menores",
        "trata de menores", "tráfico de menores",
        "sustracción de menores", "secuestro de menores",
        "riesgo de menores", "en peligro", "desprotección"
    })
    
    # 🔴 VIOLENCIA SEXUAL (Muy Alta) - +45 palabras clave
    sexual_violence: Set[str] = field(default_factory=lambda: {
        "violación", "violada", "violado", "violar",
        "violadas", "violados", "violador", "violadora",
        "abuso sexual", "abusada", "abusado", "abusador",
        "agresión sexual", "agredida sexualmente",
        "coerción sexual", "coerción", "coerced",
        "acoso sexual", "acosada", "acosador",
        "sexo forzado", "relación forzada", "tocamientos forzados",
        "violencia sexual", "agresor sexual",
        "pasó algo sexual", "algo sexual pasó",
        "me obligó", "me obligaron", "me forzó", "me forzaron",
        "sexo sin consentimiento", "sin querer", "sin consentir",
        "penetración no consentida", "contacto no consentido",
        "toqueteo", "sobaje", "manoseo", "manoseada",
        "exhibicionismo", "voyeurismo", "acto obsceno",
        "grooming sexual", "seducción", "seducida",
        "proxenetismo", "prostitución forzada",
        "trata con fines sexuales", "explotación sexual",
        "violación marital", "violación de pareja",
        "violación en cita", "violación en fiesta",
        "drogas y sexo", "drogas para abuso"
    })
    
    # 🟠 VIOLENCIA DOMÉSTICA (Alta) - +50 palabras clave
    domestic_violence: Set[str] = field(default_factory=lambda: {
        "pareja", "parejas", "ex pareja", "expareja",
        "marido", "maridos", "esposo", "esposos",
        "novio", "novios", "novia", "novias",
        "ex novio", "ex novia", "ex",
        "conviviente", "concubino",
        "golpeó", "golpea", "golpean", "pegó", "pega",
        "empujó", "empuja", "empujan", "empujada",
        "amenazó", "amenaza", "amenazas", "amenazador",
        "controla", "controlada", "controlador", "control",
        "aislamiento", "aislada", "aislado", "aislar",
        "control coercitivo", "coerción", "coercitivo",
        "abuso emocional", "abuso psicológico", "abuso verbal",
        "humillación", "humillada", "humillaciones",
        "insultos", "insulta", "insultan", "insultada",
        "menosprecia", "menosprecia", "menosprecio",
        "celos", "celoso", "celosa", "extremadamente celoso",
        "sospecha", "desconfianza", "vigilancia",
        "me prohibe", "prohibición", "impide",
        "me aísla", "me aisló", "aislamiento forzado",
        "amenaza de abandono", "amenaza de llevarse a los hijos",
        "violencia económica", "control del dinero",
        "deuda", "endeudada", "endeudado",
        "daño de propiedad", "rompe cosas", "destruye",
        "amenaza a familiares", "amenaza a hijos",
        "comportamiento agresivo", "arrebatos", "explosiones",
        "ciclo de violencia", "luna de miel", "tensión acumulada",
        "no para de pelear", "constantemente pelea",
        "demanda de atención", "demandante", "controlador"
    })
    
    # 🟠 SALUD MENTAL (Alta) - +40 palabras clave
    mental_health: Set[str] = field(default_factory=lambda: {
        "depresión", "deprimida", "deprimido", "depresivo",
        "ansiedad", "ansiosa", "ansioso", "ansiedades",
        "pánico", "ataque de pánico", "ataques de pánico",
        "estrés", "estresada", "estresado",
        "crisis nerviosa", "crisis de nervios", "ataque nervioso",
        "autolesión", "autolesiones", "se corta", "cortarse",
        "me corto", "me quemo", "me golpeo",
        "trastorno", "trastornos", "trastornada",
        "bipolar", "esquizofrenia", "psicosis",
        "adicción", "adicta", "adicto", "adiciones",
        "droga", "drogas", "drogadicta", "drogadicto",
        "alcohol", "alcoholismo", "alcohólica", "alcohólico",
        "cocaína", "heroína", "metanfetamina", "LSD",
        "marihuana", "cannabis", "sustancia", "sustancias",
        "no puedo más", "no aguanto", "no soporto",
        "tristeza", "tristísima", "tristísimo",
        "desesperación", "desesperada", "desesperado",
        "soledad", "sola", "solo", "aislamiento",
        "falta de motivación", "sin ganas", "sin ánimo",
        "insomnio", "no duermo", "duermo poco",
        "pesadillas", "pesadilla", "sueños malos",
        "falta de apetito", "como poco", "no como",
        "ideación suicida", "pensamiento suicida",
        "trauma", "traumatizada", "traumatizado",
        "TEPT", "estrés postraumático"
    })
    
    # 🟠 NECESIDAD INMEDIATA (Alta) - +30 palabras clave
    immediate_need: Set[str] = field(default_factory=lambda: {
        "ahora", "ahorita", "ya", "urgente", "urgencia",
        "rápido", "rápida", "rapidísimo", "lo antes posible",
        "inmediato", "inmediatamente", "inmediate",
        "emergencia", "emergencias", "es emergencia",
        "no sé qué hacer", "no sé cómo seguir", "estoy perdida",
        "ayuda", "ayudenme", "ayúdenme", "por favor",
        "necesito", "necesito ayuda", "necesito urgente",
        "desesperada", "desesperado", "en crisis",
        "SOS", "auxilio", "MAYDAY", "emergencia médica",
        "me muero", "me estoy muriendo", "voy a morir",
        "es grave", "muy grave", "gravísimo",
        "no puedo más", "ya no puedo", "estoy al límite",
        "en peligro", "en riesgo", "en peligro ahora",
        "sangrado", "hemorragia", "pérdida de conciencia",
        "inconsciente", "desmayada", "convulsiones"
    })
    
    # 🟡 ASESORÍA LEGAL (Media) - +35 palabras clave
    legal_advice: Set[str] = field(default_factory=lambda: {
        "abogado", "abogada", "abogados", "legal",
        "demanda", "demandar", "demandada", "demandado",
        "proceso", "procesos", "procesal",
        "derecho", "derechos", "derecha",
        "denuncia", "denunciar", "denunciada", "denunciado",
        "sentencia", "sentenciada", "sentenciado",
        "juicio", "juicios", "juzgado",
        "tribunal", "corte", "cortes",
        "abogacía gratuita", "asesor legal",
        "custodia", "custodia de menores", "batalla por custodia",
        "pensión", "alimentos", "manutención",
        "divorcio", "divorciada", "divorciado", "divorciarse",
        "separación", "separada", "separado",
        "herencia", "herencias", "testamento",
        "propiedad", "vivienda", "casa", "terreno",
        "contrato", "contratos", "contratación",
        "acuerdo", "acuerdos", "acuerdo de separación",
        "deuda", "deudas", "endeudamiento",
        "embargo", "embargada", "embargado",
        "desalojo", "desalojada", "desalojado",
        "protección de orden", "orden de protección",
        "antecedentes penales", "antecedentes",
        "compensación", "indemnización"
    })
    
    # 🟡 RECURSOS (Media) - +35 palabras clave
    resources: Set[str] = field(default_factory=lambda: {
        "refugio", "refugios", "alojamiento", "albergue",
        "hospedaje", "posada", "asilo",
        "dinero", "dineros", "recursos económicos",
        "trabajo", "empleo", "empleos", "desempleo",
        "sin trabajo", "sin empleo", "desempleada",
        "comida", "alimento", "alimentos", "hambre",
        "casa", "vivienda", "hogar", "techo",
        "medicinas", "medicamentos", "médico",
        "doctor", "doctora", "hospital", "clínica",
        "psicólogo", "psicóloga", "terapia", "psicoterapia",
        "psiquiatra", "psiquiatría",
        "educación", "escuela", "colegio", "universidad",
        "documentos", "cédula", "partida", "identidad",
        "papeles", "documentación", "DNI", "pasaporte",
        "vivienda de emergencia", "casa de tránsito",
        "ropa", "ropas", "vestimenta",
        "transporte", "pasaje", "movilidad",
        "celular", "teléfono", "comunicación",
        "internet", "conectividad", "acceso digital",
        "guardería", "cuidado de niños",
        "capacitación", "entrenamiento", "curso"
    })

    def detect_urgency(self, text: str) -> tuple[str, List[str]]:
        """Detecta urgencia y keywords."""
        text_lower = text.lower()
        found_keywords = []
        
        # Buscar por orden de importancia
        if self._check_keywords(text_lower, self.risk_of_death):
            found_keywords.extend(["🔴 RIESGO DE VIDA"])
            return "Muy Alta", found_keywords
        
        if self._check_keywords(text_lower, self.severe_violence):
            found_keywords.extend(["🔴 VIOLENCIA SEVERA"])
            if self._check_keywords(text_lower, self.immediate_need):
                return "Muy Alta", found_keywords
            return "Alta", found_keywords
        
        if self._check_keywords(text_lower, self.minors_involved):
            found_keywords.extend(["🔴 MENORES INVOLUCRADOS"])
            return "Muy Alta", found_keywords
        
        if self._check_keywords(text_lower, self.sexual_violence):
            found_keywords.extend(["🔴 VIOLENCIA SEXUAL"])
            return "Muy Alta", found_keywords
        
        if self._check_keywords(text_lower, self.domestic_violence):
            found_keywords.extend(["🟠 VIOLENCIA DOMÉSTICA"])
            return "Alta", found_keywords
        
        if self._check_keywords(text_lower, self.mental_health):
            found_keywords.extend(["🟠 SALUD MENTAL"])
            return "Alta", found_keywords
        
        if self._check_keywords(text_lower, self.immediate_need):
            found_keywords.extend(["🟠 NECESIDAD INMEDIATA"])
            return "Alta", found_keywords
        
        if self._check_keywords(text_lower, self.legal_advice):
            found_keywords.extend(["🟡 ASESORÍA LEGAL"])
            return "Media", found_keywords
        
        if self._check_keywords(text_lower, self.resources):
            found_keywords.extend(["🟡 RECURSOS"])
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
        ]
        
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

⏰ Próximo paso: Conectarte con un profesional especializado""",
                resources_suggested=["refugio", "abogado", "psicólogo"]
            ),
        ]
        
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

Conectaremos tu caso con un abogado dentro de 24 horas.""",
                resources_suggested=["abogado", "defensoría"]
            ),
        ]
        
        logger.info("✅ Plantillas inicializadas")
    
    def get_template(self, urgency: str, category: str) -> ResponseTemplate:
        """Obtiene plantilla según urgencia y categoría."""
        templates = self.templates.get(urgency, self.templates.get("Media", []))
        if templates:
            return templates[0]
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
