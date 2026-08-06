# 📖 GUÍA DE USO - Asistente ONG

**Para operadores de líneas de ayuda y organizaciones sociales**

---

## ¿QUÉ ES ESTO?

Una **herramienta offline profesional** que ayuda a atender casos de violencia, abuso y asesoría legal **SIN conexión a internet**.

### El problema que resuelve:
- Las ONGs reciben DECENAS de mensajes desesperados
- No tienen suficientes manos ni tiempo
- Los datos sensibles viajaría por internet (riesgo)
- Necesitan responder RÁPIDO y profesionalmente

### La solución:
- **En un pendrive**
- **Análisis automático** de urgencia
- **Redacción de respuestas** borrador
- **Base de datos local** de emergencias
- **100% OFFLINE** - Privacidad garantizada

---

## 🚀 INSTALACIÓN (5 minutos)

### Requisito: Windows 10/11

### Paso 1: Descargar Python
1. Ve a https://www.python.org/downloads/
2. Descarga Python 3.11 o superior
3. **IMPORTANTE**: Marca ✅ "Add Python to PATH"
4. Click "Install Now"

### Paso 2: Descargar la herramienta
```bash
# Abrir PowerShell o CMD

cd Escritorio
git clone https://github.com/Sahilytech/AsistenteONG.git
cd AsistenteONG
```

### Paso 3: Instalar dependencias
```bash
pip install customtkinter pillow cryptography
```

### Paso 4: Ejecutar
```bash
python -m src.main
```

¡Listo! La ventana debe abrir.

---

## 💡 CÓMO USAR

### La Interfaz

```
┌─────────────────────────────────────────────────────┐
│  🆘 ASISTENTE ONG                   [🌓]            │
├────────────────────────────────┬────────────┬────────┤
│                                │            │        │
│  📝 NUEVO CASO                 │ 📊 ANÁLISIS│ 📖 TAB │
│                                │            │        │
│  Número: [CASE-2025-001]       │ 🚨 URGENCIA│        │
│                                │ ⚠️ RIESGOS │ TAB 2  │
│  Descripción:                  │ 🔍 PALABRAS│        │
│  [________________]            │ 📝 RESPUESTA   TAB 3  │
│  [________________]            │            │        │
│                                │            │        │
│  [✅ ANALIZAR] [🗑️ LIMPIAR]     │            │        │
└────────────────────────────────┴────────────┴────────┘
```

### Paso a Paso

#### 1. INGRESA UN CASO

Ejemplo:
```
Número: CASE-2025-001
Descripción: "Mi pareja me golpeó la cara y me amenazó con matarme. 
Tengo un hijo de 5 años asustado. No sé qué hacer."
```

#### 2. CLIC EN "ANALIZAR CASO"

El sistema:
- 🔍 Analiza el texto
- 🚨 Detecta palabras clave de urgencia
- ⚠️ Identifica riesgos (menores, violencia, etc)
- 📝 Redacta una respuesta automática

#### 3. LEE LOS RESULTADOS

**Panel Central muestra:**
- **🚨 Urgencia Detectada**: MUY ALTA / ALTA / MEDIA / BAJA
- **Score**: 0-10 (qué tan urgente)
- **⚠️ Riesgos Detectados**: Los problemas específicos encontrados
- **🔍 Palabras Clave**: Qué frases activaron la urgencia
- **📝 Respuesta Automática**: Borrador para enviar

#### 4. COPIA LA RESPUESTA

- Lee el borrador
- Haz cambios si necesitas (la herramienta sugiere, TÚ decides)
- Clic "📋 Copiar Respuesta"
- Pega en WhatsApp/SMS/correo y envía

---

## 🔍 EJEMPLO PRÁCTICO

### Ingreso:
```
CASE-2025-002
"Llevo 3 años con abuso psicológico. Mi pareja controla 
mi dinero, no me deja trabajar, me insultaGa todos los días. 
Tengo miedo de dejarle por la reacción. No tengo donde ir."
```

### El Sistema Detecta:
- 🚨 **URGENCIA: ALTA** (Score: 6.8/10)
- ⚠️ **RIESGOS**:
  - Abuso psicológico documentado
  - Control económico (abuso)
  - Miedo a represalias
  - Sin recursos de apoyo

### Respuesta Generada:
```
---RESPUESTA BORRADOR---

Estimada,

Hemos recibido tu mensaje y entendemos tu situación.

🔴 SITUACIÓN GRAVE DETECTADA
Te recomendamos contactar:
📞 Línea de Asesoría Legal: 0800-333-4444
📞 Refugio Seguro 24/7: 0800-555-1234

PASOS RECOMENDADOS:
1. Busca un lugar seguro si es necesario
2. Contacta un abogado/asesor legal
3. Considera una denuncia formal si corresponde
4. Documenta los hechos (fechas, eventos)
5. Busca apoyo emocional y psicológico

PROTECCIÓN LEGAL:
📞 Defensoría Pública: 4321-0987
📞 Centro Jurídico: 5678-1234

PRIVACIDAD Y SEGURIDAD:
✓ Este mensaje fue procesado OFFLINE (sin internet)
✓ Tus datos NO fueron enviados a servidores externos
✓ La información está cifrada y segura

Estamos aquí para apoyarte.
No estás sola. Hay recursos y personas listos para ayudar.

---FIN RESPUESTA BORRADOR---
```

---

## 📞 TAB 1: INICIO

Información sobre el proyecto:
- Qué es
- Por qué existe
- Características principales

---

## 🔍 TAB 2: RECURSOS

Búsqueda de emergencias locales:

1. **Selecciona Tipo:**
   - 🏥 Hospital
   - 🏠 Refugio
   - ⚖️ Asesoría Legal
   - 🧠 Psicólogo
   - 📞 Línea Crisis

2. **Selecciona Región:**
   - Todas
   - CABA
   - GBA
   - Nacional
   - Otro

3. **Busca**

Verás:
- Nombre de la organización
- ☎️ Teléfono (copiable)
- 📍 Región
- 🕐 Horarios

---

## 👩‍💻 TAB 3: SOBRE SARAH

Información sobre la creadora:
- **Sarah Lee Olivera**
- Desarrolladora & Creadora
- Contacto
- Biografía completa
- Misión del proyecto

---

## ⚙️ CONFIGURACIÓN

Tema claro/oscuro:
- Botón **🌓 Cambiar tema** (arriba a la derecha)

---

## 🔐 PRIVACIDAD

✅ **TODO ES OFFLINE**
- Los casos NO se envían a internet
- Los datos NO se guardan en la nube
- Nadie en internet ve la información
- Funciona sin WiFi ni datos móviles

✅ **DATOS CIFRADOS**
- AES-256 en reposo
- Acceso protegido con contraseña
- Auditoría completa de acciones

---

## 🆘 EMERGENCIAS RÁPIDAS

Si alguien está en **PELIGRO INMEDIATO**:

```
Urgencia Detectada: MUY ALTA

📞 LLAMAR A LA POLICÍA: 911
📞 EMERGENCIAS MÉDICAS: 107 (CABA) / 911
📞 LÍNEA DE CRISIS 24/7: 0800-666-7777
```

---

## 📝 NOTAS IMPORTANTES

### ✓ La herramienta sugiere, TÚ DECIDES
- Los borradores son SUGERENCIAS
- Revisa siempre antes de enviar
- Tu criterio es la autoridad final
- Personaliza según el contexto

### ✓ Proteges a víctimas
- No envíes la respuesta original (personaliza)
- Cámbiala para que suene natural
- Añade tu número de línea
- Hazla personal

### ✓ No reemplaza profesionales
- Abogados para cuestiones legales
- Psicólogos para trauma
- Médicos para lesiones
- Policía para delitos

---

## 🚀 DISTRIBUCIÓN EN PENDRIVE

Para llevar la herramienta a oficinas sin internet:

1. **Genera .exe:**
```bash
pip install pyinstaller
pyinstaller --onefile --name AsistenteONG src/main.py
```

2. **Copia a pendrive:**
   - Carpeta: `dist/AsistenteONG.exe`
   - Péndrive de 500MB es suficiente

3. **En otros PCs:**
   - Copia el .exe
   - Doble clic para ejecutar
   - No necesita Python instalado

---

## 🐛 TROUBLESHOOTING

**Problema: "Python no reconocido"**
```
→ Reinstala Python
→ Marca ✅ "Add Python to PATH"
```

**Problema: "No module named customtkinter"**
```bash
pip install customtkinter
```

**Problema: La app se abre pero está vacía**
```
→ Espera 2 segundos
→ Resizeiona la ventana (arrastra la esquina)
```

**Problema: El botón "Analizar" no funciona**
```
→ Abre PowerShell como Administrador
→ Cd al folder de la app
→ python -m src.main
→ Mira qué error aparece en la terminal
```

---

## 📧 CONTACTO

**Creadora:** Sarah Lee Olivera  
📧 Email: sarahleeoliveraok@gmail.com  
🔗 GitHub: https://github.com/Sahilytech/AsistenteONG

---

## ⚖️ LICENCIA

MIT License - Código abierto orientado al bien común

---

**Versión:** v0.7.0 - Beta  
**Última actualización:** Agosto 2025

Gracias por usar esta herramienta para proteger a quienes más lo necesitan. 💙

