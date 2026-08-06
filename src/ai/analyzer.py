"""
Analizador de casos usando IA
Extrae información, emociones, riesgos
"""

import logging
import re
from typing import Dict, List, Tuple
import json

logger = logging.getLogger(__name__)

# Palabras clave por categoría
KEYWORDS = {
    "violencia_fisica": [
        "golpe", "golpeó", "pegó", "puñetazo", "abofeteo", "agredir", "atacar",
        "lesión", "herida", "moretón", "fractura", "golpiza"
    ],
    "violencia_psicologica": [
        "insulto", "amenaza", "manipulación", "control", "humillación", "aislamiento",
        "culpa", "vergüenza", "intimidación", "chantaje", "desprecio"
    ],
    "violencia_economica": [
        "dinero", "dinero", "gasto", "pago", "deuda", "embargo", "despido",
        "empleo", "salario", "económico", "pobreza", "hambre"
    ],
    "sexual": [
        "abuso sexual", "violación", "acoso", "tocamientos", "pornografía",
        "explotación", "coerción", "consentimiento"
    ],
    "menores": [
        "niño", "niña", "hijo", "hija", "bebé", "menor", "infancia", "adolescente",
        "escuela", "guardería", "desarrollo"
    ],
    "embarazo": [
        "embarazada", "embarazo", "gestación", "parto", "aborto", "feto", "bebé"
    ],
    "suicidio": [
        "suicidio", "matar", "muerte", "morir", "desaparecer", "huir", "huída",
        "final", "irme", "acabar", "terminar"
    ],
    "armas": [
        "arma", "pistola", "cuchillo", "revólver", "navaja", "bomba", "explosivo"
    ],
    "adulto_mayor": [
        "anciano", "adulto mayor", "jubilado", "vejez", "viejo", "abuelo",
        "edad avanzada", "pensión"
    ],
    "discapacidad": [
        "discapacidad", "discapacitado", "impedimento", "limitación", "sordera",
        "ceguera", "movilidad", "silla de ruedas"
    ],
    "migracion": [
        "migrante", "inmigrante", "refugiado", "asilo", "extranjero", "documentos",
        "visa", "pasaporte", "deportación"
    ]
}

# Emociones
EMOTIONS = {
    "miedo": ["miedo", "asustado", "aterrado", "pánico", "fobia", "angustia"],
    "tristeza": ["triste", "deprimido", "melancólico", "llorar", "lloro", "dolor"],
    "rabia": ["enojado", "furioso", "ira", "resentimiento", "odio", "rencor"],
    "vergüenza": ["avergonzado", "humillación", "vergüenza", "culpa"],
    "desesperanza": ["desesperado", "sin esperanza", "inútil", "fracaso"],
}


class TextAnalyzer:
    """Analizador de texto para casos."""
    
    def __init__(self):
        """Inicializa el analizador."""
        self.keywords = KEYWORDS
        self.emotions = EMOTIONS
    
    def analyze(self, text: str) -> Dict:
        """Analiza un caso de texto."""
        logger.info("Analizando texto...")
        
        text_lower = text.lower()
        
        return {
            "original_length": len(text),
            "detected_categories": self._detect_categories(text_lower),
            "detected_emotions": self._detect_emotions(text_lower),
            "detected_people": self._extract_people(text),
            "urgency_score": self._calculate_urgency(text_lower),
            "risk_factors": self._extract_risk_factors(text_lower),
            "keywords_found": self._extract_keywords(text_lower),
        }
    
    def _detect_categories(self, text: str) -> List[str]:
        """Detecta categorías de casos."""
        detected = []
        
        for category, keywords in self.keywords.items():
            if any(kw in text for kw in keywords):
                detected.append(category)
        
        return detected
    
    def _detect_emotions(self, text: str) -> List[str]:
        """Detecta emociones."""
        detected = []
        
        for emotion, keywords in self.emotions.items():
            count = sum(1 for kw in keywords if kw in text)
            if count > 0:
                detected.append({"emotion": emotion, "mentions": count})
        
        return sorted(detected, key=lambda x: x["mentions"], reverse=True)
    
    def _extract_people(self, text: str) -> List[str]:
        """Extrae personas mencionadas."""
        people = []
        
        # Palabras que indican relación
        relations = {
            "pareja": ["novio", "novia", "esposo", "esposa", "marido", "compañero"],
            "padre": ["padre", "papá", "padrastro"],
            "madre": ["madre", "mamá", "madrastra"],
            "hijo": ["hijo", "hija", "niño", "niña"],
            "hermano": ["hermano", "hermana", "hermanastro"],
            "otro": ["amigo", "jefe", "jefa", "vecino", "profesor"]
        }
        
        for relation, keywords in relations.items():
            if any(kw in text.lower() for kw in keywords):
                people.append(relation)
        
        return list(set(people))
    
    def _calculate_urgency(self, text: str) -> float:
        """Calcula score de urgencia (0-1)."""
        urgency_indicators = {
            "muy_alta": [
                "suicidio", "muerte", "morir", "matar", "arma", "bomba",
                "inmediato", "ahora", "ya", "emergencia", "urgente"
            ],
            "alta": [
                "agresión", "violencia", "ataque", "golpe", "lesión",
                "amenaza", "peligro"
            ],
            "media": [
                "problema", "conflicto", "dificultad", "preocupación"
            ]
        }
        
        score = 0.0
        
        if any(kw in text for kw in urgency_indicators["muy_alta"]):
            score = 0.95
        elif any(kw in text for kw in urgency_indicators["alta"]):
            score = 0.75
        elif any(kw in text for kw in urgency_indicators["media"]):
            score = 0.50
        else:
            score = 0.25
        
        return min(score, 1.0)
    
    def _extract_risk_factors(self, text: str) -> List[str]:
        """Extrae factores de riesgo."""
        risks = []
        
        # Mapeo de categorías a factores de riesgo
        risk_mapping = {
            "violencia_fisica": "Violencia física documentada",
            "violencia_psicologica": "Abuso emocional/psicológico",
            "sexual": "Abuso sexual",
            "menores": "Menores involucrados",
            "embarazo": "Embarazo en riesgo",
            "suicidio": "Riesgo suicida - DERIVACIÓN URGENTE",
            "armas": "Presencia de armas",
            "adulto_mayor": "Adulto mayor vulnerable",
            "discapacidad": "Persona con discapacidad",
            "migracion": "Situación migratoria vulnerable"
        }
        
        for category, risk_text in risk_mapping.items():
            if category in self._detect_categories(text):
                risks.append(risk_text)
        
        return risks
    
    def _extract_keywords(self, text: str) -> Dict[str, List[str]]:
        """Extrae palabras clave encontradas."""
        found = {}
        
        for category, keywords in self.keywords.items():
            found_in_cat = [kw for kw in keywords if kw in text]
            if found_in_cat:
                found[category] = found_in_cat
        
        return found
    
    def summarize(self, text: str, max_length: int = 150) -> str:
        """Crea un resumen del caso."""
        # Versión simple: primeras oraciones
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        summary = ""
        for sentence in sentences:
            if len(summary) + len(sentence) < max_length:
                summary += sentence + ". "
            else:
                break
        
        return summary.strip()


if __name__ == "__main__":
    analyzer = TextAnalyzer()
    
    test_case = """
    Mi pareja me golpeó ayer. Tengo moretones en los brazos.
    También me amenazó con un cuchillo. Tengo miedo de volver a casa.
    No sé qué hacer, tengo dos hijos pequeños.
    """
    
    analysis = analyzer.analyze(test_case)
    print(json.dumps(analysis, indent=2, ensure_ascii=False))
