"""Shell principal: navegación lateral y espacio de trabajo integrado."""
import customtkinter as ctk
import logging, inspect
from pathlib import Path
from PIL import Image
from .case_input import CaseInputFrame
from .results_panel import ResultsFrame
from .resources_panel import ResourcesPanel
from .dashboard import DashboardFrame
from .config_panel import ConfigPanel
from .help_panel import HelpPanel
from .social_report_panel import SocialReportPanel
from .workspace_panels import CasesPanel,FollowUpPanel,LibraryPanel,SecurityPanel,AgendaPanel
from .styles import COLORS,FONTS
from ..case_manager import CaseManager
from ..config_manager import ConfigManager
logger=logging.getLogger(__name__)
ctk.set_default_color_theme("blue")
class AboutPanel(ctk.CTkFrame):
 def __init__(self,parent,**kwargs):
  super().__init__(parent,**kwargs); self.grid_rowconfigure(0,weight=1); self.grid_columnconfigure(0,weight=1); scroll=ctk.CTkScrollableFrame(self,fg_color="transparent"); scroll.grid(row=0,column=0,sticky="nsew",padx=28,pady=22); ctk.CTkLabel(scroll,text="Acerca de Asistente ONG",font=FONTS["title"],text_color=COLORS["text"]).pack(anchor="w"); ctk.CTkLabel(scroll,text="NubiWorks · tecnología local para apoyo social",font=FONTS["subheading"],text_color=COLORS["primary"]).pack(anchor="w",pady=(4,18));
  for title,text in [("EL PROYECTO","Suite de escritorio para organizaciones sociales: triaje contextual orientativo, gestión de casos, informes, recursos y seguimiento."),("PRIVACIDAD","Funcionamiento completamente offline. Los relatos, casos y memoria permanecen en el equipo. No realiza búsquedas web ni envía información a servicios externos."),("CÓMO FUNCIONA","El operador ingresa un relato, el motor local identifica indicadores y genera una prioridad orientativa. El operador revisa el resultado y decide."),("QUÉ NO HACE","No diagnostica ni reemplaza profesionales. Los resultados automáticos deben revisarse."),("TECNOLOGÍAS","Python · CustomTkinter · SQLite · procesamiento local · reglas explicables · informes.")]: self._section(scroll,title,text)
 def _section(self,parent,title,text):
  card=ctk.CTkFrame(parent,fg_color=COLORS["surface_alt"],corner_radius=16,border_width=1,border_color=COLORS["border"]); card.pack(fill="x",pady=6); ctk.CTkLabel(card,text=title,font=FONTS["subheading"],text_color=COLORS["primary"],anchor="w").pack(fill="x",padx=20,pady=(15,6)); ctk.CTkLabel(card,text=text,font=FONTS["body"],text_color=COLORS["text"],justify="left",anchor="w",wraplength=760).pack(fill="x",padx=20,pady=(0,18))
class MainWindow:
 def __init__(self):
  self.root=ctk.CTk(); self.root.title("Asistente ONG | Triaje y Canalización"); self.root.geometry("1500x900"); self.root.minsize(1080,700); self.root.configure(fg_color=COLORS["background"]); self.root.grid_rowconfigure(0,weight=1); self.root.grid_columnconfigure(0,weight=1); self.case_manager=CaseManager(); self.config_manager=ConfigManager(); self._setup_ui()
 def _setup_ui(self):
  main=ctk.CTkFrame(self.root,fg_color=COLORS["background"],corner_radius=0); main.grid(row=0,column=0,sticky="nsew"); main.grid_columnconfigure(0,weight=0,minsize=265); main.grid_columnconfigure(1,weight=1); main.grid_rowconfigure(0,weight=1); sidebar=ctk.CTkFrame(main,width=265,fg_color=COLORS["surface_alt"],corner_radius=0); sidebar.grid(row=0,column=0,sticky="nsew"); sidebar.grid_propagate(False)
  brand=ctk.CTkFrame(sidebar,fg_color=COLORS["surface"],corner_radius=18,border_width=1,border_color=COLORS["border"]); brand.pack(fill="x",padx=12,pady=12)
  try:
   path=Path(__file__).parent.parent.parent/"assets"/"logo_g.png"
   if path.exists(): im=Image.open(path).convert("RGBA"); im.thumbnail((52,52)); li=ctk.CTkImage(light_image=im,size=(52,52)); lab=ctk.CTkLabel(brand,image=li,text=""); lab.image=li; lab.pack(side="left",padx=(10,8),pady=10)
  except Exception: pass
  titlebox=ctk.CTkFrame(brand,fg_color="transparent"); titlebox.pack(side="left",fill="x",expand=True); ctk.CTkLabel(titlebox,text="Asistente ONG",font=FONTS["heading"],text_color=COLORS["text"]).pack(anchor="w"); ctk.CTkLabel(titlebox,text="Triaje · Casos · Informes",font=FONTS["tiny"],text_color=COLORS["text_muted"]).pack(anchor="w"); ctk.CTkLabel(titlebox,text="NubiWorks",font=FONTS["small_bold"],text_color=COLORS["primary"]).pack(anchor="w",pady=(4,0))
  ctk.CTkButton(sidebar,text="＋  Nuevo caso",height=44,corner_radius=11,fg_color=COLORS["primary"],hover_color=COLORS["primary_dark"],font=FONTS["body_bold"],command=self.open_new_case).pack(fill="x",padx=12,pady=(2,12)); nav=ctk.CTkScrollableFrame(sidebar,fg_color="transparent"); nav.pack(fill="both",expand=True,padx=6); self.nav_buttons=[]
  tabs=[("Inicio","Inicio"),("Casos","Casos"),("Análisis","Análisis"),("Seguimiento","Seguimiento"),("Informe Social","Informe Social"),("Recursos","Recursos"),("Biblioteca","Biblioteca"),("Agenda","Agenda"),("Seguridad","Seguridad"),("Configuración","Configuración"),("Ayuda","Ayuda"),("Acerca de","Acerca de")]
  for label,target in tabs:
   b=ctk.CTkButton(nav,text=label,height=36,anchor="w",corner_radius=9,fg_color="transparent",hover_color=COLORS["primary_soft"],text_color=COLORS["text"],font=FONTS["body"],command=lambda t=target:self.select_tab(t)); b.pack(fill="x",padx=4,pady=2); self.nav_buttons.append((target,b))
  status=ctk.CTkFrame(sidebar,fg_color=COLORS["success_soft"],corner_radius=13); status.pack(fill="x",padx=12,pady=12); ctk.CTkLabel(status,text="●  OFFLINE",font=FONTS["small_bold"],text_color=COLORS["success"]).pack(anchor="w",padx=12,pady=(9,2)); ctk.CTkLabel(status,text="Todo se procesa en este equipo",font=FONTS["tiny"],text_color=COLORS["text_muted"]).pack(anchor="w",padx=12,pady=(0,9))
  center=ctk.CTkFrame(main,fg_color=COLORS["surface"],corner_radius=20,border_width=1,border_color=COLORS["border"]); center.grid(row=0,column=1,sticky="nsew",padx=(8,16),pady=14); self.tab_view=ctk.CTkTabview(center,fg_color=COLORS["surface"],corner_radius=14); self.tab_view.pack(fill="both",expand=True); self.tab_view._segmented_button.grid_remove()
  for name,cls in [("Inicio",DashboardFrame),("Casos",CasesPanel),("Análisis",ResultsFrame),("Seguimiento",FollowUpPanel),("Informe Social",SocialReportPanel),("Recursos",ResourcesPanel),("Biblioteca",LibraryPanel),("Agenda",AgendaPanel),("Seguridad",SecurityPanel),("Configuración",ConfigPanel),("Ayuda",HelpPanel),("Acerca de",AboutPanel)]:
   tab=self.tab_view.add(name); params=inspect.signature(cls.__init__).parameters; kwargs={"fg_color":COLORS["background"]};
   if "case_manager" in params: kwargs["case_manager"]=self.case_manager
   if "config_manager" in params: kwargs["config_manager"]=self.config_manager
   try: obj=cls(tab,**kwargs)
   except TypeError: obj=cls(tab,fg_color=COLORS["background"])
   obj.pack(fill="both",expand=True); setattr(self,name.replace(" ","_").lower(),obj)
  self.root.select_tab=self.select_tab; self.root.open_new_case=self.open_new_case; self.select_tab("Inicio")
 def select_tab(self,target):
  self.tab_view.set(target)
  for name,b in self.nav_buttons: b.configure(fg_color=COLORS["primary"] if name==target else "transparent",text_color=COLORS["surface"] if name==target else COLORS["text"])
 def open_new_case(self):
  self.select_tab("Casos")
  if hasattr(self,"_case_editor") and self._case_editor.winfo_exists(): self._case_editor.destroy()
  self._case_editor=CaseInputFrame(self.casos,on_submit=self._on_case_submit,fg_color=COLORS["background"]); self._case_editor.place(relx=0,rely=0,relwidth=1,relheight=1); self._case_editor.lift()
 def _on_case_submit(self,case_number,case_text):
  try:
   analysis=self.config_manager.analyze(case_text); case=self.case_manager.create_case(text=case_text,urgency=analysis["urgency"],keywords=analysis["keywords"])
   if hasattr(self,"_case_editor") and self._case_editor.winfo_exists(): self._case_editor.destroy()
   self.analisis.show_analysis(case.case_number,case_text,analysis); self.select_tab("Análisis")
   try:self.inicio.refresh(); self.casos.refresh()
   except Exception:pass
  except Exception as exc: logger.error("Error procesando caso: %s",exc,exc_info=True)
 def run(self): self.root.mainloop()
if __name__=="__main__": MainWindow().run()
