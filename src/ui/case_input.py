"""Alta de caso con selección de una persona existente o creación automática de su registro."""
import customtkinter as ctk,logging
from ..person_registry import PersonRegistry
from .styles import COLORS,FONTS
logger=logging.getLogger(__name__)
class CaseInputFrame(ctk.CTkFrame):
 def __init__(self,parent,on_submit=None,person_registry=None,initial_person_id="",**kwargs):
  super().__init__(parent,**kwargs);self.on_submit=on_submit;self.registry=person_registry or PersonRegistry();self.people=[];self.initial_person_id=initial_person_id;self._setup_ui()
 def _setup_ui(self):
  self.grid_columnconfigure(0,weight=1);self.grid_rowconfigure(5,weight=1)
  ctk.CTkLabel(self,text="Nuevo caso",font=FONTS["title"],text_color=COLORS["text"]).grid(row=0,column=0,sticky="w",padx=22,pady=(10,2));ctk.CTkLabel(self,text="Elegí una persona existente para sumar otro caso a su historial, o dejá 'Nueva persona' para crear un registro.",font=FONTS["small"],text_color=COLORS["text_muted"],wraplength=900,justify="left").grid(row=1,column=0,sticky="w",padx=22,pady=(0,12))
  data=ctk.CTkFrame(self,fg_color=COLORS["surface"],corner_radius=14,border_width=1,border_color=COLORS["border"]);data.grid(row=2,column=0,sticky="ew",padx=22,pady=(0,10));data.grid_columnconfigure((1,3),weight=1);ctk.CTkLabel(data,text="Persona registrada",font=FONTS["small_bold"],text_color=COLORS["text_muted"]).grid(row=0,column=0,sticky="w",padx=(14,8),pady=(10,2));self.person_menu=ctk.CTkOptionMenu(data,height=34,values=["Nueva persona"],command=self._person_selected);self.person_menu.grid(row=1,column=0,columnspan=2,sticky="ew",padx=(14,8),pady=(0,10))
  fields=[("Nombre / alias","Opcional"),("Contacto","Opcional"),("Tipo de caso","Violencia, legal, social..."),("Localidad / zona","Opcional")];self.entries={}
  for i,(label,placeholder) in enumerate(fields):
   r=2+(i//2)*2;c=(i%2)*2;ctk.CTkLabel(data,text=label,font=FONTS["small_bold"],text_color=COLORS["text_muted"]).grid(row=r,column=c,sticky="w",padx=(14,8),pady=(5,2));entry=ctk.CTkEntry(data,height=34,placeholder_text=placeholder);entry.grid(row=r+1,column=c,sticky="ew",padx=(14,8),pady=(0,8));self.entries[label]=entry
  self._load_people();ctk.CTkLabel(self,text="Relato / mensaje recibido",font=FONTS["subheading"],text_color=COLORS["text"]).grid(row=3,column=0,sticky="w",padx=22,pady=(0,5));self.text_input=ctk.CTkTextbox(self,font=FONTS["body"],fg_color=COLORS["surface"],text_color=COLORS["text"],border_width=1,border_color=COLORS["border"]);self.text_input.grid(row=5,column=0,sticky="nsew",padx=22);self.text_input.bind("<KeyRelease>",self._count)
  footer=ctk.CTkFrame(self,fg_color="transparent");footer.grid(row=6,column=0,sticky="ew",padx=22,pady=(8,14));footer.grid_columnconfigure(0,weight=1);self.counter=ctk.CTkLabel(footer,text="0 caracteres",font=FONTS["tiny"],text_color=COLORS["text_muted"]);self.counter.grid(row=0,column=0,sticky="w");ctk.CTkButton(footer,text="Limpiar",width=100,height=38,fg_color=COLORS["surface_alt"],hover_color=COLORS["primary_soft"],text_color=COLORS["text"],border_width=1,border_color=COLORS["border"],command=self._on_clear).grid(row=0,column=1,padx=5);ctk.CTkButton(footer,text="Guardar y analizar →",width=180,height=38,fg_color=COLORS["primary"],hover_color=COLORS["primary_dark"],font=FONTS["body_bold"],command=self._on_analyze).grid(row=0,column=2,padx=(5,0))
 def _load_people(self):
  self.people=self.registry.list_people();labels=["Nueva persona"]+[f"{p['name']} · {p.get('document_id') or p.get('birth_date') or 'sin identificador'}" for p in self.people];self.person_menu.configure(values=labels)
  if self.initial_person_id:
   for i,p in enumerate(self.people):
    if p["person_id"]==self.initial_person_id:
     self.person_menu.set(labels[i+1]);self._person_selected(labels[i+1]);break
 def _person_selected(self,value):
  if value=="Nueva persona":return
  idx=self.person_menu.cget("values").index(value)-1
  if idx<0 or idx>=len(self.people):return
  p=self.people[idx];self.entries["Nombre / alias"].delete(0,"end");self.entries["Nombre / alias"].insert(0,p["name"]);self.entries["Contacto"].delete(0,"end");self.entries["Contacto"].insert(0,p.get("contact","") or "")
 def _count(self,event=None):self.counter.configure(text=f"{len(self.text_input.get('1.0','end').strip())} caracteres")
 def _on_analyze(self):
  text=self.text_input.get("1.0","end").strip()
  if not text:self.counter.configure(text="Escribí el relato antes de continuar");return
  selected=self.person_menu.get();person_id=""
  if selected!="Nueva persona":
   idx=self.person_menu.cget("values").index(selected)-1
   if 0<=idx<len(self.people):person_id=self.people[idx]["person_id"]
  metadata={"person_id":person_id,"person_name":self.entries["Nombre / alias"].get(),"contact":self.entries["Contacto"].get(),"case_type":self.entries["Tipo de caso"].get(),"location":self.entries["Localidad / zona"].get()}
  if self.on_submit:self.on_submit(text,metadata)
 def _on_clear(self):
  self.person_menu.set("Nueva persona")
  for entry in self.entries.values():entry.delete(0,"end")
  self.text_input.delete("1.0","end");self._count()
