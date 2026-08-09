"""
Panel de ingreso de casos
"""

import customtkinter as ctk
from .styles import COLORS, FONTS
import logging

logger = logging.getLogger(__name__)


class CaseInputFrame(ctk.CTkFrame):
    """Panel para ingresar casos."""
    
    def __init__(self, parent, on_submit=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.on_submit = on_submit
        self.case_counter = 0
        self._setup_ui()
    
    def _setup_ui(self):
        """Configura UI."""
        
        # Título
        ctk.CTkLabel(
            self,
            text="📝 Nuevo Caso",
            font=FONTS["heading"],
            text_color=COLORS["primary"]
        ).pack(anchor="w", padx=15, pady=(15, 10))
        
        # Número de caso (auto-generado)
        ctk.CTkLabel(
            self,
            text="Número de caso:",
            font=FONTS["body"],
            text_color=COLORS["text"]
        ).pack(anchor="w", padx=15, pady=(0, 5))
        
        self.case_number_entry = ctk.CTkEntry(
            self,
            placeholder_text="Auto-generado",
            state="readonly",
            fg_color=COLORS["surface"],
            text_color=COLORS["text"]
        )
        self.case_number_entry.pack(fill="x", padx=15, pady=(0, 15))
        
        # Descripción
        ctk.CTkLabel(
            self,
            text="Descripción del caso:",
            font=FONTS["body"],
            text_color=COLORS["text"]
        ).pack(anchor="w", padx=15, pady=(0, 5))
        
        self.text_input = ctk.CTkTextbox(
            self,
            height=200,
            font=("Helvetica", 10),
            fg_color=COLORS["surface"],
            text_color=COLORS["text"]
        )
        self.text_input.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        # Botones
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        ctk.CTkButton(
            button_frame,
            text="✅ Analizar caso",
            command=self._on_analyze,
            fg_color=COLORS["primary"],
            text_color="white"
        ).pack(side="left", padx=(0, 10), fill="x", expand=True)
        
        ctk.CTkButton(
            button_frame,
            text="🗑️ Limpiar",
            command=self._on_clear,
            text_color=COLORS["text"]
        ).pack(side="left", fill="x", expand=True)
    
    def _on_analyze(self):
        """Analiza el caso."""
        try:
            text = self.text_input.get("0.0", "end").strip()
            
            if not text:
                logger.warning("⚠️ Caso vacío")
                return
            
            # Generar número automático
            self.case_counter += 1
            case_num = f"CASE-202608-{self.case_counter:05d}"
            
            # Mostrar en entry
            self.case_number_entry.configure(state="normal")
            self.case_number_entry.delete(0, "end")
            self.case_number_entry.insert(0, case_num)
            self.case_number_entry.configure(state="readonly")
            
            # Llamar callback
            if self.on_submit:
                self.on_submit(case_num, text)
            
            logger.info(f"✅ Caso {case_num} enviado")
            
        except Exception as e:
            logger.error(f"❌ Error: {e}")
    
    def _on_clear(self):
        """Limpia el formulario."""
        self.text_input.delete("0.0", "end")
        logger.info("✅ Formulario limpiado")
