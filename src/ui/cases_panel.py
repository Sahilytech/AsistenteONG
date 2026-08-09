"""Panel de gestión y consulta de casos."""
import customtkinter as ctk
from .styles import COLORS, FONTS
from .case_input import CaseInputFrame


class CasesPanel(ctk.CTkFrame):
    def __init__(self, parent, case_manager=None, on_analyze=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.case_manager = case_manager
        self.on_analyze = on_analyze
        self.all_cases = []
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        head = ctk.CTkFrame(self, fg_color="transparent")
        head.grid(row=0, column=0, sticky="ew", padx=24, pady=(22, 10))
        head.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(head, text="Casos", font=FONTS["title"], text_color=COLORS["text"]).grid(row=0, column=0, sticky="w")
        self.count_label = ctk.CTkLabel(head, text="0 registrados", font=FONTS["small"], text_color=COLORS["text_muted"])
        self.count_label.grid(row=1, column=0, sticky="w", pady=(3, 0))
        ctk.CTkButton(head, text="＋ Nuevo caso", width=125, height=36, fg_color=COLORS["primary"], hover_color=COLORS["primary_dark"], command=self.show_new_case).grid(row=0, column=1, rowspan=2, padx=(10, 0))

        tools = ctk.CTkFrame(self, fg_color=COLORS["surface_alt"], corner_radius=14, border_width=1, border_color=COLORS["border"])
        tools.grid(row=1, column=0, sticky="ew", padx=24, pady=(0, 10))
        tools.grid_columnconfigure(0, weight=1)
        row = ctk.CTkFrame(tools, fg_color="transparent")
        row.grid(row=0, column=0, sticky="ew", padx=12, pady=12)
        row.grid_columnconfigure(0, weight=1)
        self.search = ctk.CTkEntry(row, height=38, placeholder_text="Buscar por ID, relato, palabra clave o responsable...")
        self.search.grid(row=0, column=0, sticky="ew")
        self.search.bind("<KeyRelease>", lambda _event: self.refresh())
        self.urgency = ctk.CTkOptionMenu(row, width=125, height=38, values=["Todas", "Muy Alta", "Alta", "Media", "Baja"], command=lambda _value: self.refresh())
        self.urgency.grid(row=0, column=1, padx=(8, 0))
        self.status = ctk.CTkOptionMenu(row, width=145, height=38, values=["Todos", "nuevo", "en análisis", "revisado", "derivado", "en seguimiento", "cerrado"], command=lambda _value: self.refresh())
        self.status.grid(row=0, column=2, padx=(8, 0))
        ctk.CTkButton(row, text="Limpiar", width=72, height=38, fg_color=COLORS["surface"], hover_color=COLORS["primary_soft"], text_color=COLORS["text"], border_width=1, border_color=COLORS["border"], command=self.clear_filters).grid(row=0, column=3, padx=(8, 0))

        self.list_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.list_frame.grid(row=2, column=0, sticky="nsew", padx=24, pady=(0, 20))
        self.refresh()

    def show_new_case(self):
        if hasattr(self, "editor") and self.editor.winfo_exists():
            self.editor.destroy()
        self.editor = ctk.CTkFrame(self, fg_color=COLORS["background"])
        self.editor.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.editor.lift()
        ctk.CTkButton(self.editor, text="← Volver a casos", width=125, height=34, fg_color="transparent", hover_color=COLORS["primary_soft"], text_color=COLORS["primary"], command=self.close_editor).pack(anchor="w", padx=24, pady=(18, 0))
        CaseInputFrame(self.editor, on_submit=self._submit_new_case, fg_color=COLORS["background"]).pack(fill="both", expand=True, padx=10, pady=2)

    def close_editor(self):
        if hasattr(self, "editor") and self.editor.winfo_exists():
            self.editor.destroy()
        self.refresh()

    def _submit_new_case(self, text, metadata):
        if self.on_analyze:
            self.on_analyze(text, metadata)

    def clear_filters(self):
        self.search.delete(0, "end")
        self.urgency.set("Todas")
        self.status.set("Todos")
        self.refresh()

    def refresh(self):
        self.all_cases = self.case_manager.get_all_cases() if self.case_manager else []
        query = self.search.get().strip().lower()
        urgency = self.urgency.get().lower()
        status = self.status.get().lower()
        filtered = []
        for case in self.all_cases:
            hay = " ".join([
                str(getattr(case, "case_number", "")), str(getattr(case, "text", "")),
                str(getattr(case, "assigned_to", "")), str(getattr(case, "person_name", "")),
                str(getattr(case, "contact", "")), str(getattr(case, "case_type", "")),
                str(getattr(case, "location", "")), " ".join(getattr(case, "keywords", []) or [])
            ]).lower()
            if query and query not in hay:
                continue
            if urgency != "todas" and str(getattr(case, "urgency", "")).lower() != urgency:
                continue
            if status != "todos" and str(getattr(case, "status", "")).lower() != status:
                continue
            filtered.append(case)

        for child in self.list_frame.winfo_children():
            child.destroy()
        self.count_label.configure(text=f"{len(filtered)} de {len(self.all_cases)} registrados")
        if not filtered:
            empty = ctk.CTkFrame(self.list_frame, fg_color=COLORS["surface_alt"], corner_radius=16, border_width=1, border_color=COLORS["border"])
            empty.pack(fill="x", pady=8)
            ctk.CTkLabel(empty, text="No hay casos registrados." if not self.all_cases else "No se encontraron casos.", font=FONTS["heading"], text_color=COLORS["text"]).pack(pady=(28, 5))
            ctk.CTkLabel(empty, text="Los casos que crees aparecerán acá." if not self.all_cases else "Probá cambiar la búsqueda o los filtros.", font=FONTS["small"], text_color=COLORS["text_muted"]).pack(pady=(0, 28))
            return
        for case in filtered:
            self._case_card(case)

    def _case_card(self, case):
        card = ctk.CTkFrame(self.list_frame, fg_color=COLORS["surface"], corner_radius=14, border_width=1, border_color=COLORS["border"])
        card.pack(fill="x", pady=5)
        card.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(card, text=case.case_number, font=FONTS["subheading"], text_color=COLORS["primary"], anchor="w").grid(row=0, column=0, sticky="w", padx=16, pady=(14, 3))
        ctk.CTkLabel(card, text=str(case.urgency).upper(), font=FONTS["tiny"], text_color=COLORS["primary"], fg_color=COLORS["primary_soft"], corner_radius=7).grid(row=0, column=2, sticky="e", padx=16, pady=(12, 3))
        ctk.CTkLabel(card, text=str(case.status).replace("_", " ").title(), font=FONTS["tiny"], text_color=COLORS["text_muted"]).grid(row=1, column=0, sticky="w", padx=16, pady=(0, 10))
        summary = " · ".join(x for x in [getattr(case, "person_name", ""), getattr(case, "case_type", ""), getattr(case, "location", "")] if x)
        text = (summary + "\n" if summary else "") + str(case.text).replace("\n", " ").strip()
        ctk.CTkLabel(card, text=text, font=FONTS["small"], text_color=COLORS["text"], anchor="w", justify="left", wraplength=760).grid(row=0, column=1, rowspan=2, sticky="ew", padx=14, pady=12)
        ctk.CTkButton(card, text="Abrir", width=72, height=30, fg_color=COLORS["surface_alt"], hover_color=COLORS["primary_soft"], text_color=COLORS["primary"], border_width=1, border_color=COLORS["border"], command=lambda c=case: self.open_case(c)).grid(row=0, column=3, rowspan=2, padx=(0, 12))

    def open_case(self, case):
        if hasattr(self, "editor") and self.editor.winfo_exists():
            self.editor.destroy()
        self.editor = ctk.CTkFrame(self, fg_color=COLORS["background"])
        self.editor.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.editor.lift()
        ctk.CTkButton(self.editor, text="← Volver a casos", width=125, height=34, fg_color="transparent", hover_color=COLORS["primary_soft"], text_color=COLORS["primary"], command=self.close_editor).pack(anchor="w", padx=24, pady=(18, 0))
        box = ctk.CTkScrollableFrame(self.editor, fg_color="transparent")
        box.pack(fill="both", expand=True, padx=24, pady=8)
        ctk.CTkLabel(box, text=case.case_number, font=FONTS["title"], text_color=COLORS["text"]).pack(anchor="w")
        ctk.CTkLabel(box, text=f"Prioridad: {case.urgency} · Estado: {str(case.status).replace('_', ' ').title()}", font=FONTS["small"], text_color=COLORS["text_muted"]).pack(anchor="w", pady=(3, 14))
        self._detail(box, "Datos", f"Nombre / alias: {getattr(case, 'person_name', '') or 'No indicado'}\nContacto: {getattr(case, 'contact', '') or 'No indicado'}\nTipo: {getattr(case, 'case_type', '') or 'No indicado'}\nZona: {getattr(case, 'location', '') or 'No indicada'}")
        self._detail(box, "Relato", case.text)
        self._detail(box, "Palabras clave", ", ".join(case.keywords) if case.keywords else "Sin palabras clave")
        self._detail(box, "Seguimiento", getattr(case, "follow_up_date", "") or "Sin fecha")
        self._detail(box, "Notas", getattr(case, "notes", "") or "Sin notas")

    def _detail(self, parent, title, text):
        card = ctk.CTkFrame(parent, fg_color=COLORS["surface_alt"], corner_radius=12, border_width=1, border_color=COLORS["border"])
        card.pack(fill="x", pady=5)
        ctk.CTkLabel(card, text=title.upper(), font=FONTS["tiny"], text_color=COLORS["primary"]).pack(anchor="w", padx=16, pady=(12, 4))
        ctk.CTkLabel(card, text=text, font=FONTS["body"], text_color=COLORS["text"], justify="left", anchor="w", wraplength=800).pack(fill="x", padx=16, pady=(0, 14))
