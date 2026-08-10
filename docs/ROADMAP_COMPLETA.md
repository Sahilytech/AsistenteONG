# Asistente ONG — roadmap integral

## FASES 1–30
**Estado: IMPLEMENTADAS / EN EVOLUCIÓN**

El núcleo cubre registro único de personas y múltiples casos, biblioteca documental local, extracción PDF/XLSX/CSV, evidencia trazable, análisis explicable, comparación histórica sin decisiones automáticas, operación ONG, privacidad, control de acceso, importación revisable y workspace longitudinal.

### Principios mantenidos
- Procesamiento local como principio de diseño.
- La evidencia se mantiene separada de cualquier decisión.
- Toda salida analítica requiere revisión profesional.
- No se agregan datos ficticios al inicio.
- Una persona puede tener múltiples casos sin duplicar su identidad.

## FASE 31 — Seguridad de sesión
**Estado: IMPLEMENTADA**

- `SessionGuard` para detectar inactividad y bloquear la sesión.
- Bloqueo manual disponible desde el núcleo de seguridad.
- Desbloqueo mediante verificador derivado por SHA-256, sin almacenar la frase secreta.
- Comparación resistente a timing mediante `compare_digest`.
- Timeout configurable.

## FASE 32 — Backup y recuperación segura
**Estado: IMPLEMENTADA**

- Copia de datos locales en ZIP temporal.
- Cifrado autenticado AES-GCM.
- Derivación de clave mediante PBKDF2-HMAC-SHA256.
- Salt y nonce aleatorios por copia.
- El contenido sensible no queda visible dentro del archivo de backup.
- Restauración con validación de rutas para impedir path traversal.
- Contraseña incorrecta invalida la restauración.
- Pruebas automatizadas de backup, restore y sesión.

## FASES 33–34 — Próximo bloque
**Estado: PLANIFICADAS**

- Centro de seguridad visible en la interfaz.
- Configuración de timeout y bloqueo.
- Asistente visual de backup/restore.
- Validación previa a restaurar para evitar sobrescrituras accidentales.
- Registro auditable de operaciones de seguridad sin guardar datos sensibles.

## FASES 35–36 — Próximo bloque
**Estado: PLANIFICADAS**

- Biblioteca semántica local.
- OCR integrado con selección de páginas.
- Detección y normalización de tablas complejas.
- Recuperación híbrida: coincidencia textual + similitud semántica local.
- Explicación de por qué cada documento fue recuperado.

## Principio de producto
Asistente ONG es un **copiloto de organización y análisis**, no un sustituto de profesionales. El sistema recupera información, organiza expedientes, encuentra documentación y propone acciones para revisión humana.
