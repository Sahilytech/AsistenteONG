"""
Dashboard - Estadísticas y métricas
"""

import customtkinter as ctk
from .styles import COLORS, FONTS
import logging

logger = logging.getLogger(__name__)


class DashboardFrame(ctk.CTkFrame):
    """Panel de dashboard con estadísticas."""
    
    def __init__(self, parent, case_manager=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.case_manager = case_manager
        self.stats = {"total": 0, "por_urgencia": {}, "por_status": {}}
        self._setup_ui()
    
    def _setup_ui(self):
        """Configura UI."""
        
        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Título
        ctk.CTkLabel(
            scroll,
            text="📊 Dashboard",
            font=FONTS["heading"],
            text_color=COLORS["primary"]
        ).pack(anchor="w", pady=(0, 20))
        
        # Total de casos
        ctk.CTkLabel(
            scroll,
            text=f"Total de Casos: {self.stats['total']}",
            font=FONTS["heading"],
            text_color=COLORS["success"]
        ).pack(anchor="w", pady=10)
        
        # Por urgencia
        ctk.CTkLabel(
            scroll,
            text="Por Urgencia:",
            font=FONTS["body"],
            text_color=COLORS["text"]
        ).pack(anchor="w", pady=(10, 5))
        
        urgencies = self.stats.get("por_urgencia", {})
        for urgency, count in urgencies.items():
            ctk.CTkLabel(
                scroll,
                text=f"  {urgency}: {count}",
                font=FONTS["small"],
                text_color=COLORS["text_muted"]
            ).pack(anchor="w", padx=20, pady=2)
        
        # Por estado
        ctk.CTkLabel(
            scroll,
            text="Por Estado:",
            font=FONTS["body"],
            text_color=COLORS["text"]
        ).pack(anchor="w", pady=(10, 5))
        
        statuses = self.stats.get("por_status", {})
        for status, count in statuses.items():
            ctk.CTkLabel(
                scroll,
                text=f"  {status}: {count}",
                font=FONTS["small"],
                text_color=COLORS["text_muted"]
            ).pack(anchor="w", padx=20, pady=2)
    
    def update_stats(self, urgency: str, category: str, case_number: str):
        """Actualiza estadísticas."""
        try:
            if self.case_manager:
                self.stats = self.case_manager.get_statistics()
            
            logger.info(f"✅ Estadísticas actualizadas")
        except Exception as e:
            logger.error(f"❌ Error: {e}")
