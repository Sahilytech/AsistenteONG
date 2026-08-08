"""
Panel de resultados mejorado - Con respuestas automáticas, filtros y recursos
"""

import customtkinter as ctk
from typing import Optional, Dict, List
import logging

from ..config_manager import ConfigManager
from .styles import COLORS, FONTS, SPACING, get_urgency_color

logger = logging.getLogger(__name__)

URGENCY_LEVELS = ["Todas", "Muy Alta", "Alta", "Media", "Baja"]


class ResultsFrame(ctk.CTkFrame):
    """Panel para mostrar resultados de análisis con respuestas automáticas."""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.current_case = None
        self.all_cases = []  # Historial de casos para filtrar
        self.config_manager = ConfigManager()
        self._setup_ui()

    def _setup_ui(self):
        """Configura la interfaz."""

        # Título
        title = ctk.CTkLabel(
            self,
            text="📊 Análisis & Respuesta Automática",
            font=FONTS["heading"],
            text_color=COLORS["text"]
        )
        title.pack(anchor="w", pady=(0, SPACING["md"]), padx=SPACING["md"])

        # === PANEL DE FILTROS ===
        filter_frame = ctk.CTkFrame(self, fg_color=COLORS["surface"])
        filter_frame.pack(fill="x", padx=SPACING["md"], pady=(0, SPACING["sm"]))

        ctk.CTkLabel(filter_frame, text="🚨 Filtrar por Urgencia:", text_color=COLORS["text"]).pack(side="left", padx=5, pady=8)
        self.urgency_var = ctk.StringVar(value="Todas")
        urgency_combo = ctk.CTkComboBox(
            filter_frame,
            values=URGENCY_LEVELS,
            variable=self.urgency_var,
            command=self._on_filter_change,
            fg_color=COLORS["border"],
            text_color=COLORS["text"],
            width=120
        )
        urgency_combo.pack(side="left", padx=5, pady=8)

        clear_btn = ctk.CTkButton(
            filter_frame,
            text="🔄 Limpiar",
            command=self._clear,
            fg_color=COLORS["muted"],
            text_color="white",
            width=80
        )
        clear_btn.pack(side="right", padx=5, pady=8)

        # === ÁREA DE SCROLL PRINCIPAL ===
        self.scroll_frame = ctk.CTkScrollableFrame(
            self,
            fg_color=COLORS["surface"],
            label_text="Resultado del Análisis"
        )
        self.scroll_frame.pack(fill="both", expand=True, padx=SPACING["md"], pady=SPACING["sm"])

        # Placeholder
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
        """Realiza análisis completo del caso."""
        try:
            # Limpiar scroll
            for widget in self.scroll_frame.winfo_children():
                widget.destroy()

            # Usar ConfigManager para análisis
            analysis = self.config_manager.analyze(case_text)

            # Guardar caso
            self.current_case = {
                "case_number": case_number,
                "text": case_text,
                **analysis
            }

            # Agregar al historial
            self.all_cases.append(self.current_case)

            logger.info(f"✅ Análisis completado: {analysis['urgency']}")

            # Mostrar análisis
            self._display_analysis()

        except Exception as e:
            logger.error(f"❌ Error en análisis: {e}", exc_info=True)
            error_label = ctk.CTkLabel(
                self.scroll_frame,
                text=f"Error: {str(e)}",
                text_color=COLORS["danger"]
            )
            error_label.pack(pady=SPACING["lg"])

    def _on_filter_change(self, choice):
        """Filtra casos por nivel de urgencia."""
        self._display_analysis()

    def _display_analysis(self):
        """Muestra el análisis completo con filtro aplicado."""
        if not self.current_case:
            self._show_placeholder()
            return

        # Limpiar scroll
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        # Aplicar filtro
        filter_urgency = self.urgency_var.get()
        cases_to_show = self.all_cases

        if filter_urgency != "Todas":
            cases_to_show = [c for c in self.all_cases if c.get("urgency") == filter_urgency]

        if not cases_to_show:
            no_results = ctk.CTkLabel(
                self.scroll_frame,
                text=f"❌ No hay casos con urgencia '{filter_urgency}'",
                text_color=COLORS["text_muted"],
                font=FONTS["normal"]
            )
            no_results.pack(pady=SPACING["lg"])
            return

        # Mostrar cada caso filtrado
        for case in cases_to_show:
            self._display_single_case(case)

    def _display_single_case(self, case: Dict):
        """Muestra un caso individual."""

        # === SECCIÓN 1: INFORMACIÓN DEL CASO ===
        info_frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        info_frame.pack(fill="x", pady=SPACING["md"])

        # Número de caso
        ctk.CTkLabel(
            info_frame,
            text=f"📋 Caso: {case['case_number']}",
            font=FONTS["normal"],
            text_color=COLORS["text"]
        ).pack(anchor="w")

        # Urgencia con color
        urgency = case.get("urgency", "Desconocida")
        urgency_color = get_urgency_color(urgency)

        urgency_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        urgency_frame.pack(anchor="w", pady=SPACING["sm"])

        ctk.CTkLabel(
            urgency_frame,
            text="🚨 Urgencia:",
            font=FONTS["normal"],
            text_color=COLORS["text"]
        ).pack(side="left")

        ctk.CTkLabel(
            urgency_frame,
            text=urgency,
            font=FONTS["normal"],
            text_color=urgency_color
        ).pack(side="left", padx=SPACING["sm"])

        # Palabras clave detectadas
        if case.get("keywords"):
            keywords_frame = ctk.CTkFrame(self.scroll_frame, fg_color=COLORS["border"], corner_radius=6)
            keywords_frame.pack(fill="x", pady=SPACING["md"])

            ctk.CTkLabel(
                keywords_frame,
                text="🔑 Palabras Clave Detectadas:",
                font=FONTS["small"],
                text_color=COLORS["primary"]
            ).pack(anchor="w", padx=SPACING["sm"], pady=(SPACING["sm"], 0))

            keywords_text = " • ".join(case["keywords"])
            ctk.CTkLabel(
                keywords_frame,
                text=keywords_text,
                font=FONTS["small"],
                text_color=COLORS["text_muted"],
                wraplength=400,
                justify="left"
            ).pack(anchor="w", padx=SPACING["md"], pady=(0, SPACING["sm"]))

        # === SECCIÓN 2: RESPUESTA AUTOMÁTICA BORRADOR ===
        if case.get("template"):
            response_frame = ctk.CTkFrame(self.scroll_frame, fg_color=COLORS["border"], corner_radius=6)
            response_frame.pack(fill="both", expand=True, pady=SPACING["md"])

            ctk.CTkLabel(
                response_frame,
                text="📨 Borrador de Respuesta Automática",
                font=FONTS["normal"],
                text_color=COLORS["primary"]
            ).pack(anchor="w", padx=SPACING["sm"], pady=(SPACING["sm"], 0))

            # Área de texto con respuesta
            response_text = ctk.CTkTextbox(
                response_frame,
                height=150,
                fg_color=COLORS["surface"],
                text_color=COLORS["text"],
                border_color=COLORS["border"]
            )
            response_text.pack(fill="both", expand=True, padx=SPACING["sm"], pady=SPACING["sm"])
            response_text.insert("1.0", case["template"])
            response_text.configure(state="disabled")

            # Botones de acción
            action_frame = ctk.CTkFrame(response_frame, fg_color="transparent")
            action_frame.pack(fill="x", padx=SPACING["sm"], pady=(0, SPACING["sm"]))

            copy_btn = ctk.CTkButton(
                action_frame,
                text="📋 Copiar",
                command=lambda: self._copy_response(case["template"]),
                fg_color=COLORS["primary"],
                text_color="white",
                width=100
            )
            copy_btn.pack(side="left", padx=(0, SPACING["sm"]))

            edit_btn = ctk.CTkButton(
                action_frame,
                text="✏️ Editar",
                command=lambda: self._edit_response(response_text),
                fg_color=COLORS["muted"],
                text_color="white",
                width=100
            )
            edit_btn.pack(side="left")

        # === SECCIÓN 3: RECURSOS SUGERIDOS ===
        if case.get("resources"):
            resources_frame = ctk.CTkFrame(self.scroll_frame, fg_color=COLORS["border"], corner_radius=6)
            resources_frame.pack(fill="x", pady=SPACING["md"])

            ctk.CTkLabel(
                resources_frame,
                text="📞 Recursos Sugeridos",
                font=FONTS["normal"],
                text_color=COLORS["primary"]
            ).pack(anchor="w", padx=SPACING["sm"], pady=(SPACING["sm"], 0))

            for resource in case["resources"]:
                resource_label = ctk.CTkLabel(
                    resources_frame,
                    text=f"• {resource}",
                    font=FONTS["small"],
                    text_color=COLORS["text_muted"]
                )
                resource_label.pack(anchor="w", padx=SPACING["md"])

            # Botón: Ver detalles de recursos
            details_btn = ctk.CTkButton(
                resources_frame,
                text="🔍 Ver detalles en panel de Recursos",
                command=self._open_resources,
                fg_color=COLORS["primary"],
                text_color="white",
                width=200
            )
            details_btn.pack(pady=SPACING["sm"])

        # Separador entre casos
        ctk.CTkFrame(self.scroll_frame, height=2, fg_color=COLORS["border"]).pack(fill="x", pady=SPACING["md"])

    def _copy_response(self, text: str):
        """Copia respuesta al portapapeles."""
        try:
            import subprocess
            process = subprocess.Popen(['clip'], stdin=subprocess.PIPE)
            process.communicate(text.encode('utf-8'))
            logger.info("✅ Respuesta copiada")
        except:
            logger.warning("No se pudo copiar")

    def _edit_response(self, text_widget):
        """Habilita edición de respuesta."""
        if text_widget.cget("state") == "disabled":
            text_widget.configure(state="normal")
            logger.info("✏️ Modo edición activado")
        else:
            text_widget.configure(state="disabled")
            logger.info("✅ Cambios guardados")

    def _open_resources(self):
        """Abre panel de recursos."""
        logger.info("Abriendo panel de recursos...")
        # TODO: Implementar navegación a recursos

    def _clear(self):
        """Limpia el análisis."""
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        self._show_placeholder()
        self.current_case = None
        self.all_cases = []
        logger.info("🗑️ Análisis limpiado")
