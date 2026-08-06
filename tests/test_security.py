"""
Tests de seguridad
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.security.encryption import EncryptionManager, PasswordManager
from src.security.auth import AuthManager, AuditLogger


class TestEncryptionManager:
    """Tests de cifrado."""
    
    def test_encrypt_decrypt(self):
        """Test cifrado/descifrado básico."""
        manager = EncryptionManager("test_password")
        
        text = "Información sensible"
        encrypted = manager.encrypt(text)
        decrypted = manager.decrypt(encrypted)
        
        assert encrypted != text
        assert decrypted == text
    
    def test_different_passwords(self):
        """Test que diferentes contraseñas generan claves diferentes."""
        m1 = EncryptionManager("password1")
        m2 = EncryptionManager("password2")
        
        text = "Test"
        enc1 = m1.encrypt(text)
        enc2 = m2.encrypt(text)
        
        assert enc1 != enc2
    
    def test_decrypt_with_wrong_password(self):
        """Test que descifrar con contraseña incorrecta falla."""
        m1 = EncryptionManager("correct_password")
        m2 = EncryptionManager("wrong_password")
        
        text = "Secreto"
        encrypted = m1.encrypt(text)
        decrypted = m2.decrypt(encrypted)
        
        # No debería coincidir
        assert decrypted != text


class TestPasswordManager:
    """Tests de gestión de contraseñas."""
    
    def test_hash_password(self):
        """Test hasheo de contraseña."""
        password = "MyPassword123!"
        hashed = PasswordManager.hash_password(password)
        
        assert hashed != password
        assert len(hashed) > 0
    
    def test_verify_correct_password(self):
        """Test verificación de contraseña correcta."""
        password = "MyPassword123!"
        hashed = PasswordManager.hash_password(password)
        
        is_valid = PasswordManager.verify_password(password, hashed)
        assert is_valid == True
    
    def test_verify_wrong_password(self):
        """Test verificación de contraseña incorrecta."""
        password = "MyPassword123!"
        wrong = "WrongPassword"
        hashed = PasswordManager.hash_password(password)
        
        is_valid = PasswordManager.verify_password(wrong, hashed)
        assert is_valid == False


class TestAuthManager:
    """Tests de autenticación."""
    
    def test_successful_login(self):
        """Test login exitoso."""
        auth = AuthManager()
        
        success = auth.authenticate("user1", "password123")
        assert success == True
        assert auth.is_authenticated() == True
    
    def test_failed_login(self):
        """Test login fallido."""
        auth = AuthManager()
        
        success = auth.authenticate("user1", "short")
        assert success == False
        assert auth.is_authenticated() == False
    
    def test_failed_attempts_limit(self):
        """Test límite de intentos fallidos."""
        auth = AuthManager()
        
        for i in range(5):
            auth.authenticate("user1", "wrongpass")
        
        # Sexto intento debe ser bloqueado
        success = auth.authenticate("user1", "correctpass")
        assert success == False
    
    def test_logout(self):
        """Test logout."""
        auth = AuthManager()
        
        auth.authenticate("user1", "password123")
        assert auth.is_authenticated() == True
        
        auth.logout()
        assert auth.is_authenticated() == False
    
    def test_inactivity_timeout(self):
        """Test timeout por inactividad."""
        auth = AuthManager(inactivity_timeout_minutes=0)  # Inmediato
        
        auth.authenticate("user1", "password123")
        # Simular el paso de tiempo
        auth.check_inactivity()
        
        assert auth.is_authenticated() == False


class TestAuditLogger:
    """Tests de auditoría."""
    
    def test_log_access(self):
        """Test registro de acceso."""
        audit = AuditLogger()
        
        audit.log_access("user1", "CREATE_CASE", "case_1", "success")
        
        logs = audit.get_all_logs()
        assert len(logs) == 1
        assert logs[0]["user"] == "user1"
        assert logs[0]["action"] == "CREATE_CASE"
    
    def test_get_user_activity(self):
        """Test historial de usuario."""
        audit = AuditLogger()
        
        audit.log_access("user1", "ACTION1", "res1")
        audit.log_access("user1", "ACTION2", "res2")
        audit.log_access("user2", "ACTION3", "res3")
        
        user1_logs = audit.get_user_activity("user1")
        assert len(user1_logs) == 2
    
    def test_audit_with_status(self):
        """Test auditoría con diferentes estados."""
        audit = AuditLogger()
        
        audit.log_access("user1", "DELETE_CASE", "case_1", "failure", "Usuario sin permisos")
        
        logs = audit.get_all_logs()
        assert logs[0]["status"] == "failure"
        assert "sin permisos" in logs[0]["details"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
