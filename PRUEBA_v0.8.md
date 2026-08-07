# 🎯 PRUEBA v0.8 - VERSIÓN PROFESIONAL

**Sarah, aquí está tu nueva versión. Completamente profesional y lista para ONGs.**

---

## ⚡ PASOS RÁPIDOS (5 minutos)

### 1️⃣ Actualizar código
```bash
cd C:\Users\sarahl408\AsistenteONG
git pull origin main
```

### 2️⃣ Instalar dependencias
```bash
pip install customtkinter pillow cryptography
```

### 3️⃣ Ejecutar
```bash
python -m src.main
```

**¡La app debería abrir en segundos!**

---

## 🧪 PRUEBAS SUGERIDAS

### Test 1: Ingreso Básico
```
Número: CASE-2025-001
Texto: "Mi pareja me golpeó y tengo miedo"
Clic: "✅ Analizar caso"
```

**Esperado:**
- ✅ Switch automático a tab "📋 Análisis"
- ✅ Muestra urgencia: **ALTA**
- ✅ Detecta palabras clave: [VIOLENCIA DOMÉSTICA]
- ✅ Genera respuesta borrador con teléfonos
- ✅ Sugiere recursos: Refugio, Abogado, Psicólogo
- ✅ Dashboard actualizado: +1 caso, +1 Alta

### Test 2: Caso de Riesgo de Vida
```
Número: CASE-2025-002
Texto: "Quiero suicidarme, no sé qué hacer, tengo miedo"
```

**Esperado:**
- ✅ Urgencia: **MUY ALTA** (rojo)
- ✅ Respuesta: "LÍNEA DE CRISIS DISPONIBLE 24/7"
- ✅ Teléfonos: 0800-666-7777, 911
- ✅ Dashboard: +1 Muy Alta

### Test 3: Caso Legal
```
Número: CASE-2025-003
Texto: "Necesito un abogado para mi custodia"
```

**Esperado:**
- ✅ Urgencia: **MEDIA**
- ✅ Detecta: [ASESORÍA LEGAL]
- ✅ Sugiere: Defensoría Pública, Centro Jurídico

### Test 4: Panel de Recursos
1. Clic en tab "📞 Recursos"
2. Cambiar "Tipo" a "🏥 Hospital"
3. Cambiar "Región" a "CABA"
4. Clic "🔎 Buscar"

**Esperado:**
- ✅ Muestra 2-3 hospitales de CABA
- ✅ Cada uno con teléfono, horario, dirección
- ✅ Botón "📋 Copiar teléfono" funciona

### Test 5: Dashboard
1. Clic en tab "📊 Dashboard"

**Esperado:**
- ✅ Muestra métricas:
  - 📋 Total: 3 casos
  - 🔴 Muy Alta: 1
  - 📅 Hoy: 3
  - 📆 Semana: 3
- ✅ Historial con los 3 casos que ingresaste

### Test 6: Panel de Configuración
1. Clic en tab "⚙️ Config"

**Esperado:**
- ✅ Muestra sección "🚨 Detectores de Urgencia"
- ✅ Lista todas las categorías:
  - Riesgo de Vida (100+ palabras clave)
  - Violencia Severa
  - Menores Involucrados
  - etc
- ✅ Botón "✏️ Editar Plantillas"

### Test 7: Presentación Sarah
1. Clic en tab "👩‍💻 Creadora"

**Esperado:**
- ✅ Tu foto profesional
- ✅ "Sarah Lee Olivera"
- ✅ "Desarrolladora & Creadora del Proyecto"
- ✅ Tu email: sarahleeoliveraok@gmail.com
- ✅ Tu biografía completa
- ✅ Disclaimer legal

### Test 8: Tema Claro/Oscuro
1. Clic botón "🌓 Tema"

**Esperado:**
- ✅ UI cambia a tema claro
- ✅ Colores se invierten
- ✅ Clic again → vuelve a oscuro

---

## 🎨 VERIFICAR BRANDING

✅ **Logo G**
- Visible en header izquierdo
- Blanco sobre negro

✅ **Colores**
- Azul #0e98d6 en acentos (urgencia Alta)
- Blanco en textos
- Negro de fondo

✅ **Foto Sarah**
- Tab "Creadora" debe mostrar tu foto
- Blanco y negro, profesional

✅ **Interfaz**
- 3 paneles: Izquierda (input) | Centro (tabs) | Info
- 5 tabs organizados
- Botones claramente etiquetados

---

## ❌ SI HAY ERRORES

### Error: "No module named..."
```bash
pip install customtkinter pillow cryptography --upgrade
```

### Error: "CASE no se analiza"
- Verifica que el texto no esté vacío
- Intenta con un texto más largo
- Abre terminal y copia error completo

### Error: "Foto no muestra"
- Verifica que `/assets/sarah.jpg` existe
- Intenta con imagen PNG en su lugar
- No es crítico, la app funciona igual

### Ventana no abre
```bash
# Ejecuta con logs
python -m src.main > log.txt 2>&1
# Abre log.txt y copia los errores
```

---

## 📊 CHECKLIST DE VERIFICACIÓN

**UI y Branding:**
- [ ] Logo G visible en header izquierdo
- [ ] Tu foto en tab "Creadora"
- [ ] Colores azul #0e98d6 en lugares correctos
- [ ] 5 tabs funcionando: Dashboard | Análisis | Recursos | Config | Creadora
- [ ] Tema claro/oscuro alterna correctamente

**Análisis:**
- [ ] Ingresa texto → Detecta urgencia automáticamente
- [ ] Genera respuesta borrador
- [ ] Sugerencias de recursos aparecen
- [ ] Palabras clave detectadas se muestran

**Dashboard:**
- [ ] Muestra total de casos
- [ ] Cuenta casos por urgencia
- [ ] Muestra casos de hoy/semana
- [ ] Historial visual con timestamps

**Recursos:**
- [ ] Búsqueda por tipo funciona
- [ ] Búsqueda por región funciona
- [ ] Muestra tarjetas con info
- [ ] Botón copiar teléfono funciona

**Config:**
- [ ] Muestra detectores de urgencia
- [ ] Lista palabras clave por categoría
- [ ] Botón "Editar Plantillas" visible

**Creadora:**
- [ ] Foto de Sarah visible
- [ ] Nombre y email correctos
- [ ] Biografía completa legible
- [ ] Disclaimer legal presente

---

## 📝 FEEDBACK

Después de probar, escribe qué:

1. **Funcionó bien:**
   - ¿Qué features te parecieron útiles?
   - ¿Qué fue lo más rápido/fácil?

2. **Necesita mejora:**
   - ¿Algo que no funcione?
   - ¿UI confusa en algún punto?
   - ¿Faltan palabras clave importantes?

3. **Para ONGs:**
   - ¿Crees que una ONG lo usaría?
   - ¿Qué le falta para ser listo?
   - ¿Cambios de UI necesarios?

---

## 🎯 SIGUIENTES PASOS

Si todo funciona:
1. ✅ Generar .exe para Windows
2. ✅ Probar con 2-3 ONGs reales
3. ✅ Agregar multi-idioma
4. ✅ Integración WhatsApp (recibir casos)
5. ✅ Release v1.0 oficial

---

**¡Adelante Sarah! Esta es tu versión profesional. 🚀**

Cualquier problema, escribime los errores exactos.

