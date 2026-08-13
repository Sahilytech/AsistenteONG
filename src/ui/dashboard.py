"""Panel principal: estado del expediente, memoria y accesos rápidos."""
import logging
import customtkinter as ctk
from .styles import COLORS, FONTS, SPACING, CARD_RADIUS
from ..knowledge.memory import LocalMemory
from ..resources_data import search_resources
from ..knowledge.official_search import has_internet

logger = logging.getLogger(__name__)


class DashboardFrame(ctk.CTkFrame):
    def __init__(self, parent, case_manager=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.case_manager = case_manager
        self.memory = LocalMemory()
        self.stats = {"total": 0, "por_urgencia": {}, "por_status": {}}
        self._setup_ui()
        self.refresh()

    def _setup_ui(self):
        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll.pack(fill="both", expand=True, padx=26, pady=24)

        # Encabezado tipo producto: título + estado operativo.
        hero = ctk.CTkFrame(self.scroll, fg_color=COLORS["surface"], corner_radius=CARD_RADIUS,
                            border_width=1, border_color=COLORS["border"])
        hero.pack(fill="x", pady=(0, 18))
        left = ctk.CTkFrame(hero, fg_color="transparent")
        left.pack(side="left", fill="x", expand=True, padx=22, pady=20)
        ctk.CTkLabel(left, text="Centro de asistencia", font=FONTS["hero"],
                     text_color=COLORS["text"]).pack(anchor="w")
        ctk.CTkLabel(
            left,
            text="Todo el trabajo de la organización, ordenado en un solo espacio.",
            font=FONTS["body"], text_color=COLORS["text_muted"]
        ).pack(anchor="w", pady=(5, 2))
        ctk.CTkLabel(
            left,
            text="Casos · personas · evidencia · seguimiento · recursos",
            font=FONTS["small_bold"], text_color=COLORS["primary"]
        ).pack(anchor="w", pady=(3, 0))
        self.mode_badge = ctk.CTkLabel(
            hero, text="●  LOCAL FIRST", width=125, height=32, corner_radius=16,
            fg_color=COLORS["success_soft"], text_color=COLORS["success"],
            font=FONTS["small_bold"]
        )
        self.mode_badge.pack(side="right", padx=22, pady=22)

        metrics = ctk.CTkFrame(self.scroll, fg_color="transparent")
        metrics.pack(fill="x", pady=(0, 16))
        for i in range(4):
            metrics.grid_columnconfigure(i, weight=1, uniform="metric")
        self.metric_labels = []
        metric_data = [
            ("Casos", "registrados"),
            ("Abiertos", "requieren atención"),
            ("Prioridad alta", "para revisar"),
            ("Memoria local", "fuentes guardadas"),
        ]
        for i, (title, subtitle) in enumerate(metric_data):
            card = ctk.CTkFrame(metrics, fg_color=COLORS["surface"], corner_radius=CARD_RADIUS,
                                border_width=1, border_color=COLORS["border"])
            card.grid(row=0, column=i, sticky="nsew", padx=5)
            ctk.CTkLabel(card, text=title.upper(), font=FONTS["small_bold"],
                         text_color=COLORS["text_muted"]).pack(anchor="w", padx=17, pady=(14, 2))
            value = ctk.CTkLabel(card, text="0", font=FONTS["metric"], text_color=COLORS["primary"])
            value.pack(anchor="w", padx=17)
            ctk.CTkLabel(card, text=subtitle, font=FONTS["tiny"],
                         text_color=COLORS["text_soft"]).pack(anchor="w", padx=17, pady=(0, 14))
            self.metric_labels.append(value)

        body = ctk.CTkFrame(self.scroll, fg_color="transparent")
        body.pack(fill="both", expand=True)
        body.grid_columnconfigure(0, weight=3)
        body.grid_columnconfigure(1, weight=2)
        self._build_cases(body)
        self._build_system(body)
        self._build_search(body)
        self._build_quick(body)

    def _card(self, parent, row, column, title, subtitle=None):
        card = ctk.CTkFrame(parent, fg_color=COLORS["surface"], corner_radius=CARD_RADIUS,
                            border_width=1, border_color=COLORS["border"])
        card.grid(row=row, column=column, sticky="nsew", padx=6, pady=6)
        header = ctk.CTkFrame(card, fg_color="transparent")
        header.pack(fill="x", padx=18, pady=(15, 8))
        ctk.CTkLabel(header, text=title, font=FONTS["heading"],
                     text_color=COLORS["text"]).pack(anchor="w")
        if subtitle:
            ctk.CTkLabel(header, text=subtitle, font=FONTS["tiny"],
                         text_color=COLORS["text_muted"]).pack(anchor="w", pady=(2, 0))
        return card

    def _build_cases(self, parent):
        card = self._card(parent, 0, 0, "Actividad reciente", "Los últimos movimientos del sistema")
        self.cases_box = ctk.CTkScrollableFrame(card, height=235, fg_color="transparent")
        self.cases_box.pack(fill="both", expand=True, padx=9, pady=(0, 10))

    def _build_system(self, parent):
        card = self._card(parent, 0, 1, "Estado del sistema", "Privacidad y almacenamiento")
        self.connection = ctk.CTkLabel(card, text="", font=FONTS["body_bold"])
        self.connection.pack(anchor="w", padx=18, pady=(0, 8))
        ctk.CTkLabel(card, text="Procesamiento de casos: este equipo", font=FONTS["small"],
                     text_color=COLORS["text_muted"]).pack(anchor="w", padx=18, pady=3)
        self.memory_status = ctk.CTkLabel(card, text="Memoria local: 0 fuentes", font=FONTS["small"],
                                          text_color=COLORS["text_muted"])
        self.memory_status.pack(anchor="w", padx=18, pady=3)
        divider = ctk.CTkFrame(card, height=1, fg_color=COLORS["border"])
        divider.pack(fill="x", padx=18, pady=(13, 10))
        ctk.CTkLabel(
            card,
            text="La conexión se utiliza únicamente en funciones explícitas de fuentes oficiales. El relato del caso permanece local.",
            font=FONTS["tiny"], text_color=COLORS["text_soft"], wraplength=330, justify="left"
        ).pack(anchor="w", padx=18, pady=(0, 15))

    def _build_search(self, parent):
        card = self._card(parent, 1, 0, "Búsqueda local", "Encuentra información sin sacar el relato del equipo")
        row = ctk.CTkFrame(card, fg_color="transparent")
        row.pack(fill="x", padx=18, pady=(0, 7))
        self.search_entry = ctk.CTkEntry(
            row, height=40, corner_radius=10,
            placeholder_text="Buscar recursos, fuentes o información guardada..."
        )
        self.search_entry.pack(side="left", fill="x", expand=True)
        ctk.CTkButton(
            row, text="Buscar", width=90, height=40, corner_radius=10,
            fg_color=COLORS["primary"], hover_color=COLORS["primary_dark"],
            font=FONTS["body_bold"], command=self.run_search
        ).pack(side="left", padx=(8, 0))
        self.search_entry.bind("<Return>", lambda _: self.run_search())
        self.search_status = ctk.CTkLabel(
            card, text="La búsqueda local nunca sale de este equipo.", font=FONTS["tiny"],
            text_color=COLORS["text_muted"]
        )
        self.search_status.pack(anchor="w", padx=18, pady=(0, 6))
        self.results_box = ctk.CTkScrollableFrame(card, height=180, fg_color=COLORS["surface_alt"], corner_radius=12)
        self.results_box.pack(fill="both", expand=True, padx=12, pady=(2, 12))

    def _build_quick(self, parent):
        card = self._card(parent, 1, 1, "Acciones rápidas", "Atajos para el trabajo diario")
        actions = [
            ("Nuevo caso", "Ingresar un relato nuevo", "__new__"),
            ("Casos", "Buscar y filtrar expedientes", "Casos"),
            ("Caso + Informe", "Completar un informe social", "Caso + Informe"),
            ("Recursos", "Consultar fuentes verificadas", "Recursos"),
        ]
        for title, subtitle, target in actions:
            command = self._new_case if target == "__new__" else lambda t=target: self._go(t)
            button = ctk.CTkButton(
                card, text=f"{title}\n{subtitle}", height=53, anchor="w", corner_radius=11,
                fg_color=COLORS["surface_alt"], hover_color=COLORS["primary_soft"],
                text_color=COLORS["text"], border_width=1, border_color=COLORS["border"],
                font=FONTS["body_bold"], command=command
            )
            button.pack(fill="x", padx=15, pady=4)

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
            results.extend(self.memory.search(query, limit=8))
        except Exception:
            logger.exception("Error buscando memoria local")
        self.search_status.configure(
            text=f"Búsqueda local · {len(results)} resultado(s)",
            text_color=COLORS["success"] if results else COLORS["text_muted"]
        )
        if not results:
            ctk.CTkLabel(
                self.results_box, text="No se encontraron coincidencias en la información local.",
                font=FONTS["small"], text_color=COLORS["text_muted"], wraplength=620, justify="left"
            ).pack(anchor="w", padx=12, pady=15)
            return
        for result in results:
            if isinstance(result, dict):
                title = result.get("nombre") or result.get("name") or result.get("title") or "Recurso local"
                detail = " · ".join(
                    str(result.get(k, "")) for k in
                    ("ciudad", "país", "horario", "teléfono", "numero", "especialidad", "domain")
                    if result.get(k)
                )
            else:
                title, detail = str(result), "Recurso local"
            item = ctk.CTkFrame(
                self.results_box, fg_color=COLORS["surface"], corner_radius=10,
                border_width=1, border_color=COLORS["border"]
            )
            item.pack(fill="x", padx=3, pady=4)
            ctk.CTkLabel(
                item, text=title, font=FONTS["small_bold"], text_color=COLORS["primary"],
                anchor="w", justify="left", wraplength=650
            ).pack(fill="x", padx=11, pady=(8, 1))
            ctk.CTkLabel(
                item, text=detail or "Información local", font=FONTS["tiny"],
                text_color=COLORS["text_muted"], anchor="w", justify="left", wraplength=650
            ).pack(fill="x", padx=11, pady=(0, 8))

    def refresh(self):
        try:
            if self.case_manager:
                self.stats = self.case_manager.get_statistics()
            total = self.stats.get("total", 0)
            open_count = sum(
                v for k, v in self.stats.get("por_status", {}).items()
                if str(k).lower() not in {"cerrado", "cerrada"}
            )
            high = sum(
                v for k, v in self.stats.get("por_urgencia", {}).items()
                if str(k).lower() in {"alta", "muy alta", "urgente"}
            )
            self.metric_labels[0].configure(text=str(total))
            self.metric_labels[1].configure(text=str(open_count))
            self.metric_labels[2].configure(text=str(high))
            self.metric_labels[3].configure(text=str(self.memory.count()))
            self.memory_status.configure(text=f"Memoria local: {self.memory.count()} fuentes")
            online = has_internet()
            self.connection.configure(
                text=("● CONECTIVIDAD DISPONIBLE" if online else "● MODO OFFLINE"),
                text_color=COLORS["primary"] if online else COLORS["success"]
            )
            self.mode_badge.configure(
                text="●  CONEXIÓN DISPONIBLE" if online else "●  LOCAL FIRST",
                text_color=COLORS["primary"] if online else COLORS["success"],
                fg_color=COLORS["primary_soft"] if online else COLORS["success_soft"]
            )
            for child in self.cases_box.winfo_children():
                child.destroy()
            cases = self.case_manager.get_all_cases()[:6] if self.case_manager else []
            if not cases:
                ctk.CTkLabel(
                    self.cases_box, text="Todavía no hay casos registrados.", font=FONTS["small"],
                    text_color=COLORS["text_muted"]
                ).pack(anchor="w", padx=10, pady=18)
            for case in cases:
                row = ctk.CTkFrame(self.cases_box, fg_color=COLORS["surface_alt"], corner_radius=10)
                row.pack(fill="x", pady=3)
                ctk.CTkLabel(
                    row, text=case.case_number, font=FONTS["small_bold"],
                    text_color=COLORS["text"], width=150, anchor="w"
                ).pack(side="left", padx=10, pady=9)
                ctk.CTkLabel(
                    row, text=str(case.text).replace("\n", " ")[:80], font=FONTS["tiny"],
                    text_color=COLORS["text_muted"], anchor="w", justify="left"
                ).pack(side="left", fill="x", expand=True, pady=9)
                ctk.CTkLabel(
                    row, text=str(case.urgency).upper(), font=FONTS["tiny"],
                    text_color=COLORS["primary"], width=75
                ).pack(side="right", padx=8)
        except Exception as exc:
            logger.error("Error actualizando dashboard: %s", exc, exc_info=True)

    def update_stats(self, urgency: str, category: str, case_number: str):
        self.refresh()
