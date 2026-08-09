"""Configuración del operador."""
import customtkinter as ctk
from .styles import COLORS,FONTS

class ConfigPanel(ctk.CTkFrame):
    def __init__(self,parent,**kwargs):
        super().__init__(parent,**kwargs); self._setup_ui()
    def _setup_ui(self):
        scroll=ctk.CTkScrollableFrame(self,fg_color="transparent"); scroll.pack(fill="both",expand=True,padx=24,pady=22)
        ctk.CTkLabel(scroll,text="Configuración",font=FONTS["title"],text_color=COLORS["text"]).pack(anchor="w")
        ctk.CTkLabel(scroll,text="Preferencias del entorno de trabajo. Los casos y datos no se envían a Internet.",font=FONTS["small"],text_color=COLORS["text_muted"]).pack(anchor="w",pady=(3,20))
        card=ctk.CTkFrame(scroll,fg_color=COLORS["surface"],corner_radius=16,border_width=1,border_color=COLORS["border"]); card.pack(fill="x",pady=6)
        ctk.CTkLabel(card,text="Apariencia",font=FONTS["heading"],text_color=COLORS["text"]).pack(anchor="w",padx=18,pady=(16,3))
        ctk.CTkLabel(card,text="Elegí el aspecto de la aplicación. El cambio se aplica inmediatamente.",font=FONTS["small"],text_color=COLORS["text_muted"]).pack(anchor="w",padx=18,pady=(0,10))
        self.theme=ctk.StringVar(value="Sistema")
        ctk.CTkSegmentedButton(card,values=["Sistema","Claro","Oscuro"],variable=self.theme,command=self._theme_changed).pack(anchor="w",padx=18,pady=(0,18))
        privacy=ctk.CTkFrame(scroll,fg_color=COLORS["surface"],corner_radius=16,border_width=1,border_color=COLORS["border"]); privacy.pack(fill="x",pady=6)
        ctk.CTkLabel(privacy,text="Privacidad",font=FONTS["heading"],text_color=COLORS["text"]).pack(anchor="w",padx=18,pady=(16,4))
        ctk.CTkLabel(privacy,text="MODO OFFLINE · sin búsquedas web · sin APIs externas · relatos y casos almacenados localmente.",font=FONTS["body"],text_color=COLORS["success"],wraplength=760,justify="left").pack(anchor="w",padx=18,pady=(0,16))
        info=ctk.CTkFrame(scroll,fg_color=COLORS["surface_alt"],corner_radius=16,border_width=1,border_color=COLORS["border"]); info.pack(fill="x",pady=6)
        ctk.CTkLabel(info,text="Flujo recomendado",font=FONTS["heading"],text_color=COLORS["text"]).pack(anchor="w",padx=18,pady=(16,8))
        ctk.CTkLabel(info,text="1. Nuevo caso → 2. Datos del caso y relato → 3. Análisis local → 4. Revisión profesional → 5. Derivación o seguimiento → 6. Cierre.",font=FONTS["body"],text_color=COLORS["text_muted"],wraplength=760,justify="left").pack(anchor="w",padx=18,pady=(0,18))
    def _theme_changed(self,value):
        ctk.set_appearance_mode({"Sistema":"system","Claro":"light","Oscuro":"dark"}[value])
