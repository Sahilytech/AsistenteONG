# 🆘 Asistente ONG v0.9 - Triaje y Canalización PROFESIONAL

<div align="center">

![Asistente ONG](assets/logo_g.png)

**Herramienta Offline 100% para Líneas de Ayuda, ONGs y Organizaciones Sociales**

[![License: Social Ética 2026](https://img.shields.io/badge/License-Social%20Ética%202026-red)](LICENSE_SOCIAL.md)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue)](https://www.python.org)
[![Offline 100%](https://img.shields.io/badge/Offline-100%25-green)](docs/privacy.md)
[![Social Focus](https://img.shields.io/badge/Enfoque-Social%20%26%20Ético-purple)](docs/vision.md)

**Apoyado por** 🤝 [CCOMUSOC](https://ccomusoc.com.ar) - Cooperativa de Tecnología Social

</div>

---

## 📌 ¿QUÉ ES?

Una herramienta **gratuita, offline y ética** que ayuda a ONGs, líneas de ayuda y organizaciones sociales a:

✅ **Triaje Inteligente** - Clasifica urgencia de casos automáticamente  
✅ **+320 Palabras Clave** - Detecta violencia, crisis, emergencias  
✅ **Respuestas Automáticas** - Genera borradores personalizados  
✅ **+150 Recursos Locales** - Teléfonos, hospitales, refugios, abogados  
✅ **Sistema de Casos** - Auto-generación de IDs, filtros, historial  
✅ **Privacidad Garantizada** - 100% Offline, sin envío de datos  
✅ **UI Profesional** - Modo claro y oscuro, intuitivo  
✅ **Licencia Ética** - No se puede vender, NO adulterarlo  

---

## 🎯 CARACTERÍSTICAS v0.9

### 🚨 Motor de Análisis Inteligente
- **+320 palabras clave** en 9 categorías
- Detecta riesgo de vida, violencia, menores, salud mental
- Clasifica en 4 niveles: Muy Alta, Alta, Media, Baja
- **<500ms** análisis por caso
- **100% Offline** - Sin conexión a internet

### 📝 Respuestas Automáticas Personalizadas
- Borradores según urgencia detectada
- Teléfonos y recursos locales integrados
- Instrucciones paso a paso
- Editable en UI + copiar al portapapeles
- Seleccionar/copiar texto individual

### 📊 Sistema de Casos Profesional
- **IDs automáticos**: CASE-202608-00001
- Almacenamiento persistente en SQLite
- Filtros: por urgencia, estado, mes, operador
- Ordenamiento: por fecha, urgencia, número
- Exportar a JSON/CSV
- Historial completo

### 🔍 Dashboard Completo
- Total de casos procesados
- Estadísticas por urgencia
- Casos hoy/semana/mes
- Historial visual con timestamps
- Gráficos de estadísticas

### 📞 +150 Recursos Locales
- **Líneas de Crisis**: 7+ números 24/7
- **Refugios**: 6+ locaciones verificadas
- **Hospitales**: Emergencias + especialidades
- **Abogados**: Asesoría legal gratuita
- **Psicólogos**: Salud mental
- **Líneas Especializadas**: Violencia sexual, trata, abuso infantil
- **Instituciones Públicas**: Comisarías, juzgados

Búsqueda por: tipo, ciudad, especialidad, disponibilidad

### 🎨 UI Profesional 100%
- **6 Tabs**: Dashboard | Análisis | Recursos | Config | Ayuda | Creadora
- **Modo Claro/Oscuro**: Completo en ambos
- **Logo CCOMUSOC**: Integrado profesionalmente
- **Branding**: Colores sociales (Azul #0e98d6, Blanco, Negro)
- **Tutorial Interno**: 6 secciones de ayuda
- **Responsive**: 2000x950px optimizado

### 🔒 Privacidad & Seguridad
- **100% OFFLINE**: No necesita internet
- **AES-256**: Encriptación de datos
- **SQLite Local**: Base de datos en computadora
- **GDPR Compatible**: Protección de datos
- **Cero Telemetría**: No hay rastreo

### 👩‍💻 Información de Creadora
- Sarah Lee Olivera - Desarrolladora
- Email: sarahleeoliveraok@gmail.com
- **CCOMUSOC**: Apoyo organizacional
- Web: ccomusoc.com.ar
- Misión: Tecnología para bien social

---

## 📦 REQUISITOS

**Mínimo:**
- Python 3.11+
- Windows 10/11, macOS, Linux
- 2GB RAM
- 500MB disco

**Opcional:**
- Modelo IA local: +2GB VRAM

---

## 🚀 INSTALACIÓN RÁPIDA

### 1️⃣ Desde Python (Desarrollo)
```bash
git clone https://github.com/Sahilytech/AsistenteONG.git
cd AsistenteONG
pip install -r requirements.txt
python -m src.main
```

### 2️⃣ Ejecutable .exe (Usuarios)
```bash
# En Windows, ejecuta:
build_exe.bat
# Genera: dist/AsistenteONG.exe
```

Luego simplemente:
- Copiar `AsistenteONG.exe` a pendrive
- Hacer doble-click en cualquier PC
- Funciona sin instalar nada

---

## 📋 USO RÁPIDO

1. **Ingresa un caso:**
   - Número: Se genera automático (CASE-202608-00001)
   - Texto: Descripción del caso
   - Clic: "✅ Analizar caso"

2. **El sistema:**
   - Detecta urgencia automáticamente
   - Genera respuesta borrador
   - Sugiere recursos
   - Guarda en historial

3. **Filtra y organiza:**
   - Por urgencia (Muy Alta, Alta, etc)
   - Por estado (nuevo, en progreso, resuelto)
   - Por mes/fecha
   - Exporta a JSON/CSV

---

## 🎯 CASOS DE USO REALES

### Línea de Ayuda por Violencia
```
Llamada entrante:
"Mi pareja me golpeó"
          ↓
Sistema detecta: [VIOLENCIA DOMÉSTICA]
Urgencia: ALTA
          ↓
Respuesta: "Plan de seguridad inmediato..."
Teléfonos: Casa de Tránsito, Abogado
          ↓
Caso guardado con ID automático
Operador contacta recursos
```

### ONG de Derechos Humanos
```
Reportes de violaciones
          ↓
Sistema agrupa por urgencia
Exporta estadísticas
Investiga patrones
Genera reportes PDF
```

### Asesoría Legal Comunitaria
```
Consulta sobre derechos
          ↓
Clasifica tipo de caso
Sugiere recursos legales
Genera resumen para abogado
Guarda histórico
```

---

## 📊 ESTADÍSTICAS

- **+320 Palabras Clave**: En 9 categorías
- **+150 Recursos**: Teléfonos y locaciones
- **6 Tabs Principales**: Organización profesional
- **Auto-generación IDs**: CASE-YYYYMM-XXXXX
- **Exportación**: JSON/CSV
- **Filtros Avanzados**: 10+ criterios

---

## 🔒 PRIVACIDAD Y ÉTICA

### Garantías
✅ Código abierto (visible, auditable)  
✅ 100% OFFLINE (sin internet)  
✅ Datos locales (no compartidos)  
✅ GDPR compatible  
✅ Enfocado en bien social  

### Restricciones Éticas
❌ No se puede vender  
❌ No se puede adulterar  
❌ No se puede usar para explotación  
❌ No se puede remover créditos  
❌ No se puede violar privacidad  

Ver [LICENSE_SOCIAL.md](LICENSE_SOCIAL.md) para detalles completos.

---

## 📖 DOCUMENTACIÓN

- **README.md**: Este archivo
- **LICENSE_SOCIAL.md**: Licencia Ética 2026
- **INSTALL.md**: Guía instalación paso a paso
- **docs/**: Arquitectura, IA, Seguridad
- **PRUEBA.md**: Guía de pruebas

---

## 🤝 CONTRIBUCIONES

¿Querés mejorar esto? ¡Bienvenido!

### Buscamos:
- 🌍 Traductores (EN, PT, FR, etc)
- 🔑 Más palabras clave específicas
- 📞 Más números/recursos locales
- 🐛 Beta testers
- 📚 Documentación en otros idiomas
- ⚙️ Desarrolladores para features

**Requisitos:**
- Ser ético y comprometido con bien social
- No comercializar
- Mantener privacidad
- Respetar licencia

---

## 📞 SOPORTE

- **Email**: sarahleeoliveraok@gmail.com
- **GitHub Issues**: https://github.com/Sahilytech/AsistenteONG/issues
- **CCOMUSOC**: contacto@ccomusoc.com.ar (ccomusoc.com.ar)

---

## 👩‍💻 CREADORA

**Sarah Lee Olivera**
- Desarrolladora Full Stack
- Especialista en IA Offline
- Comprometida con tecnología social
- Argentina 🇦🇷

*"La tecnología debe servir para proteger y ayudar, nunca para explotar."*

---

## 🏛️ APOYO ORGANIZACIONAL

**CCOMUSOC** - Cooperativa de Tecnología Social
- **Web**: ccomusoc.com.ar
- **Misión**: Democratizar tecnología para bien común
- **Apoyo**: Institucional, legal, comunitario

---

## 📄 LICENCIA

**Licencia Social Ética 2026**
- ✅ Gratis para ONGs, fundaciones, instituciones sociales
- ✅ Código abierto para auditoría
- ✅ Offline 100%
- ❌ No se puede vender
- ❌ No se puede adulterar
- ❌ No se puede usar para explotación

Ver [LICENSE_SOCIAL.md](LICENSE_SOCIAL.md)

---

## 🌟 RECONOCIMIENTOS

Hecho con ❤️ para:
- Víctimas de violencia que merecen ayuda
- ONGs que trabajan sin recursos
- Operadores de líneas de ayuda agotados
- Comunidades marginadas

---

## 🎯 HOJA DE RUTA

### v0.9 ✅ ACTUAL
- Sistema de casos automático
- +150 recursos
- UI completa light/dark
- Licencia ética restrictiva

### v1.0 (Próximo)
- [ ] 2FA (TOTP)
- [ ] Multi-idioma
- [ ] Reportes PDF
- [ ] Integración WhatsApp
- [ ] Firma digital RSA

### v2.0 (Futuro)
- [ ] Síncronización offline-first
- [ ] IA más inteligente
- [ ] Capacitación incluida
- [ ] Análisis de patrones
- [ ] Red de ONGs

---

**v0.9** | Profesional | Ético | Offline 100% | ✅ Listo para usar

Última actualización: Agosto 2026

---

*Si usas esto, por favor cita: "Asistente ONG - Sarah Lee Olivera & CCOMUSOC"*
