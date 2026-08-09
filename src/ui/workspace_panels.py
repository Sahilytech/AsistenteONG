"""Paneles de trabajo secundarios con funciones reales y datos locales."""
import datetime
import customtkinter as ctk
from tkinter import filedialog, messagebox
from .styles import COLORS, FONTS
from ..knowledge.memory import LocalMemory
from ..knowledge.pdf_library import LIBRARY_DIR, import_pdf, import_folder

class WorkspacePanel(ctk.CTkFrame):
    def __init__(self, parent, title, subtitle, **kwargs):
        super().__init__(parent, **kwargs)
        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent"); scroll.pack(fill="both", expand=True, padx=24, pady=22)
        ctk.CTkLabel(scroll, text=title, font=FONTS["title"], text_color=COLORS["text"]).pack(anchor="w")
        ctk.CTkLabel(scroll, text=subtitle, font=FONTS["small"], text_color=COLORS["text_muted"], wraplength=980, justify="left").pack(anchor="w", pady=(3, 18))
        self.body = scroll

class FollowUpPanel(WorkspacePanel):
    def __init__(self, parent, case_manager=None, **kwargs):
        self.case_manager = case_manager
        super().__init__(parent, "Seguimiento", "Convertí la valoración en acciones concretas: qué hacer, quién lo hace, para cuándo y qué ocurrió.", **kwargs)
        cases = case_manager.get_all_cases() if case_manager else []
        self.case_map = {c.case_number: c for c in cases}
        selector = ctk.CTkFrame(self.body, fg_color=COLORS["surface_alt"], corner_radius=14, border_width=1, border_color=COLORS["border"]); selector.pack(fill="x", pady=6); selector.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(selector, text="Caso", font=FONTS["small_bold"]).grid(row=0, column=0, padx=12, pady=10)
        self.case_menu = ctk.CTkComboBox(selector, values=list(self.case_map) or ["Sin casos"], command=self._load_case); self.case_menu.grid(row=0, column=1, sticky="ew", padx=8, pady=10)
        self.status = ctk.CTkLabel(selector, text="", font=FONTS["tiny"], text_color=COLORS["text_muted"]); self.status.grid(row=0, column=2, padx=12)
        self._build_editor(); self._load_case(self.case_menu.get())
    def _build_editor(self):
        card = ctk.CTkFrame(self.body, fg_color=COLORS["surface"], corner_radius=14, border_width=1, border_color=COLORS["border"]); card.pack(fill="x", pady=6)
        ctk.CTkLabel(card, text="Nueva acción de seguimiento", font=FONTS["heading"], text_color=COLORS["text"]).pack(anchor="w", padx=16, pady=(14, 3))
        ctk.CTkLabel(card, text="Registrá una acción concreta. No reemplaza el criterio ni la responsabilidad profesional.", font=FONTS["tiny"], text_color=COLORS["text_muted"]).pack(anchor="w", padx=16, pady=(0, 8))
        self.task = ctk.CTkEntry(card, placeholder_text="Acción a realizar"); self.task.pack(fill="x", padx=16, pady=5)
        self.when = ctk.CTkEntry(card, placeholder_text="Fecha (AAAA-MM-DD)"); self.when.pack(fill="x", padx=16, pady=5); self.when.insert(0, datetime.date.today().isoformat())
        self.actor = ctk.CTkEntry(card, placeholder_text="Responsable"); self.actor.pack(fill="x", padx=16, pady=5)
        self.notes = ctk.CTkTextbox(card, height=80); self.notes.pack(fill="x", padx=16, pady=5)
        ctk.CTkButton(card, text="Guardar seguimiento", command=self._save, fg_color=COLORS["primary"], hover_color=COLORS["primary_dark"]).pack(anchor="e", padx=16, pady=12)
        self.timeline = ctk.CTkScrollableFrame(self.body, fg_color=COLORS["surface_alt"], height=230); self.timeline.pack(fill="x", pady=6)
    def _load_case(self, number):
        case = self.case_map.get(number)
        if not case: self.status.configure(text="Sin casos"); return
        self.status.configure(text=f"{case.status} · {len(case.timeline)} eventos"); self._render_timeline(case)
    def _render_timeline(self, case):
        for w in self.timeline.winfo_children(): w.destroy()
        for event in reversed(case.timeline):
            ctk.CTkLabel(self.timeline, text=f"{event.get('created_at','')} · {event.get('title','Evento')}", font=FONTS["small_bold"], text_color=COLORS["primary"], anchor="w").pack(fill="x", padx=12, pady=(8, 1))
            ctk.CTkLabel(self.timeline, text=event.get("description", ""), font=FONTS["tiny"], text_color=COLORS["text_muted"], anchor="w", justify="left", wraplength=900).pack(fill="x", padx=12, pady=(0, 6))
    def _save(self):
        case = self.case_map.get(self.case_menu.get()); task = self.task.get().strip()
        if not case or not task: self.status.configure(text="Seleccioná un caso y escribí una acción."); return
        date = self.when.get().strip(); actor = self.actor.get().strip(); notes = self.notes.get("1.0", "end").strip()
        case.follow_up_date = date; self.case_manager.add_timeline_event(case.case_number, "seguimiento", task, f"Fecha: {date}. {notes}", actor); self.case_manager.save_case(case)
        self.status.configure(text="Seguimiento guardado localmente."); self.task.delete(0, "end"); self.notes.delete("1.0", "end"); self.case_map[case.case_number] = self.case_manager.get_case(case.case_number); self._load_case(case.case_number)

class LibraryPanel(WorkspacePanel):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, "Biblioteca", "Cargá protocolos y documentos PDF propios. Se leen localmente, se guardan en la memoria del equipo y pueden aportar contexto a los análisis.", **kwargs)
        self.memory = LocalMemory()
        self._build_controls(); self.results = ctk.CTkScrollableFrame(self.body, fg_color="transparent"); self.results.pack(fill="both", expand=True); self._search()
    def _build_controls(self):
        actions = ctk.CTkFrame(self.body, fg_color=COLORS["surface_alt"], corner_radius=14, border_width=1, border_color=COLORS["border"]); actions.pack(fill="x", pady=6)
        ctk.CTkButton(actions, text="Importar PDFs", command=self._pick_pdfs, fg_color=COLORS["primary"], hover_color=COLORS["primary_dark"]).pack(side="left", padx=(10,5), pady=10)
        ctk.CTkButton(actions, text="Recargar carpeta", command=self._reload_folder, fg_color=COLORS["surface"], hover_color=COLORS["primary_soft"], text_color=COLORS["text"], border_width=1, border_color=COLORS["border"]).pack(side="left", padx=5, pady=10)
        ctk.CTkButton(actions, text="Abrir carpeta", command=self._open_folder, fg_color="transparent", hover_color=COLORS["primary_soft"], text_color=COLORS["text"]).pack(side="left", padx=5, pady=10)
        self.search = ctk.CTkEntry(actions, placeholder_text="Buscar en la biblioteca..."); self.search.pack(side="left", fill="x", expand=True, padx=(12,5), pady=10); self.search.bind("<Return>", lambda _: self._search())
        ctk.CTkButton(actions, text="Buscar", command=self._search, width=80, fg_color=COLORS["primary"], hover_color=COLORS["primary_dark"]).pack(side="left", padx=(0,10), pady=10)
        self.status = ctk.CTkLabel(self.body, text="", font=FONTS["small"], text_color=COLORS["text_muted"]); self.status.pack(anchor="w", pady=(4, 8))
        ctk.CTkLabel(self.body, text=f"Carpeta automática: {LIBRARY_DIR}", font=FONTS["tiny"], text_color=COLORS["text_soft"], wraplength=950, justify="left").pack(anchor="w", pady=(0,8))
    def _pick_pdfs(self):
        paths = filedialog.askopenfilenames(title="Seleccionar PDFs", filetypes=[("PDF", "*.pdf")])
        if not paths: return
        imported, errors = 0, []
        for path in paths:
            try: import_pdf(path, self.memory); imported += 1
            except Exception as exc: errors.append(f"{path}: {exc}")
        self._search()
        message = f"Se importaron {imported} PDF(s)."
        if errors: message += "\n\nNo se pudieron importar:\n" + "\n".join(errors[:5])
        messagebox.showinfo("Biblioteca", message)
    def _reload_folder(self):
        imported, errors = import_folder(LIBRARY_DIR, self.memory); self._search()
        message = f"Carpeta recargada: {imported} PDF(s) procesados."
        if errors: message += "\n\n" + "\n".join(errors[:5])
        messagebox.showinfo("Biblioteca", message)
    def _open_folder(self):
        LIBRARY_DIR.mkdir(parents=True, exist_ok=True)
        import os
        os.startfile(str(LIBRARY_DIR))
    def _search(self):
        for w in self.results.winfo_children(): w.destroy()
        q = self.search.get().strip()
        if not q:
            self.status.configure(text=f"{self.memory.count()} fuente(s) guardada(s). Biblioteca lista para recibir PDFs.")
            ctk.CTkLabel(self.results, text="Todavía no hay una búsqueda. Importá PDFs o escribí una palabra para consultar la memoria local.", font=FONTS["body"], text_color=COLORS["text_muted"], wraplength=900, justify="left").pack(anchor="w", padx=10, pady=18); return
        items = self.memory.search(q, 50); self.status.configure(text=f"{len(items)} coincidencia(s) · memoria local")
        if not items:
            ctk.CTkLabel(self.results, text="No se encontraron coincidencias.", font=FONTS["body"], text_color=COLORS["text_muted"]).pack(anchor="w", padx=10, pady=18); return
        for item in items:
            card = ctk.CTkFrame(self.results, fg_color=COLORS["surface"], corner_radius=12, border_width=1, border_color=COLORS["border"]); card.pack(fill="x", pady=5)
            ctk.CTkLabel(card, text=item.get("title", "Fuente"), font=FONTS["subheading"], text_color=COLORS["text"], anchor="w", wraplength=900).pack(fill="x", padx=14, pady=(10, 3))
            ctk.CTkLabel(card, text=f"{item.get('domain','')} · guardado {item.get('saved_at','')}", font=FONTS["tiny"], text_color=COLORS["primary"]).pack(anchor="w", padx=14)
            ctk.CTkLabel(card, text=item.get("snippet", ""), font=FONTS["small"], text_color=COLORS["text_muted"], anchor="w", justify="left", wraplength=900).pack(fill="x", padx=14, pady=(4, 10))

class SecurityPanel(WorkspacePanel):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, "Privacidad y seguridad", "Controles para entender qué se guarda, qué se consulta y qué información debe quedar protegida.", **kwargs)
        self._card("Datos del caso", "Se guardan localmente en SQLite: relato, metadatos, informe social, análisis, timeline y derivaciones. No se incluyen imágenes por defecto.")
        self._card("Fuentes", "Las fuentes guardadas en memoria incluyen dominio, título, URL y fecha de guardado para mantener trazabilidad.")
        self._card("Principio de minimización", "Ingresá solo la información necesaria para el objetivo profesional. Evitá copiar datos sensibles que no aporten a la valoración.")
        self._card("Revisión", "El análisis automático es orientativo. La decisión profesional, la derivación y cualquier documento emitido requieren revisión humana.")
    def _card(self, title, text):
        card = ctk.CTkFrame(self.body, fg_color=COLORS["surface"], corner_radius=14, border_width=1, border_color=COLORS["border"]); card.pack(fill="x", pady=6)
        ctk.CTkLabel(card, text=title, font=FONTS["heading"], text_color=COLORS["text"]).pack(anchor="w", padx=18, pady=(14, 4))
        ctk.CTkLabel(card, text=text, font=FONTS["body"], text_color=COLORS["text_muted"], wraplength=900, justify="left").pack(fill="x", padx=18, pady=(0, 15))

class AgendaPanel(WorkspacePanel):
    def __init__(self, parent, case_manager=None, **kwargs):
        super().__init__(parent, "Agenda", "Vista operativa de fechas de seguimiento registradas en los expedientes.", **kwargs)
        self.case_manager = case_manager; self.list = ctk.CTkScrollableFrame(self.body, fg_color="transparent"); self.list.pack(fill="both", expand=True); self.refresh()
    def refresh(self):
        for w in self.list.winfo_children(): w.destroy()
        cases = self.case_manager.get_all_cases() if self.case_manager else []; dated = sorted([c for c in cases if c.follow_up_date], key=lambda c: c.follow_up_date or "")
        if not dated:
            ctk.CTkLabel(self.list, text="No hay fechas de seguimiento registradas.", font=FONTS["body"], text_color=COLORS["text_muted"]).pack(anchor="w", padx=10, pady=18); return
        for case in dated:
            card = ctk.CTkFrame(self.list, fg_color=COLORS["surface"], corner_radius=12, border_width=1, border_color=COLORS["border"]); card.pack(fill="x", pady=5)
            ctk.CTkLabel(card, text=case.follow_up_date, font=FONTS["heading"], text_color=COLORS["primary"], width=120).pack(side="left", padx=14, pady=14)
            ctk.CTkLabel(card, text=f"{case.case_number} · {case.status}", font=FONTS["small_bold"], text_color=COLORS["text"]).pack(side="left", padx=5)
