# Testing y QA (v0.7)

## Visión

Cobertura completa de pruebas unitarias, integración y aceptación. CI/CD automático en GitHub Actions.

## Test suites

### Unit Tests

Pruebas individuales de cada módulo.

```bash
# Tests de base de datos
pytest tests/test_database.py -v

# Tests de IA
pytest tests/test_ai.py -v

# Tests de seguridad
pytest tests/test_security.py -v

# Tests de actualizaciones
pytest tests/test_updater.py -v
```

### Integration Tests

Pruebas de integración entre módulos.

```bash
pytest tests/test_integration.py -v
```

### Coverage

```bash
pytest --cov=src --cov-report=html tests/

# Abrir htmlcov/index.html en navegador
```

## Objetivos de cobertura

| Módulo | Meta | Actual |
|--------|------|--------|
| database | 95% | ✅ |
| ai | 90% | ✅ |
| security | 95% | ✅ |
| ui | 70% | ✅ |
| updater | 85% | ✅ |

## CI/CD con GitHub Actions

### Tests automáticos en cada push

Archivo: `.github/workflows/tests.yml`

Ejecuta:
- ✅ Tests en Python 3.11 y 3.12
- ✅ Linting (flake8)
- ✅ Type checking (mypy)
- ✅ Coverage upload (codecov)
- ✅ Tests en Linux, Windows, macOS

### Build automático de .exe

Archivo: `.github/workflows/build.yml`

En cada tag `v*`:
- ✅ Compila con PyInstaller
- ✅ Genera AsistenteONG.exe
- ✅ Crea release en GitHub
- ✅ Sube binarios

## Cómo ejecutar tests localmente

### Setup

```bash
cd AsistenteONG
python -m venv venv
source venv/bin/activate  # o venv\Scripts\activate en Windows

pip install -r requirements.txt
pip install pytest pytest-cov black flake8 mypy
```

### Ejecutar

```bash
# Todos los tests
pytest tests/ -v

# Con coverage
pytest tests/ -v --cov=src

# Generar reporte HTML
pytest tests/ --cov=src --cov-report=html
```

### Linting

```bash
# Formato
black src/ tests/

# Lint
flake8 src/ tests/ --max-line-length=127

# Type checking
mypy src/ --ignore-missing-imports
```

## Benchmarks

### Performance targets

- Análisis de caso: <500ms
- Clasificación: <100ms
- Descifrado DB: <1s (DB de 100k casos)
- Startup de app: <2s

### Ejecutar benchmarks

```bash
pytest tests/benchmarks.py -v --benchmark-only
```

## Test data

Fixtures en: `tests/fixtures/`

- `messages.json`: casos de prueba
- `users.json`: usuarios de prueba
- `resources.json`: recursos de prueba

## Calidad de código

### Estándares

- ✅ PEP 8 compliance
- ✅ Type hints en funciones públicas
- ✅ Docstrings en formato Google
- ✅ Max 88 caracteres por línea (Black)
- ✅ Max 10% cognitive complexity

### Pre-commit hooks

Opcional: configurar hooks para validar antes de commit.

```bash
pip install pre-commit
pre-commit install
```

## Checklist antes de release

- [ ] Todos los tests pasan (`pytest tests/ -v`)
- [ ] Coverage >= 80% (`pytest --cov`)
- [ ] Lint limpio (`flake8`, `black`, `mypy`)
- [ ] Documentación actualizada (`docs/`)
- [ ] CHANGELOG actualizado
- [ ] Versión bumped en `src/__init__.py`
- [ ] Tag creado (`git tag v0.x.0`)
- [ ] Release en GitHub con binarios

## Problemas comunes

### Test falla en Windows

Usar `pathlib.Path` en lugar de strings de ruta.

### Timeout en tests

Aumentar `pytest.ini`:
```ini
timeout = 300
```

### Import error

Asegurar que `src/` está en PYTHONPATH:
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
```

---

**v0.7 Status:** ✅ Testing completo y CI/CD funcionando
