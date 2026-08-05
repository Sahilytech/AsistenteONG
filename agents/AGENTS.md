# AGENTS.md

Asistente de Triaje y Canalización — Documentación de agentes

Resumen
-------
Este documento describe los "agentes" (componentes autónomos/servicios) incluidos en AsistenteONG: su propósito, flujo de datos, requisitos para funcionar offline, consideraciones de seguridad y recomendaciones de despliegue en pendrive/dispositivo.

Objetivo del agente
-------------------
- Clasificar mensajes entrantes (texto transcrito de audios, mensajes de WhatsApp, formularios) según prioridad y riesgo.
- Detectar señales de urgencia (riesgo de vida, menores involucrados, violencia con lesiones, riesgo inminente) y marcar para atención prioritaria.
- Generar borradores de respuesta y pasos recomendados (contactos de emergencia, protocolos legales y de salud local) usando plantillas que se rellenan dinámicamente.
- Operar completamente sin conexión a Internet, preservando la privacidad de las personas asistidas.

Agentes incluidos
-----------------
1. Clasificador (local)
   - Tipo: modelo de clasificación de texto ligero (ej.: TinyText, modelos quantizados de Hugging Face, o variantes soporte ONNX/TFLite).
   - Entrada: texto plano del mensaje.
   - Salida: etiqueta de prioridad (alta / media / baja), banderas (menor involucrado, riesgo de vida, riesgo inmediato, necesidad legal).

2. Motor de plantillas (rules + IA ligera)
   - Tipo: motor determinista con reglas y plantillas parametrizadas; puede usar un modelo local para reescritura segura de texto.
   - Función: rellenar plantillas de respuesta con información contextual (servicios locales, teléfonos, pasos legales) sin enviar datos a servicios externos.

3. Actualizador de datos (sincronizador)
   - Tipo: componente que gestiona la actualización local de la base de datos cuando hay conexión.
   - Función: comprobar fuentes autorizadas (listas de salud pública, servicios sociales, números de emergencia) y descargar paquetes de actualización cifrados.
   - Modo offline: si no hay conexión, funciona con la última copia local verificada.

4. Interfaz de usuario (agente de presentación)
   - Tipo: componente de UI multiplataforma (Electron, Tauri o aplicación nativa según plataforma) que consume los servicios locales anteriores.
   - Función: presentar resultados, permitir revisión humana, editar respuestas y exportar (PDF, texto cifrado, impresión).

Cómo funciona sin conexión
--------------------------
- Todos los modelos y plantillas residirán en la máquina local en la carpeta `models/` y `data/`.
- La base de datos (SQLite o similar) contendrá: plantillas, recursos locales, leyes y contactos de emergencia.
- Procesamiento: al ingresar texto, el flujo es local — clasificación → plantillas → borrador — sin conexiones externas.
- Cuando haya conexión (Wi‑Fi/USB), el Actualizador puede sincronizar paquetes firmados para mantener datos actualizados.

Seguridad y privacidad
----------------------
- Nunca enviar texto de usuarios a servicios externos por defecto. Cualquier telemetría debe estar desactivada por defecto y solicitar autorización explícita.
- Cifrado en reposo: se recomienda cifrar la base de datos local si el dispositivo puede perderse (por ejemplo, SQLite cifrado con SQLCipher).
- Acceso: implementar autenticación local (PIN/contraseña) para el acceso a la aplicación.
- Registro: limitar logs sensibles; cuando existan, mantenerlos cifrados y con acceso restringido.

Actualización de la base de datos
---------------------------------
- Formato de paquete: ZIP/PAK firmado que contenga archivos JSON/CSV/SQLite con metadatos de versión y firma.
- Proceso de actualización:
  1. El usuario importa el paquete (desde Wi‑Fi o pendrive).
  2. La aplicación valida firma y versión.
  3. Si es válido, aplica cambios a la base de datos local manteniendo copia de respaldo.
- Fuentes recomendadas: ministerios de salud, líneas oficiales, ONGs autorizadas y organizaciones locales; documentar las URLs y la frecuencia de actualización en `docs/base_de_datos.md`.

Recomendaciones de despliegue
-----------------------------
- Empaquetado multiplataforma: usar Tauri o Electron para generar binarios para Windows, macOS y Linux; para Android/iOS considerar builds nativos o empaquetados.
- Distribución offline: generar un instalador portable (.exe/.AppImage/.zip) que incluya binarios, modelos y datos iniciales.
- Actualización incremental: permitir que el dispositivo reciba paquetes de actualización por Wi‑Fi o por importación manual desde pendrive.

Interfaz y accesibilidad
------------------------
- Paleta de colores sugerida: celeste (#00AEEF), blanco (#FFFFFF) y negro (#000000). Soporte de modo claro/oscuro con contraste accesible.
- Accesibilidad: textos reajustables, compatibilidad con lectores de pantalla y navegación por teclado.
- UI: botones grandes para uso en pantallas táctiles, confirmaciones claras antes de enviar datos sensibles.

Integración con los archivos del repositorio
--------------------------------------------
- models/: modelos locales quantizados y convertidos a formatos ligeros.
- data/: plantillas, recursos, leyes, emergencias.
- src/ui/: componentes de la interfaz que consumen los agentes locales.
- src/ai/: código de inferencia y wrapper para los modelos locales.
- updater/: código responsable de validar e instalar paquetes de actualización.

Cómo probar los agentes
-----------------------
- Incluir un conjunto de mensajes de prueba en `tests/fixtures/` con casos de alta, media y baja prioridad.
- Automatizar pruebas unitarias para el clasificador (precision/recall) y pruebas end‑to‑end para la generación de borradores y la firma de paquetes.

Créditos y autoría
------------------
La creadora del proyecto es: Sarah Lee Olivera.

Nota sobre la foto: si querés mostrar una foto en la sección "Quién lo creó" dentro de la UI o documentación, añade el archivo de imagen en `assets/author.jpg` (o `assets/author.png`) y referencia en Markdown así:

```markdown
![Autor](assets/author.jpg)
```

(No estoy verificando ni identificando la imagen; sólo incluyo la ruta sugerida para que la uses en la documentación o la UI.)

Contribuir
---------
- Abrir Issues por cada función nueva o bug.
- Pull Requests con tests y documentación actualizada.
- Revisá `CONTRIBUTING.md` para las pautas del flujo de trabajo.

Preguntas frecuentes (rápidas)
-----------------------------
- ¿El sistema envía datos a la nube? No por defecto. Solo sincroniza paquetes cifrados de datos cuando el usuario lo autoriza.
- ¿Funciona en pendrive? Sí, si se empaqueta como aplicación portable y la base de datos está cifrada o protegida.
- ¿Qué pasa si se actualizan leyes locales? El Actualizador aplica paquetes firmados; la versión y fecha quedan registradas en la base de datos.

Contacto y enlaces útiles
------------------------
- Documentación principal: `docs/`
- Roadmap: `docs/roadmap.md`
- Guía de seguridad: `docs/seguridad.md`

---
Generado por Sahilytech / AsistenteONG — AGENTS.md
