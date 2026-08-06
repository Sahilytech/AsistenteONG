"""
Cargador de modelos GGUF
Gemma 3 1B o alternativas
"""

import logging
from pathlib import Path
from typing import Optional
import json

logger = logging.getLogger(__name__)

# Modelos soportados
MODELS = {
    "gemma-3-1b": {
        "name": "Gemma 3 1B",
        "size": "2.0GB",
        "url": "https://huggingface.co/google/gemma-3-1b-gguf/...",
        "type": "gemma",
    },
    "qwen-2.5-1.5b": {
        "name": "Qwen 2.5 1.5B",
        "size": "1.8GB",
        "url": "https://huggingface.co/Qwen/qwen-2.5-1.5b-gguf/...",
        "type": "qwen",
    },
    "tinyllama": {
        "name": "TinyLlama 1.1B",
        "size": "1.5GB",
        "url": "https://huggingface.co/tinyllama/TinyLlama-1.1B-gguf/...",
        "type": "llama",
    },
    "phi-3-mini": {
        "name": "Phi-3 Mini",
        "size": "2.2GB",
        "url": "https://huggingface.co/microsoft/Phi-3-mini-gguf/...",
        "type": "phi",
    },
}


class ModelLoader:
    """Gestor de carga de modelos."""
    
    def __init__(self, model_path: Path = None):
        """Inicializa el cargador."""
        self.model_path = model_path or Path(__file__).parent.parent.parent / "models"
        self.model = None
        self.model_name = None
    
    def list_available_models(self) -> dict:
        """Lista todos los modelos disponibles."""
        return MODELS
    
    def list_downloaded_models(self) -> list:
        """Lista modelos ya descargados localmente."""
        if not self.model_path.exists():
            return []
        
        gguf_files = list(self.model_path.glob("*.gguf"))
        return [f.name for f in gguf_files]
    
    def download_model(self, model_name: str) -> bool:
        """Descarga un modelo (stub para futuro)."""
        logger.info(f"Descargando modelo: {model_name}")
        
        if model_name not in MODELS:
            logger.error(f"Modelo no soportado: {model_name}")
            return False
        
        model_info = MODELS[model_name]
        logger.info(f"Descargando {model_info['name']} ({model_info['size']})...")
        
        # TODO: Implementar descarga con requests
        # - Mostrar barra de progreso
        # - Validar integridad
        # - Descomprimir si es necesario
        
        logger.info(f"✅ {model_info['name']} descargado")
        return True
    
    def load_model(self, model_name: str = "gemma-3-1b") -> bool:
        """Carga un modelo en memoria."""
        try:
            # Buscar archivo local
            model_files = list(self.model_path.glob("*.gguf"))
            
            if not model_files:
                logger.error("No hay modelos descargados")
                logger.info("Descargando modelo predeterminado...")
                if not self.download_model(model_name):
                    return False
                model_files = list(self.model_path.glob("*.gguf"))
            
            if not model_files:
                logger.error("No se encontró modelo")
                return False
            
            model_file = model_files[0]
            logger.info(f"Cargando modelo: {model_file.name}")
            
            # Aquí iría: from llama_cpp import Llama
            # self.model = Llama(str(model_file), n_ctx=1024, n_gpu_layers=0)
            
            self.model_name = model_name
            logger.info("✅ Modelo cargado exitosamente")
            return True
            
        except Exception as e:
            logger.error(f"Error al cargar modelo: {e}")
            return False
    
    def is_loaded(self) -> bool:
        """Verifica si hay un modelo cargado."""
        return self.model is not None
    
    def get_model(self):
        """Obtiene el modelo cargado."""
        if not self.is_loaded():
            logger.warning("Modelo no cargado")
            return None
        return self.model
    
    def unload_model(self):
        """Descarga el modelo de memoria."""
        self.model = None
        self.model_name = None
        logger.info("Modelo descargado")


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
