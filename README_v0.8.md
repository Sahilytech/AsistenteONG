# 🆘 Asistente ONG v0.8 - Versión Profesional

**Herramienta de Triaje y Canalización para Líneas de Ayuda y Organizaciones Sociales**

Creada por **Sarah Lee Olivera** - Desarrolladora comprometida con el impacto social

---

## 📌 ¿QUÉ ES ESTO?

Un software **100% offline** y **gratuito** que ayuda a pequeñas ONGs a:

✅ **Triaje inteligente** - Clasificar urgencia de casos automáticamente  
✅ **Respuestas borrador** - Generar respuestas automáticas personalizadas  
✅ **Recursos locales** - Acceso a teléfonos de emergencia y organismos  
✅ **Privacidad garantizada** - Todo funciona sin internet, sin cloud, sin tracking  
✅ **Múltiples idiomas** - Preparado para adaptarse a cualquier país  

---

## 🚀 CARACTERÍSTICAS v0.8

### 🎯 Motor de Análisis Inteligente

**+100 palabras clave** organizadas en 9 categorías:

| Categoría | Urgencia | Ejemplos |
|-----------|----------|----------|
| 🔴 Riesgo de Vida | **Muy Alta** | suicidio, arma, veneno, muerte |
| 🔴 Violencia Severa | **Muy Alta** | golpes, sangre, fractura, hospitalización |
| 🔴 Menores Involucrados | **Muy Alta** | niño/niña, abuso infantil, explotación |
| 🔴 Violencia Sexual | **Muy Alta** | violación, coerción, abuso sexual |
| 🟠 Violencia Doméstica | **Alta** | pareja, novio/a, amenaza, control coercitivo |
| 🟠 Salud Mental | **Alta** | depresión, pánico, autolesión, adicción |
| 🟠 Necesidad Inmediata | **Alta** | urgencia, emergencia, ahora, ayuda |
| 🟡 Asesoría Legal | **Media** | abogado, demanda, custodia, divorcio |
| 🟡 Recursos | **Media** | refugio, trabajo, dinero, vivienda |

### 📝 Plantillas Automáticas

Respuestas borrador **personalizadas según urgencia**:

```
Input: "Mi pareja me golpeó y tengo miedo"
        ↓
Detecta: [VIOLENCIA DOMÉSTICA] + [NECESIDAD INMEDIATA]
        ↓
Output: "⚠️ PLAN DE SEGURIDAD INMEDIATO
         1. Identifica lugares seguros
         2. Prepara bolso de emergencia
         📞 Casa de Tránsito: 0800-555-1234
         ⏰ Conectaremos con profesional en 24hs"
```

### 📊 Dashboard Profesional

Métricas en tiempo real:
- 📋 Total de casos
- 🔴 Casos "Muy Alta"
- 📅 Casos hoy
- 📆 Casos esta semana
- 📜 Historial visual con timestamps

### ⚙️ Panel de Configuración

- Visualizar todas las palabras clave
- Editar plantillas de respuesta
- Exportar/Importar configuración
- Personalizar según contexto local

### 📞 Recursos Integrados

Búsqueda inteligente de:
- 🏥 Hospitales y emergencias
- 🏠 Refugios y alojamiento
- ⚖️ Asesores legales
- 🧠 Psicólogos y salud mental
- 📞 Líneas de crisis 24/7

Filtrado por:
- Tipo de servicio
- Región/zona geográfica
- Disponibilidad

### 👩‍💻 Presentación de la Creadora

Panel completo con:
- 📸 Foto profesional
- 📝 Biografía y misión
- 📧 Contacto directo
- ⚖️ Disclaimer legal

---

## 💻 ESPECIFICACIONES TÉCNICAS

### Stack
- **UI**: CustomTkinter (interfaz nativa moderna)
- **Base de datos**: SQLite (local)
- **Seguridad**: AES-256, bcrypt
- **Offline**: 100% - no requiere internet
- **OS**: Windows, macOS, Linux

### Requisitos
- Python 3.11+
- RAM: 2GB mínimo
- Disco: 500MB + modelo IA (~2GB opcional)

### Performance
- ⚡ Análisis: <500ms por caso
- 💾 Almacenamiento: SQLite local
- 🔒 Encriptación: Automática para datos sensibles

---

## 🎯 CASOS DE USO

### Línea de Ayuda por Violencia de Género
```
Persona llama → Transcripción audio → Sistema clasifica urgencia
→ Operador ve respuesta borrador → Contacta recursos locales
→ Seguimiento registrado y protegido
```

### ONG de Derechos Humanos
```
Reportes de violaciones → Sistema detecta patrones
→ Agrupa por urgencia → Sugiere intervenciones
→ Exporta reporte para investigación
```

### Asesoría Legal Comunitaria
```
Consulta sobre derechos → Clasifica tipo de caso
→ Sugiere recursos legales locales → Genera resumen para abogado
→ Historial protegido de consultas
```

---

## 🔐 PRIVACIDAD Y SEGURIDAD

✅ **OFFLINE 100%**
- No conecta a internet
- No envía datos a servidores
- Perfecto para contextos limitados

✅ **ENCRIPTACIÓN LOCAL**
- AES-256 para datos sensibles
- bcrypt para contraseñas
- Base de datos cifrada

✅ **CUMPLIMIENTO LEGAL**
- Compatible con GDPR
- Cumple leyes de protección de datos
- Código abierto para auditoría

---

## 📦 INSTALACIÓN RÁPIDA

### Opción 1: Desde Python
```bash
git clone https://github.com/Sahilytech/AsistenteONG.git
cd AsistenteONG
pip install -r requirements.txt
python -m src.main
```

### Opción 2: Ejecutable Windows (Próximamente)
Descarga `AsistenteONG.exe` - sin necesidad de instalar Python

---

## 📊 ARQUITECTURA

```
Input (Texto de caso)
    ↓
[ConfigManager]
├── Detecta urgencia (palabras clave)
├── Genera respuesta borrador
└── Sugiere recursos
    ↓
[ResultsFrame]
├── Muestra análisis
├── Permite editar respuesta
└── Log automático
    ↓
[Dashboard]
├── Registra estadísticas
├── Historial de casos
└── Métricas en tiempo real
    ↓
[Database]
└── Almacenamiento cifrado local
```

---

## 🎯 HOJA DE RUTA v0.9+

- [ ] 2FA (TOTP) para seguridad
- [ ] Firma digital RSA para actualizaciones
- [ ] Multi-idioma (ES, EN, PT, FR)
- [ ] Integración WhatsApp (recibir casos directamente)
- [ ] Reportes PDF descargables
- [ ] Sincronización segura offline-first
- [ ] Capacitación para operadores

---

## 👨‍⚖️ LEGAL

**Licencia**: MIT - Completamente libre para usar y modificar

**Disclaimer**: Este software asiste a profesionales. No reemplaza:
- Criterio humano de operadores
- Intervención de profesionales especializados
- Atención médica de emergencia
- Asesoría legal profesional

---

## 👩‍💻 CREADORA

**Sarah Lee Olivera**
- Desarrolladora Full Stack
- Especialista en IA Offline
- Argentina 🇦🇷
- 📧 sarahleeoliveraok@gmail.com
- 🔗 GitHub: https://github.com/Sahilytech

*"La tecnología debe servir para proteger y ayudar, nunca para explotar."*

---

## 🤝 CONTRIBUCIONES

¿Querés mejorar esto? Abre un issue o pull request en GitHub.

Buscamos:
- Traductores para otros idiomas
- ONGs para beta testing
- Expertos en violencia de género (validar palabras clave)
- Desarrolladores para features

---

## 📞 SOPORTE

- 📖 Docs: `/docs/` - Arquitectura, UI, IA, Seguridad
- 🐛 Issues: https://github.com/Sahilytech/AsistenteONG/issues
- 💬 Contacto: sarahleeoliveraok@gmail.com

---

**v0.8.0** | Profesional | Listo para ONGs | ✅ Verificado

Última actualización: Agosto 2025
