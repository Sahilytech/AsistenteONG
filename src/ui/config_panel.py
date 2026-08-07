"""
Panel de configuración avanzada - Palabras clave, plantillas, urgencia
"""

import customtkinter as ctk
import logging
from typing import Callable

from ..config_manager import UrgencyConfig, TemplateManager
from .styles import COLORS, FONTS, SPACING

logger = logging.getLogger(__name__)


class ConfigPanel(ctk.CTkFrame):
    """Panel para configurar detectores de urgencia y plantillas."""
    
    def __init__(self, parent, on_config_change: Callable = None, **kwargs):
        super().__init__(parent, **kwargs)
        self.config = UrgencyConfig()
        self.templates = TemplateManager()
        self.on_config_change = on_config_change
        self._setup_ui()
    
    def _setup_ui(self):
        """Configura panel."""
        
        # Título
        title = ctk.CTkLabel(
            self,
            text="⚙️ Configuración",
            font=FONTS["heading"],
            text_color=COLORS["primary"]
        )
        title.pack(anchor="w", pady=(0, SPACING["md"]), padx=SPACING["md"])
        
        # Scroll principal
        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=SPACING["md"], pady=SPACING["sm"])
        
        # === SECCIÓN 1: DETECTORES DE URGENCIA ===
        section_title = ctk.CTkLabel(
            scroll,
            text="🚨 Detectores de Urgencia",
            font=FONTS["normal"],
            text_color=COLORS["text"]
        )
        section_title.pack(anchor="w", pady=(SPACING["md"], SPACING["sm"]))
        
        urgency_categories = [
            ("Riesgo de Vida", self.config.risk_of_death),
            ("Violencia Severa", self.config.severe_violence),
            ("Menores Involucrados", self.config.minors_involved),
            ("Violencia Sexual", self.config.sexual_violence),
            ("Violencia Doméstica", self.config.domestic_violence),
            ("Salud Mental", self.config.mental_health),
            ("Necesidad Inmediata", self.config.immediate_need),
        ]
        
        for category_name, keywords in urgency_categories:
            self._create_keyword_frame(scroll, category_name, keywords)
        
        # === SECCIÓN 2: PLANTILLAS ===
        sep = ctk.CTkFrame(scroll, height=2, fg_color=COLORS["border"])
        sep.pack(fill="x", pady=SPACING["md"])
        
        templates_title = ctk.CTkLabel(
            scroll,
            text="📝 Plantillas de Respuesta",
            font=FONTS["normal"],
            text_color=COLORS["text"]
        )
        templates_title.pack(anchor="w", pady=(SPACING["md"], SPACING["sm"]))
        
        # Info sobre plantillas
        info = ctk.CTkLabel(
            scroll,
            text="Las plantillas se generan automáticamente según urgencia. Personaliza tu respuesta:",
            font=FONTS["small"],
            text_color=COLORS["text_muted"],
            wraplength=350,
            justify="left"
        )
        info.pack(anchor="w", pady=(0, SPACING["sm"]))
        
        # Botón: Editar plantillas
        edit_btn = ctk.CTkButton(
            scroll,
            text="✏️ Editar Plantillas",
            command=self._open_template_editor,
            fg_color=COLORS["primary"],
            text_color="white"
        )
        edit_btn.pack(fill="x", pady=SPACING["sm"])
        
        # === SECCIÓN 3: EXPORTAR/IMPORTAR ===
        sep2 = ctk.CTkFrame(scroll, height=2, fg_color=COLORS["border"])
        sep2.pack(fill="x", pady=SPACING["md"])
        
        export_title = ctk.CTkLabel(
            scroll,
            text="💾 Guardar/Cargar",
            font=FONTS["normal"],
            text_color=COLORS["text"]
        )
        export_title.pack(anchor="w", pady=(SPACING["md"], SPACING["sm"]))
        
        button_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        button_frame.pack(fill="x", pady=SPACING["sm"])
        
        export_btn = ctk.CTkButton(
            button_frame,
            text="💾 Exportar Config",
            command=self._export_config,
            fg_color=COLORS["muted"],
            text_color="white",
            width=150
        )
        export_btn.pack(side="left", padx=(0, SPACING["sm"]))
        
        import_btn = ctk.CTkButton(
            button_frame,
            text="📂 Importar Config",
            command=self._import_config,
            fg_color=COLORS["muted"],
            text_color="white",
            width=150
        )
        import_btn.pack(side="left")
    
    def _create_keyword_frame(self, parent, category: str, keywords: set):
        """Crea frame para cada categoría de palabras clave."""
        frame = ctk.CTkFrame(parent, fg_color=COLORS["surface"], corner_radius=6)
        frame.pack(fill="x", pady=SPACING["sm"])
        
        # Título categoría
        header = ctk.CTkLabel(
            frame,
            text=f"• {category}",
            font=FONTS["small"],
            text_color=COLORS["text"]
        )
        header.pack(anchor="w", padx=SPACING["sm"], pady=(SPACING["sm"], 0))
        
        # Palabras clave (primeras 5)
        keywords_text = ", ".join(list(keywords)[:5])
        if len(keywords) > 5:
            keywords_text += f"... (+{len(keywords)-5} más)"
        
        keywords_label = ctk.CTkLabel(
            frame,
            text=keywords_text,
            font=FONTS["small"],
            text_color=COLORS["text_muted"],
            wraplength=320,
            justify="left"
        )
        keywords_label.pack(anchor="w", padx=SPACING["md"], pady=(0, SPACING["sm"]))
        
        # Contador
        count_label = ctk.CTkLabel(
            frame,
            text=f"({len(keywords)} palabras clave)",
            font=FONTS["small"],
            text_color=COLORS["primary"]
        )
        count_label.pack(anchor="e", padx=SPACING["sm"], pady=(0, SPACING["sm"]))
    
    def _open_template_editor(self):
        """Abre editor de plantillas."""
        logger.info("Abriendo editor de plantillas...")
        # TODO: Implementar editor de plantillas
    
    def _export_config(self):
        """Exporta configuración a archivo."""
        logger.info("Exportando configuración...")
        # TODO: Implementar export
    
    def _import_config(self):
        """Importa configuración desde archivo."""
        logger.info("Importando configuración...")
        # TODO: Implementar import
