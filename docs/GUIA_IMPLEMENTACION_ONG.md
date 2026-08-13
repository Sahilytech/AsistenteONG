# Implementación en una ONG

## Puesta en marcha

### Día 1 — preparación
- Definir institución responsable.
- Designar responsable del sistema.
- Definir roles: administrador, profesional, operador y consulta.
- Definir qué información puede registrarse.
- Definir política interna de backups y retención.

### Día 2 — configuración
- Instalar Asistente ONG en un equipo autorizado.
- Completar datos institucionales.
- Configurar seguridad de sesión.
- Crear un backup de prueba y comprobar que puede restaurarse.
- Cargar únicamente documentación institucional aprobada.

### Día 3 — migración
- Copiar la base histórica a un archivo de trabajo autorizado.
- Ejecutar vista previa de XLSX/PDF.
- Revisar mapeo de columnas.
- Detectar personas existentes.
- Confirmar la importación de forma explícita.
- Verificar una muestra antes de utilizar datos reales.

## Prueba de aceptación
Antes de producción, comprobar:

- [ ] Crear persona.
- [ ] Crear dos casos para la misma persona.
- [ ] Ver ambos casos en la línea temporal.
- [ ] Importar PDF y verlo en Biblioteca.
- [ ] Buscar una frase del PDF.
- [ ] Asociar evidencia a un análisis sin convertirla en decisión.
- [ ] Vista previa de XLSX.
- [ ] Confirmación explícita antes de persistir una importación.
- [ ] Crear seguimiento.
- [ ] Crear una tarea.
- [ ] Bloqueo y desbloqueo de sesión.
- [ ] Backup cifrado y restauración.
- [ ] Exportación anonimizada.
- [ ] Comprobar auditoría.

## Política de uso
El sistema es una herramienta de apoyo operativo. La revisión humana permanece obligatoria. La organización debe definir sus propios protocolos profesionales y jurídicos y mantener actualizada la documentación de referencia.

## Despliegue nacional
Para operar en distintas provincias, cada instalación debe configurar jurisdicción y fuentes aplicables. No se debe asumir que un recurso de una jurisdicción sirve para otra. La aplicación conserva las funciones generales y permite que la organización mantenga sus fuentes oficiales.
