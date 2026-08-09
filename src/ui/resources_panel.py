"""Panel de recursos: catálogo local verificable + consulta oficial opcional."""
import customtkinter as ctk
from .styles import COLORS, FONTS
from ..resources_data import RESOURCES_DATABASE
from ..knowledge.memory import LocalMemory
from ..knowledge.official_search import search_official, has_internet

class ResourcesPanel(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.memory = LocalMemory()
        self.all_items = []
        self._build_data()
        self._setup_ui()
        self._render()

    def _build_data(self):
        for key, data in RESOURCES_DATABASE.items():
            source = data.get("source", "")
            for item in data.get("locations", []):
                self.all_items.append({"category": data.get("name", key), "type": "Institución / servicio", "name": item.get("nombre", "Recurso"), "phone": item.get("teléfono", ""), "city": item.get("ciudad", ""), "hours": item.get("horario", ""), "extra": item.get("especialidades", item.get("tipo", "")), "source": source})
            for item in data.get("phone", []):
                self.all_items.append({"category": data.get("name", key), "type": "Línea telefónica", "name": item.get("nombre", item.get("especialidad", "Línea de ayuda")), "phone": item.get("numero", ""), "city": item.get("país", "Argentina"), "hours": "", "extra": item.get("especialidad", ""), "source": source})

    def _setup_ui(self):
        top = ctk.CTkFrame(self, fg_color="transparent"); top.pack(fill="x", padx=24, pady=(22, 8))
        ctk.CTkLabel(top, text="Recursos y fuentes", font=FONTS["title"], text_color=COLORS["text"]).pack(anchor="w")
        ctk.CTkLabel(top, text="Primero se consulta la base local. Si habilitás la búsqueda online, solo se muestran resultados de dominios oficiales permitidos.", font=FONTS["small"], text_color=COLORS["text_muted"], wraplength=980, justify="left").pack(anchor="w", pady=(4, 12))
        filters = ctk.CTkFrame(self, fg_color=COLORS["surface_alt"], corner_radius=12); filters.pack(fill="x", padx=24, pady=(0, 8))
        self.search = ctk.CTkEntry(filters, placeholder_text="Buscar por nombre, teléfono, ciudad o especialidad..."); self.search.pack(side="left", fill="x", expand=True, padx=10, pady=10); self.search.bind("<KeyRelease>", lambda e: self._render())
        self.category = ctk.CTkComboBox(filters, values=["Todas"] + sorted({x["category"] for x in self.all_items}), width=220, command=lambda _: self._render()); self.category.set("Todas"); self.category.pack(side="left", padx=10)
        self.type_filter = ctk.CTkComboBox(filters, values=["Todos", "Línea telefónica", "Institución / servicio"], width=170, command=lambda _: self._render()); self.type_filter.set("Todos"); self.type_filter.pack(side="left", padx=(0, 10))
        ctk.CTkButton(filters, text="Buscar oficial", width=120, command=self._online_search, fg_color=COLORS["primary"], hover_color=COLORS["primary_dark"]).pack(side="left", padx=(0, 8))
        ctk.CTkButton(filters, text="Limpiar", width=80, command=self._clear_filters, fg_color=COLORS["surface"], hover_color=COLORS["primary_soft"], text_color=COLORS["text"], border_width=1, border_color=COLORS["border"]).pack(side="left", padx=(0, 10))
        self.status = ctk.CTkLabel(self, text="", font=FONTS["tiny"], text_color=COLORS["text_muted"]); self.status.pack(anchor="w", padx=28, pady=(0, 2))
        self.count = ctk.CTkLabel(self, text="", font=FONTS["small"], text_color=COLORS["text_muted"]); self.count.pack(anchor="w", padx=28, pady=(0, 4))
        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent"); self.scroll.pack(fill="both", expand=True, padx=18, pady=(0, 18))

    def _clear_filters(self):
        self.search.delete(0, "end"); self.category.set("Todas"); self.type_filter.set("Todos"); self.status.configure(text=""); self._render()

    def _render(self):
        if not hasattr(self, "scroll"): return
        for w in self.scroll.winfo_children(): w.destroy()
        q = self.search.get().strip().lower() if hasattr(self, "search") else ""
        cat = self.category.get() if hasattr(self, "category") else "Todas"
        typ = self.type_filter.get() if hasattr(self, "type_filter") else "Todos"
        items = [x for x in self.all_items if (not q or q in str(x).lower()) and (cat == "Todas" or x["category"] == cat) and (typ == "Todos" or x["type"] == typ)]
        self.count.configure(text=f"{len(items)} recursos locales · todos con fuente oficial registrada")
        if not items:
            ctk.CTkLabel(self.scroll, text="No hay coincidencias en la base local. Probá una búsqueda oficial si hay conexión.", font=FONTS["body"], text_color=COLORS["text_muted"], wraplength=900, justify="left").pack(anchor="w", padx=12, pady=20)
        for x in items:
            card = ctk.CTkFrame(self.scroll, fg_color=COLORS["surface"], corner_radius=12, border_width=1, border_color=COLORS["border"]); card.pack(fill="x", padx=6, pady=6)
            left = ctk.CTkFrame(card, fg_color="transparent"); left.pack(side="left", fill="x", expand=True, padx=16, pady=12)
            ctk.CTkLabel(left, text=x["name"], font=FONTS["subheading"], text_color=COLORS["text"]).pack(anchor="w")
            ctk.CTkLabel(left, text=f"{x['category']} · {x['type']}", font=FONTS["tiny"], text_color=COLORS["primary"]).pack(anchor="w", pady=2)
            extra = ", ".join(x["extra"]) if isinstance(x["extra"], list) else str(x["extra"] or "")
            detail = " · ".join(v for v in [x["city"], x["hours"], extra] if v)
            ctk.CTkLabel(left, text=detail or "Información no especificada", font=FONTS["small"], text_color=COLORS["text_muted"], wraplength=760, justify="left").pack(anchor="w")
            source = ctk.CTkLabel(left, text=x["source"], font=FONTS["tiny"], text_color=COLORS["text_soft"], wraplength=760, justify="left"); source.pack(anchor="w", pady=(3, 0))
            if x["phone"]: ctk.CTkLabel(card, text=x["phone"], font=FONTS["heading"], text_color=COLORS["primary"]).pack(side="right", padx=18)

    def _online_search(self):
        query = self.search.get().strip()
        if not query:
            self.status.configure(text="Escribí qué recurso o información querés buscar.")
            return
        if not has_internet():
            self.status.configure(text="Sin conexión: se mantiene la búsqueda local.", text_color=COLORS["text_muted"])
            return
        self.status.configure(text="Consultando fuentes oficiales…", text_color=COLORS["primary"])
        self.update_idletasks()
        results = search_official(query)
        self.status.configure(text=f"{len(results)} resultado(s) oficial(es). Los enlaces pueden guardarse en la memoria local.", text_color=COLORS["success"] if results else COLORS["text_muted"])
        for w in self.scroll.winfo_children(): w.destroy()
        if not results:
            ctk.CTkLabel(self.scroll, text="No se encontraron resultados oficiales para esa búsqueda.", font=FONTS["body"], text_color=COLORS["text_muted"]).pack(anchor="w", padx=12, pady=20); return
        for result in results:
            card = ctk.CTkFrame(self.scroll, fg_color=COLORS["surface"], corner_radius=12, border_width=1, border_color=COLORS["border"]); card.pack(fill="x", padx=6, pady=6)
            ctk.CTkLabel(card, text=result["title"], font=FONTS["subheading"], text_color=COLORS["text"], anchor="w", wraplength=850, justify="left").pack(fill="x", padx=16, pady=(12, 3))
            ctk.CTkLabel(card, text=result["domain"], font=FONTS["tiny"], text_color=COLORS["primary"]).pack(anchor="w", padx=16)
            row = ctk.CTkFrame(card, fg_color="transparent"); row.pack(fill="x", padx=16, pady=(6, 12))
            ctk.CTkButton(row, text="Guardar en memoria local", height=32, command=lambda r=result: self._save_online(r), fg_color=COLORS["primary"], hover_color=COLORS["primary_dark"]).pack(side="left")
            ctk.CTkLabel(row, text=result["url"], font=FONTS["tiny"], text_color=COLORS["text_muted"], wraplength=700, justify="left").pack(side="left", padx=10)

    def _save_online(self, result):
        self.memory.save(result["url"], result["domain"], result["title"], "Fuente oficial consultada desde Asistente ONG")
        self.status.configure(text="Fuente guardada en la memoria local.", text_color=COLORS["success"])
