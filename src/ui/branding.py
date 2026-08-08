"""
Configuración de branding - Sin foto personal
"""

# Colores personalizados
BRAND_COLORS = {
    "primary": "#0e98d6",
    "white": "#FFFFFF",
    "black": "#000000",
    "gray_light": "#F5F5F5",
    "gray_dark": "#1a1a1a",
}

# Info del proyecto (NO foto personal)
PROJECT_INFO = {
    "name": "Asistente ONG",
    "version": "v0.9",
    "subtitle": "Triaje y Canalización Profesional",
    "description": """Herramienta offline 100% para líneas de ayuda, ONGs y organizaciones sociales.

Desarrollada con enfoque en privacidad, accesibilidad y bien común."""
}

# Tema claro
LIGHT_THEME = {
    "bg": BRAND_COLORS["white"],
    "fg": BRAND_COLORS["black"],
    "accent": BRAND_COLORS["primary"],
    "secondary": BRAND_COLORS["gray_light"],
    "text": BRAND_COLORS["black"],
    "text_muted": "#666666",
}

# Tema oscuro
DARK_THEME = {
    "bg": BRAND_COLORS["gray_dark"],
    "fg": BRAND_COLORS["white"],
    "accent": BRAND_COLORS["primary"],
    "secondary": "#2a2a2a",
    "text": BRAND_COLORS["white"],
    "text_muted": "#AAAAAA",
}
