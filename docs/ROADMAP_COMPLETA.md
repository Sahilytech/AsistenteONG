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

## FASE 5 — Seguridad y privacidad
**Estado: IMPLEMENTADA / EN EVOLUCIÓN**

- Redacción de datos personales para logs/exportaciones.
- Referencias internas no reversibles.
- Validación de extensiones de importación.
- Sanitización de nombres de archivos.
- Procesamiento local como principio de diseño.
- Revisión profesional obligatoria.

**Pendiente para cierre:** roles/permisos, bloqueo de sesión, cifrado de base, backup/restore y controles avanzados de exportación.

## FASE 6 — Producto y distribución
**Estado: EN EVOLUCIÓN**

- Pipeline de importación separado de la persistencia.
- Previsualización antes de guardar personas.
- Base para instalador Windows y smoke tests.

**Pendiente:** tutorial interactivo completo, modo capacitación, animaciones/onboarding definitivo, instalador, actualización segura y manual final.

## FASE 7 — Biblioteca inteligente
**Estado: IMPLEMENTADA / EN EVOLUCIÓN**

- Previsualización de PDF antes de utilizarlo como conocimiento.
- Conteo de páginas y caracteres.
- Huella SHA del documento.
- Previsualización de XLSX y CSV.
- Lectura de encabezados y filas sin persistirlas automáticamente.
- Importación explícita de personas después de revisión.
- Biblioteca separada del registro de personas.
- Eliminación de documento + índice local.
- Evidencia documental trazable.

**Pendiente:** OCR integrado con selección por página, detección de tablas complejas y búsqueda semántica local.

## FASE 8 — Contexto documental + expediente
**Estado: IMPLEMENTADA / EN EVOLUCIÓN**

- Recuperación de documentos locales relevantes para un relato.
- Integración de evidencia documental en el análisis explicable.
- Comparación con historial de casos.
- Señales positivas y negativas separadas.
- La coincidencia documental nunca se convierte automáticamente en una decisión.
- `review_required=True` en el contexto integrado.
- Importación revisable de personas desde planillas/documentos.

**Pendiente:** interfaz completa de evidencia por caso, comparación lado a lado y filtros por jurisdicción/categoría/fecha.

## Principio de producto
Asistente ONG es un **copiloto de organización y análisis**, no un sustituto de profesionales. El sistema recupera información, organiza expedientes, encuentra documentación y propone acciones para revisión humana.
