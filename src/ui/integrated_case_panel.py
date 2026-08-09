"""Espacio de trabajo que une un caso real con su informe social y análisis combinado."""
import customtkinter as ctk
from .styles import COLORS,FONTS
from ..config_manager import ConfigManager
from ..social_analyzer import SocialReportAnalyzer

FIELDS=[
 ("motivo","Motivo de la solicitud"),("miembros_hogar","Unidad de convivencia"),("historia_familiar","Historia familiar"),
 ("dinamica_familiar","Dinámica familiar"),("ingresos","Ingresos y sustento"),("situacion_laboral","Situación laboral"),
 ("egresos","Egresos básicos"),("tenencia","Tenencia de vivienda"),("condiciones_vivienda","Condiciones de vivienda"),
 ("servicios_entorno","Servicios y entorno"),("salud","Salud"),("educacion","Educación"),
 ("diagnostico","Valoración social"),("fortalezas","Fortalezas"),("vulnerabilidades","Vulnerabilidades"),("propuesta","Propuesta de intervención"),("observaciones","Observaciones")]

class IntegratedCasePanel(ctk.CTkFrame):
 def __init__(self,parent,case_manager=None,config_manager=None,**kwargs):
  super().__init__(parent,**kwargs); self.case_manager=case_manager; self.config_manager=config_manager or ConfigManager(); self.analysis=None; self.report={}; self.boxes={}; self._build(); self.refresh_cases()
 def _build(self):
  self.grid_columnconfigure(0,weight=1); self.grid_columnconfigure(1,weight=1); self.grid_rowconfigure(2,weight=1)
  head=ctk.CTkFrame(self,fg_color="transparent"); head.grid(row=0,column=0,columnspan=2,sticky="ew",padx=24,pady=(22,10)); ctk.CTkLabel(head,text="Caso + Informe Social",font=FONTS["title"],text_color=COLORS["text"]).pack(anchor="w"); ctk.CTkLabel(head,text="Unificá el relato del caso y la valoración social para obtener una única lectura contextual.",font=FONTS["small"],text_color=COLORS["text_muted"]).pack(anchor="w",pady=(3,0))
  selector=ctk.CTkFrame(self,fg_color=COLORS["surface_alt"],corner_radius=14,border_width=1,border_color=COLORS["border"]); selector.grid(row=1,column=0,columnspan=2,sticky="ew",padx=24,pady=(0,10)); selector.grid_columnconfigure(1,weight=1); ctk.CTkLabel(selector,text="Caso",font=FONTS["small_bold"],text_color=COLORS["text"]).grid(row=0,column=0,padx=(14,8),pady=12); self.case_menu=ctk.CTkOptionMenu(selector,values=["Sin casos"],command=self.load_case); self.case_menu.grid(row=0,column=1,sticky="ew",padx=8,pady=10); self.status=ctk.CTkLabel(selector,text="Seleccioná un caso existente.",font=FONTS["tiny"],text_color=COLORS["text_muted"]); self.status.grid(row=0,column=2,padx=14)
  left=ctk.CTkScrollableFrame(self,fg_color="transparent"); left.grid(row=2,column=0,sticky="nsew",padx=(24,8),pady=(0,20)); right=ctk.CTkScrollableFrame(self,fg_color="transparent"); right.grid(row=2,column=1,sticky="nsew",padx=(8,24),pady=(0,20));
  self._card(left,"Relato del caso","Seleccioná un caso para revisar su información.",attr="case_text")
  self._card(left,"Lectura actual","",attr="case_analysis")
  ctk.CTkLabel(right,text="Informe social aplicado",font=FONTS["heading"],text_color=COLORS["text"]).pack(anchor="w",pady=(0,8))
  for key,label in FIELDS:
   ctk.CTkLabel(right,text=label,font=FONTS["small_bold"],text_color=COLORS["text"],anchor="w").pack(fill="x",pady=(7,3)); box=ctk.CTkTextbox(right,height=65,fg_color=COLORS["surface"],border_width=1,border_color=COLORS["border"],text_color=COLORS["text"]); box.pack(fill="x"); self.boxes[key]=box
  buttons=ctk.CTkFrame(right,fg_color="transparent"); buttons.pack(fill="x",pady=12); ctk.CTkButton(buttons,text="Analizar todo junto",height=40,fg_color=COLORS["primary"],hover_color=COLORS["primary_dark"],command=self.analyze_combined).pack(side="left",fill="x",expand=True); ctk.CTkButton(buttons,text="Guardar en el caso",height=40,fg_color=COLORS["surface_alt"],hover_color=COLORS["primary_soft"],text_color=COLORS["primary"],border_width=1,border_color=COLORS["border"],command=self.save_to_case).pack(side="left",fill="x",expand=True,padx=(8,0))
  self.result=ctk.CTkLabel(right,text="El análisis combinado aparecerá acá.",font=FONTS["body"],text_color=COLORS["text"],justify="left",anchor="w",wraplength=520); self.result.pack(fill="x",pady=(0,18))
 def _card(self,parent,title,text,attr=None):
  card=ctk.CTkFrame(parent,fg_color=COLORS["surface"],corner_radius=14,border_width=1,border_color=COLORS["border"]); card.pack(fill="x",pady=6); ctk.CTkLabel(card,text=title,font=FONTS["heading"],text_color=COLORS["primary"],anchor="w").pack(fill="x",padx=16,pady=(14,5)); lab=ctk.CTkLabel(card,text=text,font=FONTS["body"],text_color=COLORS["text"],justify="left",anchor="w",wraplength=520); lab.pack(fill="x",padx=16,pady=(0,16));
  if attr:setattr(self,attr,lab)
 def refresh_cases(self):
  cases=self.case_manager.get_all_cases() if self.case_manager else []; self.case_map={c.case_number:c for c in cases}; values=list(self.case_map) or ["Sin casos"]; self.case_menu.configure(values=values); self.case_menu.set(values[0]); self.load_case(values[0]) if cases else self.clear_view()
 def clear_view(self): self.case_text.configure(text="No hay casos registrados."); self.case_analysis.configure(text="Creá un caso desde Casos para poder aplicar un informe social."); self.status.configure(text="Sin casos")
 def load_case(self,number):
  case=self.case_map.get(number); 
  if not case:return self.clear_view()
  self.current_case=case; self.status.configure(text=f"Prioridad: {case.urgency} · Estado: {case.status}"); self.case_text.configure(text=case.text); analysis=case.combined_analysis or {}; self.case_analysis.configure(text=self._analysis_summary(analysis) if analysis else "Todavía no hay un análisis combinado guardado para este caso.")
  report=case.social_report or {}; self.report=report
  for key,box in self.boxes.items(): box.delete("1.0","end"); box.insert("1.0",str(report.get(key,"")))
 def collect_report(self):
  return {key:box.get("1.0","end").strip() for key,box in self.boxes.items() if box.get("1.0","end").strip()}
 def analyze_combined(self):
  if not getattr(self,"current_case",None): self.status.configure(text="Primero seleccioná un caso."); return
  self.report=self.collect_report(); self.analysis=self.config_manager.analyze(self.current_case.text,self.report); self.result.configure(text=self._analysis_summary(self.analysis)); self.status.configure(text=f"Análisis combinado: {self.analysis['urgency']}")
 def save_to_case(self):
  if not getattr(self,"current_case",None): self.status.configure(text="Primero seleccioná un caso."); return
  if self.analysis is None:self.analyze_combined()
  self.case_manager.attach_social_report(self.current_case.case_number,self.collect_report(),self.analysis); self.refresh_cases(); self.case_menu.set(self.current_case.case_number); self.status.configure(text="Informe y análisis guardados en el caso.")
 def _analysis_summary(self,a):
  if not a:return "Sin análisis disponible."
  lines=[f"PRIORIDAD: {a.get('urgency','—')}",f"CLASIFICACIÓN: {a.get('classification','—')}",f"CONFIANZA: {a.get('confidence','—')}",f"CONTEXTO: {a.get('detected_context','—')}",f"MOTIVO: {a.get('priority_reason','—')}"]
  kws=a.get("keywords",[]); lines.append("PALABRAS CLAVE: "+(", ".join(kws) if kws else "ninguna")); res=a.get("suggested_resources",[]); lines.append("RECURSOS: "+(", ".join(res) if res else "ninguno")); qs=a.get("next_questions",[]); lines.append("PREGUNTAS PENDIENTES: "+(" · ".join(qs) if qs else "ninguna")); return "\n".join(lines)
