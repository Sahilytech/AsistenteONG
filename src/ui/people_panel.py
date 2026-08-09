"""Administración local de personas: un registro, muchos casos."""
import customtkinter as ctk
from tkinter import filedialog,messagebox
from .styles import COLORS,FONTS
from ..person_registry import PersonRegistry,PersonImporter
class PeoplePanel(ctk.CTkFrame):
 def __init__(self,parent,person_registry=None,**kwargs):
  super().__init__(parent,**kwargs);self.registry=person_registry or PersonRegistry();self._build();self.refresh()
 def _build(self):
  head=ctk.CTkFrame(self,fg_color="transparent");head.pack(fill="x",padx=24,pady=(22,10));head.grid_columnconfigure(0,weight=1)
  ctk.CTkLabel(head,text="Personas",font=FONTS["title"],text_color=COLORS["text"]).grid(row=0,column=0,sticky="w")
  ctk.CTkLabel(head,text="Un registro por persona. Los casos posteriores se agregan al mismo historial.",font=FONTS["small"],text_color=COLORS["text_muted"]).grid(row=1,column=0,sticky="w")
  ctk.CTkButton(head,text="＋ Nueva persona",width=130,height=36,command=self.new_person,fg_color=COLORS["primary"],hover_color=COLORS["primary_dark"]).grid(row=0,column=1,rowspan=2,padx=6)
  ctk.CTkButton(head,text="Importar XLSX / CSV / PDF",width=180,height=36,command=self.import_file,fg_color=COLORS["surface_alt"],hover_color=COLORS["primary_soft"],text_color=COLORS["text"],border_width=1,border_color=COLORS["border"]).grid(row=0,column=2,rowspan=2)
  self.search=ctk.CTkEntry(self,placeholder_text="Buscar por nombre, documento o contacto...",height=38);self.search.pack(fill="x",padx=24,pady=(0,10));self.search.bind("<KeyRelease>",lambda _:self.refresh())
  self.scroll=ctk.CTkScrollableFrame(self,fg_color="transparent");self.scroll.pack(fill="both",expand=True,padx=18,pady=(0,18))
 def refresh(self):
  for w in self.scroll.winfo_children():w.destroy()
  people=self.registry.list_people(self.search.get() if hasattr(self,"search") else "")
  if not people:
   ctk.CTkLabel(self.scroll,text="No hay personas registradas.",font=FONTS["heading"],text_color=COLORS["text_muted"]).pack(pady=40);return
  for p in people:
   card=ctk.CTkFrame(self.scroll,fg_color=COLORS["surface"],corner_radius=14,border_width=1,border_color=COLORS["border"]);card.pack(fill="x",padx=6,pady=5)
   ctk.CTkLabel(card,text=p["name"],font=FONTS["subheading"],text_color=COLORS["text"],anchor="w").pack(side="left",padx=16,pady=14)
   count=self.registry.case_count(p["person_id"]);meta=" · ".join(x for x in [p.get("birth_date"),p.get("document_id")] if x) or "Datos básicos disponibles"
   ctk.CTkLabel(card,text=f"{meta} · {count} caso(s)",font=FONTS["small"],text_color=COLORS["text_muted"]).pack(side="left",padx=8)
   ctk.CTkButton(card,text="Abrir historial",width=115,height=32,command=lambda x=p:self.open_person(x),fg_color=COLORS["surface_alt"],hover_color=COLORS["primary_soft"],text_color=COLORS["primary"],border_width=1,border_color=COLORS["border"]).pack(side="right",padx=12,pady=10)
 def new_person(self):self._person_dialog({})
 def _person_dialog(self,data):
  win=ctk.CTkToplevel(self);win.title("Registro de persona");win.geometry("650x700");win.transient(self.winfo_toplevel())
  box=ctk.CTkScrollableFrame(win,fg_color="transparent");box.pack(fill="both",expand=True,padx=20,pady=20)
  fields=[("name","Nombre / alias"),("document_id","Documento"),("birth_date","Fecha de nacimiento"),("age","Edad"),("sex_at_birth","Sexo asignado al nacer"),("gender_identity","Identidad de género"),("sexual_orientation","Orientación sexual"),("contact","Contacto"),("address","Domicilio"),("notes","Notas")];entries={}
  for key,label in fields:
   ctk.CTkLabel(box,text=label,font=FONTS["small_bold"],text_color=COLORS["text_muted"]).pack(anchor="w",pady=(6,2));e=ctk.CTkEntry(box,height=34);e.pack(fill="x");e.insert(0,str(data.get(key,"") or ""));entries[key]=e
  ctk.CTkLabel(box,text="Los campos sensibles son opcionales. Cargá únicamente la información necesaria para el trabajo de la organización.",font=FONTS["tiny"],text_color=COLORS["text_muted"],wraplength=570,justify="left").pack(anchor="w",pady=12)
  def save():
   try:self.registry.upsert({k:e.get() for k,e in entries.items()});win.destroy();self.refresh()
   except Exception as exc:messagebox.showerror("No se pudo guardar",str(exc))
  ctk.CTkButton(box,text="Guardar persona",height=40,command=save,fg_color=COLORS["primary"],hover_color=COLORS["primary_dark"]).pack(fill="x",pady=10)
 def open_person(self,p):
  win=ctk.CTkToplevel(self);win.title(p["name"]);win.geometry("850x700");win.transient(self.winfo_toplevel())
  box=ctk.CTkScrollableFrame(win,fg_color="transparent");box.pack(fill="both",expand=True,padx=22,pady=22)
  ctk.CTkLabel(box,text=p["name"],font=FONTS["title"],text_color=COLORS["text"]).pack(anchor="w")
  fields=[("Documento",p["document_id"]),("Nacimiento",p["birth_date"]),("Edad",p["age"]),("Sexo asignado al nacer",p["sex_at_birth"]),("Identidad de género",p["gender_identity"]),("Orientación sexual",p["sexual_orientation"]),("Contacto",p["contact"]),("Domicilio",p["address"])]
  for label,val in fields:
   if val:ctk.CTkLabel(box,text=f"{label}: {val}",font=FONTS["small"],text_color=COLORS["text_muted"]).pack(anchor="w",pady=2)
  ctk.CTkLabel(box,text=f"Historial · {self.registry.case_count(p['person_id'])} caso(s)",font=FONTS["heading"],text_color=COLORS["text"]).pack(anchor="w",pady=(22,8))
  cases=self.registry.cases(p["person_id"])
  if not cases:ctk.CTkLabel(box,text="Todavía no hay casos asociados.",font=FONTS["small"],text_color=COLORS["text_muted"]).pack(anchor="w")
  for c in cases:
   card=ctk.CTkFrame(box,fg_color=COLORS["surface"],corner_radius=12,border_width=1,border_color=COLORS["border"]);card.pack(fill="x",pady=4)
   ctk.CTkLabel(card,text=c["case_number"],font=FONTS["small_bold"],text_color=COLORS["primary"]).pack(anchor="w",padx=12,pady=(10,2));ctk.CTkLabel(card,text=f"{c['case_type'] or 'Caso'} · {c['urgency']} · {c['status']}",font=FONTS["tiny"],text_color=COLORS["text_muted"]).pack(anchor="w",padx=12);ctk.CTkLabel(card,text=c["text"].replace("\n"," ")[:220],font=FONTS["small"],text_color=COLORS["text"],wraplength=730,justify="left").pack(anchor="w",padx=12,pady=(3,10))
 def import_file(self):
  path=filedialog.askopenfilename(title="Importar registros",filetypes=[("Excel","*.xlsx"),("CSV","*.csv"),("PDF","*.pdf")])
  if not path:return
  try:
   ok,dup=PersonImporter(self.registry).import_file(path);self.refresh();messagebox.showinfo("Importación completada",f"Registros procesados: {ok}\nCoincidencias actualizadas: {dup}\n\nNo se crearon personas duplicadas cuando coincidieron documento, nombre + fecha de nacimiento o nombre único.")
  except Exception as exc:messagebox.showerror("No se pudo importar",str(exc))
