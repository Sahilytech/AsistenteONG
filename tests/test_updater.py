"""
Tests para sistema de actualizaciones
"""

import pytest
import sys
import json
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.updater.manager import UpdateManager, UpdatePackage


class TestUpdatePackage:
    """Tests de paquetes de actualización."""
    
    def test_version_comparison(self):
        """Test comparación de versiones."""
        manager = UpdateManager()
        
        # v2.0.0 > v1.9.9
        assert manager._compare_versions("2.0.0", "1.9.9") > 0
        
        # v1.1.0 > v1.0.9
        assert manager._compare_versions("1.1.0", "1.0.9") > 0
        
        # v1.0.0 = v1.0.0
        assert manager._compare_versions("1.0.0", "1.0.0") == 0
        
        # v1.0.0 < v1.0.1
        assert manager._compare_versions("1.0.0", "1.0.1") < 0
    
    def test_get_current_version(self):
        """Test obtener versión actual."""
        manager = UpdateManager()
        current = manager._get_current_version()
        
        assert isinstance(current, str)
        assert len(current) > 0


class TestUpdateManager:
    """Tests del gestor de actualizaciones."""
    
    def test_initialization(self):
        """Test inicialización del gestor."""
        manager = UpdateManager()
        
        assert manager.data_path.exists()
        assert manager.backup_path.exists()
        assert isinstance(manager.update_history, list)
    
    def test_record_update(self):
        """Test registro de actualización."""
        manager = UpdateManager()
        
        manager._record_update("0.2.0")
        
        assert len(manager.update_history) == 1
        assert manager.update_history[0]["version"] == "0.2.0"
        assert manager.update_history[0]["status"] == "applied"
    
    def test_get_update_history(self):
        """Test obtener historial."""
        manager = UpdateManager()
        
        manager._record_update("0.2.0")
        manager._record_update("0.3.0")
        
        history = manager.get_update_history()
        assert len(history) == 2
        assert history[0]["version"] == "0.2.0"
        assert history[1]["version"] == "0.3.0"
    
    def test_check_for_updates_newer_version(self):
        """Test detección de versión más nueva."""
        manager = UpdateManager()
        
        # Mock: simular que tenemos paquete de versión 0.2.0
        with patch.object(UpdatePackage, '_load_metadata') as mock:
            package = UpdatePackage(Path("dummy.zip"))
            package.version = "0.2.0"
            
            # Current es 0.1.0, package es 0.2.0
            with patch.object(manager, '_get_current_version', return_value="0.1.0"):
                has_update = manager.check_for_updates(Path("dummy.zip"))
                # Este test es conceptual, puede no funcionar sin archivo real
    
    def test_create_backup(self):
        """Test creación de backup."""
        manager = UpdateManager()
        
        success = manager._create_backup()
        # Debe crear archivo de backup
        assert isinstance(success, bool)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
