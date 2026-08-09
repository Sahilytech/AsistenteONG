"""
Panel de resultados - Análisis y respuestas automáticas
"""

import customtkinter as ctk
from .styles import COLORS, FONTS
import logging

logger = logging.getLogger(__name__)


class ResultsFrame(ctk.CTkFrame):
    """Panel de resultados del análisis."""
    
    def __init__(self, parent, config_manager=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.config_manager = config_manager
        self.current_case = None
        self._setup_ui()
    
    def _setup_ui(self):
        """Configura UI."""
        
        # Scroll principal
        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Título
        ctk.CTkLabel(
            scroll,
            text="📋 Análisis & Respuesta Automática",
            font=FONTS["heading"],
            text_color=COLORS["primary"]
        ).pack(anchor="w", pady=(0, 15))
        
        # Frame para resultado
        result_frame = ctk.CTkFrame(scroll, fg_color=COLORS["surface"])
        result_frame.pack(fill="both", expand=True, pady=10)
        
        self.result_text = ctk.CTkTextbox(
            result_frame,
            height=300,
            font=("Helvetica", 11),
            text_color=COLORS["text"],
            fg_color=COLORS["background"]
        )
        self.result_text.pack(fill="both", expand=True, padx=10, pady=10)
        self.result_text.insert("0.0", "Ingresa un caso para ver el análisis...")
        self.result_text.configure(state="disabled")
        
        # Botones
        button_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        button_frame.pack(fill="x", pady=10)
        
        ctk.CTkButton(
            button_frame,
            text="📋 Copiar",
            command=self._copy_text,
            fg_color=COLORS["primary"],
            text_color="white"
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            button_frame,
            text="✏️ Editar",
            command=self._edit_text,
            text_color=COLORS["text"]
        ).pack(side="left", padx=5)
    
    def show_analysis(self, case_number: str, case_text: str, analysis: dict):
        """Muestra análisis de caso."""
        try:
            self.current_case = {
                "number": case_number,
                "text": case_text,
                "analysis": analysis
            }
            
            # Construir respuesta
            urgency = analysis.get("urgency", "Baja")
            keywords = analysis.get("keywords", [])
            response = analysis.get("response", "")
            resources = analysis.get("suggested_resources", [])
            
            result_text = f"""
CASO: {case_number}
URGENCIA: {urgency}

PALABRAS CLAVE DETECTADAS:
{', '.join(keywords) if keywords else 'Ninguna'}

ANÁLISIS AUTOMÁTICO:
{response}

RECURSOS SUGERIDOS:
{', '.join(resources) if resources else 'Ninguno'}

---
Nota: Este es un borrador automático. Personaliza según el caso.
            """
            
            self.result_text.configure(state="normal")
            self.result_text.delete("0.0", "end")
            self.result_text.insert("0.0", result_text)
            self.result_text.configure(state="disabled")
            
            logger.info(f"✅ Análisis mostrado para {case_number}")
            
        except Exception as e:
            logger.error(f"❌ Error mostrando análisis: {e}")
    
    def _copy_text(self):
        """Copia texto al portapapeles."""
        try:
            self.result_text.configure(state="normal")
            text = self.result_text.get("0.0", "end")
            self.result_text.configure(state="disabled")
            
            # Copiar al portapapeles
            self.winfo_toplevel().clipboard_clear()
            self.winfo_toplevel().clipboard_append(text)
            
            logger.info("✅ Texto copiado")
        except Exception as e:
            logger.error(f"❌ Error copiando: {e}")
    
    def _edit_text(self):
        """Habilita edición."""
        try:
            current_state = self.result_text.cget("state")
            if current_state == "disabled":
                self.result_text.configure(state="normal")
                logger.info("✅ Modo edición ON")
            else:
                self.result_text.configure(state="disabled")
                logger.info("✅ Modo edición OFF")
        except Exception as e:
            logger.error(f"❌ Error editando: {e}")
