# Interfaz de Usuario (v0.3)

## Visión general

Interfaz moderna con CustomTkinter en tema oscuro, optimizada para operadores de ONGs con conexión lenta o sin experiencia técnica.

## Estructura

### Layout principal

```
┌─────────────────────────────────────────────────────────┐
│  SIDEBAR (400px)      │  CONTENIDO PRINCIPAL            │
├─────────────────────────────────────────────────────────┤
│                       │                                 │
│  • Formulario entrada │  Panel de resultados            │
│  • Número caso        │  • Urgencia                     │
│  • Área texto         │  • Tipo de caso                 │
│  • Botones Analizar   │  • Resumen                      │
│    / Limpiar          │  • Factores de riesgo           │
│                       │  • Confianza                    │
│                       │                                 │
│                       │                                 │
│                       │                                 │
│  v0.3.0 - Beta        │                                 │
└─────────────────────────────────────────────────────────┘
```

## Componentes

### CaseInputFrame
Panel de entrada de nuevos casos.

**Campos:**
- `case_number` - Identificador del caso
- `text_input` - Área de texto con descripción

**Acciones:**
- `✅ Analizar caso` - Envía para análisis
- `🗑️ Limpiar` - Limpia el formulario

### ResultsFrame
Panel de resultados del análisis.

**Muestra:**
- 🚨 Nivel de urgencia (color dinámico)
- 📂 Tipo de caso
- 📝 Resumen
- ⚠️ Factores de riesgo
- ✅/⚠️ Confianza del análisis

## Temas y Estilos

### Colores

```python
COLORS = {
    "primary": "#1f6feb",      # Azul principal
    "success": "#2da44e",      # Verde
    "warning": "#d29922",      # Naranja
    "danger": "#da3633",       # Rojo
    
    "background": "#0d1117",   # Fondo
    "surface": "#161b22",      # Superficies
    "border": "#30363d",       # Bordes
    
    "text": "#c9d1d9",         # Texto
    "text_muted": "#8b949e",   # Texto secundario
}
```

### Urgencia - Colores

| Urgencia | Color | Significado |
|----------|-------|-------------|
| Muy Alta | 🔴 Rojo | Riesgo inmediato |
| Alta | 🟠 Naranja | Requiere atención pronta |
| Media | 🟣 Índigo | Requiere seguimiento |
| Baja | ⚫ Gris | Consulta rutinaria |

## Fuentes

- **Título**: Helvetica 18 bold
- **Heading**: Helvetica 14 bold
- **Normal**: Helvetica 12
- **Small**: Helvetica 10
- **Mono**: Courier New 10

## Espaciado

- xs: 4px
- sm: 8px
- md: 16px
- lg: 24px
- xl: 32px

## Flujo de usuario

1. Operador abre aplicación
2. Ingresa número de caso
3. Copia/pega texto del caso
4. Hace clic en "Analizar caso"
5. Sistema muestra análisis en panel derecho
6. Operador revisa y edita respuesta
7. Guarda caso en base de datos

## Accesibilidad

- ✅ Alto contraste (fondo oscuro/texto claro)
- ✅ Iconos + texto (no solo iconos)
- ✅ Teclas de atajo (Ctrl+Enter para enviar)
- ✅ Tamaño de fuente configurable

## Mejoras futuras (v0.4+)

- [ ] Navegación por tabs
- [ ] Historial de casos
- [ ] Editor de respuestas draft
- [ ] Vista de recursos cercanos
- [ ] Estadísticas en dashboard
- [ ] Exportar a PDF
- [ ] Tema light/dark toggle
- [ ] Idiomas múltiples

---

**v0.3 Status:** ✅ UI completamente funcional
