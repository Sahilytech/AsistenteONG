"""Estilos de la interfaz: modo claro único."""

COLORS = {
    "background": "#FFFFFF",
    "surface": "#FFFFFF",
    "primary": "#0e98d6",
    "text": "#000000",
    "text_muted": "#666666",
    "border": "#D9D9D9",
    "success": "#16a34a",
    "warning": "#d97706",
    "danger": "#dc2626",
}

FONTS = {
    "title": ("Helvetica", 18, "bold"),
    "heading": ("Helvetica", 14, "bold"),
    "body": ("Helvetica", 11),
    "small": ("Helvetica", 9),
}

SPACING = {"xs": 5, "sm": 10, "md": 15, "lg": 20, "xl": 30}


def switch_theme(theme: str):
    """Compatibilidad con módulos antiguos; la aplicación permanece en modo claro."""
    return COLORS
