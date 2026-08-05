"""
Panel de resultados y análisis
"""

import customtkinter as ctk
from typing import Optional, Dict
import logging

from .styles import COLORS, FONTS, SPACING, get_urgency_color

logger = logging.getLogger(__name__)


class ResultsFrame(ctk.CTkFrame):
    """Panel para mostrar resultados de análisis."""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.current_case = None
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
        
        # Área de scroll para contenido
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
            text="Ingresa un caso para ver el análisis aquí",
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
        
        # Urgencia
        urgency = analysis.get("urgency", "Desconocida")
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
        if "case_type" in analysis:
            ctk.CTkLabel(
                self.scroll_frame,
                text=f"📂 Tipo: {analysis['case_type']}",
                font=FONTS["normal"],
                text_color=COLORS["text"]
            ).pack(anchor="w", pady=SPACING["sm"])
        
        # Resumen
        if "summary" in analysis:
            summary_label = ctk.CTkLabel(
                self.scroll_frame,
                text="📝 Resumen:",
                font=FONTS["normal"],
                text_color=COLORS["text"]
            )
            summary_label.pack(anchor="w", pady=(SPACING["md"], SPACING["sm"]))
            
            summary_text = ctk.CTkLabel(
                self.scroll_frame,
                text=analysis["summary"],
                font=FONTS["small"],
                text_color=COLORS["text_muted"],
                wraplength=400,
                justify="left"
            )
            summary_text.pack(anchor="w", padx=SPACING["sm"])
        
        # Factores de riesgo
        if "risk_factors" in analysis and analysis["risk_factors"]:
            risk_label = ctk.CTkLabel(
                self.scroll_frame,
                text="⚠️ Factores de riesgo:",
                font=FONTS["normal"],
                text_color=COLORS["danger"]
            )
            risk_label.pack(anchor="w", pady=(SPACING["md"], SPACING["sm"]))
            
            for risk in analysis["risk_factors"]:
                risk_text = ctk.CTkLabel(
                    self.scroll_frame,
                    text=f"• {risk}",
                    font=FONTS["small"],
                    text_color=COLORS["text_muted"]
                )
                risk_text.pack(anchor="w", padx=SPACING["sm"])
        
        # Score de confianza
        if "confidence" in analysis:
            score = analysis["confidence"]
            score_text = f"{'✅' if score > 0.8 else '⚠️'} Confianza: {score:.0%}"
            ctk.CTkLabel(
                self.scroll_frame,
                text=score_text,
                font=FONTS["small"],
                text_color=COLORS["text_muted"]
            ).pack(anchor="w", pady=(SPACING["md"], 0))
    
    def clear(self):
        """Limpia los resultados."""
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        self._show_placeholder()
        self.current_case = None
