"""Ventana principal: una sola navegación lateral y un espacio de trabajo limpio."""
import customtkinter as ctk
import logging,inspect
from pathlib import Path
from PIL import Image
from .results_panel import ResultsFrame
from .resources_panel import ResourcesPanel
from .dashboard import DashboardFrame
from .config_panel import ConfigPanel
from .help_panel import HelpPanel
from .social_report_panel import SocialReportPanel
from .workspace_panels import CasesPanel,FollowUpPanel,LibraryPanel,SecurityPanel,AgendaPanel
from .onboarding import show_first_run
from .styles import COLORS,FONTS
from ..case_manager import CaseManager
from ..config_manager import ConfigManager
logger=logging.getLogger(__name__)
ctk.set_appearance_mode("system"); ctk.set_default_color_theme("blue")
class AboutPanel(ctk.CTkFrame):
 def __init__(self,parent,**kwargs):
  super().__init__(parent,**kwargs); scroll=ctk.CTkScrollableFrame(self,fg_color="transparent"); scroll.pack(fill="both",expand=True,padx=28,pady=22)
  ctk.CTkLabel(scroll,text="Acerca de Asistente ONG",font=FONTS["title"],text_color=COLORS["text"]).pack(anchor="w"); ctk.CTkLabel(scroll,text="Presentación · propósito · funcionamiento · privacidad",font=FONTS["subheading"],text_color=COLORS["primary"]).pack(anchor="w",pady=(4,18))
  sections=[("PRESENTACIÓN","Soy Sarah, creadora y desarrolladora de este proyecto. Asistente ONG nace de la necesidad de transformar una idea social en una herramienta concreta, simple de usar y respetuosa de la privacidad de las personas que buscan ayuda."),("PROPÓSITO","La aplicación está pensada como una caja de herramientas para organizaciones sociales que reciben consultas y necesitan ordenar información, detectar indicadores relevantes y decidir qué revisar o derivar."),("CÓMO SE USA","1. Casos: crear un caso y completar sus datos junto con el relato. 2. Análisis: revisar prioridad, contexto, motivo, indicadores y preguntas pendientes. 3. Seguimiento: registrar acciones y fechas. 4. Informes y recursos: producir documentación y consultar materiales internos."),("PRIVACIDAD Y OFFLINE","El procesamiento es local. Los relatos y registros permanecen en el equipo. La aplicación no necesita Internet para realizar el triaje ni para gestionar los casos."),("CRITERIO DEL SISTEMA","El análisis utiliza reglas locales explicables. Una prioridad no es un diagnóstico ni una sentencia: indica qué conviene revisar primero. El operador mantiene siempre la decisión profesional."),("TECNOLOGÍA","Python · CustomTkinter · SQLite · reglas explicables · almacenamiento local · generación de informes."),("PROYECTO","Asistente ONG · NubiWorks. Herramienta de apoyo operativo para organizaciones sociales, diseñada para priorizar claridad, privacidad y trazabilidad.")]
  for title,text in sections:self._section(scroll,title,text)
 def _section(self,parent,title,text):
  card=ctk.CTkFrame(parent,fg_color=COLORS["surface_alt"],corner_radius=16,border_width=1,border_color=COLORS["border"]); card.pack(fill="x",pady=6); ctk.CTkLabel(card,text=title,font=FONTS["subheading"],text_color=COLORS["primary"],anchor="w").pack(fill="x",padx=20,pady=(15,6)); ctk.CTkLabel(card,text=text,font=FONTS["body"],text_color=COLORS["text"],justify="left",anchor="w",wraplength=850).pack(fill="x",padx=20,pady=(0,18))
class MainWindow:
 def __init__(self):
  self.root=ctk.CTk(); self.root.title("Asistente ONG | Triaje y Canalización"); self.root.geometry("1500x900"); self.root.minsize(1080,700); self.root.configure(fg_color=COLORS["background"]); self.root.grid_rowconfigure(0,weight=1); self.root.grid_columnconfigure(0,weight=1); self.case_manager=CaseManager(); self.config_manager=ConfigManager(); self.frames={}; self._setup_ui(); show_first_run(self.root)
 def _setup_ui(self):
  main=ctk.CTkFrame(self.root,fg_color=COLORS["background"],corner_radius=0); main.pack(fill="both",expand=True); main.grid_columnconfigure(1,weight=1); main.grid_rowconfigure(0,weight=1)
  sidebar=ctk.CTkFrame(main,width=265,fg_color=COLORS["surface_alt"],corner_radius=0); sidebar.grid(row=0,column=0,sticky="nsew"); sidebar.grid_propagate(False)
  brand=ctk.CTkFrame(sidebar,fg_color=COLORS["surface"],corner_radius=18,border_width=1,border_color=COLORS["border"]); brand.pack(fill="x",padx=12,pady=12)
  try:
   path=Path(__file__).parent.parent.parent/"assets"/"logo_g.png"
   if path.exists(): im=Image.open(path).convert("RGBA"); im.thumbnail((52,52)); li=ctk.CTkImage(light_image=im,dark_image=im,size=(52,52)); lab=ctk.CTkLabel(brand,image=li,text=""); lab.image=li; lab.pack(side="left",padx=(10,8),pady=10)
  except Exception: pass
  titlebox=ctk.CTkFrame(brand,fg_color="transparent"); titlebox.pack(side="left",fill="x",expand=True); ctk.CTkLabel(titlebox,text="Asistente ONG",font=FONTS["heading"],text_color=COLORS["text"]).pack(anchor="w"); ctk.CTkLabel(titlebox,text="Triaje · Casos · Seguimiento",font=FONTS["tiny"],text_color=COLORS["text_muted"]).pack(anchor="w"); ctk.CTkLabel(titlebox,text="NubiWorks",font=FONTS["small_bold"],text_color=COLORS["primary"]).pack(anchor="w",pady=(4,0))
  ctk.CTkButton(sidebar,text="＋  Nuevo caso",height=44,corner_radius=11,fg_color=COLORS["primary"],hover_color=COLORS["primary_dark"],font=FONTS["body_bold"],command=self.open_new_case).pack(fill="x",padx=12,pady=(2,12)); nav=ctk.CTkScrollableFrame(sidebar,fg_color="transparent"); nav.pack(fill="both",expand=True,padx=6); self.nav_buttons=[]
  for target in ["Inicio","Casos","Análisis","Seguimiento","Informe Social","Recursos","Biblioteca","Agenda","Seguridad","Configuración","Ayuda","Acerca de"]:
   b=ctk.CTkButton(nav,text=target,height=36,anchor="w",corner_radius=9,fg_color="transparent",hover_color=COLORS["primary_soft"],text_color=COLORS["text"],font=FONTS["body"],command=lambda t=target:self.select_tab(t)); b.pack(fill="x",padx=4,pady=2); self.nav_buttons.append((target,b))
  status=ctk.CTkFrame(sidebar,fg_color=COLORS["success_soft"],corner_radius=13); status.pack(fill="x",padx=12,pady=12); ctk.CTkLabel(status,text="●  OFFLINE",font=FONTS["small_bold"],text_color=COLORS["success"]).pack(anchor="w",padx=12,pady=(9,2)); ctk.CTkLabel(status,text="Todo se procesa en este equipo",font=FONTS["tiny"],text_color=COLORS["text_muted"]).pack(anchor="w",padx=12,pady=(0,9))
  workspace=ctk.CTkFrame(main,fg_color=COLORS["background"],corner_radius=0); workspace.grid(row=0,column=1,sticky="nsew",padx=(8,16),pady=14); workspace.grid_rowconfigure(0,weight=1); workspace.grid_columnconfigure(0,weight=1)
  specs=[("Inicio",DashboardFrame),("Casos",CasesPanel),("Análisis",ResultsFrame),("Seguimiento",FollowUpPanel),("Informe Social",SocialReportPanel),("Recursos",ResourcesPanel),("Biblioteca",LibraryPanel),("Agenda",AgendaPanel),("Seguridad",SecurityPanel),("Configuración",ConfigPanel),("Ayuda",HelpPanel),("Acerca de",AboutPanel)]
  for name,cls in specs:
   params=inspect.signature(cls.__init__).parameters; kwargs={"fg_color":COLORS["background"]}
   if name=="Casos": kwargs.update({"case_manager":self.case_manager,"on_analyze":self._on_case_submit})
   elif "case_manager" in params: kwargs["case_manager"]=self.case_manager
   elif "config_manager" in params: kwargs["config_manager"]=self.config_manager
   try: frame=cls(workspace,**kwargs)
   except TypeError: frame=cls(workspace,fg_color=COLORS["background"])
   frame.grid(row=0,column=0,sticky="nsew"); self.frames[name]=frame
  self.select_tab("Inicio")
 def select_tab(self,target):
  frame=self.frames.get(target)
  if frame: frame.tkraise()
  for name,b in self.nav_buttons: b.configure(fg_color=COLORS["primary"] if name==target else "transparent",text_color=COLORS["surface"] if name==target else COLORS["text"])
 def open_new_case(self): self.select_tab("Casos"); self.frames["Casos"].show_new_case()
 def _on_case_submit(self,case_text,metadata):
  try:
   analysis=self.config_manager.analyze(case_text); case=self.case_manager.create_case(text=case_text,urgency=analysis["urgency"],keywords=analysis["keywords"],metadata=metadata); casos=self.frames["Casos"]; casos.close_editor(); self.frames["Análisis"].show_analysis(case.case_number,case_text,analysis); self.select_tab("Análisis")
   try:self.frames["Inicio"].refresh(); casos.refresh()
   except Exception:pass
  except Exception as exc: logger.error("Error procesando caso: %s",exc,exc_info=True)
 def run(self): self.root.mainloop()
if __name__=="__main__": MainWindow().run()
