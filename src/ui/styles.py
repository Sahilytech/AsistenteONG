"""
Temas y estilos para la aplicación
"""

# Colores
COLORS = {
    "primary": "#1f6feb",      # Azul principal
    "success": "#2da44e",      # Verde
    "warning": "#d29922",      # Naranja/Amarillo
    "danger": "#da3633",       # Rojo
    "muted": "#6e7681",        # Gris
    
    "background": "#0d1117",   # Fondo oscuro
    "surface": "#161b22",      # Superficie
    "border": "#30363d",       # Borde
    
    "text": "#c9d1d9",         # Texto principal
    "text_muted": "#8b949e",   # Texto secundario
}

# Urgencia - colores
URGENCY_COLORS = {
    "Muy Alta": COLORS["danger"],
    "Alta": COLORS["warning"],
    "Media": "#6366f1",        # Índigo
    "Baja": COLORS["muted"],
}

# Temas
THEMES = {
    "dark": {
        "fg_color": COLORS["background"],
        "bg_color": COLORS["background"],
        "text_color": COLORS["text"],
    },
    "light": {
        "fg_color": "#ffffff",
        "bg_color": "#f6f8fa",
        "text_color": "#0d1117",
    }
}

# Fuentes
FONTS = {
    "title": ("Helvetica", 18, "bold"),
    "heading": ("Helvetica", 14, "bold"),
    "normal": ("Helvetica", 12),
    "small": ("Helvetica", 10),
    "mono": ("Courier New", 10),
}

# Padding y espacios
SPACING = {
    "xs": 4,
    "sm": 8,
    "md": 16,
    "lg": 24,
    "xl": 32,
}

def get_urgency_color(urgency: str) -> str:
    """Obtiene el color para un nivel de urgencia."""
    return URGENCY_COLORS.get(urgency, COLORS["muted"])
