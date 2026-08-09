"""Dashboard profesional y 100% offline para Asistente ONG."""
import logging
import customtkinter as ctk
from .styles import COLORS, FONTS
from ..knowledge.memory import LocalMemory
from ..resources_data import search_resources

logger = logging.getLogger(__name__)


class DashboardFrame(ctk.CTkFrame):
    """Panel principal: métricas locales, casos recientes y búsqueda offline."""

    def __init__(self, parent, case_manager=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.case_manager = case_manager
        self.memory = LocalMemory()
        self.stats = {"total": 0, "por_urgencia": {}, "por_status": {}}
        self._setup_ui()
        self.refresh()

    def _setup_ui(self):
        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll.pack(fill="both", expand=True, padx=24, pady=22)

        ctk.CTkLabel(self.scroll, text="Panel principal", font=FONTS["title"], text_color=COLORS["text"]).pack(anchor="w")
        ctk.CTkLabel(
            self.scroll,
            text="Todo lo que ves y procesás acá permanece en este equipo. No requiere Internet ni servicios externos.",
            font=FONTS["body"], text_color=COLORS["text_muted"], wraplength=900, justify="left"
        ).pack(anchor="w", pady=(4, 18))

        metrics = ctk.CTkFrame(self.scroll, fg_color="transparent")
        metrics.pack(fill="x", pady=(0, 16))
        for i in range(4):
            metrics.grid_columnconfigure(i, weight=1, uniform="metric")
        self.metric_labels = []
        definitions = [
            ("Casos", "registrados"),
            ("Abiertos", "requieren atención"),
            ("Prioridad alta", "para revisar"),
            ("Memoria local", "fuentes guardadas"),
        ]
        for i, (title, subtitle) in enumerate(definitions):
            card = ctk.CTkFrame(metrics, fg_color=COLORS["surface_alt"], corner_radius=15,
                                border_width=1, border_color=COLORS["border"])
            card.grid(row=0, column=i, sticky="nsew", padx=5)
            ctk.CTkLabel(card, text=title, font=FONTS["small_bold"], text_color=COLORS["text_muted"]).pack(anchor="w", padx=15, pady=(13, 2))
            value = ctk.CTkLabel(card, text="0", font=("Helvetica", 23, "bold"), text_color=COLORS["primary"])
            value.pack(anchor="w", padx=15)
            ctk.CTkLabel(card, text=subtitle, font=FONTS["tiny"], text_color=COLORS["text_soft"]).pack(anchor="w", padx=15, pady=(0, 12))
            self.metric_labels.append(value)

        body = ctk.CTkFrame(self.scroll, fg_color="transparent")
        body.pack(fill="both", expand=True)
        body.grid_columnconfigure(0, weight=3)
        body.grid_columnconfigure(1, weight=2)
        self._build_cases(body)
        self._build_system(body)
        self._build_search(body)
        self._build_quick(body)

    def _card(self, parent, row, column, title):
        card = ctk.CTkFrame(parent, fg_color=COLORS["surface"], corner_radius=16,
                            border_width=1, border_color=COLORS["border"])
        card.grid(row=row, column=column, sticky="nsew", padx=6, pady=6)
        ctk.CTkLabel(card, text=title, font=FONTS["heading"], text_color=COLORS["text"]).pack(anchor="w", padx=17, pady=(15, 10))
        return card

    def _build_cases(self, parent):
        card = self._card(parent, 0, 0, "Actividad reciente")
        self.cases_box = ctk.CTkScrollableFrame(card, height=220, fg_color="transparent")
        self.cases_box.pack(fill="both", expand=True, padx=8, pady=(0, 10))

    def _build_system(self, parent):
        card = self._card(parent, 0, 1, "Privacidad y almacenamiento")
        ctk.CTkLabel(card, text="● MODO OFFLINE", font=FONTS["body_bold"], text_color=COLORS["success"]).pack(anchor="w", padx=17, pady=(0, 7))
        ctk.CTkLabel(card, text="Sin consultas de red", font=FONTS["small"], text_color=COLORS["text_muted"]).pack(anchor="w", padx=17, pady=3)
        ctk.CTkLabel(card, text="Procesamiento: este equipo", font=FONTS["small"], text_color=COLORS["text_muted"]).pack(anchor="w", padx=17, pady=3)
        self.memory_status = ctk.CTkLabel(card, text="Memoria local: 0 fuentes", font=FONTS["small"], text_color=COLORS["text_muted"])
        self.memory_status.pack(anchor="w", padx=17, pady=3)
        ctk.CTkLabel(card, text="Los datos de casos no se envían automáticamente.", font=FONTS["tiny"],
                     text_color=COLORS["text_soft"], wraplength=330, justify="left").pack(anchor="w", padx=17, pady=(12, 14))

    def _build_search(self, parent):
        card = self._card(parent, 1, 0, "Búsqueda local")
        ctk.CTkLabel(card, text="Casos, recursos y memoria guardada en este equipo",
                     font=FONTS["small"], text_color=COLORS["text_muted"]).pack(anchor="w", padx=17, pady=(0, 8))
        row = ctk.CTkFrame(card, fg_color="transparent")
        row.pack(fill="x", padx=17)
        self.search_entry = ctk.CTkEntry(row, height=38, placeholder_text="Buscar recursos o información guardada...")
        self.search_entry.pack(side="left", fill="x", expand=True)
        ctk.CTkButton(row, text="Buscar", width=86, height=38, fg_color=COLORS["primary"],
                      hover_color=COLORS["primary_dark"], command=self.run_search).pack(side="left", padx=(8, 0))
        self.search_entry.bind("<Return>", lambda _: self.run_search())
        self.search_status = ctk.CTkLabel(card, text="La búsqueda nunca sale de este equipo.", font=FONTS["tiny"], text_color=COLORS["text_muted"])
        self.search_status.pack(anchor="w", padx=17, pady=(7, 3))
        self.results_box = ctk.CTkScrollableFrame(card, height=185, fg_color=COLORS["surface_alt"])
        self.results_box.pack(fill="both", expand=True, padx=12, pady=(2, 12))

    def _build_quick(self, parent):
        card = self._card(parent, 1, 1, "Acciones rápidas")
        actions = [
            ("Nuevo caso", "Analizar un relato", "__new__"),
            ("Casos", "Buscar y filtrar", "Casos"),
            ("Informe", "Crear informe social", "Informe Social"),
            ("Recursos", "Consultar base local", "Recursos"),
        ]
        for title, subtitle, target in actions:
            command = self._new_case if target == "__new__" else lambda t=target: self._go(t)
            ctk.CTkButton(card, text=f"{title}\n{subtitle}", height=48, anchor="w",
                          fg_color=COLORS["surface_alt"], hover_color=COLORS["primary_soft"],
                          text_color=COLORS["text"], border_width=1, border_color=COLORS["border"],
                          command=command).pack(fill="x", padx=15, pady=4)

    def _go(self, tab):
        root = self.winfo_toplevel()
        if hasattr(root, "select_tab"):
            root.select_tab(tab)

    def _new_case(self):
        root = self.winfo_toplevel()
        if hasattr(root, "open_new_case"):
            root.open_new_case()

    def run_search(self):
        query = self.search_entry.get().strip()
        if not query:
            return
        for child in self.results_box.winfo_children():
            child.destroy()
        self.search_status.configure(text="Buscando únicamente en datos locales...", text_color=COLORS["primary"])
        results = []
        try:
            results.extend(search_resources(query)[:8])
        except Exception:
            logger.exception("Error buscando recursos locales")
        try:
            for item in self.memory.search(query, limit=8):
                results.append(item)
        except Exception:
            logger.exception("Error buscando memoria local")
        self.search_status.configure(text=f"Búsqueda local · {len(results)} resultado(s)", text_color=COLORS["success"] if results else COLORS["text_muted"])
        if not results:
            ctk.CTkLabel(self.results_box, text="No se encontraron coincidencias en la información local.",
                         font=FONTS["small"], text_color=COLORS["text_muted"], wraplength=620,
                         justify="left").pack(anchor="w", padx=10, pady=12)
            return
        for result in results:
            if isinstance(result, dict):
                title = result.get("nombre") or result.get("name") or result.get("title") or "Recurso local"
                detail = " · ".join(str(result.get(k, "")) for k in ("ciudad", "país", "horario", "teléfono", "numero", "especialidad") if result.get(k))
            else:
                title = str(result)
                detail = "Recurso local"
            item = ctk.CTkFrame(self.results_box, fg_color=COLORS["surface"], corner_radius=10,
                                border_width=1, border_color=COLORS["border"])
            item.pack(fill="x", padx=3, pady=4)
            ctk.CTkLabel(item, text=title, font=FONTS["small_bold"], text_color=COLORS["primary"],
                         anchor="w", justify="left", wraplength=650).pack(fill="x", padx=10, pady=(8, 1))
            ctk.CTkLabel(item, text=detail or "Información local", font=FONTS["tiny"], text_color=COLORS["text_muted"],
                         anchor="w", justify="left", wraplength=650).pack(fill="x", padx=10, pady=(0, 8))

    def refresh(self):
        try:
            if self.case_manager:
                self.stats = self.case_manager.get_statistics()
            total = self.stats.get("total", 0)
            open_count = sum(v for k, v in self.stats.get("por_status", {}).items()
                             if str(k).lower() not in {"cerrado", "cerrada"})
            high = sum(v for k, v in self.stats.get("por_urgencia", {}).items()
                       if str(k).lower() in {"alta", "muy alta", "urgente"})
            self.metric_labels[0].configure(text=str(total))
            self.metric_labels[1].configure(text=str(open_count))
            self.metric_labels[2].configure(text=str(high))
            self.metric_labels[3].configure(text=str(self.memory.count()))
            self.memory_status.configure(text=f"Memoria local: {self.memory.count()} fuentes")

            for child in self.cases_box.winfo_children():
                child.destroy()
            cases = self.case_manager.get_all_cases()[:6] if self.case_manager else []
            if not cases:
                ctk.CTkLabel(self.cases_box, text="Todavía no hay casos registrados.", font=FONTS["small"],
                             text_color=COLORS["text_muted"]).pack(anchor="w", padx=10, pady=15)
            for case in cases:
                row = ctk.CTkFrame(self.cases_box, fg_color=COLORS["surface_alt"], corner_radius=9)
                row.pack(fill="x", pady=3)
                ctk.CTkLabel(row, text=case.case_number, font=FONTS["small_bold"], text_color=COLORS["text"],
                             width=150, anchor="w").pack(side="left", padx=9, pady=8)
                ctk.CTkLabel(row, text=str(case.text).replace("\n", " ")[:80], font=FONTS["tiny"],
                             text_color=COLORS["text_muted"], anchor="w", justify="left").pack(side="left", fill="x", expand=True, pady=8)
                ctk.CTkLabel(row, text=str(case.urgency).upper(), font=FONTS["tiny"],
                             text_color=COLORS["primary"], width=75).pack(side="right", padx=8)
        except Exception as exc:
            logger.error("Error actualizando dashboard: %s", exc, exc_info=True)

    def update_stats(self, urgency: str, category: str, case_number: str):
        self.refresh()
