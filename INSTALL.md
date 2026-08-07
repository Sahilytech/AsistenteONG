# 📥 INSTALACIÓN - Asistente ONG v0.8

## Windows 10/11

### Método 1: Desde Python (Recomendado)

**1. Descargar Python**
- Ve a https://www.python.org
- Descargar "Python 3.11" o superior
- ✅ MARCAR: "Add Python to PATH"
- Instalar

**2. Descargar proyecto**
```bash
# Abrir PowerShell o CMD
git clone https://github.com/Sahilytech/AsistenteONG.git
cd AsistenteONG
```

**3. Instalar dependencias**
```bash
pip install customtkinter pillow cryptography
```

**4. Ejecutar**
```bash
python -m src.main
```

¡Listo! La app debería abrir en segundos.

---

### Método 2: Ejecutable .exe (Próximamente)

Simplemente descargar y hacer doble clic.

---

## macOS

```bash
# Instalar Homebrew (si no lo tienes)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Descargar proyecto
git clone https://github.com/Sahilytech/AsistenteONG.git
cd AsistenteONG

# Instalar Python
brew install python@3.11

# Instalar dependencias
pip3 install customtkinter pillow cryptography

# Ejecutar
python3 -m src.main
```

---

## Linux (Ubuntu/Debian)

```bash
# Instalar Python
sudo apt-get update
sudo apt-get install python3.11 python3-pip git

# Descargar proyecto
git clone https://github.com/Sahilytech/AsistenteONG.git
cd AsistenteONG

# Instalar dependencias
pip install customtkinter pillow cryptography

# Ejecutar
python -m src.main
```

---

## 🆘 TROUBLESHOOTING

### "Python no se reconoce"
```
Error: 'python' is not recognized
```
**Solución**: Instala Python desde https://www.python.org  
✅ MARCA "Add Python to PATH"

### "No module named 'customtkinter'"
```bash
pip install customtkinter --upgrade
```

### "La ventana no abre"
1. Abre terminal/PowerShell como Administrador
2. Navega al proyecto: `cd C:\Users\...\AsistenteONG`
3. Ejecuta con logging: `python -m src.main`
4. Copia el error y abre un issue en GitHub

### "ImportError: no module named src"
```bash
# Asegúrate de estar en la carpeta correcta
cd AsistenteONG
python -m src.main
```

### La app es muy lenta
- Cierra otras aplicaciones
- Aumenta RAM disponible
- Reinicia la computadora

---

## ✅ VERIFICAR INSTALACIÓN

```bash
python -c "import customtkinter; print('✅ CustomTkinter OK')"
python -c "import PIL; print('✅ Pillow OK')"
python -c "import cryptography; print('✅ Cryptography OK')"
```

Si todo dice "✅ OK", estás listo.

---

## 🚀 PRIMEROS PASOS

1. Abre la app: `python -m src.main`
2. Ve al Tab "📊 Dashboard"
3. En la izquierda, ingresa:
   - Número: `CASE-2025-001`
   - Texto: `"Mi pareja me golpeó y tengo miedo"`
4. Clic en "✅ Analizar caso"
5. Verás análisis automático en el tab "📋 Análisis"

---

## 📦 PRÓXIMO: GENERAR .EXE

Para crear un ejecutable único (sin necesidad de Python):

```bash
pip install pyinstaller

pyinstaller --onefile --windowed \
  --icon=assets/logo_g.png \
  --name AsistenteONG \
  src/main.py
```

El .exe estará en `dist/AsistenteONG.exe`

---

**¿Problemas?** Abre un issue: https://github.com/Sahilytech/AsistenteONG/issues
