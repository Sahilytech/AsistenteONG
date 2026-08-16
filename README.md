# AsistenteONG

> Procesar información social compleja en orientación estructurada y accionable. Tecnología ética, offline, diseñada para organizaciones que protegen.

[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-3776ab?style=flat-square)](https://www.python.org/)
[![Estado v0.9](https://img.shields.io/badge/Estado-v0.9%20Estable-brightgreen?style=flat-square)](#estado-actual)
[![Licencia Social Ética](https://img.shields.io/badge/Licencia-Social%20Ética%202026-darkblue?style=flat-square)](LICENSE_SOCIAL.md)
[![Offline 100%](https://img.shields.io/badge/Operación-100%25%20Local-darkgreen?style=flat-square)](#seguridad-y-privacidad)
[![Tests Automatizados](https://img.shields.io/badge/Tests-71%20Pasando-brightgreen?style=flat-square)](#testing)

---

## Sobre el Proyecto

AsistenteONG es una herramienta de escritorio, completamente offline y diseñada exclusivamente para organizaciones sociales, líneas de crisis, refugios y ONGs que enfrentan un volumen permanente de consultas, relatos y casos que demandan triaje rápido, análisis estructurado y documentación profesional.

No es un reemplazante de trabajadores sociales, abogados ni psicólogos. Es un **amplificador de capacidad operativa** que normaliza el flujo desde la recepción hasta la intervención, sin comprometer privacidad ni criterio humano.

### Para Quién

- Líneas de ayuda telefónica y chat que reciben 10+ casos diarios
- Refugios y centros de atención que necesitan triaje sistematizado
- Organizaciones legales que procesan consultas múltiples
- Equipos multidisciplinarios (psicólogos, trabajadores sociales, abogados)
- ONGs que atienden violencia, trata, abandono, vulnerabilidad económica
- Instituciones públicas de asistencia sin presupuesto para plataformas comerciales

### Lo que Resuelve

| Problema | Solución | Impacto |
|----------|----------|--------|
| Triaje manual 1 caso/2-3 min | Análisis automático <500ms | Reducción 70% tiempo operativo |
| Inconsistencia entre operadores | Clasificación estandarizada | Respuestas homogéneas, confiables |
| Indicadores perdidos en relatos largos | Detección estructurada de palabras clave | Cero riesgos críticos omitidos |
| Datos sin seguimiento longitudinal | Historial persistente de la persona | Patrones recurrentes visibles |
| Información privada en servidores | Almacenamiento 100% local cifrado | Cumplimiento RGPD, privacidad garantizada |
| Documentación inconsistente | Plantillas normalizadas, auditoría completa | Informes profesionales inmediatos |

---

## Cómo Funciona

### En Breve

```
1. Relato ingresa → 2. Análisis contextual instantáneo → 3. Indicadores detectados
  ↓
4. Información faltante identificada → 5. Historial consultado → 6. Evidencia presentada
  ↓
7. PROFESIONAL REVISA → 8. TOMA DECISIÓN → 9. Intervención, seguimiento, cierre
```

AsistenteONG procesa el texto del caso mediante:

- **Búsqueda de indicadores:** +320 palabras clave organizadas en 9 categorías (riesgo de vida, violencia, menores, salud mental, etc.)
- **Clasificación de urgencia:** 4 niveles automáticos que requieren validación
- **Detección de información faltante:** qué datos critticos faltan para intervención
- **Búsqueda histórica:** si la persona fue atendida antes, se muestran casos previos
- **Búsqueda en biblioteca:** si hay documentos institucionales, se recuperan fragmentos relevantes

**Garantía:** cada hallazgo se presenta como evidencia de apoyo, nunca como decisión automatizada. La acción siempre depende de revisión y validación humana.

---

## Características Principales

### Triaje Inteligente de Casos

Cada relato se procesa mediante análisis contextual que extrae:

- Indicadores de riesgo segmentados (violencia severa, menores en peligro, urgencia médica, derechos laborales, habitabilidad crítica)
- Clasificación en 4 niveles de urgencia: Muy Alta, Alta, Media, Baja
- Palabras clave encontradas con contexto
- Información crítica ausente que limita intervención
- Coincidencias en historial de la persona (si existe)

El sistema nunca decide; presenta evidencia. El profesional valida, rechaza o complementa cada análisis.

### Gestión de Personas y Casos

- Registro único por persona (previene duplicación)
- Múltiples casos asociados a la misma persona
- Historial longitudinal sin sobrescritura
- IDs automáticos y trazables: `CASE-202608-00001`
- Búsqueda, filtrado y exportación de contactos (cuando esté autorizado)
- Importación opcional desde XLSX con revisión explícita

### Informe Social Profesional

Generador de informes estructurado en 7 secciones normalizadas, según estándares de trabajo social:

1. **Datos del profesional e institución** (configurable, reutilizable)
2. **Identificación de la persona** (nombres, DNI, domicilio, contacto)
3. **Unidad de convivencia y dinámica familiar** (genograma, vínculos, conflictos)
4. **Situación socioeconómica y laboral** (ingresos, empleabilidad, egresos)
5. **Habitabilidad y vivienda** (régimen de tenencia, servicios, hacinamiento)
6. **Salud y educación** (sanitaria, discapacidad, asistencia escolar)
7. **Diagnóstico y propuesta** (juicio técnico, fortalezas, factores de riesgo, intervención)

El análisis del informe verifica completitud, coherencia, edad calculada, ratio habitaciones/convivientes, balance ingresos/egresos.

Exportación en PDF profesional o JSON estructurado.

### Biblioteca de Documentos Institucionales

- Importación de PDFs (protocolos, leyes, recursos, guías)
- Procesamiento local con extracción de fragmentos (chunking)
- Búsqueda semántica por similitud léxica (100% offline)
- Procedencia siempre visible (archivo + página)
- OCR opcional para documentos escaneados
- Vinculación con casos específicos

### Seguimiento, Derivaciones y Agenda

- Tareas con responsables y fechas de vencimiento
- Derivaciones estructuradas a servicios externos
- Calendario integrado: vistas por fecha, prioridad, responsable
- Estados de caso: abierto, en seguimiento, cerrado
- Historial completo de cambios y eventos

### Seguridad y Control de Acceso

- Base de datos SQLite cifrada con **AES-256** en reposo
- Derivación de clave mediante PBKDF2 (100,000 iteraciones)
- Contraseñas hasheadas con bcrypt (12 rounds)
- Autenticación por usuario con roles granulares
- Bloqueo automático tras 15 minutos de inactividad
- Backup cifrado descargable (ZIP protegido)
- **Auditoría exhaustiva:** quién, qué, cuándo, cambios específicos

### Operación 100% Offline

- Aplicación de escritorio para Windows (ejecutable standalone)
- No requiere Python instalado en máquina de usuario
- Base de datos local (SQLite) como único almacenamiento
- Backup manual en USB o medio externo
- **Cero datos enviados a Internet** sin acción explícita del operador
- Funciona completamente sin conectividad

---

## Arquitectura

### Capas del Sistema

```
Interfaz Gráfica (CustomTkinter 5.2+)
      ↓ Temas claro/oscuro, 6 paneles especializados
      
Lógica de Negocio
      ↓ Análisis contextual, clasificación, extracción de indicadores,
      ↓ generación de informes, gestión de casos
      
Persistencia (SQLite 3)
      ↓ Personas, casos, análisis, documentos, usuarios, auditoría
      
Utilidades
      ↓ Criptografía (AES-256, PBKDF2, bcrypt)
      ↓ Procesamiento de PDFs, generación de reportes
      ↓ Importación XLSX, backups cifrados
```

### Flujo de Procesamiento

```
Relato o Mensaje Ingresado
           ↓
   Normalización de Texto
           ↓
    Búsqueda de Palabras Clave
           ↓
   Clasificación de Urgencia
   (Muy Alta / Alta / Media / Baja)
           ↓
   Detección de Información Faltante
           ↓
   Búsqueda en Historial de Persona
           ↓
   Búsqueda en Biblioteca de Documentos
           ↓
Presentación de Evidencia al Profesional
           ↓
   REVISIÓN Y DECISIÓN HUMANA
           ↓
Acción: Intervención, Derivación, Seguimiento, Cierre
```

### Stack Tecnológico

| Componente | Tecnología | Versión | Propósito |
|-----------|-----------|---------|----------|
| Interfaz Gráfica | CustomTkinter | 5.2+ | UI desktop responsiva |
| Base de Datos | SQLite | 3 | Almacenamiento local cifrado |
| Criptografía | cryptography | 41+ | AES-256, PBKDF2, bcrypt |
| Generación de PDFs | ReportLab, PyPDF | 4.0+, 5.0+ | Informes profesionales |
| Importación de datos | openpyxl | 3.1+ | Carga desde Excel |
| Lenguaje Base | Python | 3.11+ | Lógica y procesamiento |
| Compilación a EXE | PyInstaller | 6.0+ | Ejecutable Windows standalone |
| OCR (Opcional) | pytesseract, PyMuPDF | 0.3.13+, 1.24+ | PDFs escaneados |
| Testing | pytest | 7.0+ | Automatización de tests |

---

## Instalación y Ejecución

### Para Usuarios Finales (Windows)

**Opción 1: Archivo Ejecutable (Recomendado)**

1. Descargá `AsistenteONG.exe` desde [Releases](https://github.com/Sahilytech/AsistenteONG/releases)
2. Hacé doble clic para ejecutar
3. La aplicación se inicia inmediatamente (sin instalación adicional)

**Opción 2: Desde Python**

```bash
# Descargar el repositorio
git clone https://github.com/Sahilytech/AsistenteONG.git
cd AsistenteONG

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar
python -m src.main
```

**Documentación detallada:** [INSTALL.md](INSTALL.md)

### Para Desarrolladores

```bash
# Clonar y configurar
git clone https://github.com/Sahilytech/AsistenteONG.git
cd AsistenteONG

# Entorno virtual
python -m venv venv
venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar en modo desarrollo
python -m src.main

# Ejecutar tests
pytest tests/ -v

# Compilar a ejecutable
build_exe.bat
```

---

## Uso Rápido

### Flujo Básico

1. **Iniciar aplicación** → Tutorial de primer uso
2. **Configurar institución** → Nombre, datos profesionales, recursos locales
3. **Crear persona** → Datos básicos (opcionalmente)
4. **Agregar caso** → Relato, consulta o mensaje
5. **Ejecutar análisis** → <500ms, análisis automático
6. **Revisar evidencia** → Indicadores, información faltante, historial
7. **Validar o rechazar** → Decisión profesional obligatoria
8. **Registrar seguimiento** → Tareas, derivaciones, próximas acciones
9. **Generar informe** → PDF estructurado o JSON
10. **Realizar backup** → Cifrado, descargable

### Guías Completas

- [USER_GUIDE.md](USER_GUIDE.md) — Guía de usuario paso a paso
- [QUICK_START.md](QUICK_START.md) — Inicio rápido en 5 minutos
- [docs/](docs/) — Documentación técnica detallada

---

## Seguridad y Privacidad

### Principios Fundamentales

**Local First:** Todos los datos residen en la máquina local. Cero sincronización en la nube. Cero servidores externos obligatorios.

**Cifrado en Reposo:** Base de datos protegida con AES-256-CBC. Contraseñas hasheadas con bcrypt.

**Auditoría Completa:** Registro exhaustivo de accesos, modificaciones y exportaciones. Cada acción incluye: usuario, timestamp, detalles específicos.

**Sin Terceros Involuntarios:** No hay integraciones externas ni APIs que activen automáticamente. Todo bajo control local.

### Responsabilidades de la Organización

La privacidad depende de que la organización implemente:

1. Control de acceso físico al equipo
2. Políticas de contraseña y rotación periódica
3. Procedimientos de backup y recuperación
4. Revisión regular de auditoría de accesos
5. Políticas de confidencialidad con personal
6. Coordinación con protección de datos local

---

## Estado Actual: v0.9 — Producción Estable

El proyecto alcanzó funcionalidad productiva con **71 tests automatizados pasando** en Python 3.11, 3.12 y 3.13.

### Implementado

- Análisis contextual de casos con <500ms de latencia
- Gestión de personas con historial longitudinal sin duplicación
- Clasificación de urgencia en 4 niveles
- Detección de +320 palabras clave organizadas en 9 categorías
- Informe social profesional estructurado en 7 secciones
- Biblioteca de documentos PDF con búsqueda local
- Seguimiento, tareas, derivaciones y agenda integrada
- Base de datos SQLite cifrada con AES-256
- Backups cifrados descargables
- Auditoría completa de acciones
- Roles, permisos y bloqueo automático de sesión
- Importación XLSX con revisión explícita
- Tutorial interactivo de primer uso
- Temas claro y oscuro completamente funcionales
- Ejecutable Windows standalone

### En Desarrollo

- OCR automático para PDFs escaneados (parcialmente implementado)
- Soporte multi-idioma (arquitectura preparada)

### Próximas Versiones

**v1.0** — Piloto con ONGs reales, optimización de performance, 2FA opcional
**v1.1+** — Multi-idioma, temas personalizables, integraciones opcionales

---

## Testing

### Ejecutar Tests

```bash
# Suite completa
pytest tests/ -v

# Con cobertura de código
pytest tests/ -v --cov=src

# Reporte HTML
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

---

## Configuración

### Variables de Entorno

```bash
# Activar OCR para PDFs escaneados
ASISTENTE_OCR=1

# Ruta personalizada de almacenamiento
ASISTENTE_DATA_PATH=/ruta/personalizada
```

### Dentro de la Aplicación

Toda configuración se realiza mediante interfaz gráfica:

- Datos institucionales (nombre, logo, ubicación, contacto)
- Datos del profesional (nombre, rol, firma digital)
- Palabras clave adicionales por categoría
- Recursos locales (teléfonos, direcciones, horarios)
- Preferencias de tema (claro/oscuro)
- Políticas de bloqueo y timeout de sesión

---

## Limitaciones Explícitas

AsistenteONG **NO:**

- Realiza diagnósticos médicos, psicológicos ni jurídicos
- Toma decisiones automáticas sobre protección o intervención
- Reemplaza validación de profesionales capacitados
- Convierte una coincidencia textual en una conclusión clínica
- Funciona sin revisión humana posterior
- Garantiza cobertura de todos los indicadores de riesgo posibles
- Sustituye asesoramiento especializado de ningún tipo

**Responsabilidad:** toda acción sensible debe validarse mediante profesionales capacitados de la organización, siguiendo protocolos internos y marco legal.

---

## Estructura del Proyecto

```
AsistenteONG/
├── src/
│   ├── main.py                       # Punto de entrada
│   ├── ui/                           # Interfaz gráfica
│   │   ├── main_window.py            # Ventana principal y navegación
│   │   ├── case_input.py             # Panel de ingreso de casos
│   │   ├── results_panel.py          # Presentación de análisis
│   │   ├── social_report_panel.py    # Generador de informes
│   │   ├── resources_panel.py        # Búsqueda de recursos
│   │   ├── config_panel.py           # Configuración de la app
│   │   ├── help_panel.py             # Tutorial y ayuda
│   │   └── styles.py                 # Temas y estilos
│   ├── core/                         # Lógica de negocio
│   │   ├── case_workflow.py          # Flujo de gestión de casos
│   │   ├── analysis.py               # Análisis de casos
│   │   ├── reasoning.py              # Razonamiento de indicadores
│   │   └── ...
│   ├── database/                     # Persistencia de datos
│   │   ├── schema.py                 # Estructura de BD
│   │   ├── models.py                 # Modelos de datos
│   │   └── queries.py                # Consultas
│   ├── security/                     # Seguridad
│   │   ├── crypto.py                 # Criptografía
│   │   ├── permissions.py            # Control de acceso
│   │   └── audit.py                  # Auditoría
│   └── utils/                        # Utilidades
│       ├── pdf_processor.py          # Procesamiento de PDFs
│       ├── report_generator.py       # Generador de reportes
│       ├── backup.py                 # Backups cifrados
│       └── ...
├── tests/                            # Suite de tests automatizados
│   ├── test_core_*.py
│   ├── test_security.py
│   └── ...
├── docs/                             # Documentación técnica
├── assets/                           # Iconos y recursos
├── requirements.txt
├── LICENSE                           # MIT License
├── LICENSE_SOCIAL.md                 # Licencia Ética 2026
├── README.md                         # Este archivo
├── INSTALL.md                        # Instalación
├── QUICK_START.md                    # Inicio rápido
├── USER_GUIDE.md                     # Guía de usuario
├── CHANGELOG.md                      # Historial de versiones
└── .github/workflows/                # CI/CD con GitHub Actions
```

---

## Casos de Uso Reales

### Línea de Crisis 24/7

Operador recibe llamada. Ingresa relato en la aplicación. El sistema:
- Clasifica urgencia inmediatamente
- Detecta indicadores de riesgo de vida
- Sugiere protocolo de respuesta
- Genera propuesta de derivación

Operador valida, completa información y ejecuta intervención.

**Ganancia:** Reducción 70% en tiempo de triaje, estandarización de respuesta, auditoría completa.

### Centro de Asesoría Legal

Abogado recibe solicitud por email. Analiza caso:
- El sistema busca coincidencias en historial de la persona
- Examina biblioteca de jurisprudencia y protocolos locales
- Identifica información faltante para fundamento legal
- Sugiere argumentación con fuentes

Abogado revisa, valida y redacta dictamen con apoyo del análisis.

**Ganancia:** Reducción 50% en tiempo de investigación, trazabilidad de precedentes, documentación estandarizada.

### Refugio para Víctimas de Violencia

Trabajadora social documenta ingreso:
- Ingresa información disponible (relato, antecedentes)
- El sistema detecta indicadores de riesgo severo
- Integra historial previo si existe
- Genera informe social preliminar

Profesional completa evaluación, firma informe, define plan de protección.

**Ganancia:** Documentación estructurada inmediata, evaluación de riesgos sistematizada, auditoría de decisiones.

---

## Licencia

### Licencia MIT

El código fuente está bajo [Licencia MIT](LICENSE) — libre para usar, modificar y distribuir en contextos no comerciales.

### Licencia Social Ética 2026

Además de la MIT, el proyecto incluye [LICENSE_SOCIAL.md](LICENSE_SOCIAL.md) — restricciones éticas que garantizan:

- **Prohibición de venta:** software 100% gratis, no comercializable
- **Atribución permanente:** crédito a creadora siempre visible
- **Privacidad garantizada:** datos nunca salen del equipo local
- **Enfoque social:** restricción de uso ético obligatoria
- **Transparencia:** código abierto, auditable, sin "backend" secreto

La licencia social refleja el compromiso del proyecto: tecnología **para el bien común, nunca para la explotación**.

---

## Contribuir

Las contribuciones son bienvenidas. Proceso:

1. **Fork** el repositorio
2. **Rama** con cambio: `git checkout -b feature/descripcion`
3. **Commits** descriptivos que expliquen qué y por qué
4. **Tests** que cubran el cambio: `pytest tests/`
5. **Pull request** con descripción detallada

**Antes de contribuir:**
- Lee [CONTRIBUTING.md](CONTRIBUTING.md)
- Revisa issues abiertos para no duplicar trabajo
- Discute cambios mayores en issues primero

---

## Autor

**Sarah Lee Olivera**

Desarrolladora comprometida con tecnología cívica, justicia social y transformación de organizaciones sociales mediante herramientas éticas y accesibles.

- GitHub: [@Sahilytech](https://github.com/Sahilytech)
- Email: sarahleeoliveraok@gmail.com
- Repositorio: [github.com/Sahilytech/AsistenteONG](https://github.com/Sahilytech/AsistenteONG)

---

## Soporte y Documentación

- **Guía de Usuario:** [USER_GUIDE.md](USER_GUIDE.md)
- **Instalación Detallada:** [INSTALL.md](INSTALL.md)
- **Inicio Rápido:** [QUICK_START.md](QUICK_START.md)
- **Documentación Técnica:** [docs/](docs/)
- **Issues y Bugs:** [GitHub Issues](https://github.com/Sahilytech/AsistenteONG/issues)
- **Discusiones:** [GitHub Discussions](https://github.com/Sahilytech/AsistenteONG/discussions)

---

## Reconocimiento

Diseñado y desarrollado con compromiso hacia organizaciones sociales que trabajan en primera línea por protección, derechos y bienestar de personas en situación de vulnerabilidad.

Este software existe porque **la tecnología puede servir a la justicia social**.

---

**AsistenteONG v0.9** — Inteligencia social para acelerar intervención profesional. Sin reemplazar responsabilidad humana. 100% offline. Completamente ético.
