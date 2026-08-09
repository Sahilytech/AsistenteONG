"""
Panel de ayuda - Tutorial e instrucciones
"""

import customtkinter as ctk
from .styles import COLORS, FONTS
import logging

logger = logging.getLogger(__name__)


class HelpPanel(ctk.CTkFrame):
    """Panel con tutorial e instrucciones."""
    
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
            text="📚 TUTORIAL Y AYUDA",
            font=FONTS["heading"],
            text_color=COLORS["primary"]
        ).pack(anchor="w", pady=(0, 20))
        
        # Secciones
        sections = [
            ("🚀 INICIO RÁPIDO (3 pasos)", [
                "1. Ingresa la DESCRIPCIÓN del caso",
                "2. El sistema genera automático el número",
                "3. Clic en '✅ Analizar caso'",
                "",
                "✨ El sistema detectará:",
                "   • Nivel de urgencia",
                "   • Palabras clave",
                "   • Respuesta borrador",
                "   • Recursos sugeridos"
            ]),
            ("📋 CÓMO USAR CADA TAB", [
                "📊 DASHBOARD: Ver estadísticas",
                "📋 ANÁLISIS: Ver respuestas automáticas",
                "📞 RECURSOS: Buscar teléfonos",
                "⚙️ CONFIG: Información del sistema",
                "❓ AYUDA: Este tutorial",
                "👩‍💻 CREADORA: Información de Sarah"
            ]),
            ("🚨 NIVELES DE URGENCIA", [
                "🔴 MUY ALTA: Emergencia (vida en riesgo)",
                "🟠 ALTA: Urgente (hoy)",
                "🟡 MEDIA: Importante (48h)",
                "⚪ BAJA: Normal (sin prisa)"
            ]),
            ("💡 TIPS IMPORTANTES", [
                "✅ El análisis es automático pero verificalo",
                "✅ Personaliza las respuestas",
                "✅ Mantén los teléfonos a mano",
                "✅ Usa como guía, no como verdad absoluta",
                "✅ Funciona 100% offline",
                "✅ Los datos quedan guardados localmente"
            ]),
        ]
        
        for title, items in sections:
            ctk.CTkLabel(
                scroll,
                text=title,
                font=FONTS["body"],
                text_color=COLORS["primary"]
            ).pack(anchor="w", pady=(15, 5))
            
            for item in items:
                ctk.CTkLabel(
                    scroll,
                    text=item,
                    font=FONTS["small"],
                    text_color=COLORS["text"],
                    justify="left",
                    wraplength=350
                ).pack(anchor="w", padx=20, pady=1)
