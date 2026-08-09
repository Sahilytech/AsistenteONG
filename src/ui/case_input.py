"""Ingreso guiado de casos."""
import customtkinter as ctk, logging
from .styles import COLORS,FONTS
logger=logging.getLogger(__name__)
class CaseInputFrame(ctk.CTkFrame):
 def __init__(self,parent,on_submit=None,**kwargs):
  super().__init__(parent,**kwargs); self.on_submit=on_submit; self.case_counter=0; self._setup_ui()
 def _setup_ui(self):
  ctk.CTkLabel(self,text="Nuevo caso",font=FONTS["heading"],text_color=COLORS["text"]).pack(anchor="w",padx=15,pady=(18,2))
  ctk.CTkLabel(self,text="Escribí o pegá el relato tal como lo recibió la organización.",font=FONTS["small"],text_color=COLORS["text_muted"],wraplength=280,justify="left").pack(anchor="w",padx=15,pady=(0,15))
  ctk.CTkLabel(self,text="ID del caso",font=FONTS["small"],text_color=COLORS["text_muted"]).pack(anchor="w", padx=15)
  self.case_number_entry=ctk.CTkEntry(self,placeholder_text="Se genera automáticamente",state="readonly",fg_color=COLORS["surface_alt"],border_color=COLORS["border"],text_color=COLORS["text"]); self.case_number_entry.pack(fill="x",padx=15,pady=(4,14))
  ctk.CTkLabel(self,text="Relato / mensaje",font=FONTS["subheading"],text_color=COLORS["text"]).pack(anchor="w",padx=15,pady=(0,5))
  self.text_input=ctk.CTkTextbox(self,height=240,font=FONTS["body"],fg_color=COLORS["surface"],text_color=COLORS["text"],border_width=1,border_color=COLORS["border"]); self.text_input.pack(fill="both",expand=True,padx=15,pady=(0,8))
  self.counter=ctk.CTkLabel(self,text="0 caracteres",font=FONTS["tiny"],text_color=COLORS["text_muted"]); self.counter.pack(anchor="e",padx=15,pady=(0,10)); self.text_input.bind("<KeyRelease>",self._count)
  hint=ctk.CTkFrame(self,fg_color=COLORS["primary_soft"],corner_radius=10); hint.pack(fill="x",padx=15,pady=(0,12)); ctk.CTkLabel(hint,text="El análisis es automático y orientativo. Revisá siempre el resultado antes de actuar.",font=FONTS["tiny"],text_color=COLORS["primary_dark"],wraplength=275,justify="left").pack(padx=10,pady=8)
  buttons=ctk.CTkFrame(self,fg_color="transparent"); buttons.pack(fill="x",padx=15,pady=(0,16))
  ctk.CTkButton(buttons,text="Analizar caso",command=self._on_analyze,fg_color=COLORS["primary"],hover_color=COLORS["primary_dark"],height=40).pack(fill="x",pady=(0,8))
  ctk.CTkButton(buttons,text="Limpiar",command=self._on_clear,fg_color=COLORS["surface_alt"],hover_color=COLORS["primary_soft"],text_color=COLORS["text"],border_width=1,border_color=COLORS["border"],height=34).pack(fill="x")
 def _count(self,event=None): self.counter.configure(text=f"{len(self.text_input.get('0.0','end').strip())} caracteres")
 def _on_analyze(self):
  text=self.text_input.get("0.0","end").strip()
  if not text:return
  self.case_counter+=1; case_num=f"CASE-202608-{self.case_counter:05d}"; self.case_number_entry.configure(state="normal"); self.case_number_entry.delete(0,"end"); self.case_number_entry.insert(0,case_num); self.case_number_entry.configure(state="readonly")
  if self.on_submit:self.on_submit(case_num,text)
  logger.info("Caso %s enviado",case_num)
 def _on_clear(self): self.text_input.delete("0.0","end"); self._count(); self.case_number_entry.configure(state="normal"); self.case_number_entry.delete(0,"end"); self.case_number_entry.configure(state="readonly")
