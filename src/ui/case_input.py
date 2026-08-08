"""
Panel de entrada de casos - Número automático + Guardado en DB
"""

import customtkinter as ctk
from typing import Callable
import logging
from datetime import datetime

from .styles import COLORS, FONTS, SPACING
from ..case_manager import CaseManager

logger = logging.getLogger(__name__)


class CaseInputFrame(ctk.CTkFrame):
    """Panel para ingresar nuevos casos con número automático."""

    def __init__(self, parent, on_submit: Callable, **kwargs):
        super().__init__(parent, **kwargs)

        self.on_submit = on_submit
        self.case_manager = CaseManager()
        logger.info(f"✅ CaseInputFrame inicializado")
        self._setup_ui()
        self._generate_case_number()

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

        # Campo de número de caso (AUTO-GENERADO, no editable)
        ctk.CTkLabel(self, text="Número de caso (automático):", text_color=COLORS["text"]).pack(anchor="w", padx=SPACING["md"])
        self.case_number = ctk.CTkEntry(
            self,
            fg_color=COLORS["surface"],
            text_color=COLORS["text"],
            border_color=COLORS["border"],
            state="readonly"
        )
        self.case_number.pack(fill="x", padx=SPACING["md"], pady=(0, SPACING["sm"]))

        # Botón regenerar número
        regen_btn = ctk.CTkButton(
            self,
            text="🔄 Regenerar Número",
            command=self._generate_case_number,
            fg_color=COLORS["muted"],
            text_color="white",
            width=150,
            height=28
        )
        regen_btn.pack(anchor="w", padx=SPACING["md"], pady=(0, SPACING["md"]))

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
            text="✅ Analizar y Guardar caso",
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

    def _generate_case_number(self):
        """Genera número de caso automático."""
        try:
            case_num = self.case_manager.generate_case_number()
            self.case_number.configure(state="normal")
            self.case_number.delete(0, "end")
            self.case_number.insert(0, case_num)
            self.case_number.configure(state="readonly")
            logger.info(f"📋 Número generado: {case_num}")
        except Exception as e:
            logger.error(f"Error generando número: {e}")
            now = datetime.now()
            fallback = f"CASE-{now.strftime('%Y%m')}-MANUAL"
            self.case_number.configure(state="normal")
            self.case_number.delete(0, "end")
            self.case_number.insert(0, fallback)
            self.case_number.configure(state="readonly")

    def _on_submit(self):
        """Maneja el envío del formulario - guarda en DB automáticamente."""
        try:
            case_number = self.case_number.get().strip()
            case_text = self.text_input.get("1.0", "end").strip()

            logger.info(f"📋 Botón enviado: {case_number}")

            if not case_text:
                logger.warning("Texto de caso vacío")
                self._show_error("Ingresa la descripción del caso")
                return

            # GUARDAR EN BASE DE DATOS AUTOMÁTICAMENTE
            try:
                from ..config_manager import ConfigManager
                config = ConfigManager()
                analysis = config.analyze(case_text)

                case = self.case_manager.create_case(
                    text=case_text,
                    urgency=analysis.get("urgency", "Baja"),
                    keywords=analysis.get("keywords", [])
                )
                logger.info(f"✅ Caso guardado en DB: {case.case_number}")

                # Usar el número generado por CaseManager
                case_number = case.case_number
                self.case_number.configure(state="normal")
                self.case_number.delete(0, "end")
                self.case_number.insert(0, case_number)
                self.case_number.configure(state="readonly")

            except Exception as db_err:
                logger.error(f"❌ Error guardando en DB: {db_err}")

            # LLAMAR AL CALLBACK para mostrar análisis en UI
            if self.on_submit:
                self.on_submit(case_number, case_text)
            else:
                logger.error("❌ on_submit es None!")

        except Exception as e:
            logger.error(f"❌ Error en _on_submit: {e}", exc_info=True)
            self._show_error(f"Error: {str(e)}")

    def _on_clear(self):
        """Limpia el formulario y genera nuevo número."""
        self.text_input.delete("1.0", "end")
        self._generate_case_number()
        logger.info("🗑️ Formulario limpiado")

    def _show_error(self, message: str):
        """Muestra un error."""
        logger.error(f"⚠️ {message}")
        error_label = ctk.CTkLabel(
            self,
            text=f"⚠️ {message}",
            text_color=COLORS["danger"],
            font=FONTS["small"]
        )
        error_label.pack(anchor="w", padx=SPACING["md"])
        # Auto-eliminar después de 3 segundos
        self.after(3000, error_label.destroy)

    def get_input(self) -> dict:
        """Obtiene los datos del formulario."""
        return {
            "case_number": self.case_number.get(),
            "text": self.text_input.get("1.0", "end")
        }

    def clear(self):
        """Limpia el formulario."""
        self._on_clear()
