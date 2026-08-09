"""Alta de caso: datos básicos y relato en una única pantalla, antes del análisis."""
import customtkinter as ctk,logging
from .styles import COLORS,FONTS
logger=logging.getLogger(__name__)
class CaseInputFrame(ctk.CTkFrame):
    def __init__(self,parent,on_submit=None,**kwargs): super().__init__(parent,**kwargs); self.on_submit=on_submit; self._setup_ui()
    def _setup_ui(self):
        self.grid_columnconfigure(0,weight=1); self.grid_rowconfigure(4,weight=1)
        ctk.CTkLabel(self,text="Nuevo caso",font=FONTS["title"],text_color=COLORS["text"]).grid(row=0,column=0,sticky="w",padx=22,pady=(10,2))
        ctk.CTkLabel(self,text="Completá los datos disponibles y el relato. Todo queda dentro del mismo caso; después se realiza el análisis local.",font=FONTS["small"],text_color=COLORS["text_muted"],wraplength=900,justify="left").grid(row=1,column=0,sticky="w",padx=22,pady=(0,12))
        data=ctk.CTkFrame(self,fg_color=COLORS["surface"],corner_radius=14,border_width=1,border_color=COLORS["border"]); data.grid(row=2,column=0,sticky="ew",padx=22,pady=(0,10)); data.grid_columnconfigure((1,3),weight=1)
        fields=[("Nombre / alias","Opcional"),("Contacto","Opcional"),("Tipo de caso","Violencia, legal, social..."),("Localidad / zona","Opcional")]; self.entries={}
        for i,(label,placeholder) in enumerate(fields):
            r=i//2; c=(i%2)*2; ctk.CTkLabel(data,text=label,font=FONTS["small_bold"],text_color=COLORS["text_muted"]).grid(row=r*2,column=c,sticky="w",padx=(14,8),pady=(10,2)); entry=ctk.CTkEntry(data,height=34,placeholder_text=placeholder); entry.grid(row=r*2+1,column=c,sticky="ew",padx=(14,8),pady=(0,10)); self.entries[label]=entry
        ctk.CTkLabel(self,text="Relato / mensaje recibido",font=FONTS["subheading"],text_color=COLORS["text"]).grid(row=3,column=0,sticky="w",padx=22,pady=(0,5))
        self.text_input=ctk.CTkTextbox(self,font=FONTS["body"],fg_color=COLORS["surface"],text_color=COLORS["text"],border_width=1,border_color=COLORS["border"]); self.text_input.grid(row=4,column=0,sticky="nsew",padx=22); self.text_input.bind("<KeyRelease>",self._count)
        footer=ctk.CTkFrame(self,fg_color="transparent"); footer.grid(row=5,column=0,sticky="ew",padx=22,pady=(8,14)); footer.grid_columnconfigure(0,weight=1)
        self.counter=ctk.CTkLabel(footer,text="0 caracteres",font=FONTS["tiny"],text_color=COLORS["text_muted"]); self.counter.grid(row=0,column=0,sticky="w")
        ctk.CTkButton(footer,text="Limpiar",width=100,height=38,fg_color=COLORS["surface_alt"],hover_color=COLORS["primary_soft"],text_color=COLORS["text"],border_width=1,border_color=COLORS["border"],command=self._on_clear).grid(row=0,column=1,padx=5)
        ctk.CTkButton(footer,text="Guardar y analizar →",width=180,height=38,fg_color=COLORS["primary"],hover_color=COLORS["primary_dark"],font=FONTS["body_bold"],command=self._on_analyze).grid(row=0,column=2,padx=(5,0))
    def _count(self,event=None): self.counter.configure(text=f"{len(self.text_input.get('1.0','end').strip())} caracteres")
    def _on_analyze(self):
        text=self.text_input.get("1.0","end").strip()
        if not text: self.counter.configure(text="Escribí el relato antes de continuar"); return
        metadata={"person_name":self.entries["Nombre / alias"].get(),"contact":self.entries["Contacto"].get(),"case_type":self.entries["Tipo de caso"].get(),"location":self.entries["Localidad / zona"].get()}
        if self.on_submit:self.on_submit(text,metadata)
    def _on_clear(self):
        for entry in self.entries.values(): entry.delete(0,"end")
        self.text_input.delete("1.0","end"); self._count()
