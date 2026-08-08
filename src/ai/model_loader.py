"""
Cargador de modelos GGUF - llama.cpp real
Funciona offline, carga modelos locales
"""

import logging
from pathlib import Path
from typing import Optional
import json
import os

logger = logging.getLogger(__name__)

# Modelos soportados con info de recursos
MODELS = {
    "gemma-3-1b": {
        "name": "Gemma 3 1B",
        "file": "gemma-3-1b-it-q4_k_m.gguf",
        "size_mb": 700,
        "ram_mb": 1200,
        "context": 512,
        "threads": 2,
        "url": "https://huggingface.co/google/gemma-3-1b-it-gguf",
        "description": "Modelo ligero de Google, ideal para PCs de bajos recursos"
    },
    "qwen-2.5-1.5b": {
        "name": "Qwen 2.5 1.5B Instruct",
        "file": "qwen2.5-1.5b-instruct-q4_k_m.gguf",
        "size_mb": 1000,
        "ram_mb": 1800,
        "context": 512,
        "threads": 2,
        "url": "https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF",
        "description": "Modelo multilingue de Alibaba, buen rendimiento en español"
    },
    "tinyllama": {
        "name": "TinyLlama 1.1B",
        "file": "tinyllama-1.1b-chat-v1.0-q4_k_m.gguf",
        "size_mb": 600,
        "ram_mb": 1000,
        "context": 512,
        "threads": 2,
        "url": "https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF",
        "description": "Modelo ultra-ligero, el más rápido en hardware limitado"
    }
}


class ModelLoader:
    """Cargador de modelos GGUF con llama.cpp."""

    def __init__(self):
        self.model = None
        self.model_name = None
        self.model_path = None
        self.llama = None

    def list_available_models(self) -> list:
        """Lista modelos soportados."""
        return [
            {
                "id": key,
                "name": info["name"],
                "size_mb": info["size_mb"],
                "ram_mb": info["ram_mb"],
                "description": info["description"]
            }
            for key, info in MODELS.items()
        ]

    def list_downloaded_models(self) -> list:
        """Lista modelos descargados localmente."""
        models_dir = Path("models")
        if not models_dir.exists():
            return []

        downloaded = []
        for key, info in MODELS.items():
            model_file = models_dir / info["file"]
            if model_file.exists():
                size_mb = model_file.stat().st_size / (1024 * 1024)
                downloaded.append({
                    "id": key,
                    "name": info["name"],
                    "path": str(model_file),
                    "size_mb": round(size_mb, 1)
                })

        return downloaded

    def is_model_available(self, model_name: str) -> bool:
        """Verifica si un modelo está descargado."""
        if model_name not in MODELS:
            return False

        models_dir = Path("models")
        model_file = models_dir / MODELS[model_name]["file"]
        return model_file.exists()

    def load_model(self, model_name: str = "gemma-3-1b") -> bool:
        """Carga un modelo GGUF usando llama-cpp-python."""
        try:
            from llama_cpp import Llama

            if model_name not in MODELS:
                logger.error(f"Modelo no soportado: {model_name}")
                return False

            model_info = MODELS[model_name]
            models_dir = Path("models")
            model_file = models_dir / model_info["file"]

            if not model_file.exists():
                logger.warning(f"⚠️ Modelo no encontrado: {model_file}")
                logger.info(f"Descargalo desde: {model_info['url']}")
                return False

            logger.info(f"🧠 Cargando modelo: {model_info['name']}...")

            # Configuración para bajos recursos
            self.llama = Llama(
                model_path=str(model_file),
                n_ctx=model_info["context"],
                n_threads=model_info["threads"],
                n_gpu_layers=0,  # CPU only
                verbose=False
            )

            self.model = self.llama
            self.model_name = model_name
            self.model_path = str(model_file)

            logger.info(f"✅ Modelo cargado: {model_info['name']}")
            return True

        except ImportError:
            logger.warning("⚠️ llama-cpp-python no instalado. Instalalo con: pip install llama-cpp-python")
            return False
        except Exception as e:
            logger.error(f"❌ Error cargando modelo: {e}")
            return False

    def generate(self, prompt: str, max_tokens: int = 256, temperature: float = 0.7) -> str:
        """Genera texto con el modelo cargado."""
        if not self.llama:
            logger.warning("Modelo no cargado")
            return ""

        try:
            output = self.llama(
                prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                stop=["</s>", "Human:", "Assistant:"],
                echo=False
            )
            return output["choices"][0]["text"].strip()
        except Exception as e:
            logger.error(f"Error generando texto: {e}")
            return ""

    def generate_json(self, prompt: str, max_tokens: int = 512) -> dict:
        """Genera JSON estructurado con el modelo."""
        if not self.llama:
            return {"error": "Modelo no cargado"}

        try:
            # Prompt especial para JSON
            json_prompt = f"""{prompt}

Responde ÚNICAMENTE con un JSON válido. No agregues texto adicional.
"""
            output = self.llama(
                json_prompt,
                max_tokens=max_tokens,
                temperature=0.3,  # Baja temperatura para JSON preciso
                stop=["</s>"],
                echo=False
            )

            text = output["choices"][0]["text"].strip()

            # Intentar parsear JSON
            import json
            # Buscar JSON en el texto
            start = text.find("{")
            end = text.rfind("}") + 1
            if start >= 0 and end > start:
                json_str = text[start:end]
                return json.loads(json_str)

            return {"error": "No se pudo parsear JSON", "raw": text}

        except json.JSONDecodeError as e:
            logger.error(f"Error parseando JSON: {e}")
            return {"error": "JSON inválido"}
        except Exception as e:
            logger.error(f"Error generando JSON: {e}")
            return {"error": str(e)}

    def is_loaded(self) -> bool:
        """Verifica si hay un modelo cargado."""
        return self.llama is not None

    def get_model(self):
        """Obtiene el modelo cargado."""
        return self.llama

    def unload_model(self):
        """Descarga el modelo de memoria."""
        self.llama = None
        self.model = None
        self.model_name = None
        logger.info("🧠 Modelo descargado de memoria")

    def get_model_info(self) -> dict:
        """Retorna info del modelo actual."""
        if not self.model_name:
            return {"status": "No cargado"}

        info = MODELS.get(self.model_name, {})
        return {
            "name": info.get("name", self.model_name),
            "path": self.model_path,
            "context": info.get("context", 512),
            "threads": info.get("threads", 2),
            "loaded": self.is_loaded()
        }


# Instancia global
_loader: Optional[ModelLoader] = None


def get_model_loader() -> ModelLoader:
    """Obtiene la instancia global del cargador."""
    global _loader
    if _loader is None:
        _loader = ModelLoader()
    return _loader


def load_default_model() -> bool:
    """Carga el modelo predeterminado."""
    loader = get_model_loader()
    return loader.load_model("gemma-3-1b")


if __name__ == "__main__":
    loader = ModelLoader()
    print("Modelos disponibles:", loader.list_available_models())
    print("Modelos descargados:", loader.list_downloaded_models())
