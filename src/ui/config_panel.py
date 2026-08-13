"""Configuración útil del entorno y de los informes."""
import customtkinter as ctk
from pathlib import Path
from .styles import COLORS, FONTS
from ..reports.report_defaults import ReportDefaults

THEME_FILE = Path.home() / ".asistente_ong_theme"

class ConfigPanel(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.defaults = ReportDefaults()
        self._setup_ui()

    def _setup_ui(self):
        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=24, pady=22)
        ctk.CTkLabel(scroll, text="Configuración", font=FONTS["title"], text_color=COLORS["text"]).pack(anchor="w")
        ctk.CTkLabel(scroll, text="Configurá lo que el sistema debe recordar. Los datos institucionales se guardan localmente.", font=FONTS["small"], text_color=COLORS["text_muted"], wraplength=980, justify="left").pack(anchor="w", pady=(3, 18))
        self._institution_card(scroll)
        self._appearance_card(scroll)
        self._online_card(scroll)
        self._privacy_card(scroll)
        self._flow_card(scroll)

    def _card(self, parent, title, description):
        card = ctk.CTkFrame(parent, fg_color=COLORS["surface"], corner_radius=18, border_width=1, border_color=COLORS["border"])
        card.pack(fill="x", pady=7)
        ctk.CTkLabel(card, text=title, font=FONTS["heading"], text_color=COLORS["text"]).pack(anchor="w", padx=18, pady=(16, 3))
        ctk.CTkLabel(card, text=description, font=FONTS["small"], text_color=COLORS["text_muted"], wraplength=900, justify="left").pack(anchor="w", padx=18, pady=(0, 12))
        return card

    def _institution_card(self, parent):
        card=self._card(parent,"Datos institucionales","Estos datos se reutilizan en nuevos informes sociales. Se guardan localmente y se pueden modificar en cualquier momento.")
        self.inputs={}; defaults=self.defaults.load()
        fields=[("entidad_emisora","Entidad emisora"),("profesional_referencia","Profesional de referencia"),("colegiatura","Matrícula / colegiatura"),("destinatario","Destinatario habitual")]
        for key,label in fields:
            row=ctk.CTkFrame(card,fg_color="transparent"); row.pack(fill="x",padx=18,pady=4); row.grid_columnconfigure(1,weight=1)
            ctk.CTkLabel(row,text=label,width=190,anchor="w",font=FONTS["small_bold"],text_color=COLORS["text"]).grid(row=0,column=0,padx=(0,8))
            entry=ctk.CTkEntry(row,height=36); entry.grid(row=0,column=1,sticky="ew"); entry.insert(0,defaults.get(key,"")); self.inputs[key]=entry
        self.institution_status=ctk.CTkLabel(card,text="",font=FONTS["tiny"],text_color=COLORS["success"]); self.institution_status.pack(anchor="w",padx=18,pady=(4,0))
        ctk.CTkButton(card,text="Guardar datos institucionales",height=38,command=self._save_defaults,fg_color=COLORS["primary"],hover_color=COLORS["primary_dark"]).pack(anchor="e",padx=18,pady=12)

    def _save_defaults(self):
        self.defaults.save({k:e.get() for k,e in self.inputs.items()}); self.institution_status.configure(text="Guardado localmente.")

    def _read_theme(self):
        try:
            value=THEME_FILE.read_text(encoding="utf-8").strip().lower()
            return value if value in {"light","dark"} else ctk.get_appearance_mode().lower()
        except Exception:
            return ctk.get_appearance_mode().lower()

    def _save_theme(self, value):
        try:
            THEME_FILE.write_text(value,encoding="utf-8")
        except Exception:
            pass
        ctk.set_appearance_mode(value)
        self.theme_status.configure(text=f"Tema {('claro' if value == 'light' else 'oscuro')} aplicado. Se usará también en la próxima pantalla de carga.")

    def _appearance_card(self, parent):
        card=self._card(parent,"Apariencia","Elegí el tema visual. El mismo tema se aplica a la pantalla de carga, la introducción y la interfaz principal.")
        row=ctk.CTkFrame(card,fg_color="transparent"); row.pack(fill="x",padx=18,pady=(0,16))
        current=self._read_theme()
        self.theme_selector=ctk.CTkSegmentedButton(row,values=["light","dark"],command=self._save_theme,width=260,height=38)
        self.theme_selector.set(current if current in {"light","dark"} else "light"); self.theme_selector.pack(side="left")
        self.theme_status=ctk.CTkLabel(row,text="",font=FONTS["tiny"],text_color=COLORS["success"]); self.theme_status.pack(side="left",padx=14)
        ctk.CTkLabel(card,text="Claro · interfaz luminosa / Oscuro · interfaz nocturna futurista",font=FONTS["tiny"],text_color=COLORS["text_muted"]).pack(anchor="w",padx=18,pady=(0,14))

    def _online_card(self, parent):
        card=self._card(parent,"Conectividad y fuentes oficiales","Offline es el modo base. Si hay Internet, la función de fuentes puede consultar información pública y filtrar resultados para aceptar solamente dominios oficiales configurados. Los relatos de casos nunca se envían como consulta.")
        self.online_var=ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(card,text="Permitir consultas de fuentes oficiales cuando haya conexión",variable=self.online_var,text_color=COLORS["text"]).pack(anchor="w",padx=18,pady=(0,8))
        ctk.CTkLabel(card,text="Dominios base: argentina.gob.ar · boletinoficial.gob.ar · mpf.gob.ar · jus.gob.ar",font=FONTS["tiny"],text_color=COLORS["text_muted"],wraplength=900,justify="left").pack(anchor="w",padx=18,pady=(0,16))

    def _privacy_card(self,parent):
        card=self._card(parent,"Privacidad y almacenamiento","Los casos, informes, seguimiento y memoria se guardan en SQLite local. No se almacenan imágenes del caso salvo que una función futura lo solicite explícitamente.")
        ctk.CTkLabel(card,text="LOCAL FIRST · sin envío automático de expedientes",font=FONTS["body_bold"],text_color=COLORS["success"]).pack(anchor="w",padx=18,pady=(0,16))

    def _flow_card(self,parent):
        card=self._card(parent,"Flujo recomendado","1. Nuevo caso → 2. Relato y datos disponibles → 3. Análisis contextual → 4. Caso + Informe Social → 5. Revisión profesional → 6. Recurso o derivación → 7. Seguimiento → 8. Cierre.")
        ctk.CTkLabel(card,text="Cada pantalla tiene una función y cada acción debe producir un cambio real o abrir información relacionada.",font=FONTS["body"],text_color=COLORS["text_muted"],wraplength=900,justify="left").pack(anchor="w",padx=18,pady=(0,16))
