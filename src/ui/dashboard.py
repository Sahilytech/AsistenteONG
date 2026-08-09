"""Inicio: dashboard visual, estado local y búsqueda oficial con memoria."""
import customtkinter as ctk
import logging
import threading
import webbrowser
from .styles import COLORS, FONTS
from ..knowledge.memory import LocalMemory
from ..knowledge.official_web import OFFICIAL_SOURCES, search_official, internet_available
logger = logging.getLogger(__name__)

class DashboardFrame(ctk.CTkFrame):
    def __init__(self, parent, case_manager=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.case_manager = case_manager
        self.memory = LocalMemory()
        self.stats = {"total": 0, "por_urgencia": {}, "por_status": {}}
        self._search_running = False
        self._setup_ui(); self.refresh()

    def _setup_ui(self):
        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll.pack(fill="both", expand=True, padx=20, pady=18)
        ctk.CTkLabel(self.scroll, text="Resumen general", font=FONTS["title"], text_color=COLORS["text"]).pack(anchor="w")
        ctk.CTkLabel(self.scroll, text="Una vista rápida de casos, actividad, memoria local y fuentes oficiales.", font=FONTS["body"], text_color=COLORS["text_muted"]).pack(anchor="w", pady=(3,16))
        self.cards = ctk.CTkFrame(self.scroll, fg_color="transparent"); self.cards.pack(fill="x", pady=(0,16))
        for i in range(5): self.cards.grid_columnconfigure(i, weight=1, uniform="metric")
        self.metric_labels=[]
        for i,(title,sub) in enumerate([("Casos","registrados"),("Abiertos","requieren atención"),("Prioridad alta","revisión"),("Memoria","fuentes guardadas"),("Estado","conectividad")]):
            card=ctk.CTkFrame(self.cards, fg_color=COLORS["surface_alt"], corner_radius=15, border_width=1, border_color=COLORS["border"]); card.grid(row=0,column=i,sticky="nsew",padx=5)
            ctk.CTkLabel(card,text=title,font=FONTS["small_bold"],text_color=COLORS["text_muted"]).pack(anchor="w",padx=15,pady=(13,2)); value=ctk.CTkLabel(card,text="0",font=("Helvetica",23,"bold"),text_color=COLORS["primary"]); value.pack(anchor="w",padx=15); ctk.CTkLabel(card,text=sub,font=FONTS["tiny"],text_color=COLORS["text_soft"]).pack(anchor="w",padx=15,pady=(0,12)); self.metric_labels.append(value)
        body=ctk.CTkFrame(self.scroll,fg_color="transparent"); body.pack(fill="both",expand=True); body.grid_columnconfigure(0,weight=3); body.grid_columnconfigure(1,weight=2)
        self._build_cases(body); self._build_system(body); self._build_search(body); self._build_quick(body)

    def _card(self,parent,row,column,title):
        card=ctk.CTkFrame(parent,fg_color=COLORS["surface"],corner_radius=16,border_width=1,border_color=COLORS["border"]); card.grid(row=row,column=column,sticky="nsew",padx=6,pady=6); ctk.CTkLabel(card,text=title,font=FONTS["heading"],text_color=COLORS["text"]).pack(anchor="w",padx=17,pady=(15,10)); return card
    def _build_cases(self,parent):
        card=self._card(parent,0,0,"Últimos casos"); self.cases_box=ctk.CTkScrollableFrame(card,height=220,fg_color="transparent"); self.cases_box.pack(fill="both",expand=True,padx=8,pady=(0,10))
    def _build_system(self,parent):
        card=self._card(parent,0,1,"Estado del sistema"); self.connection=ctk.CTkLabel(card,text="● Comprobando conexión...",font=FONTS["body_bold"],text_color=COLORS["primary"]); self.connection.pack(anchor="w",padx=17,pady=(0,6)); ctk.CTkLabel(card,text="Procesamiento principal: local",font=FONTS["small"],text_color=COLORS["text_muted"]).pack(anchor="w",padx=17,pady=3); self.memory_status=ctk.CTkLabel(card,text="Memoria local: 0 fuentes",font=FONTS["small"],text_color=COLORS["text_muted"]); self.memory_status.pack(anchor="w",padx=17,pady=3); ctk.CTkLabel(card,text="Fuentes oficiales configuradas",font=FONTS["small_bold"],text_color=COLORS["text"]).pack(anchor="w",padx=17,pady=(14,5)); ctk.CTkLabel(card,text=" · ".join(list(OFFICIAL_SOURCES.values())[:4]),font=FONTS["tiny"],text_color=COLORS["primary"],wraplength=330,justify="left").pack(anchor="w",padx=17,pady=(0,14))
    def _build_search(self,parent):
        card=self._card(parent,1,0,"Búsqueda inteligente"); ctk.CTkLabel(card,text="Internet oficial + memoria local",font=FONTS["small"],text_color=COLORS["text_muted"]).pack(anchor="w",padx=17,pady=(0,8)); row=ctk.CTkFrame(card,fg_color="transparent"); row.pack(fill="x",padx=17); self.search_entry=ctk.CTkEntry(row,height=38,placeholder_text="Ej.: refugios, salud, violencia..."); self.search_entry.pack(side="left",fill="x",expand=True); self.search_button=ctk.CTkButton(row,text="Buscar",width=86,height=38,fg_color=COLORS["primary"],hover_color=COLORS["primary_dark"],command=self.run_search); self.search_button.pack(side="left",padx=(8,0)); self.search_entry.bind("<Return>",lambda e:self.run_search()); self.search_status=ctk.CTkLabel(card,text="Solo se consultan dominios oficiales configurados.",font=FONTS["tiny"],text_color=COLORS["text_muted"]); self.search_status.pack(anchor="w",padx=17,pady=(7,3)); self.results_box=ctk.CTkScrollableFrame(card,height=185,fg_color=COLORS["surface_alt"]); self.results_box.pack(fill="both",expand=True,padx=12,pady=(2,12))
    def _build_quick(self,parent):
        card=self._card(parent,1,1,"Acciones rápidas")
        for title,sub,target in [("Nuevo caso","Analizar un relato","__new__"),("Casos","Buscar y filtrar","Casos"),("Informe","Crear informe social","Informe Social"),("Recursos","Consultar recursos","Recursos")]:
            command=self._new_case if target=="__new__" else lambda t=target:self._go(t); ctk.CTkButton(card,text=f"{title}\n{sub}",height=48,anchor="w",fg_color=COLORS["surface_alt"],hover_color=COLORS["primary_soft"],text_color=COLORS["text"],border_width=1,border_color=COLORS["border"],command=command).pack(fill="x",padx=15,pady=4)
    def _go(self,tab):
        root=self.winfo_toplevel()
        if hasattr(root,"select_tab"): root.select_tab(tab)
    def _new_case(self):
        root=self.winfo_toplevel()
        if hasattr(root,"open_new_case"): root.open_new_case()

    def run_search(self):
        query=self.search_entry.get().strip()
        if not query or self._search_running:return
        self._search_running=True
        self.search_button.configure(state="disabled",text="Buscando…")
        self.search_status.configure(text="Consultando fuentes oficiales… la interfaz sigue disponible.",text_color=COLORS["primary"])
        for child in self.results_box.winfo_children(): child.destroy()
        ctk.CTkLabel(self.results_box,text="Buscando en fuentes oficiales y memoria local…",font=FONTS["small"],text_color=COLORS["text_muted"]).pack(anchor="w",padx=10,pady=12)
        threading.Thread(target=self._search_worker,args=(query,),daemon=True).start()

    def _search_worker(self,query):
        try:
            results,online=search_official(query,self.memory,limit=8)
            self.after(0,lambda:self._show_search_results(results,online))
        except Exception as exc:
            logger.error("Error de búsqueda: %s",exc,exc_info=True)
            self.after(0,lambda:self._finish_search_error())

    def _finish_search_error(self):
        self._search_running=False
        self.search_button.configure(state="normal",text="Buscar")
        self.search_status.configure(text="No fue posible consultar las fuentes. La aplicación continúa offline.",text_color=COLORS["warning"])

    def _show_search_results(self,results,online):
        self._search_running=False
        self.search_button.configure(state="normal",text="Buscar")
        self.search_status.configure(text=("Conectado: resultados oficiales guardados en memoria local." if online else "Sin conexión: mostrando memoria local."),text_color=COLORS["success"] if online else COLORS["warning"])
        for child in self.results_box.winfo_children(): child.destroy()
        if not results:
            ctk.CTkLabel(self.results_box,text="No hay resultados para esta búsqueda en las fuentes disponibles.",font=FONTS["small"],text_color=COLORS["text_muted"],wraplength=620,justify="left").pack(anchor="w",padx=10,pady=12)
            return
        for result in results:
            item=ctk.CTkFrame(self.results_box,fg_color=COLORS["surface"],corner_radius=10,border_width=1,border_color=COLORS["border"]); item.pack(fill="x",padx=3,pady=4)
            ctk.CTkLabel(item,text=result.title,font=FONTS["small_bold"],text_color=COLORS["primary"],anchor="w",justify="left",wraplength=650).pack(fill="x",padx=10,pady=(8,1))
            ctk.CTkLabel(item,text=result.snippet,font=FONTS["tiny"],text_color=COLORS["text_muted"],anchor="w",justify="left",wraplength=650).pack(fill="x",padx=10,pady=(0,3))
            ctk.CTkButton(item,text=result.domain,width=120,height=24,fg_color=COLORS["primary_soft"],hover_color=COLORS["primary"],text_color=COLORS["primary"],command=lambda u=result.url:webbrowser.open(u)).pack(anchor="e",padx=10,pady=(0,7))

    def refresh(self):
        try:
            if self.case_manager:self.stats=self.case_manager.get_statistics()
            total=self.stats.get("total",0); open_count=sum(v for k,v in self.stats.get("por_status",{}).items() if str(k).lower() not in {"cerrado","cerrada"}); high=sum(v for k,v in self.stats.get("por_urgencia",{}).items() if str(k).lower() in {"alta","muy alta","urgente"}); self.metric_labels[0].configure(text=str(total)); self.metric_labels[1].configure(text=str(open_count)); self.metric_labels[2].configure(text=str(high)); self.metric_labels[3].configure(text=str(self.memory.count())); online=internet_available(); self.metric_labels[4].configure(text="ONLINE" if online else "OFFLINE"); self.connection.configure(text=("● Internet disponible" if online else "● Modo offline"),text_color=COLORS["success"] if online else COLORS["warning"]); self.memory_status.configure(text=f"Memoria local: {self.memory.count()} fuentes")
            for child in self.cases_box.winfo_children():child.destroy()
            cases=self.case_manager.get_all_cases()[:6] if self.case_manager else []
            if not cases: ctk.CTkLabel(self.cases_box,text="Todavía no hay casos registrados.",font=FONTS["small"],text_color=COLORS["text_muted"]).pack(anchor="w",padx=10,pady=15)
            for case in cases:
                row=ctk.CTkFrame(self.cases_box,fg_color=COLORS["surface_alt"],corner_radius=9); row.pack(fill="x",pady=3); ctk.CTkLabel(row,text=case.case_number,font=FONTS["small_bold"],text_color=COLORS["text"],width=150,anchor="w").pack(side="left",padx=9,pady=8); ctk.CTkLabel(row,text=str(case.text).replace("\n"," ")[:62],font=FONTS["tiny"],text_color=COLORS["text_muted"],anchor="w").pack(side="left",fill="x",expand=True,pady=8); ctk.CTkLabel(row,text=str(case.urgency).upper(),font=FONTS["tiny"],text_color=COLORS["primary"],width=75).pack(side="right",padx=8)
        except Exception as exc: logger.error("Error actualizando dashboard: %s",exc,exc_info=True)
    def update_stats(self, urgency: str, category: str, case_number: str): self.refresh()
