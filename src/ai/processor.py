"""
Procesador principal de IA
Orquesta análisis, clasificación y extracción
"""

import logging
from typing import Dict, Optional
import json
from datetime import datetime

from .model_loader import get_model_loader
from .analyzer import TextAnalyzer
from .classifier import CaseClassifier

logger = logging.getLogger(__name__)


class CaseProcessor:
    """Procesador central de casos con IA."""
    
    def __init__(self):
        """Inicializa el procesador."""
        self.model_loader = get_model_loader()
        self.analyzer = TextAnalyzer()
        self.classifier = CaseClassifier()
        self.model = None
    
    def initialize(self) -> bool:
        """Inicializa el modelo IA."""
        logger.info("Inicializando procesador...")
        
        if self.model_loader.load_model("gemma-3-1b"):
            self.model = self.model_loader.get_model()
            logger.info("✅ Procesador listo")
            return True
        else:
            logger.warning("⚠️ Modelo no disponible, usando análisis local")
            return False
    
    def process_case(self, case_text: str) -> Dict:
        """Procesa un caso completo."""
        logger.info("Procesando caso...")
        
        try:
            # 1. Análisis de texto
            logger.info("Analizando texto...")
            analysis = self.analyzer.analyze(case_text)
            
            # 2. Clasificación
            logger.info("Clasificando caso...")
            classification = self.classifier.classify(analysis)
            
            # 3. Generar resumen
            logger.info("Generando resumen...")
            summary = self.analyzer.summarize(case_text)
            
            # 4. Generar respuesta borrador
            logger.info("Generando respuesta...")
            draft_response = self._generate_response(
                analysis, classification, case_text
            )
            
            # 5. Compilar resultado
            result = {
                "timestamp": datetime.now().isoformat(),
                "original_text": case_text[:500],  # Primeras 500 chars
                "summary": summary,
                "analysis": analysis,
                "classification": classification,
                "suggested_response": draft_response,
                "confidence": self._calculate_confidence(analysis),
            }
            
            logger.info("✅ Caso procesado exitosamente")
            return result
            
        except Exception as e:
            logger.error(f"Error procesando caso: {e}")
            return {"error": str(e), "status": "failed"}
    
    def _generate_response(self, analysis: Dict, classification: Dict,
                          case_text: str) -> str:
        """Genera una respuesta borrador."""
        response = "Gracias por comunicarte con nosotros.\n\n"
        
        # Confirmación de recibida
        response += "✅ Recibimos tu mensaje y lo estamos analizando.\n\n"
        
        # Aviso de peligro inmediato
        if classification.get("urgency") == "Muy Alta":
            response += "⚠️ IMPORTANTE: Si existe peligro inmediato, "
            response += "comunícate con emergencias (911 u otro según tu país).\n\n"
        
        # Tipo de apoyo
        case_type = classification.get("case_type", "otro")
        if case_type != "otro":
            response += f"📌 Identificamos tu consulta como: {case_type.replace('_', ' ').title()}\n\n"
        
        # Recursos sugeridos
        resources = classification.get("suggested_resources", [])
        if resources:
            response += "🔗 Recursos que pueden ayudarte:\n"
            for resource in resources[:3]:  # Primeros 3
                response += f"  • {resource.replace('_', ' ').title()}\n"
            response += "\n"
        
        # Próximos pasos
        response += "📋 Próximos pasos:\n"
        response += "1. Un operador capacitado revisará tu caso\n"
        response += "2. Te contactaremos con orientación específica\n"
        response += "3. Te derivaremos a recursos apropiados si es necesario\n\n"
        
        response += "Estamos aquí para ayudarte. Tu privacidad es nuestra prioridad."
        
        return response
    
    def _calculate_confidence(self, analysis: Dict) -> float:
        """Calcula confianza del análisis."""
        factors = []
        
        # Factor 1: Categorías detectadas
        categories = len(analysis.get("detected_categories", []))
        factors.append(min(categories / 3, 1.0))  # Máx 3 categorías
        
        # Factor 2: Palabras clave encontradas
        keywords = analysis.get("keywords_found", {})
        total_keywords = sum(len(v) for v in keywords.values())
        factors.append(min(total_keywords / 10, 1.0))  # Máx 10 palabras
        
        # Factor 3: Urgency score
        urgency = analysis.get("urgency_score", 0)
        factors.append(0.5 + (urgency * 0.5))  # Rango 0.5-1.0
        
        # Promediar
        confidence = sum(factors) / len(factors) if factors else 0.5
        
        return min(confidence, 1.0)
    
    def batch_process(self, cases: list) -> list:
        """Procesa múltiples casos."""
        results = []
        for i, case_text in enumerate(cases):
            logger.info(f"Procesando caso {i+1}/{len(cases)}")
            result = self.process_case(case_text)
            results.append(result)
        
        return results


# Instancia global
_processor: Optional[CaseProcessor] = None


def get_processor() -> CaseProcessor:
    """Obtiene la instancia global del procesador."""
    global _processor
    if _processor is None:
        _processor = CaseProcessor()
    return _processor


def initialize_processor() -> bool:
    """Inicializa el procesador global."""
    processor = get_processor()
    return processor.initialize()


if __name__ == "__main__":
    processor = get_processor()
    processor.initialize()
    
    test_case = """
    Hola, hace dos semanas mi pareja me golpeó frente a mis hijos.
    Tengo moretones y miedo de volver a casa. No sé qué hacer,
    tengo dos niños de 5 y 8 años. Me amenazó con un cuchillo.
    """
    
    result = processor.process_case(test_case)
    print(json.dumps(result, indent=2, ensure_ascii=False))
