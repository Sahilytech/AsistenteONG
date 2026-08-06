"""
Clasificador de casos
Asigna urgencia, tipo, prioridad
"""

import logging
from typing import Dict, Tuple
from enum import Enum

logger = logging.getLogger(__name__)


class Urgency(Enum):
    """Niveles de urgencia."""
    VERY_HIGH = "Muy Alta"
    HIGH = "Alta"
    MEDIUM = "Media"
    LOW = "Baja"


class CaseClassifier:
    """Clasificador de casos."""
    
    def __init__(self):
        """Inicializa el clasificador."""
        self.urgency_keywords = {
            Urgency.VERY_HIGH: [
                "suicidio", "muerte", "morir", "matar", "arma",
                "ahora", "ya", "inmediato", "riesgo de vida"
            ],
            Urgency.HIGH: [
                "agresión", "violencia", "golpe", "atacar", "lesión",
                "amenaza", "peligro", "emergencia"
            ],
            Urgency.MEDIUM: [
                "problema", "conflicto", "dificultad", "preocupación",
                "ansiedad", "estrés"
            ],
            Urgency.LOW: []  # Por defecto si no coincide
        }
        
        self.case_types = {
            "violencia_doméstica": [
                "pareja", "marido", "esposo", "novia", "compañero", "golpe",
                "agresión", "violencia", "doméstica"
            ],
            "violencia_sexual": [
                "violación", "abuso sexual", "acoso", "tocamientos",
                "coerción", "pornografía"
            ],
            "asesoría_legal": [
                "abogado", "ley", "legal", "derecho", "juzgado", "proceso",
                "divorcio", "custodia", "documento"
            ],
            "violencia_infantil": [
                "niño", "niña", "hijo", "hija", "menor", "abuso infantil",
                "negligencia", "maltrato"
            ],
            "violencia_anciano": [
                "anciano", "adulto mayor", "jubilado", "vejez",
                "abuso de anciano", "negligencia"
            ],
            "discriminación": [
                "discriminación", "racismo", "homofobia", "xenofobia",
                "prejuicio", "segregación"
            ],
            "salud_mental": [
                "depresión", "ansiedad", "suicidio", "psicológico",
                "estrés postraumático", "trauma", "fobia"
            ],
            "otro": []
        }
    
    def classify(self, analysis: Dict) -> Dict:
        """Clasifica un caso basado en análisis."""
        logger.info("Clasificando caso...")
        
        # Determinar urgencia
        urgency = self._classify_urgency(analysis)
        
        # Determinar tipo de caso
        case_type = self._classify_case_type(analysis)
        
        # Determinar estado
        status = self._determine_status(urgency)
        
        # Determinar recursos sugeridos
        suggested_resources = self._suggest_resources(
            case_type, urgency, analysis
        )
        
        return {
            "urgency": urgency.value,
            "urgency_score": self._urgency_to_score(urgency),
            "case_type": case_type,
            "status": status,
            "suggested_resources": suggested_resources,
            "requires_immediate_action": urgency in [
                Urgency.VERY_HIGH, Urgency.HIGH
            ],
            "escalate_to": self._determine_escalation(urgency, analysis),
        }
    
    def _classify_urgency(self, analysis: Dict) -> Urgency:
        """Clasifica urgencia del caso."""
        # Comprobar risk factors críticos primero
        risk_factors = analysis.get("risk_factors", [])
        
        critical_risks = [
            "Riesgo suicida", "Presencia de armas",
            "Violencia física documentada"
        ]
        
        if any(risk in str(risk_factors) for risk in critical_risks):
            return Urgency.VERY_HIGH
        
        # Usar score calculado
        urgency_score = analysis.get("urgency_score", 0)
        
        if urgency_score >= 0.90:
            return Urgency.VERY_HIGH
        elif urgency_score >= 0.70:
            return Urgency.HIGH
        elif urgency_score >= 0.40:
            return Urgency.MEDIUM
        else:
            return Urgency.LOW
    
    def _classify_case_type(self, analysis: Dict) -> str:
        """Clasifica tipo de caso."""
        detected_categories = analysis.get("detected_categories", [])
        
        # Mapear categorías a tipos de caso
        mapping = {
            "violencia_fisica": "violencia_doméstica",
            "violencia_psicologica": "violencia_doméstica",
            "violencia_economica": "violencia_doméstica",
            "sexual": "violencia_sexual",
            "menores": "violencia_infantil",
            "adulto_mayor": "violencia_anciano",
        }
        
        for category in detected_categories:
            if category in mapping:
                return mapping[category]
        
        # Si no coincide con violencia, comprobar otros tipos
        text_keywords = analysis.get("keywords_found", {})
        
        for case_type, keywords in self.case_types.items():
            if any(kw in str(text_keywords) for kw in keywords):
                return case_type
        
        return "otro"
    
    def _determine_status(self, urgency: Urgency) -> str:
        """Determina estado inicial del caso."""
        if urgency == Urgency.VERY_HIGH:
            return "pendiente_escalada"
        elif urgency == Urgency.HIGH:
            return "pendiente_atencion"
        else:
            return "nuevo"
    
    def _urgency_to_score(self, urgency: Urgency) -> float:
        """Convierte urgencia a score numérico."""
        mapping = {
            Urgency.VERY_HIGH: 0.95,
            Urgency.HIGH: 0.75,
            Urgency.MEDIUM: 0.50,
            Urgency.LOW: 0.25,
        }
        return mapping[urgency]
    
    def _suggest_resources(self, case_type: str, urgency: Urgency, 
                          analysis: Dict) -> list:
        """Sugiere recursos apropiados."""
        suggestions = []
        
        # Recursos por tipo de caso
        resources_map = {
            "violencia_doméstica": ["refugio", "linea_ayuda", "abogado"],
            "violencia_sexual": ["hospital", "fiscalia", "psicólogo"],
            "asesoría_legal": ["abogado", "consultorio_juridico"],
            "violencia_infantil": ["ddna", "escuela", "psicólogo"],
            "violencia_anciano": ["gerontólogo", "asistente_social"],
            "discriminación": ["defensoría", "ong_dh"],
            "salud_mental": ["psicólogo", "hospital_mental", "linea_crisis"],
        }
        
        type_resources = resources_map.get(case_type, [])
        suggestions.extend(type_resources)
        
        # Recursos por urgencia
        if urgency == Urgency.VERY_HIGH:
            suggestions.insert(0, "emergencias")
        
        # Recursos por riesgos específicos
        risk_factors = analysis.get("risk_factors", [])
        
        if any("menor" in str(r).lower() for r in risk_factors):
            suggestions.append("ddna")
        
        if any("embarazo" in str(r).lower() for r in risk_factors):
            suggestions.append("hospital_obstetricia")
        
        return list(set(suggestions))  # Eliminar duplicados
    
    def _determine_escalation(self, urgency: Urgency, analysis: Dict) -> str:
        """Determina si requiere escalación."""
        if urgency == Urgency.VERY_HIGH:
            risk_factors = analysis.get("risk_factors", [])
            
            if any("suicidio" in str(r) for r in risk_factors):
                return "linea_crisis_urgente"
            elif any("arma" in str(r) for r in risk_factors):
                return "policia"
            else:
                return "supervisor"
        
        elif urgency == Urgency.HIGH:
            return "operador_senior"
        
        return "ninguna"


if __name__ == "__main__":
    classifier = CaseClassifier()
    
    # Caso de prueba
    test_analysis = {
        "urgency_score": 0.95,
        "detected_categories": ["violencia_fisica", "menores", "suicidio"],
        "risk_factors": [
            "Violencia física documentada",
            "Menores involucrados",
            "Riesgo suicida - DERIVACIÓN URGENTE"
        ],
        "keywords_found": {}
    }
    
    classification = classifier.classify(test_analysis)
    print(classification)
