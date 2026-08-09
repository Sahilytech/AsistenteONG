"""
Panel de recursos - Búsqueda y contactos
"""

import customtkinter as ctk
from .styles import COLORS, FONTS
from ..resources_data import RESOURCES_DATABASE, get_emergency_numbers
import logging

logger = logging.getLogger(__name__)


class ResourcesPanel(ctk.CTkFrame):
    """Panel de recursos."""
    
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
            text="📞 Recursos de Ayuda",
            font=FONTS["heading"],
            text_color=COLORS["primary"]
        ).pack(anchor="w", pady=(0, 20))
        
        # Números de emergencia
        ctk.CTkLabel(
            scroll,
            text="🆘 Números de Emergencia (24/7)",
            font=FONTS["body"],
            text_color=COLORS["danger"]
        ).pack(anchor="w", pady=(10, 5))
        
        for item in get_emergency_numbers():
            num = item["numero"]
            tipo = item["tipo"]
            ctk.CTkLabel(
                scroll,
                text=f"{tipo}: {num}",
                font=FONTS["small"],
                text_color=COLORS["text"]
            ).pack(anchor="w", padx=20, pady=2)
        
        # Recursos por categoría
        for category, data in RESOURCES_DATABASE.items():
            if "locations" in data:
                ctk.CTkLabel(
                    scroll,
                    text=f"\n{data['name']}",
                    font=FONTS["body"],
                    text_color=COLORS["primary"]
                ).pack(anchor="w", pady=(15, 5))
                
                for location in data["locations"][:3]:  # Max 3 por categoría
                    nombre = location.get("nombre", "")
                    telefono = location.get("teléfono", "")
                    ctk.CTkLabel(
                        scroll,
                        text=f"📍 {nombre}: {telefono}",
                        font=FONTS["small"],
                        text_color=COLORS["text_muted"],
                        wraplength=350
                    ).pack(anchor="w", padx=20, pady=2)
