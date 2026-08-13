# Guía de usuario — Asistente ONG

## 1. Qué es

Asistente ONG es una herramienta local de apoyo para organizar personas, casos, documentación, análisis contextual y seguimiento. No reemplaza la revisión profesional ni toma decisiones por cuenta propia.

## 2. Primer arranque

1. Abrí `AsistenteONG.exe`.
2. Esperá la pantalla de inicio; la ventana principal se abre maximizada.
3. Completá el tutorial inicial.
4. Entrá en **Configuración** y cargá, si corresponde:
   - entidad emisora;
   - profesional de referencia;
   - matrícula/colegiatura;
   - destinatario habitual.
5. Revisá **Seguridad** antes de cargar información real.

La aplicación comienza sin casos ni ejemplos precargados.

## 3. Flujo recomendado

`Persona → Caso → Análisis → Evidencia → Revisión profesional → Acción/derivación → Seguimiento → Cierre`

### Persona

Una persona se registra una sola vez. Los nuevos contactos se agregan como nuevos casos dentro de su historial.

### Caso

Escribí el relato y los datos estrictamente necesarios. Guardá el caso y revisá el resultado antes de actuar.

### Análisis

El sistema puede señalar categorías, señales, preguntas pendientes, coincidencias históricas y documentación relevante. Las coincidencias son **evidencia de apoyo**, no decisiones.

### Biblioteca

Importá PDFs institucionales, protocolos, reglamentos o material de referencia. La biblioteca puede procesarlos localmente y recuperar fragmentos relevantes. La procedencia y página deben conservarse para revisión.

### Seguimiento

Registrá tareas, responsables, fechas, derivaciones y estado. La Agenda concentra las fechas existentes.

## 4. Importar una base existente

Para una planilla de personas/casos:

1. Abrí la función de importación.
2. Seleccioná XLSX u otro formato admitido.
3. Revisá la vista previa y el mapeo de columnas.
4. Confirmá explícitamente la importación.
5. Verificá personas existentes antes de crear nuevas.

La vista previa no debe persistir información hasta que el operador confirme.

## 5. Documentos PDF

Los PDFs se procesan para revisión. Un documento puede aportar evidencia para un caso, pero no modifica automáticamente los datos de la persona ni decide una intervención.

## 6. Seguridad

- Mantener el equipo protegido con contraseña.
- Usar bloqueo de sesión cuando corresponda.
- Hacer backups cifrados y probar periódicamente su restauración.
- No compartir la carpeta de datos con usuarios no autorizados.
- Usar únicamente la conectividad externa que la organización haya habilitado.

## 7. Revisión profesional

Antes de emitir un informe, derivar, cerrar o tomar una medida sensible, revisar:

- relato original;
- datos de la persona;
- historial;
- evidencia documental;
- fuentes y fechas;
- señales detectadas;
- información faltante;
- propuesta de acción.

## 8. Qué NO hace el sistema

No diagnostica, no reemplaza asesoramiento jurídico, no determina por sí solo situaciones de riesgo y no convierte una coincidencia documental o histórica en una decisión automática.

## 9. Cuando algo parece no funcionar

1. Revisá que el caso/persona esté seleccionado.
2. Recargá Biblioteca si agregaste documentos.
3. Revisá Seguridad y permisos.
4. Cerrá y abrí la aplicación si un panel quedó desactualizado.
5. Ejecutá `python -m pytest` si estás trabajando desde el código.
6. Conservá el mensaje de error para soporte.

## 10. Atajos

- `Ctrl + N`: nuevo caso.
- `Ctrl + B`: Biblioteca.
- `Ctrl + K`: búsqueda/análisis cuando el panel lo admita.
- `Esc`: cerrar diálogos.
