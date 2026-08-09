"""Formulario profesional para recopilar y analizar Informes Sociales."""
import json
import logging
from datetime import date
from pathlib import Path
from tkinter import filedialog, messagebox
import customtkinter as ctk
from .styles import COLORS, FONTS
from ..report_generator import generate_social_report
from ..social_analyzer import SocialReportAnalyzer

logger = logging.getLogger(__name__)
DATA_DIR = Path(__file__).parent.parent.parent / "data"
DEFAULTS_PATH = DATA_DIR / "institution_defaults.json"
DRAFT_PATH = DATA_DIR / "ultimo_informe_social.json"
ANALYSIS_PATH = DATA_DIR / "ultimo_analisis_social.json"


class SocialReportPanel(ctk.CTkFrame):
    """Recopila los siete bloques de un informe social y ofrece análisis orientativo."""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.entries = {}
        self.textboxes = {}
        self.analysis = None
        self._setup_ui()
        self._load_defaults()

    def _setup_ui(self):
        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=20, pady=18)
        ctk.CTkLabel(scroll, text="Informe Social Profesional", font=FONTS["title"], text_color=COLORS["primary"]).pack(anchor="w")
        ctk.CTkLabel(
            scroll,
            text="Recopilá la información disponible, analizala y revisá el resultado antes de emitir el documento.",
            font=FONTS["body"], text_color=COLORS["text_muted"], wraplength=900, justify="left"
        ).pack(anchor="w", pady=(3, 18))

        self._section(scroll, "1. Datos del profesional e institución", [
            ("entidad_emisora", "Entidad emisora"),
            ("profesional", "Profesional de referencia"),
            ("colegiatura", "Número de colegiatura / matrícula"),
            ("destinatario", "Destinatario"),
            ("fecha_emision", "Fecha de emisión", date.today().isoformat()),
            ("motivo", "Motivo de la solicitud"),
        ])
        self._section(scroll, "2. Identificación de la persona de referencia", [
            ("nombre_completo", "Nombres y apellidos completos"),
            ("documento", "DNI / NIE / Pasaporte"),
            ("domicilio", "Domicilio actual"),
            ("telefono", "Teléfono"),
            ("email", "Correo electrónico"),
            ("fecha_nacimiento", "Fecha de nacimiento"),
            ("edad", "Edad"),
            ("sexo", "Sexo"),
            ("nacionalidad", "Nacionalidad"),
            ("estado_civil", "Estado civil"),
        ])
        self._text_section(scroll, "3. Unidad de convivencia y dinámica familiar", [
            ("miembros_hogar", "Miembros del hogar — una persona por línea: parentesco, edad y ocupación"),
            ("historia_familiar", "Antecedentes e historia familiar"),
            ("dinamica_familiar", "Dinámica y vínculos: apoyo, conflicto, cuidados y organización"),
            ("genograma", "Genograma / observaciones visuales — opcional"),
        ])
        self._text_section(scroll, "4. Situación socioeconómica y laboral", [
            ("ingresos", "Fuentes de ingresos y sustento — indicar montos cuando sea posible"),
            ("situacion_laboral", "Situación laboral de los integrantes"),
            ("egresos", "Egresos básicos: alquiler, servicios, alimentación y otros gastos esenciales"),
        ])
        self._text_section(scroll, "5. Habitabilidad y vivienda", [
            ("tenencia", "Régimen de tenencia"),
            ("condiciones_vivienda", "Condiciones materiales, cantidad de habitaciones y hacinamiento"),
            ("servicios_entorno", "Acceso a agua, electricidad, transporte y equipamiento del entorno"),
        ])
        self._text_section(scroll, "6. Salud y educación", [
            ("salud", "Situación sanitaria, discapacidad, dependencia, tratamientos o apoyos relevantes"),
            ("educacion", "Nivel educativo y asistencia escolar de niños, niñas y adolescentes"),
        ])
        self._text_section(scroll, "7. Diagnóstico, valoración y propuesta", [
            ("diagnostico", "Juicio técnico / valoración social"),
            ("fortalezas", "Fortalezas y factores protectores"),
            ("vulnerabilidades", "Vulnerabilidades y factores de riesgo"),
            ("propuesta", "Propuesta de intervención / recursos a activar"),
            ("observaciones", "Observaciones finales"),
        ])

        analysis_card = ctk.CTkFrame(scroll, fg_color=COLORS["surface_alt"], corner_radius=16, border_width=1, border_color=COLORS["border"])
        analysis_card.pack(fill="x", pady=(12, 8))
        ctk.CTkLabel(analysis_card, text="Análisis del informe", font=FONTS["heading"], text_color=COLORS["primary"]).pack(anchor="w", padx=16, pady=(14, 4))
        ctk.CTkLabel(
            analysis_card,
            text="El sistema revisa completitud, indicadores sociales, consistencia y algunos datos cuantificables. El resultado es orientativo y requiere revisión profesional.",
            font=FONTS["small"], text_color=COLORS["text_muted"], wraplength=820, justify="left"
        ).pack(anchor="w", padx=16, pady=(0, 10))
        self.analysis_label = ctk.CTkLabel(
            analysis_card, text="Sin análisis. Completá la información disponible y seleccioná Analizar.",
            font=FONTS["body"], text_color=COLORS["text"], justify="left", anchor="w", wraplength=820
        )
        self.analysis_label.pack(fill="x", padx=16, pady=(0, 12))
        ctk.CTkButton(
            analysis_card, text="Analizar información", command=self.analyze_report,
            fg_color=COLORS["primary"], hover_color=COLORS["primary_dark"], text_color="white", width=190
        ).pack(anchor="w", padx=16, pady=(0, 15))

        buttons = ctk.CTkFrame(scroll, fg_color="transparent")
        buttons.pack(fill="x", pady=(10, 5))
        ctk.CTkButton(buttons, text="Fijar datos institucionales", command=self.save_defaults, fg_color=COLORS["primary"], text_color="white", width=190).pack(side="left", padx=(0, 8))
        ctk.CTkButton(buttons, text="Guardar borrador", command=self.save_draft, fg_color=COLORS["primary"], text_color="white", width=150).pack(side="left", padx=8)
        ctk.CTkButton(buttons, text="Generar PDF", command=self.export_pdf, fg_color=COLORS["primary"], text_color="white", width=130).pack(side="left", padx=8)
        ctk.CTkButton(buttons, text="Exportar JSON", command=self.export_json, fg_color="transparent", border_width=1, border_color=COLORS["primary"], text_color=COLORS["primary"], width=140).pack(side="left", padx=8)
        ctk.CTkButton(buttons, text="Limpiar", command=self.clear_form, fg_color="transparent", border_width=1, border_color=COLORS["border"], text_color=COLORS["text"], width=100).pack(side="left", padx=8)
        ctk.CTkLabel(
            scroll,
            text="Privacidad: los datos se procesan y almacenan localmente. Verificá la información y la interpretación antes de emitir o compartir el informe.",
            font=FONTS["small"], text_color=COLORS["text_muted"], wraplength=820
        ).pack(anchor="w", pady=(8, 15))

    def _section(self, parent, title, fields):
        frame = ctk.CTkFrame(parent, fg_color=COLORS["surface"], corner_radius=10, border_width=1, border_color=COLORS["border"])
        frame.pack(fill="x", pady=7)
        ctk.CTkLabel(frame, text=title, font=FONTS["heading"], text_color=COLORS["primary"]).pack(anchor="w", padx=14, pady=(12, 8))
        for item in fields:
            key, label = item[:2]
            default = item[2] if len(item) > 2 else ""
            row = ctk.CTkFrame(frame, fg_color="transparent")
            row.pack(fill="x", padx=14, pady=4)
            ctk.CTkLabel(row, text=label, width=250, anchor="w", text_color=COLORS["text"]).pack(side="left")
            entry = ctk.CTkEntry(row, height=34)
            entry.pack(side="left", fill="x", expand=True)
            if default:
                entry.insert(0, default)
            self.entries[key] = entry

    def _text_section(self, parent, title, fields):
        frame = ctk.CTkFrame(parent, fg_color=COLORS["surface"], corner_radius=10, border_width=1, border_color=COLORS["border"])
        frame.pack(fill="x", pady=7)
        ctk.CTkLabel(frame, text=title, font=FONTS["heading"], text_color=COLORS["primary"]).pack(anchor="w", padx=14, pady=(12, 8))
        for key, label in fields:
            ctk.CTkLabel(frame, text=label, anchor="w", text_color=COLORS["text"]).pack(anchor="w", padx=14, pady=(5, 3))
            box = ctk.CTkTextbox(frame, height=90, fg_color=COLORS["background"], text_color=COLORS["text"])
            box.pack(fill="x", padx=14, pady=(0, 7))
            self.textboxes[key] = box

    def collect_data(self):
        data = {key: widget.get().strip() for key, widget in self.entries.items()}
        data.update({key: widget.get("1.0", "end").strip() for key, widget in self.textboxes.items()})
        data["document_type"] = "Informe Social Profesional"
        data["generated_at"] = date.today().isoformat()
        if self.analysis:
            data["analysis"] = self.analysis
        return data

    def _load_defaults(self):
        try:
            if not DEFAULTS_PATH.exists():
                return
            data = json.loads(DEFAULTS_PATH.read_text(encoding="utf-8"))
            for key in ("entidad_emisora", "profesional", "colegiatura", "destinatario"):
                if data.get(key) and key in self.entries and not self.entries[key].get():
                    self.entries[key].insert(0, data[key])
        except Exception as exc:
            logger.warning("No se pudieron cargar los datos institucionales fijados: %s", exc)

    def save_defaults(self):
        try:
            DATA_DIR.mkdir(parents=True, exist_ok=True)
            data = self.collect_data()
            defaults = {key: data.get(key, "") for key in ("entidad_emisora", "profesional", "colegiatura", "destinatario")}
            DEFAULTS_PATH.write_text(json.dumps(defaults, ensure_ascii=False, indent=2), encoding="utf-8")
            messagebox.showinfo("Datos fijados", "Los datos institucionales se usarán en nuevos informes.")
        except Exception as exc:
            logger.exception("Error fijando datos institucionales")
            messagebox.showerror("Error", f"No se pudieron fijar los datos:\n{exc}")

    def analyze_report(self):
        try:
            self.analysis = SocialReportAnalyzer().analyze(self.collect_data())
            a = self.analysis
            blocks = [f"ESTADO: {a['level']}    ·    COMPLETITUD: {a['completeness']}%"]
            if a["risk_indicators"]:
                blocks.append("INDICADORES: " + ", ".join(a["risk_indicators"]))
            else:
                blocks.append("INDICADORES: no se detectaron indicadores automáticos destacados")
            if a["missing_fields"]:
                blocks.append("PENDIENTES: " + ", ".join(a["missing_fields"][:10]))
            if a["consistency_flags"]:
                blocks.append("REVISAR: " + " ".join(a["consistency_flags"]))
            metrics = []
            if a["household_members"] is not None:
                metrics.append(f"convivientes: {int(a['household_members'])}")
            if a["persons_per_room"] is not None:
                metrics.append(f"personas/habitación: {a['persons_per_room']}")
            if a["balance"] is not None:
                metrics.append(f"saldo declarado: ARS {a['balance']:,.2f}")
            if metrics:
                blocks.append("DATOS CALCULADOS: " + " · ".join(metrics))
            blocks.append("PRÓXIMO PASO: " + a["recommendations"][0])
            self.analysis_label.configure(text="\n".join(blocks))
            DATA_DIR.mkdir(parents=True, exist_ok=True)
            ANALYSIS_PATH.write_text(json.dumps(a, ensure_ascii=False, indent=2), encoding="utf-8")
        except Exception as exc:
            logger.exception("Error analizando informe social")
            messagebox.showerror("Error", f"No se pudo analizar el informe:\n{exc}")

    def save_draft(self):
        try:
            DATA_DIR.mkdir(parents=True, exist_ok=True)
            DRAFT_PATH.write_text(json.dumps(self.collect_data(), ensure_ascii=False, indent=2), encoding="utf-8")
            messagebox.showinfo("Guardado", "Borrador guardado localmente.")
        except Exception as exc:
            logger.exception("Error guardando informe")
            messagebox.showerror("Error", f"No se pudo guardar el informe:\n{exc}")

    def export_json(self):
        try:
            if self.analysis is None:
                self.analyze_report()
            path = filedialog.asksaveasfilename(title="Exportar informe social", defaultextension=".json", filetypes=[("Informe JSON", "*.json")], initialfile="informe_social.json")
            if path:
                Path(path).write_text(json.dumps(self.collect_data(), ensure_ascii=False, indent=2), encoding="utf-8")
                messagebox.showinfo("Exportado", "Informe y análisis exportados correctamente.")
        except Exception as exc:
            messagebox.showerror("Error", f"No se pudo exportar el informe:\n{exc}")

    def export_pdf(self):
        try:
            if self.analysis is None:
                self.analyze_report()
            path = filedialog.asksaveasfilename(title="Generar informe PDF", defaultextension=".pdf", filetypes=[("PDF", "*.pdf")], initialfile="informe_social.pdf")
            if path:
                generate_social_report(self.collect_data(), path)
                messagebox.showinfo("PDF generado", "Informe PDF generado correctamente.")
        except Exception as exc:
            logger.exception("Error generando PDF")
            messagebox.showerror("Error", f"No se pudo generar el informe:\n{exc}")

    def clear_form(self):
        for widget in self.entries.values():
            widget.delete(0, "end")
        for widget in self.textboxes.values():
            widget.delete("1.0", "end")
        self.analysis = None
        self.analysis_label.configure(text="Sin análisis. Completá la información disponible y seleccioná Analizar.")
        self._load_defaults()
