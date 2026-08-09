# Guía funcional de la interfaz

## Navegación lateral

- **Nuevo caso**: inicia un expediente sin datos de ejemplo.
- **Inicio**: resumen operativo: casos recientes, pendientes y acceso rápido.
- **Casos**: alta, búsqueda, filtros, apertura y edición de expedientes.
- **Caso + Informe**: une el relato con el informe social; permite completar identificación, convivencia, economía, vivienda, salud/educación, valoración y propuesta.
- **Análisis**: muestra el razonamiento del motor, señales, contexto, información faltante, prioridad orientativa y fuentes. No decide por una palabra aislada.
- **Seguimiento**: acciones pendientes, responsables, fechas y estados.
- **Recursos**: búsqueda y catálogo de recursos; cada recurso verificable debe conservar fuente, jurisdicción y fecha de actualización.
- **Biblioteca**: documentos y conocimiento local; permite buscar material guardado para trabajar offline.
- **Agenda**: próximos seguimientos, revisiones y vencimientos.
- **Seguridad**: estado de privacidad, auditoría, sesiones y herramientas de protección.
- **Configuración**: institución, profesional, preferencias de análisis, fuentes permitidas y datos que se aplican a nuevos informes.
- **Ayuda**: explicación de funciones, criterios, límites y resolución de problemas.
- **Acerca de**: proyecto, creadora, NubiWorks, arquitectura, privacidad y propósito social.

## Principio de diseño

Cada pantalla tiene una tarea. La navegación no debe duplicar acciones. Un botón debe indicar claramente qué modifica o abre. Las acciones destructivas requieren confirmación. No se incluyen casos de ejemplo en producción.

## Flujo principal

Nuevo caso → relato → análisis → Caso + Informe → valoración → intervención → recurso/derivación → seguimiento → cierre.

El análisis automático es orientativo y siempre muestra información faltante y necesidad de revisión profesional.

## Recursos online

Cuando hay conectividad, el módulo Recursos/Biblioteca puede consultar únicamente fuentes oficiales configuradas. La información recuperada debe quedar identificada con URL/fuente, fecha de consulta y jurisdicción antes de pasar a memoria local.

## Accesibilidad visual

Modo claro únicamente. Fondo mayoritariamente blanco, texto negro, azul institucional `#0e98d6`, tarjetas con jerarquía clara, textos ajustables y scroll para evitar cortes.
