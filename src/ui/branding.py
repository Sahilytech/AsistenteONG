"""
Configuración de branding y estilos personalizados
Sarah Lee Olivera - Desarrolladora del proyecto
"""

# Colores personalizados
BRAND_COLORS = {
    "primary": "#0e98d6",      # Azul principal
    "white": "#FFFFFF",
    "black": "#000000",
    "gray_light": "#F5F5F5",
    "gray_dark": "#1a1a1a",
}

# Biografía de la creadora
AUTHOR_BIO = {
    "name": "Sarah Lee Olivera",
    "title": "Desarrolladora & Creadora del Proyecto",
    "email": "sarahleeoliveraok@gmail.com",
    "bio": """Soy una estudiante y desarrolladora de software de Argentina apasionada por crear tecnología con impacto social.

Creo que la inteligencia artificial debe ser una herramienta para asistir a las personas, proteger su privacidad y facilitar el trabajo de quienes ayudan a otros.

Este proyecto es una solución que funciona incluso sin conexión a Internet, pensada para que organizaciones sociales, fundaciones y equipos de asistencia puedan responder con mayor rapidez sin comprometer la confidencialidad.

Mi interés se centra en:
• Desarrollo de aplicaciones
• Inteligencia artificial local (offline)
• Accesibilidad
• Herramientas para contextos con recursos limitados

Este software es código abierto orientado al bien común. Apoya el trabajo de profesionales y voluntarios, nunca reemplaza su criterio ni la atención humana."""
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
