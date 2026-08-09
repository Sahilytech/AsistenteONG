"""Resultados explicables y accionables."""
import customtkinter as ctk, logging
from .styles import COLORS,FONTS
logger=logging.getLogger(__name__)
class ResultsFrame(ctk.CTkFrame):
 def __init__(self,parent,config_manager=None,**kwargs):
  super().__init__(parent,**kwargs); self.config_manager=config_manager; self.current_case=None; self._setup_ui()
 def _setup_ui(self):
  scroll=ctk.CTkScrollableFrame(self,fg_color="transparent"); scroll.pack(fill="both",expand=True,padx=22,pady=18)
  ctk.CTkLabel(scroll,text="Análisis del caso",font=FONTS["title"],text_color=COLORS["text"]).pack(anchor="w")
  ctk.CTkLabel(scroll,text="Revisá la clasificación, el contexto detectado y las preguntas pendientes antes de tomar una decisión.",font=FONTS["small"],text_color=COLORS["text_muted"],wraplength=900,justify="left").pack(anchor="w",pady=(3,18))
  self.summary=ctk.CTkFrame(scroll,fg_color=COLORS["surface_alt"],corner_radius=14); self.summary.pack(fill="x",pady=(0,14))
  self.case_label=ctk.CTkLabel(self.summary,text="Sin caso seleccionado",font=FONTS["heading"],text_color=COLORS["text"]); self.case_label.pack(anchor="w",padx=18,pady=(14,2))
  self.meta=ctk.CTkLabel(self.summary,text="Esperando análisis",font=FONTS["small"],text_color=COLORS["text_muted"]); self.meta.pack(anchor="w",padx=18,pady=(0,14))
  self.result_text=ctk.CTkTextbox(scroll,height=370,font=FONTS["body"],text_color=COLORS["text"],fg_color=COLORS["surface"],border_width=1,border_color=COLORS["border"]); self.result_text.pack(fill="both",expand=True,pady=(0,12)); self.result_text.insert("0.0","Ingresá un caso para ver el análisis."); self.result_text.configure(state="disabled")
  buttons=ctk.CTkFrame(scroll,fg_color="transparent"); buttons.pack(fill="x")
  ctk.CTkButton(buttons,text="Copiar resultado",command=self._copy_text,fg_color=COLORS["primary"],hover_color=COLORS["primary_dark"]).pack(side="left",padx=(0,8))
  ctk.CTkButton(buttons,text="Editar borrador",command=self._edit_text,fg_color=COLORS["surface_alt"],hover_color=COLORS["primary_soft"],text_color=COLORS["text"],border_width=1,border_color=COLORS["border"]).pack(side="left")
 def show_analysis(self,case_number,case_text,analysis):
  self.current_case={"number":case_number,"text":case_text,"analysis":analysis}; u=analysis.get("urgency","Baja"); k=analysis.get("keywords",[]); r=analysis.get("response",""); res=analysis.get("suggested_resources",[]); cls=analysis.get("classification","Triaje social"); conf=analysis.get("confidence","Media"); ctx=analysis.get("detected_context","Consulta general"); questions=analysis.get("next_questions",[])
  self.case_label.configure(text=f"{case_number}  ·  {cls}"); self.meta.configure(text=f"Prioridad: {u}   |   Confianza orientativa: {conf}   |   Contexto: {ctx}")
  q="\n".join(f"• {x}" for x in questions)
  text=f"PRIORIDAD\n{u}\n\nCONTEXTO DETECTADO\n{ctx}\n\nPALABRAS / INDICADORES\n{', '.join(k) if k else 'Ninguno'}\n\nANÁLISIS\n{r}\n\nPREGUNTAS PENDIENTES\n{q}\n\nRECURSOS SUGERIDOS\n{', '.join(res) if res else 'Ninguno'}\n\nNOTA PROFESIONAL\n{analysis.get('context_note','Revisar manualmente el resultado antes de intervenir.')}\n"
  self.result_text.configure(state="normal"); self.result_text.delete("0.0","end"); self.result_text.insert("0.0",text); self.result_text.configure(state="disabled")
 def _copy_text(self):
  self.result_text.configure(state="normal"); text=self.result_text.get("0.0","end"); self.result_text.configure(state="disabled"); self.winfo_toplevel().clipboard_clear(); self.winfo_toplevel().clipboard_append(text)
 def _edit_text(self): self.result_text.configure(state="normal" if self.result_text.cget("state")=="disabled" else "disabled")
