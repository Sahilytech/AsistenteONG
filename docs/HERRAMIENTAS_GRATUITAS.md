# Herramientas gratuitas recomendadas

La aplicación está pensada para funcionar sin servicios pagos ni APIs obligatorias.

## Ya implementadas

- **pypdf**: lectura local de PDFs digitales.
- **SQLite**: almacenamiento local de casos y biblioteca.
- **ReportLab**: generación de informes.
- **PyInstaller**: preparación del ejecutable para Windows.
- **CustomTkinter**: interfaz de escritorio.

## Mejoras gratuitas que conviene mantener

1. **Importación múltiple de PDF**: permite cargar protocolos de la organización de una sola vez.
2. **Carpeta `data/library`**: permite copiar nuevos PDFs y recargar la biblioteca sin depender de Internet.
3. **Búsqueda local**: consulta recursos y documentos sin enviar el relato del caso a servicios externos.
4. **Tutorial interactivo**: enseña el recorrido y puede abrir directamente cada sección.
5. **Sistema vacío por defecto**: no incluye casos ficticios ni documentos de demostración.
6. **Trazabilidad local**: cada fuente conserva nombre, origen y fecha de guardado.

## Próxima mejora opcional

Se puede agregar OCR para PDFs escaneados. Para mantener el instalador liviano, conviene tratarlo como módulo opcional y no como dependencia obligatoria.
