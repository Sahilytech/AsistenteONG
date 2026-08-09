"""Expediente integrado: caso + informe social + análisis.

La pantalla sigue las siete categorías mínimas del informe social y evita
campos técnicos innecesarios para la persona operadora.
"""
import customtkinter as ctk
from .styles import COLORS, FONTS
from ..config_manager import ConfigManager
from ..reports.report_defaults import ReportDefaults

SECTIONS = [
    ("1. Profesional e institución", "Datos que pueden fijarse para nuevos informes.", [
        ("entidad_emisora", "Entidad emisora"), ("profesional_referencia", "Profesional de referencia"),
        ("colegiatura", "Número de colegiatura / matrícula"), ("destinatario", "Destinatario"),
        ("fecha_emision", "Fecha de emisión"), ("motivo", "Motivo de la solicitud")]),
    ("2. Identificación de la persona de referencia", "Datos de identificación y contacto.", [
        ("nombre_completo", "Nombres y apellidos completos"), ("documento", "DNI / NIE / pasaporte"),
        ("domicilio", "Domicilio actual"), ("telefono", "Teléfono"), ("correo", "Correo electrónico"),
        ("fecha_nacimiento", "Fecha de nacimiento"), ("edad", "Edad"), ("sexo", "Sexo"),
        ("nacionalidad", "Nacionalidad"), ("estado_civil", "Estado civil")]),
    ("3. Unidad de convivencia y dinámica familiar", "Personas que viven en el hogar, vínculos e historia familiar.", [
        ("miembros_hogar", "Miembros del hogar: parentesco, edad y ocupación"),
        ("genograma", "Genograma / vínculos familiares (opcional)"),
        ("historia_familiar", "Antecedentes familiares"), ("dinamica_familiar", "Dinámica y relaciones familiares")]),
    ("4. Situación socioeconómica y laboral", "Ingresos, trabajo y egresos básicos.", [
        ("ingresos", "Fuentes de ingresos y sustento"), ("situacion_laboral", "Situación laboral de los integrantes"),
        ("egresos", "Egresos básicos: alquiler, servicios, alimentación, etc.")]),
    ("5. Habitabilidad y vivienda", "Tenencia, condiciones materiales y acceso a servicios.", [
        ("tenencia", "Régimen de tenencia"), ("condiciones_vivienda", "Condiciones materiales, habitaciones y hacinamiento"),
        ("servicios_entorno", "Agua, electricidad, transporte y servicios del entorno")]),
    ("6. Salud y educación", "Situación sanitaria, dependencia, educación y escolaridad.", [
        ("salud", "Estado sanitario, discapacidad, dependencia o consumo problemático"),
        ("educacion", "Nivel educativo y asistencia escolar")]),
    ("7. Diagnóstico, valoración y propuesta", "Juicio técnico, fortalezas, vulnerabilidades y plan de intervención.", [
        ("diagnostico", "Valoración / juicio técnico"), ("fortalezas", "Fortalezas y factores protectores"),
        ("vulnerabilidades", "Vulnerabilidades / necesidades"), ("propuesta", "Propuesta de intervención y recurso solicitado"),
        ("observaciones", "Observaciones y límites de la información")]),
]

class IntegratedCasePanel(ctk.CTkFrame):
    def __init__(self, parent, case_manager=None, config_manager=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.case_manager = case_manager
        self.config_manager = config_manager or ConfigManager()
        self.defaults = ReportDefaults()
        self.current_case = None
        self.analysis = None
        self.boxes = {}
        self._build()
        self.refresh_cases()

    def _build(self):
        self.grid_columnconfigure(0, weight=1)
        head = ctk.CTkFrame(self, fg_color="transparent")
        head.pack(fill="x", padx=24, pady=(22, 8))
        ctk.CTkLabel(head, text="Caso + Informe Social", font=FONTS["title"], text_color=COLORS["text"]).pack(anchor="w")
        ctk.CTkLabel(head, text="Un solo expediente: relato, contexto social, valoración e intervención. El informe no reemplaza el criterio profesional.", font=FONTS["small"], text_color=COLORS["text_muted"], wraplength=980, justify="left").pack(anchor="w", pady=(3, 10))
        selector = ctk.CTkFrame(self, fg_color=COLORS["surface_alt"], corner_radius=14, border_width=1, border_color=COLORS["border"])
        selector.pack(fill="x", padx=24, pady=(0, 8))
        selector.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(selector, text="Expediente", font=FONTS["small_bold"], text_color=COLORS["text"]).grid(row=0, column=0, padx=12, pady=12)
        self.case_menu = ctk.CTkComboBox(selector, values=["Sin casos"], command=self.load_case)
        self.case_menu.grid(row=0, column=1, sticky="ew", padx=8, pady=10)
        self.status = ctk.CTkLabel(selector, text="Creá un caso para empezar.", font=FONTS["tiny"], text_color=COLORS["text_muted"])
        self.status.grid(row=0, column=2, padx=12)
        self.save_defaults_btn = ctk.CTkButton(selector, text="Fijar datos institucionales", width=190, command=self.save_institution_defaults, fg_color=COLORS["surface"], text_color=COLORS["primary"], border_width=1, border_color=COLORS["border"], hover_color=COLORS["primary_soft"])
        self.save_defaults_btn.grid(row=0, column=3, padx=(0, 12))

        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll.pack(fill="both", expand=True, padx=24, pady=(0, 20))
        self._build_case_summary(self.scroll)
        for title, description, fields in SECTIONS:
            self._section(self.scroll, title, description, fields)
        actions = ctk.CTkFrame(self.scroll, fg_color=COLORS["surface_alt"], corner_radius=14, border_width=1, border_color=COLORS["border"])
        actions.pack(fill="x", pady=10)
        ctk.CTkButton(actions, text="Analizar caso + informe", height=42, command=self.analyze_combined, fg_color=COLORS["primary"], hover_color=COLORS["primary_dark"]).pack(side="left", padx=12, pady=12)
        ctk.CTkButton(actions, text="Guardar expediente", height=42, command=self.save_to_case, fg_color=COLORS["surface"], text_color=COLORS["primary"], border_width=1, border_color=COLORS["border"], hover_color=COLORS["primary_soft"]).pack(side="left", padx=(0, 12), pady=12)
        self.result = ctk.CTkLabel(actions, text="Completá la información disponible y revisá el análisis.", font=FONTS["small"], text_color=COLORS["text_muted"], justify="left", anchor="w", wraplength=760)
        self.result.pack(side="left", fill="x", expand=True, padx=8, pady=12)

    def _build_case_summary(self, parent):
        card = ctk.CTkFrame(parent, fg_color=COLORS["surface"], corner_radius=14, border_width=1, border_color=COLORS["border"])
        card.pack(fill="x", pady=6)
        ctk.CTkLabel(card, text="Relato del caso", font=FONTS["heading"], text_color=COLORS["primary"]).pack(anchor="w", padx=16, pady=(14, 4))
        self.case_text = ctk.CTkLabel(card, text="Seleccioná un caso para revisar su relato.", font=FONTS["body"], text_color=COLORS["text"], justify="left", anchor="w", wraplength=980)
        self.case_text.pack(fill="x", padx=16, pady=(0, 14))
        self.analysis_hint = ctk.CTkLabel(card, text="", font=FONTS["small"], text_color=COLORS["text_muted"], justify="left", anchor="w", wraplength=980)
        self.analysis_hint.pack(fill="x", padx=16, pady=(0, 14))

    def _section(self, parent, title, description, fields):
        card = ctk.CTkFrame(parent, fg_color=COLORS["surface"], corner_radius=15, border_width=1, border_color=COLORS["border"])
        card.pack(fill="x", pady=6)
        ctk.CTkLabel(card, text=title, font=FONTS["heading"], text_color=COLORS["text"], anchor="w").pack(fill="x", padx=18, pady=(15, 3))
        ctk.CTkLabel(card, text=description, font=FONTS["tiny"], text_color=COLORS["text_muted"], anchor="w", justify="left", wraplength=950).pack(fill="x", padx=18, pady=(0, 8))
        grid = ctk.CTkFrame(card, fg_color="transparent")
        grid.pack(fill="x", padx=12, pady=(0, 10))
        grid.grid_columnconfigure(0, weight=1)
        grid.grid_columnconfigure(1, weight=1)
        for i, (key, label) in enumerate(fields):
            wrap = ctk.CTkFrame(grid, fg_color="transparent")
            row, col = divmod(i, 2)
            wrap.grid(row=row, column=col, sticky="ew", padx=6, pady=5)
            ctk.CTkLabel(wrap, text=label, font=FONTS["small_bold"], text_color=COLORS["text"], anchor="w").pack(fill="x", pady=(0, 3))
            height = 78 if key not in {"entidad_emisora", "profesional_referencia", "colegiatura", "destinatario", "fecha_emision", "documento", "domicilio", "telefono", "correo", "fecha_nacimiento", "edad", "sexo", "nacionalidad", "estado_civil"} else 46
            box = ctk.CTkTextbox(wrap, height=height, fg_color=COLORS["surface_alt"], border_width=1, border_color=COLORS["border"], text_color=COLORS["text"])
            box.pack(fill="x")
            self.boxes[key] = box

    def refresh_cases(self):
        cases = self.case_manager.get_all_cases() if self.case_manager else []
        self.case_map = {c.case_number: c for c in cases}
        values = list(self.case_map) or ["Sin casos"]
        self.case_menu.configure(values=values)
        self.case_menu.set(values[0])
        if cases:
            self.load_case(values[0])
        else:
            self.current_case = None
            self.case_text.configure(text="No hay casos registrados. Creá uno desde Casos.")
            self.analysis_hint.configure(text="")
            self.status.configure(text="Sin casos")

    def load_case(self, number):
        case = self.case_map.get(number)
        if not case:
            return
        self.current_case = case
        self.status.configure(text=f"{case.case_number} · prioridad {case.urgency} · estado {case.status}")
        self.case_text.configure(text=case.text)
        a = case.combined_analysis or {}
        self.analysis_hint.configure(text=(f"Clasificación: {a.get('classification', '—')} · Confianza: {a.get('confidence', '—')} · Contexto: {a.get('detected_context', '—')}\n" + a.get('priority_reason', '')) if a else "Todavía no hay un análisis integral guardado.")
        report = {**self.defaults.load(), **(case.social_report or {})}
        for key, box in self.boxes.items():
            box.delete("1.0", "end")
            box.insert("1.0", str(report.get(key, "")))
        self.analysis = a or None

    def collect_report(self):
        return {key: box.get("1.0", "end").strip() for key, box in self.boxes.items() if box.get("1.0", "end").strip()}

    def save_institution_defaults(self):
        report = self.collect_report()
        keys = ["entidad_emisora", "profesional_referencia", "colegiatura", "destinatario"]
        self.defaults.save({k: report.get(k, "") for k in keys})
        self.status.configure(text="Datos institucionales guardados localmente para nuevos informes.")

    def analyze_combined(self):
        if not self.current_case:
            self.status.configure(text="Primero seleccioná un caso.")
            return
        self.analysis = self.config_manager.analyze(self.current_case.text, self.collect_report())
        self.result.configure(text=self._summary(self.analysis), text_color=COLORS["text"])
        self.status.configure(text=f"Análisis integral: {self.analysis.get('urgency', 'no determinada')}")

    def save_to_case(self):
        if not self.current_case:
            self.status.configure(text="Primero seleccioná un caso.")
            return
        report = self.collect_report()
        if self.analysis is None:
            self.analysis = self.config_manager.analyze(self.current_case.text, report)
        self.case_manager.attach_social_report(self.current_case.case_number, report, self.analysis)
        self.refresh_cases()
        self.case_menu.set(self.current_case.case_number)
        self.status.configure(text="Expediente guardado: relato + informe + análisis.")

    def _summary(self, a):
        kws = ", ".join(a.get("keywords", [])) or "ninguno"
        qs = " · ".join(a.get("next_questions", [])) or "ninguna"
        resources = ", ".join(a.get("suggested_resources", [])) or "revisar catálogo"
        return (f"PRIORIDAD ORIENTATIVA: {a.get('urgency', '—')}\n"
                f"CLASIFICACIÓN: {a.get('classification', '—')} · CONFIANZA: {a.get('confidence', '—')}\n"
                f"INDICADORES: {kws}\n"
                f"RECURSOS POSIBLES: {resources}\n"
                f"FALTA CONFIRMAR: {qs}\n\n"
                f"{a.get('context_note', '')}")
