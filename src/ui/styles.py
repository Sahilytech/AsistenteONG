"""
Estilos y temas para la aplicación
Colores personalizados: Azul #0e98d6, Blanco, Negro
"""

# Colores
COLORS = {
    "primary": "#0e98d6",      # Azul personalizado
    "success": "#2da44e",      # Verde
    "warning": "#d29922",      # Naranja
    "danger": "#da3633",       # Rojo
    "muted": "#6e7681",        # Gris
    
    "background": "#0d0d0d",   # Negro
    "surface": "#161b22",      # Superficie gris oscuro
    "border": "#30363d",       # Borde
    
    "text": "#ffffff",         # Blanco
    "text_muted": "#8b949e",   # Gris claro
}

# Urgencia - colores
URGENCY_COLORS = {
    "Muy Alta": COLORS["danger"],
    "Alta": COLORS["warning"],
    "Media": COLORS["primary"],
    "Baja": COLORS["muted"],
}

# Fuentes
FONTS = {
    "title": ("Helvetica", 18, "bold"),
    "heading": ("Helvetica", 14, "bold"),
    "normal": ("Helvetica", 12),
    "small": ("Helvetica", 10),
    "mono": ("Courier New", 10),
}

# Espaciado
SPACING = {
    "xs": 4,
    "sm": 8,
    "md": 16,
    "lg": 24,
    "xl": 32,
}


def get_urgency_color(urgency: str) -> str:
    """Obtiene color para urgencia."""
    return URGENCY_COLORS.get(urgency, COLORS["muted"])
