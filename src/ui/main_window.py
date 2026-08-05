"""
Ventana principal de la aplicación
Interfaz con CustomTkinter
"""

import customtkinter as ctk
import logging
from typing import Optional

from .case_input import CaseInputFrame
from .results_panel import ResultsFrame
from .styles import COLORS, FONTS, SPACING

logger = logging.getLogger(__name__)

# Configurar tema global
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class MainWindow:
    """Ventana principal de la aplicación."""
    
    def __init__(self):
        """Inicializa la ventana principal."""
        self.root = ctk.CTk()
        self.root.title("Asistente ONG - Triaje y Canalización")
        self.root.geometry("1400x800")
        
        # Configurar grid
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        logger.info("Ventana principal inicializada")
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Configura la interfaz de usuario."""
        
        # Frame principal
        main_frame = ctk.CTkFrame(
            self.root,
            fg_color=COLORS["background"]
        )
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=0)
        main_frame.grid_columnconfigure(1, weight=1)
        
        # --- SIDEBAR IZQUIERDO ---
        sidebar = ctk.CTkFrame(
            main_frame,
            fg_color=COLORS["surface"],
            width=400
        )
        sidebar.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        sidebar.grid_rowconfigure(1, weight=1)
        
        # Header del sidebar
        header = ctk.CTkLabel(
            sidebar,
            text="🆘 Asistente ONG",
            font=FONTS["heading"],
            text_color=COLORS["primary"]
        )
        header.pack(pady=SPACING["lg"], padx=SPACING["md"])
        
        # Panel de entrada
        self.case_input = CaseInputFrame(
            sidebar,
            on_submit=self._on_case_submit,
            fg_color=COLORS["surface"]
        )
        self.case_input.pack(fill="both", expand=True, padx=0, pady=0)
        
        # Footer del sidebar
        footer_frame = ctk.CTkFrame(sidebar, fg_color=COLORS["border"])
        footer_frame.pack(fill="x", side="bottom")
        
        version = ctk.CTkLabel(
            footer_frame,
            text="v0.3.0 - Beta",
            font=FONTS["small"],
            text_color=COLORS["text_muted"]
        )
        version.pack(pady=SPACING["sm"])
        
        # --- PANEL DERECHO ---
        right_panel = ctk.CTkFrame(
            main_frame,
            fg_color=COLORS["background"]
        )
        right_panel.grid(row=0, column=1, sticky="nsew", padx=SPACING["md"], pady=SPACING["md"])
        right_panel.grid_rowconfigure(0, weight=1)
        right_panel.grid_columnconfigure(0, weight=1)
        
        # Panel de resultados
        self.results = ResultsFrame(
            right_panel,
            fg_color=COLORS["surface"]
        )
        self.results.grid(row=0, column=0, sticky="nsew")
        
        logger.info("UI completamente configurada")
    
    def _on_case_submit(self, case_number: str, case_text: str):
        """Maneja la sumisión de un caso."""
        logger.info(f"Caso recibido: {case_number}")
        
        # Simulación de análisis (será reemplazado por IA real)
        analysis = {
            "case_number": case_number,
            "urgency": "Alta",
            "case_type": "violencia_doméstica",
            "summary": f"Caso {case_number} ingresado el análisis será procesado por el motor IA.",
            "risk_factors": ["violencia física", "riesgo inmediato"],
            "confidence": 0.87
        }
        
        self.results.show_analysis(analysis)
    
    def run(self):
        """Inicia la aplicación."""
        logger.info("Iniciando UI...")
        self.root.mainloop()
    
    def close(self):
        """Cierra la aplicación."""
        self.root.quit()


if __name__ == "__main__":
    app = MainWindow()
    app.run()
