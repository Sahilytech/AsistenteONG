"""
Panel de resultados y análisis con filtros
"""

import customtkinter as ctk
from typing import Optional, Dict, List
import logging

from .styles import COLORS, FONTS, SPACING, get_urgency_color

logger = logging.getLogger(__name__)

URGENCY_LEVELS = ["Todas", "Muy Alta", "Alta", "Media", "Baja"]
CASE_TYPES = ["Todos", "violencia_doméstica", "violencia_sexual", "asesoría_legal", "otro"]
CASE_STATES = ["Todos", "nuevo", "en_progreso", "resuelto", "cerrado"]


class ResultsFrame(ctk.CTkFrame):
    """Panel para mostrar resultados de análisis con filtros."""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.current_case = None
        self.all_cases = []
        self._setup_ui()
    
    def _setup_ui(self):
        """Configura la interfaz."""
        
        # Título
        title = ctk.CTkLabel(
            self,
            text="📊 Análisis",
            font=FONTS["heading"],
            text_color=COLORS["text"]
        )
        title.pack(anchor="w", pady=(0, SPACING["md"]), padx=SPACING["md"])
        
        # === PANEL DE FILTROS ===
        filter_frame = ctk.CTkFrame(self, fg_color=COLORS["surface"])
        filter_frame.pack(fill="x", padx=SPACING["md"], pady=(0, SPACING["sm"]))
        
        # Urgencia
        ctk.CTkLabel(filter_frame, text="🚨 Urgencia:", text_color=COLORS["text"]).pack(side="left", padx=5, pady=8)
        self.urgency_var = ctk.StringVar(value="Todas")
        urgency_combo = ctk.CTkComboBox(
            filter_frame,
            values=URGENCY_LEVELS,
            variable=self.urgency_var,
            command=self._apply_filters,
            fg_color=COLORS["border"],
            text_color=COLORS["text"],
            width=100
        )
        urgency_combo.pack(side="left", padx=5, pady=8)
        
        # Tipo
        ctk.CTkLabel(filter_frame, text="📂 Tipo:", text_color=COLORS["text"]).pack(side="left", padx=5, pady=8)
        self.type_var = ctk.StringVar(value="Todos")
        type_combo = ctk.CTkComboBox(
            filter_frame,
            values=CASE_TYPES,
            variable=self.type_var,
            command=self._apply_filters,
            fg_color=COLORS["border"],
            text_color=COLORS["text"],
            width=120
        )
        type_combo.pack(side="left", padx=5, pady=8)
        
        # Estado
        ctk.CTkLabel(filter_frame, text="✓ Estado:", text_color=COLORS["text"]).pack(side="left", padx=5, pady=8)
        self.state_var = ctk.StringVar(value="Todos")
        state_combo = ctk.CTkComboBox(
            filter_frame,
            values=CASE_STATES,
            variable=self.state_var,
            command=self._apply_filters,
            fg_color=COLORS["border"],
            text_color=COLORS["text"],
            width=100
        )
        state_combo.pack(side="left", padx=5, pady=8)
        
        # Limpiar filtros
        clear_btn = ctk.CTkButton(
            filter_frame,
            text="🔄 Limpiar",
            command=self._clear_filters,
            fg_color=COLORS["muted"],
            text_color="white",
            width=80
        )
        clear_btn.pack(side="right", padx=5, pady=8)
        
        # === ÁREA DE SCROLL PARA CONTENIDO ===
        scroll_frame = ctk.CTkScrollableFrame(
            self,
            fg_color=COLORS["surface"],
            label_text="Resultados"
        )
        scroll_frame.pack(fill="both", expand=True, padx=SPACING["md"], pady=SPACING["sm"])
        
        self.scroll_frame = scroll_frame
        
        # Placeholder inicial
        self._show_placeholder()
    
    def _show_placeholder(self):
        """Muestra placeholder cuando no hay análisis."""
        placeholder = ctk.CTkLabel(
            self.scroll_frame,
            text="📝 Ingresa un caso en el panel izquierdo\npara ver el análisis aquí",
            text_color=COLORS["text_muted"],
            font=FONTS["small"]
        )
        placeholder.pack(pady=SPACING["lg"])
        self.placeholder = placeholder
    
    def show_analysis(self, analysis: Dict):
        """Muestra un análisis."""
        # Limpiar
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        
        self.current_case = analysis
        self.all_cases = [analysis]  # Reset a un solo caso
        
        # Mostrar análisis
        self._display_case(analysis)
    
    def _display_case(self, case: Dict):
        """Muestra detalles de un caso."""
        
        # Urgencia
        urgency = case.get("urgency", "Desconocida")
        urgency_color = get_urgency_color(urgency)
        
        urgency_frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        urgency_frame.pack(fill="x", pady=SPACING["sm"])
        
        ctk.CTkLabel(
            urgency_frame,
            text="🚨 Urgencia:",
            font=FONTS["normal"],
            text_color=COLORS["text"]
        ).pack(side="left")
        
        urgency_label = ctk.CTkLabel(
            urgency_frame,
            text=urgency,
            font=FONTS["normal"],
            text_color=urgency_color
        )
        urgency_label.pack(side="left", padx=SPACING["sm"])
        
        # Tipo de caso
        if "case_type" in case:
            type_label = ctk.CTkLabel(
                self.scroll_frame,
                text=f"📂 Tipo: {case['case_type'].replace('_', ' ').title()}",
                font=FONTS["normal"],
                text_color=COLORS["text"]
            )
            type_label.pack(anchor="w", pady=SPACING["sm"])
        
        # Número de caso
        if "case_number" in case:
            num_label = ctk.CTkLabel(
                self.scroll_frame,
                text=f"🔢 Caso: {case['case_number']}",
                font=FONTS["small"],
                text_color=COLORS["text_muted"]
            )
            num_label.pack(anchor="w", pady=(0, SPACING["md"]))
        
        # Resumen
        if "summary" in case:
            summary_label = ctk.CTkLabel(
                self.scroll_frame,
                text="📝 Resumen:",
                font=FONTS["normal"],
                text_color=COLORS["text"]
            )
            summary_label.pack(anchor="w", pady=(SPACING["md"], SPACING["sm"]))
            
            summary_text = ctk.CTkLabel(
                self.scroll_frame,
                text=case["summary"],
                font=FONTS["small"],
                text_color=COLORS["text_muted"],
                wraplength=400,
                justify="left"
            )
            summary_text.pack(anchor="w", padx=SPACING["sm"])
        
        # Factores de riesgo
        if "risk_factors" in case and case["risk_factors"]:
            risk_label = ctk.CTkLabel(
                self.scroll_frame,
                text="⚠️ Factores de riesgo:",
                font=FONTS["normal"],
                text_color=COLORS["danger"]
            )
            risk_label.pack(anchor="w", pady=(SPACING["md"], SPACING["sm"]))
            
            for risk in case["risk_factors"]:
                risk_text = ctk.CTkLabel(
                    self.scroll_frame,
                    text=f"• {risk}",
                    font=FONTS["small"],
                    text_color=COLORS["text_muted"]
                )
                risk_text.pack(anchor="w", padx=SPACING["sm"])
        
        # Score de confianza
        if "confidence" in case:
            score = case["confidence"]
            score_emoji = "✅" if score > 0.8 else "⚠️"
            score_text = f"{score_emoji} Confianza: {score:.0%}"
            ctk.CTkLabel(
                self.scroll_frame,
                text=score_text,
                font=FONTS["small"],
                text_color=COLORS["text_muted"]
            ).pack(anchor="w", pady=(SPACING["md"], 0))
    
    def _apply_filters(self, choice=None):
        """Aplica filtros (future: para múltiples casos)."""
        logger.info("Filtros aplicados")
        # Por ahora solo un caso, pero la estructura está lista
    
    def _clear_filters(self):
        """Limpia los filtros."""
        self.urgency_var.set("Todas")
        self.type_var.set("Todos")
        self.state_var.set("Todos")
        self._apply_filters()
    
    def clear(self):
        """Limpia los resultados."""
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        self._show_placeholder()
        self.current_case = None
