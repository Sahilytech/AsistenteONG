# Seguridad y Cifrado (v0.5)

## Visión general

Protección completa de datos mediante cifrado AES-256, autenticación PIN/contraseña, auditoría y bloqueo automático.

## Componentes

### 1. EncryptionManager

Cifrado simétrico AES-256 basado en contraseña maestra.

```python
from src.security.encryption import EncryptionManager

manager = EncryptionManager(master_password="mi_contraseña")

# Cifrar string
encrypted = manager.encrypt("Información sensible")

# Descifrar
decrypted = manager.decrypt(encrypted)

# Cifrar archivo
manager.encrypt_file(Path("data.db"))
```

### 2. PasswordManager

Hasheo seguro con bcrypt (12 rounds).

```python
from src.security.encryption import PasswordManager

# Hashear
hashed = PasswordManager.hash_password("password123")

# Verificar
is_valid = PasswordManager.verify_password("password123", hashed)
```

### 3. AuthManager

Autenticación con inactividad automática.

```python
from src.security.auth import get_auth_manager

auth = get_auth_manager()

# Login
if auth.authenticate("operator1", "password"):
    print("Autenticado")

# Verificar sesión
if auth.is_authenticated():
    # Hacer algo
    pass

# Timeout automático: 15 minutos de inactividad → logout
```

### 4. AuditLogger

Registro completo de acciones.

```python
from src.security.auth import get_audit_logger

audit = get_audit_logger()

# Registrar acceso
audit.log_access(
    user="operator1",
    action="CREATE_CASE",
    resource="case_123",
    status="success"
)

# Ver historial
logs = audit.get_user_activity("operator1")
```

## Características de seguridad

✅ **Cifrado en reposo**
- AES-256 para base de datos
- Derivación de clave con PBKDF2 (100k iteraciones)
- Archivos de backup cifrados

✅ **Autenticación**
- Contraseña de operador hasheada con bcrypt
- PIN numérico opcional
- 2FA futura

✅ **Control de acceso**
- Sesiones con timeout automático (15 min inactividad)
- Bloqueo de pantalla
- Máximo 5 intentos fallidos

✅ **Auditoría**
- Log de todas las operaciones
- Quién, qué, cuándo, dónde
- No se guardan datos sensibles en logs

✅ **Backups**
- Automáticos antes de cada actualización
- Cifrados
- Almacenados en carpeta privada

## Flujo de seguridad

```
Aplicación inicia
    ↓
Solicita contraseña maestra
    ↓
Verifica con bcrypt
    ↓
Carga clave de cifrado
    ↓
Descifra base de datos
    ↓
Sesión activa por 15 min
    ↓
Si inactividad → logout automático
    ↓
Antes de salir → cifra datos
```

## Configuración

**Archivo**: `.asistente_ong/config.json`

```json
{
  "security": {
    "encryption_enabled": true,
    "password_required": true,
    "2fa_enabled": false,
    "inactivity_timeout_minutes": 15,
    "max_login_attempts": 5
  }
}
```

## Limitaciones y TODOs

- [ ] 2FA (TOTP)
- [ ] Biometría (fingerprint, face)
- [ ] Cifrado de disco completo
- [ ] Sincronización cifrada en cloud
- [ ] Validación de firma RSA para paquetes

---

**v0.5 Status:** ✅ Seguridad core completa
