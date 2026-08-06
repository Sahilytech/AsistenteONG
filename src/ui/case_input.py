"""
Panel de entrada de casos
"""

import customtkinter as ctk
from typing import Callable
import logging

from .styles import COLORS, FONTS, SPACING

logger = logging.getLogger(__name__)


class CaseInputFrame(ctk.CTkFrame):
    """Panel para ingresar nuevos casos."""
    
    def __init__(self, parent, on_submit: Callable, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.on_submit = on_submit
        logger.info(f"✅ CaseInputFrame inicializado con callback: {on_submit}")
        self._setup_ui()
    
    def _setup_ui(self):
        """Configura la interfaz."""
        
        # Título
        title = ctk.CTkLabel(
            self,
            text="📝 Nuevo Caso",
            font=FONTS["heading"],
            text_color=COLORS["text"]
        )
        title.pack(anchor="w", pady=(0, SPACING["md"]), padx=SPACING["md"])
        
        # Campo de nombre de caso
        ctk.CTkLabel(self, text="Número de caso:").pack(anchor="w", padx=SPACING["md"])
        self.case_number = ctk.CTkEntry(
            self,
            placeholder_text="CASE-2025-001",
            fg_color=COLORS["surface"],
            text_color=COLORS["text"],
            border_color=COLORS["border"]
        )
        self.case_number.pack(fill="x", padx=SPACING["md"], pady=(0, SPACING["sm"]))
        
        # Área de texto principal
        ctk.CTkLabel(
            self, 
            text="Descripción del caso:",
            text_color=COLORS["text"]
        ).pack(anchor="w", padx=SPACING["md"], pady=(SPACING["md"], 0))
        
        self.text_input = ctk.CTkTextbox(
            self,
            height=150,
            fg_color=COLORS["surface"],
            text_color=COLORS["text"],
            border_color=COLORS["border"]
        )
        self.text_input.pack(fill="both", expand=True, padx=SPACING["md"], pady=SPACING["sm"])
        
        # Frame de botones
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(fill="x", padx=SPACING["md"], pady=SPACING["md"])
        
        # Botón Enviar
        submit_btn = ctk.CTkButton(
            button_frame,
            text="✅ Analizar caso",
            command=self._on_submit,
            fg_color=COLORS["primary"],
            text_color="white",
            hover_color="#2472ca"
        )
        submit_btn.pack(side="left", padx=(0, SPACING["sm"]))
        
        # Botón Limpiar
        clear_btn = ctk.CTkButton(
            button_frame,
            text="🗑️ Limpiar",
            command=self._on_clear,
            fg_color=COLORS["muted"],
            text_color="white",
            hover_color=COLORS["border"]
        )
        clear_btn.pack(side="left")
    
    def _on_submit(self):
        """Maneja el envío del formulario."""
        try:
            case_number = self.case_number.get().strip()
            case_text = self.text_input.get("1.0", "end").strip()
            
            logger.info(f"📋 Botón enviado: {case_number}")
            
            if not case_number:
                logger.warning("Número de caso vacío")
                self._show_error("Ingresa un número de caso")
                return
            
            if not case_text:
                logger.warning("Texto de caso vacío")
                self._show_error("Ingresa la descripción del caso")
                return
            
            logger.info(f"✅ Llamando callback con: {case_number}, {len(case_text)} chars")
            
            # LLAMAR AL CALLBACK
            if self.on_submit:
                self.on_submit(case_number, case_text)
            else:
                logger.error("❌ on_submit es None!")
                
        except Exception as e:
            logger.error(f"❌ Error en _on_submit: {e}", exc_info=True)
            self._show_error(f"Error: {str(e)}")
    
    def _on_clear(self):
        """Limpia el formulario."""
        self.case_number.delete(0, "end")
        self.text_input.delete("1.0", "end")
        logger.info("🗑️ Formulario limpiado")
    
    def _show_error(self, message: str):
        """Muestra un error."""
        logger.error(f"⚠️ {message}")
        # TODO: Mostrar popup de error
    
    def get_input(self) -> dict:
        """Obtiene los datos del formulario."""
        return {
            "case_number": self.case_number.get(),
            "text": self.text_input.get("1.0", "end")
        }
    
    def clear(self):
        """Limpia el formulario."""
        self._on_clear()
