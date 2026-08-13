# Distribución nacional

## Modelo recomendado

Asistente ONG debe distribuirse como aplicación Windows offline, con una instalación por organización y datos locales separados por instalación.

## Paquete de distribución

Cada entrega debe contener:

- `AsistenteONG.exe` o instalador firmado cuando esté disponible;
- guía de usuario;
- instrucciones de backup;
- notas de versión;
- checksum SHA-256 del ejecutable;
- canal de soporte;
- aviso de límites y revisión profesional.

## Versionado

Usar versiones semánticas:

- `MAJOR`: cambios incompatibles.
- `MINOR`: nuevas funciones compatibles.
- `PATCH`: correcciones.

## Canales

1. **Pilot**: organizaciones de prueba.
2. **Stable**: versión validada.
3. **Hotfix**: correcciones urgentes.

No mezclar datos de una organización con otra instalación.

## Actualizaciones

Las actualizaciones deben instalarse después de backup y verificación de integridad. El actualizador no debe borrar la base local sin confirmación explícita.

## Privacidad

La distribución nacional no implica centralizar los expedientes. El modelo base es local/offline. Cada organización es responsable de sus permisos, conservación, backup y procedimientos internos.

## Soporte

Toda incidencia debe incluir versión, sistema operativo, pasos para reproducir y logs sanitizados. Nunca enviar bases de datos con información personal a un canal público de soporte.

## Lista previa a liberar

- [ ] Suite de tests completa en verde.
- [ ] Smoke test del ejecutable.
- [ ] Instalación limpia probada.
- [ ] Desinstalación probada.
- [ ] Backup/restauración probados.
- [ ] Tutorial probado.
- [ ] Biblioteca PDF probada.
- [ ] Importación XLSX probada.
- [ ] Roles/permisos probados.
- [ ] SHA-256 publicado.
- [ ] Notas de versión publicadas.
- [ ] Piloto aprobado.
