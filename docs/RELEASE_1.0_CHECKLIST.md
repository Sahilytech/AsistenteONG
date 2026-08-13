# Checklist de salida 1.0

## Implementado y automatizado

- [x] Personas únicas y múltiples casos.
- [x] Historial y comparación longitudinal.
- [x] Análisis contextual y explicable.
- [x] Evidencia separada de decisión.
- [x] Biblioteca PDF y procedencia.
- [x] Importación XLSX con revisión previa.
- [x] Seguimientos, tareas, derivaciones y agenda.
- [x] Roles y permisos.
- [x] Bloqueo de sesión.
- [x] Backup cifrado.
- [x] Auditoría.
- [x] Exportación anonimizada.
- [x] Configuración institucional.
- [x] Tutorial interactivo.
- [x] Documentación de usuario.
- [x] Guía de implementación para ONG.
- [x] Workflow Windows de tests + EXE + instalador.
- [x] Suite actual: 71/71 tests.

## Validación previa a producción

- [ ] Instalar el artefacto Windows en un equipo limpio.
- [ ] Ejecutar smoke test de interfaz.
- [ ] Probar Biblioteca con PDFs reales autorizados.
- [ ] Probar importación de una planilla real previamente anonimizada.
- [ ] Probar backup y restauración.
- [ ] Ejecutar piloto con usuarios de una ONG.
- [ ] Corregir bloqueos de UX encontrados en el piloto.
- [ ] Aprobar política de privacidad, retención y permisos de la organización.
- [ ] Publicar checksum SHA-256 y notas de versión.

## Criterio de versión estable

La versión 1.0 se considera lista para una organización cuando los tests automatizados están en verde y el piloto cumple el protocolo de `docs/PILOTO_USUARIOS.md` sin bloqueos críticos.

La validación con personas reales no puede ser simulada por el código: requiere que una ONG ejecute el piloto y confirme el flujo.
