"""Ventana principal: navegación lateral y espacio de trabajo integrado."""
import customtkinter as ctk,logging,inspect
from pathlib import Path
from PIL import Image
from .results_panel import ResultsFrame
from .resources_panel import ResourcesPanel
from .dashboard import DashboardFrame
from .config_panel import ConfigPanel
from .help_panel import HelpPanel
from .integrated_case_panel import IntegratedCasePanel
from .cases_panel import CasesPanel
from .people_panel import PeoplePanel
from .workspace_panels import FollowUpPanel,LibraryPanel,SecurityPanel,AgendaPanel
from .onboarding import show_first_run
from .styles import COLORS,FONTS
from ..case_manager import CaseManager
from ..config_manager import ConfigManager
from ..knowledge.memory import LocalMemory
from ..person_registry import PersonRegistry
from ..knowledge.case_document_matcher import build_case_context
logger=logging.getLogger(__name__);ctk.set_appearance_mode("light");ctk.set_default_color_theme("blue")
class AboutPanel(ctk.CTkFrame):
 def __init__(self,parent,**kwargs):
  super().__init__(parent,**kwargs);scroll=ctk.CTkScrollableFrame(self,fg_color="transparent");scroll.pack(fill="both",expand=True,padx=28,pady=22);ctk.CTkLabel(scroll,text="Acerca de Asistente ONG",font=FONTS["title"],text_color=COLORS["text"]).pack(anchor="w");ctk.CTkLabel(scroll,text="Gestión de personas · casos · documentación · seguimiento",font=FONTS["subheading"],text_color=COLORS["primary"]).pack(anchor="w",pady=(4,18))
  for title,text in [("PROPÓSITO","Herramienta de apoyo para equipos de asistencia. Organiza información y tareas repetitivas sin reemplazar la revisión profesional."),("PERSONAS Y CASOS","Una persona puede tener múltiples casos. El registro de persona se reutiliza y cada atención queda como un caso separado dentro de su historial."),("DOCUMENTACIÓN","Los PDFs se procesan localmente y sus fragmentos relevantes pueden recuperarse al analizar un caso. Las coincidencias se muestran como apoyo documental, no como conclusiones."),("PRIVACIDAD","El almacenamiento prioriza este equipo. Los campos personales sensibles son opcionales y la organización debe cargar únicamente lo necesario."),("LÍMITES","El análisis no diagnostica ni decide por sí solo cuestiones legales, sanitarias o de protección. Requiere revisión humana.")]:
   card=ctk.CTkFrame(scroll,fg_color=COLORS["surface_alt"],corner_radius=16,border_width=1,border_color=COLORS["border"]);card.pack(fill="x",pady=6);ctk.CTkLabel(card,text=title,font=FONTS["subheading"],text_color=COLORS["primary"]).pack(anchor="w",padx=20,pady=(15,6));ctk.CTkLabel(card,text=text,font=FONTS["body"],text_color=COLORS["text"],justify="left",anchor="w",wraplength=950).pack(fill="x",padx=20,pady=(0,18))
class MainWindow:
 def __init__(self):
  self.root=ctk.CTk();self.root.title("Asistente ONG | Triaje y Canalización");self.root.geometry("1500x900");self.root.minsize(1080,700);self.root.configure(fg_color=COLORS["background"]);self.root.grid_rowconfigure(0,weight=1);self.root.grid_columnconfigure(0,weight=1);self.case_manager=CaseManager();self.person_registry=PersonRegistry();self.config_manager=ConfigManager();self.memory=LocalMemory();self.frames={};self._setup_ui();self.root.app_controller=self;show_first_run(self.root)
 def _setup_ui(self):
  main=ctk.CTkFrame(self.root,fg_color=COLORS["background"],corner_radius=0);main.pack(fill="both",expand=True);main.grid_columnconfigure(1,weight=1);main.grid_rowconfigure(0,weight=1);sidebar=ctk.CTkFrame(main,width=265,fg_color=COLORS["surface_alt"],corner_radius=0);sidebar.grid(row=0,column=0,sticky="nsew");sidebar.grid_propagate(False)
  brand=ctk.CTkFrame(sidebar,fg_color=COLORS["surface"],corner_radius=18,border_width=1,border_color=COLORS["border"]);brand.pack(fill="x",padx=12,pady=12)
  try:
   path=Path(__file__).parent.parent.parent/"assets"/"logo_g.png"
   if path.exists():im=Image.open(path).convert("RGBA");im.thumbnail((52,52));li=ctk.CTkImage(light_image=im,dark_image=im,size=(52,52));lab=ctk.CTkLabel(brand,image=li,text="");lab.image=li;lab.pack(side="left",padx=(10,8),pady=10)
  except Exception:pass
  titlebox=ctk.CTkFrame(brand,fg_color="transparent");titlebox.pack(side="left",fill="x",expand=True);ctk.CTkLabel(titlebox,text="Asistente ONG",font=FONTS["heading"],text_color=COLORS["text"]).pack(anchor="w");ctk.CTkLabel(titlebox,text="Personas · Casos · Triaje",font=FONTS["tiny"],text_color=COLORS["text_muted"]).pack(anchor="w");ctk.CTkLabel(titlebox,text="NubiWorks",font=FONTS["small_bold"],text_color=COLORS["primary"]).pack(anchor="w",pady=(4,0))
  ctk.CTkButton(sidebar,text="＋  Nuevo caso",height=44,corner_radius=11,fg_color=COLORS["primary"],hover_color=COLORS["primary_dark"],font=FONTS["body_bold"],command=self.open_new_case).pack(fill="x",padx=12,pady=(2,12));nav=ctk.CTkScrollableFrame(sidebar,fg_color="transparent");nav.pack(fill="both",expand=True,padx=6);self.nav_buttons=[]
  for target in ["Inicio","Personas","Casos","Caso + Informe","Análisis","Seguimiento","Recursos","Biblioteca","Agenda","Seguridad","Configuración","Ayuda","Acerca de"]:
   b=ctk.CTkButton(nav,text=target,height=36,anchor="w",corner_radius=9,fg_color="transparent",hover_color=COLORS["primary_soft"],text_color=COLORS["text"],font=FONTS["body"],command=lambda t=target:self.select_tab(t));b.pack(fill="x",padx=4,pady=2);self.nav_buttons.append((target,b))
  status=ctk.CTkFrame(sidebar,fg_color=COLORS["success_soft"],corner_radius=13);status.pack(fill="x",padx=12,pady=12);ctk.CTkLabel(status,text="●  LOCAL FIRST",font=FONTS["small_bold"],text_color=COLORS["success"]).pack(anchor="w",padx=12,pady=(9,2));ctk.CTkLabel(status,text="Personas, casos y documentos en este equipo",font=FONTS["tiny"],text_color=COLORS["text_muted"]).pack(anchor="w",padx=12,pady=(0,9))
  workspace=ctk.CTkFrame(main,fg_color=COLORS["background"],corner_radius=0);workspace.grid(row=0,column=1,sticky="nsew",padx=(8,16),pady=14);workspace.grid_rowconfigure(0,weight=1);workspace.grid_columnconfigure(0,weight=1)
  specs=[("Inicio",DashboardFrame),("Personas",PeoplePanel),("Casos",CasesPanel),("Caso + Informe",IntegratedCasePanel),("Análisis",ResultsFrame),("Seguimiento",FollowUpPanel),("Recursos",ResourcesPanel),("Biblioteca",LibraryPanel),("Agenda",AgendaPanel),("Seguridad",SecurityPanel),("Configuración",ConfigPanel),("Ayuda",HelpPanel),("Acerca de",AboutPanel)]
  for name,cls in specs:
   params=inspect.signature(cls.__init__).parameters;kwargs={"fg_color":COLORS["background"]}
   if "case_manager" in params:kwargs["case_manager"]=self.case_manager
   if "person_registry" in params:kwargs["person_registry"]=self.person_registry
   if "config_manager" in params:kwargs["config_manager"]=self.config_manager
   if name=="Casos":kwargs["on_analyze"]=self._on_case_submit
   try:frame=cls(workspace,**kwargs)
   except TypeError as exc:logger.warning("Panel %s: %s",name,exc);frame=cls(workspace,fg_color=COLORS["background"])
   frame.grid(row=0,column=0,sticky="nsew");self.frames[name]=frame
  self.select_tab("Inicio")
 def select_tab(self,target):
  frame=self.frames.get(target)
  if frame:frame.tkraise()
  for name,b in self.nav_buttons:b.configure(fg_color=COLORS["primary"] if name==target else "transparent",text_color=COLORS["surface"] if name==target else COLORS["text"])
 def open_new_case(self):self.select_tab("Casos");self.frames["Casos"].show_new_case()
 def _on_case_submit(self,case_text,metadata):
  try:
   if not metadata.get("person_id") and metadata.get("person_name"):
    pid,_=self.person_registry.upsert({"name":metadata["person_name"],"contact":metadata.get("contact","")});metadata["person_id"]=pid
   analysis=self.config_manager.analyze(case_text)
   try:analysis["knowledge_matches"]=build_case_context(case_text)["matches"]
   except Exception:analysis["knowledge_matches"]=[]
   case=self.case_manager.create_case(text=case_text,urgency=analysis["urgency"],keywords=analysis["keywords"],metadata=metadata,analysis=analysis);self.frames["Casos"].close_editor();self.frames["Análisis"].show_analysis(case.case_number,case_text,analysis);self.frames["Caso + Informe"].refresh_cases();self.select_tab("Análisis")
   for name in ("Inicio","Casos","Personas"):
    try:self.frames[name].refresh()
    except Exception:pass
  except Exception as exc:logger.error("Error procesando caso: %s",exc,exc_info=True)
 def run(self):self.root.mainloop()
if __name__=="__main__":MainWindow().run()
