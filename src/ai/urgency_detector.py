"""
Detector de urgencia - Delega a ConfigManager (motor de reglas)
Mantiene compatibilidad con codigo existente
"""

import logging
from typing import Tuple, List

from ..config_manager import ConfigManager

logger = logging.getLogger(__name__)


class UrgencyDetector:
    """Detector de urgencia que usa ConfigManager."""

    def __init__(self):
        self.config_manager = ConfigManager()
        logger.info("✅ UrgencyDetector inicializado")

    def detect(self, text: str) -> Tuple[str, List[str]]:
        """
        Detecta nivel de urgencia y palabras clave.

        Args:
            text: Texto del caso

        Returns:
            Tuple[str, List[str]]: (nivel_urgencia, palabras_clave)
        """
        try:
            analysis = self.config_manager.analyze(text)
            urgency = analysis.get("urgency", "Baja")
            keywords = analysis.get("keywords", [])

            logger.info(f"🔍 Urgencia detectada: {urgency}")
            return urgency, keywords

        except Exception as e:
            logger.error(f"Error detectando urgencia: {e}")
            return "Baja", []

    def get_urgency_level(self, text: str) -> str:
        """Retorna solo el nivel de urgencia."""
        urgency, _ = self.detect(text)
        return urgency

    def get_keywords(self, text: str) -> List[str]:
        """Retorna solo las palabras clave."""
        _, keywords = self.detect(text)
        return keywords


def detect_urgency(text: str) -> Tuple[str, List[str]]:
    """Funcion de conveniencia."""
    detector = UrgencyDetector()
    return detector.detect(text)


if __name__ == "__main__":
    detector = UrgencyDetector()

    test_cases = [
        "Tengo una alergia grave al mani",
        "Mi pareja me golpea",
        "Necesito un abogado",
        "No tengo trabajo"
    ]

    for case in test_cases:
        urgency, keywords = detector.detect(case)
        print(f"\nCaso: {case}")
        print(f"  Urgencia: {urgency}")
        print(f"  Keywords: {keywords}")
