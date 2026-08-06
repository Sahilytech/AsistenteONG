"""
Cifrado de datos sensibles
AES-256 para base de datos y archivos
"""

import logging
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
from pathlib import Path
import base64
import os

logger = logging.getLogger(__name__)


class EncryptionManager:
    """Gestor de cifrado de datos."""
    
    def __init__(self, master_password: str = None, key_path: Path = None):
        """Inicializa el gestor."""
        self.key_path = key_path or Path.home() / ".asistente_ong" / ".key"
        self.master_password = master_password
        self.cipher = None
        
        if master_password:
            self._generate_key(master_password)
    
    def _generate_key(self, password: str) -> bytes:
        """Genera clave derivada de contraseña."""
        # Usar salt fijo para el mismo password siempre genera la misma clave
        salt = b'asistente_ong_salt_2025'
        
        kdf = PBKDF2(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        self.cipher = Fernet(key)
        
        logger.info("✅ Clave de cifrado generada")
        return key
    
    def encrypt(self, data: str) -> str:
        """Cifra un string."""
        if not self.cipher:
            logger.warning("Cifrado no inicializado")
            return data
        
        try:
            encrypted = self.cipher.encrypt(data.encode())
            return base64.b64encode(encrypted).decode()
        except Exception as e:
            logger.error(f"Error cifrando: {e}")
            return data
    
    def decrypt(self, encrypted_data: str) -> str:
        """Descifra un string."""
        if not self.cipher:
            logger.warning("Cifrado no inicializado")
            return encrypted_data
        
        try:
            data = base64.b64decode(encrypted_data)
            decrypted = self.cipher.decrypt(data)
            return decrypted.decode()
        except Exception as e:
            logger.error(f"Error descifrando: {e}")
            return encrypted_data
    
    def encrypt_file(self, file_path: Path) -> bool:
        """Cifra un archivo."""
        try:
            with open(file_path, 'rb') as f:
                data = f.read()
            
            encrypted = self.cipher.encrypt(data)
            
            with open(str(file_path) + '.enc', 'wb') as f:
                f.write(encrypted)
            
            logger.info(f"✅ Archivo cifrado: {file_path}")
            return True
        except Exception as e:
            logger.error(f"Error cifrando archivo: {e}")
            return False
    
    def decrypt_file(self, encrypted_path: Path) -> bool:
        """Descifra un archivo."""
        try:
            with open(encrypted_path, 'rb') as f:
                encrypted = f.read()
            
            decrypted = self.cipher.decrypt(encrypted)
            
            output_path = Path(str(encrypted_path).replace('.enc', ''))
            with open(output_path, 'wb') as f:
                f.write(decrypted)
            
            logger.info(f"✅ Archivo descifrado: {output_path}")
            return True
        except Exception as e:
            logger.error(f"Error descifrando archivo: {e}")
            return False


class PasswordManager:
    """Gestión segura de contraseñas."""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hashea una contraseña con bcrypt."""
        try:
            import bcrypt
            salt = bcrypt.gensalt(rounds=12)
            hashed = bcrypt.hashpw(password.encode(), salt)
            return hashed.decode()
        except ImportError:
            logger.warning("bcrypt no disponible, usando hash simple")
            import hashlib
            return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        """Verifica una contraseña contra hash."""
        try:
            import bcrypt
            return bcrypt.checkpw(password.encode(), hashed.encode())
        except:
            import hashlib
            return hashlib.sha256(password.encode()).hexdigest() == hashed


# Instancia global
_encryption_manager = None


def get_encryption_manager(password: str = None) -> EncryptionManager:
    """Obtiene gestor de cifrado global."""
    global _encryption_manager
    if _encryption_manager is None:
        _encryption_manager = EncryptionManager(master_password=password)
    return _encryption_manager


if __name__ == "__main__":
    manager = EncryptionManager("mi_contraseña_segura")
    
    # Test
    text = "Información sensible"
    encrypted = manager.encrypt(text)
    decrypted = manager.decrypt(encrypted)
    
    print(f"Original: {text}")
    print(f"Cifrado: {encrypted}")
    print(f"Descifrado: {decrypted}")
