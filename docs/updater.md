# Sistema de Actualizaciones (v0.6)

## Visión

Actualización de base de conocimiento mediante paquetes ZIP firmados, 100% offline y con backup automático.

## Características

✅ Paquetes ZIP con metadatos JSON
✅ Validación de integridad (checksum)
✅ Firma digital (RSA/ECDSA) - futuro
✅ Backup automático antes de actualizar
✅ Rollback si falla la actualización
✅ Historial de versiones

## Estructura de paquete

```
update_v0.2.0.zip
├── metadata.json          # Versión, archivos, checksum
├── data/
│   ├── recursos.json      # Organismos, teléfonos
│   ├── leyes/
│   │   ├── argentina.md
│   │   └── mexico.md
│   └── plantillas.json
├── models/
│   └── classifier_v2.onnx
└── signature.asc          # Firma RSA (futuro)
```

### metadata.json

```json
{
  "version": "0.2.0",
  "date": "2025-01-15",
  "type": "data",
  "files": [
    {
      "path": "data/recursos.json",
      "checksum": "sha256_hash"
    }
  ],
  "description": "Actualización de recursos y leyes",
  "author": "AsistenteONG Team",
  "signature": "base64_encoded_signature"
}
```

## Uso

### Aplicar actualización

```python
from src.updater.manager import get_update_manager
from pathlib import Path

manager = get_update_manager()

# Desde pendrive o descarga
package_path = Path("/media/pendrive/update_v0.2.0.zip")

# Verificar si hay update disponible
if manager.check_for_updates(package_path):
    print("Actualización disponible")
    
    # Aplicar
    if manager.apply_update(package_path, backup=True):
        print("✅ Actualizado exitosamente")
    else:
        print("❌ Error en actualización")
```

### Ver historial

```python
history = manager.get_update_history()
for update in history:
    print(f"v{update['version']} - {update['timestamp']}")
```

## Proceso de actualización

1. **Cargar paquete**
   - Verificar que sea ZIP válido
   - Leer metadata.json

2. **Validar**
   - Verificar versión
   - Validar checksum de archivos
   - Verificar firma digital (futuro)

3. **Backup**
   - Copiar DB actual
   - Cifrar backup
   - Guardar en `~/.asistente_ong/backups/`

4. **Aplicar**
   - Extraer archivos
   - Actualizar DB
   - Recargar recursos

5. **Registrar**
   - Guardar en historial
   - Log de auditoría

## Distribución

### Opción 1: Pendrive

```bash
# En sitio de soporte
1. Descargar update_v0.2.0.zip
2. Copiar a pendrive
3. Llevar a ONG
4. Insertar en computadora
5. Aplicar desde UI
```

### Opción 2: Conexión (futuro)

```python
# Cuando hay conexión
manager.download_updates(url="https://...")
manager.apply_update()
```

## Seguridad de paquetes

- ✅ ZIP protegido contra corrupción
- ✅ Checksum SHA-256 de cada archivo
- ⏳ Firma digital RSA (v0.7)
- ⏳ Encriptación de paquete (v0.7)

---

**v0.6 Status:** ✅ Actualizaciones funcionales
