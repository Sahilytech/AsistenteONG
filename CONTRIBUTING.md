# Guía de Contribución

¡Gracias por tu interés en contribuir a Asistente ONG! 🙌

## Cómo contribuir

### 1. Fork y clon

```bash
git clone https://github.com/tuusuario/AsistenteONG.git
cd AsistenteONG
git checkout -b feature/mi-mejora
```

### 2. Instala dependencias

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Para testing y linting
```

### 3. Crea tu rama

```bash
git checkout -b feature/nombre-descriptivo
```

### 4. Realiza cambios

- Sigue [PEP 8](https://pep8.org/) para estilo de código
- Escribe tests unitarios (`tests/`)
- Documenta funciones complejas
- Usa commit messages descriptivos

### 5. Testing

```bash
pytest tests/
pytest --cov=src tests/  # Con cobertura
```

### 6. Lint y format

```bash
black src/
flake8 src/
mypy src/
```

### 7. Push y PR

```bash
git push origin feature/nombre-descriptivo
```

Abre un Pull Request en GitHub con:
- Descripción clara de qué cambió
- Referencias a Issues relacionados (#123)
- Screenshots si es UI

## Estándares

### Commits

```
feat: agregar clasificador de urgencia
fix: corregir cifrado de base de datos
docs: actualizar arquitectura en docs
tests: agregar tests para validación
chore: actualizar dependencias
```

### Python

- 4 espacios de indentación
- Max 88 caracteres por línea (Black)
- Type hints en funciones públicas
- Docstrings en formato Google

```python
def clasificar_urgencia(texto: str) -> str:
    """Clasifica la urgencia de un caso.
    
    Args:
        texto: Descripción del caso
        
    Returns:
        Nivel de urgencia: "Muy Alta", "Alta", "Media", "Baja"
    """
    pass
```

### Testing

- Tests en `tests/`
- Nombra: `test_nombre_funcion`
- Coverage mínimo: 70%

```python
def test_clasificar_urgencia_riesgo_inmediato():
    resultado = clasificar_urgencia("Me quiero matar")
    assert resultado == "Muy Alta"
```

## Áreas de contribución

### Código

- Motor IA y procesamiento NLP
- Interfaz UI/UX
- Base de datos y queries
- Generador de reportes
- Cifrado y seguridad

### Documentación

- Especificación técnica
- Manual de usuario
- Guías de instalación
- API documentation

### Testing

- Tests unitarios
- Tests de integración
- Casos edge

### Datos

- Bases de conocimiento
- Plantillas de respuestas
- Recursos por país/región

## Código de conducta

- Sé respetuoso
- Comunica de forma clara
- Aceptá feedback constructivo
- Enfocate en el objetivo social

## Preguntas

- 📖 [Wiki](https://github.com/Sahilytech/AsistenteONG/wiki)
- 💬 [Discusiones](https://github.com/Sahilytech/AsistenteONG/discussions)
- 🐛 [Issues](https://github.com/Sahilytech/AsistenteONG/issues)

---

**¡Gracias por cambiar vidas a través del código!** ❤️
