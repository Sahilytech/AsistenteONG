# AsistenteONG

Herramienta de inteligencia social para transformar relatos desestructurados en información procesable que acelera la intervención profesional en organizaciones sociales.

[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-3776ab?style=flat-square)](https://www.python.org/)
[![Estado v0.9](https://img.shields.io/badge/Estado-v0.9%20Estable-brightgreen?style=flat-square)](#estado-actual)
[![Tests Automatizados](https://img.shields.io/badge/Tests-71%20Pasando-brightgreen?style=flat-square)](#testing)
[![Licencia MIT](https://img.shields.io/badge/Licencia-MIT-blue?style=flat-square)](LICENSE)
[![Ético y Offline](https://img.shields.io/badge/Offline-100%25%20Local-darkgreen?style=flat-square)](#seguridad-y-privacidad)

---

## Presentación del Proyecto

AsistenteONG es una plataforma de escritorio, 100% offline y completamente gratuita, diseñada para organizaciones sociales, líneas de ayuda, refugios y ONGs que reciben y gestionan consultas, relatos y solicitudes de asistencia.

**Concepto central:** procesar información social desestructurada para convertirla en análisis organizado, accionable y auditado, preservando la responsabilidad profesional humana en cada decisión.

### Para Organizaciones Que Enfrentan:

- Volumen alto de mensajes, relatos y consultas simultáneas
- Información fragmentaria o ambigua que requiere triaje rápido
- Necesidad de identificar indicadores de riesgo sin reemplazar criterio profesional
- Documentación estructurada (informes sociales, legales, psicológicos)
- Seguimiento longitudinal de personas y casos sin duplicación
- Privacidad garantizada: datos que nunca salen de la organización

---

## El Problema

Las organizaciones sociales enfrentan un desafío operativo fundamental:

**Volumen vs. Capacidad:** mensajes, relatos, consultas legales, laborales y sociales llegan sin estructura ni prioridad. Procesarlos manualmente consume horas que podrían dedicarse a intervención directa.

**Inconsistencia Humana:** cada operador interpreta y clasifica diferente. Sin estandarización, crece el riesgo de omisiones críticas o interpretaciones sesgadas.

**Presión Temporal:** indicadores de riesgo pueden pasar desapercibidos en relatos extensos. Cada minuto de demora en triaje es un minuto sin acción.

**Escalabilidad Limitada:** una ONG con 50 casos mensuales puede operarse manualmente; con 500 mensuales, el sistema colapsa. No hay opción: o compras tecnología comercial costosa o pierdes capacidad de respuesta.

**Riesgo de Privacidad:** datos sensibles de víctimas no pueden ir a servidores externos. Necesitan estar bajo control local de la organización.

---

## La Solución: Apoyo Profesional Estructurado

AsistenteONG no reemplaza trabajadores sociales, abogados, psicólogos ni operadores. **Amplifica su capacidad.**

La herramienta normaliza el flujo desde la consulta inicial hasta la derivación, el seguimiento y el cierre:

- **Análisis Contextual Inmediato:** procesa el relato en menos de 500ms, extrae indicadores de riesgo y genera evidencia de apoyo
- **Clasificación de Urgencia:** asigna nivel (Muy Alta, Alta, Media, Baja) basado en patrones, pero requiere validación profesional
- **Detección de Información Faltante:** identifica qué datos critticos faltan para diagnóstico o intervención
- **Historial Longitudinal:** mantiene un registro único de la persona y sus casos, detectando patrones recurrentes
- **Generación de Documentos:** plantillas estructuradas para informes sociales, derivaciones y seguimientos
- **Auditoría Completa:** registro de quién accedió qué, cuándo y por qué. Transparencia garantizada.
- **Privacidad Absoluta:** operación 100% offline, base de datos cifrada, datos que nunca abandonan el equipo de la organización

---

## Características Principales

### Triaje Inteligente de Casos

Análisis contextual que procesa cada relato mediante:

- Detección de indicadores de riesgo por categoría (violencia, menores, urgencia médica, derechos laborales, habitabilidad)
- Clasificación automática en 4 niveles de urgencia
- Búsqueda de +320 palabras clave organizadas en 9 categorías temáticas
- Identificación de información faltante relevante para seguimiento
- Coincidencias con historial longitudinal de la persona

**Garantía de Proceso:** todas las coincidencias se presentan como evidencia de apoyo, nunca como decisiones automatizadas. La acción siempre requiere validación profesional.

### Gestión de Personas y Casos

- Registro único de persona (previene duplicación) con múltiples casos asociados
- Historial longitudinal sin sobrescritura
- Importación de datos XLSX en modo revisión explícita (no automática)
- Búsqueda, filtrado y reporte de contacto opcional cuando esté autorizado
- Sistema de IDs automáticos con trazabilidad (CASE-YYYYMM-XXXXX)

### Informe Social Profesional

Generador estructurado de informes en 7 secciones normalizadas:

1. Datos del profesional e institución (configurable)
2. Identificación de la persona
3. Unidad de convivencia y dinámica familiar (genograma)
4. Situación socioeconómica y laboral
5. Habitabilidad, servicios y entorno
6. Salud y educación
7. Diagnóstico, valoración y propuesta de intervención

Configuración institucional reutilizable: firma, destinatario, entidad, logos, datos de envío.

### Biblioteca de Documentos Institucionales

- Importación de PDFs institucionales (protocolos, leyes, recursos, guías)
- Procesamiento local con extracción de fragmentos relevantes (chunking)
- Preservación de procedencia: archivo y página siempre identificados
- Vinculación con casos específicos
- OCR opcional para documentos escaneados

### Seguimiento, Derivaciones y Agenda

- Tareas con responsables, fechas de vencimiento y recordatorios
- Derivaciones a servicios externos (líneas de crisis, refugios, centros legales)
- Calendario integrado con vistas por fecha, prioridad y responsable
- Estados de caso: abierto, en seguimiento, cerrado
- Historial de cambios en cada derivación y seguimiento

### Gestión de Seguridad y Acceso

- Base de datos SQLite cifrada con AES-256 en reposo
- Autenticación por usuario con roles y permisos granulares
- Bloqueo automático de sesión tras 15 minutos de inactividad
- Backup cifrado descargable (ZIP protegido)
- Auditoría completa: quién, qué, cuándo, detalles de cada acción
- Exportación anonimizada para análisis agregado sin datos personales
- Validación de integridad de archivos importados

### Operación 100% Offline

- Aplicación de escritorio para Windows (ejecutable standalone)
- No requiere Python instalado en máquina de usuario
- No requiere conexión a internet en funcionamiento normal
- Base de datos local (SQLite) como único almacenamiento
- Backup manual descargable en USB o medio externo
- Ningún dato sale del equipo sin intención explícita

---

## Arquitectura Técnica

### Capas del Sistema

```
AsistenteONG
├── Capa de Presentación (CustomTkinter 5.2+)
│   ├── Interfaz gráfica responsive
│   ├── Temas claro y oscuro
│   ├── Paneles especializados por función
│   └── Visualización de análisis y resultados
│
├── Capa de Lógica de Negocio
│   ├── Procesamiento de texto y análisis
│   ├── Clasificación de urgencia
│   ├── Extracción de indicadores de riesgo
│   ├── Generación de informes
│   └── Gestión de casos y personas
│
├── Capa de Persistencia (SQLite 3)
│   ├── Personas y casos
│   ├── Análisis y resultados almacenados
│   ├── Documentos y referencias
│   ├── Usuarios, roles y permisos
│   └── Logs de auditoría
│
└── Capa de Utilidades
    ├── Criptografía (AES-256, PBKDF2, bcrypt)
    ├── Procesamiento de PDFs (importación, OCR)
    ├── Generación de informes (ReportLab)
    ├── Manejo de XLSX (importación de datos)
    ├── Backups cifrados
    └── Actualización de versiones
```

### Flujo de Procesamiento de un Caso

```
Relato o Mensaje Ingresado
          ↓
  Normalización de Texto
          ↓
  Análisis Contextual
          ↓
    Extracción de           Búsqueda de
    Palabras Clave    →     Indicadores de
          ↓                 Riesgo
          ↓                 ↓
   Clasificación de Urgencia
   (Muy Alta / Alta / Media / Baja)
          ↓
    Búsqueda de Información
    Faltante Crítica
          ↓
  Comparación con Historial
  de la Persona
          ↓
   Generación de Evidencia
   y Propuesta de Respuesta
          ↓
  Presentación al Profesional
          ↓
  REVISIÓN Y DECISIÓN HUMANA
          ↓
  Registro, Seguimiento, Cierre
```

### Flujo de Gestión de Casos

- **Entrada:** ingreso manual o importación desde XLSX
- **Análisis:** procesamiento automático local (sin APIs externas)
- **Validación:** revisión profesional obligatoria
- **Documentación:** generación de informes estructurados
- **Seguimiento:** tareas, derivaciones, recordatorios
- **Cierre:** registro de resolución y auditoría
- **Exportación:** datos anonimizados para análisis agregado

---

## Stack Tecnológico

| Capa | Tecnología | Versión | Propósito |
|------|-----------|---------|----------|
| **Interfaz Gráfica** | CustomTkinter | 5.2+ | UI desktop responsiva con temas |
| **Base de Datos** | SQLite | 3 | Almacenamiento local cifrado |
| **Criptografía** | cryptography | 41+ | AES-256, PBKDF2, bcrypt |
| **PDFs** | ReportLab, PyPDF | 4.0+, 5.0+ | Generación e importación |
| **Importación XLSX** | openpyxl | 3.1+ | Carga de datos estructurados |
| **Lenguaje Base** | Python | 3.11+ | Lógica principal |
| **Compilación a EXE** | PyInstaller | 6.0+ | Generación de ejecutable Windows |
| **OCR (Opcional)** | pytesseract, PyMuPDF | 0.3.13+, 1.24+ | Lectura de PDFs escaneados |
| **Testing** | pytest | 7.0+ | Automatización de tests |
| **Herramientas** | black, flake8, mypy | — | Formato, lint, type checking |

---

## Estado Actual: v0.9 - Producción Estable

El proyecto ha alcanzado funcionalidad productiva con 71 tests automatizados pasando en Python 3.11, 3.12 y 3.13.

### Características Implementadas

- ✅ Entrada de casos con análisis local automático
- ✅ Gestión de personas con historial longitudinal sin duplicación
- ✅ Clasificación de urgencia en 4 niveles
- ✅ Detección de indicadores de riesgo (+320 palabras clave)
- ✅ Informe social profesional estructurado en 7 secciones
- ✅ Biblioteca de documentos PDF con búsqueda local
- ✅ Seguimiento, tareas, derivaciones y agenda integrada
- ✅ Roles, permisos y bloqueo de sesión
- ✅ Base de datos cifrada con AES-256
- ✅ Backups cifrados y descargables
- ✅ Auditoría completa de acciones
- ✅ Importación XLSX con revisión explícita
- ✅ Tutorial interactivo de primer uso
- ✅ Exportación anonimizada de datos
- ✅ Ejecutable Windows standalone
- ✅ Temas claro y oscuro

### En Desarrollo

- OCR automático para PDFs escaneados (parcialmente implementado)
- Soporte multi-idioma (arquitectura preparada)

---

## Instalación

### Para Usuarios Finales (Windows)

1. **Descargar** el instalador desde [Releases](https://github.com/Sahilytech/AsistenteONG/releases)
2. **Ejecutar** el archivo `AsistenteONG-Setup-*.exe`
3. **Seguir** el asistente de instalación
4. **Abrir** la aplicación desde el menú de inicio

**No requiere instalación de Python ni dependencias adicionales en la máquina.**

### Para Desarrolladores

```bash
# Clonar el repositorio
git clone https://github.com/Sahilytech/AsistenteONG.git
cd AsistenteONG

# Crear entorno virtual
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/macOS

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la aplicación
python -m src.main
```

**Documentación detallada en [INSTALL.md](INSTALL.md)**

---

## Uso Rápido

1. **Iniciar** la aplicación
2. **Completar** el tutorial de primer uso (configura datos institucionales)
3. **Ir a Configuración** e ingresar:
   - Nombre de la institución
   - Datos del profesional
   - Palabras clave específicas (opcional)
   - Recursos locales
4. **Crear una persona** nueva con datos básicos
5. **Agregar un caso** con el relato, mensaje o consulta
6. **Iniciar análisis** (genera análisis automático en <500ms)
7. **Revisar evidencia:** indicadores detectados, información faltante, coincidencias históricas
8. **Validar o rechazar** propuestas de análisis
9. **Registrar seguimiento:** tareas, derivaciones, próximas acciones
10. **Realizar backup** regularmente de la base de datos cifrada

**Guías completas disponibles:**
- [USER_GUIDE.md](USER_GUIDE.md) - Guía de usuario
- [docs/](docs/) - Documentación técnica

---

## Development y Testing

### Ejecutar Tests

```bash
# Suite completa de tests
python -m pytest tests/ -v

# Con reporte de cobertura
python -m pytest tests/ -v --cov=src

# Generar reporte HTML
pytest tests/ --cov=src --cov-report=html
```

**Estado:** 71 tests pasando en Python 3.11, 3.12, 3.13

### Code Quality

```bash
# Formato automático
black src/ tests/

# Linting
flake8 src/ tests/ --max-line-length=127

# Type checking
mypy src/ --ignore-missing-imports
```

### Compilar a Ejecutable Windows

```bash
# Script de build
build_exe.bat

# Resultado: dist/AsistenteONG.exe
# Tamaño aproximado: 150-200 MB (incluye Python embebido)
```

**Documentación de testing en [docs/testing.md](docs/testing.md)**

---

## Configuración

### Variables de Entorno

```bash
# Activar OCR para procesamiento de PDFs escaneados
ASISTENTE_OCR=1

# Ruta personalizada de almacenamiento de datos
# Por defecto: ./data/
ASISTENTE_DATA_PATH=/ruta/personalizada
```

### Configuración en Aplicación

Toda configuración se realiza mediante la interfaz gráfica:

- Datos institucionales (nombre, logo, ubicación, contacto)
- Datos del profesional (nombre, rol, firma digital)
- Palabras clave adicionales por categoría
- Recursos locales (teléfonos, direcciones, horarios)
- Preferencias de tema (claro/oscuro)
- Políticas de bloqueo y timeout

La configuración se persiste en la base de datos local cifrada.

---

## Seguridad y Privacidad

### Principios Fundamentales

**Local First:** Todos los datos residen en la máquina local por defecto. Cero sincronización con la nube. Cero servidores externos obligatorios.

**Cifrado en Reposo:** Base de datos protegida con AES-256-CBC. Derivación de clave mediante PBKDF2 (100,000 iteraciones). Contraseñas hasheadas con bcrypt (12 rounds).

**Auditoría Exhaustiva:** Registro completo de accesos, modificaciones y exportaciones. Cada acción incluye: usuario, timestamp, acción, registro afectado, cambios específicos.

**Sin Terceros Involuntarios:** No hay integraciones externas, APIs de terceros, o recolección de datos a menos que la organización lo habilite explícitamente.

### Checklist de Seguridad para Administradores

- [ ] Usar contraseña fuerte en la cuenta de usuario del equipo
- [ ] Activar bloqueo de sesión cuando se deja la máquina desatendida
- [ ] Realizar backups cifrados regularmente
- [ ] Probar periódicamente restauración de backups
- [ ] No compartir credenciales de acceso a la aplicación
- [ ] Limitar acceso físico al equipo a personal autorizado
- [ ] Revisar auditoría de accesos periódicamente
- [ ] Documentar procedimientos de escalada para casos sensibles

### Responsabilidades de la Organización

La privacidad de datos depende de la organización implementar:

1. Control de acceso físico al equipo
2. Políticas de contraseña y cambio periódico
3. Procedimientos de backup y recuperación
4. Auditoría de accesos (revisar logs regularmente)
5. Políticas de uso y confidencialidad con personal
6. Coordinación con protección de datos de la jurisdicción

---

## Limitaciones Explícitas

AsistenteONG **NO:**

- Realiza diagnósticos médicos, psicológicos ni jurídicos
- Toma decisiones automáticas sobre intervenciones o protección
- Reemplaza validación de profesionales capacitados
- Convierte una coincidencia textual en una conclusión clínica o legal
- Funciona sin revisión humana posterior
- Garantiza cobertura de todos los indicadores de riesgo posibles
- Sustituye asesoramiento especializado de cualquier tipo

**Responsabilidad:** toda acción sensible debe ser validada y autorizada por profesionales capacitados de la organización, siguiendo protocolos internos y marco legal aplicable.

---

## Estructura del Proyecto

```
AsistenteONG/
├── src/
│   ├── main.py                       # Punto de entrada
│   ├── ui/                           # Interfaz gráfica
│   │   ├── main_window.py
│   │   ├── case_input.py
│   │   ├── results_panel.py
│   │   ├── social_report_panel.py
│   │   ├── resources_panel.py
│   │   ├── config_panel.py
│   │   └── styles.py
│   ├── core/                         # Lógica de negocio
│   │   ├── case_workflow.py
│   │   ├── analysis.py
│   │   ├── reasoning.py
│   │   └── ...
│   ├── database/                     # Base de datos
│   │   ├── schema.py
│   │   ├── models.py
│   │   └── queries.py
│   ├── security/                     # Seguridad
│   │   ├── crypto.py
│   │   ├── permissions.py
│   │   └── audit.py
│   └── utils/                        # Utilidades
│       ├── pdf_processor.py
│       ├── report_generator.py
│       ├── backup.py
│       └── ...
├── tests/                            # Suite de tests
│   ├── test_core_*.py
│   ├── test_security.py
│   ├── test_social_analyzer.py
│   └── ...
├── docs/                             # Documentación técnica
│   ├── GUIA_USUARIO_FINAL.md
│   ├── ai.md
│   ├── ui.md
│   └── testing.md
├── assets/                           # Iconos y recursos
├── build/                            # Artefactos de compilación
├── installer/                        # Script de instalador
├── requirements.txt                  # Dependencias Python
├── LICENSE                           # Licencia MIT
├── LICENSE_SOCIAL.md                 # Licencia Ética 2026
├── README.md                         # Este archivo
├── INSTALL.md                        # Guía de instalación
├── USER_GUIDE.md                     # Guía de usuario
├── CHANGELOG.md                      # Historial de versiones
└── .github/workflows/                # CI/CD con GitHub Actions
    ├── core-tests.yml
    ├── windows-build.yml
    └── build.yml
```

---

## Roadmap

### v0.9 (Actual)

- ✅ Análisis contextual de casos
- ✅ Gestión de personas y casos
- ✅ Clasificación de urgencia
- ✅ Detección de indicadores de riesgo
- ✅ Informe social profesional
- ✅ Biblioteca documental
- ✅ Seguimiento y agenda
- ✅ Seguridad y auditoría
- ✅ Ejecutable Windows
- ✅ 71 tests automatizados

### v1.0 (Próxima)

- Piloto con ONGs reales
- Optimización de performance
- Manual en PDF descargable
- Autenticación 2FA (TOTP) opcional
- Firma digital RSA en paquetes de actualización

### v1.1+

- Soporte multi-idioma
- Temas adicionales personalizables
- Exportación a formatos específicos por país
- Integración opcional con sistemas externos (previa solicitud de ONG)

---

## Contribuir

Las contribuciones son bienvenidas. Proceso:

1. **Fork** el repositorio
2. **Crea una rama** con tu cambio: `git checkout -b feature/descripcion`
3. **Commits descriptivos** que expliquen qué y por qué
4. **Tests** que cubran el cambio (ejecutar `pytest tests/`)
5. **Pull request** con descripción detallada del problema y solución

**Antes de contribuir:**
- Lee [CONTRIBUTING.md](CONTRIBUTING.md)
- Revisa issues abiertos para no duplicar trabajo
- Discute cambios mayores en issues primero

---

## Casos de Uso

### Línea de Ayuda Telefónica / Chat

Operador recibe llamada o mensaje de persona en situación de crisis. Ingresa el relato en tiempo real. El sistema:
- Clasifica urgencia inmediatamente
- Detecta indicadores de riesgo
- Sugiere protocolo de respuesta
- Genera propuesta de derivación

El operador valida, completa información faltante y ejecuta la intervención.

**Ganancia:** reducción de 70% en tiempo de triaje, estandarización de respuestas, auditoría completa.

### Centro de Asesoría Legal

Abogado recibe solicitud por WhatsApp, email o presencial. Analiza caso:
- El sistema busca coincidencias en historial de la persona
- Examina biblioteca de jurisprudencia y protocolos locales
- Identifica información faltante para fundamento legal
- Sugiere argumentación con fuentes

El abogado revisa, valida y redacta dictamen con apoyo del análisis.

**Ganancia:** reducción de 50% en tiempo de investigación, trazabilidad de precedentes, documentación estandarizada.

### Refugio para Víctimas de Violencia

Trabajadora social documenta ingreso de persona en riesgo:
- Ingresa información disponible (relato, antecedentes)
- El sistema detecta indicadores de riesgo severo
- Integra historial previo si existe
- Genera informe social preliminar

Profesional completa evaluación, firma informe y define plan de protección.

**Ganancia:** documentación estructurada inmediata, evaluación de riesgos sistematizada, auditoría de decisiones.

### Organización Multidisciplinaria

Equipo de psicólogos, trabajadores sociales, abogados accede simultáneamente (con permisos granulares):
- Cada profesional ve su perspectiva especializada
- Comentarios y notas compartidas
- Auditoría completa de quién vio qué y cuándo
- Derivaciones cruzadas sin duplicación

**Ganancia:** coordinación sin fricción, responsabilidad clara, privacidad garantizada.

---

## Licencia

### Licencia MIT

El código fuente está bajo [Licencia MIT](LICENSE) - libre para usar, modificar y distribuir comercialmente si se respetan los términos.

### Licencia Social Ética 2026

Además de la licencia MIT, el proyecto incluye [LICENSE_SOCIAL.md](LICENSE_SOCIAL.md) - restricciones éticas adicionales que protegen:

- **Prohibición de venta:** software 100% gratis, nunca comercializable
- **Protección de atribución:** crédito permanente a creadora
- **Garantía de privacidad:** datos nunca salen del equipo local
- **Enfoque social:** restricción de uso ético obligatoria
- **Transparencia:** código abierto, auditable, sin "backend" secreto

La licencia social es voluntaria pero refleja el compromiso del proyecto.

---

## Autor

**Sarah Lee Olivera**

Desarrolladora comprometida con tecnología cívica, justicia social y transformación de organizaciones sociales mediante herramientas éticas y accesibles.

- GitHub: [@Sahilytech](https://github.com/Sahilytech)
- Email: sarahleeoliveraok@gmail.com
- Repositorio: [github.com/Sahilytech/AsistenteONG](https://github.com/Sahilytech/AsistenteONG)

---

## Soporte

- **Documentación:** [docs/](docs/)
- **Guía de Usuario:** [USER_GUIDE.md](USER_GUIDE.md)
- **Instalación:** [INSTALL.md](INSTALL.md)
- **Issues y Bugs:** [GitHub Issues](https://github.com/Sahilytech/AsistenteONG/issues)
- **Discusiones:** [GitHub Discussions](https://github.com/Sahilytech/AsistenteONG/discussions)

---

## Reconocimientos

Diseñado y desarrollado con compromiso hacia organizaciones sociales que trabajan en primera línea por protección, derechos y bienestar.

Este software existe porque la tecnología puede servir a la justicia social.

---

**AsistenteONG v0.9** — Inteligencia social para acelerar intervención profesional, sin reemplazar responsabilidad humana.
