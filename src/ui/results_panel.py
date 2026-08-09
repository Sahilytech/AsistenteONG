"""Panel de resultados: lectura rápida, evidencia y próximos pasos."""
import customtkinter as ctk
from .styles import COLORS,FONTS

class ResultsFrame(ctk.CTkFrame):
 def __init__(self,parent,config_manager=None,**kwargs):
  super().__init__(parent,**kwargs); self.config_manager=config_manager; self.current_case=None; self._setup_ui()
 def _setup_ui(self):
  self.grid_columnconfigure(0,weight=1); self.grid_rowconfigure(0,weight=1)
  scroll=ctk.CTkScrollableFrame(self,fg_color="transparent"); scroll.grid(row=0,column=0,sticky="nsew",padx=24,pady=20)
  ctk.CTkLabel(scroll,text="Análisis integral",font=FONTS["title"],text_color=COLORS["text"]).pack(anchor="w")
  ctk.CTkLabel(scroll,text="El sistema separa contexto de indicadores y explica por qué propone una prioridad. Revisá siempre el relato completo.",font=FONTS["small"],text_color=COLORS["text_muted"],wraplength=1000,justify="left").pack(anchor="w",pady=(3,18))
  self.case_label=ctk.CTkLabel(scroll,text="Sin caso seleccionado",font=FONTS["heading"],text_color=COLORS["text"]); self.case_label.pack(anchor="w")
  self.meta=ctk.CTkLabel(scroll,text="Esperando análisis",font=FONTS["small"],text_color=COLORS["text_muted"],wraplength=1000,justify="left"); self.meta.pack(anchor="w",pady=(2,12))
  self.priority_card=self._card(scroll,"PRIORIDAD Y CRITERIO",height=None)
  self.priority_value=ctk.CTkLabel(self.priority_card,text="—",font=FONTS["title"],text_color=COLORS["text"]); self.priority_value.pack(anchor="w",padx=18,pady=(0,3))
  self.reason=ctk.CTkLabel(self.priority_card,text="",font=FONTS["small"],text_color=COLORS["text_muted"],wraplength=980,justify="left",anchor="w"); self.reason.pack(fill="x",padx=18,pady=(0,14))
  self._make_section(scroll,"LECTURA DEL CASO", "classification_label")
  self._make_section(scroll,"SEÑALES DETECTADAS", "signals_label")
  self._make_section(scroll,"ANÁLISIS", "analysis_label")
  self._make_section(scroll,"PREGUNTAS PARA COMPLETAR", "questions_label")
  self._make_section(scroll,"RECURSOS / DERIVACIONES A CONSIDERAR", "resources_label")
  note=self._card(scroll,"CRITERIO PROFESIONAL",None)
  self.note_label=ctk.CTkLabel(note,text="",font=FONTS["small"],text_color=COLORS["text_muted"],wraplength=980,justify="left",anchor="w"); self.note_label.pack(fill="x",padx=18,pady=(0,14))
  buttons=ctk.CTkFrame(scroll,fg_color="transparent"); buttons.pack(fill="x",pady=(4,10)); ctk.CTkButton(buttons,text="Copiar resumen",command=self._copy_text,fg_color=COLORS["primary"],hover_color=COLORS["primary_dark"]).pack(side="left",padx=(0,8)); ctk.CTkButton(buttons,text="Editar borrador",command=self._edit_text,fg_color=COLORS["surface_alt"],hover_color=COLORS["primary_soft"],text_color=COLORS["text"],border_width=1,border_color=COLORS["border"]).pack(side="left")
  self._summary="Ingresá un caso para ver el análisis."
 def _card(self,parent,title,height):
  card=ctk.CTkFrame(parent,fg_color=COLORS["surface_alt"],corner_radius=14,border_width=1,border_color=COLORS["border"]); card.pack(fill="x",pady=(0,10)); ctk.CTkLabel(card,text=title,font=FONTS["tiny"],text_color=COLORS["primary"]).pack(anchor="w",padx=18,pady=(12,7)); return card
 def _make_section(self,parent,title,attr):
  card=self._card(parent,title,None); label=ctk.CTkLabel(card,text="—",font=FONTS["body"],text_color=COLORS["text"],wraplength=980,justify="left",anchor="w"); label.pack(fill="x",padx=18,pady=(0,14)); setattr(self,attr,label)
 def show_analysis(self,case_number,case_text,analysis):
  self.current_case={"number":case_number,"text":case_text,"analysis":analysis}
  u=analysis.get("urgency","Baja"); k=analysis.get("keywords",[]); risk=analysis.get("risk_keywords",[]); ctx=analysis.get("context_keywords",[]); cls=analysis.get("classification","Consulta social"); conf=analysis.get("confidence","Media"); detected=analysis.get("detected_context","Consulta general"); questions=analysis.get("next_questions",[]); resources=analysis.get("suggested_resources",[])
  self.case_label.configure(text=f"{case_number} · {cls}")
  social=" · Informe social integrado" if analysis.get("combined_with_social_report") else ""
  self.meta.configure(text=f"Prioridad: {u} · Confianza orientativa: {conf} · Contexto: {detected}{social}")
  self.priority_value.configure(text=u); self.reason.configure(text=analysis.get("priority_reason","Revisar manualmente el resultado."))
  self.classification_label.configure(text=f"Clasificación: {cls}\nContexto principal: {detected}\nConfianza orientativa: {conf}")
  signals=[]
  if risk: signals.append("Indicadores concretos: " + ", ".join(risk))
  if ctx: signals.append("Contexto: " + ", ".join(ctx))
  if not signals: signals=["No se detectaron señales específicas con las reglas actuales."]
  self.signals_label.configure(text="\n".join(signals))
  self.analysis_label.configure(text=analysis.get("response","Sin análisis disponible."))
  self.questions_label.configure(text="\n".join(f"• {x}" for x in questions) if questions else "No hay preguntas automáticas adicionales.")
  self.resources_label.configure(text="\n".join(f"• {x}" for x in resources) if resources else "No se sugirieron recursos automáticamente. Revisar directorio local de recursos.")
  self.note_label.configure(text=analysis.get("context_note","Revisar manualmente el resultado antes de intervenir."))
  self._summary=self._build_summary(case_number,analysis)
 def _build_summary(self,case_number,a):
  def bullets(items):return "\n".join("• "+str(x) for x in items) if items else "• Ninguno"
  return f"CASO: {case_number}\nPRIORIDAD: {a.get('urgency','Baja')}\nCLASIFICACIÓN: {a.get('classification','Consulta social')}\nCONTEXTO: {a.get('detected_context','Consulta general')}\nCONFIANZA: {a.get('confidence','Baja')}\n\nINDICADORES\n{bullets(a.get('risk_keywords',[]))}\n\nCONTEXTO DETECTADO\n{bullets(a.get('context_keywords',[]))}\n\nCRITERIO\n{a.get('priority_reason','')}\n\nANÁLISIS\n{a.get('response','')}\n\nPREGUNTAS\n{bullets(a.get('next_questions',[]))}\n\nRECURSOS\n{bullets(a.get('suggested_resources',[]))}\n"
 def _copy_text(self):
  self.winfo_toplevel().clipboard_clear(); self.winfo_toplevel().clipboard_append(self._summary)
 def _edit_text(self):
  # Mantener el resultado visible y permitir edición mediante una ventana separada en una futura iteración.
  self._summary=self._summary
