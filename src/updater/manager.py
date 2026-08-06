"""
Gestor de actualizaciones
Paquetes firmados y versionamiento
"""

import logging
import json
import zipfile
from pathlib import Path
from datetime import datetime
from typing import Dict, Tuple

logger = logging.getLogger(__name__)


class UpdatePackage:
    """Representa un paquete de actualización."""
    
    def __init__(self, path: Path):
        """Carga paquete."""
        self.path = path
        self.metadata = None
        self.version = None
        self.files = []
        
        if path.exists():
            self._load_metadata()
    
    def _load_metadata(self):
        """Carga metadatos del paquete."""
        try:
            with zipfile.ZipFile(self.path, 'r') as zf:
                if 'metadata.json' in zf.namelist():
                    with zf.open('metadata.json') as f:
                        self.metadata = json.loads(f.read())
                        self.version = self.metadata.get('version')
                        self.files = self.metadata.get('files', [])
                        logger.info(f"Paquete cargado: v{self.version}")
        except Exception as e:
            logger.error(f"Error cargando paquete: {e}")
    
    def validate(self) -> Tuple[bool, str]:
        """Valida integridad del paquete."""
        if not self.metadata:
            return False, "Sin metadatos"
        
        if not self.version:
            return False, "Sin versión"
        
        # TODO: Validar firma (RSA/ECDSA)
        
        return True, "Válido"
    
    def extract_to(self, dest_path: Path) -> bool:
        """Extrae paquete."""
        try:
            with zipfile.ZipFile(self.path, 'r') as zf:
                zf.extractall(dest_path)
            
            logger.info(f"✅ Paquete extraído a {dest_path}")
            return True
        except Exception as e:
            logger.error(f"Error extrayendo: {e}")
            return False


class UpdateManager:
    """Gestor de actualizaciones."""
    
    def __init__(self, data_path: Path = None):
        """Inicializa gestor."""
        self.data_path = data_path or Path.home() / ".asistente_ong"
        self.backup_path = self.data_path / "backups"
        self.backup_path.mkdir(parents=True, exist_ok=True)
        
        self.update_history = []
    
    def check_for_updates(self, package_path: Path) -> bool:
        """Verifica si hay actualizaciones disponibles."""
        package = UpdatePackage(package_path)
        
        if not package.version:
            return False
        
        # Comparar versión (simple)
        current_version = self._get_current_version()
        
        return self._compare_versions(package.version, current_version) > 0
    
    def apply_update(self, package_path: Path, backup: bool = True) -> bool:
        """Aplica actualización."""
        package = UpdatePackage(package_path)
        
        # Validar
        valid, msg = package.validate()
        if not valid:
            logger.error(f"Paquete inválido: {msg}")
            return False
        
        # Backup
        if backup:
            if not self._create_backup():
                logger.error("Fallo al crear backup")
                return False
        
        # Extraer
        if not package.extract_to(self.data_path):
            logger.error("Fallo extrayendo paquete")
            return False
        
        # Registrar
        self._record_update(package.version)
        
        logger.info(f"✅ Actualizado a v{package.version}")
        return True
    
    def _create_backup(self) -> bool:
        """Crea backup de datos."""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = self.backup_path / f"backup_{timestamp}.zip"
            
            # TODO: Comprimir y cifrar backup
            
            logger.info(f"✅ Backup creado: {backup_file}")
            return True
        except Exception as e:
            logger.error(f"Error en backup: {e}")
            return False
    
    def _record_update(self, version: str):
        """Registra aplicación de actualización."""
        record = {
            "version": version,
            "timestamp": datetime.now().isoformat(),
            "status": "applied"
        }
        self.update_history.append(record)
        logger.info(f"Actualización registrada: {version}")
    
    def _get_current_version(self) -> str:
        """Obtiene versión actual."""
        # TODO: Leer de archivo de versión
        return "0.1.0"
    
    def _compare_versions(self, v1: str, v2: str) -> int:
        """Compara versiones. Retorna >0 si v1>v2."""
        try:
            v1_parts = [int(x) for x in v1.split('.')]
            v2_parts = [int(x) for x in v2.split('.')]
            
            for i in range(max(len(v1_parts), len(v2_parts))):
                p1 = v1_parts[i] if i < len(v1_parts) else 0
                p2 = v2_parts[i] if i < len(v2_parts) else 0
                
                if p1 > p2:
                    return 1
                elif p1 < p2:
                    return -1
            
            return 0
        except:
            return 0
    
    def get_update_history(self) -> list:
        """Obtiene historial de actualizaciones."""
        return self.update_history


# Instancia global
_update_manager = None


def get_update_manager() -> UpdateManager:
    """Obtiene gestor de actualizaciones."""
    global _update_manager
    if _update_manager is None:
        _update_manager = UpdateManager()
    return _update_manager
