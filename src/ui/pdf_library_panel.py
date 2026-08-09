"""Interfaz completa de Biblioteca PDF."""
from __future__ import annotations
import customtkinter as ctk
from tkinter import filedialog, messagebox
from pathlib import Path
from ..knowledge.pdf_library import LIBRARY_DIR, import_pdf, list_pdfs, search_pdfs, delete_pdf, open_pdf
from ..knowledge.memory import LocalMemory
from .styles import COLORS, FONTS

class PDFLibraryPanel(ctk.CTkFrame):
    def __init__(self,parent,**kwargs):
        super().__init__(parent,**kwargs); self.memory=LocalMemory(); self._build(); self.refresh()
    def _build(self):
        top=ctk.CTkFrame(self,fg_color="transparent");top.pack(fill="x",padx=24,pady=(22,10))
        ctk.CTkLabel(top,text="Biblioteca",font=FONTS["title"],text_color=COLORS["text"]).pack(anchor="w")
        ctk.CTkLabel(top,text="Importá protocolos, guías y documentos PDF. Se procesan localmente para poder encontrarlos durante el trabajo.",font=FONTS["small"],text_color=COLORS["text_muted"],wraplength=1000,justify="left").pack(anchor="w",pady=(3,12))
        actions=ctk.CTkFrame(self,fg_color=COLORS["surface_alt"],corner_radius=12);actions.pack(fill="x",padx=24,pady=(0,10))
        ctk.CTkButton(actions,text="＋ Importar PDF",height=38,command=self.import_file,fg_color=COLORS["primary"],hover_color=COLORS["primary_dark"]).pack(side="left",padx=10,pady=10)
        ctk.CTkButton(actions,text="↻ Recargar",height=38,command=self.refresh,fg_color=COLORS["surface"],hover_color=COLORS["primary_soft"],text_color=COLORS["text"],border_width=1,border_color=COLORS["border"]).pack(side="left",pady=10)
        ctk.CTkButton(actions,text="Abrir carpeta",height=38,command=self.open_folder,fg_color=COLORS["surface"],hover_color=COLORS["primary_soft"],text_color=COLORS["text"],border_width=1,border_color=COLORS["border"]).pack(side="left",padx=8,pady=10)
        self.search=ctk.CTkEntry(actions,placeholder_text="Buscar dentro de los PDFs...",height=38);self.search.pack(side="left",fill="x",expand=True,padx=(20,8),pady=10);self.search.bind("<Return>",lambda _:self.do_search())
        ctk.CTkButton(actions,text="Buscar",height=38,width=80,command=self.do_search).pack(side="left",padx=(0,10),pady=10)
        self.status=ctk.CTkLabel(self,text="",font=FONTS["tiny"],text_color=COLORS["text_muted"]);self.status.pack(anchor="w",padx=28,pady=(0,5))
        self.scroll=ctk.CTkScrollableFrame(self,fg_color="transparent");self.scroll.pack(fill="both",expand=True,padx=18,pady=(0,18))
    def refresh(self):
        self._render(list_pdfs());self.status.configure(text="Biblioteca actualizada · procesamiento local",text_color=COLORS["text_muted"])
    def _render(self,items):
        for w in self.scroll.winfo_children():w.destroy()
        if not items:
            box=ctk.CTkFrame(self.scroll,fg_color=COLORS["surface"],corner_radius=18,border_width=1,border_color=COLORS["border"]);box.pack(fill="x",padx=8,pady=25)
            ctk.CTkLabel(box,text="Tu biblioteca está vacía",font=FONTS["heading"],text_color=COLORS["text"]).pack(anchor="w",padx=24,pady=(24,5));ctk.CTkLabel(box,text="Importá un PDF para comenzar. No hay documentos de ejemplo.",font=FONTS["body"],text_color=COLORS["text_muted"]).pack(anchor="w",padx=24,pady=(0,22));return
        for item in items:self._card(item)
    def _card(self,item):
        card=ctk.CTkFrame(self.scroll,fg_color=COLORS["surface"],corner_radius=14,border_width=1,border_color=COLORS["border"]);card.pack(fill="x",padx=6,pady=6)
        info=ctk.CTkFrame(card,fg_color="transparent");info.pack(side="left",fill="x",expand=True,padx=16,pady=13)
        ctk.CTkLabel(info,text=item["title"],font=FONTS["subheading"],text_color=COLORS["text"],anchor="w",wraplength=650,justify="left").pack(fill="x")
        state="Procesado" if item["status"]=="procesado" else ("Sin texto extraíble" if item["status"]=="sin_texto" else "Error de procesamiento")
        detail=f"{state} · {item['pages']} páginas · {item['chars']:,} caracteres";ctk.CTkLabel(info,text=detail,font=FONTS["small"],text_color=COLORS["success"] if state=="Procesado" else COLORS["text_muted"]).pack(anchor="w",pady=(3,0))
        buttons=ctk.CTkFrame(card,fg_color="transparent");buttons.pack(side="right",padx=12,pady=12)
        ctk.CTkButton(buttons,text="Abrir",width=72,height=32,command=lambda p=item["path"]:open_pdf(p),fg_color=COLORS["primary"],hover_color=COLORS["primary_dark"]).pack(side="left",padx=3)
        ctk.CTkButton(buttons,text="Ver texto",width=78,height=32,command=lambda i=item:self.view_text(i),fg_color=COLORS["surface_alt"],hover_color=COLORS["primary_soft"],text_color=COLORS["text"],border_width=1,border_color=COLORS["border"]).pack(side="left",padx=3)
        ctk.CTkButton(buttons,text="Eliminar",width=78,height=32,command=lambda p=item["path"]:self.remove(p),fg_color=COLORS["surface_alt"],hover_color="#f4dddd",text_color=COLORS["text"],border_width=1,border_color=COLORS["border"]).pack(side="left",padx=3)
    def import_file(self):
        paths=filedialog.askopenfilenames(title="Seleccionar PDFs",filetypes=[("PDF","*.pdf")])
        if not paths:return
        ok=0;errors=[]
        for path in paths:
            try:import_pdf(path,self.memory);ok+=1
            except Exception as exc:errors.append(f"{Path(path).name}: {exc}")
        self.refresh()
        if errors:messagebox.showwarning("Importación",f"Procesados: {ok}\n\n"+"\n".join(errors))
    def do_search(self):
        q=self.search.get().strip()
        if not q:self.refresh();return
        results=search_pdfs(q);items=[]
        for r in results:
            p=r["url"].replace("file://","") if r["url"].startswith("file://") else r["url"]
            items.append({"title":r["title"],"path":p,"pages":"—","chars":len(r.get("snippet", "")),"status":"procesado"})
        self._render(items);self.status.configure(text=f"Búsqueda local · {len(items)} resultado(s)")
    def view_text(self,item):
        row=self.memory.get_document(Path(item["path"]));text=row[4] if row else ""
        win=ctk.CTkToplevel(self);win.title(item["title"]);win.geometry("900x650");win.transient(self.winfo_toplevel())
        ctk.CTkLabel(win,text="Texto extraído · revisión",font=FONTS["heading"],text_color=COLORS["text"]).pack(anchor="w",padx=20,pady=(18,8))
        box=ctk.CTkTextbox(win,wrap="word");box.pack(fill="both",expand=True,padx=20,pady=(0,20));box.insert("1.0",text or "No hay texto extraíble en este documento.");box.configure(state="disabled")
    def remove(self,path):
        if not messagebox.askyesno("Eliminar documento","¿Eliminar este PDF de la biblioteca y de su índice local?"):return
        try:delete_pdf(path,self.memory);self.refresh()
        except Exception as exc:messagebox.showerror("Error",str(exc))
    def open_folder(self):
        LIBRARY_DIR.mkdir(parents=True,exist_ok=True);open_pdf(LIBRARY_DIR)
