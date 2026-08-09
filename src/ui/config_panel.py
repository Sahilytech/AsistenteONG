"""Configuración del operador: tema, privacidad y preferencias locales."""
import customtkinter as ctk
from .styles import COLORS,FONTS,switch_theme

class ConfigPanel(ctk.CTkFrame):
    def __init__(self,parent,**kwargs):
        super().__init__(parent,**kwargs); self._setup_ui()
    def _setup_ui(self):
        scroll=ctk.CTkScrollableFrame(self,fg_color="transparent"); scroll.pack(fill="both",expand=True,padx=24,pady=22)
        ctk.CTkLabel(scroll,text="Configuración",font=FONTS["title"],text_color=COLORS["text"]).pack(anchor="w")
        ctk.CTkLabel(scroll,text="Personalizá el entorno de trabajo sin salir de la aplicación.",font=FONTS["small"],text_color=COLORS["text_muted"]).pack(anchor="w",pady=(3,20))
        card=ctk.CTkFrame(scroll,fg_color=COLORS["surface"],corner_radius=16,border_width=1,border_color=COLORS["border"]); card.pack(fill="x",pady=6)
        ctk.CTkLabel(card,text="Apariencia",font=FONTS["heading"],text_color=COLORS["text"]).pack(anchor="w",padx=18,pady=(16,3))
        ctk.CTkLabel(card,text="Elegí cómo querés ver la aplicación. Los cambios se aplican a las ventanas nuevas.",font=FONTS["small"],text_color=COLORS["text_muted"]).pack(anchor="w",padx=18,pady=(0,10))
        self.theme=ctk.StringVar(value="Sistema")
        selector=ctk.CTkSegmentedButton(card,values=["Sistema","Claro","Oscuro"],variable=self.theme,command=self._theme_changed); selector.pack(anchor="w",padx=18,pady=(0,18))
        privacy=ctk.CTkFrame(scroll,fg_color=COLORS["surface"],corner_radius=16,border_width=1,border_color=COLORS["border"]); privacy.pack(fill="x",pady=6)
        ctk.CTkLabel(privacy,text="Privacidad",font=FONTS["heading"],text_color=COLORS["text"]).pack(anchor="w",padx=18,pady=(16,4))
        ctk.CTkLabel(privacy,text="MODO OFFLINE · sin búsquedas web · sin envío de relatos a servidores · almacenamiento local.",font=FONTS["body"],text_color=COLORS["success"]).pack(anchor="w",padx=18,pady=(0,16))
        info=ctk.CTkFrame(scroll,fg_color=COLORS["surface_alt"],corner_radius=16,border_width=1,border_color=COLORS["border"]); info.pack(fill="x",pady=6)
        ctk.CTkLabel(info,text="Herramientas locales",font=FONTS["heading"],text_color=COLORS["text"]).pack(anchor="w",padx=18,pady=(16,8))
        ctk.CTkLabel(info,text="Triaje orientativo · gestión de casos · seguimiento · informes · recursos · biblioteca · agenda · copias de seguridad.",font=FONTS["body"],text_color=COLORS["text_muted"],wraplength=720,justify="left").pack(anchor="w",padx=18,pady=(0,18))
    def _theme_changed(self,value):
        mode={"Sistema":"light","Claro":"light","Oscuro":"dark"}[value]; switch_theme(mode); ctk.set_appearance_mode("dark" if mode=="dark" else "light")
