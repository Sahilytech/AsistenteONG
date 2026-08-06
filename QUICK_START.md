# 🚀 Inicio Rápido - Asistente ONG

**Windows 10/11 - Ejecución Local**

## Opción 1: Ejecutar desde Python (Recomendado para desarrollo)

### 1. Actualizar repositorio
```bash
cd AsistenteONG
git pull origin main
```

### 2. Instalar dependencias
```bash
pip install customtkinter cryptography
```

### 3. Ejecutar la aplicación
```bash
python -m src.main
```

O desde la carpeta `src`:
```bash
cd src
python main.py
```

## Opción 2: Generador de .exe (Próximamente)

Para compilar a ejecutable único (sin necesidad de Python):
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name AsistenteONG src/main.py
```

El `.exe` estará en `dist/AsistenteONG.exe`

## Requisitos

- **Python 3.11+** — Descargar de https://www.python.org
- **Git** — Descargar de https://git-scm.com
- **Espacio en disco**: 500 MB mínimo

## Primeros pasos en la aplicación

1. **Abre la app** → Verás 3 paneles:
   - Izquierda: Ingreso de casos
   - Centro: Análisis en tiempo real
   - Derecha: Información sobre la creadora

2. **Prueba con un caso de ejemplo**:
   - Número: `CASE-001`
   - Texto: `"Mi pareja me golpeó y tengo miedo"`
   - Clic en "Analizar caso"

3. **Cambiar tema**: Botón "🌓 Cambiar tema" (arriba a la derecha)

## Troubleshooting

### Error: `No module named 'customtkinter'`
```bash
pip install customtkinter
```

### Error: `Python no reconocido`
- Instala Python desde https://www.python.org
- Marca ✅ "Add Python to PATH" durante instalación

### La ventana no abre
- Abre PowerShell o CMD como Administrador
- Navega a la carpeta del proyecto: `cd C:\ruta\AsistenteONG`
- Ejecuta: `python -m src.main`

## Características

✅ Offline 100% - Sin conexión a internet
✅ Seguro - Datos cifrados localmente
✅ Rápido - <500ms por análisis
✅ Inteligente - IA basada en reglas
✅ Bonito - Interfaz moderna con tema claro/oscuro

## Documentación completa

- `docs/` — Arquitectura, base de datos, seguridad, IA
- `README.md` — Información del proyecto
- `CONTRIBUTING.md` — Cómo contribuir

## Contacto

Creado por **Sarah Lee Olivera**  
📧 sarahleeoliveraok@gmail.com  
🔗 GitHub: https://github.com/Sahilytech/AsistenteONG

---

¿Problemas? Abre un [Issue](https://github.com/Sahilytech/AsistenteONG/issues) en GitHub.
