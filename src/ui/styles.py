"""Sistema visual unificado para Asistente ONG.

La interfaz usa pares claro/oscuro compatibles con CustomTkinter. Los componentes
consumen estas constantes para mantener jerarquía, espaciado y contraste coherentes.
"""

COLORS = {
    "background": ("#F4F8FB", "#070C11"),
    "surface": ("#FFFFFF", "#0C141B"),
    "surface_alt": ("#EAF2F6", "#101B23"),
    "surface_blue": ("#E2F4FB", "#0D2835"),
    "surface_elevated": ("#FFFFFF", "#121F28"),
    "primary": ("#0E98D6", "#43C3F2"),
    "primary_dark": ("#0878AB", "#1595C9"),
    "primary_soft": ("#D7EFF9", "#153B4B"),
    "primary_pale": ("#F0FAFE", "#0B202A"),
    "text": ("#0C1720", "#F4F9FC"),
    "text_muted": ("#5F737D", "#9AAEB8"),
    "text_soft": ("#84959E", "#718690"),
    "border": ("#D1E0E7", "#20333E"),
    "border_strong": ("#B6CBD5", "#34505D"),
    "success": ("#168A4A", "#55D19A"),
    "success_soft": ("#E5F6ED", "#102F24"),
    "warning": ("#A86100", "#F2BA63"),
    "warning_soft": ("#FFF2DC", "#382B19"),
    "danger": ("#C62828", "#FF7777"),
    "danger_soft": ("#FCE9E9", "#3B1D20"),
    "info": ("#3478B9", "#6FB6EE"),
}

FONTS = {
    "display": ("Helvetica", 30, "bold"),
    "hero": ("Helvetica", 26, "bold"),
    "title": ("Helvetica", 21, "bold"),
    "heading": ("Helvetica", 15, "bold"),
    "subheading": ("Helvetica", 12, "bold"),
    "body": ("Helvetica", 11),
    "body_bold": ("Helvetica", 11, "bold"),
    "small": ("Helvetica", 9),
    "small_bold": ("Helvetica", 9, "bold"),
    "tiny": ("Helvetica", 8),
    "metric": ("Helvetica", 25, "bold"),
}

SPACING = {"xs": 5, "sm": 9, "md": 14, "lg": 20, "xl": 28, "xxl": 36}
CARD_RADIUS = 18
BUTTON_RADIUS = 11
BUTTON_HEIGHT = 40


def switch_theme(theme: str):
    """Mantiene compatibilidad: CustomTkinter resuelve automáticamente los pares."""
    return COLORS
