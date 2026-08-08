"""
Motor de procesamiento híbrido:
- IA local (llama.cpp) cuando está disponible
- Motor de reglas (keywords) como fallback
- Siempre funciona offline
- Optimizado para PCs de bajos recursos
"""

import logging
from typing import Dict, List, Optional
import json

from .model_loader import get_model_loader, ModelLoader
from ..config_manager import ConfigManager

logger = logging.getLogger(__name__)


class HybridProcessor:
    """
    Procesador híbrido que usa IA cuando puede, reglas cuando no.
    Funciona en PCs de bajos recursos (Sarmiento) y en PCs modernas.
    """

    def __init__(self):
        self.model_loader = get_model_loader()
        self.config_manager = ConfigManager()
        self.use_ai = False
        self._try_load_model()

    def _try_load_model(self):
        """Intenta cargar modelo IA. Si falla, usa reglas."""
        try:
            if self.model_loader.is_model_available("gemma-3-1b"):
                success = self.model_loader.load_model("gemma-3-1b")
                self.use_ai = success
                if success:
                    logger.info("🧠 IA local activada (Gemma 3 1B)")
                else:
                    logger.info("⚙️ Modo reglas activado (sin IA)")
            elif self.model_loader.is_model_available("tinyllama"):
                success = self.model_loader.load_model("tinyllama")
                self.use_ai = success
                if success:
                    logger.info("🧠 IA local activada (TinyLlama)")
                else:
                    logger.info("⚙️ Modo reglas activado (sin IA)")
            else:
                logger.info("⚙️ Modo reglas activado (sin IA local)")
                logger.info("💡 Descargá un modelo en la pestaña Configuracion > IA")
        except Exception as e:
            logger.warning(f"No se pudo cargar IA: {e}")
            self.use_ai = False

    def analyze(self, text: str) -> Dict:
        """
        Analiza un caso usando IA o reglas.
        Siempre retorna resultado, nunca falla.
        """
        try:
            if self.use_ai:
                return self._analyze_with_ai(text)
            else:
                return self._analyze_with_rules(text)
        except Exception as e:
            logger.error(f"Error en analisis: {e}")
            return self._analyze_with_rules(text)  # Fallback seguro

    def _analyze_with_ai(self, text: str) -> Dict:
        """Analiza usando IA local (llama.cpp)."""
        try:
            prompt = f"""Analiza el siguiente caso de una linea de ayuda social.

TEXTO DEL CASO:
{text}

Responde UNICAMENTE con un JSON valido en este formato exacto:
{{
    "category": "categoria_principal",
    "urgency": "Muy Alta|Alta|Media|Baja",
    "summary": "resumen breve del caso en 2-3 oraciones",
    "keywords": ["palabra1", "palabra2"],
    "missing_info": ["info que falta"],
    "suggested_actions": ["accion1", "accion2"],
    "confidence": 0.85
}}

Categorias posibles: salud, legal, violencia_domestica, menores, recursos, salud_mental, discriminacion, general.
"""

            result = self.model_loader.generate_json(prompt, max_tokens=512)

            # Validar resultado
            if "error" in result:
                logger.warning(f"IA devolvio error, usando reglas: {result['error']}")
                return self._analyze_with_rules(text)

            # Asegurar campos requeridos
            return {
                "category": result.get("category", "general"),
                "urgency": result.get("urgency", "Media"),
                "summary": result.get("summary", "No se pudo generar resumen"),
                "keywords": result.get("keywords", []),
                "missing_info": result.get("missing_info", []),
                "suggested_actions": result.get("suggested_actions", []),
                "confidence": result.get("confidence", 0.5),
                "source": "ia_local"
            }

        except Exception as e:
            logger.error(f"Error en analisis IA: {e}")
            return self._analyze_with_rules(text)

    def _analyze_with_rules(self, text: str) -> Dict:
        """Analiza usando motor de reglas (keywords)."""
        analysis = self.config_manager.analyze(text)

        return {
            "category": self._detect_category(text),
            "urgency": analysis.get("urgency", "Media"),
            "summary": self._generate_summary(text),
            "keywords": analysis.get("keywords", []),
            "missing_info": ["Informacion de contacto", "Ubicacion", "Edad"],
            "suggested_actions": ["Revisar caso manualmente", "Consultar recursos disponibles"],
            "confidence": 0.6,
            "source": "reglas"
        }

    def _detect_category(self, text: str) -> str:
        """Detecta categoria por keywords."""
        text_lower = text.lower()

        categories = {
            "salud": ["alergia", "alergias", "hospital", "medico", "medicamento", "dolor", "fiebre", "asma", "diabetes"],
            "violencia_domestica": ["pareja", "golpe", "golpes", "maltrato", "violencia", "abuso", "amenaza"],
            "menores": ["nino", "nina", "menor", "hijo", "hija", "bebe", "adolescente"],
            "salud_mental": ["depresion", "ansiedad", "suicidio", "autolesion", "panico", "estres"],
            "legal": ["abogado", "denuncia", "demanda", "derecho", "custodia", "divorcio"],
            "recursos": ["trabajo", "comida", "vivienda", "dinero", "albergue", "refugio"],
            "discriminacion": ["discriminacion", "racismo", "homofobia", "machismo"]
        }

        for category, keywords in categories.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return category

        return "general"

    def _generate_summary(self, text: str) -> str:
        """Genera resumen simple."""
        words = text.split()
        if len(words) > 30:
            return " ".join(words[:30]) + "..."
        return text

    def get_status(self) -> Dict:
        """Retorna estado del procesador."""
        return {
            "ia_available": self.use_ai,
            "model_name": self.model_loader.model_name if self.use_ai else None,
            "model_loaded": self.model_loader.is_loaded(),
            "mode": "ia_hibrida" if self.use_ai else "reglas"
        }


# Instancia global
_processor: Optional[HybridProcessor] = None


def get_processor() -> HybridProcessor:
    """Obtiene instancia global del procesador."""
    global _processor
    if _processor is None:
        _processor = HybridProcessor()
    return _processor


def analyze_case(text: str) -> Dict:
    """Analiza un caso (funcion de conveniencia)."""
    processor = get_processor()
    return processor.analyze(text)


if __name__ == "__main__":
    processor = HybridProcessor()
    print("Estado:", processor.get_status())

    # Test
    test_text = "Tengo una alergia grave al mani y no se que hacer"
    result = processor.analyze(test_text)
    print(f"\nAnalisis: {json.dumps(result, indent=2, ensure_ascii=False)}")
