"""
Clasificador de casos - Usa el motor hibrido
"""

import logging
from typing import Dict, List

from .processor import get_processor

logger = logging.getLogger(__name__)

# Mapeo de categorias a tipos de caso
CATEGORY_MAP = {
    "salud": "Salud/Emergencia medica",
    "legal": "Asesoria legal",
    "violencia_domestica": "Violencia domestica",
    "menores": "Proteccion de menores",
    "salud_mental": "Salud mental",
    "recursos": "Recursos basicos",
    "discriminacion": "Discriminacion/Derechos",
    "general": "General"
}

URGENCY_MAP = {
    "Muy Alta": "CRITICA - Intervencion inmediata",
    "Alta": "ALTA - Atencion prioritaria",
    "Media": "MEDIA - Atencion programada",
    "Baja": "BAJA - Seguimiento rutinario"
}


class CaseClassifier:
    """Clasificador de casos usando motor hibrido."""

    def __init__(self):
        self.processor = get_processor()
        logger.info("✅ CaseClassifier inicializado")

    def classify(self, text: str) -> Dict:
        """Clasifica un caso y retorna resultado estructurado."""
        analysis = self.processor.analyze(text)

        category = analysis.get("category", "general")
        urgency = analysis.get("urgency", "Media")

        return {
            "category": category,
            "category_label": CATEGORY_MAP.get(category, "General"),
            "urgency": urgency,
            "urgency_label": URGENCY_MAP.get(urgency, "Media"),
            "keywords": analysis.get("keywords", []),
            "summary": analysis.get("summary", ""),
            "confidence": analysis.get("confidence", 0.5),
            "source": analysis.get("source", "reglas")
        }

    def get_categories(self) -> List[str]:
        """Retorna lista de categorias disponibles."""
        return list(CATEGORY_MAP.values())

    def get_urgency_levels(self) -> List[str]:
        """Retorna niveles de urgencia."""
        return list(URGENCY_MAP.values())


def classify_case(text: str) -> Dict:
    """Funcion de conveniencia."""
    classifier = CaseClassifier()
    return classifier.classify(text)


if __name__ == "__main__":
    classifier = CaseClassifier()
    test = "Tengo una alergia grave al mani"
    result = classifier.classify(test)
    print(f"Categoria: {result['category_label']}")
    print(f"Urgencia: {result['urgency_label']}")
