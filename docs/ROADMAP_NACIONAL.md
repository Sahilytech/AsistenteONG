# Asistente ONG — hoja de ruta nacional

La plataforma evoluciona por fases. El sistema debe ser offline-first, explicable, auditable y configurable por organización. La IA asiste; el criterio profesional prevalece.

## Fase 1 — Núcleo inteligente — LISTO
- [x] Perfil integral estructurado.
- [x] Separación entre contexto, indicadores y señales de riesgo.
- [x] Detección por frases completas y límites de palabra.
- [x] Negación básica.
- [x] Preguntas de información faltante.
- [x] Motor de razonamiento explicable.
- [x] Integración inicial con la creación de casos.
- [x] Tests de regresión para falsos positivos.
- [x] Smoke test del núcleo.

## Fase 2 — Caso + Informe + Seguimiento — EN PROGRESO
- [x] Informe social persistido dentro del caso.
- [x] Esquema estructurado del informe social.
- [x] Estructura base de timeline.
- [x] Derivaciones con estado persistidas.
- [x] Modelo de genograma.
- [x] Núcleo de plan de intervención.
- [x] Modelo de seguimiento.
- [ ] Genograma visual en UI.
- [ ] Integrar plan de intervención al flujo visual.
- [ ] Próxima acción y vencimientos en UI.
- [ ] Historial completo de cambios en SQLite.

## Fase 3 — Cobertura Argentina — EN PROGRESO
- [x] Modelo de jurisdicción.
- [x] Catálogo de recursos extensible.
- [x] Registro que exige fuente y fecha de verificación.
- [x] Provincias y CABA como catálogo base.
- [ ] Catálogo nacional verificado.
- [ ] Municipios/localidades.
- [ ] Recursos oficiales por jurisdicción.

## Fase 4 — Memoria y conocimiento — EN PROGRESO
- [x] Base documental lógica local.
- [x] Búsqueda local por relevancia.
- [x] Metadatos de fuente, versión y jurisdicción.
- [ ] Persistencia/indexación documental completa.
- [ ] RAG offline.
- [ ] Actualización online desde fuentes permitidas.
- [ ] Revisión de cambios antes de reemplazar conocimiento.
- [ ] Evidencia y fuentes visibles en cada respuesta.

## Fase 5 — Seguridad profesional — EN PROGRESO
- [x] Utilidad de minimización de datos.
- [x] Eventos de auditoría estructurados.
- [x] Esquema de exportación anonimizada.
- [ ] Cifrado de base y backups.
- [ ] Roles y permisos.
- [ ] Bloqueo automático.
- [ ] Auditoría persistente.
- [ ] Modo privacidad/anónimo para capacitación.
- [ ] Exportaciones protegidas completas.

## Fase 6 — Documentos y trabajo profesional — EN PROGRESO
- [x] Esquema base de informe social.
- [x] Modelo normalizado de informe social.
- [ ] Informe social profesional en UI.
- [ ] Nota de derivación.
- [x] Núcleo de plan de intervención.
- [ ] Integración visual del plan.
- [ ] Resumen de caso.
- [ ] Seguimiento visual.
- [ ] PDF/DOCX.
- [ ] Plantillas institucionales configurables.

## Fase 7 — Analítica y capacitación — PLANIFICADA
- [ ] Estadísticas sin datos identificatorios.
- [ ] Panel por período/jurisdicción/categoría.
- [ ] Alertas de seguimientos pendientes.
- [ ] Modo capacitación separado de datos reales.
- [ ] Casos ficticios solo dentro del módulo de capacitación.

## Fase 8 — Distribución — PLANIFICADA
- [ ] Instalador Windows.
- [ ] `.exe` offline.
- [ ] Migraciones automáticas de SQLite.
- [ ] Recuperación ante errores.
- [ ] Actualizaciones firmadas.
- [ ] Documentación para ONG.

## QA
- [x] Tests unitarios del núcleo nuevo.
- [x] Compilación de `src` y `scripts` en CI.
- [x] Smoke test automatizado.
- [x] CI para Python 3.11, 3.12 y 3.13.
- [ ] Ejecución Windows real de UI.
- [ ] Prueba de empaquetado `.exe` en runner Windows.

## Criterios de calidad
- No inventar recursos, teléfonos ni normativa.
- No elevar urgencia por una palabra aislada.
- Mostrar por qué se llegó a una clasificación.
- Diferenciar información faltante de información negativa.
- Mantener trazabilidad de fuentes.
- No sustituir evaluación profesional.
