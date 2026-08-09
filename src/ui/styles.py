"""
Estilos - Colores y fuentes para luz y oscuridad
"""

# Colores para TEMA OSCURO
COLORS_DARK = {
    "background": "#0d0d0d",
    "surface": "#161b22",
    "primary": "#0e98d6",
    "text": "#FFFFFF",
    "text_muted": "#888888",
    "border": "#333333",
    "success": "#22c55e",
    "warning": "#f59e0b",
    "danger": "#ef4444",
}

# Colores para TEMA CLARO
COLORS_LIGHT = {
    "background": "#f5f5f5",
    "surface": "#ffffff",
    "primary": "#0e98d6",
    "text": "#000000",
    "text_muted": "#666666",
    "border": "#dddddd",
    "success": "#16a34a",
    "warning": "#d97706",
    "danger": "#dc2626",
}

# Por defecto, oscuro
COLORS = COLORS_DARK

def switch_theme(theme: str):
    """Cambia el tema global."""
    global COLORS
    if theme == "light":
        COLORS = COLORS_LIGHT
    else:
        COLORS = COLORS_DARK

FONTS = {
    "title": ("Helvetica", 18, "bold"),
    "heading": ("Helvetica", 14, "bold"),
    "body": ("Helvetica", 11),
    "small": ("Helvetica", 9),
}

SPACING = {
    "xs": 5,
    "sm": 10,
    "md": 15,
    "lg": 20,
    "xl": 30,
}
