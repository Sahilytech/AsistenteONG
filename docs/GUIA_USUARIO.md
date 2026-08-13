# Guía de usuario — Asistente ONG

## Primer inicio
La aplicación comienza vacía: no incluye personas, casos ni expedientes de ejemplo.

Orden recomendado:
1. Configuración → completar datos institucionales.
2. Seguridad → revisar protección de sesión y backup.
3. Biblioteca → cargar protocolos, guías y normativa autorizada.
4. Personas → importar una base existente mediante vista previa o crear una persona.
5. Casos → registrar cada atención como un caso separado.
6. Análisis → revisar señales, preguntas, historial y evidencia.
7. Caso + Informe → completar y revisar el informe.
8. Seguimiento / Agenda → registrar derivaciones, tareas y fechas.

## Personas y casos
Una persona tiene un único registro y puede tener muchos casos. Una nueva atención no requiere duplicar a la persona.

Cada caso conserva su propia fecha, relato, análisis, evidencia, seguimiento y estado.

## Biblioteca
Flujo recomendado: **Importar → Vista previa → Procesar → Revisar procedencia → Recargar índice → Buscar → Usar como evidencia.**

Los documentos no son autoridad automática. Una coincidencia se muestra como evidencia para revisión humana. Los PDF con texto se extraen localmente; los documentos escaneados pueden requerir OCR.

## Importación de personas
La planilla XLSX pasa primero por vista previa y mapeo de columnas. Se muestran coincidencias con personas existentes. La persistencia debe confirmarse explícitamente.

Las columnas desconocidas no deben interpretarse por suposición: el operador decide el campo correspondiente.

## Análisis
El análisis puede relacionar relato actual, historial, señales, documentación local, fuentes oficiales permitidas y datos faltantes. El resultado es apoyo para el equipo y requiere revisión profesional.

## Seguridad
El modo base es local. La organización debe usar una frase de desbloqueo robusta, bloquear el equipo, realizar backups cifrados en medios autorizados, limitar permisos por rol y evitar copias de expedientes en servicios no autorizados.

## Atajos
- Ctrl + N: nuevo caso.
- Ctrl + B: Biblioteca.
- Ctrl + K: Análisis.
- Esc: cerrar diálogo activo.

## Si algo no aparece
1. Comprobar que el archivo fue aceptado.
2. Revisar la vista previa.
3. Usar Recargar en Biblioteca.
4. Comprobar que el PDF contiene texto extraíble.
5. Revisar auditoría si corresponde.
6. No volver a importar una persona sin comprobar primero si ya existe.
