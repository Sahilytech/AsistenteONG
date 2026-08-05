# Guía de Instalación

## Requisitos del sistema

- **Windows 10+**, **macOS 10.14+** o **Linux** (Ubuntu 20.04+)
- **Python 3.11+**
- **4GB RAM** mínimo
- **500MB** espacio disponible (+ 2GB para modelos IA)
- Conexión a internet (solo para descarga inicial)

## Instalación para desarrollo

### 1. Clonar repositorio

```bash
git clone https://github.com/Sahilytech/AsistenteONG.git
cd AsistenteONG
```

### 2. Crear entorno virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

```bash
cp .env.example .env
# Editar .env si es necesario
```

### 5. Inicializar base de datos

```bash
python -c "from src.database.schema import init_database; init_database()"
```

### 6. Ejecutar la aplicación

```bash
python src/main.py
```

## Instalación para usuarios finales

### Windows (Ejecutable)

1. Descargar `AsistenteONG.exe` desde [Releases](https://github.com/Sahilytech/AsistenteONG/releases)
2. Ejecutar el archivo
3. Seguir wizard de instalación

### En pendrive (Portable)

1. Crear carpeta `AsistenteONG/` en pendrive
2. Copiar:
   - `AsistenteONG.exe`
   - Carpeta `models/`
   - Carpeta `data/`
3. Ejecutar desde pendrive

### macOS

```bash
# Con Homebrew
brew install asistente-ong

# O descargar .dmg desde releases
```

### Linux

```bash
# Distribuido como AppImage
wget https://releases.../AsistenteONG.AppImage
chmod +x AsistenteONG.AppImage
./AsistenteONG.AppImage
```

## Descargar modelos IA

La aplicación te pedirá descargar el modelo la primera vez:

```bash
# O manual:
python -c "from src.ai.model_loader import download_model; download_model()"
```

Esto descargará **Gemma 3 1B** (~2GB) a `models/`

## Verificar instalación

```bash
python -m pytest tests/ -v
```

## Troubleshooting

### Error: ModuleNotFoundError

```bash
# Asegúrate que el venv esté activado
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate
```

### Error: No module named 'customtkinter'

```bash
pip install customtkinter
```

### Base de datos no inicializa

```bash
# Eliminar data/ y reiniciar
rm -rf data/
python src/main.py
```

### Puerto 8000 ya está en uso

```bash
# Cambiar puerto en .env
FLASK_PORT=8001
```

## Soporte

- 📖 [Documentación completa](../docs/)
- 🐛 [Reportar bugs](https://github.com/Sahilytech/AsistenteONG/issues)
- 💬 [Discusiones](https://github.com/Sahilytech/AsistenteONG/discussions)

---

¿Problemas? Abre un [Issue](https://github.com/Sahilytech/AsistenteONG/issues/new) 🆘
