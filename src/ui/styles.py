"""
Estilos y temas para la aplicación - Modo Claro y Oscuro completos
"""

# Colores base (modo oscuro por defecto)
COLORS = {
    "primary": "#0e98d6",
    "success": "#2da44e",
    "warning": "#d29922",
    "danger": "#da3633",
    "muted": "#6e7681",

    "background": "#0d0d0d",
    "surface": "#161b22",
    "border": "#30363d",

    "text": "#ffffff",
    "text_muted": "#8b949e",
}

# Colores para MODO CLARO
LIGHT_COLORS = {
    "primary": "#0e98d6",
    "success": "#2da44e",
    "warning": "#d29922",
    "danger": "#da3633",
    "muted": "#6e7681",

    "background": "#f6f8fa",
    "surface": "#ffffff",
    "border": "#d0d7de",

    "text": "#1f2328",
    "text_muted": "#656d76",
}

# Urgencia - colores (funcionan en ambos modos)
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

# Tema activo (se actualiza dinámicamente)
_current_theme = "dark"

def get_urgency_color(urgency: str) -> str:
    """Obtiene color para urgencia."""
    return URGENCY_COLORS.get(urgency, COLORS["muted"])

def get_theme_colors():
    """Retorna colores según tema activo."""
    if _current_theme == "light":
        return LIGHT_COLORS
    return COLORS

def set_theme(theme: str):
    """Cambia el tema activo."""
    global _current_theme
    _current_theme = theme

def get_current_theme():
    """Retorna tema actual."""
    return _current_theme
