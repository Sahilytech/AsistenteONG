"""
Autenticación y control de acceso
PIN/Contraseña + 2FA opcional
"""

import logging
from typing import Optional
from datetime import datetime, timedelta
import secrets

logger = logging.getLogger(__name__)


class AuthManager:
    """Gestor de autenticación."""
    
    def __init__(self, inactivity_timeout_minutes: int = 15):
        """Inicializa autenticación."""
        self.current_user = None
        self.last_activity = None
        self.inactivity_timeout = timedelta(minutes=inactivity_timeout_minutes)
        self.failed_attempts = 0
        self.max_attempts = 5
    
    def authenticate(self, username: str, password: str) -> bool:
        """Autentica un usuario."""
        from .encryption import PasswordManager
        
        if self.failed_attempts >= self.max_attempts:
            logger.warning(f"❌ Demasiados intentos fallidos para {username}")
            return False
        
        # TODO: Obtener hash de DB
        # stored_hash = get_user_password_hash(username)
        # if PasswordManager.verify_password(password, stored_hash):
        
        # Simulación
        if username and len(password) >= 6:
            self.current_user = username
            self.last_activity = datetime.now()
            self.failed_attempts = 0
            logger.info(f"✅ Usuario autenticado: {username}")
            return True
        
        self.failed_attempts += 1
        logger.warning(f"❌ Fallo de autenticación para {username}")
        return False
    
    def check_inactivity(self) -> bool:
        """Verifica si el usuario está inactivo."""
        if not self.current_user or not self.last_activity:
            return True
        
        if datetime.now() - self.last_activity > self.inactivity_timeout:
            logger.warning(f"Sesión expirada por inactividad: {self.current_user}")
            self.logout()
            return True
        
        self.last_activity = datetime.now()
        return False
    
    def logout(self):
        """Cierra sesión."""
        if self.current_user:
            logger.info(f"Usuario desconectado: {self.current_user}")
        self.current_user = None
        self.last_activity = None
    
    def is_authenticated(self) -> bool:
        """Verifica si hay sesión activa."""
        return self.current_user is not None and not self.check_inactivity()
    
    def require_auth(self, func):
        """Decorador que requiere autenticación."""
        def wrapper(*args, **kwargs):
            if not self.is_authenticated():
                raise PermissionError("Autenticación requerida")
            return func(*args, **kwargs)
        return wrapper


class AuditLogger:
    """Registro de auditoría detallado."""
    
    def __init__(self):
        """Inicializa auditoría."""
        self.logs = []
    
    def log_access(self, user: str, action: str, resource: str, 
                   status: str = "success", details: str = None):
        """Registra acceso a recurso."""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "user": user,
            "action": action,
            "resource": resource,
            "status": status,
            "details": details
        }
        
        self.logs.append(log_entry)
        logger.info(f"[AUDIT] {user} - {action} - {resource} - {status}")
    
    def get_user_activity(self, user: str, limit: int = 50) -> list:
        """Obtiene actividad de un usuario."""
        return [log for log in self.logs if log["user"] == user][-limit:]
    
    def get_all_logs(self, limit: int = 100) -> list:
        """Obtiene todos los logs."""
        return self.logs[-limit:]


# Instancias globales
_auth_manager = None
_audit_logger = None


def get_auth_manager() -> AuthManager:
    """Obtiene gestor de autenticación."""
    global _auth_manager
    if _auth_manager is None:
        _auth_manager = AuthManager()
    return _auth_manager


def get_audit_logger() -> AuditLogger:
    """Obtiene auditor."""
    global _audit_logger
    if _audit_logger is None:
        _audit_logger = AuditLogger()
    return _audit_logger
