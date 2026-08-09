import customtkinter as ctk
from .styles import COLORS,FONTS

class WorkspacePanel(ctk.CTkFrame):
    def __init__(self,parent,title,subtitle,**kwargs):
        super().__init__(parent,**kwargs)
        self.grid_rowconfigure(0,weight=1); self.grid_columnconfigure(0,weight=1)
        scroll=ctk.CTkScrollableFrame(self,fg_color="transparent"); scroll.grid(row=0,column=0,sticky="nsew",padx=24,pady=22)
        ctk.CTkLabel(scroll,text=title,font=FONTS["title"],text_color=COLORS["text"]).pack(anchor="w")
        ctk.CTkLabel(scroll,text=subtitle,font=FONTS["small"],text_color=COLORS["text_muted"],wraplength=950,justify="left").pack(anchor="w",pady=(3,18))
        self.body=scroll
    def card(self,title,text,action=None):
        card=ctk.CTkFrame(self.body,fg_color=COLORS["surface_alt"],corner_radius=14,border_width=1,border_color=COLORS["border"]); card.pack(fill="x",pady=6)
        ctk.CTkLabel(card,text=title,font=FONTS["subheading"],text_color=COLORS["text"],anchor="w").pack(fill="x",padx=18,pady=(14,4))
        ctk.CTkLabel(card,text=text,font=FONTS["small"],text_color=COLORS["text_muted"],wraplength=900,justify="left",anchor="w").pack(fill="x",padx=18,pady=(0,12))
        if action: ctk.CTkButton(card,text=action,height=32,fg_color=COLORS["primary"],hover_color=COLORS["primary_dark"]).pack(anchor="e",padx=18,pady=(0,14))

class CasesPanel(ctk.CTkFrame):
    def __init__(self,parent,case_manager=None,**kwargs):
        super().__init__(parent,**kwargs); self.case_manager=case_manager; self.all_cases=[]
        self.grid_rowconfigure(1,weight=0); self.grid_rowconfigure(2,weight=1); self.grid_columnconfigure(0,weight=1)
        head=ctk.CTkFrame(self,fg_color="transparent"); head.grid(row=0,column=0,sticky="ew",padx=24,pady=(22,10)); head.grid_columnconfigure(0,weight=1)
        ctk.CTkLabel(head,text="Casos",font=FONTS["title"],text_color=COLORS["text"]).grid(row=0,column=0,sticky="w")
        self.count_label=ctk.CTkLabel(head,text="0 registrados",font=FONTS["small"],text_color=COLORS["text_muted"]); self.count_label.grid(row=1,column=0,sticky="w",pady=(3,0))
        ctk.CTkButton(head,text="＋ Nuevo caso",width=125,height=36,fg_color=COLORS["primary"],hover_color=COLORS["primary_dark"],command=self._new_case).grid(row=0,column=1,rowspan=2,padx=(10,0))
        tools=ctk.CTkFrame(self,fg_color=COLORS["surface_alt"],corner_radius=14,border_width=1,border_color=COLORS["border"]); tools.grid(row=1,column=0,sticky="ew",padx=24,pady=(0,10)); tools.grid_columnconfigure(0,weight=1)
        row=ctk.CTkFrame(tools,fg_color="transparent"); row.grid(row=0,column=0,sticky="ew",padx=12,pady=12); row.grid_columnconfigure(0,weight=1)
        self.search=ctk.CTkEntry(row,height=38,placeholder_text="Buscar por ID, relato, palabra clave o responsable..."); self.search.grid(row=0,column=0,sticky="ew"); self.search.bind("<KeyRelease>",lambda e:self.refresh())
        self.urgency=ctk.CTkOptionMenu(row,width=125,height=38,values=["Todas","Muy Alta","Alta","Media","Baja"],command=lambda _:self.refresh(),fg_color=COLORS["surface"],button_color=COLORS["primary"],text_color=COLORS["text"]); self.urgency.grid(row=0,column=1,padx=(8,0))
        self.status=ctk.CTkOptionMenu(row,width=145,height=38,values=["Todos","nuevo","en análisis","revisado","derivado","en seguimiento","cerrado"],command=lambda _:self.refresh(),fg_color=COLORS["surface"],button_color=COLORS["primary"],text_color=COLORS["text"]); self.status.grid(row=0,column=2,padx=(8,0))
        ctk.CTkButton(row,text="Limpiar",width=72,height=38,fg_color=COLORS["surface"],hover_color=COLORS["primary_soft"],text_color=COLORS["text"],border_width=1,border_color=COLORS["border"],command=self.clear_filters).grid(row=0,column=3,padx=(8,0))
        self.list_frame=ctk.CTkScrollableFrame(self,fg_color="transparent"); self.list_frame.grid(row=2,column=0,sticky="nsew",padx=24,pady=(0,20))
        self.refresh()
    def _new_case(self):
        root=self.winfo_toplevel()
        if hasattr(root,"open_new_case"): root.open_new_case()
    def clear_filters(self):
        self.search.delete(0,"end"); self.urgency.set("Todas"); self.status.set("Todos"); self.refresh()
    def refresh(self):
        self.all_cases=self.case_manager.get_all_cases() if self.case_manager else []
        query=self.search.get().strip().lower(); urgency=self.urgency.get().lower(); status=self.status.get().lower()
        filtered=[]
        for case in self.all_cases:
            hay=" ".join([case.case_number,case.text,case.assigned_to," ".join(case.keywords)]).lower()
            if query and query not in hay: continue
            if urgency!="todas" and str(case.urgency).lower()!=urgency: continue
            if status!="todos" and str(case.status).lower()!=status: continue
            filtered.append(case)
        for child in self.list_frame.winfo_children(): child.destroy()
        self.count_label.configure(text=f"{len(filtered)} de {len(self.all_cases)} registrados")
        if not filtered:
            empty=ctk.CTkFrame(self.list_frame,fg_color=COLORS["surface_alt"],corner_radius=16,border_width=1,border_color=COLORS["border"]); empty.pack(fill="x",pady=8)
            title="No hay casos registrados." if not self.all_cases else "No se encontraron casos."
            detail="Los casos que crees aparecerán acá." if not self.all_cases else "Probá cambiar la búsqueda o los filtros."
            ctk.CTkLabel(empty,text=title,font=FONTS["heading"],text_color=COLORS["text"]).pack(pady=(28,5)); ctk.CTkLabel(empty,text=detail,font=FONTS["small"],text_color=COLORS["text_muted"],wraplength=620,justify="center").pack(padx=20,pady=(0,28)); return
        for case in filtered: self._case_card(case)
    def _case_card(self,case):
        card=ctk.CTkFrame(self.list_frame,fg_color=COLORS["surface"],corner_radius=14,border_width=1,border_color=COLORS["border"]); card.pack(fill="x",pady=5); card.grid_columnconfigure(1,weight=1); card.grid_columnconfigure(2,weight=0)
        ctk.CTkLabel(card,text=case.case_number,font=FONTS["subheading"],text_color=COLORS["primary"],anchor="w").grid(row=0,column=0,sticky="w",padx=16,pady=(14,3))
        ctk.CTkLabel(card,text=str(case.urgency).upper(),font=FONTS["tiny"],text_color=COLORS["primary"],fg_color=COLORS["primary_soft"],corner_radius=7).grid(row=0,column=2,sticky="e",padx=16,pady=(12,3))
        ctk.CTkLabel(card,text=str(case.status).replace("_"," ").title(),font=FONTS["tiny"],text_color=COLORS["text_muted"]).grid(row=1,column=0,sticky="w",padx=16,pady=(0,10))
        ctk.CTkLabel(card,text=str(case.created_at)[:16].replace("T"," "),font=FONTS["tiny"],text_color=COLORS["text_soft"]).grid(row=1,column=2,sticky="e",padx=16,pady=(0,10))
        text=str(case.text).replace("\n"," ").strip(); body=ctk.CTkLabel(card,text=text,font=FONTS["small"],text_color=COLORS["text"],anchor="w",justify="left",wraplength=650); body.grid(row=0,column=1,rowspan=2,sticky="ew",padx=14,pady=12)
        ctk.CTkButton(card,text="Abrir",width=72,height=30,fg_color=COLORS["surface_alt"],hover_color=COLORS["primary_soft"],text_color=COLORS["primary"],border_width=1,border_color=COLORS["border"],command=lambda c=case:self.open_case(c)).grid(row=0,column=3,rowspan=2,padx=(0,12))
        card.bind("<Configure>",lambda e,b=body:b.configure(wraplength=max(280,e.width-310)))
        for widget in (body,): widget.bind("<Button-1>",lambda e,c=case:self.open_case(c))
    def open_case(self,case):
        win=ctk.CTkToplevel(self.winfo_toplevel()); win.title(f"{case.case_number} · Asistente ONG"); win.geometry("760x680"); win.minsize(650,560); win.configure(fg_color=COLORS["background"]); win.transient(self.winfo_toplevel())
        ctk.CTkLabel(win,text=case.case_number,font=FONTS["title"],text_color=COLORS["text"]).pack(anchor="w",padx=24,pady=(22,2)); ctk.CTkLabel(win,text=f"Creado: {case.created_at[:19].replace('T',' ')}  ·  Prioridad: {case.urgency}",font=FONTS["small"],text_color=COLORS["text_muted"]).pack(anchor="w",padx=24,pady=(0,14))
        scroll=ctk.CTkScrollableFrame(win,fg_color="transparent"); scroll.pack(fill="both",expand=True,padx=18,pady=0)
        self._detail_card(scroll,"RELATO ORIGINAL",case.text); self._detail_card(scroll,"PALABRAS CLAVE",", ".join(case.keywords) if case.keywords else "No se detectaron palabras clave."); self._detail_card(scroll,"ESTADO",str(case.status).replace("_"," ").title()); self._detail_card(scroll,"RESPONSABLE",case.assigned_to or "Sin asignar"); self._detail_card(scroll,"SEGUIMIENTO",case.follow_up_date or "Sin fecha de seguimiento"); self._detail_card(scroll,"NOTAS",case.notes or "Sin notas registradas.")
    def _detail_card(self,parent,title,text):
        card=ctk.CTkFrame(parent,fg_color=COLORS["surface_alt"],corner_radius=12,border_width=1,border_color=COLORS["border"]); card.pack(fill="x",pady=5); ctk.CTkLabel(card,text=title,font=FONTS["small_bold"],text_color=COLORS["primary"]).pack(anchor="w",padx=16,pady=(12,4)); ctk.CTkLabel(card,text=text,font=FONTS["small"],text_color=COLORS["text"],justify="left",anchor="w",wraplength=680).pack(fill="x",padx=16,pady=(0,14))

class FollowUpPanel(WorkspacePanel):
    def __init__(self,parent,case_manager=None,**kwargs):
        super().__init__(parent,"Seguimiento","Organizá próximas acciones, derivaciones y revisiones.",**kwargs); self.case_manager=case_manager
        cases=self.case_manager.get_all_cases() if self.case_manager else []; pending=[c for c in cases if c.status.lower() not in {"cerrado","cerrada"}]
        self.card("Pendientes",f"{len(pending)} casos abiertos que requieren revisión.")
        self.card("Sin fecha de seguimiento",f"{sum(1 for c in pending if not c.follow_up_date)} casos todavía no tienen una fecha asignada.")
        self.card("Historial","Abrí un caso desde la sección Casos para consultar su información registrada.")

class LibraryPanel(WorkspacePanel):
    def __init__(self,parent,**kwargs):
        super().__init__(parent,"Biblioteca local","Documentos y materiales internos que la organización puede consultar sin conexión.",**kwargs)
        self.card("Protocolos","Guardá procedimientos internos, guías y documentos de referencia.","Agregar documento")
        self.card("Plantillas","Organizá plantillas para informes, derivaciones y comunicaciones.","Administrar plantillas")
        self.card("Búsqueda","La biblioteca está preparada para indexar contenido local y permitir consultas sin conexión.")

class SecurityPanel(WorkspacePanel):
    def __init__(self,parent,**kwargs):
        super().__init__(parent,"Privacidad y seguridad","Controles locales para proteger la información de los casos.",**kwargs)
        self.card("Estado","Modo offline-first · almacenamiento local · sin envío automático de casos.")
        self.card("Bloqueo de sesión","Configurá un bloqueo local para impedir acceso accidental al equipo.","Configurar bloqueo")
        self.card("Copias de seguridad","Creá y restaurá copias de la información de la organización según su política interna.","Gestionar copias")
        self.card("Auditoría","Consultá acciones administrativas sin almacenar innecesariamente el contenido sensible de los relatos.","Abrir registro")

class AgendaPanel(WorkspacePanel):
    def __init__(self,parent,**kwargs):
        super().__init__(parent,"Agenda","Vista rápida de tareas y fechas de seguimiento locales.",**kwargs)
        self.card("Hoy","Revisá las tareas y seguimientos que correspondan a la fecha actual.")
        self.card("Esta semana","Organizá revisiones, entrevistas e informes pendientes.")
        self.card("Próximas fechas","Preparado para integrar recordatorios con los casos locales.")
