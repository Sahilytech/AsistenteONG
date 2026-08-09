"""Resultados explicables, claros y accionables."""
import customtkinter as ctk
from .styles import COLORS,FONTS
class ResultsFrame(ctk.CTkFrame):
 def __init__(self,parent,config_manager=None,**kwargs):
  super().__init__(parent,**kwargs); self.config_manager=config_manager; self.current_case=None; self._setup_ui()
 def _setup_ui(self):
  self.grid_columnconfigure(0,weight=1); self.grid_rowconfigure(0,weight=1); scroll=ctk.CTkScrollableFrame(self,fg_color="transparent"); scroll.grid(row=0,column=0,sticky="nsew",padx=24,pady=20)
  ctk.CTkLabel(scroll,text="Análisis del caso",font=FONTS["title"],text_color=COLORS["text"]).pack(anchor="w"); ctk.CTkLabel(scroll,text="El sistema ordena indicadores para ayudar al operador. Revisá siempre el relato y confirmá el contexto antes de actuar.",font=FONTS["small"],text_color=COLORS["text_muted"],wraplength=900,justify="left").pack(anchor="w",pady=(3,18))
  self.case_label=ctk.CTkLabel(scroll,text="Sin caso seleccionado",font=FONTS["heading"],text_color=COLORS["text"]); self.case_label.pack(anchor="w"); self.meta=ctk.CTkLabel(scroll,text="Esperando análisis",font=FONTS["small"],text_color=COLORS["text_muted"]); self.meta.pack(anchor="w",pady=(2,12))
  card=ctk.CTkFrame(scroll,fg_color=COLORS["surface_alt"],corner_radius=14,border_width=1,border_color=COLORS["border"]); card.pack(fill="x",pady=(0,10)); ctk.CTkLabel(card,text="PRIORIDAD",font=FONTS["tiny"],text_color=COLORS["primary"]).pack(anchor="w",padx=18,pady=(12,2)); self.priority_value=ctk.CTkLabel(card,text="—",font=FONTS["title"],text_color=COLORS["text"]); self.priority_value.pack(anchor="w",padx=18,pady=(0,4)); self.reason=ctk.CTkLabel(card,text="",font=FONTS["small"],text_color=COLORS["text_muted"],wraplength=850,justify="left"); self.reason.pack(anchor="w",padx=18,pady=(0,14))
  self.result_text=ctk.CTkTextbox(scroll,height=430,font=FONTS["body"],text_color=COLORS["text"],fg_color=COLORS["surface"],border_width=1,border_color=COLORS["border"]); self.result_text.pack(fill="both",expand=True,pady=(0,12)); self.result_text.insert("0.0","Ingresá un caso para ver el análisis."); self.result_text.configure(state="disabled")
  ctk.CTkButton(scroll,text="Copiar resultado",command=self._copy_text,fg_color=COLORS["primary"],hover_color=COLORS["primary_dark"]).pack(anchor="w")
 def show_analysis(self,case_number,case_text,analysis):
  self.current_case={"number":case_number,"text":case_text,"analysis":analysis}; u=analysis.get("urgency","Baja"); k=analysis.get("keywords",[]); r=analysis.get("response",""); res=analysis.get("suggested_resources",[]); cls=analysis.get("classification","Triaje social"); conf=analysis.get("confidence","Media"); ctx=analysis.get("detected_context","Consulta general"); questions=analysis.get("next_questions",[])
  self.case_label.configure(text=f"{case_number} · {cls}"); self.meta.configure(text=f"Confianza orientativa: {conf} · Contexto: {ctx}"); self.priority_value.configure(text=u); self.reason.configure(text=analysis.get("priority_reason","Revisar manualmente el resultado."))
  q="\n".join(f"• {x}" for x in questions); text=f"CONTEXTO DETECTADO\n{ctx}\n\nPALABRAS / INDICADORES\n{', '.join(k) if k else 'Ninguno'}\n\nANÁLISIS\n{r}\n\nPREGUNTAS PENDIENTES\n{q}\n\nRECURSOS SUGERIDOS\n{', '.join(res) if res else 'Ninguno'}\n\nNOTA PROFESIONAL\n{analysis.get('context_note','Revisar manualmente el resultado antes de intervenir.')}\n"
  self.result_text.configure(state="normal"); self.result_text.delete("0.0","end"); self.result_text.insert("0.0",text); self.result_text.configure(state="disabled")
 def _copy_text(self):
  self.result_text.configure(state="normal"); text=self.result_text.get("0.0","end"); self.result_text.configure(state="disabled"); self.winfo_toplevel().clipboard_clear(); self.winfo_toplevel().clipboard_append(text)
