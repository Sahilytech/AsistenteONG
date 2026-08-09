"""Sistema visual de Asistente ONG: claro, limpio y centrado en accesibilidad."""

COLORS = {
    "background": "#FFFFFF", "surface": "#FFFFFF", "surface_alt": "#F7FBFD",
    "primary": "#0e98d6", "primary_dark": "#0879ad", "primary_soft": "#EAF6FC",
    "text": "#111111", "text_muted": "#66717A", "border": "#DCE5EA",
    "success": "#168A4A", "warning": "#B86A00", "danger": "#C62828",
}

FONTS = {
    "display": ("Helvetica", 25, "bold"), "title": ("Helvetica", 20, "bold"),
    "heading": ("Helvetica", 14, "bold"), "subheading": ("Helvetica", 12, "bold"),
    "body": ("Helvetica", 11), "small": ("Helvetica", 9), "tiny": ("Helvetica", 8),
}

SPACING = {"xs": 5, "sm": 10, "md": 15, "lg": 20, "xl": 30}

CARD_RADIUS = 12


def switch_theme(theme: str):
    """Compatibilidad: el producto utiliza exclusivamente modo claro."""
    return COLORS
