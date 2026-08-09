"""Ayuda y acceso al tutorial interactivo."""
import customtkinter as ctk
from .styles import COLORS, FONTS
from .onboarding import show_tutorial

class HelpPanel(ctk.CTkFrame):
 def __init__(self,parent,**kwargs):
  super().__init__(parent,**kwargs); self._setup_ui()
 def _setup_ui(self):
  scroll=ctk.CTkScrollableFrame(self,fg_color="transparent"); scroll.pack(fill="both",expand=True,padx=24,pady=22)
  ctk.CTkLabel(scroll,text="Ayuda",font=FONTS["title"],text_color=COLORS["text"]).pack(anchor="w")
  ctk.CTkLabel(scroll,text="Aprendé el recorrido de la plataforma sin llenar el sistema con ejemplos.",font=FONTS["small"],text_color=COLORS["text_muted"],wraplength=900).pack(anchor="w",pady=(3,16))
  ctk.CTkButton(scroll,text="Abrir tutorial interactivo",height=46,fg_color=COLORS["primary"],hover_color=COLORS["primary_dark"],command=lambda:show_tutorial(self.winfo_toplevel())).pack(anchor="w",pady=(0,18))
  for title,text in [("Inicio","El panel inicial muestra únicamente tus propios casos, fechas y documentos. Si está vacío, es porque todavía no cargaste información."),("Casos","Usá Nuevo caso para crear un expediente. Completá solo lo necesario y revisá el relato antes de analizarlo."),("Biblioteca","Importá PDFs desde el botón Importar PDFs o copiálos en data/library y elegí Recargar carpeta. Los PDFs digitales se procesan localmente con pypdf."),("Análisis","El sistema aplica reglas locales explicables. Si existen documentos relacionados en la biblioteca, aparecen como documentación relevante; no se incorporan automáticamente como verdad ni reemplazan la revisión profesional."),("Seguimiento y Agenda","Registrá acciones y fechas en Seguimiento. Agenda muestra las fechas guardadas."),("Privacidad","Los casos y documentos se almacenan localmente. La búsqueda por Internet es una función separada y explícita.")]:
   card=ctk.CTkFrame(scroll,fg_color=COLORS["surface_alt"],corner_radius=14,border_width=1,border_color=COLORS["border"]); card.pack(fill="x",pady=5); ctk.CTkLabel(card,text=title,font=FONTS["heading"],text_color=COLORS["text"]).pack(anchor="w",padx=18,pady=(13,4)); ctk.CTkLabel(card,text=text,font=FONTS["body"],text_color=COLORS["text_muted"],wraplength=900,justify="left").pack(fill="x",padx=18,pady=(0,15))
