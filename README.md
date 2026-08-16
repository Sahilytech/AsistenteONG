# AsistenteONG

Tecnología estructurada para convertir relatos complejos en orientación y seguimiento profesional.

[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-3776ab?style=flat-square)](https://www.python.org/)
[![Licencia MIT](https://img.shields.io/badge/Licencia-MIT-green?style=flat-square)](LICENSE)
[![Estado: Estable](https://img.shields.io/badge/Estado-Estable-brightgreen?style=flat-square)](#estado-actual)
[![Tests: 71 Pasando](https://img.shields.io/badge/Tests-71%20Pasando-brightgreen?style=flat-square)](#testing)
[![Platform: Windows](https://img.shields.io/badge/Platform-Windows-0078d4?style=flat-square)](#plataformas-soportadas)

---

## Qué es AsistenteONG

AsistenteONG es una herramienta de escritorio, 100% offline y gratuita, diseñada específicamente para organizaciones sociales y líneas de ayuda que gestionan relatos, consultas y solicitudes de apoyo que requieren triaje, análisis contextual y seguimiento profesional.

El sistema procesa información desestructurada (textos, relatos, mensajes extensos) y genera:

- Análisis inteligente con detección de indicadores de riesgo
- Clasificación automática de urgencia
- Propuestas de respuesta personalizadas
- Gestión estructurada de personas y casos
- Informes sociales profesionales
- Seguimiento, agenda y derivaciones
- Auditoría completa de operaciones

Todo funciona **sin conexión a internet**, garantizando privacidad local total. No hay sincronización en la nube, ni análisis centralizados, ni terceros externos.

---

## El Problema

Las organizaciones sociales enfrentan un desafío operativo fundamental:

**Información desestructurada:** llegan textos largos, relatos fragmentarios, consultas legales, laborales y sociales que requieren procesamiento manual.

**Falta de estandarización:** cada operador interpreta y clasifica de manera diferente, generando inconsistencias.

**Tiempo de respuesta:** sin herramientas, triaje y análisis consumen horas que podrían dedicarse a intervención directa.

**Riesgo de omisión:** indicadores críticos pueden pasar desapercibidos en relatos extensos o ambiguos.

**Escalabilidad limitada:** una ONG con 50 casos/mes puede manejarse manualmente; con 500/mes se colapsa.

AsistenteONG intenta aliviar esta presión operativa sin reemplazar el criterio profesional.

---

## La Solución

Una plataforma de apoyo que:

1. **Normaliza el flujo** desde el relato inicial hasta la derivación y el seguimiento
2. **Detecta indicadores** sin realizar diagnósticos ni tomar decisiones automáticas
3. **Genera respuestas borrador** personalizadas según urgencia y tipo de caso
4. **Gestiona el historial** de personas y casos en una base de datos estructurada
5. **Integra documentación** institucional (PDFs, protocolos, recursos)
6. **Produce informes** sociales profesionales con datos recopilados
7. **Mantiene auditoría completa** de quién accedió qué y cuándo
8. **Funciona sin internet** y sin terceros, garantizando privacidad

**Concepto central:** la herramienta amplifica la capacidad del operador humano. No reemplaza su juicio, sino que lo organiza, lo contextualiza y lo acelera.

---

## Para Quién Está Diseñado

- Líneas de ayuda telefónica o chat
- ONGs de protección, derechos humanos, violencia
- Centros de asesoría jurídica
- Organizaciones de salud mental
- Refugios y albergues
- Cooperativas y espacios de contención social
- Equipos multidisciplinarios (trabajadores sociales, abogados, psicólogos, operadores)

**Condición:** revisión profesional obligatoria. Ninguna acción final sin validación humana.

---

## Características Principales

### Triaje Inteligente

Análisis contextual de casos con detección de:

- Indicadores de riesgo por categoría (violencia, menores, urgencia, etc.)
- Urgencia clasificada en 4 niveles (Muy Alta, Alta, Media, Baja)
- Señales detectadas según +100 palabras clave organizadas
- Información faltante relevante
- Coincidencias con historial longitudinal de la persona

**Importante:** todas las coincidencias se presentan como evidencia de apoyo, no como decisiones.

### Gestión de Personas y Casos

- Una persona, múltiples casos: historial longitudinal sin duplicación
- Registro de contacto opcional cuando esté autorizado
- Importación XLSX en modo revisión y confirmación explícita
- Búsqueda y filtrado

### Informe Social Profesional

Generador de informes estructurados en 7 bloques:

1. Datos del profesional e institución
2. Identificación de la persona
3. Unidad de convivencia y dinámica familiar
4. Situación socioeconómica y laboral
5. Habitabilidad y vivienda
6. Salud y educación
7. Diagnóstico, valoración y propuesta

Configuración institucional reutilizable para firma, destinatario, entidad.

### Biblioteca Documental

- Importación de PDFs institucionales (protocolos, leyes, recursos)
- Procesamiento local y recuperación de fragmentos relevantes
- Procedencia y página siempre preservadas
- Vinculación con casos específicos
- OCR opcional para documentos escaneados

### Seguimiento y Agenda

- Tareas con responsables y fechas
- Derivaciones a otros servicios
- Calendario integrado
- Estado de casos (abierto, en seguimiento, cerrado)

### Seguridad y Privacidad

- Base de datos cifrada en disco
- Roles y permisos por usuario
- Bloqueo de sesión tras inactividad
- Backup cifrado y descargable
- Auditoría completa: quién, qué, cuándo
- Exportación anonimizada para análisis agregado
- Ningún dato sale del equipo sin intención explícita

### Instalable en Windows

- Ejecutable standalone `.exe` mediante PyInstaller
- Instalador con wizard mediante Inno Setup
- Portable en USB (ejecutable + carpetas de datos)
- No requiere Python instalado en máquina de usuario

---

## Arquitectura

```
AsistenteONG
├── Interfaz Gráfica (CustomTkinter)
│   ├── Entrada de casos
│   ├── Visualización de análisis
│   ├── Panel de informe social
│   ├── Gestión de biblioteca
│   ├── Configuración y seguridad
│   └── Auditoría
├── Motor de Análisis
│   ├── Procesamiento de texto
│   ├── Clasificación de urgencia
│   ├── Extracción de indicadores
│   ├── Detección de patrones
│   └── Generación de respuestas
├── Base de Datos (SQLite)
│   ├── Personas y casos
│   ├── Análisis almacenados
│   ├── Documentos y referencias
│   ├── Usuarios y permisos
│   └── Logs de auditoría
└── Utilidades
    ├── Criptografía y backup
    ├── Procesamiento de PDFs
    ├── Generación de informes
    ├── OCR (opcional)
    └── Actualización automática
```

### Flujo de Procesamiento

```
Relato/Mensaje
      ↓
Procesamiento de Texto
      ↓
Análisis Contextual → Extracción de Palabras Clave
      ↓              ↓
Clasificación de    Detección de Indicadores
Urgencia            de Riesgo
      ↓              ↓
      └──────┬───────┘
             ↓
      Gestión del Caso
             ↓
      Evidencia Presentada
             ↓
    Revisión Profesional Humana
             ↓
    Decisión y Acción
             ↓
    Seguimiento y Cierre
```

---

## Tecnologías

| Capa | Tecnología | Propósito |
|------|-----------|-----------|
| UI | CustomTkinter 5.2+ | Interfaz gráfica desktop |
| BD | SQLite 3 | Base de datos local |
| Cripto | cryptography 41+ | Cifrado de datos en reposo |
| PDF | reportlab, pypdf | Generación e importación de documentos |
| XLSX | openpyxl 3.1+ | Importación de datos estructurados |
| Análisis | Python 3.11+ | Procesamiento de texto y lógica |
| Build | PyInstaller 6.0+ | Compilación a ejecutable Windows |
| Instalador | Inno Setup 6 | Generador de instalador Windows |
| Testing | pytest | Suite de tests unitarios e integración |
| Lenguaje | Python | Código fuente del proyecto |
| OCR | pytesseract, PyMuPDF | Opcional para documentos escaneados |

---

## Estado Actual

### v0.9 - Producción Estable

El proyecto ha alcanzado estabilidad funcional:

- 71 tests automatizados pasando
- Suite de pruebas en Python 3.11, 3.12, 3.13
- CI/CD completo en GitHub Actions
- Compilación automática a .exe y instalador
- Documentación extensiva para usuarios y desarrolladores

### Características Implementadas

- ✅ Entrada de casos con análisis local
- ✅ Gestión de personas con historial longitudinal
- ✅ Clasificación de urgencia en 4 niveles
- ✅ Detección de indicadores de riesgo
- ✅ Informe social profesional completo
- ✅ Biblioteca de documentos PDF
- ✅ Seguimiento, tareas y agenda
- ✅ Roles, permisos y bloqueo de sesión
- ✅ Base de datos cifrada y backups
- ✅ Auditoría completa
- ✅ Importación XLSX con revisión
- ✅ Tutorial interactivo de primer arranque
- ✅ Exportación anonimizada
- ✅ Ejecutable Windows standalone

### En Desarrollo

- OCR automático para PDFs escaneados (parcialmente implementado)
- Soporte multi-idioma (arquitectura preparada)
- Tema light/dark toggle (preparado)

---

## Instalación

### Para Usuarios Finales (Windows)

1. **Descargar** el instalador desde [Releases](https://github.com/Sahilytech/AsistenteONG/releases)
2. **Ejecutar** `AsistenteONG-Setup-*.exe`
3. **Seguir** el wizard de instalación
4. **Abrir** desde el menú de inicio

### Para Desarrolladores

```bash
# Clonar
git clone https://github.com/Sahilytech/AsistenteONG.git
cd AsistenteONG

# Entorno virtual
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/macOS

# Dependencias
pip install -r requirements.txt

# Ejecutar
python -m src.main
```

Más detalles en [INSTALL.md](INSTALL.md).

---

## Uso Rápido

1. **Abrir** la aplicación
2. **Completar** el tutorial inicial (primera vez)
3. **Ir a Configuración** e ingresar datos institucionales
4. **Crear una persona** nueva
5. **Agregar un caso** con el relato/mensaje
6. **Analizar** el caso (genera análisis automático)
7. **Revisar** evidencia, indicadores y propuesta
8. **Registrar seguimiento** si corresponde
9. **Hacer backup** regularmente

Guía detallada en [USER_GUIDE.md](USER_GUIDE.md) y [docs/GUIA_USUARIO_FINAL.md](docs/GUIA_USUARIO_FINAL.md).

---

## Desarrollo y Testing

### Ejecutar Tests

```bash
# Todos los tests
python -m pytest tests/ -v

# Con cobertura
python -m pytest tests/ -v --cov=src

# Reporte HTML
pytest tests/ --cov=src --cov-report=html
```

**Estado:** 71 tests pasando

### Linting y Formato

```bash
# Formato
black src/ tests/

# Lint
flake8 src/ tests/ --max-line-length=127

# Type checking
mypy src/ --ignore-missing-imports
```

### Compilar Ejecutable

```bash
# Windows
build_exe.bat

# Resultado: dist/AsistenteONG.exe
```

Más detalles en [docs/testing.md](docs/testing.md).

---

## Configuración

### Variables de Entorno

El proyecto soporta configuración mediante variables de entorno:

```bash
# Activar OCR para PDFs escaneados
ASISTENTE_OCR=1

# Ruta personalizada de datos (por defecto: ./data)
ASISTENTE_DATA_PATH=/ruta/personalizada
```

### Archivos de Configuración

- Datos de la organización: almacenados en base de datos
- Tema (claro/oscuro): `~/.asistente_ong_theme`
- Datos de casos/personas: carpeta `data/` (cifrada)

---

## Seguridad y Privacidad

### Principios

1. **Local First:** Todos los datos residen en la máquina local por defecto. Sin sincronización a la nube.
2. **Cifrado en Reposo:** Base de datos cifrada con cryptography AES-256
3. **Cifrado de Backups:** Backups cifrados y descargables manualmente
4. **Auditoría:** Registro completo de accesos y modificaciones
5. **Sin Terceros:** No hay integraciones externas obligatorias

### Checklist de Seguridad

- Usar contraseña fuerte en el equipo
- Usar bloqueo de sesión cuando se deja la máquina desatendida
- Hacer backups cifrados regularmente
- Probar periódicamente restauración de backups
- No compartir carpeta de datos con usuarios no autorizados
- Usar únicamente conectividad externa que la organización haya habilitado

---

## Limitaciones

AsistenteONG **no:**

- Realiza diagnósticos médicos, psicológicos ni jurídicos
- Toma decisiones automáticas sobre intervenciones o protección
- Reemplaza la revisión profesional humana
- Convierte una coincidencia documental en una decisión
- Funciona sin revisión humana posterior
- Garantiza cobertura de todos los indicadores posibles
- Sustituye asesoramiento especializado

Toda acción sensible debe ser validada por profesionales capacitados de la organización.

---

## Estructura del Proyecto

```
AsistenteONG/
├── src/
│   ├── main.py                  # Punto de entrada
│   ├── ui/                      # Interfaz gráfica (CustomTkinter)
│   │   ├── main_window.py
│   │   ├── case_input.py
│   │   ├── results.py
│   │   ├── social_report_panel.py
│   │   ├── styles.py
│   │   └── ...
│   ├── ai/                      # Motor de análisis
│   │   ├── processor.py
│   │   ├── classifier.py
│   │   └── indicators.py
│   ├── database/                # Base de datos
│   │   ├── schema.py
│   │   ├── models.py
│   │   └── queries.py
│   ├── security/                # Cifrado y permisos
│   │   ├── crypto.py
│   │   ├── permissions.py
│   │   └── audit.py
│   └── utils/                   # Utilidades
│       ├── pdf_processor.py
│       ├── report_generator.py
│       └── backup.py
├── tests/                       # Suite de tests
│   ├── test_ai.py
│   ├── test_database.py
│   ├── test_security.py
│   └── ...
├── docs/                        # Documentación
│   ├── GUIA_USUARIO_FINAL.md
│   ├── PILOTO_USUARIOS.md
│   ├── DISTRIBUCION_NACIONAL.md
│   ├── ai.md
│   ├── ui.md
│   ├── testing.md
│   └── ...
├── assets/                      # Iconos, imágenes
├── data/                        # Datos locales (generados en tiempo de ejecución)
├── requirements.txt             # Dependencias Python
├── LICENSE                      # MIT
├── README.md                    # Este archivo
├── INSTALL.md                   # Guía de instalación
├── USER_GUIDE.md                # Guía de usuario
├── CHANGELOG.md                 # Historial de versiones
└── .github/
    └── workflows/               # GitHub Actions CI/CD
        ├── core-tests.yml
        ├── windows-build.yml
        └── build.yml
```

---

## Roadmap

### v0.9 (Actual)

- ✅ Triaje, análisis e informe social
- ✅ Gestión de personas y casos
- ✅ Biblioteca documental
- ✅ Seguridad y auditoría
- ✅ Compilación a .exe
- ✅ 71 tests automatizados

### v1.0 (Próxima)

- Piloto con ONGs reales
- Optimización de performance
- Manual en PDF descargable
- 2FA (TOTP) opcional
- Firma digital RSA en paquetes

### v1.1+

- Soporte multi-idioma
- Themes adicionales
- Exportación a formatos específicos por país
- Integración opcional con sistemas externos (solo si la ONG lo solicita)

---

## Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Fork el repositorio
2. Crea una rama con tu cambio: `git checkout -b feature/tu-feature`
3. Commits descriptivos
4. Tests que cubran tu cambio
5. Pull request con descripción detallada

Más detalles en [CONTRIBUTING.md](CONTRIBUTING.md) (cuando esté disponible).

---

## Casos de Uso

### Línea de Ayuda Telefónica

Operador recibe llamada de persona en crisis. Ingresa el relato en tiempo real. El sistema clasifica urgencia, detecta indicadores y sugiere protocolo de respuesta. Operador valida y atiende según criterio profesional.

### Centro de Asesoría Legal

Abogado recibe solicitud por WhatsApp. Analiza caso contra biblioteca de jurisprudencia local. Sistema detecta coincidencias con casos previos. Abogado revisa e interviene.

### Refugio para Víctimas de Violencia

Trabajadora social documenta ingreso de persona. El sistema integra historial longitudinal, detecta patrones de riesgo, genera informe social preliminar. Profesional completa y firma.

### Organización Multidisciplinaria

Equipo de psicólogos, trabajadores sociales y abogados accede simultáneamente (con permisos). Cada uno ve su perspectiva. Auditoría completa de accesos.

---

## Licencia

MIT License - Ver [LICENSE](LICENSE) para detalles completos.

Este proyecto es software libre. Puedes usarlo, modificarlo y distribuirlo bajo los términos de la licencia MIT.

---

## Autor

**Sarah Lee Olivera**

Desarrolladora comprometida con tecnología cívica y transformación social.

- GitHub: [@Sahilytech](https://github.com/Sahilytech)
- Repositorio: [Sahilytech/AsistenteONG](https://github.com/Sahilytech/AsistenteONG)

---

## Soporte

- Documentación: [docs/](docs/)
- Guía de usuario: [USER_GUIDE.md](USER_GUIDE.md)
- Instalación: [INSTALL.md](INSTALL.md)
- Issues: [GitHub Issues](https://github.com/Sahilytech/AsistenteONG/issues)
- Discusiones: [GitHub Discussions](https://github.com/Sahilytech/AsistenteONG/discussions)

---

## Reconocimientos

Diseñado y desarrollado con compromiso hacia organizaciones sociales que trabajan en primera línea por derechos, protección y bienestar.

Este software existe porque la tecnología puede servir a la justicia social.

---

**AsistenteONG v0.9** | Tecnología para transformar información social en acción estructurada y responsable.
