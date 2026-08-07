"""
Dashboard con estadísticas, historial y reportes
"""

import customtkinter as ctk
from typing import List, Dict
from datetime import datetime
import logging

from .styles import COLORS, FONTS, SPACING

logger = logging.getLogger(__name__)


class CaseStats:
    """Estadísticas de casos."""
    
    def __init__(self):
        self.total_cases = 0
        self.by_urgency = {
            "Muy Alta": 0,
            "Alta": 0,
            "Media": 0,
            "Baja": 0
        }
        self.by_category = {}
        self.cases_today = 0
        self.cases_this_week = 0
    
    def add_case(self, urgency: str, category: str):
        """Agrega un caso a las estadísticas."""
        self.total_cases += 1
        self.by_urgency[urgency] = self.by_urgency.get(urgency, 0) + 1
        self.by_category[category] = self.by_category.get(category, 0) + 1
        self.cases_today += 1
        self.cases_this_week += 1
        logger.info(f"📊 Caso agregado: {urgency} - {category}")


class DashboardFrame(ctk.CTkFrame):
    """Dashboard con métricas y estadísticas."""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.stats = CaseStats()
        self.cases_history = []
        self._setup_ui()
    
    def _setup_ui(self):
        """Configura dashboard."""
        
        # Título
        title = ctk.CTkLabel(
            self,
            text="📊 Dashboard",
            font=FONTS["heading"],
            text_color=COLORS["primary"]
        )
        title.pack(anchor="w", pady=(0, SPACING["md"]), padx=SPACING["md"])
        
        # Frame de métricas principales
        metrics_frame = ctk.CTkFrame(self, fg_color="transparent")
        metrics_frame.pack(fill="x", padx=SPACING["md"], pady=(0, SPACING["md"]))
        
        # Métrica 1: Total de casos
        self._create_metric(metrics_frame, "📋 Total", "0", 0)
        
        # Métrica 2: Muy Altas
        self._create_metric(metrics_frame, "🔴 Muy Alta", "0", 1)
        
        # Métrica 3: Hoy
        self._create_metric(metrics_frame, "📅 Hoy", "0", 2)
        
        # Métrica 4: Esta semana
        self._create_metric(metrics_frame, "📆 Semana", "0", 3)
        
        # Frame de scroll para historial
        scroll_label = ctk.CTkLabel(
            self,
            text="📜 Historial de Casos",
            font=FONTS["normal"],
            text_color=COLORS["text"]
        )
        scroll_label.pack(anchor="w", padx=SPACING["md"], pady=(SPACING["md"], SPACING["sm"]))
        
        self.history_scroll = ctk.CTkScrollableFrame(
            self,
            fg_color=COLORS["surface"]
        )
        self.history_scroll.pack(fill="both", expand=True, padx=SPACING["md"], pady=(0, SPACING["md"]))
        
        # Placeholder
        self.history_placeholder = ctk.CTkLabel(
            self.history_scroll,
            text="No hay casos registrados aún",
            text_color=COLORS["text_muted"],
            font=FONTS["small"]
        )
        self.history_placeholder.pack(pady=SPACING["lg"])
    
    def _create_metric(self, parent, label: str, value: str, column: int):
        """Crea una métrica visual."""
        metric_frame = ctk.CTkFrame(parent, fg_color=COLORS["surface"], corner_radius=8)
        metric_frame.grid(row=0, column=column, padx=SPACING["sm"], sticky="nsew", ipadx=10, ipady=10)
        parent.grid_columnconfigure(column, weight=1)
        
        label_w = ctk.CTkLabel(metric_frame, text=label, font=FONTS["small"], text_color=COLORS["text_muted"])
        label_w.pack()
        
        value_w = ctk.CTkLabel(metric_frame, text=value, font=("Helvetica", 24, "bold"), text_color=COLORS["primary"])
        value_w.pack()
        
        # Guardar referencia para actualizar
        if column == 0:
            self.metric_total = value_w
        elif column == 1:
            self.metric_muy_alta = value_w
        elif column == 2:
            self.metric_today = value_w
        elif column == 3:
            self.metric_week = value_w
    
    def update_stats(self, urgency: str, category: str, case_number: str):
        """Actualiza estadísticas con nuevo caso."""
        self.stats.add_case(urgency, category)
        
        # Actualizar métricas
        self.metric_total.configure(text=str(self.stats.total_cases))
        self.metric_muy_alta.configure(text=str(self.stats.by_urgency["Muy Alta"]))
        self.metric_today.configure(text=str(self.stats.cases_today))
        self.metric_week.configure(text=str(self.stats.cases_this_week))
        
        # Agregar al historial
        self._add_to_history(case_number, urgency, category)
    
    def _add_to_history(self, case_number: str, urgency: str, category: str):
        """Agrega caso al historial."""
        # Limpiar placeholder si es el primer caso
        if self.stats.total_cases == 1:
            self.history_placeholder.destroy()
        
        # Crear tarjeta de caso
        case_card = ctk.CTkFrame(self.history_scroll, fg_color=COLORS["border"], corner_radius=6)
        case_card.pack(fill="x", pady=SPACING["sm"])
        
        # Encabezado con número y urgencia
        header = ctk.CTkFrame(case_card, fg_color="transparent")
        header.pack(fill="x", padx=SPACING["sm"], pady=(SPACING["sm"], 0))
        
        case_label = ctk.CTkLabel(
            header,
            text=f"📋 {case_number}",
            font=FONTS["normal"],
            text_color=COLORS["text"]
        )
        case_label.pack(side="left")
        
        urgency_color = self._get_urgency_color(urgency)
        urgency_label = ctk.CTkLabel(
            header,
            text=urgency,
            font=FONTS["small"],
            text_color=urgency_color
        )
        urgency_label.pack(side="right")
        
        # Info
        time_label = ctk.CTkLabel(
            case_card,
            text=f"{category} • {datetime.now().strftime('%H:%M')}",
            font=FONTS["small"],
            text_color=COLORS["text_muted"]
        )
        time_label.pack(anchor="w", padx=SPACING["sm"], pady=(0, SPACING["sm"]))
    
    @staticmethod
    def _get_urgency_color(urgency: str) -> str:
        """Retorna color según urgencia."""
        colors = {
            "Muy Alta": COLORS["danger"],
            "Alta": COLORS["warning"],
            "Media": COLORS["primary"],
            "Baja": COLORS["muted"]
        }
        return colors.get(urgency, COLORS["muted"])
