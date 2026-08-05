# Base de Datos

## Visión general

SQLite como base de datos local, completamente offline, con esquema robusto para casos, usuarios, recursos y auditoría.

## Estructura

### Tablas

#### `users`
Usuarios que operan el sistema.

```
id (INTEGER PRIMARY KEY)
username (TEXT UNIQUE)
password_hash (TEXT)
role (TEXT) - 'operator', 'admin', 'supervisor'
created_at (TIMESTAMP)
```

#### `cases`
Casos ingresados por operadores.

```
id (INTEGER PRIMARY KEY)
case_number (TEXT UNIQUE) - Ej: "CASE-2025-001"
input_text (TEXT) - Texto original del caso
summary (TEXT) - Resumen generado por IA
urgency (TEXT) - 'Muy Alta', 'Alta', 'Media', 'Baja'
case_type (TEXT) - Ej: 'violencia_doméstica', 'asesoría_legal'
status (TEXT) - 'new', 'in_progress', 'resolved', 'closed'
created_by (INTEGER FK) - Usuario que creó el caso
created_at (TIMESTAMP)
updated_at (TIMESTAMP)
```

#### `case_analysis`
Análisis detallado de cada caso.

```
id (INTEGER PRIMARY KEY)
case_id (INTEGER FK)
emotions (TEXT) - Emociones detectadas
risk_factors (TEXT) - Factores de riesgo
identified_people (TEXT) - Personas mencionadas
ai_score (REAL) - Confianza del análisis (0-1)
analysis_data (TEXT) - JSON con datos completos
created_at (TIMESTAMP)
```

#### `resources`
Organismos y recursos locales.

```
id (INTEGER PRIMARY KEY)
name (TEXT)
type (TEXT) - 'hospital', 'refugio', 'abogado', etc.
phone (TEXT)
email (TEXT)
address (TEXT)
hours (TEXT)
description (TEXT)
region (TEXT) - País/Región
created_at (TIMESTAMP)
```

#### `audit_log`
Registro completo de todas las acciones.

```
id (INTEGER PRIMARY KEY)
user_id (INTEGER FK)
action (TEXT) - 'CREATE_CASE', 'UPDATE_CASE', 'DELETE_CASE'
table_name (TEXT) - Tabla afectada
record_id (INTEGER)
details (TEXT) - Detalles adicionales
timestamp (TIMESTAMP)
```

## DAOs (Data Access Objects)

### Uso

Cada tabla tiene su DAO correspondiente:

```python
from src.database.dao import CaseDAO, UserDAO, ResourceDAO

# Crear caso
case_dao = CaseDAO()
case_id = case_dao.create("CASE-001", "Mi pareja me golpeó", user_id=1)

# Actualizar caso
case_dao.update(case_id, urgency="Muy Alta", status="in_progress")

# Obtener caso
case = case_dao.get_by_id(case_id)

# Listar casos por urgencia
urgent_cases = case_dao.list_by_urgency("Muy Alta")
```

### DAOs disponibles

- `UserDAO` - Gestión de usuarios
- `CaseDAO` - Gestión de casos
- `CaseAnalysisDAO` - Análisis de casos
- `ResourceDAO` - Recursos y organismos
- `AuditLogDAO` - Registro de auditoría

## Migraciones

### Sistema de migraciones

Las migraciones se ejecutan automáticamente al iniciar:

```python
from src.database.migrations import init_migrations
init_migrations()
```

### Crear una migración

1. Crear archivo `src/database/migrations/001_nombre.sql`
2. Escribir SQL
3. Se ejecutará automáticamente en próximo inicio

## Índices

Índices para optimizar queries:

```
- idx_case_status: Búsquedas por estado
- idx_case_urgency: Búsquedas por urgencia
- idx_case_type: Búsquedas por tipo
- idx_audit_user: Auditoría por usuario
- idx_audit_timestamp: Auditoría por fecha
```

## Seguridad

### Encriptación

- Base de datos cifrada en reposo (opcional con cryptography)
- Contraseñas hasheadas con bcrypt/argon2
- Datos sensibles en campos cifrados

### Auditoría

Cada operación se registra en `audit_log`:

```python
from src.database.dao import AuditLogDAO

audit = AuditLogDAO()
audit.log(
    user_id=1,
    action="CREATE_CASE",
    table_name="cases",
    record_id=1,
    details="Caso de violencia"
)
```

## Backups

- Backup automático diario
- Almacenamiento en `data/backups/`
- Encriptación de backups
- Retención de 30 días

## Performance

### Límites

- **SQLite**: Adecuado hasta 100k casos
- **Consultas**: <1s en queries típicas
- **Tamaño DB**: ~50MB por 10k casos

### Para escalar

Si se necesita más: Migrar a PostgreSQL sin cambiar DAOs

## Testing

```bash
pytest tests/test_database.py -v
```

Cubre:
- CRUD de todas las tablas
- Búsquedas y filtros
- Auditoría
- Integridad referencial

---

**v0.2 Status:** ✅ Completo
