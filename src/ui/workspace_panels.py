import customtkinter as ctk
from .styles import COLORS,FONTS

class WorkspacePanel(ctk.CTkFrame):
    def __init__(self,parent,title,subtitle,**kwargs):
        super().__init__(parent,**kwargs)
        scroll=ctk.CTkScrollableFrame(self,fg_color="transparent"); scroll.pack(fill="both",expand=True,padx=24,pady=20)
        ctk.CTkLabel(scroll,text=title,font=FONTS["title"],text_color=COLORS["text"]).pack(anchor="w")
        ctk.CTkLabel(scroll,text=subtitle,font=FONTS["small"],text_color=COLORS["text_muted"],wraplength=950,justify="left").pack(anchor="w",pady=(3,18))
        self.body=scroll
    def card(self,title,text,action=None):
        card=ctk.CTkFrame(self.body,fg_color=COLORS["surface_alt"],corner_radius=14); card.pack(fill="x",pady=6)
        ctk.CTkLabel(card,text=title,font=FONTS["subheading"],text_color=COLORS["text"]).pack(anchor="w",padx=18,pady=(14,4))
        ctk.CTkLabel(card,text=text,font=FONTS["small"],text_color=COLORS["text_muted"],wraplength=900,justify="left").pack(anchor="w",padx=18,pady=(0,12))
        if action: ctk.CTkButton(card,text=action,height=32,fg_color=COLORS["primary"],hover_color=COLORS["primary_dark"]).pack(anchor="e",padx=18,pady=(0,14))

class CasesPanel(WorkspacePanel):
    def __init__(self,parent,**kwargs):
        super().__init__(parent,"Gestión de casos","Buscá, filtrá y revisá casos almacenados localmente.",**kwargs)
        bar=ctk.CTkFrame(self.body,fg_color="transparent"); bar.pack(fill="x",pady=(0,12))
        ctk.CTkEntry(bar,placeholder_text="Buscar por ID, texto o etiqueta...",height=38).pack(side="left",fill="x",expand=True,padx=(0,8))
        ctk.CTkOptionMenu(bar,values=["Todos","Muy Alta","Alta","Media","Baja"],fg_color=COLORS["surface_alt"],button_color=COLORS["primary"],text_color=COLORS["text"]).pack(side="left",padx=4)
        ctk.CTkOptionMenu(bar,values=["Todos","Nuevos","En revisión","Derivados","Seguimiento","Cerrados"],fg_color=COLORS["surface_alt"],button_color=COLORS["primary"],text_color=COLORS["text"]).pack(side="left",padx=4)
        self.card("Búsqueda local","La búsqueda está preparada para trabajar sobre la base de datos local del sistema, sin enviar el contenido a servicios externos.")
        self.card("Estados del caso","Nuevo → En análisis → Revisado → Derivado → En seguimiento → Cerrado","Abrir historial")

class FollowUpPanel(WorkspacePanel):
    def __init__(self,parent,**kwargs):
        super().__init__(parent,"Seguimiento","Organizá próximas acciones, derivaciones y revisiones.",**kwargs)
        self.card("Hoy","Seguimientos pendientes, entrevistas y tareas que requieren revisión.","Ver pendientes")
        self.card("Próximamente","La agenda local puede utilizarse para recordar revisiones y fechas de seguimiento.","Nueva tarea")
        self.card("Historial","Registro cronológico de acciones asociadas a un caso.","Abrir historial")

class LibraryPanel(WorkspacePanel):
    def __init__(self,parent,**kwargs):
        super().__init__(parent,"Biblioteca local","Documentos y materiales internos que la organización puede consultar sin conexión.",**kwargs)
        self.card("Protocolos","Guardá procedimientos internos, guías y documentos de referencia.","Agregar documento")
        self.card("Plantillas","Organizá plantillas para informes, derivaciones y comunicaciones.","Administrar plantillas")
        self.card("Búsqueda","Preparado para indexar contenido local y encontrar rápidamente información cargada por la organización.")

class SecurityPanel(WorkspacePanel):
    def __init__(self,parent,**kwargs):
        super().__init__(parent,"Privacidad y seguridad","Controles locales para proteger la información de los casos.",**kwargs)
        self.card("Estado","Modo offline · almacenamiento local · sin envío automático de casos.")
        self.card("Bloqueo de sesión","Configurá un bloqueo local para impedir acceso accidental al equipo.","Configurar bloqueo")
        self.card("Copias de seguridad","Creá y restaurá copias de la información de la organización según su política interna.","Gestionar copias")
        self.card("Auditoría","Consultá acciones administrativas sin almacenar innecesariamente el contenido sensible de los relatos.","Abrir registro")

class AgendaPanel(WorkspacePanel):
    def __init__(self,parent,**kwargs):
        super().__init__(parent,"Agenda","Vista rápida de tareas y fechas de seguimiento locales.",**kwargs)
        self.card("Hoy","Tareas y seguimientos previstos para hoy.","Agregar")
        self.card("Esta semana","Organizá revisiones, entrevistas e informes pendientes.","Ver semana")
        self.card("Próximas fechas","Preparado para integrar recordatorios con los casos locales.","Ver calendario")
