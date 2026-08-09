# Inicio rápido — Asistente ONG

## Windows 10/11

### Ejecutar desde el repositorio

```bat
git clone https://github.com/Sahilytech/AsistenteONG.git
cd AsistenteONG
run_app.bat
```

El lanzador crea un entorno virtual, instala las dependencias y ejecuta la aplicación.

### Ejecutar manualmente

```bat
cd AsistenteONG
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m src.main
```

### Generar el ejecutable de Windows

```bat
build_exe.bat
```

El resultado queda en:

```text
dist\AsistenteONG.exe
```

### Flujo de uso

1. Abrí la aplicación.
2. Seleccioná **Nuevo caso**.
3. Cargá únicamente la información disponible de la persona o situación real que estés atendiendo.
4. Ejecutá el análisis y revisá los indicadores.
5. Para un informe social, abrí **Informe Social** y completá los siete bloques.
6. Si corresponde, fijá los datos institucionales para reutilizarlos en futuros informes.
7. Analizá, revisá profesionalmente y recién después exportá el PDF o JSON.

### Casos y datos iniciales

La aplicación **no incluye casos ficticios, expedientes de demostración ni relatos predeterminados**. Al instalarla, la lista de casos debe comenzar vacía. Los registros se crean únicamente cuando el operador carga información.

### Dependencias

```text
customtkinter
pillow
python-dotenv
cryptography
reportlab
pyinstaller
```

### Solución rápida de errores

**Python no reconocido**

```bat
python --version
```

Instalá Python 3.11 o superior y volvé a abrir la terminal.

**Dependencia faltante**

```bat
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

**La aplicación no inicia**

```bat
python -m src.main
```

Usá la salida de la terminal para identificar el error.

### Privacidad

El triaje, la gestión de casos y el análisis de informes funcionan localmente. Los datos sensibles no se envían automáticamente a servicios externos.

### Documentación

- `README.md` — descripción general.
- `docs/` — arquitectura, seguridad, base de datos y pruebas.
- `USER_GUIDE.md` — guía funcional.
