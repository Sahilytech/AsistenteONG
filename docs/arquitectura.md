# Arquitectura del Sistema

## Flujo General

```
┌─────────────┐
│  Operador   │
└──────┬──────┘
       │ Escribe caso
       ▼
┌─────────────────────┐
│  Interfaz (UI)      │ ◄─ CustomTkinter
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  Motor de Análisis  │ ◄─ Procesa texto
├─────────────────────┤
│ • Tokenización      │
│ • Análisis NLP      │
│ • Extracción datos  │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  Clasificador IA    │ ◄─ Gemma 3 1B (GGUF)
├─────────────────────┤
│ • Urgencia          │
│ • Tipo de caso      │
│ • Factores de riesgo│
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  Motor de Reglas    │
├─────────────────────┤
│ • Validaciones      │
│ • Cierre de casos   │
│ • Escaladas         │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  Base de Datos      │ ◄─ SQLite
├─────────────────────┤
│ • Casos             │
│ • Historial         │
│ • Recursos          │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  Generador Respuesta│
├─────────────────────┤
│ • Template matching │
│ • Personalización   │
│ • Sugerencias       │
└──────┬──────────────┘
       │
       ▼
┌─────────────┐
│  Operador   │◄─ Revisa y envía
└─────────────┘
```

## Componentes

### 1. UI (Interfaz Gráfica)

**Tecnología:** CustomTkinter

**Responsabilidades:**
- Recibir input del operador
- Mostrar análisis en tiempo real
- Permitir edición de borradores
- Exportar reportes

**Archivos:**
- `src/ui/main_window.py` — Ventana principal
- `src/ui/case_input.py` — Formulario de entrada
- `src/ui/results_panel.py` — Panel de resultados
- `src/ui/templates.py` — Diseño y temas

### 2. Motor IA

**Tecnología:** llama.cpp + Gemma 3 1B

**Responsabilidades:**
- Procesar texto natural
- Extraer información estructurada
- Clasificar urgencia
- Detectar riesgos

**Archivos:**
- `src/ai/model_loader.py` — Carga del modelo GGUF
- `src/ai/analyzer.py` — Análisis de casos
- `src/ai/classifier.py` — Clasificación
- `src/ai/extractor.py` — Extracción de datos

### 3. Base de Datos

**Tecnología:** SQLite

**Tablas principales:**
- `cases` — Casos ingresados
- `categories` — Tipos de casos
- `resources` — Organismos y contactos
- `audit_log` — Registro de acciones

**Archivos:**
- `src/database/schema.py` — Esquema
- `src/database/dao.py` — Data Access Objects
- `src/database/migrations.py` — Migraciones

### 4. Motor de Reglas

**Responsabilidades:**
- Validar datos extraídos
- Detectar escaladas automáticas
- Aplicar lógica negocio
- Generar auditoría

**Archivos:**
- `src/rules/validator.py` — Validaciones
- `src/rules/escalation.py` — Reglas de escalada
- `src/rules/engine.py` — Motor

### 5. Generador de Reportes

**Tecnología:** ReportLab

**Formatos:**
- PDF (detallado)
- CSV (datos)
- Excel (análisis)
- TXT (legible)

**Archivos:**
- `src/reports/pdf_generator.py`
- `src/reports/csv_exporter.py`
- `src/reports/formatter.py`

### 6. Seguridad

**Tecnología:** cryptography, pycryptodome

**Features:**
- Autenticación por contraseña
- Cifrado de base de datos
- Auditoría de accesos
- Copias de seguridad cifradas

**Archivos:**
- `src/security/auth.py` — Autenticación
- `src/security/encryption.py` — Cifrado
- `src/security/audit.py` — Auditoría

### 7. Actualizador

**Responsabilidades:**
- Verificar actualizaciones
- Descargar paquetes (opcional online)
- Actualizar base de conocimiento
- Rollback si falla

**Archivos:**
- `src/updater/manager.py` — Gestión
- `src/updater/downloader.py` — Descargas

## Base de Conocimiento

Estructura: `data/`

```
data/
├── leyes/
│   ├── argentina.md
│   ├── méxico.md
│   └── ...
├── recursos/
│   ├── emergencias.json
│   ├── organismos.json
│   └── telefonos.csv
├── plantillas/
│   ├── respuesta_violencia.txt
│   ├── derivacion_legal.txt
│   └── ...
└── emergencias/
    ├── codigos.json
    └── escaladas.json
```

## Flujo de Datos

```
Caso ingresado (texto)
    ↓
Análisis NLP (tokenización, extracción)
    ↓
IA Classification (urgencia, tipo, riesgos)
    ↓
Validación (reglas)
    ↓
Base de datos (CRUD)
    ↓
Generación respuesta (template + personalización)
    ↓
Exportación (PDF, CSV, etc)
    ↓
Auditoría (registro de quién hizo qué)
```

## Seguridad

- ✅ Datos en reposo: **Cifrado AES-256**
- ✅ Autenticación: **Contraseña + 2FA opcional**
- ✅ Acceso: **Control por roles**
- ✅ Auditoría: **Log completo de acciones**
- ✅ Backup: **Cifrado automático**

## Escalabilidad

- Single machine: ✅ Soporta 1000+ casos/mes
- Offline: ✅ Sin dependencias externas
- Modelo IA: ✅ 1B params = ~4GB RAM mínimo
- Base de datos: ✅ SQLite ade para <100k casos

Para más casos: Migrar a PostgreSQL
