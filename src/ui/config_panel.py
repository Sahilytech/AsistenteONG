"""
Panel de configuración
"""

import customtkinter as ctk
from .styles import COLORS, FONTS
import logging

logger = logging.getLogger(__name__)


class ConfigPanel(ctk.CTkFrame):
    """Panel de configuración."""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self._setup_ui()
    
    def _setup_ui(self):
        """Configura UI."""
        
        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Título
        ctk.CTkLabel(
            scroll,
            text="⚙️ Configuración",
            font=FONTS["heading"],
            text_color=COLORS["primary"]
        ).pack(anchor="w", pady=(0, 20))
        
        # Información
        info = """
SISTEMA COMPLETAMENTE OFFLINE
✅ Funciona sin internet
✅ Datos guardados localmente
✅ Privacidad garantizada

PALABRAS CLAVE
+320 palabras clave en 9 categorías:
• Riesgo de vida
• Violencia severa
• Menores
• Violencia sexual
• Violencia doméstica
• Salud mental
• Necesidad inmediata
• Asesoría legal
• Recursos

RECURSOS
+150 teléfonos y locaciones:
• Líneas de crisis
• Refugios
• Hospitales
• Abogados
• Psicólogos
• Instituciones públicas

LICENCIA
Social Ética 2026
❌ No se puede vender
❌ No se puede adulterar
✅ Código abierto
✅ Bien común
        """
        
        ctk.CTkLabel(
            scroll,
            text=info,
            font=FONTS["small"],
            justify="left",
            text_color=COLORS["text"],
            wraplength=400
        ).pack(anchor="w", pady=10)
