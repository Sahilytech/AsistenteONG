"""
Panel de resultados mejorado con análisis de urgencia
"""

import customtkinter as ctk
from typing import Optional, Dict, List
import logging
import sys
from pathlib import Path

# Agregar parent dir al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from ai.urgency_detector import detect_urgency, generate_response
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
            text="📊 Análisis de Caso",
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
            fg_color=COLORS["surface"]
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
    
    def show_analysis(self, case_number: str, case_text: str):
        """Muestra análisis completo de un caso."""
        try:
            # Limpiar
            for widget in self.scroll_frame.winfo_children():
                widget.destroy()
            
            logger.info(f"📊 Analizando caso: {case_number}")
            
            # Detectar urgencia
            urgency_data = detect_urgency(case_text)
            logger.info(f"🚨 Urgencia detectada: {urgency_data['urgency_level']} (score: {urgency_data['score']})")
            
            # Generar respuesta
            response = generate_response(urgency_data)
            
            # Crear analysis dict
            analysis = {
                "case_number": case_number,
                "case_text": case_text,
                "urgency": urgency_data["urgency_level"],
                "score": urgency_data["score"],
                "keywords_found": urgency_data["keywords_found"],
                "detected_risks": urgency_data["detected_risks"],
                "needs_immediate_action": urgency_data["needs_immediate_action"],
                "response": response,
                "case_type": "violencia_doméstica"  # TODO: Detectar tipo
            }
            
            self.current_case = analysis
            self._display_case(analysis)
            
        except Exception as e:
            logger.error(f"❌ Error en show_analysis: {e}", exc_info=True)
            error_label = ctk.CTkLabel(
                self.scroll_frame,
                text=f"❌ Error al analizar: {str(e)}",
                text_color=COLORS["danger"],
                font=FONTS["small"]
            )
            error_label.pack(pady=SPACING["lg"])
    
    def _display_case(self, case: Dict):
        """Muestra detalles de un caso."""
        
        # NÚMERO DE CASO
        num_label = ctk.CTkLabel(
            self.scroll_frame,
            text=f"📋 Caso: {case['case_number']}",
            font=FONTS["normal"],
            text_color=COLORS["text_muted"]
        )
        num_label.pack(anchor="w", pady=(0, SPACING["md"]))
        
        # === URGENCIA (DESTACADA) ===
        urgency = case.get("urgency", "Desconocida")
        urgency_color = get_urgency_color(urgency)
        score = case.get("score", 0)
        
        urgency_frame = ctk.CTkFrame(self.scroll_frame, fg_color=COLORS["border"], corner_radius=10)
        urgency_frame.pack(fill="x", pady=SPACING["sm"])
        
        urgency_label = ctk.CTkLabel(
            urgency_frame,
            text=f"🚨 URGENCIA: {urgency}",
            font=("Helvetica", 14, "bold"),
            text_color=urgency_color
        )
        urgency_label.pack(side="left", padx=SPACING["md"], pady=SPACING["sm"])
        
        score_label = ctk.CTkLabel(
            urgency_frame,
            text=f"Score: {score}/10",
            font=FONTS["small"],
            text_color=urgency_color
        )
        score_label.pack(side="right", padx=SPACING["md"], pady=SPACING["sm"])
        
        # RIESGOS DETECTADOS
        if "detected_risks" in case and case["detected_risks"]:
            risks_title = ctk.CTkLabel(
                self.scroll_frame,
                text="⚠️ Riesgos Detectados:",
                font=FONTS["normal"],
                text_color=COLORS["danger"]
            )
            risks_title.pack(anchor="w", pady=(SPACING["md"], SPACING["sm"]))
            
            for risk in case["detected_risks"]:
                risk_text = ctk.CTkLabel(
                    self.scroll_frame,
                    text=f"  {risk}",
                    font=FONTS["small"],
                    text_color=COLORS["danger"]
                )
                risk_text.pack(anchor="w", padx=SPACING["md"])
        
        # PALABRAS CLAVE ENCONTRADAS
        if "keywords_found" in case and case["keywords_found"]:
            keywords_title = ctk.CTkLabel(
                self.scroll_frame,
                text="🔍 Palabras Clave Detectadas:",
                font=FONTS["normal"],
                text_color=COLORS["text"]
            )
            keywords_title.pack(anchor="w", pady=(SPACING["md"], SPACING["sm"]))
            
            keywords_text = ", ".join(case["keywords_found"][:5])  # Primeras 5
            keywords_label = ctk.CTkLabel(
                self.scroll_frame,
                text=keywords_text,
                font=FONTS["small"],
                text_color=COLORS["text_muted"],
                wraplength=400
            )
            keywords_label.pack(anchor="w", padx=SPACING["md"])
        
        # RESPUESTA BORRADOR
        if "response" in case:
            response_title = ctk.CTkLabel(
                self.scroll_frame,
                text="📝 Respuesta Automática (Borrador):",
                font=FONTS["normal"],
                text_color=COLORS["primary"]
            )
            response_title.pack(anchor="w", pady=(SPACING["md"], SPACING["sm"]))
            
            response_box = ctk.CTkTextbox(
                self.scroll_frame,
                height=200,
                fg_color=COLORS["border"],
                text_color=COLORS["text"],
                border_color=COLORS["primary"]
            )
            response_box.pack(fill="both", padx=SPACING["md"], pady=SPACING["sm"])
            response_box.insert("1.0", case["response"])
            response_box.configure(state="disabled")  # Read-only
            
            # Botón copiar
            copy_btn = ctk.CTkButton(
                self.scroll_frame,
                text="📋 Copiar Respuesta",
                fg_color=COLORS["primary"],
                text_color="white",
                command=lambda: self._copy_to_clipboard(case["response"])
            )
            copy_btn.pack(anchor="w", padx=SPACING["md"], pady=SPACING["sm"])
    
    def _copy_to_clipboard(self, text: str):
        """Copia texto al portapapeles."""
        try:
            import subprocess
            process = subprocess.Popen(['clip'], stdin=subprocess.PIPE)
            process.communicate(text.encode('utf-8'))
            logger.info("✅ Respuesta copiada al portapapeles")
        except:
            logger.warning("No se pudo copiar al portapapeles")
    
    def _apply_filters(self, choice=None):
        """Aplica filtros."""
        logger.info("Filtros aplicados")
    
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
