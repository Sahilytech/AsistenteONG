# Asistente ONG — roadmap integral

## FASE 1 — Núcleo de personas y casos
**Estado: IMPLEMENTADA**

- Registro único por persona.
- Detección de coincidencias por documento, nombre + fecha de nacimiento y nombre único.
- Una persona puede tener múltiples casos.
- `person_id` persistente para vincular casos.
- Expediente de persona con historial.
- Crear un nuevo caso directamente desde el expediente.
- Línea temporal básica por caso.
- Búsqueda y filtros de casos.
- Importación de personas desde XLSX, CSV y PDF de texto.
- No se agregan datos ficticios al inicio.

## FASE 2 — Documentos y conocimiento local
**Estado: IMPLEMENTADA / EN EVOLUCIÓN**

- Biblioteca PDF local.
- Importación y copia controlada de documentos.
- Extracción de texto con limpieza de saltos y palabras partidas.
- Fragmentación solapada para recuperar contexto relevante.
- Búsqueda local por términos.
- Ranking de evidencia por coincidencia.
- Comparación de relato de caso contra fragmentos documentales.
- Huella SHA para identificar cambios de archivos.
- Estado de extracción del documento.
- Eliminación de PDF + índice asociado.
- Vaciar biblioteca sin eliminar personas ni casos.
- OCR opcional para PDFs escaneados mediante PyMuPDF + Tesseract.

## FASE 3 — Inteligencia explicable
**Estado: IMPLEMENTADA / EN EVOLUCIÓN**

- Perfil estructurado antes de clasificar.
- Negación y señales descartadas explícitamente.
- Indicadores positivos y negativos.
- Información faltante y preguntas sugeridas.
- Confianza orientativa.
- Explicación de por qué se clasificó.
- Evidencia documental relevante con términos coincidentes.
- Comparación con historial de la persona.
- Comparación entre relatos sin afirmar identidad del hecho.
- Revisión profesional obligatoria.
- Limitaciones explícitas para evitar presentar la salida como diagnóstico o decisión.

## FASE 4 — Operación ONG
**Estado: IMPLEMENTADA / EN EVOLUCIÓN**

- Recursos nacionales verificables.
- Registro de derivaciones y estados.
- Tareas por caso.
- Fechas de vencimiento y detección de tareas vencidas.
- Seguimientos por caso y canal.
- Dashboard operativo básico.
- Estados controlados para evitar datos operativos inválidos.
- Base preparada para agenda, alertas y protocolos configurables en la interfaz.

## FASE 5 — Seguridad
**Pendiente**

- Roles y permisos.
- Bloqueo de sesión.
- Cifrado en reposo.
- Auditoría completa.
- Exportaciones controladas.
- Backup/restore.
- Vista anonimizada.
- Minimización de datos.

## FASE 6 — Producto y distribución
**Pendiente**

- Tutorial interactivo.
- Modo capacitación con datos ficticios claramente marcados.
- Animaciones y onboarding.
- Instalador Windows.
- Smoke test de arranque.
- Instalación limpia.
- Actualizaciones seguras.
- Manual de uso.

## Principio de producto
Asistente ONG es un **copiloto de organización y análisis**, no un sustituto de profesionales. El sistema recupera información, organiza expedientes, encuentra documentación y propone acciones para revisión humana.
