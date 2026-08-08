"""
Analizador de casos - Usa el motor hibrido (IA + reglas)
"""

import logging
from typing import Dict, List, Optional

from .processor import get_processor, analyze_case

logger = logging.getLogger(__name__)


class CaseAnalyzer:
    """Analizador de casos que delega al motor hibrido."""

    def __init__(self):
        self.processor = get_processor()
        logger.info("✅ CaseAnalyzer inicializado")

    def analyze(self, text: str) -> Dict:
        """Analiza un caso y retorna resultado estructurado."""
        logger.info(f"🔍 Analizando caso: {text[:50]}...")

        result = self.processor.analyze(text)

        logger.info(f"✅ Analisis completado: {result.get('urgency', 'Desconocida')} - {result.get('category', 'general')}")
        return result

    def get_status(self) -> Dict:
        """Retorna estado del analizador."""
        return self.processor.get_status()

    def analyze_batch(self, texts: List[str]) -> List[Dict]:
        """Analiza multiples casos."""
        results = []
        for text in texts:
            results.append(self.analyze(text))
        return results


def analyze(text: str) -> Dict:
    """Funcion de conveniencia para analizar un caso."""
    analyzer = CaseAnalyzer()
    return analyzer.analyze(text)


if __name__ == "__main__":
    # Test
    test_cases = [
        "Tengo una alergia grave al mani y no se que hacer",
        "Mi pareja me golpea y tengo miedo",
        "Necesito un abogado para una custodia",
        "No tengo trabajo ni comida para mis hijos"
    ]

    analyzer = CaseAnalyzer()
    for case in test_cases:
        result = analyzer.analyze(case)
        print(f"\nCaso: {case[:40]}...")
        print(f"  Categoria: {result['category']}")
        print(f"  Urgencia: {result['urgency']}")
        print(f"  Fuente: {result['source']}")
