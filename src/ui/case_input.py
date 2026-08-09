"""Editor integrado para crear, revisar y enviar casos sin ventanas emergentes."""
import customtkinter as ctk, logging
from .styles import COLORS,FONTS
logger=logging.getLogger(__name__)

class CaseInputFrame(ctk.CTkFrame):
    def __init__(self,parent,on_submit=None,**kwargs):
        super().__init__(parent,**kwargs); self.on_submit=on_submit; self._setup_ui()
    def _setup_ui(self):
        self.grid_columnconfigure(0,weight=1); self.grid_rowconfigure(3,weight=1)
        ctk.CTkLabel(self,text="Nuevo caso",font=FONTS["title"],text_color=COLORS["text"]).grid(row=0,column=0,sticky="w",padx=22,pady=(22,3))
        ctk.CTkLabel(self,text="Registrá, editá y revisá el relato antes de enviarlo al análisis local.",font=FONTS["small"],text_color=COLORS["text_muted"]).grid(row=1,column=0,sticky="w",padx=22,pady=(0,16))
        meta=ctk.CTkFrame(self,fg_color=COLORS["surface_alt"],corner_radius=12,border_width=1,border_color=COLORS["border"]); meta.grid(row=2,column=0,sticky="ew",padx=22,pady=(0,12)); meta.grid_columnconfigure(1,weight=1)
        ctk.CTkLabel(meta,text="ID del caso",font=FONTS["small_bold"],text_color=COLORS["text_muted"]).grid(row=0,column=0,padx=14,pady=11)
        self.case_number_entry=ctk.CTkEntry(meta,placeholder_text="Se asignará al guardar",state="readonly",fg_color=COLORS["surface"],border_color=COLORS["border"],text_color=COLORS["text"]); self.case_number_entry.grid(row=0,column=1,sticky="ew",padx=(0,14),pady=8)
        editor=ctk.CTkFrame(self,fg_color="transparent"); editor.grid(row=3,column=0,sticky="nsew",padx=22); editor.grid_columnconfigure(0,weight=1); editor.grid_rowconfigure(1,weight=1)
        ctk.CTkLabel(editor,text="Relato / mensaje recibido",font=FONTS["subheading"],text_color=COLORS["text"]).grid(row=0,column=0,sticky="w",pady=(0,6))
        self.text_input=ctk.CTkTextbox(editor,font=FONTS["body"],fg_color=COLORS["surface"],text_color=COLORS["text"],border_width=1,border_color=COLORS["border"]); self.text_input.grid(row=1,column=0,sticky="nsew"); self.text_input.bind("<KeyRelease>",self._count)
        footer=ctk.CTkFrame(self,fg_color="transparent"); footer.grid(row=4,column=0,sticky="ew",padx=22,pady=(8,18)); footer.grid_columnconfigure(0,weight=1)
        self.counter=ctk.CTkLabel(footer,text="0 caracteres",font=FONTS["tiny"],text_color=COLORS["text_muted"]); self.counter.grid(row=0,column=0,sticky="w")
        ctk.CTkButton(footer,text="Limpiar",width=100,height=38,fg_color=COLORS["surface_alt"],hover_color=COLORS["primary_soft"],text_color=COLORS["text"],border_width=1,border_color=COLORS["border"],command=self._on_clear).grid(row=0,column=1,padx=5)
        ctk.CTkButton(footer,text="Guardar y analizar",width=170,height=38,fg_color=COLORS["primary"],hover_color=COLORS["primary_dark"],font=FONTS["body_bold"],command=self._on_analyze).grid(row=0,column=2,padx=(5,0))
    def _count(self,event=None): self.counter.configure(text=f"{len(self.text_input.get('1.0','end').strip())} caracteres")
    def _on_analyze(self):
        text=self.text_input.get("1.0","end").strip()
        if not text:
            self.counter.configure(text="Escribí un relato antes de guardar"); return
        if self.on_submit:self.on_submit("",text)
        logger.info("Caso enviado al flujo integrado")
    def _on_clear(self):
        self.text_input.delete("1.0","end"); self._count(); self.case_number_entry.configure(state="normal"); self.case_number_entry.delete(0,"end"); self.case_number_entry.configure(state="readonly")
