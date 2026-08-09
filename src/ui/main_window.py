"""Shell principal: navegación lateral, modo claro y espacio de trabajo responsivo."""
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
ctk.set_appearance_mode("light"); ctk.set_default_color_theme("blue")

class AboutPanel(ctk.CTkFrame):
 def __init__(self,parent,**kwargs):
  super().__init__(parent,**kwargs); self.grid_rowconfigure(0,weight=1); self.grid_columnconfigure(0,weight=1)
  scroll=ctk.CTkScrollableFrame(self,fg_color="transparent"); scroll.grid(row=0,column=0,sticky="nsew",padx=28,pady=22)
  ctk.CTkLabel(scroll,text="Acerca de Asistente ONG",font=FONTS["title"],text_color=COLORS["text"]).pack(anchor="w")
  ctk.CTkLabel(scroll,text="NubiWorks · tecnología offline para apoyo social",font=FONTS["subheading"],text_color=COLORS["primary"]).pack(anchor="w",pady=(4,18))
  sections=[("EL PROYECTO","Asistente ONG es una suite de escritorio orientada a organizaciones sociales, fundaciones y equipos de asistencia. Ayuda a organizar relatos, realizar un triaje contextual orientativo, gestionar casos, preparar informes, consultar recursos y mantener seguimientos en un entorno local."),("EL PROBLEMA","Los equipos pequeños pueden recibir muchos mensajes y consultas mientras cuentan con tiempo y recursos limitados. El proyecto busca reducir tareas repetitivas de clasificación y organización sin convertir la automatización en una sustitución del criterio profesional."),("CÓMO FUNCIONA","El flujo comienza con el relato recibido. El motor local identifica contexto e indicadores, estima una prioridad orientativa, explica qué encontró, señala información faltante y sugiere recursos. Luego el profesional revisa, corrige cuando corresponda y decide la intervención."),("PRIVACIDAD Y OFFLINE","La arquitectura prioriza procesamiento y almacenamiento local. Cuando existe conexión, el sistema puede consultar únicamente fuentes oficiales configuradas y guardar referencias útiles en una memoria local para futuras consultas. La organización mantiene el control sobre sus datos y protocolos."),("QUÉ INCLUYE","Triaje contextual · gestión de casos · seguimiento · dashboard · recursos y filtros · informes sociales · biblioteca local · agenda · seguridad y copias · configuración institucional · búsqueda en fuentes oficiales · memoria local · ayuda integrada."),("QUÉ NO HACE","No diagnostica, no reemplaza profesionales, no confirma por sí solo una emergencia, no determina responsabilidades legales y no debe ser la única fuente para decisiones de alto impacto. Los resultados automáticos son apoyo para organizar información y deben revisarse."),("NUBIWORKS","NubiWorks es mi proyecto y marca tecnológica, actualmente en proceso de formación. Su objetivo es crear software accesible, privado y útil, especialmente herramientas que puedan funcionar con recursos limitados y generar impacto social."),("SOBRE LA CREADORA","Mi nombre es Sarah Lee Olivera y soy una estudiante y desarrolladora de software de Argentina apasionada por crear tecnología con impacto social. Creo que la inteligencia artificial debe ser una herramienta para asistir a las personas, proteger su privacidad y facilitar el trabajo de quienes ayudan a otros. Mi interés se centra en aplicaciones, inteligencia artificial local (offline), accesibilidad y herramientas que puedan utilizarse en distintos contextos. Este software es un proyecto de código abierto orientado al bien común y busca apoyar a profesionales y voluntarios, nunca reemplazar su criterio ni la atención humana."),("TECNOLOGÍAS","Python · CustomTkinter · SQLite · procesamiento local · reglas explicables · generación de informes · almacenamiento local · consulta controlada de fuentes oficiales · memoria local · arquitectura preparada para Windows.")]
  for title,text in sections:self._section(scroll,title,text)
  ctk.CTkFrame(scroll,height=1,fg_color=COLORS["border"]).pack(fill="x",pady=18)
  ctk.CTkLabel(scroll,text="Sarah Lee Olivera",font=FONTS["heading"],text_color=COLORS["primary"]).pack(anchor="w"); ctk.CTkLabel(scroll,text="Creadora y desarrolladora · NubiWorks",font=FONTS["small"],text_color=COLORS["text_muted"]).pack(anchor="w",pady=(3,15))
 def _section(self,parent,title,text):
  card=ctk.CTkFrame(parent,fg_color=COLORS["surface_alt"],corner_radius=16,border_width=1,border_color=COLORS["border"]); card.pack(fill="x",pady=6)
  ctk.CTkLabel(card,text=title,font=FONTS["subheading"],text_color=COLORS["primary"],anchor="w").pack(fill="x",padx=20,pady=(15,6))
  body=ctk.CTkLabel(card,text=text,font=FONTS["body"],text_color=COLORS["text"],justify="left",anchor="w",wraplength=760); body.pack(fill="x",padx=20,pady=(0,18)); card.bind("<Configure>",lambda e,b=body:b.configure(wraplength=max(420,e.width-42)))

class MainWindow:
 def __init__(self):
  self.root=ctk.CTk(); self.root.title("Asistente ONG | Triaje y Canalización"); self.root.geometry("1500x900"); self.root.minsize(1120,720); self.root.configure(fg_color=COLORS["background"]); self.root.grid_rowconfigure(0,weight=1); self.root.grid_columnconfigure(0,weight=1); self.case_manager=CaseManager(); self.config_manager=ConfigManager(); self._setup_ui()
 def _setup_ui(self):
  main=ctk.CTkFrame(self.root,fg_color=COLORS["background"],corner_radius=0); main.grid(row=0,column=0,sticky="nsew"); main.grid_columnconfigure(0,weight=0,minsize=255); main.grid_columnconfigure(1,weight=1); main.grid_rowconfigure(0,weight=1)
  sidebar=ctk.CTkFrame(main,width=255,fg_color=COLORS["surface_alt"],corner_radius=0); sidebar.grid(row=0,column=0,sticky="nsew"); sidebar.grid_propagate(False)
  brand=ctk.CTkFrame(sidebar,fg_color=COLORS["surface"],corner_radius=18,border_width=1,border_color=COLORS["border"]); brand.pack(fill="x",padx=12,pady=12)
  try:
   path=Path(__file__).parent.parent.parent/"assets"/"logo_g.png"
   if path.exists():
    im=Image.open(path).convert("RGBA"); im.thumbnail((58,58)); li=ctk.CTkImage(light_image=im,size=(58,58)); lab=ctk.CTkLabel(brand,image=li,text=""); lab.image=li; lab.pack(side="left",padx=(10,8),pady=10)
  except Exception: pass
  titlebox=ctk.CTkFrame(brand,fg_color="transparent"); titlebox.pack(side="left",fill="x",expand=True); ctk.CTkLabel(titlebox,text="Asistente ONG",font=FONTS["heading"],text_color=COLORS["text"]).pack(anchor="w"); ctk.CTkLabel(titlebox,text="Triaje · Casos · Informes",font=FONTS["tiny"],text_color=COLORS["text_muted"]).pack(anchor="w",pady=(2,0)); ctk.CTkLabel(titlebox,text="NubiWorks",font=FONTS["small_bold"],text_color=COLORS["primary"]).pack(anchor="w",pady=(4,0))
  ctk.CTkButton(sidebar,text="＋  Nuevo caso",height=42,corner_radius=11,fg_color=COLORS["primary"],hover_color=COLORS["primary_dark"],font=FONTS["body_bold"],command=self.open_new_case).pack(fill="x",padx=12,pady=(2,12))
  nav=ctk.CTkScrollableFrame(sidebar,fg_color="transparent"); nav.pack(fill="both",expand=True,padx=6)
  self.nav_buttons=[]
  tabs=[("Inicio","Inicio"),("Casos","Casos"),("Análisis","Análisis"),("Seguimiento","Seguimiento"),("Informe Social","Informe Social"),("Recursos","Recursos"),("Biblioteca","Biblioteca"),("Agenda","Agenda"),("Seguridad","Seguridad"),("Configuración","Configuración"),("Ayuda","Ayuda"),("Acerca de","Acerca de")]
  for label,target in tabs:
   b=ctk.CTkButton(nav,text=label,height=36,anchor="w",corner_radius=9,fg_color="transparent",hover_color=COLORS["primary_soft"],text_color=COLORS["text"],font=FONTS["body"],command=lambda t=target:self.select_tab(t)); b.pack(fill="x",padx=4,pady=2); self.nav_buttons.append((target,b))
  status=ctk.CTkFrame(sidebar,fg_color=COLORS["primary_soft"],corner_radius=13); status.pack(fill="x",padx=12,pady=12); ctk.CTkLabel(status,text="●  OFFLINE-FIRST",font=FONTS["small_bold"],text_color=COLORS["primary"]).pack(anchor="w",padx=12,pady=(9,2)); ctk.CTkLabel(status,text="Datos y memoria en este equipo",font=FONTS["tiny"],text_color=COLORS["text_muted"]).pack(anchor="w",padx=12,pady=(0,9))
  center=ctk.CTkFrame(main,fg_color=COLORS["surface"],corner_radius=20,border_width=1,border_color=COLORS["border"]); center.grid(row=0,column=1,sticky="nsew",padx=(8,16),pady=14)
  top=ctk.CTkFrame(center,fg_color="transparent"); top.pack(fill="x",padx=24,pady=(18,4)); left=ctk.CTkFrame(top,fg_color="transparent"); left.pack(side="left"); ctk.CTkLabel(left,text="Centro de asistencia",font=FONTS["title"],text_color=COLORS["text"]).pack(anchor="w"); ctk.CTkLabel(left,text="Gestión local de casos, triaje, recursos y documentación",font=FONTS["small"],text_color=COLORS["text_muted"]).pack(anchor="w",pady=(3,0))
  self.status_badge=ctk.CTkLabel(top,text="●  COMPROBANDO...",font=FONTS["small_bold"],text_color=COLORS["primary"],fg_color=COLORS["primary_soft"],corner_radius=10); self.status_badge.pack(side="right",padx=4,pady=2)
  self.tab_view=ctk.CTkTabview(center,fg_color=COLORS["surface"],corner_radius=14,segmented_button_fg_color=COLORS["surface_alt"],segmented_button_selected_color=COLORS["primary"],segmented_button_selected_hover_color=COLORS["primary_dark"],segmented_button_unselected_color=COLORS["surface_alt"],segmented_button_unselected_hover_color=COLORS["primary_soft"],text_color=COLORS["text"],anchor="w"); self.tab_view.pack(fill="both",expand=True,padx=14,pady=(8,14)); self.tab_view._segmented_button.grid_remove()
  for name,cls in [("Inicio",DashboardFrame),("Casos",CasesPanel),("Análisis",ResultsFrame),("Seguimiento",FollowUpPanel),("Informe Social",SocialReportPanel),("Recursos",ResourcesPanel),("Biblioteca",LibraryPanel),("Agenda",AgendaPanel),("Seguridad",SecurityPanel),("Configuración",ConfigPanel),("Ayuda",HelpPanel),("Acerca de",AboutPanel)]:
   tab=self.tab_view.add(name); params=inspect.signature(cls.__init__).parameters; kwargs={"fg_color":COLORS["background"]};
   if "case_manager" in params: kwargs["case_manager"]=self.case_manager
   if "config_manager" in params: kwargs["config_manager"]=self.config_manager
   try: obj=cls(tab,**kwargs)
   except TypeError as exc: logger.warning("Constructor %s rechazó opcionales: %s",cls.__name__,exc); obj=cls(tab,fg_color=COLORS["background"])
   obj.pack(fill="both",expand=True); setattr(self,name.replace(" ","_").lower(),obj)
  self.select_tab("Inicio"); self.root.after(250,self._update_connection_badge)
 def select_tab(self,target):
  self.tab_view.set(target)
  for name,b in self.nav_buttons:
   active=name==target; b.configure(fg_color=COLORS["primary"] if active else "transparent",text_color=COLORS["surface"] if active else COLORS["text"])
 def open_new_case(self):
  win=ctk.CTkToplevel(self.root); win.title("Nuevo caso · Asistente ONG"); win.geometry("620x650"); win.minsize(560,560); win.configure(fg_color=COLORS["background"]); win.transient(self.root); win.grab_set()
  ctk.CTkLabel(win,text="Nuevo caso",font=FONTS["title"],text_color=COLORS["text"]).pack(anchor="w",padx=24,pady=(22,3)); ctk.CTkLabel(win,text="Ingresá el relato tal como fue recibido por la organización.",font=FONTS["small"],text_color=COLORS["text_muted"]).pack(anchor="w",padx=24,pady=(0,12))
  def submit(case_number,case_text): self._on_case_submit(case_number,case_text); win.destroy()
  frame=CaseInputFrame(win,on_submit=submit,fg_color=COLORS["background"]); frame.pack(fill="both",expand=True,padx=16,pady=4)
 def _update_connection_badge(self):
  try:
   from ..knowledge.official_web import internet_available
   online=internet_available(); self.status_badge.configure(text="●  INTERNET DISPONIBLE" if online else "●  MODO OFFLINE",text_color=COLORS["success"] if online else COLORS["warning"],fg_color=COLORS["success_soft"] if online else COLORS["warning_soft"])
  except Exception: pass
 def _on_case_submit(self,case_number,case_text):
  try:
   analysis=self.config_manager.analyze(case_text); case=self.case_manager.create_case(text=case_text,urgency=analysis["urgency"],keywords=analysis["keywords"]); self.analisis.show_analysis(case.case_number,case_text,analysis); self.select_tab("Análisis");
   try:self.inicio.update_stats(analysis["urgency"],"general",case.case_number)
   except Exception:pass
  except Exception as exc: logger.error("Error procesando caso: %s",exc,exc_info=True)
 def run(self): self.root.mainloop()
if __name__=="__main__": MainWindow().run()
