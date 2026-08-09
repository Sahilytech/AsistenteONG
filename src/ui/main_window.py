"""Ventana principal del Asistente ONG: interfaz clara, accesible y offline."""
import customtkinter as ctk
import logging
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
  super().__init__(parent,**kwargs); scroll=ctk.CTkScrollableFrame(self,fg_color="transparent"); scroll.pack(fill="both",expand=True,padx=30,pady=24)
  ctk.CTkLabel(scroll,text="Acerca de Asistente ONG",font=FONTS["title"],text_color=COLORS["text"]).pack(anchor="w")
  ctk.CTkLabel(scroll,text="Proyecto de NubiWorks · tecnología offline para apoyo social",font=FONTS["subheading"],text_color=COLORS["primary"]).pack(anchor="w",pady=(4,18))
  sections=[("EL PROYECTO","Asistente ONG es una suite de escritorio orientada a organizaciones sociales, fundaciones y equipos de asistencia. Ayuda a organizar relatos, realizar un triaje contextual orientativo, gestionar casos, preparar informes, consultar recursos y mantener seguimientos en un entorno local."),("EL PROBLEMA","Los equipos pequeños pueden recibir muchos mensajes y consultas mientras cuentan con tiempo y recursos limitados. El proyecto busca reducir tareas repetitivas de clasificación y organización sin convertir la automatización en una sustitución del criterio profesional."),("CÓMO FUNCIONA","El flujo comienza con el relato recibido. El motor local identifica contexto e indicadores, estima una prioridad orientativa, explica qué encontró, señala información faltante y sugiere recursos. Luego el profesional revisa, corrige cuando corresponda y decide la intervención."),("PRIVACIDAD Y OFFLINE","La arquitectura prioriza procesamiento y almacenamiento local. El modo offline está pensado para minimizar exposición de información sensible y permitir uso en contextos con conectividad limitada. Cada organización debe aplicar sus propias políticas de protección de datos y protocolos."),("QUÉ INCLUYE","Triaje contextual · gestión de casos · seguimiento · dashboard · recursos y filtros · informes sociales · biblioteca local · agenda · seguridad y copias · configuración institucional · ayuda integrada · preparación para Windows."),("QUÉ NO HACE","No diagnostica, no reemplaza profesionales, no confirma por sí solo una emergencia, no determina responsabilidades legales y no debe ser la única fuente para decisiones de alto impacto. Los resultados automáticos son apoyo para organizar información y deben revisarse."),("NUBIWORKS","NubiWorks es mi proyecto y marca tecnológica, actualmente en proceso de formación. Su objetivo es crear software accesible, privado y útil, especialmente herramientas que puedan funcionar con recursos limitados y generar impacto social."),("SOBRE LA CREADORA","Mi nombre es Sarah Lee Olivera y soy una estudiante y desarrolladora de software de Argentina apasionada por crear tecnología con impacto social. Creo que la inteligencia artificial debe ser una herramienta para asistir a las personas, proteger su privacidad y facilitar el trabajo de quienes ayudan a otros. Mi interés se centra en aplicaciones, inteligencia artificial local (offline), accesibilidad y herramientas que puedan utilizarse en distintos contextos. Este software es un proyecto de código abierto orientado al bien común y busca apoyar a profesionales y voluntarios, nunca reemplazar su criterio ni la atención humana."),("TECNOLOGÍAS","Python · CustomTkinter · SQLite · procesamiento local · reglas explicables · generación de informes · almacenamiento local · arquitectura preparada para distribución como aplicación Windows.")]
  for title,text in sections:self._section(scroll,title,text)
  ctk.CTkFrame(scroll,height=1,fg_color=COLORS["border"]).pack(fill="x",pady=20)
  ctk.CTkLabel(scroll,text="Sarah Lee Olivera",font=FONTS["heading"],text_color=COLORS["primary"]).pack(anchor="w"); ctk.CTkLabel(scroll,text="Creadora y desarrolladora · NubiWorks",font=FONTS["small"],text_color=COLORS["text_muted"]).pack(anchor="w",pady=(3,15))
 def _section(self,parent,title,text):
  card=ctk.CTkFrame(parent,fg_color=COLORS["surface_alt"],corner_radius=14); card.pack(fill="x",pady=7); ctk.CTkLabel(card,text=title,font=FONTS["subheading"],text_color=COLORS["primary"]).pack(anchor="w",padx=20,pady=(16,5)); ctk.CTkLabel(card,text=text,font=FONTS["body"],text_color=COLORS["text"],justify="left",anchor="w",wraplength=1050).pack(fill="x",padx=20,pady=(0,18))

class MainWindow:
 def __init__(self):
  self.root=ctk.CTk(); self.root.title("Asistente ONG | Triaje y Canalización"); self.root.geometry("1500x900"); self.root.minsize(1100,700); self.root.configure(fg_color=COLORS["background"]); self.root.grid_rowconfigure(0,weight=1); self.root.grid_columnconfigure(0,weight=1); self.case_manager=CaseManager(); self.config_manager=ConfigManager(); self._setup_ui()
 def _setup_ui(self):
  main=ctk.CTkFrame(self.root,fg_color=COLORS["background"]); main.grid(row=0,column=0,sticky="nsew"); main.grid_columnconfigure(0,weight=0); main.grid_columnconfigure(1,weight=1); main.grid_rowconfigure(0,weight=1)
  sidebar=ctk.CTkFrame(main,width=330,fg_color=COLORS["background"],corner_radius=0); sidebar.grid(row=0,column=0,sticky="nsew"); sidebar.grid_propagate(False)
  header=ctk.CTkFrame(sidebar,fg_color=COLORS["surface_alt"],corner_radius=14); header.pack(fill="x",padx=14,pady=14)
  try:
   path=Path(__file__).parent.parent.parent/"assets"/"logo_g.png"
   if path.exists():
    im=Image.open(path).resize((58,58),Image.Resampling.LANCZOS); li=ctk.CTkImage(light_image=im,size=(58,58)); lab=ctk.CTkLabel(header,image=li,text=""); lab.image=li; lab.pack(side="left",padx=(12,10),pady=12)
  except Exception: pass
  titlebox=ctk.CTkFrame(header,fg_color="transparent"); titlebox.pack(side="left",fill="x",expand=True); ctk.CTkLabel(titlebox,text="Asistente ONG",font=FONTS["heading"],text_color=COLORS["text"]).pack(anchor="w"); ctk.CTkLabel(titlebox,text="Triaje · Casos · Informes",font=FONTS["tiny"],text_color=COLORS["text_muted"]).pack(anchor="w")
  self.case_input=CaseInputFrame(sidebar,on_submit=self._on_case_submit,fg_color=COLORS["background"]); self.case_input.pack(fill="both",expand=True,padx=8)
  status=ctk.CTkFrame(sidebar,fg_color=COLORS["primary_soft"],corner_radius=10); status.pack(fill="x",padx=14,pady=14); ctk.CTkLabel(status,text="● OFFLINE 100%  ·  DATOS LOCALES",font=FONTS["small"],text_color=COLORS["primary"]).pack(anchor="w",padx=12,pady=8)
  center=ctk.CTkFrame(main,fg_color=COLORS["surface"],corner_radius=16,border_width=1,border_color=COLORS["border"]); center.grid(row=0,column=1,sticky="nsew",padx=(0,16),pady=16)
  toolbar=ctk.CTkFrame(center,fg_color="transparent"); toolbar.pack(fill="x",padx=22,pady=(18,6)); ctk.CTkLabel(toolbar,text="Centro de asistencia",font=FONTS["title"],text_color=COLORS["text"]).pack(side="left"); ctk.CTkLabel(toolbar,text="  ·  Suite local de gestión social",font=FONTS["small"],text_color=COLORS["text_muted"]).pack(side="left",pady=(6,0))
  self.tab_view=ctk.CTkTabview(center,fg_color=COLORS["surface"],segmented_button_fg_color=COLORS["surface_alt"],segmented_button_selected_color=COLORS["primary"],segmented_button_selected_hover_color=COLORS["primary_dark"],segmented_button_unselected_color=COLORS["surface_alt"],segmented_button_unselected_hover_color=COLORS["primary_soft"],text_color=COLORS["text"]); self.tab_view.pack(fill="both",expand=True,padx=14,pady=10)
  tabs=[("Inicio",DashboardFrame),("Casos",CasesPanel),("Análisis",ResultsFrame),("Seguimiento",FollowUpPanel),("Informe Social",SocialReportPanel),("Recursos",ResourcesPanel),("Biblioteca",LibraryPanel),("Agenda",AgendaPanel),("Seguridad",SecurityPanel),("Configuración",ConfigPanel),("Ayuda",HelpPanel),("Acerca de",AboutPanel)]
  for name,cls in tabs:
   tab=self.tab_view.add(name)
   try:
    obj=cls(tab,case_manager=self.case_manager,config_manager=self.config_manager,fg_color=COLORS["background"])
   except TypeError:
    obj=cls(tab,fg_color=COLORS["background"])
   obj.pack(fill="both",expand=True)
   setattr(self,name.replace(" ","_").lower(),obj)
 def _on_case_submit(self,case_number,case_text):
  try:
   analysis=self.config_manager.analyze(case_text); case=self.case_manager.create_case(text=case_text,urgency=analysis["urgency"],keywords=analysis["keywords"]); self.analisis.show_analysis(case.case_number,case_text,analysis); self.tab_view.set("Análisis")
   try:self.inicio.update_stats(analysis["urgency"],"general",case.case_number)
   except Exception:pass
  except Exception as exc: logger.error("Error procesando caso: %s",exc,exc_info=True)
 def run(self): self.root.mainloop()
if __name__=="__main__": MainWindow().run()
