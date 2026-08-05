# Asistente de Triaje y Canalización para Líneas de Ayuda

**Una herramienta offline para ONGs que atienden casos de violencia, derechos humanos y asesoría legal.**

## 🎯 Visión

Reducir el tiempo de espera para obtener una primera orientación en organizaciones sociales con recursos limitados, protegiendo completamente la privacidad de las víctimas al funcionar 100% offline.

## 🚀 Características

- ✅ **Offline completo** — Sin enviar datos a internet
- ✅ **Motor IA local** — Modelo GGUF pequeño (1-2GB)
- ✅ **Clasificación automática** — Detecta urgencia, tipo de caso, personas involucradas
- ✅ **Canalización inteligente** — Sugiere recursos y organismos
- ✅ **Respuesta borrador** — Asiste al operador
- ✅ **Cifrado end-to-end** — Datos protegidos en local
- ✅ **Portátil** — Ejecutable en pendrive o `.exe` en Windows
- ✅ **Fácil de actualizar** — Paquetes de conocimiento

## 📋 Público objetivo

- ONGs de violencia de género
- Organizaciones de derechos humanos
- Defensorías públicas
- Centros jurídicos comunitarios
- Municipios
- Refugios
- Consultorios de salud mental

## 🛠️ Tecnologías

| Componente | Tecnología |
|-----------|-----------|
| Lenguaje | Python 3.11+ |
| Interfaz | CustomTkinter |
| Base de datos | SQLite |
| IA local | llama.cpp + Gemma 3 1B |
| Reportes | ReportLab |
| Cifrado | cryptography |
| Ejecutable | PyInstaller |
| Testing | pytest |

## 📁 Estructura del repositorio

```
AsistenteONG/
├── src/              # Código fuente
│   ├── ui/          # Interfaz CustomTkinter
│   ├── ai/          # Lógica de IA y procesamiento
│   ├── database/    # Manejo de SQLite
│   ├── reports/     # Generación de PDF y reportes
│   ├── security/    # Cifrado y acceso
│   ├── updater/     # Gestión de actualizaciones
│   └── utils/       # Utilidades
├── data/            # Datos y recursos
│   ├── plantillas/  # Plantillas de respuestas
│   ├── recursos/    # Organismos, teléfonos
│   ├── leyes/       # Normativas locales
│   └── emergencias/ # Números de emergencia
├── docs/            # Documentación
├── tests/           # Tests unitarios
├── models/          # Modelos GGUF
└── build/           # Artefactos de compilación
```

## 🚀 Inicio rápido

### Requisitos

- Python 3.11+
- pip
- Git

### Instalación

```bash
git clone https://github.com/Sahilytech/AsistenteONG.git
cd AsistenteONG
pip install -r requirements.txt
python src/main.py
```

## 📚 Documentación

- [Visión y objetivos](docs/vision.md)
- [Arquitectura del sistema](docs/arquitectura.md)
- [Guía de instalación](docs/instalacion.md)
- [Manual del usuario](docs/manual_usuario.md)
- [Guía de desarrollo](docs/desarrollo.md)
- [Roadmap](docs/roadmap.md)

## 🗺️ Roadmap

- **v0.1** — Diseño y documentación ✅
- **v0.2** — Base de datos y esquema
- **v0.3** — Interfaz gráfica básica
- **v0.4** — Motor IA offline
- **v0.5** — Generador de reportes
- **v0.6** — Seguridad y cifrado
- **v0.7** — Actualizador
- **v0.8** — Pruebas
- **v0.9** — Beta pública
- **v1.0** — Lanzamiento oficial

## 🤝 Cómo contribuir

Leé [CONTRIBUTING.md](CONTRIBUTING.md) para conocer cómo participar en el proyecto.

## 📄 Licencia

Este proyecto está bajo licencia [MIT License](LICENSE) para que otras organizaciones puedan usar y mejorar la herramienta libremente.

## 💬 Preguntas y soporte

- 📖 [Wiki del proyecto](https://github.com/Sahilytech/AsistenteONG/wiki)
- 🐛 [Issues y bugs](https://github.com/Sahilytech/AsistenteONG/issues)
- 💬 [Discusiones](https://github.com/Sahilytech/AsistenteONG/discussions)

## 🙌 Reconocimientos

Proyecto desarrollado con ❤️ para ONGs que cambian vidas.

---

**Nota importante:** Esta herramienta **asiste pero nunca reemplaza** la decisión de operadores capacitados. En situaciones de riesgo inmediato, siempre se debe activar emergencias y servicios competentes.
